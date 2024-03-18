from django.db import models
from users.models import BaseModel
from django.core.validators import FileExtensionValidator


class Category(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'


class Product(BaseModel):
    name = models.CharField(max_length=200)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='products')
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(default='', null=True, blank=True)
    image = models.ImageField(upload_to='product_images/', null=True,
                              validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg'])])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'


class Order(BaseModel):
    order_id = models.CharField(unique=True, max_length=50)
    order_date = models.DateField(auto_now_add=True)
    total_price = models.IntegerField()
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return self.order_id


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} -- Quantity {self.quantity}"

    @property
    def total_price(self):
        return self.price * self.quantity
