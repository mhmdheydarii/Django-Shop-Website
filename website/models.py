from django.db import models
from accounts.validators import validate_iranian_cellphone_number

# Create your models here.


class Contact(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=12, validators=[validate_iranian_cellphone_number]
    )
    message = models.TextField()
    is_seen = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name

    class Meta:
        ordering = ["-created_date"]


class NewsLetter(models.Model):
    email = models.EmailField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
