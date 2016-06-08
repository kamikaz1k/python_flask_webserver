from flask import Flask, render_template, json, request, redirect, session
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

# from pprint import pprint

# App Configurations
app = Flask(__name__)

# Load config file for DB user info
with open('config.json') as data_file: 
    config = json.load(data_file)

# Set secret key to use the session module
app.secret_key = config["secret_key"]

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = config["username"]
app.config['MYSQL_DATABASE_PASSWORD'] = config["password"]
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL()
mysql.init_app(app)

# Routing Definitions
@app.route("/")
def main():
	return render_template("index.html")

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp', methods=['POST'])
def signUp():
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    # Check that the forms were filled out
    if _name and _email and _password:

        # Generate password hash
        _hashed_password = generate_password_hash(_password)
        print "_hashed_password: ", _hashed_password

        # Wrap db calls in try/except/finally
        try:
            # Connect to DB
            conn = mysql.connect()

            # Retrieve DB Cursor
            cursor = conn.cursor()

            # Make query
            cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
            data = cursor.fetchall()

             
            if len(data) is 0:
                # Commit changes to db
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                print "Username already exists? - ", data
                return json.dumps({'error':str(data[0])})

        # Catch any exceptions
        except Exception as e:
            return json.dumps({'error':str(e)})

        # Finally close cursor & connection so that next 
        # transaction can take place separately
        finally:
            cursor.close()
            conn.close()

    # IF the signup form fields were not populated
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

@app.route('/showSignIn')
def showSignIn():
    return render_template('signin.html')

@app.route('/validateLogin', methods=['POST'])
def validateLogin():

    _username = request.form['inputEmail']
    _password = request.form['inputPassword']

    if _username and _password:
        
        try:
            # Connect to DB
            conn = mysql.connect()

            # Retrieve DB Cursor
            cursor = conn.cursor()

            # Make query
            cursor.callproc('sp_validateLogin',(_username,))
            data = cursor.fetchall()

            # Check there was data returned, otherwise return error
            if len(data) > 0:
                # Check the hash against the entered value
                if check_password_hash(str(data[0][3]),_password):
                    session['user'] = data[0][0]
                    return redirect('/userHome')
                else:
                    return render_template('error.html', error = 'Wrong Password.')
            else:
                return render_template('error.html', error = 'Wrong Email address.')
     
        except Exception as e:
            return render_template('error.html', error = str(e))

        # Finally close cursor & connection so that next 
        # transaction can take place separately
        finally:
            cursor.close()
            conn.close()

    # IF the signup form fields were not populated
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})
    
@app.route('/userHome')
def showUserHome():
    print "Session Info: ", session.get('user')
    # return render_template('userHome.html')
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html', error = 'Unauthorized Access')

@app.route('/logOut')
def logOut():
    session.pop('user', None)
    return redirect('/')

if __name__ == "__main__":
	app.run()
