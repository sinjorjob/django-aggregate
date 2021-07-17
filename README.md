# Django集計メソッド練習

aggreagte,annotateを使った売上データの集計例

## 対象テーブル構成

以下の4つのテーブルを定義しています。

#### カテゴリテーブル(Category)
| カラム名  | 用途  |
| ------------ | ------------ |
| name  |  カテゴリ名 |


#### 製品テーブル(Product)
| カラム名  | 用途  |
| ------------ | ------------ |
| name  |  製品名 |
| price  |  製品価格 |
| category  |  カテゴリ名 |

#### 注文テーブル(OrderItem)
| カラム名  | 用途  |
| ------------ | ------------ |
| user  |  ユーザID|
|items|  製品名 |
| created_date |  注文日 |
| price |  合計金額 |
| name |  氏名|


#### 注文明細テーブル(OrderItemDetail)
| カラム名  | 用途  |
| ------------ | ------------ |
| invoice  | 注文データ|
|product|  製品名 |
| quantity  |  注文数 |
| created_date |  注文日 |

## サンプルデータのロード
```console
pip install -r requirements.txt

python manage.py loaddata --format=yaml ec_site/fixtures/sample_data.yaml
```

## 各テーブルのレコード数をチェック

Looping with reference to own table only

```python
Category.objects.count()
3
Product.objects.count()
9
 OrderItem.objects.count()
18
OrderItemDetail.objects.count()
24
```

## 全期間の全商品の売上合計金額を求める

```python
from django.db.models import Sum
all_sales = OrderItem.objects.all()
total_price = all_sales.aggregate(Sum('price'))
total_price
{'price__sum': Decimal('337220')}
```

## 月毎の全商品の売上合計金額を求める


```python
from django.db.models import Sum
import calendar
dates_q = OrderItem.objects.dates('created_date', 'month', order='ASC')
dates_list = [ [date, date.replace(day=calendar.monthrange(date.year,date.month)[1])] for date in dates_q]

for date in dates_list:
    OrderItem.objects.filter(created_date__range=(date[0], date[1])).aggregate(total_price=Sum('price'))
{'total_price': Decimal('221740')}
{'total_price': Decimal('115480')}

```


## 全期間の商品毎の売上合計金額



```python
products_count = OrderItemDetail.objects.values('product').annotate(total = Sum('quantity'))
for product in products_count:
    product_data = Product.objects.get(pk=product['product'])
    print(f"{product_data},{product['total']}個 , 合計金額：{product['total'] * product_data.price}円")


電子レンジ,3個 , 合計金額：75000円
冷蔵庫,2個 , 合計金額：70000円
4Kテレビ,2個 , 合計金額：110000円
コート,2個 , 合計金額：39600円
Tシャツ,12個 , 合計金額：30000円
ハット,2個 , 合計金額：7800円
掛け時計,3個 , 合計金額：15000円
照明器具,3個 , 合計金額：29400円
ティッシュケース,4個 , 合計金額：7920円

```
## 月毎の商品毎の売上合計金額



```python
dates_q = OrderItemDetail.objects.dates('created_date', 'month', order='ASC')
dates_list = [ [date, date.replace(day=calendar.monthrange(date.year,date.month)[1])] for date in dates_q]
monthly_detail_data=[]
for date in dates_list:
    monthly_detail_data.append(OrderItemDetail.objects.filter(created_date__range=(date[0], date[1])))


for data in monthly_detail_data:
    print("="*50)
    products_count = data.values('product').annotate(total = Sum('quantity'))
    for product in products_count:
        product_data = Product.objects.get(pk=product['product'])
        print(f"{product_data},{product['total']}個 , 単価：{product_data.price},合計金額：{product['total'] * product_data.price}円")


=================================================
電子レンジ,2個 , 単価：25000,合計金額：50000円
冷蔵庫,1個 , 単価：35000,合計金額：35000円
4Kテレビ,1個 , 単価：55000,合計金額：55000円
コート,1個 , 単価：19800,合計金額：19800円
Tシャツ,6個 , 単価：2500,合計金額：15000円
ハット,1個 , 単価：3900,合計金額：3900円
掛け時計,2個 , 単価：5000,合計金額：10000円
照明器具,2個 , 単価：9800,合計金額：19600円
ティッシュケース,3個 , 単価：1980,合計金額：5940円
==================================================
電子レンジ,1個 , 単価：25000,合計金額：25000円
冷蔵庫,1個 , 単価：35000,合計金額：35000円
4Kテレビ,1個 , 単価：55000,合計金額：55000円
コート,1個 , 単価：19800,合計金額：19800円
Tシャツ,6個 , 単価：2500,合計金額：15000円
ハット,1個 , 単価：3900,合計金額：3900円
掛け時計,1個 , 単価：5000,合計金額：5000円
照明器具,1個 , 単価：9800,合計金額：9800円
ティッシュケース,1個 , 単価：1980,合計金額：1980円
```

## 全期間のカテゴリ毎の販売数を求める

```python
OrderItemDetail.objects.values('product__category').annotate(total = Sum('quantity'))
<QuerySet [{'product__category': 1, 'total': 7}, {'product__category': 2, 'total': 16}, {'product__category': 3, 'total': 10}]>


for data in number_of_sales_per_category:
    print(Product.objects.get(pk=data['product__category']), data['total'])
...
電子レンジ 7
冷蔵庫 16
4Kテレビ 10
```


## 月毎のカテゴリ毎の販売数を求める


```python
dates_q = OrderItemDetail.objects.dates('created_date', 'month', order='ASC')
dates_list = [ [date, date.replace(day=calendar.monthrange(date.year,date.month)[1])] for date in dates_q]
monthly_detail_data=[]
for date in dates_list:
    monthly_detail_data.append(OrderItemDetail.objects.filter(created_date__range=(date[0], date[1])))
for data in monthly_detail_data:
    print("="*50)
    number_of_sales_per_category = data.values('product__category').annotate(total = Sum('quantity'))
    for data in number_of_sales_per_category:
        print(Product.objects.get(pk=data['product__category']), data['total'])

  ==================================================
電子レンジ 4
冷蔵庫 8
4Kテレビ 7
==================================================
電子レンジ 3
冷蔵庫 8
4Kテレビ 3
```     

