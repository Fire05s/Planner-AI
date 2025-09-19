from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        taskName = request.form.get('addName')
        taskDate = request.form.get('addDate')
        taskDesc = request.form.get('addDesc')
        taskParts = request.form.get('addParts')

        print(taskName, taskDate, taskDesc, taskParts)
    
    return render_template('index.html')
# def index():
#     return render_template('index.html')

# @app.route('/submit_form', methods=['POST'])
# def submit_form():
#     if request.method == 'POST':
#         taskName = request.form.get('addName')
#         taskDate = request.form.get('addDate')
#         taskDesc = request.form.get('addDesc')
#         taskParts = request.form.get('addParts')

#         print(taskName, taskDate, taskDesc, taskParts)

#         return "Form submitted successfully!"

if __name__ == '__main__':
    app.run(debug=True)