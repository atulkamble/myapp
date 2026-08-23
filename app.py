from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Azure Blue-Green Deployment</h1>
    <h2>Version: BLUE - V1</h2>
    <p>Application is running successfully.</p>
    """

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
