from django.urls import path
from . import views

#app_name = 'heropy'

urlpatterns = [
    path('', views.index, name='index'),
    path('start/', views.start, name='start'),
    path('load/', views.load, name='load'),
    path('book/', views.book, name='book'),
    path('book/chapter/<int:book_id>/<int:chapter_id>/', views.chapter, name='chapter'),

    path('stat/<str:stat_name>/<str:value>', views.stat, name='stat'),
]
