from app import app, db

class ReshwapItems(db.Model):
    __tablename__ = 'reshwap_items'

    id = db.Column(db.Integer, primary_key=True)
    uploader = db.Column(db.String())
    title = db.Column(db.String())
    details = db.Column(db.String())
    category = db.Column(db.String())
    department = db.Column(db.String())
    money = db.Column(db.String())
    exchange = db.Column(db.String())
    image_one = db.Column(db.String())
    image_two = db.Column(db.String())
    image_three = db.Column(db.String())
    image_four = db.Column(db.String())
    date = db.Column(db.String())
    is_completed = db.Column(db.Boolean())
    school = db.Column(db.String())


    def __init__(self, uploader, title, details, category, department, money, exchange, image_one, image_two, image_three, image_four, date, is_completed, school):
        self.uploader = uploader
        self.title = title
        self.details = details
        self.category = category
        self.department = department
        self.money = money
        self.exchange = exchange
        self.image_one = image_one
        self.image_two = image_two
        self.image_three = image_three
        self.image_four = image_four
        self.date = date
        self.is_completed = is_completed
        self.school = school

    def createSession(self):
        Session = sessionmaker()
        self.session = Session.configure(bind=self.engine)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class ReshwapUsers(db.Model):
    __tablename__ = 'reshwap_users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    profile_pic = db.Column(db.String())
    email = db.Column(db.String())
    signup_date = db.Column(db.String())
    last_login = db.Column(db.String())

    def __init__(self, name, profile_pic, email, signup_date, last_login):
        self.name = name
        self.profile_pic = profile_pic
        self.email = email
        self.signup_date = signup_date
        self.last_login = last_login


    def createSession(self):
        Session = sessionmaker()
        self.session = Session.configure(bind=self.engine)

    def __repr__(self):
        return '<id {}>'.format(self.id)
