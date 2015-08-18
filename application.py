from functools import wraps
from flask import request, Response, Flask, render_template, send_from_directory, redirect
from datetime import datetime, date, time
import encoder, json, os
import bitly_api

application = Flask(__name__, instance_relative_config=False)

app_settings = os.environ.get("APP_SETTINGS")

if app_settings == None:
    app_settings = config.DevelopmentConfig

application.config.from_object( app_settings )
s3_bucket = application.config["S3_BUCKET"]
use_bucket = application.config["USE_BUCKET"]
hash_split = '$$!!'

# ---------------------------------------------------------

@application.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js/', path)

@application.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css/', path)

@application.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('static/fonts/', path)

@application.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('static/img/', path)

@application.route('/mov/<path:path>')
def send_mov(path):
    return send_from_directory('static/mov/', path)

@application.route('/favicon.ico')
def send_favicon():
    return send_from_directory('static/', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# ---------------------------------------------------------

@application.context_processor
def inject_static_url():
    """
    Inject the variable 'static_url' into the templates. Grab it from
    the environment variable STATIC_URL, or use the default.

    Template variable will always have a trailing slash.

    """
    if( use_bucket ):
        static_url = s3_bucket #os.environ.get('STATIC_URL', application.static_url_path)
    else:
        static_url = ""

    if not static_url.endswith('/'):
        static_url += '/'

    return dict(static_url = static_url)

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# ---------------------------------------------------------

@application.route('/')
@application.route('/fav')
def index():
    return render_template('index.html', name='test')
    #return 'Hello World!'

@application.route('/admin')
@requires_auth
def admin_page():
    return render_template('admin.html')

@application.route('/gethash', methods=['POST'])
def get_hash():
    
    user_name = str(request.form['UserName']);
    expiration_date = str(request.form['InputDateTime']);

    #convert date
    #expiration_date = datetime.strptime(expiration_date, "%m/%d/%y")

    hash, enc = encoder.encode_data(user_name + '$$' + expiration_date)
    encoded_data = hash + hash_split + enc
    longurl = request.url_root + encoded_data
    print longurl

    b = bitly_api.Connection(access_token="####")

    print request.url_root

    if not "localhost" in request.url_root:
        bitly = b.shorten(uri=longurl)
        myurl = bitly['url']
    else:
        myurl = longurl

    return myurl

@application.route('/<userhash>')
def show_content(userhash):

    if not hash_split in userhash:
        return redirect("/", code=302)

    my_hash = userhash.split(hash_split)[0]
    my_enc = userhash.split(hash_split)[1]
    my_info = encoder.decode_data(my_hash, my_enc)

    # get values
    username = my_info.split('$$')[0]
    expiration_date = my_info.split('$$')[1]

    # check date
    expiration_date = datetime.strptime(expiration_date, "%m/%d/%y")
    current_date = datetime.now()

    # if date ok - show page + add variable for google tracking
    if( current_date < expiration_date ):
        return render_template('main.html', user_name=username)
    # if date is not ok - redirect to the main page
    else:
        return redirect("/", code=302)

    #return username + "<br>" + str(expiration_date)


# ---------------------------------------------------------

if __name__ == '__main__':
    application.debug = True
    application.run()



# basic http auth for admin
# list of created page + expiration date
# create a page from existing templates