import pandas as pd


def convert_date_cell(value):
    try:
        if pd.NaT == value:
            return 'null'
        return f'\'{pd.to_datetime(value, errors='raise')}\''
    except (ValueError, TypeError):
        return 'null'
