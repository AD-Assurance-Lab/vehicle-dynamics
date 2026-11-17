# Copyright 2026 AD Assurance Lab. Licensed under the Apache License, Version 2.0.
# Lab 1, Task 2: the layout an engineer would want. Have your AI assistant fill it in, then check each comment.
import numpy as np
import matplotlib.pyplot as plt

# 1. Constants at the top, units in the comment
MPH = ...                              # m/s per mph

# 2. The physics only: SI units in, meters out, nothing added
def stopping_distance(v0, a_b):        # v0 in m/s, a_b in m/s^2
    ...                                # d = v0^2 / (2 a_b)

# 3. The four surfaces and their a_b (m/s^2) in one dictionary
surfaces = ...

# 4. Speeds 10 to 80 mph for the plot, converted to m/s once, here
mph = ...
v0 = ...

# 5. One curve per surface; each axis says what it shows and its unit
...

# 6. Check: dry asphalt from 30 and 60 mph (11.2 m and 45.0 m)
...
