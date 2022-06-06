# Import libraries
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image

import numpy as np
import os
import pandas as pd
import pickle

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


# Function for detect vegetable plant disease
def detect_disease(folder_path):

    test_data = folder_path
    img_width = 224
    img_height = 224
    model_path = APP_ROOT + "/detection/model.h5"
    pickle_path = APP_ROOT + "/detection/pickle.pkl"

    # Load trained model
    model = keras.models.load_model(model_path)
    print(model.summary())

    # Generate data for prediction
    predict_data_generator = ImageDataGenerator(rescale=1. / 255)
    predict_generator = predict_data_generator.flow_from_directory(
        test_data,
        shuffle=False,
        target_size=(img_height, img_width))

    # Getting prediction
    predictions = model.predict_generator(predict_generator)
    predicted_class = np.argmax(predictions, axis=1)

    # Load pickle and get predicted class name
    init_dic = pickle.load(open(pickle_path, 'rb'))
    swap_dict = dict([(value, key) for key, value in init_dic.items()])

    predClassArray = []
    for class_indices in predicted_class:
        predClassArray.append(swap_dict.get(class_indices))

    # Calculate accuracy
    predPercentArray = []
    for predPercentage in predictions:
        predPercentArray.append("{0:0.1f}".format(
            (np.max(predPercentage) / np.sum(predPercentage) * 100)))

    # Create result set
    prediction = pd.DataFrame({'IMAGE_NAME': predict_generator.filenames,
                               'PREDICTED_CLASS': predClassArray, 'SCORE': predPercentArray})

    predict_class = str(prediction['PREDICTED_CLASS'][0])
    predict_accuracy = int(float(prediction['SCORE'][0]))

    plant_name = predict_class.split("___")[0].upper()
    disease_name = predict_class.split("___")[1].replace("_", " ").upper()

    return plant_name, disease_name, predict_accuracy
