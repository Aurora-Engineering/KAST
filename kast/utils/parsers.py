import pandas as pd
from typing import Dict, Iterator

class CSVParser():
    def __init__(self,filename):
        self.df: pd.DataFrame = pd.read_csv(filename)
        self._iterator: Iterator = self.df.itertuples()    
    
    def get_next_mapped_line(self) -> Dict:
        """
        Moves to the next line in the read DataFrame and returns it with index.
        
        When the final line is reached, this method will return None.

        Returns
        -------
        tuple[int, pd.Series]
            The row index of the next line and the data contained in the next line as a tuple
        """
        nextline = next(self._iterator,None)
        if nextline != None:
            nextline = nextline._asdict()
        return(nextline)