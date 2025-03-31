#/siswa/models.py
from django.db import models

class Siswa(models.Model):
    namaSiswa = models.CharField(max_length=100)
    alamatSiswa = models.TextField()
