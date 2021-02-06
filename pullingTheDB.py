import pandas as pd
import requests
import sys
import codecs

sys.stdout.reconfigure(encoding='utf-8')

if __name__ == '__main__':
    df = pd.read_csv("TheCatogories.csv", encoding="utf-8")

    print(df.head(5))
