from flask import Flask, request, url_for, redirect, render_template

app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/')
def main():
    return 'Hello, World!'


@app.route('/homepage')
def home():
    """View foe the Home page of your website"""
    agent = request.user_agent
    return f'This is your Home page - {agent}'


@app.route('/hi/<string:name>')
def greeting(name):
    name = name.upper()
    age = request.args.get('age', 0, int)
    return render_template('hi.html', name=name, age=age)


@app.route('/admin')
def admin():
    to_url = url_for("greeting", name='administrator', age=30, _external=True)
    print(to_url)
    return redirect(to_url)


if __name__ == '__main__':
    app.run(debug=True)
