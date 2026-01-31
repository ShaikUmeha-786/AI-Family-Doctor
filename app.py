from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from PIL import Image
import pytesseract

app = Flask(__name__)

# ================= TESSERACT PATH =================
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ================= GEMINI CONFIG =================
genai.configure(api_key="AIzaSyA3QEwogZHUG0YM3nSt-I6zM9mni9j7bYQ")

model = genai.GenerativeModel("models/gemini-flash-latest")

# ================= FAMILY DOCTOR =================
@app.route("/", methods=["GET", "POST"])
def home():
    response = ""

    if request.method == "POST":
        symptoms = request.form.get("symptoms")
        age = request.form.get("age")
        gender = request.form.get("gender")

        prompt = f"""
You are an AI Family Doctor assistant.
Educational use only. Not a licensed doctor.

Symptoms: {symptoms}
Age: {age}
Gender: {gender}

Respond ONLY in HTML.
Use <h3> headings and <ul><li> bullets.
No paragraphs. No markdown.

<h3>🩺 Possible Causes</h3>
<ul><li>Point</li></ul>

<h3>🧠 What It Means</h3>
<ul><li>Point</li></ul>

<h3>💊 Common OTC Medicines (India)</h3>
<ul><li>Medicine</li></ul>

<h3>🏠 Home Care</h3>
<ul><li>Tip</li></ul>

<h3>🚨 See a Doctor If</h3>
<ul><li>Warning</li></ul>

<h3>⚠️ Disclaimer</h3>
<ul><li>Educational only</li></ul>
"""

        try:
            result = model.generate_content(prompt)
            response = result.text
        except Exception as e:
            response = f"<p>Error: {e}</p>"

    return render_template("index.html", response=response)


# ================= CALORIES PAGE =================
@app.route("/calories")
def calories():
    return render_template("calories.html")


@app.route("/get-calories", methods=["POST"])
def get_calories():
    food = request.form.get("food")

    if not food:
        return jsonify({"error": "No food item provided"})

    prompt = f"""
Food item: {food}

Give output:
Food:
Approx Quantity:
Calories (kcal):
Benefits:
"""

    try:
        result = model.generate_content(prompt)
        return jsonify({"result": result.text})
    except Exception as e:
        return jsonify({"error": str(e)})


# ================= REPORTS INPUT PAGE =================
@app.route("/reports")
def reports():
    return render_template("reports.html")


# ================= REPORT ANALYSIS =================
@app.route("/analyze-report", methods=["POST"])
def analyze_report():
    report_text = request.form.get("report_text")
    image = request.files.get("report_image")

    # DEBUG (keep for now)
    print("FILES:", request.files)

    # If image uploaded → OCR
    if image and image.filename != "":
        print("IMAGE RECEIVED:", image.filename)
        img = Image.open(image)
        report_text = pytesseract.image_to_string(img)

    if not report_text:
        return "No report text or image provided"

    prompt = f"""
You are a medical report explanation assistant.
Educational use only.

Report text:
{report_text}

Respond ONLY in HTML.
Use <h3> and <ul><li>.
No paragraphs. No markdown.

<h3>📄 Report Summary</h3>
<ul><li>Point</li></ul>

<h3>🧠 What It Means</h3>
<ul><li>Point</li></ul>

<h3>🚨 When to See a Doctor</h3>
<ul><li>Point</li></ul>

<h3>⚠️ Disclaimer</h3>
<ul><li>Educational only</li></ul>
"""

    try:
        result = model.generate_content(prompt)
        return render_template("report_result.html", result=result.text)
    except Exception as e:
        return f"Error: {e}"


# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=10000)
