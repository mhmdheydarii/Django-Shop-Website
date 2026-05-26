from django.core.management.base import BaseCommand
from faker import Faker
from django.utils.text import slugify
from django.core.files import File
import random
from shop.models import ProductModel, ProductStatusType, ProductCategoryModel
from accounts.models import User, UserType
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

class Command(BaseCommand):
    help = "Generate fake categories"

    def handle(self, *args, **kwargs):
        fake = Faker(locale="fa_IR")
        user = User.objects.get(type=UserType.superuser.value)

        image_list = [
            "images/img1.jpg",
            "images/img2.jpg",
            "images/img3.jpg",
            "images/img4.jpg",
            "images/img5.jpg",
            "images/img6.jpg",
        ]

        categories = ProductCategoryModel.objects.all()

        for _ in range(10):
            user = user
            selected_categories = random.choice(categories)
            title = ' '.join([fake.word() for _ in range(1,3)])
            slug = slugify(title, allow_unicode=True)
            selected_image = random.choice(image_list)
            image_obj = File(file=open(BASE_DIR / selected_image, "rb"),name=Path(selected_image).name)
            description = fake.paragraph(nb_sentences=5)
            brief_description = fake.paragraph(nb_sentences=1)
            stock = fake.random_int(min=0, max=10)
            status = random.choice(ProductStatusType.choices)[0]
            price =  fake.random_int(min=10000, max=100000)
            discount_percent = fake.random_int(min=0, max=50)

            product = ProductModel.objects.create(
                user=user,
                title=title, 
                slug=slug,
                image=image_obj,
                description=description,
                brief_description=brief_description,
                stock=stock,
                status=status,
                price=price,
                discount_percent=discount_percent
            )
            product.category = selected_categories
            product.save()
        
        self.stdout.write(self.style.SUCCESS("Successfully generated 10 fake products"))