from flask import Flask, render_template, request, redirect, url_for, session
from Forms import *
from Model import *
from passlib.hash import pbkdf2_sha256
import shelve

from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "verysecretkey"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/aston")
def aston():
    return render_template("aston.html")

"""@app.route("/seatplan")
def seatplan():
    return render_template("temporary.html")"""

"""@app.route("/temporary")
def temporary():
    return render_template("temporary.html")"""

@app.route("/reserveseat", methods=["GET", "POST"])
def reserveseat():
    select = SeatForm(request.form)
    if request.method == 'POST' and select.validate():
        guest_dict = {}
        db = shelve.open('databases/guest_storage.db', 'c')

        try:
            guest_dict = db['Seats']
        except:
            print('Error in retrieving Seats from guest_storage.db')

        seat = Seat(select.name.data, select.seat.data)
        guest_dict[seat.get_user_id()] = seat
        db['Seats'] = guest_dict

        db.close()

        return redirect(url_for('home'))
    return render_template('temporary.html', form=select) #error: had to change form=SeatForm to select instead
                                                          #need to pop out a confirmation screen+shelve

@app.route('/retrieveSeats')
def retrieve_seats():
    guest_dict = {}
    db = shelve.open('databases/guest_storage.db', 'r')
    guest_dict = db['Seats']
    db.close()

    guest_list = []
    for key in guest_dict:
        seat = guest_dict.get(key)
        guest_list.append(seat)

    return render_template('retrieveSeats.html', count=len(guest_list), guest_list=guest_list)


@app.route("/updateSeats/<int:id>/", methods=['GET', 'POST'])
def update_seats(id):
    update_seats = SeatForm(request.form)
    if request.method == 'POST' and update_seats.validate():
        guest_dict = {}
        db = shelve.open('databases/guest_storage.db', 'w')
        guest_dict = db['Seats']

        seat = guest_dict.get(id)
        seat.set_name(update_seats.name.data)
        seat.set_seat(update_seats.seat.data)

        db['Seats'] = guest_dict
        db.close()

        return redirect(url_for('retrieve_seats'))
    else:
        guest_dict = {}
        db = shelve.open('databases/guest_storage.db', 'r')
        guest_dict = db['Seats']
        db.close()

        seat = guest_dict.get(id)
        update_seats.name.data = seat.get_name()
        update_seats.seat.data = seat.get_seat()

        return render_template("updateSeats.html", form = update_seats)

@app.route('/deleteSeats/<int:id>', methods=['POST'])
def delete_seats(id):
    guest_dict = {}
    db = shelve.open('databases/guest_storage.db', 'w')
    guest_dict = db['Seats']

    guest_dict.pop(id)

    db['Seats'] = guest_dict
    db.close()

    return redirect(url_for('retrieve_seats'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('loggedin') == True:
        return redirect(url_for('home'))
    else:
        form = LoginForm(request.form)
        if request.method == 'POST' and form.validate():
            print("posting")
            db = shelve.open('databases/user.db', 'r')
            username = request.form['username'].lower()
            pw = request.form['password']
            #for loop to check every users in db whether they have the same username and password
            for user in db:
                user = db[user]
                if user.get_username() == username and pbkdf2_sha256.verify(pw, user.get_user_pw()) == True:
                    session['user_id'] = user.get_user_id()
                    session['name'] = user.get_user_fullname()
                    # session['profile_pic'] = user.get_user_profile_pic()
                    session['loggedin'] = True
                    db.close()
                    # #making session['verifying'] by checking if user is inside pendingstaff.db
                    # db = shelve.open('databases/pendingstaff.db')
                    # if session['user_id'] in db:
                    #     session['verifying'] = True
                    # db.close()
                    #checking is user is staff, if so redirect them to the staff interface
                    # staffdb = shelve.open('databases/staff.db','r')
                    # if session['user_id'] in tutordb:
                    #     session['isstaff'] = True
                    # staffdb.close()
                    # try:
                    #     if request.form['remember']:
                    #         session['remember'] = True
                    # except:
                    #     pass
                    #this means that the for loop found a match, and our session data is now in used.
                    return redirect(url_for('home'))
                print("checking")
            #for loops ends and has no match...
            db.close()
            error = 'Invalid Credentials. Please try again.'
            return render_template('login.html', form=form, error=error)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def createUser():
    if session.get('loggedin') == True:
        return redirect(url_for("home"))
    else:
        createUserForm = CreateUserForm(request.form)
        if request.method == 'POST' and createUserForm.validate():
            print("posting")
            email = request.form['email'].lower()
            username = request.form['username'].lower()
            password = request.form['password']
            firstname= request.form['first_name']
            lastname= request.form['last_name']

            #Validating form(if similar)
            if username == password:
                similarerror = 'Username and password cannot be the same'
                return render_template('register.html', form=createUserForm, similarerror=similarerror)

            #retrieving user.db
            db = shelve.open('databases/user.db', 'w')
            if len(db) == 0:
                user = User(email, username, password, firstname, lastname)  # user object
                db[user.get_user_id()] = user
                # testing code
                print("successfully posted")
                db.close()
                return redirect(url_for("home"))
            else:
                for user in db:
                    user = db[user]
                    if user.get_user_email() == email:
                        emailerror = 'This email is in use, please enter another email.'
                        return render_template('register.html', form=createUserForm, emailerror=emailerror)
                    if user.get_username() == username:
                        usernameerror = 'This username is in use, please enter another username.'
                        return render_template('register.html', form=createUserForm, usernameerror=usernameerror)
                    else:
                        db.close()

                        #posting to user.db after no errors
                        db = shelve.open('databases/user.db')
                        user = User(email,username,password,firstname,lastname) #user object
                        db[user.get_user_id()] = user

                        #testing code
                        print("successfully posted")
                        db.close()
                        return redirect(url_for("home"))

    return render_template('register.html', form=createUserForm)

@app.route('/logout')
def logout():
    if session.get('loggedin')==True:
        session.clear()
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
