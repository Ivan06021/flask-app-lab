from flask import Flask

app = Flask(__name__)


@app.route('/')
def main():
    return 'Hello, World!'


@app.route('/homepage')
def home():
    """View foe the Home page of your website"""
    return 'This is your Home page'


if __name__ == '__main__':
    app.run(debug=True)
