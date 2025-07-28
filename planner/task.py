"""
Module that contains Task classes: Task parent class with InputTask and OutputTask child classes.
"""



class Task:
    """
    Parent classes for Task objects that are used by the Planner.
    """
    def __init__(self, name: str, day: int, month: int, year: int, desc: str) -> None:
        """
        Create a new Task object.
        """
        self._name = name
        self._day = day
        self._month = month
        self._year = year
        self._desc = desc

    @property
    def name(self):
        return self._name

    @property
    def day(self):
        return self._day

    @property
    def month(self):
        return self._month

    @property
    def year(self):
        return self._year

    @property
    def desc(self):
        return self._desc


class InputTask(Task):
    """
    Task child class that creates a Task object from user inputs into the Planner.
    """

    def __init__(self, name: str, day: int, month: int, year: int, desc: str, parts: int) -> None:
        """
        Create a new InputTask object.
        """
        super().__init__(name, day, month, year, desc)
        self._parts = parts

    @property
    def name(self):
        return self._name

    @property
    def day(self):
        return self._day

    @property
    def month(self):
        return self._month

    @property
    def year(self):
        return self._year

    @property
    def desc(self):
        return self._desc

    @property
    def parts(self):
        return self._parts

    def __str__(self) -> str:
        """
        Return the string expression of this Task.
        """
        return f"TASK {self._name} DUE {self._day:02d} {self._month:02d} {self._year:04d} DESC {self._desc} PARTS {self._parts}"


class OutputTask(Task):
    """
    Task child class that creates a Task object from outputs from the Planner's AI.
    """

    def __init__(self, name: str, day: int, month: int, year: int, desc: str, part_num: int, total_parts: int) -> None:
        """
        Create a new OutputTask object.
        """
        super().__init__(name, day, month, year, desc)
        self._part_num = part_num
        self._total_parts = total_parts

    @property
    def part_num(self):
        return self._part_num

    @property
    def total_parts(self):
        return self._total_parts

    def __str__(self) -> str:
        """
        Return the string expression of this Task.
        """
        return f"TASK {self._name} DUE {self._day:02d} {self._month:02d} {self._year:04d} DESC {self._desc} PARTS {self._part_num} {self._total_parts}"

__all__ = [Task.__name__, InputTask.__name__, OutputTask.__name__]
