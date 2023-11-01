import pandas as pd

class CSVParser():
    def __init__(self,filename,line_by_line=True):
        self.df = pd.read_csv(filename)
        if line_by_line:
            self.iterator = self.df.iterrows()
    
    def get_df(self) -> pd.DataFrame:
        return(self.df)
    
    def get_columns(self) -> pd.Index:
        return(self.df.columns) 

    def get_size(self) -> tuple:
        return(self.df.shape)       
    
    def get_next_line(self) -> tuple[int, pd.Series]:
        """
        Moves to the next line in the read DataFrame and returns it with index.
        
        When the final line is reached, this method will return None.

        Returns
        -------
        tuple[int, pd.Series]
            The row index of the next line and the data contained in the next line as a tuple
        """
        nextline = next(self.iterator,None)
        return(nextline)