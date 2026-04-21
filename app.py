
from openai import OpenAI

from flask import Flask,render_template,request,redirect,jsonify,send_file
import sqlite3
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
import csv
# Load environment variables from .env file
load_dotenv()

# AI setup

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import os


password = os.getenv("ADMIN_PASSWORD")
print(os.getenv("ADMIN_PASSWORD"))

# Initialize Flask app
app = Flask(__name__)
# Darabase setup
def get_db():
    conn = sqlite3.connect('chat_history.db')
    conn.row_factory=sqlite3.Row
    return conn
# Create the chat_history table if it doesn't exist
conn=get_db()
conn.execute('''CREATE TABLE IF NOT EXISTS chat_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  email TEXT,
                  rating INTEGER,
                  comment TEXT,
                  date TEXT,
                  user_message TEXT,
                  ai_response TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()
conn.close() 


API_KEY = os.getenv("GOOGLE_API_KEY")
print("API KEY:", os.getenv("GOOGLE_API_KEY"))




    

def ask_gemini(prompt):
    API_KEY = os.getenv("GOOGLE_API_KEY")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"
    headers={
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                    ]
            }
        ]
    }
    try:
       response = requests.post(url, headers=headers, json=data)
       result = response.json()

       if response.status_code != 200:
        print("API Error:", response.text)
        print("STATUS:", response.status_code)
        return "AI not available but your feedback is valuable!"

       if "candidates"  in result :
        return result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print("EXCEPTION:", e)
        return "AI not available but your feedback is valuable!"

   

    
# Routes



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])   
def submit():
    data=(
        request.form.get('name'),
        request.form.get('email'),
        request.form.get('rating'),
        request.form.get('comment'),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    )
    conn=get_db()
    conn.execute('INSERT INTO chat_history (name, email, rating, comment, date) VALUES (?, ?, ?, ?, ?)', data)
    conn.commit()
    conn.close()
    return redirect('/admin')
@app.route('/admin', methods=['GET','POST'])
def admin():
    # get shows login page, post processes login and shows admin dashboard with insights and export option
    if request.method=='GET':
        return render_template('login.html')
    # Post checks password
    if request.method=='POST':
        if request.form['password'] != os.getenv("ADMIN_PASSWORD"):
            return "Unauthorized", 401
        # Fetch all chat history for insights and export
        conn=get_db()
        rows=conn.execute('SELECT * FROM chat_history').fetchall()
        conn.close()
        # Calculate average rating and total feedback count
        ratings=[int(r['rating']) for r in rows if r['rating']]
        total=len(ratings)
        average=round(sum(ratings)/total,2) if total else 0
        # AI Insights
        
                 

        insight = "No Data"

        if ratings:
            prompt = f"""Based on the following ratings: {ratings}, provide a brief insight about customer satisfaction.
            Ratings:{ratings}
            Comments:{[r['comment'] for r in rows]}
           Give short business insights based on the ratings and comments, and suggest one improvement for the business.:
           Give output in CLEAN HTML format using:
            <ul>
            <li>points</li>
            </ul>
            Include in the insights:
           - sentiments
           - issues
           - suggestions
            """
            insight = ask_gemini(prompt)
        return render_template('admin.html', rows=rows, total=total, avg=average, ratings=ratings, insight=insight)
# Chatbot
@app.route('/chat', methods=['POST'])
def chat():
    msg = request.json.get("message")

    prompt = f"""
    You are a helpful assistant for feedback collection app.
    User: {msg}
    Reply politely and guide them.
    """

    response = ask_gemini(prompt)
    conn = get_db()
    conn.execute(
        'INSERT INTO chat_history (user_message, ai_response) VALUES (?, ?)',
        (msg, response)
    )
    conn.commit()
    conn.close()
    return jsonify({"response": response})

    
@app.route('/export')
def export():
    conn=get_db()
    rows=conn.execute('SELECT * FROM chat_history').fetchall()
    conn.close()
    file='chat_history.csv'
    with open(file,'w', newline='') as f:
        writer=csv.writer(f)
        writer.writerow(['ID','Name','Email','Rating','Comment','Date','User Message','AI Response','Timestamp'])
        for row in rows:
            writer.writerow([row['id'],row['name'],row['email'],row['rating'],row['comment'],row['date'],row['user_message'],row['ai_response'],row['timestamp']])
    return send_file(file, as_attachment=True)
@app.route('/test-ai')
def test_ai():
    import requests, os

    API_KEY = os.getenv("GOOGLE_API_KEY")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"

    data = {
        "contents": [
            {
                "parts": [{"text": "Say hello"}]
            }
        ]
    }

    r = requests.post(url, json=data)

    

    return r.text

    return ask_gemini("Say hello in one line")
@app.route('/list-models')
def list_models():
    import requests

    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
    res = requests.get(url)
    return res.text
@app.route('/test-gemini')
def test_gemini():
    
    import requests, os

    API_KEY = os.getenv("GOOGLE_API_KEY")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"

    data = {
        "contents": [
            {
                "parts": [{"text": "Say hello"}]
            }
        ]
    }

    r = requests.post(url, json=data)

    

    return r.text



if __name__ == '__main__':
    app.run(debug=True)
   
