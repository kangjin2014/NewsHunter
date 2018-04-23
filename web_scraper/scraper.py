import urllib
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
import os.path

class scraper(object):
    
    def __init__(self, home_path):
        '''
        home_path example: 'https://www.cbc.ca'
        '''
        self.home_path = home_path
        assert (self.home_path.startswith('http') == True), "The home path should include 'http' or 'https'" 
        self.paths = []

    def __soupify(self, link = None):
        '''
        convert html_script to soup, BS4 object
        '''
        if link == None:
            link = self.home_path
        try:
            html_script = urllib.request.urlopen(urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})).read()
            soup = BeautifulSoup(html_script, 'html.parser')
            return soup
        except:
            return "no page found"
    
    def __relative_path_to_absolute_path(self, path):
        '''
        if condiction1 : remove '/' at the end of the home path
        if condiction2 : only take relative path, and then concatenate relative path with home path. 
        ''' 
        if self.home_path[-1] == '/': 
            self.home_path = self.home_path[:-1]
        if path is not None:
            if path.startswith('/'):
                path = self.home_path + path
                return path
        else :
            pass
    
    def __filter_irrelevant_link(self):
        pass

    def find_all_links(self, link = None):
        '''
        it takes in soup object and find all links on this webpage
        try/except handles the case when no valid soup is provided
        '''
        soup = self.__soupify(link)
        try:
            for path in soup.findAll('a'):
                path = path.get('href')
                path = self.__relative_path_to_absolute_path(path)
#                 print ('Path found : {}'.format(path))
                self.paths.append(path)
            return self.paths
        except:
            return self.paths
        
    def recursive_link_searching(self, ctr):
        '''
        recursively find pages accross the pages
        '''
        indicator = 0
        all_links = []
        indicator = 0
        paths = self.find_all_links()

        for path in paths:
            found_on_each_path = self.find_all_links(path)
            all_links.append(found_on_each_path)
            indicator += 1
            print ("Parsed {} page(s)".format(indicator))
            while indicator == ctr :
                return all_links

    def get_text(self, link):
        soup = self.__soupify(link)
        """
        removes a tag or string from the tree. 
        It returns the tag or string that was extracted:
        """
        while type(soup) != str:
            for script in soup(["script", "style"]):
                script.extract()

            tokens = soup.get_text().split('\n')
            text = ' '.join(tokens)
            text = re.sub('\xa0',' ', text)
            return text

    def save_links(self, links):
        '''
        save file if the file doesn't exist: overwrite not allow.
        '''
        file_name = re.findall(r'\/\/(.*?)$', self.home_path)[0].split('.')[-2]
        file_path = 'data/'+ 'links_' + file_name+'.csv'
        while os.path.exists(file_path) == False:
            ds = [x for sublist in links for x in sublist]
            ds = list(set(ds))
            df = pd.DataFrame(ds)
            df.columns = ['link']
            df.to_csv(file_path, index=False)

class link_analyzer(object):
    '''
    input: links, type :panda series
    ouput: filter out irrelevant path, keep related paths ranked by frequency
    '''
    def __init__(self, links):
        self.links = links.tolist()
    
    def __remove_home_path(self, link):
        return re.sub('http(.*?)//(.*?)/', '', link)
    
    def __split(self, link):
        return link.split('/')
    
    def __rename_columns(self, df_block):
        number_of_columns = df_block.shape[1]
        df_block.columns = [ 'col'+str(element) for element in np.arange(number_of_columns)]
        return df_block
    
    def generate_df_blocks(self):
        '''
        call above private functions to generate dataframe of path blocks
        eg. for single record 
        http://www.cnn.com/news/cananda/who-is-121.3.131 
        will turn to ['news', 'canada', 'who-is-121.3.131'] in a row
        '''
        sr_links = pd.Series(self.links)
        sr_links = sr_links.apply(self.__remove_home_path)
        sr_block = sr_links.apply(self.__split)
        df_block = pd.DataFrame(sr_block.tolist())
        df_block = self.__rename_columns(df_block)
        return df_block
    
    def block_analyzer(self, df_block):
        '''
        get frequent paths
        '''
        df_block_sorted = df_block.groupby(by=['col0']).count().sort_values(by=['col1'], ascending=False)
        df_block_sorted['percentage'] = df_block_sorted.col1/sum(df_block_sorted.col1)
        df_block_sorted = df_block_sorted[df_block_sorted.percentage > 0.01]
        return df_block_sorted
