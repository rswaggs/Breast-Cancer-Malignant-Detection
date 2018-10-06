from flask import Flask
app = Flask(__name__)

# comment to test git 
# test 2

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/page2')
def new_temp():
    return 'WTF'