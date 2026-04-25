from flask import Flask, request, render_template, send_file, session, redirect
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import letter

app = Flask(__name__)
app.secret_key = "secret123"

# Load dataset
data = pd.read_csv("dataset.csv")

X = data[["age","fever","cough","fatigue","headache","sore_throat"]]
y = data["disease"]

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)

# Store history
history = []
last_prediction = ""
last_message = ""

# LOGIN ROUTE
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "1234":
            session["user"] = "admin"
            return redirect("/")
    return render_template("login.html")

# HOME ROUTE
@app.route("/", methods=["GET","POST"])
def home():
    global last_prediction, last_message

    if "user" not in session:
        return redirect("/login")

    prediction = None
    message = ""
    confidence = 0

    if request.method == "POST":
        age = int(request.form["age"])
        fever = int(request.form["fever"])
        cough = int(request.form["cough"])
        fatigue = int(request.form["fatigue"])
        headache = int(request.form["headache"])
        sore = int(request.form["sore_throat"])

        # Prediction
        result = model.predict([[age, fever, cough, fatigue, headache, sore]])
        probs = model.predict_proba([[age, fever, cough, fatigue, headache, sore]])

        prediction = result[0]
        confidence = round(max(probs[0]) * 100, 2)

        # Messages
        if prediction == "Covid":
            message = "⚠️ High risk. Get tested immediately."
        elif prediction == "Flu":
            message = "🤒 Rest and hydration recommended."
        elif prediction == "Cold":
            message = "😷 Mild cold. Take care."
        elif prediction == "Allergy":
            message = "🌼 Allergy detected."
        else:
            message = "🧠 Possible stress or minor issue."

        last_prediction = prediction
        last_message = message

        history.append({"age": age, "prediction": prediction})

    return render_template("index.html",
                           prediction=prediction,
                           message=message,
                           confidence=confidence,
                           history=history)

# DOWNLOAD PDF
@app.route("/download")
def download():
    file_path = "report.pdf"

    doc = SimpleDocTemplate(file_path, pagesize=letter)
    content = []

    content.append(Paragraph(f"Disease Prediction: {last_prediction}"))
    content.append(Paragraph(f"Advice: {last_message}"))

    doc.build(content)

    return send_file(file_path, as_attachment=True)

# 🔥 DEPLOYMENT FIX (IMPORTANT)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
