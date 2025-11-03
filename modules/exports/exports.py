from typing import Final
from fob_postgres.functions import execute_query_with_results,exec_query_no_result
import glob
import win32com.client as win32
import os

PUBLIC_EXPORTS_QUERY : Final[str] = r"""

                SELECT 'COPY '||TABLE_NAME||' TO ''C:\exports\'||table_name||'.csv'' WITH (FORMAT csv, HEADER);'
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_SCHEMA = 'public'

            """

SOURCE_FOLDER: Final[str] = r'C:\exports'
DESTINATION_FOLDER: Final[str] = r'C:\merged_folder'


def export_data():
    MASTER_STRING = ""
    result = execute_query_with_results(PUBLIC_EXPORTS_QUERY)
    for item in result:
        MASTER_STRING += item[0]
        MASTER_STRING += "\n"
    exec_query_no_result(MASTER_STRING)
