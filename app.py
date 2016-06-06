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

# Connect to DB
conn = mysql.connect()

# Retrieve DB Cursor
cursor = conn.cursor()

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

    # Generate password hash
    _hashed_password = generate_password_hash(_password)
    print "_hashed_password: ", _hashed_password

    cursor.callproc('sp_createUser',(_name,_email,_hashed_password))

    data = cursor.fetchall()
     
    if len(data) is 0:
        conn.commit()
        return json.dumps({'message':'User created successfully !'})
    else:
        return json.dumps({'error':str(data[0])})

    # # validate the received values
    # if _name and _email and _password:
    #     return json.dumps({'html':'<span>All fields good !!</span>'})
    # else:
    #     return json.dumps({'html':'<span>Enter the required fields</span>'})

if __name__ == "__main__":
	app.run()



# CREATE TABLE `BucketList`.`tbl_user` (`user_id` BIGINT NOT NULL AUTO_INCREMENT, `user_name` VARCHAR(45) NULL, `user_username` VARCHAR(45) NULL, `user_password` VARCHAR(45) NULL, PRIMARY KEY (`user_id`));

# DELIMITER $$ CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`( IN p_name VARCHAR(20), IN p_username VARCHAR(20), IN p_password VARCHAR(20) ) BEGIN if ( select exists (select 1 from tbl_user where user_username = p_username) ) THEN select 'Username Exists !!'; ELSE insert into tbl_user ( user_name, user_username, user_password ) values ( p_name, p_username, p_password ); END IF; END$$ DELIMITER;

# select * from BucketList.information_schema.routines where routine_type = 'PROCEDURE';