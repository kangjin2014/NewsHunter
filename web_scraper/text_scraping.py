import scraper as sp
import pandas as pd
import numpy as np

df = pd.read_csv('data/links_cnn.csv')
print ('{} records'.format(df.shape[0]))
ins_scraper = sp.scraper('http://i-just-want-to-initiate-the-class')

ctr = 0
text_list = []
for link in df['link']:
    ctr += 1
    try: 
        text_list.append(ins_scraper.get_text(link))
        print ('Page ' + str(ctr))
    except:
        text_list.append('no text found')
        print ('no text found')
df['text'] = pd.Series(text_list)

df.to_csv('data/text_cnn.csv', index= False)
