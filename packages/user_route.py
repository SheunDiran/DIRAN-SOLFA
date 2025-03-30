from flask import render_template,flash,request,redirect,session,url_for
from packages import app
from packages.user_forms import UserForm,ArtistForm,User_reg,Artist_Reg
from packages.models import db,User,Artists,User_Instrument,Instruments
from werkzeug.security import generate_password_hash,check_password_hash



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
    return render_template('User/search.html')



@app.route('/user/login/', methods=['GET', 'POST'])
def user_login():
    user_login = UserForm()
    if request.method == 'POST':
        if user_login.validate_on_submit():
            email = user_login.email.data
            pwd = user_login.pwd.data
            user = db.session.query(User).filter(User.users_email == email).first()
            if user:
                password = user.users_password
                if check_password_hash(password, pwd):
                    session['username'] = user.users_id 
                    session['pwd'] = password
                    print("Session:", session)
                    return redirect('/userdash/')
                else:
                    print("Password incorrect")
                    flash('Invalid password', category='failed')
            else:
                print("User not found")
                flash('Invalid email', category='failed')
       
    return render_template('User/user_login.html', user=user_login)


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
            return  render_template('User/user_login.html')
    return render_template('User/artist_login.html', artist=artist)
 
           

@app.route('/user/register/', methods=['GET', 'POST'])
def user_register():
    user=User_reg()
    if request.method=='POST':
        if user.validate_on_submit():
                flash('You are now logged in ', category='success')
                fname=user.fname.data
                lname=user.lname.data
                email=user.email.data
                phone=user.phone.data
                pwd=user.pwd.data
                users=user.users.data
                hashed_password=generate_password_hash(pwd)
                users=User(users_firstname=fname,users_lastname=lname,users_email=email,
                          users_phonenumber=phone,users_password=hashed_password,users_role=users)
                db.session.add(users)
                db.session.commit() 
                session['username'] = f"{user.fname.data} {user.lname.data}"
                session['email'] = user.email.data
                session['password'] = user.pwd.data
                session['phone'] = user.phone.data 
                return  redirect(url_for('user_login'))
        else:
         flash('Please register ', category='error')
         return render_template('User/user_reg.html',user=user)
        
    return render_template('User/user_reg.html',user=user)




@app.route('/artist/register/',methods=['GET','POST'])
def register():
    artist=Artist_Reg()
    if request.method=='POST':
        if artist.validate_on_submit():
                flash('You are now logged in ', category='success')
                fname=artist.fname.data
                lname=artist.lname.data
                artists=Artists(artist_firstname=fname,artist_lastname=lname)
                db.session.add(artists)
                db.session.commit() 
                session['fullname'] = f"{artist.fname.data} {artist.lname.data}" 
                return redirect('/artist/login/')    
        else:
         flash('Please register ', category='error')
         return render_template('User/artist_reg.html',artist=artist)
        
    return render_template('User/artist_reg.html',artist=artist)


@app.route('/artists/')
def artists():
    artist = db.session.query(Artists).all()
    artist_count = len(artist)
    return render_template('User/artists.html',artist=artist,artist_count=artist_count)


@app.route('/scorers/')
def scorers():
    scorers = db.session.query(User).filter(User.users_role == 'Scorers').all()
    user_count = len(scorers)
    return render_template('User/scorers.html', scorers=scorers, user_count=user_count)


@app.route('/userdash/')
def userdash():
    if session.get('username')==None:
        return redirect('/user/login/')
    else:
        user_id = session['username']
        user = db.session.query(User).filter(User.users_id == user_id).first()
        return render_template('User/user_dash.html', user=user)


@app.route('/artistdash/')
def artistdash():
    if session.get('artist_id')==None:
        return redirect('/artist/login/')
    else:
        artist_id = session['artist_id']
        artist = db.session.query(Artists).filter(Artists.artist_id == artist_id).first()
        return render_template('User/artist_dash.html', artist=artist)
       
@app.route('/dashboard/')
def dashboard():
    if session.get('username'):
        user_id = session['username']
        user = db.session.query(User).filter(User.users_id == user_id).first()
        return render_template('User/user_dash.html', user=user)
    elif session.get('fullname'):
         user_id = session['fullname']
         artist = db.session.query(Artists).filter(Artists.artist_firstname == user_id).first()
         return render_template('User/artist_dash.html',artist=artist)
    return redirect('/user/register')

@app.route('/songs/')
def songs():
      return render_template('User/songs.html')

@app.route('/omemma/')
def omemma():
    return render_template('User/omemma.html')

@app.route('/worthy/')
def worthy():
    return render_template('User/worthy.html')


@app.route('/logout/')
def logout():
    session.pop('username', None)
    session.pop('fullname', None)
    flash('You have been logged out.', category='success')
    return redirect('/index')


@app.route('/user/<int:user_id>/update/', methods=['GET', 'POST'])
def user_edit_details(user_id):
    user = User_reg()
    if user.validate_on_submit():
        fname = user.fname.data
        lname = user.lname.data
        email = user.email.data
        password = user.pwd.data
        phonenumber = user.phone.data
        roles = user.users.data
        hashed_password=generate_password_hash(password)
        user = db.session.query(User).filter(User.users_id == user_id).first()
        user.users_firstname = fname
        user.users_lastname = lname
        user.users_email = email
        user.users_password = hashed_password
        user.users_phonenumber = phonenumber
        user.users_role = roles
        db.session.commit()
        return redirect('/userdash/')
    return render_template('User/user_edit_details.html',user=user)
    

@app.route('/artist/<int:artist_id>/update/', methods=['GET', 'POST'])
def artist_edit_details(artist_id):
    artist = Artist_Reg()
    if artist.validate_on_submit():
        try:
            fname = artist.fname.data
            lname = artist.lname.data
            artist_db = db.session.query(Artists).filter(Artists.artist_id == artist_id).first()
            artist_db.artist_firstname = fname
            artist_db.artist_lastname = lname
            db.session.commit()
            flash('Artist details updated successfully', 'success')
            return redirect(url_for('artistdash')) 
        except Exception as e:
            flash('Error updating artist details: ' + str(e), 'error')
    return render_template('User/artist_edit_details.html', artist=artist)


@app.route('/scorers/<int:users_id>/details/')
def scorers_details(users_id):
    scorer = User.query.get_or_404(users_id)
    return render_template('User/details.html', scorer=scorer)

@app.route('/artist/<int:artist_id>/details/')
def artist_details(artist_id):
    artist = Artists.query.get_or_404(artist_id)
    return render_template('User/artist_details.html', artist=artist)