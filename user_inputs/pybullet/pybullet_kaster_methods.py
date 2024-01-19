def strlist_to_list(strlist: str):
	return strlist.strip('][').split(',')

def pose_to_posxy(pose):
	pose = strlist_to_list(pose)
	pose_float = [float(p) for p in pose]
	return({
		'posx': pose_float[0],
		'posy': pose_float[1]
		})