from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    name = "Python Flask framework"
    task = f"Create a web application using {name}"
    return render_template('index.html',nm=name,task=task)

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/design_basics')
def design_basics():
    return render_template('html_css.html')

@app.route('/form1',methods=['GET','POST'])
def form1_handler():
    return render_template('form_1.html')

@app.route('/form1_ajax',methods=['POST'])
def form1_ajax_handler():
    name = request.form.get('fullname')
    email = request.form.get('email')
    college = request.form.get('college')
    password = request.form.get('password')
    cpassword = request.form.get('cpassword')
    return jsonify({'status':'success'})

@app.route('/form2', methods=['GET','POST'])
def form2_handler():
    if request.method == "POST":
        print(request.form.keys())
        name = request.form.get('name')
        city = request.form.get('city')
        print("We got", name, city)
    return render_template('form_2.html')

if __name__ == "__main__":
    app.run(debug=True)