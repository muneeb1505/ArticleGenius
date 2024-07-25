from flask import Flask, render_template, request, flash, redirect, url_for
from dotenv import load_dotenv
import os
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

prompt_template = """You are an expert article writer. Write an informative and engaging article about the following topic:
Topic: {topic}
The article should be structured with an introduction, several body paragraphs, and a conclusion. Aim for around 800 words and increase the all main headings like introduction,font size larger without any stars or any other symbols."""

def generate_article(topic):
    prompt = prompt_template.format(topic=topic)
    response = model.generate_content(prompt)
    return response.text

@app.route('/', methods=['GET', 'POST'])
def index():
    article = None
    error = None

    if request.method == 'POST':
        topic = request.form['topic']
        try:
            article_text = generate_article(topic)
            article = article_text.split('\n')
        except Exception as e:
            error = str(e)

    return render_template('article.html', article=article, error=error)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Handle form submission (e.g., save to database, send email)
        flash('Thank you for your message! We will get back to you shortly.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/services')
def services():
    return render_template('services.html')

if __name__ == '__main__':
    app.run(debug=True)
