import cv2
import numpy as np

def hitung_persentase_reflektansi(gambar):
    # Konversi gambar ke tipe data float32
    gambar = gambar.astype(np.float32)

    # Normalisasi nilai reflektansi ke rentang 0 hingga 1
    gambar /= 255.0

    # Hitung rata-rata reflektansi
    rata_rata_reflektansi = np.mean(gambar)

    # Hitung persentase reflektansi
    persentase_reflektansi = rata_rata_reflektansi * 100

    return persentase_reflektansi

if __name__ == "__main__":
    # Tentukan path gambar
    gambar_path = "50 meter/1.jpg"  # Ganti dengan path gambar yang Anda gunakan

    # Baca gambar
    gambar = cv2.imread(gambar_path)

    # Hitung persentase reflektansi
    persentase_reflektansi = hitung_persentase_reflektansi(gambar)

    print("Persentase Reflektansi:", persentase_reflektansi, "%")