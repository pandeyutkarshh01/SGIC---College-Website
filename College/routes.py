import secrets, os
from flask import render_template, flash, redirect, url_for, request, send_file, abort
from College import app, db , bcrypt
from College.forms import FeedbackForm, LoginForm, RegistrationForm, UpdateAccountForm, AdmissionForm, SearchForm
from College.models import User, Feedback, Admission, Student
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
from werkzeug.utils import secure_filename
import os
from fpdf import FPDF
import datetime

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form =FeedbackForm()
    if form.validate_on_submit():
        feedback_content = Feedback(username=form.name.data, email=form.email.data, phone=form.phone.data, feedback=form.feedback.data, author=current_user)
        db.session.add(feedback_content)
        db.session.commit()
        flash('Your feedback has been taken. Thank You!', 'success')
        return redirect(url_for('home'))
    return render_template('home.html', title='Feedback', form=form)


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/feedback")
@login_required
def feedback():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    feedbacks = Feedback.query.all()

    return render_template("feed.html", feedback=feedbacks, image_file=image_file)
 
@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/admission", methods=['GET', 'POST'])
def admission():
    form = AdmissionForm()
    if request.method == 'POST':
        name = request.form['name']
        father_name = request.form['father_name']
        mother_name = request.form['mother_name']
        email = request.form['email']
        phone = request.form['phone']
        dob = request.form['dob']
        address = request.form['address']
        photo = request.files['photo']
        signature = request.files['signature']

        if photo and signature:
            photo_filename = secure_filename(photo.filename)
            signature_filename = secure_filename(signature.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
            signature.save(os.path.join(app.config['UPLOAD_FOLDER'], signature_filename))

            new_admission = Admission(name=name, father_name=father_name,mother_name=mother_name, email=email, phone=phone,
                                      dob=dob, address=address, photo=photo_filename, signature=signature_filename)
            db.session.add(new_admission)
            db.session.commit()
            
            return redirect(url_for('generate_pdf', admission_id=new_admission.id))
    
    return render_template("admission_form.html", form=form)


app.route('/generate_pdf/<int:admission_id>')
def generate_pdf(admission_id):
    admission = Admission.query.get_or_404(admission_id)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Admission Form", ln=True, align='C')
    pdf.ln(10)
    
    pdf.cell(200, 10, txt=f"Name: {admission.name}", ln=True)
    pdf.cell(200, 10, txt=f"Father's Name: {admission.father_name}", ln=True)
    pdf.cell(200, 10, txt=f"Mother's Name: {admission.mother_name}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {admission.email}", ln=True)
    pdf.cell(200, 10, txt=f"Phone: {admission.phone}", ln=True)
    pdf.cell(200, 10, txt=f"Date of Birth: {admission.dob}", ln=True)
    pdf.cell(200, 10, txt=f"Address: {admission.address}", ln=True)
    pdf.ln(10)
    
    photo_path = os.path.join(app.config['UPLOAD_FOLDER'], admission.photo)
    signature_path = os.path.join(app.config['UPLOAD_FOLDER'], admission.signature)
    
    pdf.cell(200, 10, txt="Photo:", ln=True)
    pdf.image(photo_path, x=10, y=pdf.get_y(), w=30)
    pdf.ln(35)
    pdf.cell(200, 10, txt="Signature:", ln=True)
    pdf.image(signature_path, x=10, y=pdf.get_y(), w=30)
    
    pdf_filename = f"static/{admission.name}_admission.pdf"
    pdf.output(pdf_filename)
    
    return send_file(pdf_filename, as_attachment=True), redirect(url_for('generate_pdf', ))



@app.route('/submit', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        name = request.form['name']
        father_name = request.form['father_name']
        mother_name = request.form['mother_name']
        email = request.form['email']
        phone = request.form['phone']
        dob = request.form['dob']
        address = request.form['address']

        # Save uploaded files
        photo = request.files['photo']
        signature = request.files['signature']
        
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
        signature_path = os.path.join(app.config['UPLOAD_FOLDER'], signature.filename)

        photo.save(photo_path)
        signature.save(signature_path)

        student_data = Admission(name=name, father_name=father_name, mother_name=mother_name, email=email, phone=phone, dob=dob, address=address, photo=photo_path, signature=signature_path)
        db.session.add(student_data)
        db.session.commit()
        flash('Your form has been submitted. Print the hard Copy and submit in your college. Thank You!', 'success')

        return render_template('print_preview.html', name=name, father_name=father_name, mother_name=mother_name, email=email, phone=phone, dob=dob , address=address, photo=photo.filename, signature=signature.filename, date=datetime.date.today().strftime(f'%d/%m/%Y'))







@app.route("/contact")
def contact():
    return render_template("contact.html")






@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created You are now able to login', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful Please Check your email or password', 'danger')

    return render_template("login.html", title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    output_size = (100, 100)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route('/my_account', methods=['GET', 'POST'])
@login_required
def my_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account_info'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("my_account.html", title='Account', image_file=image_file, form=form)



@app.route('/account_info', methods=['GET', 'POST'])
@login_required
def account_info():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        return redirect(url_for('account_info'))
    elif request.method == 'GET':
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
        return render_template("account_info.html", title='Account', image_file=image_file, form=form)
    
