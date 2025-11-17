from rest_framework.routers import DefaultRouter
from .views_api import ProductViewSet, CategoryViewSet, UnitViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"units", UnitViewSet, basename="unit")

urlpatterns = router.urls
