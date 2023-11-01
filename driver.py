# Knowledge Aquisition and Synthesis Tool

from src.predicate import Predicate
from src.telem.telemetry import Telemetry
import numpy as np

def main():
	temp_pred = Predicate('at', [1,2,3])
	temp_arr = np.array([(1,2),(3,4)])
	temp_telem = Telemetry('Numpy Array',type(temp_arr),temp_arr)
	print(temp_pred)
	print(temp_telem)
	return 

if __name__ == '__main__':
    main()