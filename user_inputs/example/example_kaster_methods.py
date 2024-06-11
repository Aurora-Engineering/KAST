def pose_and_rpy_to_posxy(pose, rpy):

	def strlist_to_list(strlist: str):
		return strlist.strip('][').split(',')

	pose = strlist_to_list(pose)
	rpy = strlist_to_list(rpy)

	pose_float = [float(p) for p in pose]
	rpy_float= [float(r) for r in rpy]

	posx = pose_float[0]
	posy = pose_float[1]
	rpy_x = rpy_float[0]
	return(posx, posy, rpy_x)