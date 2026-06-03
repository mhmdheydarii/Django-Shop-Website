from django import forms
from .models import ReviewModel
from shop.models import ProductStatusType, ProductModel


class SubmitReviewForm(forms.ModelForm):
    
    class Meta:
        model = ReviewModel
        fields = ["product", "rate", "description"]

    def clean(self):
        cleaned_date = super().clean()
        product = cleaned_date.get("product")

        try:
            ProductModel.objects.get(id=product.id, status=ProductStatusType.publish.value)
        except ProductModel.DoesNotExist:
            raise forms.ValidationError("این محصول وجود ندارد")

        return cleaned_date
