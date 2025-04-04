from flask import render_template,flash,request,redirect,session,url_for
from packages import app
from flask_bcrypt import Bcrypt
from packages.admin_forms import AdminLogin,AdminRegister
from packages.models import Admin,db,User,Artists,Songs
from werkzeug.security import generate_password_hash,check_password_hash


bcrypt = Bcrypt(app)

@app.after_request
def after_request(response):
    response.headers['Cache-Control']='no-cache','no-store','must-revalidate'
    return response

@app.errorhandler(404)
def pagenotfound(error):
    return render_template('/Admin/pagenotfound_error.html'), 404


@app.errorhandler(500)
def error505(error):
    return render_template('/Admin/500_error.html'), 500

@app.errorhandler(503)
def error503(error):
    return render_template('/Admin/503_error.html'), 503

@app.route('/admin/index/')
def admin_index():
    return render_template('Admin/index.html')


@app.route('/admin/songs/')
def admin_songs():
    return render_template('Admin/songs.html')



@app.route('/admin/login/', methods=['GET', 'POST'])
def admin_login():
    form = AdminLogin()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            pwd = form.password.data
            admin = Admin.query.filter_by(username=username).first()
            if admin:
                if bcrypt.check_password_hash(admin.password, pwd):
                    session['username'] = admin.id  # Store the admin's ID in the session
                    return redirect('/Admin/admindash/')
                else:
                    flash('Incorrect password', category='error')
            else:
                flash('Admin not found', category='error')
    return render_template('Admin/login.html', form=form)


@app.route('/admin/register/', methods=['GET', 'POST'])
def admin_register():
    form = AdminRegister()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            pwd = form.password.data
            hashed_password = bcrypt.generate_password_hash(pwd).decode('utf-8')
            admin = Admin(username=username, email=email, password=hashed_password)
            db.session.add(admin)
            db.session.commit()
            session['username'] = admin.id  # Store the admin's ID in the session
            return redirect('/Admin/admindash/')
    return render_template('Admin/register.html', form=form)

@app.route('/admin/logout/')
def admin_logout():
    session.clear() 
    flash('You have been logged out.', category='success')
    return redirect('/admin/login/')

@app.route('/Admin/admindash/')
def admin_dashboard():
    admin = Admin.query.get(session['username'])
    return render_template('Admin/admin_dash.html', admin=admin)

@app.route('/admin/user/')
def admin_user():
    users = db.session.query(User).filter(User.users_role=='Users').all()
    users_count = len(users)
    return render_template('Admin/users.html',users=users,users_count=users_count)


@app.route('/admin/artists/')
def admin_artists():
    artists = db.session.query(Artists).all()
    artist_count = len(artists)
    return render_template('Admin/artists.html',artists=artists,artist_count=artist_count)

@app.route('/admin/scorers/')
def admin_scorer():
    scorers = db.session.query(User).filter(User.users_role=='Scorers').all()
    scorers_count = len(scorers)
    return render_template('Admin/scorers.html',scorers=scorers,scorers_count=scorers_count)

@app.route('/users/<int:users_id>/details/')
def users_details(users_id):
    user = User.query.get_or_404(users_id)
    return render_template('Admin/user_details.html', user=user)

@app.route('/admin/artist/<int:artist_id>/details/')
def admin_artist_details(artist_id):
    artist = Artists.query.get_or_404(artist_id)
    return render_template('Admin/artist_details.html', artist=artist)

@app.route('/users/<int:users_id>/delete/')
def users_delete(users_id):
    users=db.session.query(User).get(users_id)
    db.session.delete(users)
    db.session.commit()
    return redirect('/admin/user/')

@app.route('/admin/artist/<int:artist_id>/delete/')
def admin_artist_delete(artist_id):
    artists=db.session.query(Artists).get(artist_id)
    db.session.delete(artists)
    db.session.commit()
    return redirect('/admin/artists/')

@app.route('/admin/approve-song/<int:song_id>')
def approve_song(song_id):
    song = db.session.query(Songs).filter(Songs.songs_id==song_id).first()
    if song:
        song.approved = True
        db.session.commit()
        flash('Song approved successfully!', 'success')
    else:
        flash('Song not found!', 'error')
    return redirect(url_for('admin_dashboard'))
