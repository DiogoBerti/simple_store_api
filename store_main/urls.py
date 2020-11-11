from django.conf.urls import url, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"clients", views.ClientViewSet)
router.register(r"products", views.ProductViewSet)
router.register(r"order", views.SaleOrderViewSet)
router.register(r"order_lines", views.SaleOrderLineViewSet)

urlpatterns = [
    url('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    url(r"api/v1/", include(router.urls)) 
]