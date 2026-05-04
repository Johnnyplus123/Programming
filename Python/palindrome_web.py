#!/usr/bin/env python3
from flask import Flask, render_template, request
import palindrome

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    message = None
    text = ''

    if request.method == 'POST':
        text = request.form.get('text', '').strip()
        if text:
            is_pal = palindrome.is_palindrome(text)
            result = 'correct' if is_pal else 'incorrect'
            message = f"'{text}' is {result}."

    return render_template('palindrome.html', text=text, result=result, message=message)

if __name__ == '__main__':
    app.run(debug=True)
