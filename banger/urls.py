from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('make_banger/<str:nkdsu_id>/', views.make_banger, name='make_banger'),
    path('banger/<str:banger_id>/', views.view_banger, name='view_banger'),
    path('banger/', views.bangers, name='view_bangers'),
]
