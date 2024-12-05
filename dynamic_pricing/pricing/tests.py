from django.test import TestCase
from .models import *

class ProductTestCase(TestCase):
    def setUp(self):
        self.seasonal_product = Product.objects.create(
            name="Seasonal Product", base_price=100, product_type="seasonal", season_discount=20
        )
        self.bulk_product = Product.objects.create(
            name="Bulk Product", base_price=10, product_type="bulk", tiered_discounts={"10": 5, "20": 10}
        )
        self.premium_product = Product.objects.create(
            name="Premium Product", base_price=50, product_type="premium", markup_percentage=15
        )

    def test_seasonal_product_price(self):
        self.assertEqual(self.seasonal_product.get_price(), 80)  # 20% discount

    def test_bulk_product_price(self):
        self.assertEqual(self.bulk_product.get_price(15), 142.5)  # 5% discount for 15 units
        self.assertEqual(self.bulk_product.get_price(25), 225)    # 10% discount for 25 units

    def test_premium_product_price(self):
        self.assertEqual(round(self.premium_product.get_price(), 2), 57.5)  # Rounding to 2 decimals


class DiscountTestCase(TestCase):
    def setUp(self):
        # Example tier criteria
        self.tiered_discount = TieredDiscount.objects.create(
            name="Tiered Discount",
            discount_type="tiered",
            priority=3,
            tier_criteria={"500": 5, "1000": 10}  # Thresholds and discounts
        )

    def test_tiered_discount(self):
        self.assertEqual(self.tiered_discount.apply_discount(600), 570)  # 5% off
        self.assertEqual(self.tiered_discount.apply_discount(1100), 990)  # 10% off


class OrderTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Test Product", base_price=100)
        self.discount = Discount.objects.create(name="10% Off", discount_type="percentage", priority=1, percentage=10)
        self.order = Order.objects.create()
        self.order.products.add(self.product, through_defaults={'quantity': 2})
        self.order.discounts.add(self.discount)

    def test_order_total(self):
        self.order.calculate_total()
        self.assertEqual(self.order.total_price, 180)  # 2 products @ $100 each, 10% discount applied
