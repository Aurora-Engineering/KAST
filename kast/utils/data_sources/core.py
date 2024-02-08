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