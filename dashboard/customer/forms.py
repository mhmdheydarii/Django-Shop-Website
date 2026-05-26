from django.contrib.auth import forms as auth_forms
from django import forms
from accounts.models import Profile
from order.models import UserAddressModel


class CustomerPasswordChangeForm(auth_forms.PasswordChangeForm):

    error_messages = {
        "password_incorrect":
            "پسوورد قدیمی شما اشتباه است لطفا به درستی وارد کنید",
        "password_mismatch":
            "دو پسوورد جدید شماا مطابقت ندارند"
    }

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields["old_password"].widget.attrs["class"] = "form-control text-center"
        self.fields["new_password1"].widget.attrs["class"] = "form-control text-center"
        self.fields["new_password2"].widget.attrs["class"] = "form-control text-center"
        self.fields["old_password"].widget.attrs["placeholder"] = "پسوورد فعلی را وارد کنید"
        self.fields["new_password1"].widget.attrs["placeholder"] = "پسورد جدید را وارد کنید"
        self.fields["new_password2"].widget.attrs["placeholder"] = "پسورد جدید را تکرار کنید"

class CustomerProfileEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "phone_number"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["class"] = "form-control text-center"
        self.fields["last_name"].widget.attrs["class"] = "form-control text-center"
        self.fields["phone_number"].widget.attrs["class"] = "form-control text-center"


class CustomerProfileEditImageForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            "image"
        ]


class CustomerAddressForm(forms.ModelForm):

    class Meta:
        model = UserAddressModel
        fields = [
            "address",
            "state",
            "city",
            "zip_code",
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["address"].widget.attrs["class"] = "form-control text-center"
        self.fields["state"].widget.attrs["class"] = "form-control text-center"
        self.fields["city"].widget.attrs["class"] = "form-control text-center"
        self.fields["zip_code"].widget.attrs["class"] = "form-control text-center"