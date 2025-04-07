## Cara membuar virtual evirontment python3 - macOS
 
 https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/

```python

#buat folder >> buka dengan vscode
#create venv
python3 -m venv .venv
#activate venv
source .venv/bin/activate
#check python venv
which python
#deactivate venv
deactivate
```

```py
#melanjutkan 
python3 -m pip install --upgrade pip
python3 -m pip --version
```

### Install Django 
```py
pip install django djangorestframework

django-admin --version

django-admin startproject myapi .

python manage.py runserver

#Starting development server at http://127.0.0.1:8000/

```

### Django dengan SQLite3

settings.py 

```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}

```

### Django migrate / membuat tabel dengan ORM

```py
#/siswa/models.py
from django.db import models

class Siswa(models.Model):
    namaSiswa = models.CharField(max_length=100)
    alamatSiswa = models.TextField()

```
```py
python3 manage.py makemigrations
python3 manage.py migrate

```

### Django membuat tabel dmanual
```py
python3 manage.py dbshell
```
```sql
CREATE TABLE siswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    namaSiswa TEXT NOT NULL,
    alamatSiswa TEXT NOT NULL
);


PRAGMA table_info(siswa);

```

### API SPEC
API Specification (API Spec)

Base URL:

http://127.0.0.1:8000/api/siswa/

1️⃣ Get All Siswa

Endpoint:

GET /api/siswa/

Response:
```
[
    {"id": 1, "namaSiswa": "John Doe", "alamatSiswa": "Jl. Merdeka"},
    {"id": 2, "namaSiswa": "Jane Doe", "alamatSiswa": "Jl. Sudirman"}
]
```

2️⃣ Get Siswa by ID

Endpoint:

GET /api/siswa/{id}/

Response (200 OK):
```
{
    "id": 1,
    "namaSiswa": "John Doe",
    "alamatSiswa": "Jl. Merdeka"
}
```
Response (404 Not Found):
```
{
    "message": "Siswa tidak ditemukan"
}
```
3️⃣ Create Siswa

Endpoint:

POST /api/siswa/create/

Request Body (Form Data):
```
{
    "namaSiswa": "John Doe",
    "alamatSiswa": "Jl. Merdeka"
}
```
Response (201 Created):
```
{
    "message": "Siswa berhasil ditambahkan"
}
```
4️⃣ Update Siswa

Endpoint:

POST /api/siswa/update/{id}/

Request Body (Form Data):
```
{
    "namaSiswa": "Jane Doe",
    "alamatSiswa": "Jl. Sudirman"
}
```
Response (200 OK):
```
{
    "message": "Siswa berhasil diperbarui"
}
```
5️⃣ Delete Siswa

Endpoint:

DELETE /api/siswa/delete/{id}/

Response (200 OK):
```
{
    "message": "Siswa berhasil dihapus"
}
```

### SISWA API

```py
python3 manage.py startapp siswa
```

```
your_project/
│── your_project/        # Folder utama proyek Django
│── siswa/               # Folder aplikasi siswa
│   ├── migrations/
│   ├── models.py        # Menyimpan database model >> migrate
│   ├── tests.py         # File unit test
│   ├── views.py
│   ├── urls.py          # Tambahkan jika belum ada
│── manage.py
```

Buka settings.py di folder proyek utama dan pastikan siswa sudah ditambahkan dalam INSTALLED_APPS:

```py
python3 manage.py migrate #JIKA MEMBUAT TABLE DENGAN ORM
```

```py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'siswa',  # Tambahkan aplikasi siswa di sini
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware', #untuk dev >> csrf off
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

```

```py
#/myapi/urls.py >> URL Utama
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('siswa.urls')),
]

#/siswa/urls.py >> URL Turunan siswa
from django.urls import path
from .views import siswa_handler

urlpatterns = [
    path('siswa', siswa_handler, name='siswa_handler'), #name >> reverse url
    path('siswa/<int:siswa_id>', siswa_handler, name='siswa_handler_detail'),
]

#/siswa/views.py
from django.db import connection
from django.http import JsonResponse
from rest_framework.parsers import JSONParser 

def siswa_handler(request, siswa_id=None):
    #request method POST
    if request.method == "POST":
        return create_siswa(request)
    #request method GET
    elif request.method == "GET":
        if siswa_id is not None:
            #request method GET dengan id
            return get_siswa_by_id(request, siswa_id)
        #request method GET tanpa id
        return get_all_siswa(request)
    #request PUT
    elif request.method == "PUT" and siswa_id is not None:
        return update_siswa(request, siswa_id)
    #request DELETE
    elif request.method == "DELETE" and siswa_id is not None:
        return delete_siswa(request, siswa_id)
    #request lainnya
    return JsonResponse({"error": "Metode tidak diizinkan"}, status=405)

def create_siswa(request):
    try:
        #1. ambil data body berupa json
        datajson = JSONParser().parse(request)
        #2. ambil variable masing2 variabel dalam json
        nama = datajson.get("namaSiswa")
        alamat = datajson.get("alamatSiswa")
        #3. validasi jika variable tidak lengkap
        if not nama or not alamat:
            return JsonResponse({"error": "Nama dan alamat wajib diisi"}, status=400)
        #4. Koneksi SQL kemudian eksekusi perintah SQL
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO siswa (namaSiswa, alamatSiswa) VALUES (%s, %s)", [nama, alamat])
        #5. Response Sukses
        return JsonResponse({"message": "Siswa berhasil ditambahkan"}, status=201)
    except Exception as e:
        #6. Response Error
        return JsonResponse({"error": str(e)}, status=500)

def get_all_siswa(request):
    #1. Koneksi SQL kemudian eksekusi perintah SQL
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, namaSiswa, alamatSiswa FROM siswa")
        #2. Mengambil semua baris hasil query dalam bentuk list of tuples
        siswa_list = cursor.fetchall()
    #3. Ubah list menjadi format json
    siswa_dict_list = [{"id": row[0], "namaSiswa": row[1], "alamatSiswa": row[2]} for row in siswa_list]
    #4. Return json
    return JsonResponse(siswa_dict_list, safe=False)

def get_siswa_by_id(request, siswa_id):
    #1. Koneksi SQL kemudian eksekusi perintah SQL
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, namaSiswa, alamatSiswa FROM siswa WHERE id = %s", [siswa_id])
        #2. Mengambil satu baris hasil query dalam bentuk tuple 
        row = cursor.fetchone()
    #3. jika ada data row maka response dalam bentuk json
    if row:
        return JsonResponse({"id": row[0], "namaSiswa": row[1], "alamatSiswa": row[2]})
    #4. response jika row kosong
    return JsonResponse({"message": "Siswa tidak ditemukan"}, status=404)

def update_siswa(request, siswa_id):
    try:
        #1. ambil data body berupa json
        datajson = JSONParser().parse(request)
        #2. ambil variable masing2 variabel dalam json
        nama = datajson.get("namaSiswa")
        alamat = datajson.get("alamatSiswa")
        #3. validasi jika variable tidak lengkap >> response
        if not nama or not alamat:
            return JsonResponse({"error": "Nama dan alamat wajib diisi"}, status=400)
        #4. Koneksi SQL kemudian eksekusi perintah SQL
        with connection.cursor() as cursor:
            cursor.execute("UPDATE siswa SET namaSiswa = %s, alamatSiswa = %s WHERE id = %s", [nama, alamat, siswa_id])
        #5. Response berhasil
        return JsonResponse({"message": "Siswa berhasil diperbarui"})
    except Exception as e:
        #6. response error
        return JsonResponse({"error": str(e)}, status=500)

def delete_siswa(request, siswa_id):
    try:
        #1. Koneksi SQL kemudian eksekusi perintah SQL
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM siswa WHERE id = %s", [siswa_id])
        #2. Response berhasil
        return JsonResponse({"message": "Siswa berhasil dihapus"})
    #3. response error
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

```

Aplikasi sudah bisa dijalankan dan dilakukan test menggunakan postman
`python manage.py runserver`

### UNIT TEST

```py
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

```
jalankan test `python manage.py test siswa`

### TEST REKUEST

```js
//request.rest >> setelah install extension rest client

POST http://localhost:8000/api/siswa
content-type: application/json

{
    "namaSiswa": "John Doe12",
    "alamatSiswa": "Jl. Merdeka12"
}

### GET SISWA ALL
GET http://localhost:8000/api/siswa HTTP/1.1


### GET SISWA BY ID
GET http://localhost:8000/api/siswa/3 HTTP/1.1

### DELETE SISWA
DELETE  http://localhost:8000/api/siswa/2 HTTP/1.1

### UODATE SISWA
PUT http://localhost:8000/api/siswa/3
content-type: application/json

{
    "namaSiswa": "John Doe12 UPDATE",
    "alamatSiswa": "Jl. Merdeka12"
}
```

### GITHUB

```js
echo "# django1" >> README.md
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/edycoleee/django1.git
git push -u origin main

```


==========================================================
## UPDATE IMPLEMETASI :
1. Raw SQL 
2. Unit Testing
3. ViewSet + Router
4. custem exception hanlder, 
5. response wrapper (status,data,url), 
6. versioning api (v1)
7. Serializer untuk input/output
8. Swagger/OpenAPI Docs

## 1. INSTALL 

```py
#masuk ke venv
source venv/bin/activate 
which python

#Install Swagger
pip install drf-yasg

```
## 2. 



=============================================================
## AUTH IMPLEMETASI :
9. Filtering, Pagination
10. Permission & AUTH
- Swagger/OpenAPI Docs
- Unit Testing
