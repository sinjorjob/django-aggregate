# Generated by Django 3.2.5 on 2021-07-16 18:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'カテゴリ',
                'verbose_name_plural': 'カテゴリ',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('price', models.DecimalField(blank=True, decimal_places=0, max_digits=7, null=True, verbose_name='合計金額')),
                ('name', models.CharField(blank=True, max_length=50, verbose_name='氏名')),
            ],
            options={
                'verbose_name': '注文データ',
                'verbose_name_plural': '注文データ',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='製品名')),
                ('price', models.IntegerField(verbose_name='価格')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ec_site.category', verbose_name='カテゴリ')),
            ],
            options={
                'verbose_name': '商品',
                'verbose_name_plural': '商品',
            },
        ),
        migrations.CreateModel(
            name='OrderItemDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='数量')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ec_site.orderitem')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ec_site.product', verbose_name='商品')),
            ],
            options={
                'verbose_name': '注文明細',
                'verbose_name_plural': '注文明細',
            },
        ),
        migrations.AddField(
            model_name='orderitem',
            name='items',
            field=models.ManyToManyField(blank=True, related_name='order', to='ec_site.Product'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザ'),
        ),
    ]
