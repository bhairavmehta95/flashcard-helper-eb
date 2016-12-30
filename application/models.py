from application import db

class flashcard_users(db.Model):
    access_token = db.Column(db.String)
    quizlet_username = db.Column(db.String)
    pin_code = db.Column(db.String, unique=True, primary_key=True)
    
    def __init__(self, quizlet_username, access_token, pin_code):
        self.quizlet_username = quizlet_username
        self.access_token = access_token
        self.pin_code = pin_code

    def __repr__(self):
        return 'User:{} with PIN: {}'.format(self.quizlet_username, self.pin_code)