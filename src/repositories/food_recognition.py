import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np
from PIL import Image
import glob

from scipy.misc import imresize
import os
from os import listdir
from os.path import isfile, join
import shutil
import stat
import collections
from collections import defaultdict

from ipywidgets import interact, interactive, fixed
import ipywidgets as widgets
import json
import h5py


import matplotlib.image as img
import glob
import cv2




#Total number of classe
ix_to_class={"0": "apple_pie", "1": "baby_back_ribs", "2": "baklava", "3": "beef_carpaccio", "4": "beef_tartare", "5": "beet_salad", "6": "beignets", "7": "bibimbap", "8": "bread_pudding", "9": "breakfast_burrito", "10": "bruschetta", "11": "caesar_salad", "12": "cannoli", "13": "caprese_salad", "14": "carrot_cake", "15": "ceviche", "16": "cheesecake", "17": "cheese_plate", "18": "chicken_curry", "19": "chicken_quesadilla", "20": "chicken_wings", "21": "chocolate_cake", "22": "chocolate_mousse", "23": "churros", "24": "clam_chowder", "25": "club_sandwich", "26": "crab_cakes", "27": "creme_brulee", "28": "croque_madame", "29": "cup_cakes", "30": "deviled_eggs", "31": "donuts", "32": "dumplings", "33": "edamame", "34": "eggs_benedict", "35": "escargots", "36": "falafel", "37": "filet_mignon", "38": "fish_and_chips", "39": "foie_gras", "40": "french_fries", "41": "french_onion_soup", "42": "french_toast", "43": "fried_calamari", "44": "fried_rice", "45": "frozen_yogurt", "46": "garlic_bread", "47": "gnocchi", "48": "greek_salad", "49": "grilled_cheese_sandwich", "50": "grilled_salmon", "51": "guacamole", "52": "gyoza", "53": "hamburger", "54": "hot_and_sour_soup", "55": "hot_dog", "56": "huevos_rancheros", "57": "hummus", "58": "ice_cream", "59": "lasagna", "60": "lobster_bisque", "61": "lobster_roll_sandwich", "62": "macaroni_and_cheese", "63": "macarons", "64": "miso_soup", "65": "mussels", "66": "nachos", "67": "omelette", "68": "onion_rings", "69": "oysters", "70": "pad_thai", "71": "paella", "72": "pancakes", "73": "panna_cotta", "74": "peking_duck", "75": "pho", "76": "pizza", "77": "pork_chop", "78": "poutine", "79": "prime_rib", "80": "pulled_pork_sandwich", "81": "ramen", "82": "ravioli", "83": "red_velvet_cake", "84": "risotto", "85": "samosa", "86": "sashimi", "87": "scallops", "88": "seaweed_salad", "89": "shrimp_and_grits", "90": "spaghetti_bolognese", "91": "spaghetti_carbonara", "92": "spring_rolls", "93": "steak", "94": "strawberry_shortcake", "95": "sushi", "96": "tacos", "97": "takoyaki", "98": "tiramisu", "99": "tuna_tartare", "100": "waffles"}


class FoodRecognition:

    model = None
    process_image = None

    def __init__(self, filepath,model, process_image):
        self.filepath = filepath
        self.model = model
        self.process_image = process_image
    

    def load_images(self):
            root = self.filepath
            min_side=299
            all_imgs = []
            all_classes = []
            resize_count = 0
            invalid_count = 0
            for img_name in sorted(glob.glob(root)):
                img_arr = img.imread(img_name)
                if img_arr.shape[2]==4:
            
                    img_arr = cv2.cvtColor(img_arr, cv2.COLOR_BGR2RGB)
                img_arr_rs = img_arr
                try:
                    w, h, _ = img_arr.shape
                    if w < min_side:
                        wpercent = (min_side/float(w))
                        hsize = int((float(h)*float(wpercent)))
                        #print('new dims:', min_side, hsize)
                        img_arr_rs = imresize(img_arr, (min_side, hsize))
                        resize_count += 1
                    elif h < min_side:
                        hpercent = (min_side/float(h))
                        wsize = int((float(w)*float(hpercent)))
                        #print('new dims:', wsize, min_side)
                        img_arr_rs = imresize(img_arr, (wsize, min_side))
                        resize_count += 1
                    all_imgs.append(img_arr_rs)
                except:
                    print('Skipping bad image: ',img_name)
                    invalid_count += 1
            img1 = np.array(all_imgs)
            #print(img1.shape)
            img1= np.reshape(img1,(img1.shape[1],img1.shape[2],3))
            img_resized = cv2.resize(img1,(299,299))
            return img_resized
    def model_predict(self,img,model):
        top_n=5
        x=np.reshape(img,(1,299,299,3))
        x =self.process_image(x.astype('float32'))   
        y_pred = model.predict(x)
        #print(x.shape)
        preds = np.argmax(y_pred, axis=1)
        score = y_pred[0][preds[0]]
        top_n_preds= np.argpartition(y_pred, -top_n)[:,-top_n:]
        pred_class = ix_to_class[str(preds[0])]
        result ={}
        for i in top_n_preds[0]:
            pred_class = ix_to_class[str(i)]
            score = y_pred[0][i]
            result[str(pred_class)]=score
        sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)   
        return sorted_result


    def main(self):
        img = self.load_images()
        result= self.model_predict(img,self.model)
        return result
