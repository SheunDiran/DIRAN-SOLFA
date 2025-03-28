from flask import render_template,flash,request,redirect,session
from packages import app
from packages.user_forms import UserForm,ArtistForm,User_reg,Artist_Reg
from packages.models import db,User



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
    user = UserForm()
    if user.validate_on_submit():
        email = user.email.data
        pwd = user.pwd.data
        session['email'] = email
        session['fullname'] = email.split('@')[0]
        session['password'] = pwd
        flash('You are now logged in ', category='success')
        cust = User(users_email=email,users_password=pwd)
        db.session.add(cust)
        db.session.commit()
        return redirect('/userdash/')
    return render_template('User/user_login.html', user=user)


@app.route('/artist/login/', methods=['GET', 'POST'])
def artist_login():
    artist=ArtistForm()
    if artist.validate_on_submit():
        if request.method == 'POST':
            fname=request.form.get('fname')
            lname=request.form.get('lname')
            if fname =='' and lname=='':
                flash('Please fill in all required fields', category='error')  
            else:
                session['fullname'] = f'{fname} {lname}'
                flash('You are now logged in ', category='success')
                return redirect('/artistdash/')
       
   
    return render_template('User/artist_login.html',artist=artist)
 
           



@app.route('/user/register/', methods=['GET', 'POST'])
def user_register():
    user= User_reg()
    if request.method=='POST':
        if user.validate_on_submit():
            session['fullname'] = f"{user.fname.data} {user.lname.data}"
            session['email'] = user.email.data
            session['password'] = user.pwd.data
            session['phone'] = user.phone.data
            flash('You are now logged in ', category='success')
            return redirect('/userdash/')
    return render_template('User/user_reg.html',user=user)



@app.route('/artist/register/', methods=['GET', 'POST'])
def artist_register():
    artist = Artist_Reg()
    if request.method=='POST':
        if artist.validate_on_submit():
            session['fullname'] = f"{artist.fname.data} {artist.lname.data}"
            session['pwd'] = artist.pwd.data
            flash('You are now logged in ', category='success')
            return redirect('/artistdash/')
    return render_template('User/artist_reg.html', artist=artist)

@app.route('/artists/')
def artists():
    return render_template('User/artists.html')


@app.route('/scorers/')
def scorers():
    return render_template('User/scorers.html')

@app.route('/userdash/')
def userdash():
    if session.get('fullname')==None:
        return redirect('/user/login/')
    else:
        return render_template('User/user_dash.html')
    
@app.route('/artistdash/')
def artistdash():
    if session.get('fullname')==None:
        return redirect('/artist/login/')
    else:
        return render_template('User/artist_dash.html')    

@app.route('/songs/')
def songs():
      if session.get('fullname')==None:
          return redirect('/login/')
      elif session.get('fullname')==None:
          return redirect('/login/')
      return render_template('User/songs.html')

@app.route('/omemma/')
def omemma():
    return render_template('User/omemma.html')

@app.route('/worthy/')
def worthy():
    return render_template('User/worthy.html')


@app.route('/logout/')
def logout():
    session.pop('fullname', None)
    flash('You have been logged out.', category='success')
    return redirect('/index')



