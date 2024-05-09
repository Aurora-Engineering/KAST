import csv
import numpy as np

from kast.src.kast_runtime import KastRuntime
from kast.utils.data_sources.core import DataSource

class LiveDataSource(DataSource):
    def __init__(self,runtime: KastRuntime):
        self.runtime = runtime
        self.headers = self.runtime.headers
        self.index = 0

    def get_new_information(self,new_frame):
        new_information = dict(zip(self.headers, new_frame))
        self.index += 1

        return(new_information)
    
    def has_more(self):
        return True
        