from chatbot import chatbot
from flask import Flask, render_template, request
import re
import bodmos_cal

app = Flask(__name__)
app.static_folder = 'static'

possible_elements_in_expression = ['+','-','/','*','(',')','.','^','0','1','2','3','4','5','6','7','8','9']
operators = ['+','-','/','*','^']

# Function for detect mathematical expression in the user message
def detect_maths_exp(s):
    for elem in s:
        if elem in operators:
            return True

# Function to extract mathematical expression from string, also handing spaces in maths expression
def extract_exp(s):
    expression_str = ''
    for elem in s:
        if elem in possible_elements_in_expression:
            expression_str += elem

    return expression_str



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    if detect_maths_exp(userText):
        maths_exp = extract_exp(userText)
        # If expression is divisible by zero
        if type(bodmos_cal.calc_input(maths_exp)) == str:
            # Return string 'Oops! Found 0 in the denominator of given mathematical expression'
            return bodmos_cal.calc_input(maths_exp)
        return 'Answer is '+ str(round(bodmos_cal.calc_input(maths_exp),2)) + ' !!'

    return str(chatbot.get_response(userText))

if __name__ == "__main__":
    app.run() 