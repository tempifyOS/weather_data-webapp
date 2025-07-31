from flask import Flask, render_template, jsonify, request

app = Flask(__name__, template_folder='templates',static_folder='static')


@app.route('/')
def index():
    return render_template('index.html')

# Testing edit/commit to repo


if __name__ == '__main__':
    # local dev with auto‑reload and debug info
    app.run(host='0.0.0.0', port=8080, debug=True)