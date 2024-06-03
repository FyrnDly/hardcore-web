import cv2
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

def hitung_ndvi(saluran_noir, saluran_merah):
    # Konversi ke tipe data float32 untuk operasi aritmatika
    saluran_noir = saluran_noir.astype(np.float32)
    saluran_merah = saluran_merah.astype(np.float32)

    # Hitung NDVI
    ndvi = (saluran_noir - saluran_merah) / (saluran_noir + saluran_merah + 1e-6)  # ditambah 1e-6 untuk menghindari pembagian oleh nol

    return ndvi

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

# Definisikan variabel input dan output untuk fuzzy
nilai_ndvi = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'nilai_ndvi')
nilai_reflektansi = ctrl.Antecedent(np.arange(0, 101, 1), 'nilai_reflektansi')
kualitas_tanaman = ctrl.Consequent(np.arange(0, 101, 1), 'kualitas_tanaman')

# Membership functions for NDVI
nilai_ndvi['rendah'] = fuzz.trimf(nilai_ndvi.universe, [0, 0, 0.26])
nilai_ndvi['tinggi'] = fuzz.trapmf(nilai_ndvi.universe, [0.2, 0.3, 1, 1])

# Membership functions for Reflektansi
nilai_reflektansi['rendah'] = fuzz.trapmf(nilai_reflektansi.universe, [0, 0, 35, 55])
nilai_reflektansi['tinggi'] = fuzz.trapmf(nilai_reflektansi.universe, [40, 50, 100, 100])

# Membership functions for Kualitas Tanaman
kualitas_tanaman['sakit'] = fuzz.trimf(kualitas_tanaman.universe, [0, 25, 50])
kualitas_tanaman['sehat'] = fuzz.trapmf(kualitas_tanaman.universe, [40, 60, 100, 100])

# Define the fuzzy rules
rule1 = ctrl.Rule(nilai_ndvi['rendah'] | nilai_reflektansi['tinggi'], kualitas_tanaman['sakit'])
rule2 = ctrl.Rule(nilai_ndvi['rendah'] | nilai_reflektansi['rendah'], kualitas_tanaman['sakit'])
rule3 = ctrl.Rule(nilai_ndvi['tinggi'] | nilai_reflektansi['tinggi'], kualitas_tanaman['sakit'])
rule4 = ctrl.Rule(nilai_ndvi['tinggi'] | nilai_reflektansi['rendah'], kualitas_tanaman['sehat'])
rule5 = ctrl.Rule(nilai_ndvi['tinggi'] | nilai_reflektansi['rendah'], kualitas_tanaman['sehat'])

# Control system
kualitas_tanaman_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
kualitas_tanaman_simulasi = ctrl.ControlSystemSimulation(kualitas_tanaman_ctrl)

if __name__ == "__main__":
    # Tentukan path gambar
    gambar_path = "50 meter cut/Pohon 1.jpg"  # Ganti dengan path gambar yang Anda gunakan

    # Baca gambar
    gambar = cv2.imread(gambar_path)

    # Pisahkan saluran warna
    saluran_merah = gambar[:, :, 0]  # Saluran merah (620-750 nm)
    saluran_noir = gambar[:, :, 2]   # Saluran NoIR (NIR, 700-1000 nm)

    # Hitung NDVI
    ndvi = hitung_ndvi(saluran_noir, saluran_merah)

    # Hitung nilai rata-rata NDVI
    ndvi_mean = np.mean(ndvi)
    print("Nilai rata-rata NDVI:", ndvi_mean)

    # Hitung persentase reflektansi
    persentase_reflektansi = hitung_persentase_reflektansi(gambar)
    print("Persentase Reflektansi:", persentase_reflektansi, "%")

    # Set input values for fuzzy system
    kualitas_tanaman_simulasi.input['nilai_ndvi'] = ndvi_mean
    kualitas_tanaman_simulasi.input['nilai_reflektansi'] = persentase_reflektansi

    # Compute fuzzy logic
    kualitas_tanaman_simulasi.compute()

    # Output hasil fuzzy
    print(f'Input NDVI: {ndvi_mean}')
    print(f'Input Reflektansi: {persentase_reflektansi}')
    print(f'Output Kualitas Tanaman: {kualitas_tanaman_simulasi.output["kualitas_tanaman"]}')

    # Defuzzification result
    kualitas_tanaman.view(sim=kualitas_tanaman_simulasi)
    plt.show()
