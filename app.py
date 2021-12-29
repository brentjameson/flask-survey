from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def start_survey():
    
    return render_template('start.html', survey = survey)

@app.route('/questions/<int:question_num>')
def get_questions(question_num):
    questions = survey.questions[question_num]

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
    return 'THANK YOU FOR COMPLETING OUR SURVEY!'
