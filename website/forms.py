from django import forms
from .models import Contact, NewsLetter


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "email", "phone_number", "message"]

    error_messages = {
        "email": {"required": "فیلد ایمیل نمی تواند خالی باشد"},
        "content": {
            "required": "فیلد محتوا نمی تواند خالی باشد",
            "min_length": "طول محتوای وارد شده غیر مجاز است",
        },
        "subject": {"required": "فیلد  عنوان نمی تواند خالی باشد"},
        "full_name": {"required": "فیلد نام و نام خانوادگی نمی تواند خالی باشد"},
    }


class NewsLetterForm(forms.ModelForm):

    class Meta:
        model = NewsLetter
        fields = ["email"]
