from flask import Flask, render_template, json, request
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

# from pprint import pprint

app = Flask(__name__)

mysql = MySQL()

# Load config file for DB user info
with open('config.json') as data_file: 
    config = json.load(data_file)

# print config

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = config["username"]
app.config['MYSQL_DATABASE_PASSWORD'] = config["password"]
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
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

@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')

if __name__ == "__main__":
	app.run()
