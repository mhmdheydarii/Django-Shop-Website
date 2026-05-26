from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal
from accounts.models import User

# Create your models here.


class ProductStatusType(models.IntegerChoices):
    publish = 1, ("نمایش")
    draft = 2, ("عدم نمایش")


class ProductCategoryModel(models.Model):
    title = models.CharField()
    slug = models.SlugField(allow_unicode=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ProductModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    category = models.ForeignKey(
        ProductCategoryModel, on_delete=models.SET_NULL, null=True
    )
    slug = models.SlugField(allow_unicode=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    brief_description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="Products/image")
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    discount_percent = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    status = models.IntegerField(
        choices=ProductStatusType.choices, default=ProductStatusType.publish.value
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_date"]

    def get_price(self):
        discount_amount = (self.price * Decimal(self.discount_percent)) / Decimal(100)
        discounted_price = self.price - discount_amount
        return int(discounted_price)

    def is_discounted(self):
        return self.discount_percent != 0

    def is_published(self):
        return self.status == ProductStatusType.publish.value


class ProductImageModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    file = models.ImageField(upload_to="Products/extra-image")

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
