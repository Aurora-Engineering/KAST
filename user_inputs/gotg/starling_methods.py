import re
import numpy as np
import json

from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Bool

def tb_pose_to_position(tb_pose: PoseStamped):
    try:
        x = tb_pose.pose.position.x
        y = tb_pose.pose.position.y
        z = tb_pose.pose.position.z
    except AttributeError:
        x, y, z = (-999, -999, -999)
    tb_position = [x, y, z]
    return (tb_position, )

def tb_event_to_bool(tb_event: Bool):
    try:
        tb_event_bool = tb_event.data
    except AttributeError:
        tb_event_bool = False

    return (tb_event_bool, )

def redis_mavlink_to_drone_position(mavlink_tlm_position_velocity_ned):
    transform_mask = np.array([1, 1, -1]) # Change NED to XYZ

    msg = json.loads(mavlink_tlm_position_velocity_ned['data'].decode())
    position_dict = msg['position_velocity_ned']['position']

    ned_coords =  (position_dict['north_m'], position_dict['east_m'], position_dict['down_m'])
    drone_position = np.multiply(transform_mask, np.array(ned_coords))

    return (drone_position, )
	