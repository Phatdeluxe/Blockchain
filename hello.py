from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, world!"

@app.route("/newpage")
def newpage():
    return "This is a new page"

if __name__ == "__main__":
    app.run()