from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from accounts.models import User
from shop.models import ProductModel
# Create your models here.
class ReviewTypeModel(models.IntegerChoices):
    pending = 1, "در انتظار تایید"
    accepted = 2, "تایید شده"
    rejected = 3, "رد شده"

class ReviewModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    description = models.TextField()
    rate = models.IntegerField(
        default=5, validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    status = models.IntegerField(choices=ReviewTypeModel.choices, default=ReviewTypeModel.pending.value)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField()


    def __str__(self):
        return self.user.email
    
    class Meta:
        ordering = ["-created_date"]


@receiver(post_save, sender=ReviewModel)
def create_profile(sender,instance,created,**kwargs):
    pass