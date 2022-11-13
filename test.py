import app
from app import User, BlogPost, BlogComments, Contact, Adverts, db

with app.app.app_context():
    db.create_all()
    users = User.query.all()
    print(users)
    blogs = BlogPost.query.all()
    for i in blogs:
        print("############")
        print(i.tags)
        print(i.img_link)
        