import base64
from distutils import extension
import os
import sys
import random
import hashlib
import threading
import webbrowser
import shutil

from datetime import datetime
from flask import Flask, render_template, redirect, jsonify, url_for, request, session

sys.path.append(os.path.abspath('./python/'))
sys.path.append(os.path.abspath('./models/'))

import utils

import system_users as su
import trained_classes as tc
import diseases_and_treatments as dat

import efarmer_detection as detect

app = Flask(__name__)

app.secret_key = "efarmer"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# Route for login


@app.route('/login')
def login():
    if 'userId' in session:
        return redirect('index')

    return render_template('login.html')


# Route for index/home page
@app.route('/')
@app.route('/index')
def index():
    if 'userId' not in session:
        return redirect('login')

    details = dat.get_all_diseases_and_treatments()

    trained_classes_count = len(tc.get_all_trained_classes())
    diseases_and_treatments_count = len(details)
    system_users_count = len(su.get_all_system_users())

    return render_template('index.html', details=details,
                           trained_classes_count=trained_classes_count,
                           diseases_and_treatments_count=diseases_and_treatments_count,
                           system_users_count=system_users_count)


# Diseases
@app.route('/all_diseases')
def all_diseases():
    if 'userId' not in session:
        return redirect('login')

    details = dat.get_all_diseases_and_treatments()
    return render_template('all_diseases.html', details=details)


@app.route('/add_disease')
def add_disease():
    if 'userId' not in session:
        return redirect('login')

    return render_template('add_disease.html')


@app.route('/view_disease')
def view_disease():
    if 'userId' not in session:
        return redirect('login')

    id = request.args.get('id', default="")
    if id == "":
        return redirect('all_diseases')

    details = dat.get_diseases_and_treatments_details(id)
    return render_template('view_disease.html', details=details)


# System user
@app.route('/all_system_users')
def all_system_users():
    if 'userId' not in session:
        return redirect('login')

    users = su.get_all_system_users_without_login(session['userId'])
    return render_template('all_system_users.html', users=users)


@app.route('/add_system_user')
def add_system_user():
    if 'userId' not in session:
        return redirect('login')

    return render_template('add_system_user.html')


@app.route('/view_system_user')
def view_system_user():
    if 'userId' not in session:
        return redirect('login')

    id = request.args.get('id', default="")
    if id == "":
        return redirect('all_system_users')

    details = su.get_system_user_details(id)
    return render_template('view_system_user.html', details=details)


# Trained classes
@app.route('/all_classes')
def all_classes():
    if 'userId' not in session:
        return redirect('login')

    classes = tc.get_all_trained_classes()
    return render_template('all_classes.html', classes=classes)


@app.route('/add_class')
def add_class():
    if 'userId' not in session:
        return redirect('login')

    return render_template('add_class.html')


@app.route('/view_class')
def view_class():
    if 'userId' not in session:
        return redirect('login')

    id = request.args.get('id', default="")
    if id == "":
        return redirect('all_classes')

    details = tc.get_trained_class_details(id)
    return render_template('view_class.html', details=details)


# Model
@app.route('/change_model')
def change_model():
    if 'userId' not in session:
        return redirect('login')

    return render_template('change_model.html')


# Profile
@app.route('/profile')
def profile():
    if 'userId' not in session:
        return redirect('login')

    details = su.get_system_user_details(session['userId'])
    return render_template('profile.html', details=details)


@app.route('/change_psw')
def change_psw():
    if 'userId' not in session:
        return redirect('login')

    return render_template('change_psw.html')


# @app.route('/prediction')
# def prediction():
#     return render_template('prediction.html')


# Route for system login
@app.route('/system_login', methods=['GET', 'POST'])
def system_login():

    if request.method == "POST":

        if 'userId' in session:
            return jsonify({'redirect': url_for('index')})

        else:
            email = request.form.get('email')
            psw = request.form.get('psw')

            if len(email) == 0 or len(psw) == 0:
                return jsonify({'error': "Fields are empty!"})

            else:
                # Check login
                details = su.system_users_login(
                    email, hashlib.md5(psw.encode()).hexdigest())
                if len(details) < 1:
                    return jsonify({'error': "Email or Password incorrect!"})

                else:
                    session['userId'] = str(details[0][0])
                    return jsonify({'redirect': url_for('index')})

    return jsonify({'redirect': url_for('login')})


@app.route('/logout')
def logout():
    if 'userId' in session:
        session.pop('userId', None)

    return redirect("login")


# Route for add system user
@app.route('/add_system_user_details', methods=['GET', 'POST'])
def add_system_user_details():

    if request.method == "POST":

        if 'userId' in session:

            name = request.form.get('name')
            email = request.form.get('email')
            psw = request.form.get('psw')

            if len(name) == 0 or len(email) == 0 or len(psw) == 0:
                return jsonify({'error': "Fields are empty!"})

            else:

                if (su.check_email_exist(email)[0][0]) < 1:

                    if su.add_system_user(name, email, hashlib.md5(psw.encode()).hexdigest()) < 1:
                        return jsonify({'error': "System user not added. Try again!"})

                    else:
                        return jsonify({'success': "System user added!"})

                else:
                    return jsonify({'error': "This email exist!"})

    return jsonify({'redirect': url_for('index')})


# Route for remove system user
@app.route('/remove_system_user', methods=['GET', 'POST'])
def remove_system_user():

    if request.method == "POST":

        if 'userId' in session:

            id = request.form.get('id')

            if len(id) == 0:
                return jsonify({'error': "System user not selected!"})

            else:

                if (su.check_system_user_exist_by_id(id)[0][0]) > 0:

                    if su.delete_system_user(id) < 1:
                        return jsonify({'error': "System user not removed. Try again!"})

                    else:
                        return jsonify({'success': "System user removed!"})

                else:
                    return jsonify({'error': "User not exist!"})

    return jsonify({'redirect': url_for('index')})


# Route for update account details
@app.route('/update_profile_details', methods=['GET', 'POST'])
def update_profile_details():

    if request.method == "POST":

        if 'userId' in session:

            name = request.form.get('name')

            if len(name) == 0:
                return jsonify({'error': "Fields are empty!"})

            else:

                id = session['userId']
                if su.update_system_user_details(id, name) < 1:
                    return jsonify({'error': "Account not updated. Try again!"})

                else:
                    return jsonify({'success': "Account updated!"})

    return jsonify({'redirect': url_for('index')})


# Route for update account psw
@app.route('/update_profile_psw', methods=['GET', 'POST'])
def update_profile_psw():

    if request.method == "POST":

        if 'userId' in session:

            psw = request.form.get('psw')
            cpsw = request.form.get('cpsw')

            if len(psw) == 0 or len(cpsw) == 0:
                return jsonify({'error': "Fields are empty!"})

            if psw != cpsw:
                return jsonify({'error': "Password and confirm password not matched!"})

            else:

                id = session['userId']
                if su.update_system_user_psw(id, hashlib.md5(psw.encode()).hexdigest()) < 1:
                    return jsonify({'error': "Account password not updated. Try again!"})

                else:
                    return jsonify({'success': "Account password updated!"})

    return jsonify({'redirect': url_for('index')})


# Route for add system user
@app.route('/add_trained_class', methods=['GET', 'POST'])
def add_trained_class():

    if request.method == "POST":

        if 'userId' in session:

            disease_name = request.form.get('disease_name')
            plant_name = request.form.get('plant_name')
            today_date_date = datetime.now().strftime("%Y-%m-%d")

            if len(disease_name) == 0 or len(plant_name) == 0:
                return jsonify({'error': "Fields are empty!"})

            else:

                if tc.add_trained_class(disease_name, plant_name, today_date_date) < 1:
                    return jsonify({'error': "Trained class not added. Try again!"})

                else:
                    return jsonify({'success': "Trained class added!"})

    return jsonify({'redirect': url_for('index')})


# Route for update trained class details
@app.route('/update_trained_class', methods=['GET', 'POST'])
def update_trained_class():

    if request.method == "POST":

        if 'userId' in session:

            id = request.form.get('id')
            disease_name = request.form.get('disease_name')
            plant_name = request.form.get('plant_name')

            if len(disease_name) == 0 or len(plant_name) == 0:
                return jsonify({'error': "Fields are empty!"})

            else:

                if tc.update_trained_class_update(id, disease_name, plant_name) < 1:
                    return jsonify({'error': "Trained class not updated. Try again!"})

                else:
                    return jsonify({'success': "Trained class updated!"})

    return jsonify({'redirect': url_for('index')})


# Route for remove trained class
@app.route('/remove_trained_class', methods=['GET', 'POST'])
def remove_trained_class():

    if request.method == "POST":

        if 'userId' in session:

            id = request.form.get('id')

            if len(id) == 0:
                return jsonify({'error': "Trained class not selected!"})

            else:

                if tc.delete_trained_class(id) < 1:
                    return jsonify({'error': "Trained class not removed. Try again!"})

                else:
                    return jsonify({'success': "Trained class removed!"})

    return jsonify({'redirect': url_for('index')})


# Route for add disease and treatments
@app.route('/add_disease_and_treatments', methods=['GET', 'POST'])
def add_disease_and_treatments():

    if request.method == "POST":

        plant_name = request.form.get('plant')
        disease_name = request.form.get('disease')
        details = request.form.get('details')
        treatments = request.form.get('treatments')
        image = request.files.get('image')

        if (len(plant_name) == 0 or len(disease_name) == 0
                or len(details) == 0 or len(treatments) == 0 or image == None):
            return jsonify({'error': "Fields are empty!"})

        else:

            # Save image
            save_folder = app.static_folder + '/diseases_and_treatments/'

            if not os.path.exists(save_folder):
                os.makedirs(save_folder)

            image_name_front = plant_name + "_" + disease_name + "_"
            image_name = save_file(image, save_folder, image_name_front)

            if dat.add_diseases_and_treatments(plant_name, disease_name, details, treatments, image_name) < 1:
                return jsonify({'error': "Disease and treatments not added!"})

            else:
                return jsonify({'success': "Disease and treatments added!"})

    return jsonify({'redirect': url_for('index')})


# Route for remove diseases and treatment
@app.route('/remove_diseases_and_treatments', methods=['GET', 'POST'])
def remove_diseases_and_treatments():

    if request.method == "POST":

        if 'userId' in session:

            id = request.form.get('id')

            if len(id) == 0:
                return jsonify({'error': "Disease & Treatment not selected!"})

            else:

                if dat.delete_diseases_and_treatments(id) < 1:
                    return jsonify({'error': "Disease & Treatment not removed. Try again!"})

                else:
                    return jsonify({'success': "Disease & Treatment removed!"})

    return jsonify({'redirect': url_for('index')})


# Route for add disease and treatments
@app.route('/update_disease_and_treatments', methods=['GET', 'POST'])
def update_disease_and_treatments():

    if request.method == "POST":

        id = request.form.get('id')
        plant_name = request.form.get('plant')
        disease_name = request.form.get('disease')
        details = request.form.get('details')
        treatments = request.form.get('treatments')

        if (len(plant_name) == 0 or len(disease_name) == 0
                or len(details) == 0 or len(treatments) == 0):
            return jsonify({'error': "Fields are empty!"})

        else:

            if dat.update_diseases_and_treatments_update(id, plant_name, disease_name, details, treatments) < 1:
                return jsonify({'error': "Disease and treatments not update!"})

            else:
                return jsonify({'success': "Disease and treatments update!"})

    return jsonify({'redirect': url_for('index')})


# Route for add disease and treatments image
@app.route('/update_disease_and_treatments_image', methods=['GET', 'POST'])
def update_disease_and_treatments_image():

    if request.method == "POST":

        id = request.form.get('id')
        plant_name = request.form.get('plant')
        disease_name = request.form.get('disease')
        image = request.files.get('image')

        if (len(plant_name) == 0 or len(disease_name) == 0
                or len(id) == 0 or image == None):
            return jsonify({'error': "Fields are empty!"})

        else:

            # Save image
            save_folder = app.static_folder + '/diseases_and_treatments/'

            if not os.path.exists(save_folder):
                os.makedirs(save_folder)

            image_name_front = plant_name + "_" + disease_name + "_"
            image_name = save_file(image, save_folder, image_name_front)

            if dat.update_diseases_and_treatments_image_update(id, image_name) < 1:
                return jsonify({'error': "Disease and treatments image not updated!"})

            else:
                return jsonify({'success': "Disease and treatments image updated!"})

    return jsonify({'redirect': url_for('index')})


# Route for change model
@app.route('/model_change', methods=['GET', 'POST'])
def model_change():

    if request.method == "POST":

        model = request.files.get('model')
        pickle = request.files.get('pickle')

        if (model == None or pickle == None):
            return jsonify({'error': "Fields are empty!"})

        else:

            folder_path = APP_ROOT + "/python/detection/"

            try:

                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                model_name = save_file(
                    file=model, save_folder=folder_path, file_name="model")
                pickle_name = save_file(
                    file=pickle, save_folder=folder_path, file_name="pickle")

                return jsonify({'success': "Model changed!"})

            except Exception as e:
                return jsonify({'error': "Some error occur! " + str(e)})

    return redirect("index")


# APIs
# # Get classes
# @app.route('/api/classes', methods=['GET', 'POST'])
# def classes():

#     details = tc.get_all_trained_classes()
#     return jsonify(details)


# Get diseases and treatments
@app.route('/api/diseases_and_treatments', methods=['GET', 'POST'])
def diseases_and_treatments():

    details = dat.get_all_diseases_and_treatments()
    return jsonify(details)


# Get diseases and treatments by id
@app.route('/api/diseases_and_treatments/<id>', methods=['GET', 'POST'])
def diseases_and_treatments_by_id(id):

    details = dat.get_diseases_and_treatments_details(id)
    return jsonify(details)


# Detect diseases
@app.route('/api/detect_disease', methods=['GET', 'POST'])
def detect_disease():

    image = request.json['image']

    if image == None:
        return jsonify({'error': "Image not uploaded"})

    else:

        today_date = str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))

        # Get random number
        random_no = str(random.randint(100000, 999999))

        # Paths
        folder_name = today_date + "_" + random_no + "/"
        folder_path = APP_ROOT + '/static/detection/' + folder_name
        uploaded_img_path = folder_path + '/images/'

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        if not os.path.exists(uploaded_img_path):
            os.makedirs(uploaded_img_path)

        filename = "uploaded_image_file.png"

        img_url = uploaded_img_path + "/" + filename
        with open(img_url, "wb") as fh:
            fh.write(base64.b64decode(image))

        try:
            # Getting prediction
            plant_name, disease_name, predict_accuracy = detect.detect_disease(
                folder_path)

            data = {"plant": plant_name, "disease": disease_name,
                    "accuracy": predict_accuracy}

            shutil.rmtree(folder_path)

            return jsonify(data)

        except Exception as ex:
            print(f"Detection Exception - {str(ex)}")
            return jsonify({'error': "Some error occur!"})


# Function for save files
def save_file(file, save_folder, image_name_front="", file_name=""):
    if file != None:
        file_save_name = file.filename

        if image_name_front != "":
            file_save_name = image_name_front + file_save_name

        if file_name != "":
            extension = os.path.splitext(file_save_name)[1]
            file_save_name = file_name + extension

        file.save(save_folder + file_save_name)

    else:
        file_save_name = None

    return str(file_save_name)


# Main
if __name__ == '__main__':

    port = "5000"
    host = "0.0.0.0"
    app.run(host=host, port=port, debug=True)
