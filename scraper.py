import urllib
from bs4 import BeautifulSoup
import re
import pandas as pd

class web_scraping(object):
    
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
        if condiction2 : concatenate relative path with home path
        ''' 
        if self.home_path[-1] == '/': 
            self.home_path = self.home_path[:-1]
        if path is not None:
            if path.startswith('/'):
                path = self.home_path + path
            if path.startswith('http') == False:
                path = self.home_path
            return path
        else :
            pass
    
    def __filter_irrelevant_link(self):
        pass

    def find_all_links(self, link = None):
        '''
        it takes in soup object and find all links on this webpage
        try/except handles the case when no valid soup is provided.
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
        paths = self.find_all_links()
        
        for path in paths:
            found_on_each_path = self.find_all_links(path)
            all_links.append(found_on_each_path)
            indicator += 1
            print ("Parsed {} page(s)".format(indicator))
            if indicator < ctr:
                pass
            else:
                return all_links
             
front_page_link = 'http://www.cbc.ca/'
w = web_scraping(front_page_link)
s = w.recursive_link_searching(300)
ds = [x for sublist in s for x in sublist]
df = pd.DataFrame(ds)
df.to_csv('data/dataset.csv')