import unittest

from planner.task_interpreter import *

class InterpreterTests(unittest.TestCase):
    """
    Test cases for the task_interpreter module.
    """

    def setUp(self):
        """
        Create basic Task string variables for testing.
        """
        self.input_task1 = "TASK Project 1 DUE 26 07 2025 DESC NONE PARTS 4"
        self.input_task2 = "TASK NONE DUE 20 07 2025 DESC Hello PARTS 1"
        self.input_task3 = "TASK Meeting DUE 23 07 2025 DESC Multiple Words PARTS 1"
        self.output_task1 = "TASK Project 1 DUE 26 07 2025 DESC NONE PARTS 1 4"
        self.output_task2 = "TASK NONE DUE 20 07 2025 DESC Hello PARTS 1 1"
        self.output_task3 = "TASK Meeting DUE 23 07 2025 DESC Multiple Words PARTS 1 1"
        self.all_input_tasks = self.input_task1 + ' ' + self.input_task2 + ' ' + self.input_task3
        self.all_output_tasks = self.output_task1 + ' ' + self.output_task2 + ' ' + self.output_task3


    def test_params_to_input_task(self):
        """
        Testing if manually inserting all the parameters of an InputTask result in a correct InputTask object.
        """
        test1 = params_to_input_task("Project 1", "26", "07", "2025", "NONE", "4")
        test2 = params_to_input_task("NONE", "20", "07", "2025", "Hello", "1")
        test3 = params_to_input_task("Meeting", "23", "07", "2025", "Multiple Words", "1")
        self.assertEqual(str(test1), self.input_task1)
        self.assertEqual(str(test2), self.input_task2)
        self.assertEqual(str(test3), self.input_task3)

    def test_input_tasks_to_lines(self):
        """
        Testing if a list of Tasks are accurately converted into multiple InputTask lines.
        """
        test1 = params_to_input_task("Project 1", "26", "07", "2025", "NONE", "4")
        test2 = params_to_input_task("NONE", "20", "07", "2025", "Hello", "1")
        test3 = params_to_input_task("Meeting", "23", "07", "2025", "Multiple Words", "1")
        test_concat = input_tasks_to_lines([test1, test2, test3])
        self.assertEqual(self.all_input_tasks, test_concat)


    def test_params_to_output_task(self):
        """
        Testing if manually inserting all the parameters of an OutputTask result in a correct OutputTask object.
        """
        test1 = params_to_output_task("Project 1", "26", "07", "2025", "NONE", "1", "4")
        test2 = params_to_output_task("NONE", "20", "07", "2025", "Hello", "1", "1")
        test3 = params_to_output_task("Meeting", "23", "07", "2025", "Multiple Words", "1", "1")
        self.assertEqual(str(test1), self.output_task1)
        self.assertEqual(str(test2), self.output_task2)
        self.assertEqual(str(test3), self.output_task3)

    def test_line_to_output_task(self):
        """
        Testing if an OutputTask line is accurately converted into a correct OutputTask object.
        """
        test1 = line_to_output_task(self.output_task1)
        self.assertEqual(str(test1), self.output_task1)

        test2 = line_to_output_task(self.output_task2)
        self.assertEqual(str(test2), self.output_task2)

        test3 = line_to_output_task(self.output_task3)
        self.assertEqual(str(test3), self.output_task3)

    def test_lines_to_task(self):
        """
        Testing if multiple OutputTask lines are accurately converted into a list of OutputTask objects.
        """
        test_list = lines_to_output_tasks(self.all_output_tasks)
        print('output task list', test_list)
        self.assertEqual(str(test_list[0]), self.output_task1)
        self.assertEqual(str(test_list[1]), self.output_task2)
        self.assertEqual(str(test_list[2]), self.output_task3)



if __name__ == "__main__":
    unittest.main()
