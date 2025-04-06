import secrets
from flask_wtf.csrf import CSRFProtect
from flask import render_template,flash,request,redirect,session,url_for
from packages import app
from flask_bcrypt import Bcrypt
from packages.admin_forms import AdminLogin,DpForm,SongForm
from packages.models import Admin,db,User,Artists,Songs,Song_solfa,SongsRequest
csrf = CSRFProtect()
csrf.init_app(app)
bcrypt = Bcrypt(app)

@app.after_request
def after_request(response):
    response.headers['Cache-Control']='no-cache','no-store','must-revalidate'
    return response

@app.errorhandler(404)
def pagenotfound(error):
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    return render_template('/Admin/pagenotfound_error.html', admin=admin), 404


@app.errorhandler(500)
def error505(error):
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    return render_template('/Admin/500_error.html',admin=admin), 500

@app.errorhandler(503)
def error503(error):
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    return render_template('/Admin/503_error.html',admin=admin), 503

@app.route('/admin/index/')
def admin_index():
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    return render_template('Admin/index.html',admin=admin)


@app.route('/admin/songs/')
def admin_songs():
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    songs=Songs.query.order_by(Songs.songs_id.desc()).all()
    return render_template('Admin/songs.html',admin=admin,songs=songs)


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
                    session['username'] = admin.id
                    flash(f'{admin.username},You are now logged in', category='success')
                    return redirect('/admin/admindash/')
                else:
                    flash('Incorrect password', category='error')
            else:
                flash('Admin not found', category='error')
    return render_template('Admin/login.html', form=form)

@app.route('/admin/logout/')
def admin_logout():
    session.clear() 
    flash('You have been logged out.', category='success')
    return redirect('/admin/login/')



@app.route('/admin/admindash/')
def admindash():
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    songs = Songs.query.all()
    return render_template('Admin/admin_dash.html', admin=admin,songs=songs)
       

@app.route('/admin/user/')
def admin_user():
    users = db.session.query(User).filter(User.users_role=='Users').all()
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    users_count = len(users)
    return render_template('Admin/users.html',users=users,users_count=users_count,admin=admin)


@app.route('/admin/artists/')
def admin_artists():
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    artists = db.session.query(Artists).all()
    artist_count = len(artists)
    return render_template('Admin/artists.html',artists=artists,artist_count=artist_count,admin=admin)

@app.route('/admin/scorers/')
def admin_scorer():
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    scorers = db.session.query(User).filter(User.users_role=='Scorers').all()
    scorers_count = len(scorers)
    return render_template('Admin/scorers.html',scorers=scorers,scorers_count=scorers_count,admin=admin)

@app.route('/users/<int:users_id>/details/')
def users_details(users_id):
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    user = User.query.get_or_404(users_id)
    return render_template('Admin/user_details.html', user=user,admin=admin)

@app.route('/admin/artist/<int:artist_id>/details/')
def admin_artist_details(artist_id):
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    artist = Artists.query.get_or_404(artist_id)
    return render_template('Admin/artist_details.html', artist=artist,admin=admin)

@app.route('/users/<int:users_id>/delete/')
def users_delete(users_id):
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    users=db.session.query(User).get(users_id)
    db.session.delete(users)
    db.session.commit()
    return redirect('/admin/user/',admin=admin)

@app.route('/admin/artist/<int:artist_id>/delete/')
def admin_artist_delete(artist_id):
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    artists=db.session.query(Artists).get(artist_id)
    db.session.delete(artists)
    db.session.commit()
    return redirect('/admin/artists/',admin=admin)

@app.route('/admin/approve-song/<int:song_id>')
def approve_song(song_id):
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    song = db.session.query(Songs).filter(Songs.songs_id==song_id).first()
    if song:
        song.approved = True
        db.session.commit()
        flash('Song approved successfully!', 'success')
    else:
        flash('Song not found!', 'error')
    return redirect(url_for('admin_dashboard'),admin=admin)


@app.route('/admin/upload/dp/', methods=['GET', 'POST'])
def adminupload_db():
    dpform = DpForm()
    adminid = session.get('username')
    if adminid==None:
        return redirect(url_for('admin_login'))
    admin = db.session.query(Admin).get(adminid)
    if request.method == 'GET':
        return render_template('Admin/upload_dp.html', admin=admin, dpform=dpform)
    else:
        if dpform.validate_on_submit():
            file = dpform.photo.data
            filename = file.filename
            extension = filename.split('.')
            ext = extension[-1]
            generated_filename = secrets.token_urlsafe() + '.' + ext
            file.save('packages/static/uploads/' + generated_filename)
            admin.dp = generated_filename
            db.session.commit()
            return redirect('/admin/admindash/')
        else:
            return render_template('Admin/upload_dp.html',admin=admin, dpform=dpform)

@app.route('/admin/edit/', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'GET':
        admin = Admin.query.get(session['username'])
        return render_template('Admin/profile_update.html', admin=admin)
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        if username == '' or email == '':
            return 'All Fields are required'
        else:
            admin = Admin.query.get(session['username'])
            if admin.username == username and admin.email == email:
                flash('No update made', 'info')
            else:
                admin.username = username
                admin.email = email
                db.session.commit()
                flash('profile updated successfully', 'success')
            return redirect('/admin/admindash/')
        
@app.route('/admin/add_song/', methods=['GET', 'POST'])
def add_songs():
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    form = SongForm()
    if form.validate_on_submit():
        lyrics = form.song_lyrics.data
        if lyrics is not None and len(lyrics) > 2000:
            flash('Song lyrics cannot exceed 2000 characters!')
            return render_template('admin/add_songs.html', form=form, admin=admin)
        else:
            song = Songs(songs_title=form.song_title.data, song_lyrics=lyrics, admin_id=adminid)
            db.session.add(song)
            db.session.commit()
            solfa_notation = form.solfa_notation.data
            if solfa_notation:
                solfa = Song_solfa(song_id=song.songs_id, solfa_notation=solfa_notation)
                db.session.add(solfa)
                db.session.commit()
            flash('Song Upload was successful','success')
            return redirect('/admin/songs/')
    return render_template('admin/add_songs.html', form=form, admin=admin)

@app.route('/my_songs/')
def my_songs():
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    songs = Songs.query.filter_by(admin_id=adminid).all()
    return render_template('Admin/mysongs.html', admin=admin, songs=songs)

@app.route('/song_details/<int:id>')
def song_details(id):
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    song = Songs.query.get(id)
    return render_template('Admin/song_details.html', song=song,admin=admin)     

@app.route('/edit_song/<int:id>', methods=['GET', 'POST'])
@csrf.exempt
def edit_song(id):
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    song = Songs.query.get(id)
    if request.method == 'POST':
        song_title = song.songs_title
        song_lyrics = song.song_lyrics
        existing_solfa = Song_solfa.query.filter_by(song_id=song.songs_id).first()
        solfa_notation = existing_solfa.solfa_notation if existing_solfa else None

        song.songs_title = request.form['songs_title']
        song.song_lyrics = request.form['song_lyrics']
        solfa_notation = request.form['solfa_notation']

        if existing_solfa:
            existing_solfa.solfa_notation = solfa_notation
        else:
            solfa = Song_solfa(song_id=song.songs_id, solfa_notation=solfa_notation)
            db.session.add(solfa)

        db.session.commit()

        if (song_title != song.songs_title or song_lyrics != song.song_lyrics or solfa_notation != solfa_notation):
            flash('Song updated successfully', 'success')
        else:
            flash('No update was made', 'warning')

        return redirect(url_for('admin_songs'))
    return render_template('Admin/edit_song.html', song=song, admin=admin)

@app.route('/delete_song/<int:id>')
def delete_song(id):
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    song = Songs.query.get(id)

    if song is not None:
        try:
            db.session.delete(song)
            db.session.commit()
            flash(f'{song} deleted')
            return redirect(url_for('admin_songs', admin=admin))
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return f"Error deleting song: {e}", 500
    else:
        return "Song not found", 404


@app.route('/admin/approve_request/<int:id>')
def admin_approve_request(id):
    request = SongsRequest.query.get(id)
    song = Songs(title=request.song_title, lyrics=request.song_lyrics, artist_id=request.artist_id, scorer_id=request.scorer_id, solfa_notation=request.solfa_notation)
    db.session.add(song)
    db.session.delete(request)
    db.session.commit()
    return redirect(url_for('admin_songs'))

@app.route('/admin/requests/')
def admin_requests():
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    requests = SongsRequest.query.all()
    return render_template('Admin/song_request.html', requests=requests,admin=admin)