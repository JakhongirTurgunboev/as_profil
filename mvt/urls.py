from django.urls import path
from .views import main_view, part1_view, part2_view, part3_view

urlpatterns = [
    path('main/', main_view),
    path('', part1_view),
    path('part-second/<str:type>/', part2_view),
    path('part-third/<int:material>/', part3_view),
]