import pandas as pd
from typing import Callable, List

def load_datasets(file_name: str):
    return pd.read_csv(f'datasets/{file_name}')

def apply_clear_function(
    data: pd.DataFrame, 
    data_column: str, 
    clear_func: Callable[[str], str],
    drop_columns: List[str]
) -> pd.DataFrame:
    for c in drop_columns:
        data = data.drop(c, axis=1)
        
    return  data[data_column].apply(clear_func)

def cache_data_frame(data: pd.DataFrame, file_name: str):
    data.to_csv(f'datasets/{file_name}')