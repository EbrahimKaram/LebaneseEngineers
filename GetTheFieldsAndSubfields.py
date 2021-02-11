import pandas as pd
import numpy as np
import requests
import sys
import codecs

sys.stdout.reconfigure(encoding="utf-8")

if __name__ == "__main__":
    subfields_df = pd.read_csv("subfields.csv", encoding="utf-8", index_col=0)
    fields_df = pd.read_csv("fields.csv", encoding="utf-8", index_col=0)

    fields = np.delete(
        fields_df.index.to_numpy(), np.where(fields_df.index.to_numpy() == -1)
    )
    subfields = np.delete(
        subfields_df.index.to_numpy(), np.where(subfields_df.index.to_numpy() == -1)
    )
    print("Hello")

    # "fstname":,
    # "lstname":,
    # "fatname":,
    # "numb":,
    with codecs.open("TheCatogories.txt", "w", encoding="utf-8") as file1:

        for field in fields:
            for subfield in subfields:
                # print(field, subfield)
                # subfield = -1
                # field = -1
                parameters = {
                    "PageID": 112,
                    "CurrPage": 1,
                    "spec": field,
                    "spec1": subfield,
                    "searchoption": "And",
                    "rand": 0.055286690143709905,
                }
                r = requests.get(
                    "https://www.oea.org.lb/Arabic/GetMembers.aspx", params=parameters
                )

                response = r.text

                if "لا يوجد أي نتيجة" in response:
                    print("wrong issue")
                else:
                    print(
                        field,
                        fields_df.loc[field].Field,
                        subfield,
                        subfields_df.loc[subfield].Subfield,
                        sep=", ",
                    )

                    # Writing data to a file
                    file1.write(
                        ", ".join(
                            map(
                                str,
                                [
                                    field,
                                    fields_df.loc[field].Field,
                                    subfield,
                                    subfields_df.loc[subfield].Subfield,
                                ],
                            )
                        )
                    )
                    file1.write("\n")
