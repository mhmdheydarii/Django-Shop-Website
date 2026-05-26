from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from .cart import CartSession
from shop.models import ProductModel
from .models import Cart

# Create your views here.


class AddProductItem(View):

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        product = ProductModel.objects.get(id=product_id)
        product_stock = product.stock
        if product_id and product_stock:
            cart.add_product(product_id, product_stock)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)
        return JsonResponse({"total_quantity": cart.get_total_quantity()})


class UpdateProductQuantity(View):

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")
        if product_id and quantity:
            cart.update_product_quantity(product_id, quantity)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)
        return JsonResponse({"total_quantity": cart.get_total_quantity()})


class RemoveProductQuantity(View):
    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        if product_id:
            cart.remove_product(product_id)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)
        return JsonResponse({"total_quantity": cart.get_total_quantity()})


class CartSummary(TemplateView):
    template_name = "cart/cart-summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = CartSession(self.request.session)
        context["cart_items"] = cart.get_cart_items()
        context["total_quantity"] = cart.get_total_quantity()
        context["total_payment_price"] = cart.get_total_payment_amount()
        return context
