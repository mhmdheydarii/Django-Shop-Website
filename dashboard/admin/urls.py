from django.urls import path, re_path
from . import views

app_name = "admin"

urlpatterns = [
    path("home/", views.AdminDashboardView.as_view(), name="home"),
    # Profile pages
    path("profile/security/edit/", views.AdminSecurityEditView.as_view(), name="security-edit"),
    path("profile/edit/", views.AdminProfileEditView.as_view(), name="profile-edit"),
    path("profile/image/edit/", views.AdminProfileImageEditView.as_view(), name="profile-image-edit"),

    # Product pages
    path("product/list/", views.AdminProductListView.as_view(), name="product-list"),
    path("product/<int:pk>/edit/", views.AdminProductEditView.as_view(), name="product-edit"),
    path("product/<int:pk>/delete/", views.AdminProductDeleteView.as_view(), name="product-delete"),
    path("product/create/", views.AdminProductCreateView.as_view(), name="product-create"),
    path("category/create/", views.AdminCategoryCreateView.as_view(), name="category-create"),
    path("add/image/", views.AdminAddImageView.as_view(), name="add-image"),

    # Coupon pages
    path("coupon/list/", views.AdminCouponListView.as_view(), name="coupon-list"),
    path("coupon/<int:pk>/edit/", views.AdminCouponEditView.as_view(), name="coupon-edit"),
    path("coupon/create/", views.AdminCouponCreateView.as_view(), name="coupon-create"),

    # Order pages
    path("order/list/", views.AdminOrderListView.as_view(), name="order-list"),
    path("order/<int:pk>/detail/", views.AdminOrderDetailView.as_view(), name="order-detail"),
]
