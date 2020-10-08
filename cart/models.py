from django.db import models
from app.models import Product



class Order(models.Model):
    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50)
    email = models.EmailField('E-mail')
    address = models.CharField('Адрес', max_length=250)
    postal_code = models.CharField('Телефон', max_length=20)
    city = models.CharField('Город', max_length=100)
    CHOOSE_SIZE = (
        ('Extra Small', 'XS'),
        ('Small', 'S'),
        ('Medium', 'M'),
        ('Large', 'L'),
        ('Extra Large', 'XL'),
        ('Double Large', 'XXL'),
        
    )
    size = models.CharField('Размер', max_length=120, choices=CHOOSE_SIZE)
    created = models.DateTimeField('Создано', auto_now_add=True)
    updated = models.DateTimeField('Обновлено', auto_now=True)
    paid = models.BooleanField('оплаченный', default=False)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Продукт', related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество', default=1)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity



# class ProductSize(models.Model):
#     CHOOSE_SIZE = (
#         ('Extra Small', 'XS'),
#         ('Small', 'S'),
#         ('Medium', 'M'),
#         ('Large', 'L'),
#         ('Extra Large', 'XL'),
#         ('Double Large', 'XXL'),
#         ('Triple Large', 'XXXL'),
#     )
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     size = models.CharField(max_length=120, choices=CHOOSE_SIZE)
#     active = models.BooleanField(default=False)
#     # active = models.BooleanField(max_length=120)
#
#
#     @property
#     def __str__(self):
#         return self.size
#
#     def get_absolute_url(self):
#         return self.product.get_absolute_url()


