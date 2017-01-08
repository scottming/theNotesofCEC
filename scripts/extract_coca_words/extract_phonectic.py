# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


def find_phonetic(data):
    """寻找所有音标."""
    bsObj = BeautifulSoup(data, "lxml")
    mylist = bsObj.find_all('font', {'color': 'darkslategray'})
    lst = [i.get_text() for i in mylist]
    return '\n'.join(lst)


def find_speech(data):
    """寻找所有词性."""
    bsObj = BeautifulSoup(data, "lxml")
    mylist = bsObj.find_all('span', {
        'style':'color: #FFFFFF; background-color: #006400; font-size: xx-small'})
    lst = [i.get_text() for i in mylist]
    return '\n'.join(lst)


def find_intersection(values, eight_df):
    arr1 = np.asarray(values.split('\n'))  # 先转成列表，再转 array
    arr2 = eight_df.speech.values
    result = np.intersect1d(arr1, arr2)
    lst = result.tolist()
    return '\n'.join(lst)


class WordsData(object):
    """docstring for WordsData"""
    def __init__(self, html_data, csv_data, source_data,
                 csv_export=None, xlsx_export=None):
        self.html_data = html_data
        self.csv_data = csv_data
        self.source_data = source_data
        self.csv_export = csv_export
        self.xlsx_export = xlsx_export


    def get_html_df(self):
        """获取字典的 HTML 对象."""
        with open(self.html_data) as file:
            html_data = file.read()
        df = pd.DataFrame({
            'all': html_data.split('<tr>\n                ')[2:]})
        df['phonetic'] = df['all'].map(find_phonetic)
        return df

    def get_csv_df(self):
        csv_df = pd.read_csv(self.csv_data)
        csv_df.rename(columns={
            '单词': 'words',
            '解释': 'meaning',
            }, inplace=True)
        return csv_df

    def get_eight_speech(self):
        EIGHT_SPEECH_PATH = 'data/eight_speech.txt'
        eight_df = pd.read_csv(EIGHT_SPEECH_PATH)
        return eight_df

    def get_source_df(self):
        source_df = pd.read_csv(self.source_data)
        source_df = source_df.ix[:, 'rank words speech'.split()]
        source_df.rename(columns={
            'speech': 'coca_speech',
        }, inplace=True)
        return source_df

    def wrange(self):
        html_df = self.get_html_df()
        csv_df = self.get_csv_df()
        df = pd.concat(
            [csv_df.ix[:, ['words']], html_df], axis=1)
        df['all_speech'] = df['all'].map(find_speech)
        df['WB_speech'] = df.all_speech.apply(
            find_intersection, eight_df=self.get_eight_speech())
        df = pd.merge(self.get_source_df(), df, on='words', how='left')
        return df

    def export(self):
        columns = 'rank words phonetic coca_speech WB_speech'.split()
        df = self.wrange()
        df.to_csv(
            self.csv_export, columns=columns, index=False)
        df.to_excel(
            self.xlsx_export, columns=columns, index=False)


coca = WordsData(
    'data/coca60k_WB.html',
    'data/coca60k_WB.csv',
    'data/coca60k_source.csv')

coca.csv_export = 'coca60k_WB_speech.csv'
coca.xlsx_export = 'coca60k_WB_speech.xlsx'
coca.export()
# coca = WordsData(
#     'data/coca20k_WB.html',
#     'data/coca20k_WB.csv',
#     'data/coca20k_source.csv')
#
# coca.csv_export = 'coca20k_WB_speech.csv'
# coca.xlsx_export = 'coca20k_WB_speech.xlsx'
# coca.export()
print("DONE!!!")

