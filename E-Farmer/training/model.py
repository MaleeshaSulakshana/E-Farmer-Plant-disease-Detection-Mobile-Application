# Tf library
import tensorflow as tf
from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Flatten, Dense
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

# Other library
import os
import json
import time
import sys


# Function for create folder structure
def create_folders():
    # Get date and time
    t = time.localtime()
    date_time = time.strftime("%Y_%m_%d_%H_%M_%S", t)

    # Model save path
    model_name = "oil_spill_classification_" + date_time
    model_path = "saved_model/" + model_name
    save_model_path = model_path + "/" + model_name + ".h5"

    # Json file path
    classes_folder = "classes_" + date_time + "/"
    classes_save_name = "classes/" + classes_folder
    classes_path = classes_save_name + "classes.json"

    if not os.path.exists(model_path):
        os.makedirs(model_path)

    if not os.path.exists(classes_save_name):
        os.makedirs(classes_save_name)

    return save_model_path, classes_path


def train_model():
    save_model_path, classes_path = create_folders()

    train_data_path = r"..\dataset\train"
    img_width = 224
    img_height = 224
    batch_size = 4
    val_split = 0.3
    epochs = 10

    # Get classes count
    list = os.listdir(train_data_path)
    classes_count = len(list)

    # Load model weights
    model = VGG19(weights='imagenet', include_top=False,
                  input_shape=(img_width, img_height, 3))

    # Select layers from weight model
    for layer in model.layers[:-5]:
        layer.trainable = False

    # Set input and output layers
    layers = model.output
    layers = Flatten()(layers)
    layers = Dense(classes_count, activation="softmax")(layers)

    custom_Model = Model(inputs=model.input, outputs=layers)

    # Cerate genarators
    train_datagen = ImageDataGenerator(rescale=1. / 255,
                                       shear_range=0.2,
                                       zoom_range=0.2,
                                       horizontal_flip=True,
                                       validation_split=val_split)

    train_generator = train_datagen.flow_from_directory(
        train_data_path,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='categorical',
        subset='training')

    validation_generator = train_datagen.flow_from_directory(
        train_data_path,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation')

    print("** Create Generators **")

    # Create class dictionary
    init_dic = dict(train_generator.class_indices.items())

    # Save classes in json
    dict_classes = dict([(value, key) for key, value in init_dic.items()])

    with open(classes_path, 'w') as outfile:
        json.dump(dict_classes, outfile)

    # Compile model
    base_learning_rate = 0.00001
    custom_Model.compile(loss='categorical_crossentropy',
                         optimizer=tf.keras.optimizers.Adam(
                             lr=base_learning_rate, clipnorm=0.001),
                         metrics=['accuracy'])

    # Save our model using specified conditions
    cp = ModelCheckpoint(save_model_path, monitor='val_acc', verbose=1,
                         save_best_only=False, save_weights_only=False, mode='auto', period=1)

    # Set early stopping
    es = EarlyStopping(monitor='val_acc', min_delta=0,
                       patience=10, verbose=1, mode='auto')

    print(f"** Training Started **")

    trained_Model = ''

    # Model traning
    try:
        trained_Model = custom_Model.fit_generator(
            train_generator,
            epochs=epochs,
            validation_data=validation_generator,
            callbacks=[es, cp]
        )

    except:
        print(f"** Training Not Success **")
        sys.exit(1)

    print(f"** Training Completed **")


# Run code
if __name__ == "__main__":
    train_model()
