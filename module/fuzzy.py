import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def input_fuzzy(ndvi_input, reflektansi_input):
    # Definisikan variabel input dan output untuk fuzzy
    nilai_ndvi = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'nilai_ndvi')
    nilai_reflektansi = ctrl.Antecedent(np.arange(0, 101, 1), 'nilai_reflektansi')
    kualitas_tanaman = ctrl.Consequent(np.arange(0, 51, 1), 'kualitas_tanaman')

    # Membership functions for NDVI
    nilai_ndvi['rendah'] = fuzz.trimf(nilai_ndvi.universe, [0, 0, 0.27])
    nilai_ndvi['tinggi'] = fuzz.trapmf(nilai_ndvi.universe, [0.25, 0.3, 1, 1])

    # Membership functions for Reflektansi
    nilai_reflektansi['rendah'] = fuzz.trapmf(nilai_reflektansi.universe, [0, 0, 35, 49.5])
    nilai_reflektansi['tinggi'] = fuzz.trapmf(nilai_reflektansi.universe, [47.5, 50, 100, 100])

    # Membership functions for Kualitas Tanaman
    kualitas_tanaman['sakit'] = fuzz.trimf(kualitas_tanaman.universe, [0, 35, 55])
    kualitas_tanaman['sehat'] = fuzz.trimf(kualitas_tanaman.universe, [45, 75, 100, 100])

    # Define the fuzzy rules
    rule1 = ctrl.Rule(nilai_ndvi['rendah'] | nilai_reflektansi['tinggi'], kualitas_tanaman['sakit'])
    rule2 = ctrl.Rule(nilai_ndvi['rendah'] | nilai_reflektansi['rendah'], kualitas_tanaman['sakit'])
    rule3 = ctrl.Rule(nilai_ndvi['tinggi'] | nilai_reflektansi['tinggi'], kualitas_tanaman['sakit'])
    rule4 = ctrl.Rule(nilai_ndvi['tinggi'] | nilai_reflektansi['rendah'], kualitas_tanaman['sehat'])

    # Control system
    kualitas_tanaman_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
    kualitas_tanaman_simulasi = ctrl.ControlSystemSimulation(kualitas_tanaman_ctrl)

    # Set input values for fuzzy system
    kualitas_tanaman_simulasi.input['nilai_ndvi'] = ndvi_input
    kualitas_tanaman_simulasi.input['nilai_reflektansi'] = reflektansi_input
    
    # Compute fuzzy logic
    kualitas_tanaman_simulasi.compute()

    # Defuzzifikasi menggunakan metode Mamdani
    nilai_tegas = kualitas_tanaman_simulasi.output['kualitas_tanaman']

    # Tentukan status berdasarkan nilai tegas
    if nilai_tegas < 50:
        status = "sakit"
    else:
        status = "sehat"
        
    return (nilai_tegas, status)