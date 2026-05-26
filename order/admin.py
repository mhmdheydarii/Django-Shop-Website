from django.contrib import admin
from .models import UserAddressModel, CouponModel, OrderModel, OrderItemModel


# Register your models here.
@admin.register(UserAddressModel)
class UserAddressModelAdmin(admin.ModelAdmin):
    list_display = ["user", "state", "city"]
    search_fields = ["city"]


@admin.register(CouponModel)
class CouponModelAdmin(admin.ModelAdmin):
    list_display = ["code", 
                    "discount_percent", 
                    "max_limit_usage",
                    "used_by_count", 
                    "expiering_date"]
    search_fields = ["coupon"]

    def used_by_count(self, obj):
        return obj.used_by.all().count()
    



@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ["id" ,
                    "user", 
                    "state", 
                    "city", 
                    "status", 
                    "created_date"]
    
    list_filter = ["coupon"]
    search_fields = ["state"]


@admin.register(OrderItemModel)
class OrderItemModelAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "quantity"]



