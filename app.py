from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# 🔑 API KEY (move to .env later)
genai.configure(api_key="AIzaSyCVhS_QRJDmWrq6VkSOzhSZTqP_I6oMUN4")

# ✅ CONFIRMED WORKING MODEL
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
This is for EDUCATIONAL PURPOSES ONLY.
You are NOT a licensed medical professional.

Patient Details:
Symptoms: {symptoms}
Age: {age}
Gender: {gender}

STRICT RULES:
- Respond ONLY in HTML
- Use <h3> for headings
- Use <ul><li> for bullet points
- Use emojis in headings
- NO markdown
- NO paragraphs
- NO extra text

FORMAT EXACTLY LIKE THIS:

<h3>🩺 Possible Causes</h3>
<ul>
<li>Point</li>
<li>Point</li>
</ul>

<h3>🧠 What It Means</h3>
<ul>
<li>Point</li>
</ul>

<h3>💊 Common OTC Medicines (India)</h3>
<ul>
<li>Medicine name</li>
</ul>

<h3>🏠 Home Care</h3>
<ul>
<li>Tip</li>
</ul>

<h3>🚨 See a Doctor If</h3>
<ul>
<li>Warning</li>
</ul>

<h3>⚠️ Disclaimer</h3>
<ul>
<li>Educational use only. Not medical advice.</li>
</ul>
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
You are a nutrition assistant.

Food item: {food}

Give output in this exact format:
Food:
Approx Quantity:
Calories (kcal):
Benefits:

Keep it simple and short.
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


# ================= REPORT ANALYSIS RESULT PAGE =================
@app.route("/analyze-report", methods=["POST"])
def analyze_report():
    report_text = request.form.get("report_text")

    if not report_text:
        return "No report text provided"

    prompt = f"""
You are a medical report explanation assistant.
This is for EDUCATIONAL PURPOSES ONLY.

Given report text:
{report_text}

STRICT RULES:
- Respond ONLY in HTML
- Use <h3> for headings
- Use <ul><li> for bullet points
- Simple language
- NO paragraphs
- NO markdown

FORMAT:

<h3>📄 Report Summary</h3>
<ul>
<li>Point</li>
</ul>

<h3>🧠 What It Means</h3>
<ul>
<li>Point</li>
</ul>

<h3>🚨 When to See a Doctor</h3>
<ul>
<li>Point</li>
</ul>

<h3>⚠️ Disclaimer</h3>
<ul>
<li>Educational use only. Not medical advice.</li>
</ul>
"""

    try:
        result = model.generate_content(prompt)
        return render_template("report_result.html", result=result.text)
    except Exception as e:
        return f"Error: {e}"


# ================= RUN APP =================
if __name__ == "__main__":
    app.run(debug=True)
