import requests
import json
import numpy as np
import pandas as pd
from dotenv import load_dotenv
import os
import pyarrow.parquet as pq
import pyarrow as pa


data = {'one': [-1, np.nan, 2.5],
        'two': ['foo', 'bar', 'baz'],
        'three': [True, False, True]
        }


df = pd.DataFrame(data, index=list('abc'))

table = pa.Table.from_pandas(df)
pq.write_table(table, 'test.parquet')
table2 = pq.read_table('test.parquet').to_pandas()
print(table2)