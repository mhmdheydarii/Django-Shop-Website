from django.urls import path
from . import views

app_name = "customer"

urlpatterns = [
    # Profile pages
    path("home/", views.CustomerDashboardView.as_view(), name="home"),
    path("profile/security/edit/", views.CustomerSecurityEditView.as_view(), name="security-edit"),
    path("profile/edit/", views.CustomerProfileEditView.as_view(), name="profile-edit"),
    path("profile/edit/image/", views.CustomerProfileEditImageView.as_view(), name="profile-edit-image"),

    # Address pages
    path("address/list/", views.CustomerAddressListView.as_view(), name="address-list"),
    path("address/create/", views.CustomerAddressCreateView.as_view(), name="address-create"),
    path("address/<int:pk>/edit/", views.CustomerAddressEditView.as_view(), name="address-edit"),
    path("address/<int:pk>/delete/", views.CustomerAddressDeleteView.as_view(), name="address-delete"),

    # Order pages
    path("order/list/", views.CustomerOrderListView.as_view(), name="order-list"),
    path("order/<int:pk>/detail/", views.CustomerOrderDetailView.as_view(), name="order-detail"),
]