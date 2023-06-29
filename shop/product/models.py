from django.db import models
from users.models import CustomUser
from django.shortcuts import render
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps


# python manage.py makemigrations
# python manage.py migrate
# python manage.py createsuperuser
# python manage.py runserver
# pip install psycopg2


class Category(models.Model):

    class Meta:
        db_table = "category"
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    photo_0 = models.ImageField(upload_to="photos/%Y/%m/%d/")

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        db_table = "products"
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)

    photo_0 = models.ImageField(upload_to="photos/%Y/%m/%d/")
    photo_1 = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    photo_2 = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    photo_3 = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)


def __str__(self):
    return f"{self.name} {self.description} {self.price} {self.catedory}"


# class Order(models.Model):
#     class Meta:
#         db_table = "orders"
#     user = models.ForeignKey(
#         CustomUser, on_delete=models.CASCADE, blank=True, null=True)
#     product = models.ForeignKey(
#         Product, on_delete=models.CASCADE, blank=True, null=True)
#     quantity = models.PositiveIntegerField(default=1)
#     total_price = models.PositiveIntegerField(default=1)


class Basket(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Basket for {self.user.username} | Product: {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity

    def get_json(self):
        item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum())
        }
        return item

    @classmethod
    def create_or_update(cls, product_id, user):
        baskets = Basket.objects.filter(user=user, product_id=product_id)

        if not baskets.exists():
            obj = Basket.objects.create(
                user=user, product_id=product_id, quantity=1)
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()
            is_created = False
            return basket, is_created
