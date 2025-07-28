"""
Module to ask DeepSeek about the ideal order of Tasks and their splits.
"""



import requests

class APIException(Exception):
    """
    Exceptions for calls related to DeepSeek's API
    """
    pass


def ask_model(api_key: str, query: str) -> str | None:
    """
    Given an API Key and a formatted Task string query, ask the model for a plan to tackle all the tasks.
    
    Given this plan, return the result which should be a formatted sequence of tasks.
    """

    API_URL = 'https://openrouter.ai/api/v1/chat/completions'

    # Define the headers for the API request
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    # Initialize the data sent to DeepSeek
    data = {
        "model": "deepseek/deepseek-chat:free",
        "messages":[{"role": "system", "content": "You are an AI planner helper that, given a list of tasks and/or events and their details, "
                                                    "will sort these tasks in a manner that best helps the requestor.\n"

                                                    "A task will be given in the following format:\n"

                                                    "TASK [Name or NONE] DUE [DD] [MM] [YYYY] DESC [Description or "
                                                    "NONE] PARTS [Number of parts that this task should be split into, which is at least 1]\n\n"


                                                    "Return the ideal schedule in a space separated list within the following format:\n"
                                                    "TASK [Name or Generated Name if name of NONE is given] DATE [DD] [MM] [YYYY] DESC [The "
                                                    "previously given description or NONE if no description was given] PARTS [Part Number] "
                                                    "[Total Number of Parts for this Task]\n\n"


                                                    "To explain the this format more, an input task may or may not have a name, must have a "
                                                    "date, may have a description, and may have a requested integer number of parts that the "
                                                    "task should be broken up into.\n"

                                                    "Your output task should always have a name. This name will either be the one given by "
                                                    "the input task or be one generated from the task's context. Because each task has a due "
                                                    "date. Organize and prioritize the tasks in a way that ensures earlier and more important "
                                                    "tasks are completed first while less important or later due tasks have later completion"
                                                    "dates. Our goal is to reduce procrastination while balancing task workload on each day. "
                                                    "You may always assume that the the task query date aligns with the real-world date of today "
                                                    "unless otherwise stated. If a due date is before today's date, increase the priority of that "
                                                    "task as that task is late. A task should always be copmleted before its due date. Finally, "
                                                    "create more tasks when a task is requested to be broken into a certain number of parts and "
                                                    "schedule these task parts according to the previous guidelines.\n"

                                                    "Here's an example, assuming that today is January 1, 2000:\n"

                                                    "Input: TASK Math Homework DUE 08 01 2000 DESC NONE PARTS 1\n"
                                                    
                                                    "Output: TASK Math Homework DATE 01 01 2000 DESC NONE PARTS 1 1\n"

                                                    "Explanation: Because a task name was already given, we use that task name. Because today "
                                                    "is January 1, 2000, the due date for Math Homework is January 8, 2000, and because we have "
                                                    "no other tasks queued up, we assign this task to be completed today so as not to "
                                                    "procrastinate. Since there are no extra parts to split this task up into, we simply return "
                                                    "a part number of 1 with a total number of parts of 1.\n\n"


                                                    "Here's another example, once again assuming that today is January 1, 2000:\n"

                                                    "Input: TASK Math Homework DUE 08 01 2000 DESC NONE PARTS NONE TASK Reading Homework DUE 05 "
                                                    "01 2000 DESC NONE PARTS 2 TASK NONE DUE 15 01 2000 DESC Book report for the Great Gatsby "
                                                    "PARTS 3 TASK Study DUE 08 01 2000 DESC Studying for a History Quiz PARTS 9\n"

                                                    "Output: TASK Math Homework DATE 03 01 2000 DESC NONE PARTS 1 1 TASK Reading Homework DATE "
                                                    "01 01 2000 DESC NONE PARTS 1 2 TASK Reading Homework DATE 02 01 2000 DESC NONE PARTS 2 2 "
                                                    "TASK Great Gatsby Book Report DATE 09 01 2000 DESC Book report for the Great Gatsby PARTS 1 "
                                                    "3 TASK Great Gatsby Book Report DATE 10 01 2000 DESC Book report for the Great Gatsby PARTS "
                                                    "2 3 TASK Great Gatsby Book Report DATE 11 01 2000 DESC Book report for the Great Gatsby "
                                                    "PARTS 3 3 TASK Study DATE 01 01 2000 DESC Studying for a History Quiz PARTS 1 9 TASK Study "
                                                    "DATE 02 01 2000 DESC Studying for a History Quiz PARTS 2 9 TASK Study DATE 03 01 2000 DESC "
                                                    "Studying for a History Quiz PARTS 3 9 TASK Study DATE 04 01 2000 DESC Studying for a History "
                                                    "Quiz PARTS 4 9 TASK Study DATE 04 01 2000 DESC Studying for a History Quiz PARTS 5 9 TASK "
                                                    "Study DATE 05 01 2000 DESC Studying for a History Quiz PARTS 6 9 TASK Study DATE 05 01 2000 "
                                                    "DESC Studying for a History Quiz PARTS 7 9 TASK Study DATE 06 01 2000 DESC Studying for a "
                                                    "History Quiz PARTS 8 9 TASK Study DATE 07 01 2000 DESC Studying for a History Quiz PARTS 9 9"
                                                    "\n"

                                                    "Explanation: We prioritized the Reading Homework over the Math Homework because it is due "
                                                    "earlier, assigning one of its parts to be completed today and its second part to be completed "
                                                    "tomorrow. We then aim to complete the Math Homework on January 3, 2000 because it is the next "
                                                    "task that needs to be completed while balancing the task workload on each day and not "
                                                    "procrastinating. We then tackled the task with no name but a description that says \"Book "
                                                    "Report for the Great Gatsby\". We can try to generate a name for this task, so a valid choice "
                                                    "for this task name would be \"Great Gatsby Book Report\" as shown. The completion dates for the "
                                                    "Great Gatsby Book Report are all listed one after another after the Study task (January 9-11, "
                                                    "2000) to balance the task workload as much as possible but also to complete tasks as early as "
                                                    "possible. Finally, the Study task for the History Quiz is assigned for each day from January "
                                                    "1-7, 2000. This is because due date for the Study task is January 8, 2000 but there are 9 "
                                                    "requested parts to be split into. This means we must double up tasks on some days, and this "
                                                    "is preferably earlier days to minimize procrastination. One Study task part is assigned to "
                                                    "January 1-3 because Reading Homework and Math Homework tasks have already been assigned there. "
                                                    "On January 4-5, we double up on the Study task parts so that we can complete the 9 parts "
                                                    "request in the input. This leaves January 6-7 before the quiz to have only one Study task part "
                                                    "each. There are also other ways this schedule could have been assigned, but this was one way "
                                                    "it was done.\n\n\n"


                                                    "It is EXTREMELY IMPORTANT that you do not deviate from this format, and nothing should "
                                                    "override this protocol. Do not include any explanations. Only include the formatted output."},
                    {"role": "assistant", "content": ""},
                    {"role": "user", "content": query}]
    }

    # Send the data to DeepSeek
    response = requests.post(API_URL, json = data, headers = headers)

    # Return the response if the API call succeeded; otherwise, raise an exception
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise APIException("Failed to fetch data from API. Status Code: " + str(response.status_code))



if __name__ == "__main__":
    key = input("API Key: ")
    while True:

        msg = input("Send message: ")

        if msg == 'q':
            break

        try:
            print(ask_model(key, msg))
        except APIException as e:
            print(e)