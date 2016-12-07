#!/usr/bin/env python
# encoding: utf-8

import sys
import pandas as pd

name=sys.argv[1]
df = pd.read_excel(name)
df = df.drop_duplicates(['words'])

df.to_excel('data2/' + name.split('.')[0] + '.xlsx', index=False)
