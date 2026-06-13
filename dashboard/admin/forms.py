from django.contrib.auth import forms as auth_form
from django import forms
from accounts.models import Profile
from shop.models import ProductModel, ProductCategoryModel, ProductImageModel
from order.models import CouponModel
from review.models import ReviewModel

class AdminPasswordChangeForm(auth_form.PasswordChangeForm):

    error_messages = {
        "password_incorrect": "پسوورد قدیمی شما اشتباه است . لطفا به درستی وارد کنید",
        "password_mismatch": "پسووردهای جدید یکسان نیستند",
    }

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields["old_password"].widget.attrs["class"] = "form-control text-center"
        self.fields["new_password1"].widget.attrs["class"] = "form-control text-center"
        self.fields["new_password2"].widget.attrs["class"] = "form-control text-center"
        self.fields["old_password"].widget.attrs[
            "placeholder"
        ] = "پسوورد فعلی را وارد کنید"
        self.fields["new_password1"].widget.attrs[
            "placeholder"
        ] = "پسورد جدید را وارد کنید"
        self.fields["new_password2"].widget.attrs[
            "placeholder"
        ] = "پسورد جدید را تکرار کنید"


class AdminProfileEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "phone_number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["class"] = "form-control text-center"
        self.fields["last_name"].widget.attrs["class"] = "form-control text-center"
        self.fields["phone_number"].widget.attrs["class"] = "form-control text-center"


class AdminProfileImageEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ["image"]


class AdminProductEditForm(forms.ModelForm):

    class Meta:
        model = ProductModel
        fields = [
            "slug",
            "category",
            "title",
            "description",
            "brief_description",
            "image",
            "stock",
            "price",
            "discount_percent",
            "status",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["slug"].widget.attrs["class"] = "form-control"
        self.fields["category"].widget.attrs["class"] = "form-select"
        self.fields["title"].widget.attrs["class"] = "form-control"
        self.fields["description"].widget.attrs["class"] = "form-control"
        self.fields["brief_description"].widget.attrs["class"] = "form-control"
        self.fields["image"].widget.attrs["class"] = "form-control"
        self.fields["stock"].widget.attrs["class"] = "form-control"
        self.fields["price"].widget.attrs["class"] = "form-control"
        self.fields["discount_percent"].widget.attrs["class"] = "form-control"
        self.fields["status"].widget.attrs["class"] = "form-select"


class AdminProductCreateForm(forms.ModelForm):
    # body = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = ProductModel
        fields = [
            "slug",
            "category",
            "title",
            "description",
            "brief_description",
            "image",
            "stock",
            "price",
            "discount_percent",
            "status",
            #"body",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["slug"].widget.attrs["class"] = "form-control"
        self.fields["category"].widget.attrs["class"] = "form-select"
        self.fields["title"].widget.attrs["class"] = "form-control"
        self.fields["description"].widget.attrs["class"] = "form-control"
        self.fields["brief_description"].widget.attrs["class"] = "form-control"
        self.fields["image"].widget.attrs["class"] = "form-control"
        self.fields["stock"].widget.attrs["class"] = "form-control"
        self.fields["price"].widget.attrs["class"] = "form-control"
        self.fields["discount_percent"].widget.attrs["class"] = "form-control"
        self.fields["status"].widget.attrs["class"] = "form-select"
        # self.fields["body"].widget.attrs["class"] = "form-control"


class AdminCategoryCreateForm(forms.ModelForm):

    class Meta:
        model = ProductCategoryModel
        fields = [
            "title",
            "slug",
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs["class"] = "form-control"
        self.fields["slug"].widget.attrs["class"] = "form-control"

class AdminAddImageForm(forms.ModelForm):

    class Meta:
        model = ProductImageModel
        fields = [
            "product",
            "file",
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product"].widget.attrs["class"] = "form-select"
        self.fields["file"].widget.attrs["class"] = "form-control"


class CouponForm(forms.ModelForm):

    class Meta:
        model = CouponModel
        fields = ["code", "discount_percent", "max_limit_usage", "used_by", "expiering_date"]
        widgets = {
            'expiering_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.expiering_date:
            self.initial['expiration_date'] = self.instance.expiering_date.strftime('%Y-%m-%dT%H:%M')
        self.fields["code"].widget.attrs["class"] = "form-control"
        self.fields["discount_percent"].widget.attrs["class"] = "form-control"
        self.fields["max_limit_usage"].widget.attrs["class"] = "form-control"
        self.fields["used_by"].widget.attrs["class"] = "form-select"



class ReviewForm(forms.ModelForm):

    class Meta:
        model = ReviewModel
        fields = [
            "product",
            "description",
            "rate",
            "status"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product"].widget.attrs["class"] = "form-control"
        self.fields["description"].widget.attrs["class"] = "form-control"
        self.fields["rate"].widget.attrs["class"] = "form-select"
        self.fields["status"].widget.attrs["class"] = "form-select"