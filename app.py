from flask import Flask, request, render_template
from flask import redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey
from pynput.mouse import Listener

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def start_survey():
    """Shows user a page with a button to begin the survey"""
    return render_template('start.html', survey = survey)


@app.route('/begin', methods=['POST'])
def get_first_question():
    """Clears the session of responses"""
    session['User_Answers'] = []
    return redirect('/questions/0')


@app.route('/questions/<int:question_num>')
def get_questions(question_num):
    """Displays question. Logic ensures user answers each question in order"""
    List_of_Answers = session.get('User_Answers')

    if question_num > len(survey.questions):
        flash (f"Question {question_num + 1} is out of the range of survey questions. You are on question #{len(List_of_Answers) + 1}")
        return redirect(f"/questions/{len(List_of_Answers )}")

    if question_num != len(List_of_Answers) and len(List_of_Answers ) < len(survey.questions):
        flash (f"Please answer each question in the correct order. You are on question #{len(List_of_Answers ) + 1}.")
        return redirect(f"/questions/{len(List_of_Answers )}")

    if len(List_of_Answers ) >= len(survey.questions):
        flash (f'Click the "Start Survey" button below to take the survey.')
        return redirect ('/')
    
    questions = survey.questions[question_num]

    if question_num == len(List_of_Answers):
        return render_template('questions.html', survey = survey, questions = questions, question_num = question_num)

        
@app.route('/answer', methods=['POST'])
def post_answer():
    """Appends answer to sesssion responses"""
    
    list_of_answers = session['User_Answers']
    form_items = request.form

    list_of_answers.append(form_items)
    session['User_Answers'] = list_of_answers

    form_keys = request.form.keys()

    for key in form_keys:
        num = int(key) + 1
    
    if num < len(survey.questions):
        return redirect(f'/questions/{num}')

    else:
        return redirect('/thank-you')

@app.route('/thank-you')
def thank_user():
    """thanks the user for completing the survey"""
    return render_template('thank_you.html')
