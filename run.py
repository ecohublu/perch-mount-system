from app import create_app
from app.model import Projects

app = create_app()


@app.route("/ping")
def ping():
    return "pong"


if __name__ == "__main__":
    app.run(debug=True)
