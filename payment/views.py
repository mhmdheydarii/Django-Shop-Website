from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.urls import reverse_lazy
from .models import PaymentModel, PaymentStatusType
from .zarinpall_client import ZarinPalSandbox
from order.models import StatusTypeModel, OrderModel
from shop.models import ProductModel
# Create your views here.


class PaymentVerifyView(View):

    def get(self, request, *args, **kwargs):
        authority_id = request.GET.get("Authority")
        payment_obj = get_object_or_404(PaymentModel, authority_id=authority_id)
        order = OrderModel.objects.get(payment=payment_obj)
        zarinpal = ZarinPalSandbox()
        response = zarinpal.payment_verify(
            int(payment_obj.amount), payment_obj.authority_id
        )

        data = response.get('data', {})

        if data.get("code") in [100, 101]:

            if payment_obj.status == PaymentStatusType.success.value:
                return render(request, "order/completed.html")

            with transaction.atomic():

                for item in order.order_items.all():

                    product = ProductModel.objects.select_for_update().get(
                        id=item.product.id
                    )

                    if product.stock < item.quantity:
                        return render(request, "order/failed.html")

                    product.stock -= item.quantity
                    product.save()

            payment_obj.ref_id = data.get("ref_id")
            payment_obj.response_code = data.get("code")
            payment_obj.status = PaymentStatusType.success.value
            payment_obj.response_json = response
            payment_obj.save()

            order.status = StatusTypeModel.success.value
            order.save()

            return render(request, "order/completed.html")
        else:
            payment_obj.ref_id = data.get("ref_id")
            payment_obj.response_code = data.get("code")
            payment_obj.status = PaymentStatusType.failed.value
            payment_obj.response_json = response
            payment_obj.save()

            order.status = StatusTypeModel.failed.value
            order.save()

            return render(request, "order/failed.html")
