import scraper as sp

front_page_link = 'https://www.cnn.com'
pages_to_parse = 30

instance = sp.scraper(front_page_link)
links = instance.recursive_link_searching(pages_to_parse)
instance.save_links(links)

# df = pd.read_csv('data/links_cnn.csv')
# w = sp.link_analyzer(df.link)
# a = w.generate_df_blocks()
# b = w.block_analyzer(a)
# print ('Most frequent first-level paths are {}'.format(b.index.tolist()))