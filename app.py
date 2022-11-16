import os
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json 
import supp as supp
from random import randint
from werkzeug.utils import secure_filename

with open("info.json", "r") as c:
    parameters = json.load(c)["parameters"]

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = parameters["database"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = parameters["track_modifications"]
app.config['SECRET_KEY'] = parameters["secret_key"] 
app.config['UPLOAD_FOLDER'] = parameters["upload_folder"]
app.config['MAX_CONTENT_PATH'] = 16 * 1000 * 1000



db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(255), nullable = False)
    password = db.Column(db.String(255), nullable = False)
    user_admin_status = db.Column(db.Boolean, nullable = False, default = False)
    blogs = db.relationship('BlogPost', backref = 'user', lazy = True)

    def __repr__(self):
        return "Id: " + str(self.id) + " Name: " + str(self.name)  


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.String(100), nullable = False)
    title = db.Column(db.String(100), nullable = False)
    desc = db.Column(db.String(225), nullable = False)
    yt_link = db.Column(db.String(225), nullable = True, default = False)
    img_link = db.Column(db.String(512), nullable = True, default = False)
    content = db.Column(db.Text, nullable = False)
    place = db.Column(db.String(256), nullable = False)
    tags = db.Column(db.String(256), nullable = False)
    date = db.Column(db.String , nullable = False, default = datetime.now().strftime("%d-%m-%Y"))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    # comments = db.relationship('BlogComments', backref = 'blogpost', lazy = True)
    
    def __repr__(self):
        return "Id: " + str(self.id) + " Title" + str(self.title)

    
class BlogComments(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name_com = db.Column(db.String(256), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # blog_id = db.Column(db.Integer, db.ForeignKey('blogpost.id'), nullable = False)
    
    def __repr__(self):
        return "Id: " + str(self.id) + " Blog Id" + str(self.blog_id)
    

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.String(256), nullable = False)
    content = db.Column(db.Text, nullable = False)
    email = db.Column(db.String(256), nullable = False)
    
    def __repr__(self):
        return "Id: " + str(self.id) + " Author" + str(self.author)
    

class Adverts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    company_name = db.Column(db.String(256), nullable = False)
    content = db.Column(db.Text, nullable = False)
    img_add_com = db.Column(db.String(512), nullable = True)
    
    def __repr__(self):
        return "Id: " + str(self.id) + " Author" + str(self.author) + " Company Name" + str(self.company_name)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def get_blogs():
    blogs = BlogPost.query.all()
    ft_news, tp_news, fin_news, govt_news, yt_news = [], [], [], [], []
    
    for i in blogs:
        if i.tags == "YouTube Podcast":
            yt_news.append(i)
        if i.tags == "Top News":
            tp_news.append(i)
        if i.tags == "Featured News":
            ft_news.append(i)
        if i.tags == "Finance News":
            fin_news.append(i)
        if i.tags == "Goverment News":
            govt_news.append(i)
            
    if len(ft_news)>6:
        ft_news = ft_news[6]
    if len(tp_news) > 6:
        tp_news = tp_news[6]
    if len(fin_news) > 6:
        fin_news = fin_news[6]
    if len(govt_news) > 6:
        govt_news = govt_news[6]
    if len(yt_news) > 3:
        yt_news = yt_news[3]
        
    return ft_news, tp_news, fin_news, govt_news, yt_news


def info_admin():
    blogs = BlogPost.query.all()
    user_info = User.query.all()
    ads = Adverts.query.all()
    comms = Contact.query.all()
    return blogs, user_info, ads, comms
    

def get_ads():
    ads = Adverts.query.all()
    if len(ads) == 0:
        return False
    
    x = randint(0,len(ads)-1)
    ad = ads[x]
    return ad


@app.route('/', methods=['GET','POST'])
def index():
    ft_news, tp_news, fin_news, govt_news, yt_news = get_blogs()
    return render_template('index.html', msg_green = False, msg_red = False, user = False, ft_news = ft_news, tp_news = tp_news, fin_news = fin_news, govt_news = govt_news, yt_news = yt_news)


@app.route('/about', methods = ['GET', 'POST'])
def about():
    ad = get_ads()
    return render_template('about.html', ad = ad)


@app.route('/contactUs', methods = ['GET', 'POST'])
def contactUs():
    ad = get_ads()
    if request.method == 'POST':
        email = request.form.get('email')
        author = request.form.get('author')
        content = request.form.get('content')
        contact = Contact(author = author,
                          content = content,
                          email = email)
        db.session.add(contact)
        db.session.commit()
        return render_template('about.html', ad = ad, msg_green = True, msg_green_con = "Query sent sucesfully!!")
    else:
        return render_template('about.html', ad = ad, msg_red = True, msg_red_con = "Something went wrong!!",)


@app.route('/blog/<int:id>', methods = ['GET', 'POST'])
def read_blog(id):
    blog = BlogPost.query.get_or_404(id)
    ad = get_ads()
    return render_template('blog.html', blog = blog, ad = ad)


@app.route('/blog/audio/<int:id>', methods = ['GET', 'POST'])
def read_blog_with_audio(id):
    blog = BlogPost.query.get_or_404(id)
    ad = get_ads()
    audio = supp.text_to_voice(blog)
    return render_template('blog.html', blog = blog, ad = ad, audio = audio)

@app.route('/blog/comment/<int:id>')
@login_required
def blog_comments(id):
    blog = BlogPost.query.get_or_404(id)
    ad = get_ads()
    
    if request.method == 'POST':
        content = request.form.get('content')
        comm = BlogComments(author = current_user.name, 
                            content = content,
                            blog_id = id)
        db.session.add(comm)
        db.session.commit()
        return render_template('blog.html', blog = blog, ad = ad, msg_green = True, msg_green_con = "Comment Added!!")
    else:
        return render_template('blog.html', blog = blog, ad = ad, msg_red = True, msg_red_con = "Something Went wrong!")



@app.route('/login',methods = ['GET', 'POST'])
def login():
    ft_news, tp_news, fin_news, govt_news, yt_news = get_blogs()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password = supp.SHA256(password)
        pos_users = User.query.filter_by(email = email).all()
        
        if pos_users:
            for i in pos_users:
                if i.email == email and i.password == password and i.user_admin_status:
                    user = User.query.get(i.id)
                    load_user(user.id)
                    login_user(user)
                    return redirect(url_for('admin'))
                if i.email == email and i.password == password:
                    user = User.query.get(i.id)
                    load_user(user.id)
                    login_user(user)
                    msg = str(user.name) + " has Logged in successfully!!"
                    return render_template('index.html', msg_green = True, msg_green_con = msg, user = current_user, ft_news = ft_news, tp_news = tp_news, fin_news = fin_news, govt_news = govt_news, yt_news = yt_news)
        else:
            msg = "Invalid Details!"
            return render_template('index.html', msg_red = True, msg_red_con = msg, user = False ,ft_news = ft_news, tp_news = tp_news, fin_news = fin_news, govt_news = govt_news, yt_news = yt_news)
    return redirect( url_for('index'))
    


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    ft_news, tp_news, fin_news, govt_news, yt_news = get_blogs()
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        password = supp.SHA256(password)
        user = User(name = name, 
                    password = password, 
                    email = email)
        msg = str(name) + " Welcome!!"
        db.session.add(user)
        db.session.commit()
        load_user(user.id)
        login_user(user)
        return render_template('index.html', msg_green = True, msg_green_con = msg, current_user = False, ft_news = ft_news, tp_news = tp_news, fin_news = fin_news, govt_news = govt_news, yt_news = yt_news, user = current_user)
    else:
        msg = "Invalid Details!"
        return render_template('index.html', msg_red = True, msg_red_con = msg, current_user = False, ft_news = ft_news, tp_news = tp_news, fin_news = fin_news, govt_news = govt_news, yt_news = yt_news)

        
    
@app.route('/logout')
@login_required
def logout():
    ft_news, tp_news, fin_news, govt_news, yt_news = get_blogs()
    msg = str(current_user.name) + " has been logged out!!"
    logout_user()
    return render_template('index.html', msg_green = True, msg_green_con = msg, current_user = False, ft_news = ft_news, tp_news = tp_news, fin_news = fin_news, govt_news = govt_news, yt_news = yt_news)


@app.route('/admin/', methods = ['GET', 'POST'])
@login_required
def admin():
    if current_user.user_admin_status == True:
        blogs, user_info, ads, comms = info_admin()
        msg = "Welcome back Admin!!"
        return render_template('admin.html', msg_green = True, msg_green_con = msg, blogs = blogs, user_info = user_info, ads = ads, comms = comms)
    else:
        return "Invalid Arguments!"

@app.route('/admin/del/ads/<int:id>', methods = ['GET', 'POST'])
@login_required
def delads(id):
    if current_user.user_admin_status == True:
        ad = Adverts.query.get_or_404(id)
        db.session.delete(ad)
        db.session.commit()
        blogs, user_info, ads, comms = info_admin()
        return render_template('admin.html', blogs = blogs, user_info = user_info, ads = ads, comms = comms, msg_red = True, msg_red_con = "Ad Deleted!!", user = current_user)
    else:
        return "Invalid Arguments!"

@app.route('/admin/del/com/<int:id>', methods = ['GET', 'POST'])
@login_required
def delcom(id):
    if current_user.user_admin_status == True:
        com = Contact.query.get_or_404(id)
        db.session.delete(com)
        db.session.commit()
        blogs, user_info, ads, comms = info_admin()
        return render_template('admin.html', blogs = blogs, user_info = user_info, ads = ads, comms = comms, msg_red = True, msg_red_con = "Communication Deleted!!", user = current_user)
    else:
        return "Invalid Arguments!"


@app.route('/admin/del/blog/<int:id>', methods = ['GET', 'POST'])
@login_required
def delblog(id):
    if current_user.user_admin_status == True:
        blog = BlogPost.query.get_or_404(id)
        db.session.delete(blog)
        db.session.commit()
        blogs, user_info, ads, comms = info_admin()
        return render_template('admin.html', blogs = blogs, user_info = user_info, ads = ads, comms = comms, msg_red = True, msg_red_con = "Blog Deleted!!", user = current_user)
    else:
        return "Invalid Arguments!"


@app.route('/admin/del/blogcoms/<int:id>', methods = ['GET', 'POST'])
@login_required
def delblogcoms(id):
    if current_user.user_admin_status == True:
        bc = BlogComments.query.get_or_404(id)
        db.session.delete(bc)
        db.session.commit()
        blogs, user_info, ads, comms = info_admin()
        return render_template('admin.html', blogs = blogs, user_info = user_info, ads = ads, comms = comms, msg_red = True, msg_red_con = "Blog Comment Deleted!!", user = current_user)
    else:
        return "Invalid Arguments!"
    

@app.route('/admin/create/blog',  methods=("POST", "GET"))
@login_required
def createBlog():    
    if request.method == 'POST' and current_user.user_admin_status == True:
        if request.files['img_link'].filename == "":
            img_link = ""
        else:
            uploaded_img = request.files['img_link']
            img_filename = secure_filename(uploaded_img.filename)
            uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
            img_link = str("/static/imgs/") + str(img_filename)
        
        author = request.form.get('author')
        title = request.form.get('title')
        desc = request.form.get('desc')
        yt_link = request.form.get('yt_link')
        content = request.form.get('content')
        place = request.form.get('place')
        tags = request.form.get('tags')
        
        if author == "":
            author = current_user.name
        elif title == "":
            blogs, user_info, ads, comms = info_admin()
            return render_template('admin.html', blogs = blogs, user_info = user_info, ads = ads, comms = comms, msg_red = True, msg_red_con = "Pls enter a title", user = current_user)
        elif desc == "":
            blogs, user_info, ads, comms = info_admin()
            return render_template('admin.html', blogs = blogs, user_info = user_info, ads = ads, comms = comms, msg_red = True, msg_red_con = "Pls enter a Description", user = current_user)
        elif yt_link == "":
            yt_link = ""
        elif content == "":
            blogs, user_info, ads, comms = info_admin()
            return render_template('admin.html', blogs = blogs, user_info = user_info, ads = ads, comms = comms, msg_red = True, msg_red_con = "Pls enter the Content", user = current_user)
        elif place == "":
            blogs, user_info, ads, comms = info_admin()
            return render_template('admin.html', blogs = blogs, user_info = user_info, ads = ads, comms = comms, msg_red = True, msg_red_con = "Pls enter the place", user = current_user)
        elif tags == "":
            blogs, user_info, ads, comms = info_admin()
            return render_template('admin.html', blogs = blogs, user_info = user_info, ads = ads, comms = comms, msg_red = True, msg_red_con = "Pls enter the Tags", user = current_user)
        
        new_blog = BlogPost(author = author, 
                            title = title,
                            desc = desc,
                            yt_link = yt_link,
                            img_link = img_link,
                            content = content,
                            place = place,
                            tags = tags,
                            user_id = current_user.id)
        
        db.session.add(new_blog)
        db.session.commit()
        blogs, user_info, ads, comms = info_admin()
        return render_template('admin.html', blogs = blogs, user_info = user_info, ads = ads, comms = comms, msg_green = True, msg_green_con = "Blog Added!!", user = current_user)
                  
    blogs, user_info, ads, comms = info_admin()
    return render_template('admin.html', blogs = blogs, user_info = user_info, ads = ads, comms = comms, msg_red = True, msg_red_con = "Something went wrong!!", user = current_user)


@app.route('/admin/create/adverts/', methods = ['GET','POST'])
@login_required
def adverts():
    if request.method == 'POST' and current_user.user_admin_status == True:
        company_name = request.form.get('company_name')
        content = request.form.get('content')
        
        if request.files['img_link'].filename == "":
            img_link = ""
        else:
            uploaded_img = request.files['img_link']
            img_filename = secure_filename(uploaded_img.filename)
            uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
            img_link = str("/static/imgs/") + str(img_filename)
        
        ads = Adverts(company_name = company_name,
                      content = content,
                      img_add_com = img_link)
        
        db.session.add(ads)
        db.session.commit()
        blogs, user_info, ads, comms = info_admin()
        return render_template('admin.html', blogs = blogs, user_info = user_info, ads = ads, comms = comms, msg_green = True, msg_green_con = "Ad Created!!", user = current_user)
    blogs, user_info, ads, comms = info_admin()
    return render_template('admin.html', blogs = blogs, user_info = user_info, ads = ads, comms = comms, msg_green = True, msg_green_con = "Something went wrong!!", user = current_user)


@app.route('/admin/edit/blog/<int:id>', methods=['GET', 'POST'])
@login_required
def edid_blog(id):
    blog = BlogPost.query.get_or_404(id)
    if request.method == 'POST' and current_user.user_admin_status == True:
        blog.title = request.form.get('title')
        blog.desc = request.form.get('desc')
        blog.yt_link = request.form.get('yt_link')
        blog.content = request.form.get('content')
        blog.place = request.form.get('place')
        blog.tags = request.form.get('tags')
        uploaded_img = request.files['img_link']
        if uploaded_img == None:
            img_link = ""
        else:
            img_filename = secure_filename(uploaded_img.filename)
            uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
            img_link = str("/static/img/") + str(img_filename)
            
        blog.img_link = img_link
        
        blogs, user_info, ads, comms = info_admin()
        return render_template('admin.html', blogs = blogs, user_info = user_info, ads = ads, comms = comms, msg_green = True, msg_green_con = "Changes Added!!", user = current_user)
    return render_template('blog.html', blog = blog, admin_con = True)



if __name__ == '__main__':
    app.run(debug = True, threaded = True)