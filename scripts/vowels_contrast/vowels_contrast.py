# coding: utf-8

import re
import numpy as np
import pandas as pd

from bs4 import BeautifulSoup

df_WB = pd.read_csv('data/coca20k_WB_speech.csv')


df_nn = df_WB[df_WB.phonetic.notnull()]

# AI -> aı
df_nn[df_nn.phonetic.str.contains('aı')].ix[:5000, :].to_excel('coca5k_AI.xlsx', index=False)

# AA -> æ
df_nn[df_nn.phonetic.str.contains('æ')].ix[:5000, :].to_excel('coca5k_AA.xlsx', index=False)

# EH -> ɛ
df_nn[df_nn.phonetic.str.contains('ɛ')].ix[:5000, :].to_excel('coca5k_EH.xlsx', index=False)

# AH -> ɑ
df_nn[df_nn.phonetic.str.contains('ɑ') & ~df_nn.phonetic.str.contains('aı')]
# df_ar = df_nn[df_nn.phonetic.str.contains('ɑ') & ~df_nn.phonetic.str.contains('aı') &
   # ~df_nn.phonetic.str.contains('ɑː')]

## 关于 ɔ

with open('coca-macm/coca20k-macm.html') as file:
    data = file.read()

def find_phonetic(data):
    bsObj = BeautifulSoup(data, "lxml")
    mylist2 = bsObj.find_all('font', {'color':'#21887d'})
    lst2 = [i.get_text() for i in mylist2]
    return '\n'.join(lst2)

df_html = pd.DataFrame({'all': data.split('\n            \n             <tr>')[1:]})
df_csv = pd.read_csv('coca-macm/coca20k-macm.csv').ix[:, 1:]
df_csv.rename(columns={
        '单词': 'words',
        '解释': 'des',
    }, inplace=True)

df_c = pd.concat([df_csv.ix[:, ['words']], df_html], axis=1 )
df_c['mac_speech'] = df_c['all'].map(find_phonetic)
df_mm = pd.merge(df_nn, df_c.ix[:, ['words', 'mac_speech']], on='words', how='right')
df_mm = df_mm[df_mm['mac_speech'].notnull()]
df_AW = df_mm[df_mm['mac_speech'].str.contains('ɔ')]

# AW -> ɔ
df_AW[df_AW['rank'] < 5000].to_excel(
    'coca5k_AW.xlsx', index=False,
    columns='rank words mac_speech coca_speech phonetic WB_speech'.split())

# OW -> aʊ
df_nn[df_nn.phonetic.str.contains('aʊ')].ix[:5000, :].to_excel('coca5k_OW.xlsx', index=False)

# IH -> ɪ
df_nn[df_nn.phonetic.str.contains('ı') &
    ~df_nn.phonetic.str.contains('eı') &
    ~df_nn.phonetic.str.contains('oı')
    ].ix[:5000, :].to_excel('coca5k_IH.xlsx', index=False)

# AY -> eı
df_nn[df_nn.phonetic.str.contains('eı')].ix[:5000, :].to_excel('coca5k_AY.xlsx', index=False)

# EE -> i
df_nn[df_nn.phonetic.str.contains('i')].ix[:5000, :].to_excel('coca5k_EE.xlsx', index=False)

# UH3 -> ʊ
df_nn[df_nn.phonetic.str.contains('ʊ')].ix[:5000, :].to_excel('coca5k_UH3.xlsx', index=False)

# OO -> u
df_nn[df_nn.phonetic.str.contains('u')].ix[:5000, :].to_excel('coca5k_OO.xlsx', index=False)
