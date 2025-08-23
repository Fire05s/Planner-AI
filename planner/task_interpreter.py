"""
Module to convert parameters and strings to Task objects for further use.
"""



from planner.task import *


class CreateTaskException(Exception):
    """
    Exceptions for creating a Task.
    """
    pass

class TasktoLineException(Exception):
    """
    Exceptions for converting a Task to a Line.
    """
    pass

class TaskInterpreterException(Exception):
    """
    Exceptions when interpreting a Task.
    """
    pass



def params_to_input_task(name: str, day: str, month: str, year: str, desc: str, parts: str) -> InputTask:
    """
    Given a Task's name, due date (day, month, and year), description, and parts, create an InputTask object.

    Can be used for taking user inputs from the Planner and creating InputTask objects to send to the AI.
    """
    # Error handling
    nameExc = not isinstance(name, str)
    dayExc = False
    monthExc = False
    yearExc = False
    try:
        day = int(day)
    except ValueError:
        dayExc = True
    try:
        month = int(month)
    except ValueError:
        monthExc = True
    try:
        year = int(year)
    except ValueError:
        yearExc = True
    descExc = not isinstance(desc, str)
    partsExc = False
    try:
        parts = int(parts)
    except ValueError:
        partsExc = True
    errorMsg = ""

    if nameExc:
        errorMsg += "Name is not a string; "
    if dayExc:
        errorMsg += "Day is not an integer; "
    if monthExc:
        errorMsg += "Month is not an integer; "
    if yearExc:
        errorMsg += "Year is not an integer; "
    if descExc:
        errorMsg += "Description is not a string; "
    if partsExc:
        errorMsg += "Parts is not an integer; "

    if errorMsg != "":
        raise CreateTaskException("Error when creating Task: " + errorMsg[:-2])

    return InputTask(name, day, month, year, desc, parts)


def input_tasks_to_lines(task_list: list[InputTask]) -> str:
    """
    Given a list of InputTasks, create one string containing multiple "lines" of InputTasks.

    Used for sending one or multiple InputTask objects to the AI in InputTask string format.
    """
    if not isinstance(task_list, list):
        raise TasktoLineException("Input Task list is not a list.")

    result = ""
    for task in task_list:
        if not isinstance(task, Task):
            raise TasktoLineException("Object in list is not a Task.")
        elif result == "":
            result = str(task)
        else:
            result += ' ' + str(task)
    return result



def params_to_output_task(name: str, day: str, month: str, year: str, desc: str, part_num: str, total_parts: str) -> OutputTask:
    """
    Given a Task's name, assigned date (day, month, and year), description, and parts, create an OutputTask object.

    Can be used for taking output parameters from the AI and creating processable OutputTask objects.
    """
    # Error handling
    nameExc = not isinstance(name, str)
    dayExc = False
    monthExc = False
    yearExc = False
    try:
        day = int(day)
    except ValueError:
        dayExc = True
    try:
        month = int(month)
    except ValueError:
        monthExc = True
    try:
        year = int(year)
    except ValueError:
        yearExc = True
    descExc = not isinstance(desc, str)
    partNumExc = False
    try:
        part_num = int(part_num)
    except ValueError:
        partNumExc = True
    totalPartsExc = False
    try:
        total_parts = int(total_parts)
    except ValueError:
        totalPartsExc = True
    errorMsg = ""

    if nameExc:
        errorMsg += "Name is not a string; "
    if dayExc:
        errorMsg += "Day is not an integer; "
    if monthExc:
        errorMsg += "Month is not an integer; "
    if yearExc:
        errorMsg += "Year is not an integer; "
    if descExc:
        errorMsg += "Description is not a string; "
    if partNumExc:
        errorMsg += "Part Number is not an integer; "
    if totalPartsExc:
        errorMsg += "Total Number of Parts is not an integer; "

    if errorMsg != "":
        raise CreateTaskException("Error when creating Task: " + errorMsg[:-2])

    return OutputTask(name, day, month, year, desc, part_num, total_parts)


def line_to_output_task(line: str) -> OutputTask:
    """
    Given a single line for a Task, create an OutputTask object.

    Used for breaking down individual lines from an OutputTask string output and converting them into an OutputTask object.
    """
    if not isinstance(line, str):
        raise TaskInterpreterException("Input line is not a string.")
    elif not line:
        raise TaskInterpreterException("Empty line given.")

    line_list = line.split()
    active_state = "NONE"
    data = {"NAME": "", "DAY": "", "MONTH": "", "YEAR": "", "DESC": "", "PART_NUM": "", "TOTAL_PARTS": ""}

    if "TASK" not in line_list or "DUE" not in line_list or "DESC" not in line_list or "PARTS" not in line_list:
        raise TaskInterpreterException("All required parameters not given to create an OutputTask.")

    for word in line_list:
        if word == "TASK" or word == "DUE" or word == "DESC" or word == "PARTS":
            # Found keyword -> change processed parameter
            active_state = word
        else:
            if active_state == "TASK":
                if data["NAME"] == "":
                    data["NAME"] = word
                else:
                    data["NAME"] += ' ' + word
            elif active_state == "DUE":
                if data["DAY"] == "":
                    data["DAY"] = word
                elif data["MONTH"] == "":
                    data["MONTH"] = word
                elif data["YEAR"] == "":
                    data["YEAR"] = word
                else:
                    raise TaskInterpreterException("More values given to Due Date than expected.")
            elif active_state == "DESC":
                if data["DESC"] == "":
                    data["DESC"] = word
                else:
                    data["DESC"] += ' ' + word
            elif active_state == "PARTS":
                if data["PART_NUM"] == "":
                    data["PART_NUM"] = word
                elif data["TOTAL_PARTS"] == "":
                    data["TOTAL_PARTS"] = word
                else:
                    raise TaskInterpreterException("More values given to Parts than expected.")
    
    return params_to_output_task(data["NAME"], data["DAY"], data["MONTH"], data["YEAR"], data["DESC"], data["PART_NUM"], data["TOTAL_PARTS"])


def lines_to_output_tasks(lines: str) -> list[OutputTask]:
    """
    Given multiple lines of OutputTasks, create a list of OutputTask objects.

    Used for taking a complete OutputTask string input and converting them into a list of OutputTask objects.
    """
    if not isinstance(lines, str):
        raise CreateTaskException("Lines of OutputTasks input are not in a string.")

    lines_list = lines.split()
    line = ""
    output_tasks = []
    for word in lines_list:
        if word == "TASK":
            # Add the new OutputTask if a line has been compiled
            if line != "":
                output_tasks.append(line_to_output_task(line))
            # Reset the extracted line
            line = "TASK"
        else:
            line += ' ' + word
    
    if line != "":
        output_tasks.append(line_to_output_task(line))

    return output_tasks

__all__ = [params_to_input_task.__name__, input_tasks_to_lines.__name__, params_to_output_task.__name__, line_to_output_task.__name__, 
        lines_to_output_tasks.__name__, CreateTaskException.__name__, TasktoLineException.__name__, TaskInterpreterException.__name__]