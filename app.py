import streamlit as st
import os
from PIL import Image
from main import extract_feature
import keras
from keras.applications.resnet import ResNet50,preprocess_input
from keras.layers import GlobalMaxPool2D
import pickle
import numpy as np
from main import recommend

model=ResNet50(weights="imagenet",include_top=False,input_shape=(224,224,3))
model.trainable=False
model=keras.Sequential([
    model,
    GlobalMaxPool2D()
])
feature_list=np.array(pickle.load(open("embedding.pkl","rb")))
filename=pickle.load(open("filenames.pkl","rb"))
st.title("Welcome to this system")



def save_upload_file(uploaded_file):
    try:
        with open(os.path.join("upload",uploaded_file.name),"wb") as f:
            f.write(uploaded_file.getbuffer())
            return 1
    except:
        return 0

uploaded_file=st.file_uploader("Choose an image")
if uploaded_file is not None:
    if save_upload_file(uploaded_file):
        display_image=Image.open(uploaded_file)
        st.image(display_image)


        feature=extract_feature(os.path.join("upload",uploaded_file.name),model)
        indices=recommend(feature,feature_list)

        col1,col2,col3,col4,col5=st.columns(5)

        with col1:
            st.image(filename[indices[0][0]])
        with col2:
            st.image(filename[indices[0][1]])
        with col3:
            st.image(filename[indices[0][2]])
        with col4:
            st.image(filename[indices[0][3]])
        with col5:
            st.image(filename[indices[0][4]])
    else:
        st.header("some error occured")