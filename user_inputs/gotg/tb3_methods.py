import re
import numpy as np
import json

from nav_msgs.msg import Odometry
from std_msgs.msg import Bool

def starling_msg_to_bool(starling_sample_collected: Bool):
    # Extract data from Starling-published message
    try:
        drone_sampled = starling_sample_collected.data
    except AttributeError:
        print(f'Null message received for Starling msg; returning ridiculous value')
        drone_sampled = False

    return (drone_sampled, )

def tb_odometry_to_position(odom: Odometry):
    # Extract position data from odom message
    print(odom)
    try:
        position = odom.pose.pose.position
        tb_position = np.array([position.x, position.y])
    except AttributeError:
        print(f'Null message received for odom; returning ridiculous value')
        tb_position = [-999, -999]

    return(tb_position, )