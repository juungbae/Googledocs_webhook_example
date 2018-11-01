from flask import Flask, request, render_template

app = Flask(__name__, static_url_path='')


@app.route("/webhook", methods=['POST'])
def webhook_counter():
    pass


@app.route("/")
def current():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(port=8901, debug=True)
