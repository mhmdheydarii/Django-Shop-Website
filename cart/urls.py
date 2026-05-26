from django.urls import path, re_path
from . import views

app_name = "cart"

urlpatterns = [
    path("session/add-product/", views.AddProductItem.as_view(), name="session-add-product"),
    path("session/update-product-quantity/", views.UpdateProductQuantity.as_view(), name="session-update-product-quantity"),
    path("session/remove-product/", views.RemoveProductQuantity.as_view(), name="session-remove-product"),
    path("summary/", views.CartSummary.as_view(), name="cart-summary")
]