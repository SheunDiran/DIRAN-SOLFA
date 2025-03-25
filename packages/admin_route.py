from flask import render_template,flash,request,redirect,session
from packages import app
from packages.admin_forms import AdminForm, Admin_Reg

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
    email = session.get('email')
    return render_template('Admin/index.html',email=email)

@app.route('/admin/login/', methods=['GET', 'POST'])
def admin_login():
    admin=AdminForm()
    if admin.validate_on_submit():
        if request.method=='POST':
            username=request.form.get('username')
            pwd=request.form.get('pwd')
            if username=='' and pwd=='':
             flash('Please fill in all required fields', category='error')   
            else:
                session['fullname'] = username
                flash('You are now logged in ', category='success')
                return redirect('/Admin/admindash/')


    return render_template('Admin/login.html',admin=admin)

@app.route('/admin/register/', methods=['GET', 'POST'])
def admin_register():
    admin= Admin_Reg()
    if admin.validate_on_submit():
        if request.method=='POST':
            username=request.form.get('username')
            pwd=request.form.get('pwd')
            if username=='' and pwd=='':
             flash('Please fill in all required fields', category='error')   
            else:
                session['fullname'] = username
                flash('You are now logged in ', category='success')
                return redirect('/Admin/admindash/')
    return render_template('Admin/admin_reg.html',admin=admin)


@app.route('/admin/artists/')
def admin_artists():
    return render_template('Admin/artists.html')

   
@app.route('/admin/users/')
def admin_users():
    return render_template('Admin/users.html')


@app.route('/admin/scorers/')
def admin_scorers():
    return render_template('Admin/scorers.html')

@app.route('/Admin/admindash/')
def admindash():
     if session.get('fullname')==None:
        return redirect('/admin/login/')
     else:
      return render_template('Admin/admin_dash.html')

@app.route('/admin/songs/')
def admin_songs():
    return render_template('Admin/songs.html')

@app.route('/admin/logout/')
def admin_logout():
    if 'fullname' in session:
        session.pop('fullname')
    return render_template('Admin/index.html')