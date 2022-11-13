import app
from app import User, BlogPost, BlogComments, Contact, Adverts, db

with app.app.app_context():
    db.create_all()
    users = User.query.all()
    for i in users:
        if i.email == "admin@admin.com":
            i.user_admin_status = True
    db.session.commit()
    for i in users:
        print(i.user_admin_status)