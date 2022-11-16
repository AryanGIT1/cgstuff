import app
from app import User, BlogPost, BlogComments, Contact, Adverts, db

with app.app.app_context():
    db.create_all()
    users = User.query.all()
    print(users)
    
    for i in users:
        print(i.user_admin_status)
        print(i.email)
        print(i.password)
        
    blogs = BlogPost.query.all()
    
    for i in blogs:
        print("############")
        print(i.tags)
        print(i.img_link)
        if i.tags == "YouTube Podcast":
            i.yt_link = "g6fnFALEseI"
    
    ads = Adverts.query.all()
    
    for ad in ads:
        if ad.img_add_com:
            ad.img_add_com = ""
        print(ad.company_name)
        print(ad.content)
        