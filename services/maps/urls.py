from django.conf.urls import url, include
from rest_framework import routers
from services.maps import views as maps


router = routers.SimpleRouter()
router.register('maps', maps.MapViewSet, base_name='maps')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^$', maps.home_view)
]
