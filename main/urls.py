# from django.urls import path, include
from rest_framework import routers

from main.views import *


router = routers.SimpleRouter()

router.register(r'items', ItemViewSet)
router.register(r'shifts', ShiftViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = router.urls
