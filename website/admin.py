from django.contrib import admin
from .models import Contact, NewsLetter

# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_display = ("last_name", "created_date", "is_seen")
    list_filter = ("is_seen",)
    searching_fields = ("phone_number")

admin.site.register(Contact, ContactAdmin)

class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ("email", "created_date")

admin.site.register(NewsLetter, NewsLetterAdmin)