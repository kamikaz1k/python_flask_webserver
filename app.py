from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def main():
	return render_template("index.html")

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

if __name__ == "__main__":
	app.run()



# CREATE TABLE `BucketList`.`tbl_user` (`user_id` BIGINT NOT NULL AUTO_INCREMENT, `user_name` VARCHAR(45) NULL, `user_username` VARCHAR(45) NULL, `user_password` VARCHAR(45) NULL, PRIMARY KEY (`user_id`));

# DELIMITER $$ CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`( IN p_name VARCHAR(20), IN p_username VARCHAR(20), IN p_password VARCHAR(20) ) BEGIN if ( select exists (select 1 from tbl_user where user_username = p_username) ) THEN select 'Username Exists !!'; ELSE insert into tbl_user ( user_name, user_username, user_password ) values ( p_name, p_username, p_password ); END IF; END$$ DELIMITER;

# select * from BucketList.information_schema.routines where routine_type = 'PROCEDURE';