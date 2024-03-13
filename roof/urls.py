from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoofMaterialViewSet, calculate_roof_p

router = DefaultRouter()
router.register(r'materials', RoofMaterialViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('calculate_roof_p/', calculate_roof_p)
]
