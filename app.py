from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Hello from my backend!"})

@app.route("/about")
def about():
    return jsonify({
        "name": "Karthikeyan",
        "role": "MCA Student",
        "project": "Smallest Backend API"
    })
        
if (__name__)=="__main__":
    app.run(debug=True)