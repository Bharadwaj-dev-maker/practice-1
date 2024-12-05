from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, DiscountViewSet, OrderViewSet

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('discounts', DiscountViewSet)
router.register('orders', OrderViewSet)

urlpatterns = router.urls
