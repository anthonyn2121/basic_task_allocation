class Task:
    def __init__(self, name, duration, deadline=None, resources=1):
        self.name = name
        self.duration = duration
        self.deadline = deadline
        self.resources = resources

    def __repr__(self):
        return f"Task(name={self.name}, duration={self.duration}, deadline={self.deadline}, resources={self.resources})"

class Method:
    def __init__(self, name, sub_tasks):
        self.name = name
        self.sub_tasks = sub_tasks

    def __repr__(self):
        return f"Method(name={self.name}, sub_tasks={self.sub_tasks})"

class Plan:
    def __init__(self, tasks):
        self.tasks = tasks
        self.total_duration = sum(task.duration for task in tasks)
        self.total_resources = sum(task.resources for task in tasks)

    def __repr__(self):
        return f"Plan(total_duration={self.total_duration}, total_resources={self.total_resources}, tasks={self.tasks})"