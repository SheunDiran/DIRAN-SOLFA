import secrets,os
from sqlalchemy import text
from functools import wraps
from flask import render_template,flash,request,redirect,session,url_for
from packages import app
from packages.user_forms import UserForm,ArtistForm,User_reg,Artist_Reg,AddSongForm,UploadDpForm,Edit_User
from packages.models import db,User,Artists,Songs,Song_solfa,SongsRequest,SearchHistory,Admin,User__Instrument,Instruments
from werkzeug.security import generate_password_hash,check_password_hash




def login_reguired(f):
    @wraps(f)
    def login_decorator(*args, **kwargs):
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

@app.route('/index/')
def index():
    email = session.get('email')
    return render_template('User/index.html',email=email)

@app.route('/about/')
def about():
    return render_template('User/about.html')

@app.route('/search/')
def search():
    search_term = request.args.get('search_term')
    instrument = Instruments.query.all()
    songs = Songs.query.join(Admin).filter(
        (Songs.songs_title.like('%' + search_term + '%')) |
        (Admin.username.like('%' + search_term + '%'))
    ).all()
    instrument_songs = Songs.query.join(Song_solfa).join(Instruments).filter(
        (Instruments.name.like('%' + search_term + '%')) |
        (Instruments.type.like('%' + search_term + '%'))
    ).all()
    if search_term.lower()=='omemma':
        return redirect('/omemma/')
    elif 'worthy' in search_term:
        return redirect('/worthy/')
    if songs or instrument_songs:
        user_id = session.get('username')
        artist_id = session.get('fullname')
        search_history = SearchHistory(user_id=user_id,artist_id=artist_id ,search_term=search_term)
        db.session.add(search_history)
        db.session.commit()
        return render_template('User/search_results.html', songs=songs + instrument_songs, instrument=instrument)
    else:
        flash(f'No songs found for "{search_term}". Please try searching for another song.', 'error')
        return redirect('/songs/')

@app.route('/search_history/')
def search_history():
    user_id = session.get('username')
    artist_id=session.get('fullname')
    search_history = SearchHistory.query.filter_by(user_id=user_id,artist_id=artist_id).all()
    return render_template('User/search_history.html', search_history=search_history)

@app.route('/delete_search_history/<int:id>')
def delete_search_history(id):
    user_id = session.get('username')
    artist_id=session.get('fullname')
    search_history = SearchHistory.query.get(id)
    if search_history.user_id == user_id or search_history.artist_id == artist_id :
        db.session.delete(search_history)
        db.session.commit()

    return redirect('/search_history/')

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
                    return redirect('/userdash/')
                else:
                    flash('Invalid password', category='failed')
            else:
                flash('Invalid email', category='failed')
    return redirect('/songs/')



@app.route('/artist/login/', methods=['GET', 'POST'])
def artist_login():
    artist = ArtistForm()
    if artist.validate_on_submit():
        fname = artist.fname.data
        lname = artist.lname.data
        artist_db = db.session.query(Artists).filter(Artists.artist_firstname == fname, Artists.artist_lastname == lname).first()
        if artist_db:
            session['fullname'] = artist_db.artist_firstname
            session['artist_id'] = artist_db.artist_id
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
            session['artist_id'] = artists.artist_id  # Set the artist_id session variable
            return redirect('/artist/login/')
        else:
            flash('Please register ', category='error')
    return render_template('User/artist_reg.html', artist=artist)


@app.route('/artists/')
def artists():
    artists = db.session.query(Artists).all()
    artist_count = len(artists)
    return render_template('User/artists.html', artists=artists, artist_count=artist_count)


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



@app.route('/artistdash/')
@login_reguired
def artistdash():
        artist_id = session['fullname']
        artist = db.session.query(Artists).filter(Artists.artist_id == artist_id).first()
        return render_template('User/artist_dash.html', artist=artist)
       
@app.route('/dashboard/')
@login_reguired
def dashboard():
    if session.get('username'):
        user_id = session['username']
        user = db.session.query(User).filter(User.users_id == user_id).first()
        return render_template('User/user_dash.html', user=user)
    elif session.get('fullname'):
         artist_id = session['fullname']
         artist = db.session.query(Artists).filter(Artists.artist_firstname == artist_id).first()
         return render_template('User/artist_dash.html',artist=artist)
    return redirect('/user/register')


@app.route('/songs/')
@login_reguired
def songs():
    try:
        songs = Songs.query.order_by(Songs.songs_id.desc()).all()
        return render_template('User/songs.html', songs=songs)
    except Exception as e:
        return str(e)


@app.route('/user/song_details/<int:id>')
@login_reguired
def songdetails(id):
    song = Songs.query.get(id)
    return render_template('User/song_details.html', song=song) 

@app.route('/omemma/')
def omemma():
    return render_template('User/omemma.html')
1
@app.route('/worthy/')
def worthy():
    return render_template('User/worthy.html')


@app.route('/logout/')
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
    
    # Get the user's current information
    user_info = User.query.filter_by(users_id=user_id).first()
    user_instrument = User__Instrument.query.filter_by(user_id=user_id).first()
    
    if request.method == 'GET':
        # Populate the form with the user's current information
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
            elif existing_phone== phonenumber:
                flash('Phone number already exists. Please try another one.', 'error')
                return render_template('User/user_edit_details.html', user=user)
            else:
                user_to_update = db.session.query(User).filter(User.users_id == user_id).first()
                user_to_update.users_firstname = fname
                user_to_update.users_lastname = lname
                user_to_update.users_email = email
                user_to_update.users_phonenumber = phonenumber
                
                db.session.commit()
                
                if instrument != '0':
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
    if artist.validate_on_submit():
        fname = artist.fname.data
        lname = artist.lname.data
        artist_db = db.session.query(Artists).filter(Artists.artist_id == artist_id).first()
        artist_db.artist_firstname = fname
        artist_db.artist_lastname = lname
        db.session.commit()
        flash('Artist details updated successfully')
        return redirect(url_for('artistdash'))
    if artist.errors:
        flash('Sorry that name is taken, TRY AGAIN')
    return render_template('User/artist_edit_details.html', artist=artist)


@app.route('/scorers/<int:users_id>/details/')
@login_reguired
def scorers_details(users_id):
    scorer = User.query.get_or_404(users_id)
    return render_template('User/details.html', scorer=scorer)

@app.route('/artist/<int:artist_id>/details/')
@login_reguired
def artist_details(artist_id):
    artist = Artists.query.get_or_404(artist_id)
    return render_template('User/artist_details.html', artist=artist)

@app.route('/upload_dp/', methods=['GET', 'POST'])
@login_reguired
def upload_dp():
    dp = UploadDpForm()
    user = User.query.filter_by(users_id=session.get('username')).first()
    artist = Artists.query.filter_by(artist_firstname=session.get('fullname')).first()

    if not user and not artist: return redirect('/login')

    if dp.validate_on_submit():
        file = dp.picture.data
        ext = file.filename.split('.')[-1].lower()

        if ext not in ['jpg', 'jpeg', 'png', 'gif']:
            flash('Invalid file type.', 'error')
            return render_template('User/upload_db.html', user=user, artist=artist, dp=dp), 400

        filename = secrets.token_urlsafe() + '.' + ext
        try: file.save('packages/static/uploads/' + filename)
        except Exception as e: 
            flash(f"Error uploading file: {str(e)}", 'error')
            return render_template('User/upload_db.html', user=user, artist=artist, dp=dp), 500

        if user: user.users_profilepicture = filename
        elif artist: artist.artist_dp = filename
        db.session.commit()
        return redirect('/dashboard/')

    return render_template('User/upload_db.html', user=user, artist=artist, dp=dp)


@app.route('/add_song/', methods=['GET', 'POST'])
@login_reguired
def add_song():
    form = AddSongForm()
    artists = Artists.query.all()
    scorers = db.session.query(User).filter(User.users_role == 'Scorers').all()
    form.artist_id.choices = [(artist.artist_id, f"{artist.artist_firstname} {artist.artist_lastname}") for artist in artists]
    form.scorer_id.choices = [(scorer.users_id, scorer.users_email) for scorer in scorers]
    if request.method == 'POST':
        print(request.form)
        if form.validate_on_submit():
            print("Form is valid")
            try:
                if request.form.get('selection') == 'artist':
                    print("Artist selected")
                    song_request = SongsRequest(
                        song_title=form.song_title.data,
                        song_lyrics=form.song_lyrics.data,
                        artist_id=form.artist_id.data,
                        scorer_id=None,
                        solfa_notation=form.solfa_notation.data,
                        user_id=None,
                        status='pending'
                    )
                else:
                    print("Scorer selected")
                    song_request = SongsRequest(
                        song_title=form.song_title.data,
                        song_lyrics=form.song_lyrics.data,
                        artist_id=None,
                        scorer_id=form.scorer_id.data,
                        solfa_notation=form.solfa_notation.data,
                        user_id=None,
                        status='pending'
                    )
                print("Song request created")
                db.session.add(song_request)
                print("Song request added to database session")
                db.session.commit()
                print("Database session committed")
                flash('Your song upload is been approved.Please wait for approval....','success')
                return redirect('/index/')
            except Exception as e:
                print(f"Error: {e}")
                db.session.rollback()
                flash('Error adding song')
        else:
            print("Form is not valid")
            print(form.errors)
    return render_template('User/add_songs.html', form=form, artists=artists, scorers=scorers)
