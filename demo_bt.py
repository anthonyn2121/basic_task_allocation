import numpy as np
from bt_utils import Sequence, Selector, Action

# Define action functions for behavior trees
def search_for_survivors_quickly(agent):
    print(f"{agent.name} is searching for survivors quickly at {agent.goal}")
    return agent.execute_subtask()

def navigate_to_location(agent):
    print(f"{agent.name} is navigating to location {agent.goal}")
    direction = agent.goal - agent.pos
    step = np.sign(direction)
    agent.pos = agent.pos + step
    agent.path.append(agent.pos.copy())
    return np.array_equal(agent.pos, agent.goal)

def drop_supplies(agent):
    print(f"{agent.name} is dropping supplies at {agent.goal}")
    return agent.execute_subtask()

def compile_report(agent):
    print(f"{agent.name} is compiling report at {agent.goal}")
    return agent.execute_subtask()

def transmit_data(agent):
    print(f"{agent.name} is transmitting data at {agent.goal}")
    return agent.execute_subtask()

def quick_patrol_area(agent):
    print(f"{agent.name} is patrolling area quickly at {agent.goal}")
    return agent.execute_subtask()

def detect_threat(agent):
    print(f"{agent.name} is detecting threats")
    if agent.detect_enemy():
        agent.handle_threat()
        return True
    return False

def handle_threat(agent):
    print(f"{agent.name} is handling threat at {agent.goal}")
    return agent.execute_subtask()

# Define the agent class
class Agent:
    def __init__(self, name, start_pos):
        self.name = name
        self.pos = np.array(start_pos)
        self.path = [np.array(start_pos)]
        self.goal = None
        self.current_task = None
        self.bt = Selector([
            Sequence([
                Action("Detect Threat", detect_threat),
                Action("Handle Threat", handle_threat)
            ]),
            Sequence([
                Action("Search for Survivors Quickly", search_for_survivors_quickly),
                Action("Navigate to Location", navigate_to_location),
                Action("Drop Supplies", drop_supplies),
                Action("Compile Report", compile_report),
                Action("Transmit Data", transmit_data),
                Action("Quick Patrol Area", quick_patrol_area)
            ])
        ])

    def set_goal(self, goal):
        self.goal = np.array(goal)

    def execute_task(self):
        if self.current_task and not self.current_task.completed:
            if self.bt.run(self):
                self.current_task.completed = True
                print(f"{self.name} completed task: {self.current_task.name}")
                self.move_to_next_task()

    def execute_subtask(self):
        if self.goal is None:
            return False
        if np.array_equal(self.pos, self.goal):
            return True
        return False

    def detect_enemy(self):
        # Placeholder for enemy detection logic
        # threat detected 20% of the time for demonstration purposes
        return np.random.rand() < 0.2

    def handle_threat(self):
        # Placeholder for threat handling logic
        # print(f"{self.name} is handling a threat at {self.pos}")
        self.path.append(self.pos.copy())

    def move_to_next_task(self):
        if self.tasks:
            self.current_task = self.tasks.pop(0)
            self.set_goal(self.current_task.location)
            self.path.append(self.current_task.location)
        else:
            self.current_task = None

class Task:
    def __init__(self, name, duration, location, resources=1):
        self.name = name
        self.duration = duration
        self.location = np.array(location)
        self.resources = resources
        self.completed = False

# Initialize an agent and tasks
agent = Agent("Agent 1", [0, 0])
tasks = [
    Task("Search for Survivors Quickly", 3, [5, 5], resources=3),
    Task("Navigate to Location", 1, [8, 3]),
    Task("Drop Supplies", 1, [8, 3]),
    Task("Compile Report", 0.5, [2, 7]),
    Task("Transmit Data", 0.5, [2, 7]),
    Task("Quick Patrol Area", 2, [6, 2], resources=2)
]

# Assign tasks to the agent
agent.tasks = tasks
agent.move_to_next_task()

# Run the simulation
while agent.current_task:
    navigate_to_location(agent)
    agent.execute_task()
    agent.move_to_next_task()