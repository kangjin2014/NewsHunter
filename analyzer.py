import pandas as pd
import numpy as np
import re

def load_raw_links():
    df = pd.read_csv('data/dataset_ctvnews.csv')
    links = set(df.link.values.tolist())
    print ('Found {} links (duplicated)'.format(df.shape[0]))
    print ('Found {} links (unique).'.format(len(links)))
    return links

class link_analyzer(object):
    
    def __init__(self, links):
        self.links = list(links)
    
    def __remove_home_path(self, link):
        return re.sub('http(.*?)//(.*?)/', '', link)
    
    def __split(self, link):
        return link.split('/')
    
    def __rename_columns(self, df_block):
        number_of_columns = df_block.shape[1]
        df_block.columns = [ 'col'+str(element) for element in np.arange(number_of_columns)]
        return df_block
    
    def generate_df_blocks(self):
        sr_links = pd.Series(self.links)
        sr_links = sr_links.apply(self.__remove_home_path)
        sr_block = sr_links.apply(self.__split)
        df_block = pd.DataFrame(sr_block.tolist())
        df_blcok = self.__rename_columns(df_block)
        return df_block
    
    def block_analyzer(self, df_block):
        df_block_sorted = df_block.groupby(by=['col0']).count().sort_values(by=['col1'], ascending=False)
        df_block_sorted['percentage'] = df_block_sorted.col1/sum(df_block_sorted.col1)
        df_block_sorted = df_block_sorted[df_block_sorted.percentage > 0.01]
        return df_block_sorted
        
links = load_raw_links()
w = link_analyzer(links)
a = w.generate_df_blocks()
b = w.block_analyzer(a)
print ('Most frequent first-level paths are {}'.format(b.index.tolist()))