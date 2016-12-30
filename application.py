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
application.secret_key = 'kZGvjUVmmbtXj2akXxwKX6nm '


@application.route('/')
@application.route('/index')
def index_route():
    client_id = 'tSV43kqc3K'
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

    # assert(state == session.get('state'))

    code = request.args.get('code')

    grant_type = 'authorization_code'
    redirect_uri = 'http://flashcard-env.epum35ydrs.us-west-2.elasticbeanstalk.com/steptwo'
    #redirect_uri = 'http://localhost:5000/steptwo'

    user_and_pass = 'dFNWNDNrcWMzSzpIYXJUM1pwTUplZ0FKTTREam5NUjgy'

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

    print(quizlet_username, access_token)


    # try:     
    new_user = fc_u(quizlet_username, access_token)

    db.session.add(new_user)
    db.session.commit()        
    db.session.close()

    print('added, commited, and closed.')

    # except:
    #     db.session.rollback()
    #     print('rolled back')

    url_fragment_dic = {
        "token_type" : "bearer",
        "access_token" : access_token,
        "state" : state
    }

    url_fragment = urlencode(url_fragment_dic)

    full_redirect_url = 'https://pitangui.amazon.com/spa/skill/account-linking-status.html?vendorId=M1N25YHTSEDAWK#' + url_fragment

    print url_fragment, full_redirect_url

    context = {
        'url' : full_redirect_url
    }

    return render_template('index.html', **context)


# run the app.
if __name__ == "__main__":
    application.run(host='0.0.0.0')
