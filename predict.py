import matplotlib.image as mpimg
import numpy as np
import tensorflow as tf
from tensorflow import keras


model = keras.models.load_model('models/mnist.h5')


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.299, 0.587, 0.114])


def mnist_predict(imgFile):
    img = mpimg.imread(imgFile)
    img = rgb2gray(img).reshape((-1, 28, 28, 1))
    prob_vec = model.predict(img).ravel()
    result = tf.argmax(prob_vec).numpy().item()

    return result, prob_vec[result]
