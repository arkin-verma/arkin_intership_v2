from flask import Flask, jsonify, request, render_template, session, flash, redirect, url_for
from sqlalchemy.orm import sessionmaker
from database import Base, User, ReviewData, create_engine, DATABASE_PATH
from spider import collect_reviews, get_review_link, save_reviews

app = Flask(__name__)
app.secret_key = '' # INPUT SECRET KEY HERE

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
    next =  request.args.get('next','/')
    return render_template('login.html', nextaddr=next)   

@app.route('/login_api', methods=['POST']) 
def login_api():
    email = request.form.get('email')
    password = request.form.get('password')
    if len(email) == 0 or len(password) == 0:
        return jsonify({"message": "Please enter email and password", 'status':'error'})
    elif len(email)<10 or '@' not in email:
        return jsonify({"message": "Please enter a valid email", 'status':'error'})
    else:
        db = connect_db()
        user = db.query(User).filter_by(email=email).first()
        if user is None:
            db.close()
            return jsonify({"message": "User not found", 'status':'error'})
        elif user.password != password:
            db.close()
            return jsonify({"message": "Incorrect password", 'status':'error'})
        else:
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['is_logged_in'] = True
            db.close()
            return jsonify({'status':"success", "message":"Login successful"})

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

@app.route('/startmining',methods=['GET','POST'])
def start_mining():
    if 'is_logged_in' not in session:
        flash('Please login to start mining')
        return redirect('/login?next=startmining')
    return render_template('start_mining.html')

@app.route('/scrapper_api',methods=['POST'])
def scrapper_api():
    if 'is_logged_in' not in session:
        return jsonify({"status":"error","message":"Please login to start mining"})
    else:
        url = request.form.get('product_url')
        if len(url)<10: # url validation should be fixed,not the best
            return jsonify({"status":"error","message":"Please enter a valid url"})
        else:
            # call scrapper function
            # save the result in database
            return jsonify({"status":"success","message":"Product scrapped successfully"})

if __name__ == "__main__":
    app.run(debug=True)
