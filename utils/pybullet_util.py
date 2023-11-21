def strlist_to_list(strlist):
	return strlist.strip('][').split(',')

def pose_to_posz(pose):
	pose = [float(p) for p in pose]
	return({
		'posz': [pose[2]]
		})