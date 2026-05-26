from shop.models import ProductModel, ProductStatusType
from .models import Cart, CartItem

class CartSession:

    def __init__(self, session):
        self.session = session
        self._cart = self.session.get(
            "cart",
            {
                "items": [],
            },
        )

        self.session["cart"] = self._cart

    def add_product(self, product_id, quantity):

        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                if quantity > item["quantity"]:
                    item["quantity"] += 1
                    break
                else:
                    return False
        else:
            new_item = {
                "product_id": product_id,
                "quantity": 1,
            }
            self._cart["items"].append(new_item)
        self.save()

    def update_product_quantity(self, product_id, quantity):
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                item["quantity"] = int(quantity)
                break
        else:
            return
        self.save()


    def remove_product(self, product_id):
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                self._cart["items"].remove(item)
                break
        else:
            return
        self.save()


    def clear(self):
        self._cart = self.session["cart"] = {"items": []}
        self.save()


    def get_cart_dict(self):
        return self._cart

    def get_cart_items(self):
        cart_items = self._cart["items"]
        for item in cart_items:
            product_obj = ProductModel.objects.get(
                id=item["product_id"], status=ProductStatusType.publish.value
            )
            item["product_obj"] = {
                "id": product_obj.id,
                "title": product_obj.title,
                "image": product_obj.image.url,
                "category": product_obj.category.title,
                "stock": product_obj.stock,
                "slug": product_obj.slug,
                "price": int(product_obj.get_price()),
            }
            item.update(
                {
                    "product_obj": item["product_obj"],
                    "total_price": item["quantity"] * product_obj.get_price(),
                }
            )
        return cart_items

    def get_total_payment_amount(self):
        return sum(item["total_price"] for item in self._cart["items"])

    def get_total_quantity(self):
        return sum(item["quantity"] for item in self._cart["items"])

    def save(self):
        self.session.modified = True
        

    def sync_cart_item_from_db(self, user):
        cart, created = Cart.objects.get_or_create(user=user)
        cart_items = CartItem.objects.filter(cart=cart)

        for cart_item in cart_items:
            for item in self._cart["items"]:
                if str(cart_item.product.id) == item["product_id"]:
                    cart_item.quantity = item["quantity"]
            else:
                new_item = {"product_id":str(cart_item.product.id), "quantity":cart_item.quantity}
                self._cart["items"].append(new_item)
        self.merge_session_cart_in_db(user)
        self.save()

    def merge_session_cart_in_db(self, user):
        cart, created = Cart.objects.get_or_create(user=user)
        
        for item in self._cart["items"]:
            product_obj = ProductModel.objects.get(id=item["product_id"], status=ProductStatusType.publish.value)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product_obj)
            cart_item.quantity = item["quantity"]
            cart_item.save()
        session_product_ids = (item["product_id"] for item in self._cart["items"])
        CartItem.objects.filter(cart=cart).exclude(product__id__in=session_product_ids).delete()