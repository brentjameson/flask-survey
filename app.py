from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey
from pynput.mouse import Listener



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def start_survey():
    
    return render_template('start.html', survey = survey)

@app.route('/begin')
def get_first_question():
    
    return redirect('/questions/0')

@app.route('/questions/<int:question_num>')
def get_questions(question_num):

    if question_num > len(survey.questions):
        flash (f"Question {question_num + 1} is out of the range of survey questions. You are on question #{len(responses) + 1}")
        return redirect(f"/questions/{len(responses)}")

    if question_num != len(responses) and len(responses) < len(survey.questions):
        flash (f"Please answer each question in the correct order. You are on question #{len(responses) + 1}.")
        return redirect(f"/questions/{len(responses)}")

    if len(responses) >= len(survey.questions):
        flash (f"You may only take this survey once")
        return redirect ('/')
    
    questions = survey.questions[question_num]

    if question_num == len(responses):
        return render_template('questions.html', survey = survey, questions = questions, question_num = question_num)

        
@app.route('/answer', methods=['POST'])
def post_answer():
    # answer = request.form[""]
    form_items = request.form
    responses.append(form_items)

    form_keys = request.form.keys()

    for key in form_keys:
        num = int(key) + 1
    
    if num < len(survey.questions):
        return redirect(f'/questions/{num}')

    else:
        return redirect('/thank-you')

@app.route('/thank-you')
def thank_user():
    return render_template('thank_you.html')
