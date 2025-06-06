
from flask import Flask, render_template, request
import requests
import re

app = Flask(__name__)

def extract_token(cookie_str):
    cookies = {}
    for c in cookie_str.split(';'):
        try:
            name, value = c.strip().split('=', 1)
            cookies[name] = value
        except:
            pass

    try:
        res = requests.get("https://www.facebook.com/adsmanager", cookies=cookies)
        token_match = re.search(r'EAA\w+', res.text)
        if token_match:
            return token_match.group(0)
        else:
            return "Token not found. Make sure your cookie is valid and fresh."
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    token = None
    if request.method == 'POST':
        cookie_input = request.form['cookie']
        token = extract_token(cookie_input)
    return render_template('index.html', token=token)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
