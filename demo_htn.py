from htn_utils import Task, Method, Plan

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
        if task.name == "Search and Rescue":
            return [Method("Mission Method 1", [Task("Search for Survivors", 4, resources=2),
                                                Task("Deliver Supplies", 2),
                                                Task("Report Back", 1),
                                                Task("Secure Area", 2)]),
                    Method("Mission Method 2", [Task("Search for Survivors Quickly", 1, resources=3),
                                                Task("Deliver Supplies", 2),
                                                Task("Report Back", 1),
                                                Task("Secure Area Quickly", 1, resources=2)])]
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
            return [Method("Quick Secure Method", [Task("Quick Patrol Area", 1, resources=2)])]
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
        ## Base check if there are no more tasks left to process
        if not self.tasks:
            plans.append(Plan(current_plan.copy()))
            self.total_duration = sum(task.duration for task in self.tasks)
            return
        ## Process current task and deecompose the method to get list of possible methods to achieve this task
        current_task = self.tasks.pop(0)
        methods = self.decompose(current_task)
        ## Handle Tasks with no methods
        if not methods:
            current_plan.append(current_task)  ## add current task to plan
            self.generate_plans(current_plan, plans)  ## call self method to process next task
            current_plan.pop()  ## task is removed from 'current_plan' to allow for exploring other branches
        else:
            for method in methods:
                self.tasks = method.sub_tasks + self.tasks  ## subtasks are added to front of list of self.tasks
                self.generate_plans(current_plan, plans)  ## recursive call with new set of self.tasks
                self.tasks = self.tasks[len(method.sub_tasks):]  ## remove subtasks added from 2 lines above to restore original state
        self.tasks.insert(0, current_task)

    def select_best_plan(self, plans):
        ## Minimize total duration and total resource usage
        best_plan = min(plans, key=lambda plan: (plan.total_duration, plan.total_resources))
        return best_plan

# Define the root tasks with overall time limits and resource constraints
root_tasks = [Task("Search and Rescue", 10)]

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

print("\nReadable Plan:")
print([task.name for task in best_plan.tasks])