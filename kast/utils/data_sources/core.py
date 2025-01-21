# GSC-19360-1, "Knowledge Acquisition and Synthesis Tool"
#
# Copyright © 2024 United States Government as represented by the 
# Administrator of the National Aeronautics and Space Administration.   
# All Rights Reserved.
#
# Licensed under the NASA Open Source Agreement version 1.3
# See "NOSA GSC-19360-1 KAST.pdf"

from typing import Dict

class DataSource():
    def __init__(self):
        # Initialize data source (read csv, subscribe to Redis channels, etc)
        raise NotImplementedError

    def get_new_information(self) -> Dict:
        # Get the next packet of information
        raise NotImplementedError
    
    def has_more(self) -> bool:
        # Does the data source have more information to return?
        raise NotImplementedError