import numpy as np
from generals.env import generals_v0
import generals.utils

# by hand
map_string = """
0001
1003
2001
0104
"""

map = generals.utils.map_from_string(map_string)

# from file
map = generals.utils.load_map("test_map")

# generate
map = generals.utils.generate_map(
    grid_size=4,
    mountain_density=0.1,
    town_density=0.1,
    n_generals=2,
    general_positions=None,
)

env = generals_v0(map)
o, i, = env.reset(seed=42, options={"replay": "test"})

agent_names = ['red', 'blue']

while env.agents:
    actions = {}
    for agent in env.agents:
        mask = o[agent]['action_mask']
        valid_actions = np.argwhere(mask == 1)
        action = np.random.choice(len(valid_actions))
        actions[agent] = valid_actions[action]
    o, r, te, tr, i = env.step(actions)
    env.render()
env.close()

