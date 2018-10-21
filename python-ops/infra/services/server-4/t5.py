from flask import Flask, render_template, request, url_for
app = Flask(__name__)

a = "About us"

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/aboutus")
def about():
    return render_template('aboutus.html', a=a)

@app.route("/contactus")
def contact():
    return render_template('contactus.html')

@app.route("/contactprocess", methods=['POST'])
def contactprocess():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    return render_template('thankyou.html', firstname=firstname, lastname=lastname)


if __name__ == "__main__":
    app.run()
