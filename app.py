from flask import Flask, render_template, request
import sqlite3
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


app = Flask(__name__)

API_KEY = "bbe31acdf79441f7f4a46750f5859dfc"

def get_latest_data():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT 1")
    data = c.fetchone()
    conn.close()
    return data

def get_last_50_data():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT 50")
    data = c.fetchall()
    conn.close()
    return data[::-1]

def get_weather_data(location):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        if data.get("main"):
            return {
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "desc": data["weather"][0]["description"]
            }
        else:
            return None
    except:
        return None
def send_email_alert(subject, body, to_email):
    sender_email = "priyadharshinirajesh7@gmail.com"
    sender_password = "vzoiyiyigyahoxpu"  # your 16-character App Password
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, message.as_string())
        server.quit()
        print("✅ Email alert sent successfully.")
    except Exception as e:
        print("❌ Failed to send email:", e)


@app.route("/", methods=["GET", "POST"])
def index():
    latest = get_latest_data()
    history = get_last_50_data()
    weather_data = None
    location = ""

    irrigation_alert = None
    if latest and latest[2] < 30:
        irrigation_alert = f"IRRIGATION NEEDED! Soil moisture is low ({latest[2]:.2f}%)"
        # Send an email alert
        send_email_alert(
            "Irrigation Alert - Smart Agriculture",
            f"Attention!\nSoil moisture is low ({latest[2]:.2f}%). Please irrigate your field.",
            "yourgmail@gmail.com"  # send to yourself
        )

    if request.method == "POST":
        location = request.form.get("location")
        weather_data = get_weather_data(location)

    return render_template("index.html", latest=latest, history=history,
                           weather_data=weather_data, location=location,
                           irrigation_alert=irrigation_alert)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


