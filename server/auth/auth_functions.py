from json import dumps
from flask import Flask
import re
import jwt
from datetime import datetime

#import functions from another file

APP = Flask(__name__)

class Member:
    def __init__(self, u_id, name_first, name_last)
    

#self.handle = first + last;

data = {
    "messages": {}, 
    "users": [],
    "channel_id": {},
}

SECRET = 'IE4';

#in user_data:
#{'u_id': u_id, 'name_first': name_first, "name_last": name_last, 'token': token, "handle": handle, 'email': email, 'password': password, 'permission_id': permission_id, 'channel_involve': []}

#def get_user_data():
#    global data
#    global SECRET
#    return data.get("user_data")
    #return specific type of data?

#HELPER FUNCTIONS BELOW

def check_valid_email(email): 
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(regex.search(regex,email)):  
        pass
    else:
        raise ValueError

def check_user_details(email, password):
    global data
    is_found = 0;
    for user in data['users']:
        if user['email'] == email:
            if user['password'] == password:
                is_found = 1
                ID = u_id
                break
            else:
                raise ValueError  
    if is_found == 0:
        raise ValueError
    return ID

def check_valid_password(password):
    if len(password) < 6:
        raise ValueError
    else:
        pass

def check_already_user(email):
    global data
    for user in data['users']:
        if user['email'] == email:
            raise ValueError


def check_name(name_first, name_last):
    if ((len(name_first) < 1) | (len(name_last) < 1)):
        raise ValueError
    elif ((len(name_first) > 50 | (len(name_last) > 50)):
        raise ValueError
    else:
        pass

def generateToken(first, last):
    payload = {
        'name_first': name_first,
        'name_last': name_last,
        'time_create': datetime.strftime(datetime.now(), "%m/%d/%Y, %H:%M:%S")
    }
    return str(jwt.encode(payload, SECRET, algorithm='HS256'))

     
def generateHandle(first, last):
    global data
    handle = first + last
    excess = len(handle) - 20
    if excess > 0:
        handle = handle[:21]
    
    if handleAlreadyExists(handle) || len(handle) < 3:
        handle = datetime.strftime(datetime.now(), "%m/%d/%Y, %H:%M:%S")

    return handle
                
def handleAlreadyExists(handle):
    global data
    for user in data['users']:
        if user['handle'] = handle:
            return True
    return False

def findUserFromToken(token):
    global data
    for user in data['users']:
        if user['token'] == token:
            return user

    return None


#HELPER FUNCTIONS ABOVE

@APP.route("/auth/login", methods=['POST'])
def auth_login():
    # fn_auth_login(request.args.get('email'), request.form.get('password'))
    #return dumps({})
    
    global data
    email = request.args.get('email')
    password = request.args.get('password')
    check_valid_email(email)
    u_id = check_user_details(email, password)
    
    u_data[u_id][isLoggedIn] = True
    
    token = jwt.encode({'password': password}, SECRET, algorithm = 'HS256')
    
    return dumps({'u_id': u_id, 'token': token,
    })
    

@APP.route("/auth/logout", methods = ['POST']) #done?
def auth_logout():
    global data
    
    token = request.args.get('token')
    
    user = findUserFromToken(token)
    
    if user is not None:
        user['token'] = None
        is_success = 1

    return dumps({is_sucess})
    
@APP.route("/auth/register", methods=['POST'])  # check handle
def auth_register():
    global data
    email = request.form.get('email')
    password = request.form.get('password')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    
    check_valid_email(email)
    check_valid_password(password)
    check_name(name_first, name_last)
    check_already_user(email)

    u_id = len(data['users']) + 1
    
    token = generateToken(name_first, name_last)
    
    handle = generateHandle(name_first, name_last)

    data['users'].append({
        'u_id': u_id,
        'name_first': name_first,
        'name_last': name_last,
        'token': token,
        'handle': handle,
        'email': email,
        'password': password,
        'permission_id': 1,
        'channel_involve': [],
    })

    return dumps({
        'u_id': u_id,
        'token': token
    })


@APP.route("/auth/passwordreset/request", methods = ['POST'])
def auth_reset_request():
    global data
    email = request.args.get('email')

@APP.route("/auth/passwordreset/reset")
def auth_reset():
    pass


if __name__ == "__main__":
    APP.run()
