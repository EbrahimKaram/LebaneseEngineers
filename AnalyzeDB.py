import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv("Data/all_engineers.csv", encoding="utf-8")
    # df.Links = "https://www.oea.org.lb/Arabic/"+df.Links
    # df.to_csv("Data/all_engineers.csv", index=False)
# Useful
# https://intellipaat.com/community/32844/insert-a-link-inside-a-pandas-table
# from IPython.display import HTML
# df['Links'] = df['Links'].apply(lambda x: '<a href="{0}">Details</a>'.format(x))
# HTML(df.to_html(escape=False))

