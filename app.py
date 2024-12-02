from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def main():
    return 'Hello, World!'


@app.route('/homepage')
def home():
    """View foe the Home page of your website"""
    agent = request.user_agent
    return f'This is your Home page - {agent}'


@app.route('/hi/<string:name>/<int:age>')
def gretting(name, age):
    name = name.upper()
    return f'Welcome, {name} - {age}!'


if __name__ == '__main__':
    app.run(debug=True)
