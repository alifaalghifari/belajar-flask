from json import load
from unittest import result
from flask import (Flask, flash, make_response,
                   redirect, render_template, request, session, url_for, jsonify
                   )
from keras.models import load_model
from keras.preprocessing import image
import tensorflow as tf
import numpy as np
import struct
from PIL import Image
import os

app = Flask(__name__)
app.secret_key = "randomstring"

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
# app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'

model = load_model('my_model.h5')


@app.route("/")
def index():
    search = request.args.get('search')
    return render_template('index.html', search=search)


@app.route('/setting')
def show_setting():
    return "halo kamu di halaman setting"


@app.route('/profile/<username>')
def show_profile(username):
    return render_template('profile.html',  username=username)


@app.route('/blog/<int:blog_id>')
def show_blog(blog_id):
    return 'halo kamu di blog nomer %d' % blog_id


@app.route('/login', methods=['GET', 'POST'])
def show_login():
    if request.method == "POST":
        # cookie
        # resp = make_response("Email kamu adalah " + request.form["email"])
        # resp.set_cookie('email_user', request.form["email"])

        # sesion
        session['username'] = request.form['email']

        # flash message
        flash("Kamu berhasil login!", "success")
        return redirect(url_for('show_profile', username=session['username']))

        # return resp

    if 'username' in session:
        username = session['username']
        return redirect(url_for('show_profile', username=username))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('show_login'))


@app.route('/getcookie')
def get_cookie():
    email = request.cookies.get('email_user')
    return "Email yang tersimpan di cookie adalah " + email


# @app.route('/tesmodel', methods=['GET', 'POST'])
# def tes_model():
#     # if request.method == "POST":
#     # images = request.form['img']
#     img = tf.keras.preprocessing.image.load_img(
#         'static/images.jpg', target_size=(224, 224))
#     # print(images)
#     x = tf.keras.preprocessing.image.img_to_array(img)
#     x = np.expand_dims(x, axis=0)

#     images = np.vstack([x])
#     classes = model.predict(images, batch_size=10)
#     result = np.argmax(classes[0])
#     return "hasil " + str(classes[0])
#     # return render_template('sendImage.html')


@app.route('/tesmodel', methods=['GET', 'POST'])
def tes_model():
    if request.method == "POST":
        images = request.files['img']
        # app.logger.info(images.stream.read())

        # # print(images)

        # img = images.stream.read()
        # print(f'img {type(img)}')
        # app.logger.info(img.decode('utf-8', 'ignore'))
        # print(img)
        # img = str(img, 'UTF-8')
        # tes = struct.unpack('<HH', img)
        # with open(img, encoding="utf8", errors='ignore') as f:
        #     print(f.read())
        # img = tf.keras.preprocessing.image.array_to_img(
        #     img.decode('utf-8', 'ignore'))

        # save file
        if images.filename != '':
            images.save(os.path.join(
                app.config['UPLOAD_PATH'], images.filename))

        img = tf.keras.preprocessing.image.load_img(
            os.path.join(
                app.config['UPLOAD_PATH'], images.filename), target_size=(224, 224))
        x = tf.keras.preprocessing.image.img_to_array(img)
        x = np.expand_dims(x, axis=0)

        img = np.vstack([x])
        classes = model.predict(img, batch_size=10)
        result = np.argmax(classes[0])

        # menghapus file
        os.remove(os.path.join(
            app.config['UPLOAD_PATH'], images.filename))
        return 'hasil training : ' + str(classes) + ' hasil akhir : ' + str(result)
    return render_template('sendImage.html')


if __name__ == '__main__':
    app.run(debug=True)
