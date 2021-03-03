
import numpy as np
import pandas as pd

np.random.seed(seed=1) # set random seed
actions = ["north", "east", "west", "south", "suck"]

def simple_randomized_agent(bumpers, dirty):
    return np.random.choice(actions)

# define percepts (current location is NW corner and it is dirty)
bumpers = {"north" : True, "east" : False, "south" : False, "west" : True}
dirty = True

# call agent program function with percepts and it returns an action
simple_randomized_agent(bumpers, dirty)


def simple_environment(agent, max_steps, verbose=True):
    num_cleaned = 0

    for i in range(max_steps):
        dirty = True
        bumpers = {"north": False, "south": False, "west": False, "east": False}

        action = agent(bumpers, dirty)
        if (verbose): print("step", i, "- action:", action)

        if (action == "suck"):
            num_cleaned = num_cleaned + 1

    return num_cleaned


# Description:
#   My environment creates random dirty squares and stores them in a 2D array.
#   It also tracks where the agent is and removes dirt from 2D array when appropriate.
#   In this array, element zero represents the negative vertical axis, visually, and
#   element one represents the positive horizontal axis. This is to simplify two
#   processes: printing the array and mentally converting the visual positions
#   to coordinates.

# Code:
def my_environment(agent, n=5, max_steps=20, verbose=True):
    # Initializing the environment.
    data = {'num_cleaned': 0, 'energy_used': 0}
    pos = np.random.randint(n, size=(2))  # Agent starts in a random square.
    if (verbose): print(pos)
    dirty = np.random.choice([0, 1], p=[0.8, 0.2], size=(n, n))
    if (verbose): print(dirty)

    # Limited by battery.
    for i in range(max_steps):
        data['energy_used'] += 1

        # Update the bumper sensors.
        bumpers = {"north": False, "south": False, "west": False, "east": False}
        if (pos[0] == 0): bumpers['north'] = True
        if (pos[0] == 4): bumpers['south'] = True
        if (pos[1] == 0): bumpers['west'] = True
        if (pos[1] == 4): bumpers['east'] = True

        # Send sensor info to the agent.
        action = agent(bumpers, dirty[pos[0], pos[1]])

        # React to the agent's action.
        if (verbose): print("step", i, "- action:", action)
        if (action == "north" and pos[0] != 0):
            pos[0] -= 1  # Agent can't go through walls
        elif (action == "south" and pos[0] != 4):
            pos[0] += 1
        elif (action == "west" and pos[1] != 0):
            pos[1] -= 1
        elif (action == "east" and pos[1] != 4):
            pos[1] += 1
        elif (action == "suck" and dirty[pos[0], pos[1]]):
            # Remove dirt from 2d array, and record a cleaned square.
            dirty[pos[0], pos[1]] = 0
            data['num_cleaned'] += 1
            # If all clean, return data.
            if (data['num_cleaned'] == 25):
                break

    print(pos)
    print(dirty)
    return pd.DataFrame(data, index=[''])

# Description:
#   My simple reflex agent reacts to dirt by sucking, and it travels a random direction
#   where there is no wall in its way.

# Code:
travel = ["north", "east", "west", "south"]

def simple_reflex_agent(bumpers, dirty):
    if (dirty): return "suck"
    action = np.random.choice(travel)
    while (bumpers[action]): # Check for wall
        action = np.random.choice(travel)
    return action


class MBR_Agent:
    def __init__(self, name="A Model-Based Reflex Agent"):
        self.name = name
        self.c = 0

    def act(self, bumpers, dirty):
        # 0. if no west wall, go west
        if (self.c == 0):
            if (not bumpers["west"]): return ("west")
            self.c += 1

        # 1. if no north wall, go north
        if (self.c == 1):
            if (not bumpers["north"]): return ("north")
            self.c += 1

        while (True):
            # 2. if dirt, suck
            if (self.c == 2):
                self.c += 1
                if (dirty): return ("suck")

            # 3. if no east wall, go east
            if (self.c == 3):
                if (not bumpers["east"]):
                    self.c -= 1  # Continue suck-east loop
                    return ("east")
                self.c += 1

            # 4. go south
            if (self.c == 4):
                self.c += 1
                if (not bumpers["south"]): return ("south")

            # 5. if dirt, suck
            if (self.c == 5):
                self.c += 1
                if (dirty): return ("suck")

            # 6. if no west wall, go west
            if (self.c == 6):
                if (not bumpers["west"]):
                    self.c -= 1  # Continue suck-west loop
                    return ("west")
                self.c += 1

            # 7. go south
            if (self.c == 7):
                self.c = 2
                if (not bumpers["south"]): return ("south")

mbr_agent = MBR_Agent()
my_environment(mbr_agent.act)
