from flask import Flask, jsonify, request, render_template, session, flash, redirect, url_for
from sqlalchemy.orm import sessionmaker
from database import Base, User, ReviewData, create_engine, DATABASE_PATH

app = Flask(__name__)
app.secret_key = '3021alkfjf123=9saasd'

def connect_db():
    engine = create_engine(DATABASE_PATH)
    DBSession = sessionmaker(bind=engine)
    return DBSession()


@app.route('/')
def index():
    name = "Python Flask framework"
    task = f"Create a web application using {name}"
    return render_template('index.html',nm=name,task=task)

@app.route('/register',methods=['GET','POST'])
def form1_handler():
    return render_template('form_1.html')


@app.route('/login')
def login_form():
    return render_template('login.html')   

@app.route('/login_api', methods=['POST']) 
def login_api():
    email = request.form.get('email')
    password = request.form.get('password')
    if len(email) == 0 or len(password) == 0:
        return jsonify({"error": "Please enter email and password"})
    elif len(email)<10 or '@' not in email:
        return jsonify({"error": "Please enter a valid email"})
    else:
        db = connect_db()
        user = db.query(User).filter_by(email=email).first()
        if user is None:
            db.close()
            return jsonify({"error": "User not found"})
        elif user.password != password:
            db.close()
            return jsonify({"error": "Incorrect password"})
        else:
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['is_logged_in'] = True
            db.close()
            return jsonify({"success": "Login successful"})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/register_api',methods=['POST'])
def form1_ajax_handler():
    name = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    cpassword = request.form.get('cpassword')
    if len(name)<3:
        return jsonify({"status":"error","message":"Username must be atleast 3 characters"})
    elif len(email)<    10 or '@' not in email:
        return jsonify({"status":"error","message":"Invalid email"})
    elif len(password)<6:
        return jsonify({"status":"error","message":"Password must be atleast 6 characters"})
    elif password != cpassword:
        return jsonify({"status":"error","message":"Passwords do not match"})
    else:
        db = connect_db()
        user = User(name=name,email=email,password=password)
        db.add(user)
        db.commit()
        db.close()
        return jsonify({"status":"success","message":"User created successfully"})



if __name__ == "__main__":
    app.run(debug=True)