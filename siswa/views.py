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
