import cv2
import numpy as np
from module.fuzzy import input_fuzzy

class ImageProcessing:
    def __init__(self, path_image):
        self.path = path_image

    def get_ndvi(self):
        # Read Image
        path = self.path
        image_show = cv2.imread(path)
        
        # Pisahkan saluran warna
        red_image = image_show[:, :, 0]
        noir_image = image_show[:, :, 2]
        
        # Konversi ke tipe data float32 untuk operasi aritmatika
        noir_image = noir_image.astype(np.float32)
        red_image = red_image.astype(np.float32)
        
        # Hitung ndvi
        ndvi = (noir_image - red_image) / (noir_image + red_image + 1e-6)
        avg_ndvi = np.mean(ndvi)
        return avg_ndvi
    
    def get_reflectance(self):
        # Read Image
        path = self.path
        image_show = cv2.imread(path)
        
        # Konversi gambar ke tipe data float32
        image = image_show.astype(np.float32)
        # Normalization
        image /= 255.0
        # Average Reflectance
        avg_reflectance = np.mean(image)
        
        # Percentace
        reflectance = avg_reflectance * 100
        
        return reflectance
    
    def get_fuzzy(self):
        # Get data input
        ndvi = self.get_ndvi()
        reflectance = self.get_reflectance()
        # Get Output Fuzzy
        output, status = input_fuzzy(ndvi, reflectance)
        
        return (output, status)
        
        