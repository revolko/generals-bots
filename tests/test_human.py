import numpy as np
import time
from generals.env import generals_v0
import generals.utils

class GameConfig():
    test = 4

testik = GameConfig(test=5)
print(testik.test)
# by hand
map_string = \
"""
...#
#..A
2..#
.#.B
"""
map = generals.utils.map_from_string(map_string)

# from file
# map = generals.utils.load_map("test_map")

# generate
map = generals.utils.map_from_generator(
    grid_size=16,
    mountain_density=0.2,
    town_density=0.05,
    general_positions=None,
)

env = generals_v0(map)
o, i, = env.reset(seed=42, options={"replay": "test"})

agent_names = ['red', 'blue']
tick = 0

while env.agents:
    if not env.renderer.paused and tick % env.renderer.game_speed == 0:
        # think whether I should reset 'tick' or not
        actions = {}
        for agent in env.agents:
            mask = o[agent]['action_mask']
            valid_actions = np.argwhere(mask == 1)
            action = np.random.choice(len(valid_actions))
            actions[agent] = valid_actions[action]
        o, r, te, tr, i = env.step(actions)
    env.render()
    time.sleep(0.064)
    tick += 1
env.close()

