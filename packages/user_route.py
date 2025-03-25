from flask import render_template,flash,request,redirect,session
from packages import app
from packages.user_forms import UserForm,ArtistForm,User_reg,Artist_Reg



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

@app.route('/login/', methods=['GET', 'POST'])
def login():
    user=UserForm()
    artist=ArtistForm()
    if user.validate_on_submit():
        if request.method == 'POST':
            email = request.form.get('email')
            pwd = request.form.get('pwd')

            if email == ''  and pwd == '':
                flash('Please fill in all required fields', category='error')
            else:
                session['fullname'] =  email.split('@')[0]
                flash('You are now logged in ', category='success')
                return redirect('/userdash/')
    if artist.validate_on_submit():
        if request.method=='POST':
            fname=request.form.get('fname')
            lname=request.form.get('lname')
            if fname =='' and lname=='':
                flash('Please fill in all required fields', category='error')  
            else:
                session['fullname'] = f'{fname} {lname}'
                flash('You are now logged in ', category='success')
                return redirect('/artistdash/')

    return render_template('User/user_login.html',user=user,artist=artist)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    user=User_reg()
    artist=Artist_Reg()
    if request.method == 'POST':
         if user.validate_on_submit():
            fname = request.form.get('fname')
            lname = request.form.get('lname')
            email = request.form.get('email')
            pwd = request.form.get('pwd')
            phone=request.form.get('phone')
            file=request.form.get('file')
            file2=request.form.get('file2')

            if email == ''  and pwd == '' and fname == '' and lname == '' and phone=='' and file=='' and file2=='':
                flash('Please fill in all required fields', category='error')
            else:
                session['fullname'] =  f'{fname} {lname}'
                flash('You are now logged in ', category='success')
                return redirect('/userdash/')
    elif artist.validate_on_submit():
            fname=request.form.get('fname')
            lname=request.form.get('lname')
            file=request.form.get('file')
            pwd=request.form.get('pwd')
            if fname =='' and lname=='' and file=='' and pwd=='':
                flash('Please fill in all required fields', category='error')  
            else:
                session['fullname'] = f'{fname} {lname}'
                flash('You are now logged in ', category='success')
                return redirect('/artistdash/')
    
    return render_template('User/user_reg.html',user=user,artist=artist)


@app.route('/artists/')
def artists():
    return render_template('User/artists.html')

   
@app.route('/user_reg/')
def user_reg():
    return render_template('User/user_reg.html')

@app.route('/scorers/')
def scorers():
    return render_template('User/scorers.html')

@app.route('/artistdash/')
def artistdash():
        if session.get('fullname')==None:
          return redirect('/login/')
        else:
          return render_template('User/artist_dash.html')

@app.route('/userdash/')
def userdash():
    if session.get('fullname')==None:
        return redirect('/login/')
    else:
        return render_template('User/user_dash.html')

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