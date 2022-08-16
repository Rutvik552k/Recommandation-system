# from fileinput import filename
# from main import extract_feature
import pickle 
from keras.applications.resnet import ResNet50,preprocess_input
from keras.layers import GlobalMaxPool2D
import tensorflow as tf
import keras
from sklearn.neighbors import NearestNeighbors
import numpy as np
import cv2
from keras.utils import load_img,img_to_array
from numpy.linalg import norm
from main import recommend

model=ResNet50(weights="imagenet",include_top=False,input_shape=(224,224,3))
model.trainable=False
model=keras.Sequential([
    model,
    GlobalMaxPool2D()
])

feature_list=np.array(pickle.load(open("embedding.pkl","rb")))
filename=pickle.load(open("filenames.pkl","rb"))

img_path="sample.png"
img=load_img(img_path,target_size=(224,224))
img_array=img_to_array(img)
expanded_img_array=np.expand_dims(img_array,axis=0)
preprocessed_image=preprocess_input(expanded_img_array)
result=model.predict(preprocessed_image).flatten()
normalized_result=result/norm(result)



indices=recommend(normalized_result,feature_list)

for file in indices[0]:
    temp_img=cv2.imread(filename[file])
    cv2.imshow("output",cv2.resize(temp_img,(512,512)))

    cv2.waitKey(0)

