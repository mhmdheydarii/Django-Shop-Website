from django.db import models
from accounts.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from shop.models import ProductModel
from payment.models import PaymentModel
# Create your models here.

class StatusTypeModel(models.IntegerChoices):
    pending = 1, "در انتظار پرداخت"
    success = 2, "پرداخت شده"
    failed = 3, "لغو شده"


class UserAddressModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    address = models.CharField(max_length=300)
    state = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    zip_code = models.CharField(max_length=50)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


class CouponModel(models.Model):
    code = models.CharField(max_length=100)
    discount_percent = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_limit_usage = models.PositiveIntegerField(default=0)
    used_by = models.ManyToManyField(User, related_name="coupon_users", blank=True)

    expiering_date = models.DateTimeField(default = timezone.now(),null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code
    
    class Meta:
        ordering = ["-created_date"]

class OrderModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    address = models.CharField(max_length=300)
    state = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    zip_code = models.CharField(max_length=50)

    payment = models.ForeignKey(PaymentModel, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    coupon = models.ForeignKey(CouponModel, on_delete=models.PROTECT, null=True, blank=True)

    status = models.IntegerField(choices=StatusTypeModel.choices, default=StatusTypeModel.pending.value)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
    
    class Meta:
        ordering = ["-created_date"]
        
    def calcolate_total_price(self):
        return sum(item.price * item.quantity for item in self.order_items.all())
    
    def get_status(self):
        return {
            "id":self.status,
            "title":StatusTypeModel(self.status).name,
            "label":StatusTypeModel(self.status).label,
        }

class OrderItemModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(ProductModel, on_delete=models.PROTECT)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    quantity = models.PositiveIntegerField(default=0)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.id} - {self.order.id}"


