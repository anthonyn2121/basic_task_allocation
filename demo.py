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

class HTNPlanner:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def decompose(self, task):
        methods = self.get_methods_for_task(task)
        feasible_methods = []
        for method in methods:
            if self.is_feasible(method, task):
                feasible_methods.append(method)
        return feasible_methods

    def get_methods_for_task(self, task):
        if task.name == "Complete Mission":
            return [Method("Mission Method 1", [Task("Search for Survivors", 4, resources=2),
                                                Task("Deliver Supplies", 2),
                                                Task("Report Back", 1),
                                                Task("Secure Area", 1)]),
                    Method("Mission Method 2", [Task("Search for Survivors Quickly", 3, resources=3),
                                                Task("Deliver Supplies", 2),
                                                Task("Report Back", 1),
                                                Task("Secure Area Quickly", 2, resources=2)])]
        elif task.name == "Search for Survivors":
            return [Method("Search Method", [Task("Search Area A", 2),
                                             Task("Search Area B", 2)])]
        elif task.name == "Search for Survivors Quickly":
            return [Method("Quick Search Method", [Task("Quick Search Area A", 1.5),
                                                   Task("Quick Search Area B", 1.5)])]
        elif task.name == "Deliver Supplies":
            return [Method("Supply Method", [Task("Navigate to Location", 1),
                                             Task("Drop Supplies", 1)])]
        elif task.name == "Report Back":
            return [Method("Report Method", [Task("Compile Report", 0.5),
                                             Task("Transmit Data", 0.5)])]
        elif task.name == "Secure Area":
            return [Method("Secure Method", [Task("Patrol Area", 1)])]
        elif task.name == "Secure Area Quickly":
            return [Method("Quick Secure Method", [Task("Quick Patrol Area", 2, resources=2)])]
        return []

    def is_feasible(self, method, parent_task):
        total_duration = sum(task.duration for task in method.sub_tasks)
        if total_duration > parent_task.duration:
            return False
        return True

    def plan(self, root_tasks):
        for task in root_tasks:
            self.add_task(task)
        plans = []
        self.generate_plans([], plans)
        return plans

    def generate_plans(self, current_plan, plans):
        if not self.tasks:
            plans.append(Plan(current_plan.copy()))
            return
        current_task = self.tasks.pop(0)
        methods = self.decompose(current_task)
        if not methods:
            current_plan.append(current_task)
            self.generate_plans(current_plan, plans)
            current_plan.pop()
        else:
            for method in methods:
                self.tasks = method.sub_tasks + self.tasks
                self.generate_plans(current_plan, plans)
                self.tasks = self.tasks[len(method.sub_tasks):]
        self.tasks.insert(0, current_task)

    def select_best_plan(self, plans):
        # Criteria: Minimize total duration and total resource usage
        best_plan = min(plans, key=lambda plan: (plan.total_duration, plan.total_resources))
        return best_plan

# Define the root tasks with overall time limits and resource constraints
root_tasks = [Task("Complete Mission", 8)]

# Create the HTN planner
planner = HTNPlanner()

# Generate multiple plans
plans = planner.plan(root_tasks)

# Output all feasible plans
print("All Feasible Plans:")
for plan in plans:
    print(plan)

# Select the best plan based on criteria
best_plan = planner.select_best_plan(plans)
print("\nBest Plan:")
print(best_plan)
