from django.views.generic import FormView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from decimal import Decimal
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import redirect
from .permissions import HasCustomerPermission
from .models import UserAddressModel, OrderModel, OrderItemModel, CouponModel
from cart.models import Cart
from .forms import CheckoutForm
from cart.models import Cart, CartItem
from cart.cart import CartSession
from payment.zarinpall_client import ZarinPalSandbox
from payment.models import PaymentModel


class OrderCheckoutView(HasCustomerPermission, LoginRequiredMixin, FormView):
    template_name = "order/checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("order:completed")

    def get_form_kwargs(self):
        kwargs = super(OrderCheckoutView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        cleaned_data = form.cleaned_data
        address = cleaned_data["address_id"]
        coupon = cleaned_data["coupon"]

        cart = Cart.objects.get(user=user)
        order = self.create_order(address)

        self.create_order_items(order, cart)
        self.clear_cart(cart)

        total_price = order.calcolate_total_price()
        self.apply_coupon(coupon, order, user, total_price)
        order.save()
        return redirect(self.create_payment_url(order))

    def create_payment_url(self, order):
        zarinpal = ZarinPalSandbox()
        response = zarinpal.payment_request(order.total_price)

        authority = response.get("data", {}).get("authority")
        if not authority:
            error_msg = response.get("errors", {}).get("message", "خطای ناشناخته")
            # یا redirect به صفحه خطا یا raise
            raise Exception(f"خطا از زرین‌پال: {error_msg}")
        
        payment_obj = PaymentModel.objects.create(
            authority_id=authority,
            amount=order.total_price
        )
        order.payment = payment_obj
        order.save()
        return zarinpal.generate_payment_url(authority)

    def create_order(self, address):
        return OrderModel.objects.create(
            user=self.request.user,
            address=address.address,
            state=address.state,
            city=address.city,
            zip_code=address.zip_code,
        )

    def create_order_items(self, order, cart):
        for item in cart.cart_items.all():
            OrderItemModel.objects.create(
                order=order,
                product=item.product,
                price=item.product.get_price(),
                quantity=item.quantity,
            )

    def clear_cart(self, cart):
        cart.cart_items.all().delete()
        CartSession(self.request.session).clear()

    def apply_coupon(self, coupon, order, user, total_price):
        if coupon:
            discoun_amount = round(
                (total_price * Decimal(coupon.discount_percent / 100))
            )
            total_price -= discoun_amount

            order.coupon = coupon
            coupon.used_by.add(user)
            coupon.save()
        order.total_price = total_price
        order.save()

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.get(user=self.request.user)
        context["addresses"] = UserAddressModel.objects.filter(user=self.request.user)
        total_price = cart.calcolate_total_price()
        context["total_price"] = total_price
        return context


class OrderCompletedView(HasCustomerPermission, LoginRequiredMixin, TemplateView):
    template_name = "order/completed.html"
    
class OrderFaileddView(HasCustomerPermission, LoginRequiredMixin, TemplateView):
    template_name = "order/failed.html"
    


class ValidateCouponView(HasCustomerPermission, LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        code = request.POST.get("coupon")
        user = self.request.user

        status_code = 200
        message = "کد تخفیف با موفقیت اعمال شد"
        total_price = 0

        try:
            coupon = CouponModel.objects.get(code=code)
        except CouponModel.DoesNotExist:
            return JsonResponse({"message": "کد تخفیف وجود ندارد"}, status=404)

        else:
            if coupon.used_by.count() >= coupon.max_limit_usage:
                status_code, message = 403, "کد تخفیف به پایان رسیده"

            if coupon.expiering_date and coupon.expiering_date < timezone.now():
                status_code, message = 403, "کد تخفیف منقضی شده است"

            if user in coupon.used_by.all():
                (status_code, message,) = (403, "کد تخفیف توسط شما استفاده شده است")

            else:
                cart = Cart.objects.get(user=self.request.user)
                total_price = cart.calcolate_total_price()
                total_price = total_price - round( total_price * (coupon.discount_percent / 100))

        return JsonResponse(
            {
                "message": message,
                "total_price": total_price,
            },
            status=status_code,
        )
