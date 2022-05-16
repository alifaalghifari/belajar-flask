from flask import (Flask, flash, make_response,
                   redirect, render_template, request, session, url_for
                   )
app = Flask(__name__)
app.secret_key = "randomstring"


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
