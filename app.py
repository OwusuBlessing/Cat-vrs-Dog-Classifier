from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
import keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image
import  tensorflow
from tensorflow.keras.utils import load_img

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
import cv2
from PIL import Image

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'C:/Users/user/Desktop/DL_projects/Free Code_CAMP_projects/Cat vrs Dog/cats_and_dogs_small_augment2.h5'

# Load your trained model

model = keras.models.load_model("C:/Users/user/Desktop/DL_projects/Free Code_CAMP_projects/Cat vrs Dog/cats_and_dogs_small_augment2.h5")        # Necessary
# print('Model loaded. Start serving...')
print('Model loaded. Check http://127.0.0.1:5000/')


def model_predict(img_path, model):
    img = np.array(Image.open(img_path).resize((224,224)))
    #img = load_img(img_path, target_size=(224, 224))

    # Preprocessing the image

    #x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    x = np.expand_dims(img, axis=0)

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    x = preprocess_input(x, mode='caffe')
    preds = model.predict(x)
    result = int(preds[0][0])
    return result


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'Uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        result = model_predict(file_path, model)

        # Process your result for human
        # pred_class = preds.argmax(axis=-1)            # Simple argmax
        if result == 0:
            return "This is likely to be a cat"
        else:
            return "This is likely to be a dog"
           
    return None


if __name__ == '__main__':
    app.run(debug=True)

