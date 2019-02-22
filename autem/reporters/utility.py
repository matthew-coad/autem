import numpy as np
import pandas as pd

def get_report_columns(records):
    """
    Get all the columns for a report from a set of records
    """
    columnDict = {}
    for row in records:
        for k in row.__dict__:
            if not k in columnDict:
                columnDict[k] = k
    return list(columnDict.keys())

def get_report_frame(records):
    """
    Convert a
    """
    columns = get_report_columns(records)
    columnValues = dict([ (column, []) for column in columns ])
    for row in records:
        for column in columns:
            value = getattr(row, column) if hasattr(row, column) else np.nan
            columnValues[column].append(value)
    frame = pd.DataFrame(data=columnValues) 
    return frame
