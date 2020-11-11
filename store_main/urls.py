from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"clients", views.ClientViewSet)
router.register(r"products", views.ProductViewSet)
router.register(r"order", views.SaleOrderViewSet)
router.register(r"order_lines", views.SaleOrderLineViewSet)

urlpatterns = [
    url(r"api/v1/", include(router.urls)) 
]