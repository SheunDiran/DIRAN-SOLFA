from flask import render_template,flash,request,redirect,session
from packages import app
from packages.myforms import UserForm,AdminForm,ArtistForm,User_reg,Artist_Reg, Admin_Reg



@app.after_request
def after_request(response):
    response.headers['Cache-Control']='no-cache','no-store','must-revalidate'
    return response

@app.route('/index/')
def index():
    email = session.get('email')
    return render_template('index.html',email=email)

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/search/')
def search():
    return render_template('search.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    user=UserForm()
    admin=AdminForm()
    artist=ArtistForm()
    if user.validate_on_submit():
        if request.method == 'POST':
            email = request.form.get('email')
            pwd = request.form.get('pwd')

            if email == ''  and pwd == '':
                flash('Please fill in all required fields', category='error')
            else:
                session['fullname'] =  f'{fname} {lname}'
                flash('You are now logged in ', category='success')
                return redirect('/userdash/')
    if admin.validate_on_submit():
        if request.method=='POST':
            username=request.form.get('username')
            pwd=request.form.get('pwd')
            if username=='' and pwd=='':
             flash('Please fill in all required fields', category='error')   
            else:
                session['username'] = username
                flash('You are now logged in ', category='success')
                return redirect('/admindash/')
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

    return render_template('user_login.html',user=user,admin=admin,artist=artist)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    user=User_reg()
    admin= Admin_Reg()
    artist=Artist_Reg()
    if user.validate_on_submit():
        if request.method == 'POST':
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
    if admin.validate_on_submit():
        if request.method=='POST':
            username=request.form.get('username')
            pwd=request.form.get('pwd')
            if username=='' and pwd=='' :
             flash('Please fill in all required fields', category='error')   
            else:
                session['username'] = username
                flash('You are now logged in ', category='success')
                return redirect('/admindash/')
    if artist.validate_on_submit():
        if request.method=='POST':
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

    return render_template('user_reg.html',user=user,admin=admin,artist=artist)


@app.route('/artists/')
def artists():
    return render_template('artist.html')

   
@app.route('/user_reg/')
def user_reg():
    return render_template('user_reg.html')

@app.route('/scorers/')
def scorers():
    return render_template('scorers.html')

@app.route('/artistdash/')
def artistdash():
    return render_template('artist_dash.html')

@app.route('/admindash/')
def admindash():
    return render_template('admin_dash.html')

@app.route('/userdash/')
def userdash():
    return render_template('user_dash.html')

@app.route('/songs/')
def songs():
    return render_template('songs.html')

@app.route('/omemma/')
def omemma():
    return render_template('omemma.html')

@app.route('/worthy/')
def worthy():
    return render_template('worthy.html')


@app.route('/logout/')
def logout():
    session.pop('email')
    return render_template('index.html')