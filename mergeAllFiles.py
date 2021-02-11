import glob
import pandas as pd


if __name__ == "__main__":
    files = glob.glob("Data/*[0-9].csv")
    print(files)
    print(len(files))
    dfs = []
    for file in files:
        df = pd.read_csv(file, encoding="utf-8")
        dfs.append(df)

    all_engineers = pd.concat(dfs, ignore_index=True)

    all_engineers.to_csv("Data/all_engineers.csv", index=False)
