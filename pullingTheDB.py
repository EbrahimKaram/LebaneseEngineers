import pandas as pd
import requests
import random
from bs4 import BeautifulSoup
import sys
import codecs

sys.stdout.reconfigure(encoding='utf-8')

if __name__ == '__main__':
    df = pd.read_csv("Categories/TheCatogories.csv", encoding="utf-8")

    for index, row in df.iterrows():
        field = row['Field_ID']
        subfield = row["SubField_ID"]
        # TODO: CurrPage needs to increase by 1 until end
        random_number = random.uniform(0, 1)
        print(random_number)
        parameters = {
            "PageID": 112,
            "CurrPage": 1,
            "spec": field,
            "spec1": subfield,
            "searchoption": "And",
            "rand": random_number
        }
        r = requests.get(
            "https://www.oea.org.lb/Arabic/GetMembers.aspx", params=parameters)

        response = r.text

        soup = BeautifulSoup(response, 'html.parser')
        # print(response)
        engineer_IDs = soup.find_all(class_="date")
        arabic_names = soup.find_all(class_="company")
        latin_names = soup.find_all(class_="field")
        links = soup.find_all(class_="more")


        data={"Engineer_ID":engineer_IDs,
        "Arabic_Names":arabic_names,
        "Latin_Names":latin_names,
        "Links": links}

# TODO: Create CSV and check it
# TODO: create dictionaary
# We need the remove the added divs and info

        break
