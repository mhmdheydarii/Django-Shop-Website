from django.shortcuts import render, redirect
from django.views.generic import TemplateView, UpdateView, ListView, CreateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_view
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from dashboard.permissions import HasCustomerPermission
from dashboard.customer.forms import (
    CustomerPasswordChangeForm,
    CustomerProfileEditForm, 
    CustomerProfileEditImageForm,
    CustomerAddressForm
    )
from django.core.exceptions import FieldError
from accounts.models import Profile
from order.models import UserAddressModel, OrderModel, StatusTypeModel
from shop.models import ProductWishListModel

# Create your views here.


class CustomerDashboardView(LoginRequiredMixin, HasCustomerPermission, TemplateView):
    template_name = "dashboard/customer/home.html"


class CustomerSecurityEditView(LoginRequiredMixin, HasCustomerPermission, SuccessMessageMixin,auth_view.PasswordChangeView):

    form_class = CustomerPasswordChangeForm
    success_url = reverse_lazy("dashboard:customer:security-edit")
    template_name = "dashboard/customer/profile/security-edit.html"
    success_message = "پسوورد شما با موفقیت تغییر کرد"


class CustomerProfileEditView(LoginRequiredMixin, HasCustomerPermission, SuccessMessageMixin, UpdateView):

    form_class = CustomerProfileEditForm
    success_url = reverse_lazy("dashboard:customer:profile-edit")
    template_name = "dashboard/customer/profile/profile-edit.html"
    success_message = "اطلاعات شما با موفقیت تعییر کرد"

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)
    
    def form_invalid(self, form):
        messages.error(self.request, "مشکلی در ویرایش فیلد ها بوجود امد. لطفا دوباره تلاش کنید")
        return redirect(self.success_url)


class CustomerProfileEditImageView(LoginRequiredMixin, HasCustomerPermission, SuccessMessageMixin, UpdateView):

    http_method_names = ["post"]
    form_class = CustomerProfileEditImageForm
    success_url = reverse_lazy("dashboard:customer:profile-edit")
    success_message = "تصویر پروفایل شما با موفقیت تغییر کرد"

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)
    
    def form_invalid(self, form):
        messages.error(self.request, "مشکلی در ارسال تصویر بوجود امد. لطفا دوباره تلاش کنید")
        return redirect(self.success_url)
    

class CustomerAddressListView(LoginRequiredMixin, HasCustomerPermission, SuccessMessageMixin, ListView):
    template_name = "dashboard/customer/address/address-list.html"
    
    def get_queryset(self):
        return UserAddressModel.objects.filter(user=self.request.user)
    

class CustomerAddressCreateView(LoginRequiredMixin, HasCustomerPermission, SuccessMessageMixin, CreateView):
    template_name = "dashboard/customer/address/address-create.html"
    form_class = CustomerAddressForm
    success_message = "آدرس با موفقت ایجاد شد"
    success_url = reverse_lazy("dashboard:customer:address-list")
    
    def get_queryset(self):
        return UserAddressModel.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class CustomerAddressEditView(LoginRequiredMixin, HasCustomerPermission, SuccessMessageMixin, UpdateView):
    template_name = "dashboard/customer/address/address-edit.html"
    form_class = CustomerAddressForm
    success_message = "آدرس با موفقیت ادیت شد"
    queryset = UserAddressModel.objects.all()
    
    def get_success_url(self):
        return reverse_lazy("dashboard:customer:address-edit", kwargs={"pk":self.get_object().pk})
    

class CustomerAddressDeleteView(LoginRequiredMixin, HasCustomerPermission, SuccessMessageMixin, DeleteView):
    template_name = "dashboard/customer/address/address-delete.html"
    success_message = "آدرس با موفقیت حذف شد"
    queryset = UserAddressModel.objects.all()
    success_url = reverse_lazy("dashboard:customer:address-list")
    
    
class CustomerOrderListView(LoginRequiredMixin, HasCustomerPermission, ListView):
    template_name = "dashboard/customer/orders/order-list.html"
    
    def get_queryset(self):
        queryset = OrderModel.objects.all()

        if search_q:=self.request.GET.get("q"):
            queryset = queryset.filter(id__in=search_q)
        if status:= self.request.GET.get("status"):
            queryset = queryset.filter(status=status)
        if order_by:= self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_items"] = self.get_queryset().count()
        context["status_types"] = StatusTypeModel.choices
        return context


class CustomerOrderDetailView(LoginRequiredMixin, HasCustomerPermission, DetailView):
    template_name = "dashboard/customer/orders/order-detail.html"
    
    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user)
    

class CustomerWishListView(LoginRequiredMixin, HasCustomerPermission, ListView):
    template_name = "dashboard/customer/wishlist/wishlist-list.html"
    paginate_by = 9

    def get_queryset(self):
        queryset = ProductWishListModel.objects.all()
        if search_q:= self.request.GET.get("q"):
            queryset = queryset.filter(product__title__icontains=search_q)
        if order_by:= self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_items"] = self.get_queryset().count()
        return context
    
class CustomerWishListDeleteView(LoginRequiredMixin, HasCustomerPermission, SuccessMessageMixin, DeleteView):
    http_method_names = ["post"]
    queryset = ProductWishListModel.objects.all()
    success_url = reverse_lazy("dashboard:customer:wishlist-list")
    success_message = "محصول با موفقیت از لیست شما حذف شد"