import csv
import numpy as np

from kast.src.runtime.core import KastRuntime
from kast.utils.data_sources.core import DataSource

class MANUALDataSource(DataSource):
    def __init__(self,runtime: KastRuntime):
        self.runtime = runtime
        self.headers = self.runtime.config['DEFAULT']['LowLevelHeaders'].split(",")
        self.index = 0

    def get_new_information(self,new_frame):
        new_information = dict(zip(self.headers, new_frame))
        self.index += 1

        return(new_information)
    
    def has_more(self):
        return True
        