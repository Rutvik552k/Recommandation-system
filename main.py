from locale import normalize
import tensorflow as tf
import keras
from keras.applications.resnet import ResNet50,preprocess_input
from keras.layers import GlobalMaxPool2D
from keras.preprocessing import image
import numpy as np
from numpy.linalg import norm
import os
from keras.utils import load_img,img_to_array
import pickle
from sklearn.neighbors import NearestNeighbors



model=ResNet50(weights="imagenet",include_top=False,input_shape=(224,224,3))
model.trainable=False
model=keras.Sequential([
    model,
    GlobalMaxPool2D()
])

def extract_feature(img_path,model):
    img=load_img(img_path,target_size=(224,224))
    img_array=img_to_array(img)
    expanded_img_array=np.expand_dims(img_array,axis=0)
    preprocessed_image=preprocess_input(expanded_img_array)
    result=model.predict(preprocessed_image).flatten()
    normalized_result=result/norm(result)
    return normalized_result

def recommend(feature,feature_list):
    neighbors=NearestNeighbors(n_neighbors=5,algorithm="brute",metric='euclidean')
    neighbors.fit(feature_list)

    distance,indices=neighbors.kneighbors([feature])
    return indices


model.save("Recommanded_model")

file_names=[]
for file in os.listdir("image"):
    file_names.append(os.path.join("image",file))

feature_list=[]

for file in file_names:
    feature_list.append(extract_feature(file,model=model))



pickle.dump(feature_list,open("embedding.pkl","wb"))
pickle.dump(file_names,open("filenames.pkl","wb"))
