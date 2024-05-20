from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

# app_name = 'heropy'

urlpatterns = [
    path('', views.index, name='index'),
    path('start/', views.start, name='start'),
    path('settings/', views.settings, name='settings'),
    path('book_list/', views.book_list, name='book_list'),
    path('book_config/<int:book_id>', views.book_config, name='book_config'),
    path('load/', views.load, name='load'),
    path('book/<int:book_id>', views.book, name='book'),
    path('book/chapter/<int:book_id>/<int:chapter_id>/', views.chapter, name='chapter'),

    # PARTIAL
    path('partial/chapter_player_board/<str:stat_name>/<str:value>', views.partial_player_board, name='partial_player_board'),
    path('partial/chapter_battle', views.partial_chapter_battle, name='partial_chapter_battle'),

    # API
    path('stat/<str:stat_name>/<str:value>', views.stat, name='stat'),
]
