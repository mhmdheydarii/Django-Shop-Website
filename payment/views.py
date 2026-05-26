from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import PaymentModel, PaymentStatusType
from .zarinpall_client import ZarinPalSandbox
from order.models import StatusTypeModel, OrderModel
# Create your views here.

class PaymentVerifyView(View):

    def get(self, request, *args, **kwargs):
        authority_id = request.GET.get("Authority")
        status = request.GET.get("Status")
        payment_obj = get_object_or_404(PaymentModel, authority_id=authority_id)
        order = OrderModel.objects.get(payment=payment_obj)
        zarinpal = ZarinPalSandbox()
        response = zarinpal.payment_verify(int(payment_obj.amount), payment_obj.authority_id)
        if response["Status"] == 100 or response["Status"] == 101:
            payment_obj.ref_id = response["RefID"]
            payment_obj.response_code = response["Status"]
            payment_obj.status = PaymentStatusType.success.value
            payment_obj.response_json = response
            payment_obj.save()
            order.status = StatusTypeModel.success.value
            order.save()
            return render(reverse_lazy("order:completed"))
        else:
            payment_obj.ref_id = response["RefID"]
            payment_obj.response_code = response["Status"]
            payment_obj.status = PaymentStatusType.failed.value
            payment_obj.response_json = response
            order.status = StatusTypeModel.failed.value
            order.save()
            return render(reverse_lazy("order:failed"))
    