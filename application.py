from flask import *
import random, string
from application import db
from application.models import flashcard_users as fc_u
import requests
from urllib import urlencode


def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# TODO: Change this
application.secret_key = 'YOUR_SECRET_KEY '


@application.route('/')
@application.route('/index')
def index_route():
   # TODO: Change this
    client_id = 'GET_FROM_QUIZLET'
    scope = 'read'
    state = randomword(10)

    redirect_uri = 'https://google.com'

    url = 'https://quizlet.com/authorize?response_type=code&client_id={}&scope={}&state={}'.format(
        client_id, scope, state)

    context = {
        'url' : url
    }

    session['state'] = state

    return render_template('index.html', **context)

@application.route('/steptwo')
def step_two_route():
    state = request.args.get('state')

    assert(state == session.get('state'))

    code = request.args.get('code')
    
    grant_type = 'authorization_code'
      
    # TODO: Change this
    redirect_uri = 'REDIRECT_URI'
    #redirect_uri = 'http://localhost:5000/steptwo'

    # TODO: Change this
    user_and_pass = 'CHANGE'

    headers = { 'Authorization' : 'Basic %s' %  user_and_pass }

    url = 'https://api.quizlet.com/oauth/token'

    params = {
        'code' : code,
        'grant_type' : grant_type,
        'redirect_uri': redirect_uri
    }

    r = requests.post(url, params=params, headers=headers)

    quizlet_username = json.loads(r.text)['user_id']
    access_token = json.loads(r.text)['access_token']

    pin = None

    context = {}

    result = fc_u.query.filter_by(quizlet_username=quizlet_username).first()

    if result == None:
        while True:
            pin_try ="%04d" % random.randint(0,9999)
            result = fc_u.query.filter_by(pin_code=pin_try).first()
            if result == None:
                print(pin_try, "is the pin for new user", quizlet_username)
                new_user = fc_u(quizlet_username, access_token, pin_try)

                db.session.add(new_user)
                db.session.commit()        
                db.session.close()

                pin = pin_try
                print('added, commited, and closed.')
                context['greeting'] = 'Welcome to Flashcard Helper {}'.format(quizlet_username)
                context['pin_code'] = pin
                break
    else:
        print(result)
        pin = result.pin_code
        context['greeting'] = 'Welcome back to Flashcard Helper {}'.format(quizlet_username)
        context['pin_code'] = pin
        print('found a user')
    
    return render_template('index.html', **context)


# run the app.
if __name__ == "__main__":
    application.run(host='0.0.0.0')
