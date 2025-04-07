from rest_framework import serializers

class SiswaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    namaSiswa = serializers.CharField(max_length=100)
    alamatSiswa = serializers.CharField(max_length=200)
