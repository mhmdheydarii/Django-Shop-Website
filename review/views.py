from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import ReviewModel
from .forms import SubmitReviewForm
# Create your views here.

class SubmitReviewView(LoginRequiredMixin, CreateView):

    http_method_names = ["post"]
    model = ReviewModel
    form_class = SubmitReviewForm

    def form_valid(self, form):
        product = form.cleaned_data["product"]
        messages.success(self.request, "دیدگاه شما با موفقیت ثبت شد و در انتظار تایید است")
        return redirect(reverse_lazy("shop:product-detail", kwargs={"slug":product.slug}))
    
    def form_invalid(self, form):
        messages.error(self.request, "خطایی در ثبت دیدگاه اتفاق افتاد")

        return redirect(self.request.META.get('HTTP_REFERER'))
    
    def get_queryset(self):
        return ReviewModel.objects.filter(user=self.request.user)