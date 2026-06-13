from django.shortcuts import render, redirect
from django.views.generic import TemplateView, UpdateView, ListView, DeleteView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_view
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import FieldError
from dashboard.permissions import HasAdminPermission
from dashboard.admin.forms import (
    AdminPasswordChangeForm,
    AdminProfileEditForm, 
    AdminProfileImageEditForm,
    AdminProductEditForm, 
    AdminProductCreateForm,
    AdminCategoryCreateForm,
    AdminAddImageForm,
    CouponForm,
    ReviewForm
)
from accounts.models import Profile
from shop.models import ProductModel, ProductStatusType, ProductCategoryModel, ProductImageModel
from order.models import CouponModel, OrderModel, OrderItemModel, StatusTypeModel
from review.models import ReviewModel, ReviewTypeModel
# Create your views here.


class AdminDashboardView(LoginRequiredMixin, HasAdminPermission, TemplateView):
    template_name = "dashboard/admin/home.html"


class AdminSecurityEditView(LoginRequiredMixin, HasAdminPermission, SuccessMessageMixin, auth_view.PasswordChangeView):

    template_name = "dashboard/admin/profile/security-edit.html"
    form_class = AdminPasswordChangeForm
    success_url = reverse_lazy("dashboard:admin:security-edit")
    success_message = "رمز عبور با موفقیت تغییر کرد"


class AdminProfileEditView(LoginRequiredMixin, HasAdminPermission, SuccessMessageMixin, UpdateView):

    template_name = "dashboard/admin/profile/profile-edit.html"
    form_class = AdminProfileEditForm
    success_url = reverse_lazy("dashboard:admin:profile-edit")
    success_message = "اطلاعات شما با موفقیت تغییر کرد"

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)


class AdminProfileImageEditView(LoginRequiredMixin, HasAdminPermission, SuccessMessageMixin, UpdateView):

    http_method_names = ["post"]
    
    form_class = AdminProfileImageEditForm
    success_url = reverse_lazy("dashboard:admin:profile-edit")
    success_message = "تصویر پروفایل شما با موفقیت ویرایش شد."

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

    def form_invalid(self):
        messages.error(self.request, "مشکلی در اپلود تصویر بوجود امد")
        return redirect(self.success_url)
    

class AdminProductListView(LoginRequiredMixin, HasAdminPermission, ListView):

    template_name = "dashboard/admin/product/product-list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = ProductModel.objects.all()

        if search_q:= self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
        if category_id:=self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)
        if order_by:=self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ProductCategoryModel.objects.all()
        return context
    

class AdminProductEditView(LoginRequiredMixin, HasAdminPermission, SuccessMessageMixin,UpdateView):
    template_name = "dashboard/admin/product/product-edit.html"
    queryset = ProductModel.objects.all()
    form_class = AdminProductEditForm
    success_message = "محصول با موفقیت ویرایش شد"

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:product-edit", kwargs={"pk":self.get_object().pk})
    

class AdminProductDeleteView(LoginRequiredMixin, HasAdminPermission, SuccessMessageMixin, DeleteView):
    template_name = "dashboard/admin/product/product-delete.html"
    queryset = ProductModel.objects.all()
    success_message = "محصول با موفقیت حذف شد"
    success_url = reverse_lazy("dashboard:admin:product-list")

class AdminProductCreateView(LoginRequiredMixin, HasAdminPermission, SuccessMessageMixin, CreateView):
    template_name = "dashboard/admin/product/product-create.html"
    queryset = ProductModel.objects.all()
    form_class = AdminProductCreateForm
    success_url = reverse_lazy("dashboard:admin:product-list")
    success_message = "محصول با موفقیت ایجاد شد"

    def form_valid(self, form):
        form.instance.user = self.request.user
        
        return super().form_valid(form)
    

class AdminCategoryCreateView(LoginRequiredMixin, HasAdminPermission, SuccessMessageMixin, CreateView):
    template_name = "dashboard/admin/product/category-create.html"
    queryset = ProductCategoryModel.objects.all()
    form_class = AdminCategoryCreateForm
    success_url = reverse_lazy("dashboard:admin:product-list")
    success_message = "دسته بندی با موفقیت ساخته شد"


class AdminAddImageView(LoginRequiredMixin, HasAdminPermission, SuccessMessageMixin, CreateView):
    template_name = "dashboard/admin/product/add-image.html"
    queryset = ProductImageModel.objects.all()
    form_class = AdminAddImageForm
    success_url = reverse_lazy("dashboard:admin:product-list")
    success_message = "تصویر با موفقیت برای محصول مورد نظر ایجاد شد"


class AdminCouponListView(LoginRequiredMixin, HasAdminPermission, ListView):
    template_name = "dashboard/admin/coupon/coupon-list.html"
    
    def get_queryset(self):
        queryset = CouponModel.objects.all()
        
        if search_q:= self.request.GET.get("q"):
            queryset = queryset.filter(code__icontains=search_q)
        if order_by:= self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset


class AdminCouponEditView(LoginRequiredMixin, HasAdminPermission, SuccessMessageMixin, UpdateView):
    template_name = "dashboard/admin/coupon/coupon-edit.html"
    queryset = CouponModel.objects.all()
    form_class = CouponForm
    success_message = "کد تخفیف با موفقیت اپدیت شد"
    
    def get_success_url(self):
        return reverse_lazy("dashboard:admin:coupon-edit", kwargs={"pk":self.get_object().pk})
    


class AdminCouponCreateView(LoginRequiredMixin, HasAdminPermission, SuccessMessageMixin, CreateView):
    template_name = "dashboard/admin/coupon/coupon-create.html"
    queryset = CouponModel.objects.all()
    form_class = CouponForm
    success_url = reverse_lazy("dashboard:admin:coupon-list")
    success_message = "کد تخفیف ایجاد شد"


class AdminOrderListView(LoginRequiredMixin, HasAdminPermission, ListView):
    template_name = "dashboard/admin/orders/order-list.html"
    paginate_by = 10
    
    def get_queryset(self):
        queryset = OrderModel.objects.all()

        if search_q:= self.request.GET.get("q"):
            queryset = queryset.filter(user__email=search_q)
        if status:= self.request.GET.get("status"):
            queryset = queryset.filter(status=status)
        if order_by := self.request.GET.get("order_by"):
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
    
class AdminOrderDetailView(LoginRequiredMixin, HasAdminPermission, DetailView):
    template_name = "dashboard/admin/orders/order-detail.html"
    queryset = OrderModel.objects.all()

    

class AdminReviewListView(LoginRequiredMixin, HasAdminPermission, ListView):
    template_name = "dashboard/admin/review/review-list.html"
    paginate_by = 30

    def get_queryset(self):
        queryset = ReviewModel.objects.all()

        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(product__title=search_q)
        if status := self.request.GET.get("status"):
            queryset = queryset.filter(status=status)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_comments"] = self.get_queryset().count()
        return context
    
class AdminReviewEditView(LoginRequiredMixin, HasAdminPermission, SuccessMessageMixin, UpdateView):
    template_name = "dashboard/admin/review/review-edit.html"
    queryset = ReviewModel.objects.all()
    form_class = ReviewForm

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:review-edit",kwargs={"pk":self.get_object().pk})