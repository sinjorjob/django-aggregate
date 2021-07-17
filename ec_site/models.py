from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    class Meta:
        verbose_name = 'カテゴリ'
        verbose_name_plural = "カテゴリ"
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    class Meta:
        verbose_name = '商品'
        verbose_name_plural = "商品"

    name = models.CharField(verbose_name = '製品名', max_length=150, null = False, blank=False)
    price = models.IntegerField(verbose_name = '価格')
    category = models.ForeignKey(Category, on_delete = models.PROTECT,verbose_name ="カテゴリ")

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    class Meta:
        verbose_name = '注文データ'
        verbose_name_plural = '注文データ'

    user = models.ForeignKey(User,verbose_name = 'ユーザ',on_delete = models.CASCADE, null=True)
    items = models.ManyToManyField('Product', related_name='order', blank=True)
    created_date = models.DateField(auto_now_add=True)
    price = models.DecimalField(verbose_name="合計金額",max_digits=7, decimal_places=0, null=True, blank=True)
    name = models.CharField(verbose_name="氏名", max_length=50, blank=True)

    def __str__(self):
        return f'注文日: {self.created_date.strftime("%b %d %Y %I:%M %p")}'


class OrderItemDetail(models.Model):
    class Meta:
        verbose_name = '注文明細'
        verbose_name_plural = '注文明細'

    invoice = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,verbose_name='商品',on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='数量')
    created_date = models.DateField(auto_now_add=True)

