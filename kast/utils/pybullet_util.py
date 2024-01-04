def strlist_to_list(strlist):
	return strlist.strip('][').split(',')

def pose_to_posxy(pose):
	pose = [float(p) for p in pose]
	return({
		'posx': pose[0],
		'posy': pose[1]
		})