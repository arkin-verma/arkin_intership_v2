from flask import Flask, request, render_template

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

if __name__ == "__main__":
    app.run(debug=True)