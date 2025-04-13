import secrets
from functools import wraps
from sqlalchemy.exc import IntegrityError
from flask_wtf.csrf import CSRFProtect
from flask import render_template,flash,request,redirect,session,url_for
from packages import app
from flask_bcrypt import Bcrypt
from packages.admin_forms import AdminLogin,DpForm,SongForm
from packages.models import Admin,db,User,Artists,Songs,Song_solfa,SongsRequest,Instruments
csrf = CSRFProtect()
csrf.init_app(app)
bcrypt = Bcrypt(app)


@app.after_request
def after_request(response):
    response.headers['Cache-Control']='no-cache','no-store','must-revalidate'
    return response

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None:
            flash('You must be logged in to view this page', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/index/')
def admin_index():
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    return render_template('Admin/index.html',admin=admin)


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
@admin_required
def admin_logout():
    session.clear() 
    flash('You have been logged out.', category='success')
    return redirect('/admin/login/')


@app.route('/admin/admindash/')
@admin_required
def admin_dashboard():
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    songs = Songs.query.all()
    users_count = User.query.filter(User.users_role=='Users').count()
    artists_count = Artists.query.count()
    songs_count = Songs.query.count()
    instruments = Instruments.query.count()
    requests = SongsRequest.query.count()
    scorers_count = User.query.filter(User.users_role=='Scorers').count()
    return render_template('Admin/admin_dash.html', users_count=users_count, 
    artists_count=artists_count, songs_count=songs_count,admin=admin,songs=songs,
      scorers_count=scorers_count,instruments=instruments,requests=requests)     

@app.route('/admin/user/<int:user_id>/')
@admin_required
def admin_user(user_id):
    user = db.session.query(User).get(user_id)
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    if user.users_profilepicture:
        picture_url = url_for('static', filename='uploads/' + user.users_profilepicture)
    else:
        flash('No profile picture found', 'error')
    return render_template('Admin/users.html', user=user, admin=admin, picture_url=picture_url)


@app.route('/admin/users/')
@admin_required
def admin_view_users():
    users = db.session.query(User).filter(User.users_role=='Users').all()
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    users_count= len(users)
    return render_template('Admin/users.html', users=users, admin=admin,users_count=users_count)

@app.route('/admin/artists/')
@admin_required
def admin_view_artists():
    artists = db.session.query(Artists).all()
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    artist_count= len(artists)
    return render_template('Admin/artists.html',artists=artists, admin=admin,artist_count=artist_count)

@app.route('/admin/artists/<int:artist_id>/')
@admin_required
def admin_artists(artist_id):
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    artists = db.session.query(Artists).get(artist_id)
    artist_count = len(artists)
    for artist in artists:
        if artist.artist_dp:
            artist.artist_dp = url_for('static', filename='uploads/' + artist.artist_dp)
        else:
            artist.artist_dp = url_for('static', filename='uploads/default.jpg')
    return render_template('Admin/artists.html',artists=artists,artist_count=artist_count,admin=admin)

@app.route('/admin/scorers/<int:user_id>')
@admin_required
def admin_scorer(user_id):
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    scorers = db.session.query(User).get(user_id)
    scorers_count = len(scorers)
    return render_template('Admin/scorers.html',scorers=scorers,scorers_count=scorers_count,admin=admin)


@app.route('/admin/scorers/')
@admin_required
def admin_view_scorers():
    scorers= db.session.query(User).filter(User.users_role=='Scorers').all()
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    scorers_count= len(scorers)
    return render_template('Admin/scorers.html',scorers=scorers, admin=admin,
                           scorers_count=scorers_count)

@app.route('/users/<int:users_id>/details/')
@admin_required
def users_details(users_id):
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    user = User.query.get_or_404(users_id)
    return render_template('Admin/user_details.html', user=user,admin=admin)

@app.route('/admin/artist/<int:artist_id>/details/')
@admin_required
def admin_artist_details(artist_id):
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    artist = Artists.query.get_or_404(artist_id)
    return render_template('Admin/artist_details.html', artist=artist,admin=admin)

@app.route('/users/<int:users_id>/delete/')
@admin_required
def users_delete(users_id):
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    users=db.session.query(User).get(users_id)
    db.session.delete(users)
    db.session.commit()
    return redirect('/admin/user/',admin=admin)

@app.route('/admin/artist/<int:artist_id>/delete/')
@admin_required
def admin_artist_delete(artist_id):
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    artists=db.session.query(Artists).get(artist_id)
    db.session.delete(artists)
    db.session.commit()
    return redirect('/admin/artists/',admin=admin)

@app.route('/admin/upload/dp/', methods=['GET', 'POST'])
@admin_required
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
@admin_required
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
@admin_required
def add_songs():
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    form = SongForm()
    if form.validate_on_submit():
        lyrics = form.song_lyrics.data
        title = form.song_title.data
        solfa_notation = form.solfa_notation.data
        if not title or not lyrics or not solfa_notation:
            flash('Please fill out all fields', 'danger')
            return render_template('admin/songs.html', form=form, admin=admin)
        if lyrics is not None and len(lyrics) > 2000:
            flash('Song lyrics cannot exceed 2000 characters!', 'danger')
            return render_template('admin/songs.html', form=form, admin=admin)
        else:
            song = Songs(songs_title=title, song_lyrics=lyrics, admin_id=adminid)
            db.session.add(song)
            db.session.commit()
            solfa = Song_solfa(song_id=song.songs_id, solfa_notation=solfa_notation)
            db.session.add(solfa)
            db.session.commit()
            flash('Song Upload was successful', 'success')
            return redirect('/admin/songs/')
    return render_template('Admin/songs.html', form=form, admin=admin)

@app.route('/admin/view_song/<int:id>/')
@admin_required
def view_song(id):
    admin_id = session.get('admin_id')
    admin = db.session.query(Admin).get(admin_id)
    song = Songs.query.get(id)
    solfa = Song_solfa.query.filter_by(song_id=id).first()
    if song is not None:
        return render_template('Admin/song_details.html', song=song, solfa=solfa, admin=admin)
    else:
        return "Song not found", 404




@app.route('/song_details/<int:id>/')
@admin_required
def song_details(id):
    admin_id = session.get('admin_id')
    admin = db.session.query(Admin).get(admin_id)
    song = Songs.query.get(id)
    if song is not None:
        return render_template('Admin/song_details.html', song=song, admin=admin)
    else:
        return "Song not found", 404    
@app.route('/edit_song/<id>', methods=['GET', 'POST'])
@admin_required
def edit_song(id):
    song = Songs.query.get(id)
    if song is None:
        flash('Song not found', 'error')
        return redirect(url_for('admin_songs'))

    if request.method == 'POST':
        # Update song details here
        song.songs_title = request.form.get('title')
        song.song_lyrics = request.form.get('lyrics')
        # Update solfa notation if it exists
        sof = Song_solfa.query.filter_by(song_id=id).first()
        if sof:
            sof.solfa_notation = request.form.get('notation')
            db.session.add(sof)
        db.session.add(song)
        db.session.commit()
        flash('Song updated successfully', 'success')
        return redirect(url_for('admin_songs'))

    return render_template('edit_song.html', song=song)



@app.route('/delete_song/<int:id>/', methods=['POST'])
@admin_required
def delete_song(id):
    song = Songs.query.get(id)
    if song is None:
        flash('Song not found', 'error')
        return redirect(url_for('admin_songs'))

    try:
        sof = Song_solfa.query.filter_by(song_id=id).first()
        if sof is not None:
            db.session.delete(sof)
        db.session.delete(song)
        db.session.commit()
        flash(f'{song.songs_title} deleted')
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting song: {e}", 'error')

    return redirect(url_for('admin_songs'))



@app.route('/admin/approve_request/<int:id>/', methods=['POST'])
@admin_required
@csrf.exempt
def admin_approve_request(id):
    request = SongsRequest.query.get(id)
    if request is None:
        flash('Request not found', 'error')
        return redirect(url_for('index'))

    song = Songs(
    songs_title=request.song_title,
    song_lyrics=request.song_lyrics,
    artist_id=request.artist_id
)
    db.session.add(song)
    db.session.commit()

    solfa = Song_solfa(
        song_id=song.songs_id,
        solfa_notation=request.solfa_notation
    )
    db.session.add(solfa)
    db.session.commit()

    db.session.delete(request)
    db.session.commit()
    flash('Request approved', 'success')
    return redirect(url_for('admin_requests'))

 

@app.route('/admin/requests/')
@admin_required
def admin_requests():
    requests = SongsRequest.query.all()
    adminid = session.get('username')
    admin = Admin.query.get(adminid)
    return render_template('Admin/song_request.html', requests=requests,admin=admin)


@app.route('/admin/delete_request/<int:id>/', methods=['POST'])
@admin_required
def admin_delete_request(id):
    request_to_delete = SongsRequest.query.get(id)
    db.session.delete(request_to_delete)
    db.session.commit()
    flash(f'Sorry your Request ({request_to_delete}) was not approved!', 'success')
    return redirect(url_for('admin_requests'))

@app.route('/admin/edit_request/<int:id>/', methods=['GET', 'POST'])
@admin_required
@csrf.exempt
def admin_edit_request(id):
    song_request = SongsRequest.query.get(id)
    if song_request is None:
        return "Request not found", 404
    if request.method == 'POST':
        song_request.song_title = request.form['title']
        song_request.song_lyrics = request.form['lyrics']
        song_request.solfa_notation = request.form['notation']
        db.session.commit()
        flash('Song request updated successfully', 'success')
        return redirect(url_for('admin_requests'))
    return render_template('Admin/edit_request.html', request=song_request)

@app.route('/admin/view_request/<int:id>/',methods=['GET','POST'])
@admin_required
def admin_view_request(id):
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    request = SongsRequest.query.get(id)
    if request is None:
        return "Request not found", 404
    return render_template('Admin/view_request.html', request=request, admin=admin)

@app.route('/instruments/')
@admin_required
def instruments():
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    instruments = Instruments.query.order_by(Instruments.instru_id.desc()).all()
    instrument_names = Instruments.query.with_entities(Instruments.name).distinct().all()
    instrument_types = Instruments.query.with_entities(Instruments.type).distinct().all()
    return render_template('Admin/instruments.html', admin=admin, instruments=instruments, instrument_names=instrument_names, instrument_types=instrument_types)

@app.route('/add_instrument/', methods=['POST'])
@admin_required
def add_instrument():
    print("Form submitted")
    custom_instrument_name = request.form['customInstrumentName']
    instrument_name_id = request.form.get('instrumentName')
    custom_instrument_type = request.form['customInstrumentType']
    instrument_type_id = request.form.get('instrumentType')

    if not instrument_name_id and not custom_instrument_name:
        flash('Please select an instrument name or enter a custom name', 'error')
        return redirect(url_for('instruments'))

    if not instrument_type_id and not custom_instrument_type:
        flash('Please select an instrument type or enter a custom type', 'error')
        return redirect(url_for('instruments'))

    instrument_name = custom_instrument_name if custom_instrument_name else instrument_name_id
    instrument_type = custom_instrument_type if custom_instrument_type else instrument_type_id

    if not instrument_name or not instrument_type:
        flash('Error adding instrument to database', 'error')
        return redirect(url_for('instruments'))

    try:
        new_instrument = Instruments(name=instrument_name, type=instrument_type)
        db.session.add(new_instrument)
        db.session.commit()
        flash('Instrument Added', 'success')
    except Exception as e:
        print("Error adding instrument to database:", e)
        flash('Error adding instrument to database', 'error')

    return redirect(url_for('instruments'))



@app.route('/admin/songs/', methods=['GET', 'POST'])
@admin_required
@csrf.exempt
def admin_songs():
    form = SongForm()
    adminid = session.get('username')
    admin = db.session.query(Admin).get(adminid)
    try:
        songs = Songs.query.order_by(Songs.songs_id.desc()).all()
        solfa = Song_solfa.query.all()
        instrument = Instruments.query.all()
        instrument_names = Instruments.query.with_entities(Instruments.name).distinct().all()
        instrument_types = Instruments.query.with_entities(Instruments.type).distinct().all()
        if form.validate_on_submit():
            lyrics = form.song_lyrics.data
            if lyrics is not None and len(lyrics) > 2000:
                flash('Song lyrics cannot exceed 2000 characters!')
                return render_template('Admin/songs.html', songs=songs, admin=admin, form=form, solfa=solfa, instrument=instrument, instrument_names=instrument_names, instrument_types=instrument_types)
            else:
                song = Songs(songs_title=form.song_title.data, song_lyrics=lyrics, admin_id=adminid)
                db.session.add(song)
                db.session.commit()
                solfa_notation = form.solfa_notation.data
                if solfa_notation:
                    solfa = Song_solfa(song_id=song.songs_id, solfa_notation=solfa_notation)
                    db.session.add(solfa)
                    db.session.commit()
                instrument_name = request.form.get('instrumentName')
                instrument_type = request.form.get('instrumentType')
                # You may want to add some error checking here to make sure the instrument name and type are valid
                instrument = Instruments(name=instrument_name, type=instrument_type)
                db.session.add(instrument)
                db.session.commit()
                flash('Song Upload was successful', 'success')
                return redirect('/admin/songs/')
        else:
            if request.method=='POST':
                flash('Song addition was unsuccessful.Please try readding ', 'danger') 
        return render_template('Admin/songs.html', songs=songs, admin=admin, form=form, solfa=solfa, instrument=instrument, instrument_names=instrument_names, instrument_types=instrument_types)
    except Exception as e:
        return str(e)
    
@app.route('/edit_instrument/<id>/', methods=['POST'])
@admin_required
def edit_instrument(id):
    instrument = Instruments.query.get(id)
    new_name = request.form['name']
    new_type = request.form['type']

    if new_name == instrument.name and new_type == instrument.type:
        flash('No changes made', 'info')
    else:
        instrument.name = new_name
        instrument.type = new_type
        try:
            db.session.commit()
            flash('Edit successful', 'primary')
        except Exception as e:
            print("Error updating instrument in database:", e)
            flash('Error updating instrument in database', 'error')

    return redirect(url_for('instruments'))

@app.route('/delete_instrument/<id>/', methods=['POST'])
@admin_required
def delete_instrument(id):
    instrument = Instruments.query.get(id)
    try:
        db.session.delete(instrument)
        db.session.commit()
        flash('Instrument Deleted', 'success')
    except Exception as e:
        print("Error deleting instrument from database:", e)
        flash('Error deleting instrument from database', 'error')
    return redirect(url_for('instruments'))


