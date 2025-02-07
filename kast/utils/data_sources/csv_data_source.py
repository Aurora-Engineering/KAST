# GSC-19360-1, "Knowledge Acquisition and Synthesis Tool"
#
# Copyright © 2024 United States Government as represented by the 
# Administrator of the National Aeronautics and Space Administration.   
# All Rights Reserved.
#
# Licensed under the NASA Open Source Agreement version 1.3
# See "NOSA GSC-19360-1 KAST.pdf"

import csv
import numpy as np

from kast.src.kast_runtime import KastRuntime
from kast.utils.data_sources.core import DataSource

class CsvDataSource(DataSource):
    def __init__(self,runtime: KastRuntime):
        self.runtime = runtime
        self.data = np.array(list(
            csv.reader(open(self.runtime.data_file_path, 'r'))
            ))
        
        self.headers = self.data[0]
        self.data = self.data[1:]
        self.index = 0 # Set index to access second row on first call; first row stored as headers 

    def get_new_information(self):
        new_frame = self.data[self.index]
        new_information = dict(zip(self.headers, new_frame))
        self.index += 1

        return(new_information)
    
    def has_more(self):
        if self.index >= len(self.data):
            return False
        else:
            return True
        