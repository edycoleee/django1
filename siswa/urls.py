#/siswa/urls.py >> URL Turunan siswa
from django.urls import path
from .views import siswa_handler

urlpatterns = [
    path('siswa', siswa_handler, name='siswa_handler'),
    path('siswa/<int:siswa_id>', siswa_handler, name='siswa_handler_detail'),
]
