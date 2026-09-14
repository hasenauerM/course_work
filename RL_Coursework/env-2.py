from enum import IntEnum
#from platform import win32_edition
from typing import Tuple, Optional, List
from gym import Env, spaces
from gym.utils import seeding
from gym.envs.registration import register


def register_env(id_="WindyGridWorld-v0", entry_point="env:WindyGridWorldEnv") -> None:
    """Register custom gym environment so that we can use `gym.make()`

    In your main file, call this function before using `gym.make()` to use the Four Rooms environment.
        register_env()
        env = gym.make('WindyGridWorld-v0')

    There are a couple of ways to create Gym environments of the different variants of Windy Grid World.
    1. Create separate classes for each env and register each env separately.
    2. Create one class that has flags for each variant and register each env separately.

        Example:
        (Original)     register(id="WindyGridWorld-v0", entry_point="env:WindyGridWorldEnv")
        (King's moves) register(id="WindyGridWorldKings-v0", entry_point="env:WindyGridWorldEnv", **kwargs)

        The kwargs will be passed to the entry_point class.

    3. Create one class that has flags for each variant and register env once. You can then call gym.make using kwargs.

        Example:
        (Original)     gym.make("WindyGridWorld-v0")
        (King's moves) gym.make("WindyGridWorld-v0", **kwargs)

        The kwargs will be passed to the __init__() function.

    Choose whichever method you like.
    """
    register(id=id_, entry_point=entry_point)


class Action(IntEnum):
    """Action"""

    LEFT = 0
    DOWN = 1
    RIGHT = 2
    UP = 3

class Action_ext(IntEnum):
    """Action"""

    LEFT = 0
    DOWN = 1
    RIGHT = 2
    UP = 3
    UP_LEFT = 4
    DOWN_LEFT = 5
    DOWN_RIGHT = 6
    UP_RIGHT = 7

def actions_to_dxdy(action: Action) -> Tuple[int, int]:
    """
    Helper function to map action to changes in x and y coordinates
    Args:
        action (Action): taken action
    Returns:
        dxdy (Tuple[int, int]): Change in x and y coordinates
    """
    mapping = {
        Action.LEFT: (-1, 0),
        Action.DOWN: (0, -1),
        Action.RIGHT: (1, 0),
        Action.UP: (0, 1),
    }
    return mapping[action]

def actionsext_to_dxdy(action: Action_ext) -> Tuple[int, int]:
    """
    Helper function to map action to changes in x and y coordinates
    Args:
        action (Action): taken action
    Returns:
        dxdy (Tuple[int, int]): Change in x and y coordinates
    """
    mapping = {
        Action_ext.LEFT: (-1, 0),
        Action_ext.DOWN: (0, -1),
        Action_ext.RIGHT: (1, 0),
        Action_ext.UP: (0, 1),
        Action_ext.UP_LEFT: (-1, 1),
        Action_ext.DOWN_LEFT: (-1, -1),
        Action_ext.DOWN_RIGHT: (1, -1),
        Action_ext.UP_RIGHT: (1, 1)
    }
    return mapping[action]


class WindyGridWorldEnv(Env):
    def __init__(self):
        """Windy grid world gym environment
        This is the template for Q4a. You can use this class or modify it to create the variants for parts c and d.
        """

        # Grid dimensions (x, y)
        self.rows = 10
        self.cols = 7

        # Wind
        # TODO define self.wind as either a dict (keys would be states) or multidimensional array (states correspond to indices)
        self.wind = [[0]*self.rows]*self.cols
        for i in range(len(self.wind)):
            for j in range(len(self.wind[i])):
                if j == 3 or j == 4 or j == 5 or j == 8:
                    self.wind[i][j] = 1
                if j == 6 or j == 7:
                    self.wind[i][j] = 2

        self.action_space = spaces.Discrete(len(Action))
        self.observation_space = spaces.Tuple(
            (spaces.Discrete(self.rows), spaces.Discrete(self.cols))
        )

        # Set start_pos and goal_pos
        self.start_pos = (0, 3)
        self.goal_pos = (7, 3)
        self.agent_pos = None

    def seed(self, seed: Optional[int] = None) -> List[int]:
        """Fix seed of environment

        In order to make the environment completely reproducible, call this function and seed the action space as well.
            env = gym.make(...)
            env.seed(seed)
            env.action_space.seed(seed)

        This function does not need to be used for this assignment, it is given only for reference.
        """

        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def reset(self):
        self.agent_pos = self.start_pos
        return self.agent_pos

    def step(self, action: Action) -> Tuple[Tuple[int, int], float, bool, dict]:
        """Take one step in the environment.

        Takes in an action and returns the (next state, reward, done, info).
        See https://github.com/openai/gym/blob/master/gym/core.py#L42-L58 foand r more info.

        Args:
            action (Action): an action provided by the agent

        Returns:
            observation (object): agent's observation after taking one step in environment (this would be the next state s')
            reward (float) : reward for this transition
            done (bool): whether the episode has ended, in which case further step() calls will return undefined results
            info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning). Not used in this assignment.
        """
         # Check if goal was reached
        #print(f"agent pos: {self.agent_pos}")
        if self.agent_pos == self.goal_pos:
            done = True
            reward = 0.0
        else:
            done = False
            reward = -1.0
            
        if not done:
            #print(f"change from action: {actions_to_dxdy(action)}")
            next_pos = tuple(map(lambda x,y: x + y, self.agent_pos, actions_to_dxdy(action)))
            #print(f"next position: {next_pos}")
        
            #add the wind change to next pos
            #print(f"wind value: {self.wind[self.agent_pos[1]][self.agent_pos[0]]}")
            wind_dy = (0,self.wind[self.agent_pos[1]][self.agent_pos[0]])
            final_pos = tuple(map(lambda x,y: x+y, next_pos, wind_dy))
            #print(f"final position: {final_pos}")
        
            #check for grid boundaries 
            if final_pos[0] < 0 or final_pos[0] >= self.rows:
                final_pos = (self.agent_pos[0], final_pos[1])
            if final_pos[1] < 0 or final_pos[1] >= self.cols:
                final_pos = (final_pos[0], self.agent_pos[1])
            
            #print(f"final agent position: {self.agent_pos}")
        
        else:
            #print("restarting episode")
            final_pos = self.start_pos
    
        self.agent_pos = final_pos
        return self.agent_pos, reward, done, {}

class WindyGridWorldKingsEnv(Env):
    def __init__(self):
        """Windy grid world gym environment
        This is the template for Q4a. You can use this class or modify it to create the variants for parts c and d.
        """

        # Grid dimensions (x, y)
        self.rows = 10
        self.cols = 7

        # Wind
        # TODO define self.wind as either a dict (keys would be states) or multidimensional array (states correspond to indices)
        self.wind = [[0]*self.rows]*self.cols
        for i in range(len(self.wind)):
            for j in range(len(self.wind[i])):
                if j == 3 or j == 4 or j == 5 or j == 8:
                    self.wind[i][j] = 1
                if j == 6 or j == 7:
                    self.wind[i][j] = 2

        self.action_space = spaces.Discrete(len(Action_ext))
        self.observation_space = spaces.Tuple(
            (spaces.Discrete(self.rows), spaces.Discrete(self.cols))
        )

        # Set start_pos and goal_pos
        self.start_pos = (0, 3)
        self.goal_pos = (7, 3)
        self.agent_pos = None

    def seed(self, seed: Optional[int] = None) -> List[int]:
        """Fix seed of environment

        In order to make the environment completely reproducible, call this function and seed the action space as well.
            env = gym.make(...)
            env.seed(seed)
            env.action_space.seed(seed)

        This function does not need to be used for this assignment, it is given only for reference.
        """

        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def reset(self):
        self.agent_pos = self.start_pos
        return self.agent_pos

    def step(self, action: Action_ext) -> Tuple[Tuple[int, int], float, bool, dict]:
        """Take one step in the environment.

        Takes in an action and returns the (next state, reward, done, info).
        See https://github.com/openai/gym/blob/master/gym/core.py#L42-L58 foand r more info.

        Args:
            action (Action): an action provided by the agent

        Returns:
            observation (object): agent's observation after taking one step in environment (this would be the next state s')
            reward (float) : reward for this transition
            done (bool): whether the episode has ended, in which case further step() calls will return undefined results
            info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning). Not used in this assignment.
        """
         # Check if goal was reached
        #print(f"agent pos: {self.agent_pos}")
        if self.agent_pos == self.goal_pos:
            done = True
            reward = 0.0
        else:
            done = False
            reward = -1.0
            
        if not done:
            #print(f"change from action: {actions_to_dxdy(action)}")
            next_pos = tuple(map(lambda x,y: x + y, self.agent_pos, actionsext_to_dxdy(action)))
            #print(f"next position: {next_pos}")
        
            #add the wind change to next pos
            #print(f"wind value: {self.wind[self.agent_pos[1]][self.agent_pos[0]]}")
            wind_dy = (0,self.wind[self.agent_pos[1]][self.agent_pos[0]])
            final_pos = tuple(map(lambda x,y: x+y, next_pos, wind_dy))
            #print(f"final position: {final_pos}")
        
            #check for grid boundaries 
            if final_pos[0] < 0 or final_pos[0] >= self.rows:
                final_pos = (self.agent_pos[0], final_pos[1])
            if final_pos[1] < 0 or final_pos[1] >= self.cols:
                final_pos = (final_pos[0], self.agent_pos[1])
            
            #print(f"final agent position: {self.agent_pos}")
        
        else:
            #print("restarting episode")
            final_pos = self.start_pos
    
        self.agent_pos = final_pos
        return self.agent_pos, reward, done, {}

    from enum import IntEnum
#from platform import win32_edition
from typing import Tuple, Optional, List
from gym import Env, spaces
from gym.utils import seeding
from gym.envs.registration import register

def register_env(id="WindyGridWorld-v0", entry_point="env:WindyGridWorldEnv") -> None:
    """Register custom gym environment so that we can use `gym.make()`

    In your main file, call this function before using `gym.make()` to use the Four Rooms environment.
        register_env()
        env = gym.make('WindyGridWorld-v0')

    There are a couple of ways to create Gym environments of the different variants of Windy Grid World.
    1. Create separate classes for each env and register each env separately.
    2. Create one class that has flags for each variant and register each env separately.

        Example:
        (Original)     register(id="WindyGridWorld-v0", entry_point="env:WindyGridWorldEnv")
        (King's moves) register(id="WindyGridWorldKings-v0", entry_point="env:WindyGridWorldEnv", **kwargs)

        The kwargs will be passed to the entry_point class.

    3. Create one class that has flags for each variant and register env once. You can then call gym.make using kwargs.

        Example:
        (Original)     gym.make("WindyGridWorld-v0")
        (King's moves) gym.make("WindyGridWorld-v0", **kwargs)

        The kwargs will be passed to the __init__() function.

    Choose whichever method you like.
    """
    register(id=id, entry_point=entry_point)

class Action_9(IntEnum):
    """Action extended"""

    LEFT = 0
    DOWN = 1
    RIGHT = 2
    UP = 3
    UP_LEFT = 4
    DOWN_LEFT = 5
    DOWN_RIGHT = 6
    UP_RIGHT = 7
    NOTHING = 8

def actions9_to_dxdy(action: Action_9) -> Tuple[int, int]:
    """
    Helper function to map action to changes in x and y coordinates
    Args:
        action (Action_ext): taken action
    Returns:
        dxdy (Tuple[int, int]): Change in x and y coordinates
    """
    mapping = {
        Action_9.LEFT: (-1, 0),
        Action_9.DOWN: (0, -1),
        Action_9.RIGHT: (1, 0),
        Action_9.UP: (0, 1),
        Action_9.UP_LEFT: (-1, 1),
        Action_9.DOWN_LEFT: (-1, -1),
        Action_9.DOWN_RIGHT: (1, -1),
        Action_9.UP_RIGHT: (1, 1),
        Action_9.NOTHING: (0, 0)
    }
    return mapping[action]

class WindyGridWorldKingsEnv9(Env):
    def __init__(self):
        """Windy grid world gym environment
        This is the template for Q4a. You can use this class or modify it to create the variants for parts c and d.
        """

        # Grid dimensions (x, y)
        self.rows = 10
        self.cols = 7

        # Wind
        # TODO define self.wind as either a dict (keys would be states) or multidimensional array (states correspond to indices)
        self.wind = [[0]*self.rows]*self.cols
        for i in range(len(self.wind)):
            for j in range(len(self.wind[i])):
                if j == 3 or j == 4 or j == 5 or j == 8:
                    self.wind[i][j] = 1
                if j == 6 or j == 7:
                    self.wind[i][j] = 2

        self.action_space = spaces.Discrete(len(Action_9))
        self.observation_space = spaces.Tuple(
            (spaces.Discrete(self.rows), spaces.Discrete(self.cols))
        )

        # Set start_pos and goal_pos
        self.start_pos = (0, 3)
        self.goal_pos = (7, 3)
        self.agent_pos = None

    def seed(self, seed: Optional[int] = None) -> List[int]:
        """Fix seed of environment

        In order to make the environment completely reproducible, call this function and seed the action space as well.
            env = gym.make(...)
            env.seed(seed)
            env.action_space.seed(seed)

        This function does not need to be used for this assignment, it is given only for reference.
        """

        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def reset(self):
        self.agent_pos = self.start_pos
        return self.agent_pos

    def step(self, action: Action_9) -> Tuple[Tuple[int, int], float, bool, dict]:
        """Take one step in the environment.

        Takes in an action and returns the (next state, reward, done, info).
        See https://github.com/openai/gym/blob/master/gym/core.py#L42-L58 foand r more info.

        Args:
            action (Action): an action provided by the agent

        Returns:
            observation (object): agent's observation after taking one step in environment (this would be the next state s')
            reward (float) : reward for this transition
            done (bool): whether the episode has ended, in which case further step() calls will return undefined results
            info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning). Not used in this assignment.
        """
         # Check if goal was reached
        #print(f"agent pos: {self.agent_pos}")
        if self.agent_pos == self.goal_pos:
            done = True
            reward = 0.0
        else:
            done = False
            reward = -1.0
            
        if not done:
            #print(f"change from action: {actions_to_dxdy(action)}")
            next_pos = tuple(map(lambda x,y: x + y, self.agent_pos, actions9_to_dxdy(action)))
            #print(f"next position: {next_pos}")
        
            #add the wind change to next pos
            #print(f"wind value: {self.wind[self.agent_pos[1]][self.agent_pos[0]]}")
            wind_dy = (0,self.wind[self.agent_pos[1]][self.agent_pos[0]])
            final_pos = tuple(map(lambda x,y: x+y, next_pos, wind_dy))
            #print(f"final position: {final_pos}")
        
            #check for grid boundaries 
            if final_pos[0] < 0 or final_pos[0] >= self.rows:
                final_pos = (self.agent_pos[0], final_pos[1])
            if final_pos[1] < 0 or final_pos[1] >= self.cols:
                final_pos = (final_pos[0], self.agent_pos[1])
            
            #print(f"final agent position: {self.agent_pos}")
        
        else:
            #print("restarting episode")
            final_pos = self.start_pos
    
        self.agent_pos = final_pos
        return self.agent_pos, reward, done, {}


class WindyStochasticGridWorldEnv(Env):
    def __init__(self):
        """Windy grid world gym environment
        This is the template for Q4a. You can use this class or modify it to create the variants for parts c and d.
        """

        # Grid dimensions (x, y)
        self.rows = 10
        self.cols = 7

        # Wind
        # TODO define self.wind as either a dict (keys would be states) or multidimensional array (states correspond to indices)
        self.wind = [[0]*self.rows]*self.cols
        for i in range(len(self.wind)):
            for j in range(len(self.wind[i])):
                if j == 3 or j == 4 or j == 5 or j == 8:
                    self.wind[i][j] = 1
                if j == 6 or j == 7:
                    self.wind[i][j] = 2

        self.action_space = spaces.Discrete(len(Action))
        self.observation_space = spaces.Tuple(
            (spaces.Discrete(self.rows), spaces.Discrete(self.cols))
        )

        # Set start_pos and goal_pos
        self.start_pos = (0, 3)
        self.goal_pos = (7, 3)
        self.agent_pos = None

    def seed(self, seed: Optional[int] = None) -> List[int]:
        """Fix seed of environment

        In order to make the environment completely reproducible, call this function and seed the action space as well.
            env = gym.make(...)
            env.seed(seed)
            env.action_space.seed(seed)

        This function does not need to be used for this assignment, it is given only for reference.
        """

        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def reset(self):
        self.agent_pos = self.start_pos
        return self.agent_pos

    def step(self, action: Action) -> Tuple[Tuple[int, int], float, bool, dict]:
        """Take one step in the environment.

        Takes in an action and returns the (next state, reward, done, info).
        See https://github.com/openai/gym/blob/master/gym/core.py#L42-L58 foand r more info.

        Args:
            action (Action): an action provided by the agent

        Returns:
            observation (object): agent's observation after taking one step in environment (this would be the next state s')
            reward (float) : reward for this transition
            done (bool): whether the episode has ended, in which case further step() calls will return undefined results
            info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning). Not used in this assignment.
        """
         # Check if goal was reached
        #print(f"agent pos: {self.agent_pos}")
        if self.agent_pos == self.goal_pos:
            done = True
            reward = 0.0
        else:
            done = False
            reward = -1.0
            
        if not done:
            #print(f"change from action: {actions_to_dxdy(action)}")
            next_pos = tuple(map(lambda x,y: x + y, self.agent_pos, actions_to_dxdy(action)))
            #print(f"next position: {next_pos}")
        
            #add the wind change to next pos
            #print(f"wind value: {self.wind[self.agent_pos[1]][self.agent_pos[0]]}")
            wind_dy = (0,self.wind[self.agent_pos[1]][self.agent_pos[0]])
            final_pos = tuple(map(lambda x,y: x+y, next_pos, wind_dy))
            #print(f"final position: {final_pos}")
        
            #check for grid boundaries 
            if final_pos[0] < 0 or final_pos[0] >= self.rows:
                final_pos = (self.agent_pos[0], final_pos[1])
            if final_pos[1] < 0 or final_pos[1] >= self.cols:
                final_pos = (final_pos[0], self.agent_pos[1])
            
            #print(f"final agent position: {self.agent_pos}")
        
        else:
            #print("restarting episode")
            final_pos = self.start_pos
    
        self.agent_pos = final_pos
        return self.agent_pos, reward, done, {}
