from application import db

class flashcard_users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String)
    quizlet_username = db.Column(db.String)
    
    def __init__(self, quizlet_username, access_token):
        self.quizlet_username = quizlet_username
        self.access_token = access_token

    def __repr__(self):
        return '<Data %r>' % self.notes