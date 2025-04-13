import secrets,requests
from sqlalchemy import text
from functools import wraps
from flask import render_template,flash,request,redirect,session,url_for
from flask_wtf.csrf import CSRFProtect
from packages import app,config
from packages.user_forms import UserForm,ArtistForm,User_reg,Artist_Reg,AddSongForm,UploadDpForm,Edit_User
from packages.models import db,User,Artists,Songs,Song_solfa,SongsRequest
from packages.models import SearchHistory,Admin,User__Instrument,Instruments
from werkzeug.security import generate_password_hash,check_password_hash

csrf=CSRFProtect(app)


def login_reguired(f):
    @wraps(f)
    def login_decorator(*args, **kwargs):
        allowed_routes = ['index', 'user_login', 'artist_login', 'user_register', 'register']
        if request.endpoint in allowed_routes:
            return f(*args, **kwargs)
        user_id = session.get('username')
        artist_id = session.get('fullname')
        if user_id or artist_id:
            return f(*args, **kwargs)
        else:
            flash('You must be logged in to view this page', category='failed')
            if user_id is None and artist_id is None:
                return redirect('/user/login/')
            elif user_id is None:
                return redirect('/artist/login/')
            else:
                return redirect('/user/login/')
    return login_decorator



@app.errorhandler(404)
def notfound(error):
    return render_template('/User/pagenotfound_error.html'), 404


@app.errorhandler(500)
def error(error):
    return render_template('/User/500_error.html'), 500

@app.errorhandler(503)
def error50(error):
    return render_template('/User/503_error.html'), 503

@app.after_request
def after_request(response):
    response.headers['Cache-Control']='no-cache','no-store','must-revalidate'
    return response



api_key = config.YOUR_GENIUS_API_KEY


@app.route('/index/')
def index():
    username = session.get('username')
    fullname = session.get('fullname')
    user = None
    artist = None
    if username:
        user = User.query.filter_by(users_firstname=username).first()
    elif fullname:
        artist = Artists.query.filter_by(artist_firstname=fullname).first()
    return render_template('User/index.html', artist=artist, user=user)


@app.route('/about/')
def about():
    return render_template('User/about.html')


@app.route('/search/')
@login_reguired
def search():
    search_term = request.args.get('search_term')
    if not search_term:
        flash('Please enter a search term.', 'error')
        return redirect('/songs/')
    if search_term.lower()=='omemma':
        return redirect('/omemma/')
    if search_term.lower()=='worthy':
        return redirect('/worthy/')

    user_id = session.get('username')
    artist_id = session.get('fullname')
    search_history = SearchHistory(user_id=user_id, artist_id=artist_id, search_term=search_term)
    try:
        db.session.add(search_history)
        db.session.commit()
        print("Search history saved:", search_history)
    except Exception as e:
        print("Error saving search history:", e)

    search_term = search_term.lower()
    songs = Songs.query.filter(Songs.songs_title.ilike('%' + search_term + '%')).all()
    if songs:
        return render_template('User/search_results.html', songs=songs)
    else:
        api_key = config.YOUR_GENIUS_API_KEY
        url = f"https://api.genius.com/search?q={search_term}&access_token={api_key}"
        response = requests.get(url)
        data = response.json()

        search_results = []

        for result in data['response']['hits']:
            song_url = result['result']['url']

            search_result = {
                'title': result['result']['title'],
                'artist': result['result']['primary_artist']['name'],
                'url': song_url
            }

            search_results.append(search_result)

        return render_template('User/genius_search_results.html', search_results=search_results)



@app.route('/search_history/')
@login_reguired
def search_history():
    user_id = session.get('username')
    artist_id = session.get('fullname')
    if user_id:
        search_history = SearchHistory.query.filter_by(user_id=user_id).all()
        return render_template('User/search_history.html', search_history=search_history)
    elif artist_id:
        search_history = SearchHistory.query.filter_by(artist_id=artist_id).all()
        return render_template('User/search_history.html', search_history=search_history)
    else:
        flash('User not found.', 'error')
        return redirect('/songs/')





@app.route('/delete_search_history/<int:id>')
@login_reguired
def delete_search_history(id):
    search_history = SearchHistory.query.get(id)
    if search_history:
        db.session.delete(search_history)
        db.session.commit()
        flash('Search history deleted successfully.', 'success')
    else:
        flash('Search history not found.', 'error')
    return redirect(url_for('search_history'))




@app.route('/user/login/', methods=['GET', 'POST'])
def user_login():
    user_login = UserForm()
    if request.method == 'POST':
        if user_login.validate_on_submit():
            email = user_login.email.data
            pwd = user_login.pwd.data
            user = db.session.query(User).filter(User.users_email==email).first()
            if user:
                password = user.users_password
                if check_password_hash(password, pwd):
                    session['username'] = user.users_id 
                    session['pwd'] = password
                    flash(f'Welcome! {user.users_firstname} ,You are now logged in', category='success')
                    return render_template('User/user_dash.html',user=user)
                else:
                    flash('Invalid password', category='failed')
            else:
                flash('Invalid email', category='failed')
    return render_template('User/user_login.html',user=user_login)



@app.route('/artist/login/', methods=['GET', 'POST'])
def artist_login():
    artist = ArtistForm()
    if artist.validate_on_submit():
        fname = artist.fname.data
        lname = artist.lname.data
        artist_db = db.session.query(Artists).filter(Artists.artist_firstname == fname, Artists.artist_lastname == lname).first()
        if artist_db:
            session['fullname'] = artist_db.artist_firstname
            session['fullname'] = artist_db.artist_id
            flash(f'Welcome {artist_db.artist_firstname},You are now logged in ','success')
            return render_template('User/artist_dash.html', artist=artist_db)
        else:
            flash('Artist not found', 'error')
            return render_template('User/artist_login.html', artist=artist)
    return render_template('User/artist_login.html', artist=artist)
 
@app.route('/user/register/', methods=['GET', 'POST'])
def user_register():
    user = User_reg()
    user.instrument.choices = [(i.instru_id, i.name) for i in Instruments.query.all()]
    if request.method == 'POST':
        if user.validate_on_submit():
            fname = user.fname.data
            lname = user.lname.data
            email = user.email.data
            pwd = user.pwd.data
            users = user.users.data
            instrument = user.instrument.data
            hashed_password = generate_password_hash(pwd)
            existing_email = User.query.filter_by(users_email=email).first()
            if existing_email:
                flash('Email address already exists. Please try another one.', 'error')
                return render_template('User/user_reg.html', user=user)
            else:
                new_user = User(
                    users_firstname=fname,
                    users_lastname=lname,
                    users_email=email,
                    users_password=hashed_password,
                    users_role=users
                )
                db.session.add(new_user)
                db.session.commit()
                user_instrument = User__Instrument(
                    user_id=new_user.users_id,
                    instrument_id=instrument
                )
                db.session.add(user_instrument)
                db.session.commit()
                session['username'] = f"{user.fname.data} {user.lname.data}"
                session['email'] = user.email.data
                session['password'] = user.pwd.data
                flash('User registered successfully!', 'success')
                return redirect(url_for('user_login'))
        else:
            flash('Invalid form data. Please try again.', 'error')
    return render_template('User/user_reg.html', user=user)


@app.route('/artist/register/', methods=['GET', 'POST'])
def register():
    artist = Artist_Reg()
    if request.method == 'POST':
        if artist.validate_on_submit():
            print("Artist registered successfully!")
            fname = artist.fname.data
            lname = artist.lname.data
            artists = Artists(artist_firstname=fname, artist_lastname=lname)
            db.session.add(artists)
            db.session.commit()
            print("Artist added to database:", artists.artist_firstname, artists.artist_lastname)
            session['fullname'] = f"{artist.fname.data} {artist.lname.data}"
            session['fullname'] = artists.artist_id  # Set the artist_id session variable
            return redirect('/artist/login/')
        else:
            flash('Please register ', category='error')
    return render_template('User/artist_reg.html', artist=artist)

@app.route('/artist/')
@login_reguired
def artists():
    artists = Artists.query.all()
    artist_count = len(artists)
    return render_template('User/artists.html', artists=artists, artist_count=artist_count)
     




@app.route('/artists/<int:artist_id>/')
@login_reguired
def user_artists(artist_id):
    artists = db.session.query(Artists).get(artist_id)
    artist_count = len(artists)
    for artist in artists:
        if artist.artist_dp:
            artist.artist_dp = url_for('static', filename='uploads/' + artist.artist_dp)
        else:
            artist.artist_dp = url_for('static', filename='uploads/default.jpg')
    return render_template('User/artist_dash.html',artists=artists,artist_count=artist_count)


@app.route('/scorers/<int:user_id>/')
@login_reguired
def user_scorer(user_id):
    scorers = db.session.query(User).get(user_id)
    scorers_count = len(scorers)
    return render_template('User/scorers.html',scorers=scorers,
                           scorers_count=scorers_count)



@app.route('/scorers/')
@login_reguired
def scorers():
    scorers = db.session.query(User).filter(User.users_role == 'Scorers').all()
    user_count = len(scorers)
    return render_template('User/scorers.html', scorers=scorers, user_count=user_count)


@app.route('/userdash/')
@login_reguired
def userdash():
        user_id = session.get('username')
        user = db.session.query(User).filter(User.users_id == user_id).first()
        return render_template('User/user_dash.html', user=user)



@app.route('/artist/dashboard/')
@login_reguired
def artist_dashboard():
    artist_id = session.get('fullname')
    artist = Artists.query.get(artist_id)
    if artist:
        songs = Songs.query.filter_by(artist_id=artist_id).all()
        return render_template('User/artist_dash.html', artist=artist, songs=songs)
    else:
        flash('Artist not found', 'error')
        return redirect(url_for('index'))

       
@app.route('/dashboard/')
@login_reguired
def dashboard():
    if session.get('username'):
        user_id = session['username']
        user = db.session.query(User).filter(User.users_id == user_id).first()
        return render_template('User/user_dash.html', user=user)
    elif session.get('fullname'):
        artist_id = session['fullname']
        artist = db.session.query(Artists).filter(Artists.artist_id == artist_id).first()
        return render_template('User/artist_dash.html', artist=artist)
    return redirect('/user/register')

@app.route('/artist/<int:artist_id>/details/')
@login_reguired
def artist_details(artist_id):
    artist = Artists.query.get(artist_id)
    if artist:
        return render_template('User/artist_details.html', artist=artist)
    else:
        flash('Artist not found', 'error')
        return redirect(url_for('index'))


@app.route('/songs/')
@login_reguired
def songs():
    try:
        songs = Songs.query.order_by(Songs.songs_id.desc()).all()
        solfa=Song_solfa.query.all()
        return render_template('User/songs.html', songs=songs,solfa=solfa)
    except Exception as e:
        return str(e)

@app.route('/user/song_details/<int:id>')
@login_reguired
def songdetails(id):
    song = Songs.query.get(id)
    if song is not None:
        return render_template('User/song_details.html', song=song)
    else:
        return "Song not found", 404

@app.route('/omemma/')
def omemma():
    return render_template('User/omemma.html')

@app.route('/worthy/')
def worthy():
    return render_template('User/worthy.html')


@app.route('/logout/')
@login_reguired
def logout():
    session.pop('username', None)
    session.pop('fullname', None)
    flash('You have been logged out.', category='success')
    return redirect('/index/')

@app.route('/user/<int:user_id>/update/', methods=['GET', 'POST'])
@login_reguired
def user_edit_details(user_id):
    user = Edit_User()
    instruments = Instruments.query.all()
    instrument_choices = [('0', 'Select an instrument')] + [(i.instru_id, i.name) for i in instruments]
    instrument_type_choices = [('0', 'Select an instrument type')] + [(i.instru_id, i.type) for i in instruments]
    user.instrument.choices = instrument_choices
    user.instrument_type.choices = instrument_type_choices
    user_info = User.query.filter_by(users_id=user_id).first()
    user_instrument = User__Instrument.query.filter_by(user_id=user_id).first()
    if request.method == 'GET':
        user.fname.data = user_info.users_firstname
        user.lname.data = user_info.users_lastname
        user.email.data = user_info.users_email
        user.phone.data = user_info.users_phonenumber
        if user_instrument:
            user.instrument.data = user_instrument.instrument_id
    if request.method == 'POST':
        user.instrument.choices = instrument_choices
        user.instrument_type.choices = instrument_type_choices
        if user.validate_on_submit():
            fname = user.fname.data
            lname = user.lname.data
            email = user.email.data
            phonenumber = user.phone.data
            instrument = user.instrument.data
            instrument_type = user.instrument_type.data
            existing_email = User.query.filter_by(users_email=email).first()
            existing_phone = User.query.filter_by(users_phonenumber=phonenumber).first()
            if existing_email and existing_email.users_id != user_id:
                flash('Email address already exists. Please try another one.', 'error')
                return render_template('User/user_edit_details.html', user=user)
            elif existing_phone and existing_phone.users_phonenumber == phonenumber and existing_phone.users_id != user_id:
                flash('Phone number already exists. Please try another one.', 'error')
                return render_template('User/user_edit_details.html', user=user)
            else:
                user_to_update = db.session.query(User).filter(User.users_id == user_id).first()
                user_to_update.users_firstname = fname
                user_to_update.users_lastname = lname
                user_to_update.users_email = email
                user_to_update.users_phonenumber = phonenumber
                db.session.commit()
                if instrument != 0:
                    user_instrument = User__Instrument.query.filter_by(user_id=user_id).first()
                    if user_instrument:
                        user_instrument.instrument_id = instrument
                    else:
                        user_instrument = User__Instrument(user_id=user_id, instrument_id=instrument)
                        db.session.add(user_instrument)
                    db.session.commit()
                flash('User details updated successfully!', 'success')
                return redirect('/userdash/')
    return render_template('User/user_edit_details.html', user=user)

@app.route('/artist/<int:artist_id>/update/', methods=['GET', 'POST'])
@login_reguired
def artist_edit_details(artist_id):
    artist = Artist_Reg()
    artist_db = db.session.query(Artists).filter(Artists.artist_id == artist_id).first()
    if request.method == 'GET':
        artist.fname.data = artist_db.artist_firstname
        artist.lname.data = artist_db.artist_lastname
    if artist.validate_on_submit():
        fname = artist.fname.data
        lname = artist.lname.data
        artist_db.artist_firstname = fname
        artist_db.artist_lastname = lname
        db.session.commit()
        session['fullname'] = artist_id
        flash('Artist details updated successfully')
        return redirect(url_for('artist_dashboard'))
    return render_template('User/artist_edit_details.html', artist=artist)

@app.route('/scorers/<int:users_id>/details/')
@login_reguired
def scorers_details(users_id):
    scorer = User.query.get_or_404(users_id)
    user = User.query.get_or_404(users_id)
    return render_template('User/details.html', scorer=scorer,user=user)




@app.route('/upload_dp/', methods=['GET', 'POST'])
@login_reguired
def upload_dp():
    dp = UploadDpForm()
    user_id = session.get('username')
    artist_id = session.get('fullname')
    
    if user_id:
        user = User.query.filter_by(users_id=user_id).first()
        if dp.validate_on_submit():
            file = dp.picture.data
            ext = file.filename.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png', 'gif']:
                flash('Invalid file type.', 'error')
                return render_template('User/upload_db.html', user=user, dp=dp), 400
            filename = secrets.token_urlsafe() + '.' + ext
            try:
                file.save('packages/static/uploads/' + filename)
            except Exception as e:
                flash(f"Error uploading file: {str(e)}", 'error')
                return render_template('User/upload_db.html', user=user, dp=dp), 500
            user.users_profilepicture = filename
            db.session.commit()
            return redirect('/dashboard/')
        return render_template('User/upload_db.html', user=user, dp=dp)
    
    elif artist_id:
        artist = Artists.query.filter_by(artist_id=artist_id).first()
        if dp.validate_on_submit():
            file = dp.picture.data
            ext = file.filename.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png', 'gif']:
                flash('Invalid file type.', 'error')
                return render_template('User/upload_db.html', artist=artist, dp=dp), 400
            filename = secrets.token_urlsafe() + '.' + ext
            try:
                file.save('packages/static/uploads/' + filename)
            except Exception as e:
                flash(f"Error uploading file: {str(e)}", 'error')
                return render_template('User/upload_db.html', artist=artist, dp=dp), 500
            artist.artist_dp = filename
            db.session.commit()
            return redirect('/dashboard/')
        return render_template('User/upload_db.html', artist=artist, dp=dp)
    
    else:
        flash('User or Artist not found', 'error')
        return redirect('/index/')

@app.route('/add_song/', methods=['GET', 'POST'])
@login_reguired
def add_song():
    form = AddSongForm()
    artists = Artists.query.all()
    scorers = User.query.filter(User.users_role=='Scorers').all()  # Assuming you have a Scorers model
    form.artist_id.choices = [(artist.artist_id, artist.artist_firstname + ' ' + artist.artist_lastname) for artist in artists]
    if request.method == 'POST':
        print("Form submitted")
        if form.validate_on_submit():
            print("Form validated")
            try:
                new_song_request = SongsRequest(
                    song_title=form.song_title.data,
                    song_lyrics=form.song_lyrics.data,
                    solfa_notation=form.solfa_notation.data,
                    artist_id=form.artist_id.data
                )
                print("New song request created")
                db.session.add(new_song_request)
                print("Song request added to session")
                db.session.commit()
                print("Changes committed")
                flash('Your song upload is been approved. Please wait for approval....', 'success')
                return redirect('/index/')
            except Exception as e:
                print(f"Error: {e}")
                flash('Error adding song please try again', 'error')
        else:
            print("Form not validated")
            print(form.errors)
    return render_template('User/add_songs.html', form=form, artists=artists, scorers=scorers)



@app.route('/edit/<int:songs_id>', methods=['GET', 'POST'])
@login_reguired
@csrf.exempt
def edit(songs_id):
    form = AddSongForm()
    song = Songs.query.get(songs_id)
    artists = Artists.query.all()
    scorers = db.session.query(User).filter(User.users_role == 'Scorers').all()
    solfa = db.session.query(Song_solfa).filter(Song_solfa.song_id == songs_id).first()

    form.artist_id.choices = [(artist.artist_id, artist.artist_firstname) for artist in artists]
    form.scorer_id.choices = [(scorer.users_id, scorer.users_email) for scorer in scorers]

    if request.method == 'POST':
        if form.validate_on_submit():
            existing_request = db.session.query(SongsRequest).filter(
                SongsRequest.id == song.songs_id,
                SongsRequest.song_title == song.songs_title,
                SongsRequest.song_lyrics == song.song_lyrics,
                SongsRequest.artist_id == form.artist_id.data,
                SongsRequest.user_id == form.scorer_id.data,
                SongsRequest.solfa_notation == solfa.solfa_notation,
                SongsRequest.status == 'pending'
            ).first()

            if existing_request is None:
                new_request = SongsRequest(
                    id=song.songs_id,
                    song_title=song.songs_title,
                    song_lyrics=song.song_lyrics,
                    artist_id=form.artist_id.data,
                    user_id=form.scorer_id.data,
                    solfa_notation=solfa.solfa_notation,
                    status='pending'
                )
                db.session.add(new_request)
                db.session.commit()
                flash('Your song edit request is been processed', 'success')
                return redirect(url_for('songs'))
            else:
                flash('A request for this song already exists', 'error')
        else:
            print(form.errors)
            flash('SONG EDIT FAILED', 'error')
    return render_template('User/songs.html', artist=artists, form=form, scorers=scorers, song=song, solfa=solfa)