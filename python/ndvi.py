import cv2
import numpy as np

def hitung_ndvi(saluran_noir, saluran_merah):
    # Konversi ke tipe data float32 untuk operasi aritmatika
    saluran_noir = saluran_noir.astype(np.float32)
    saluran_merah = saluran_merah.astype(np.float32)

    # Hitung NDVI
    ndvi = (saluran_noir - saluran_merah) / (saluran_noir + saluran_merah + 1e-6)  # ditambah 1e-6 untuk menghindari pembagian oleh nol

    return ndvi

if __name__ == "__main__":
    # Tentukan path gambar
    gambar_path = "50 meter/1.jpg"  # Ganti dengan path gambar yang Anda gunakan

    # Baca gambar
    gambar = cv2.imread(gambar_path)

    # Pisahkan saluran warna
    saluran_merah = gambar[:, :, 0]  # Saluran merah (620-750 nm)
    saluran_noir = gambar[:, :, 2]   # Saluran NoIR (NIR, 700-1000 nm)

    # Konversi ke tipe data float32 untuk operasi aritmatika
    saluran_noir = saluran_noir.astype(np.float32)
    saluran_merah = saluran_merah.astype(np.float32)

    # Hitung NDVI
    ndvi = hitung_ndvi(saluran_noir, saluran_merah)

    # Bagian ini untuk membagi gambar menjadi piksel dan menampilkan nilai NDVI per piksel
#for i in range(ndvi.shape[0]):
    #for j in range(ndvi.shape[1]):
        #print(f"Pixel ({i},{j}): NDVI = {ndvi[i,j]}")

# Hitung nilai rata-rata NDVI
ndvi_mean = np.mean(ndvi)
print("Nilai rata-rata NDVI:", ndvi_mean)