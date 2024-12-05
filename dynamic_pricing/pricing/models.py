from django.db import models

# Product Model
class Product(models.Model):
    PRODUCT_TYPES = [
        ('seasonal', 'Seasonal Product'),
        ('bulk', 'Bulk Product'),
        ('premium', 'Premium Product'),
    ]

    name = models.CharField(max_length=100)
    base_price = models.FloatField()
    product_type = models.CharField(choices=PRODUCT_TYPES, max_length=20)
    season_discount = models.FloatField(null=True, blank=True)  # For Seasonal Products
    tiered_discounts = models.JSONField(null=True, blank=True)  # For Bulk Products
    markup_percentage = models.FloatField(null=True, blank=True)  # For Premium Products

    def get_price(self, quantity=1):
        price = self.base_price * quantity
        if self.product_type == 'seasonal' and self.season_discount:
            price *= (1 - self.season_discount / 100)
        elif self.product_type == 'bulk' and self.tiered_discounts:
            applicable_discount = 0
            for min_quantity, discount in sorted(self.tiered_discounts.items()):
                if quantity >= int(min_quantity):
                    applicable_discount = discount
            price *= (1 - applicable_discount / 100)
        elif self.product_type == 'premium' and self.markup_percentage:
            price *= (1 + self.markup_percentage / 100)
        return price

    def __str__(self):
        return self.name

# Discount Model
class Discount(models.Model):
    DISCOUNT_TYPES = [
        ('percentage', 'Percentage Discount'),
        ('fixed', 'Fixed Amount Discount'),
        ('tiered', 'Tiered Discount'),
    ]

    name = models.CharField(max_length=100)
    discount_type = models.CharField(choices=DISCOUNT_TYPES, max_length=20)
    priority = models.IntegerField()
    percentage = models.FloatField(null=True, blank=True)
    fixed_amount = models.FloatField(null=True, blank=True)
    tier_criteria = models.JSONField(null=True, blank=True)  # {min_value: percentage}

    def apply_discount(self, price):
        if self.discount_type == 'percentage' and self.percentage:
            return price * (1 - self.percentage / 100)
        elif self.discount_type == 'fixed' and self.fixed_amount:
            return max(price - self.fixed_amount, 0)
        elif self.discount_type == 'tiered' and self.tier_criteria:
            applicable_discount = 0
            for min_value, discount in sorted(self.tier_criteria.items()):
                if price >= float(min_value):
                    applicable_discount = discount
            return price * (1 - applicable_discount / 100)
        return price

    def __str__(self):
        return self.name
    
class TieredDiscount(Discount):
    def apply_discount(self, price):
        # Sort the criteria by threshold (ascending order)
        applicable_discount = 0
        for threshold, discount in sorted(self.tier_criteria.items(), key=lambda x: float(x[0])):
            if price >= float(threshold):  # Apply the highest applicable discount
                applicable_discount = discount
            else:
                break  # Stop checking when price is below the threshold

        # Calculate and return the discounted price
        discounted_price = price - (price * (applicable_discount / 100))
        return round(discounted_price, 2)



# Order Model
class Order(models.Model):
    products = models.ManyToManyField(Product, through='OrderProduct')
    discounts = models.ManyToManyField(Discount)
    total_price = models.FloatField(default=0)

    def calculate_total(self):
        total = 0
        for order_product in self.orderproduct_set.all():
            total += order_product.product.get_price(order_product.quantity)

        # Apply discounts based on priority
        for discount in self.discounts.all().order_by('-priority'):
            total = discount.apply_discount(total)

        self.total_price = total
        self.save()
        return total

# Intermediate Model for Order and Product
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
