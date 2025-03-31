#/siswa/tests.py
from django.test import TestCase, Client
from django.db import connection

class SiswaAPITestCase(TestCase):
    def setUp(self):
        """Menyiapkan database sebelum setiap pengujian."""
        self.client = Client()

        # Buat tabel siswa jika belum ada
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS siswa (
                    id INTEGER PRIMARY KEY,  -- SQLite otomatis AUTO_INCREMENT
                    namaSiswa TEXT,
                    alamatSiswa TEXT
                )
            """)

        # Masukkan data dummy untuk pengujian (dilakukan dalam blok with yang berbeda)
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO siswa (namaSiswa, alamatSiswa) VALUES ('Jane Doe', 'Jl. Sudirman')")

    def test_create_siswa(self):
        """Test endpoint POST /api/siswa"""
        response = self.client.post('/api/siswa', 
                                    {"namaSiswa": "John Doe", "alamatSiswa": "Jl. Merdeka"}, 
                                    content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "Siswa berhasil ditambahkan")

    def test_get_all_siswa(self):
        """Test endpoint GET /api/siswa"""
        response = self.client.get('/api/siswa')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)  # Harus ada setidaknya 1 siswa

    def test_get_siswa_by_id(self):
        """Test endpoint GET /api/siswa/1"""
        response = self.client.get('/api/siswa/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["namaSiswa"], "Jane Doe")

    def test_update_siswa(self):
        """Test endpoint PUT /api/siswa/1"""
        response = self.client.put('/api/siswa/1', 
                                   {"namaSiswa": "Jane Doe Updated", "alamatSiswa": "Jl. Asia Afrika"}, 
                                   content_type="application/json")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Siswa berhasil diperbarui")

    def test_delete_siswa(self):
        """Test endpoint DELETE /api/siswa/1"""
        response = self.client.delete('/api/siswa/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Siswa berhasil dihapus")

        # Pastikan siswa tidak ditemukan setelah dihapus
        response_after_delete = self.client.get('/api/siswa/1/')
        self.assertEqual(response_after_delete.status_code, 404)
