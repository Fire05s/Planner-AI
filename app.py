from flask import Flask, request, render_template
from planner import params_to_input_task

app = Flask(__name__)

inputTaskList = []

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        # get all task information from one form
        taskName = request.form.get('addName')
        taskDate = request.form.get('addDate')
        taskDesc = request.form.get('addDesc')
        taskParts = request.form.get('addParts')

        print(taskName, taskDate, taskDesc, taskParts)

        # process date info
        taskYear, taskMonth, taskDay = taskDate.split('-')

        # create an InputTask from form data
        inputTask = params_to_input_task(taskName, taskDay, taskMonth, taskYear, taskDesc, taskParts)
        print(inputTask)

        # add this InputTask to the session's task list
        inputTaskList.append(inputTask)
        print(inputTaskList)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)