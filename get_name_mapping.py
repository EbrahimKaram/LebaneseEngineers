# %%
import json
import re

import editdistance
import pandas as pd
from tqdm import tqdm

# %%
engineers_df = pd.read_csv("Data/all_engineers.csv", encoding="utf-8")
half_names = [
    x.split(",")
    for x in open("half_names.csv", "r", encoding="utf-8").read().split("\n")
    if x != ""
]
# %%
# %%
full_name_map = []
for row in engineers_df[["Arabic_Names", "Latin_Names"]].iterrows():
    full_name_map.append(
        (row[0], row[1]["Arabic_Names"], row[1]["Latin_Names"]))
# %%

rejected_chars_regex = r"[^\u0621-\u063A\u0641-\u064Aa-z\- ]"


def clean(name: str):
    name = name.lower()
    name = name.replace("آ", "ا")
    name = name.replace("أ", "ا")
    name = name.replace("إ", "ا")
    name = re.sub(rejected_chars_regex, "", name)
    return name


def join_name_list(arabic_full_name: str, latin_full_name: str):
    """
    Splits the string by whitespace, then tries to find
    composite names using a predefined list of prefixes and suffixes
    """
    arabic_name_full_list_tmp = [clean(x) for x in arabic_full_name.split()]

    arabic_name_full_list = []
    for name in arabic_name_full_list_tmp:
        if name != "متاهلة":
            arabic_name_full_list.append(name)
        else:
            break

    latin_full_name_list = [clean(x) for x in latin_full_name.split()]
    flag = False
    for ar_hf_name, la_hf_name, is_start in half_names:
        new_ar_name_list = []
        if ar_hf_name in arabic_name_full_list and la_hf_name in " ".join(
            latin_full_name_list
        ):
            flag = True
            index = arabic_name_full_list.index(ar_hf_name)
            if is_start == "start":
                new_ar_name_list.extend(arabic_name_full_list[:index])
                new_ar_name_list.append(
                    ar_hf_name + "-" + arabic_name_full_list[index + 1]
                )
                new_ar_name_list.extend(arabic_name_full_list[index + 2:])
                arabic_name_full_list = new_ar_name_list
            else:
                new_ar_name_list.extend(arabic_name_full_list[: index - 1])
                new_ar_name_list.append(
                    arabic_name_full_list[index - 1] + "-" + ar_hf_name
                )
                new_ar_name_list.extend(arabic_name_full_list[index + 1:])
                arabic_name_full_list = new_ar_name_list
        new_la_name_list = []
        if la_hf_name in latin_full_name_list and ar_hf_name in " ".join(
            arabic_name_full_list
        ):
            flag = True
            index = latin_full_name_list.index(la_hf_name)
            if is_start == "start":
                new_la_name_list.extend(latin_full_name_list[:index])
                new_la_name_list.append(
                    la_hf_name + "-" + latin_full_name_list[index + 1]
                )
                new_la_name_list.extend(latin_full_name_list[index + 2:])
                latin_full_name_list = new_la_name_list
            else:
                new_la_name_list.extend(latin_full_name_list[: index - 1])
                new_la_name_list.append(
                    latin_full_name_list[index - 1] + "-" + la_hf_name
                )
                new_la_name_list.extend(latin_full_name_list[index + 1:])
                latin_full_name_list = new_la_name_list
    if flag:
        return join_name_list(
            " ".join(arabic_name_full_list), " ".join(latin_full_name_list)
        )
    else:
        return arabic_name_full_list, latin_full_name_list


def add_name_to_dict(source_name: str, target_name: str, name_dict: dict):
    if source_name in name_dict:
        if target_name in name_dict[source_name]:
            name_dict[source_name][target_name] += 1
        else:
            name_dict[source_name][target_name] = 1
    else:
        name_dict[source_name] = {target_name: 1}
    return name_dict


latin_to_arabic_name_map = {}
arabic_to_latin_name_map = {}
weird_names = []
fix_erros = []
for name_tuple in tqdm(full_name_map):
    id = name_tuple[0]
    arabic_full_name = name_tuple[1]
    latin_full_name = name_tuple[2]
    try:
        arabic_name_full_list, latin_full_name_list = join_name_list(
            arabic_full_name, latin_full_name
        )
    except:
        fix_erros.append(name_tuple)
        continue

    if len(arabic_name_full_list) == len(latin_full_name_list):
        for arabic_name, latin_name in zip(arabic_name_full_list, latin_full_name_list):
            latin_to_arabic_name_map = add_name_to_dict(
                latin_name, arabic_name, latin_to_arabic_name_map
            )
            arabic_to_latin_name_map = add_name_to_dict(
                arabic_name, latin_name, arabic_to_latin_name_map
            )
    else:
        weird_names.append((id, arabic_name_full_list, latin_full_name_list))


# %%
cleaned_latin_to_arabic_name_map = {}
wrong_count = 0
wrong_names = [("source_name", "target_name", "top_target_name")]
for source_name, value in latin_to_arabic_name_map.items():
    value = dict(sorted(value.items(), key=lambda item: item[1], reverse=True))
    cleaned_value = {}
    for idx, (target_name, count) in enumerate(value.items()):
        if idx == 0:
            cleaned_value[target_name] = count
            continue
        top_target_name = list(
            dict(
                sorted(
                    arabic_to_latin_name_map[target_name].items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
            ).keys()
        )[0]
        if editdistance.eval(top_target_name, source_name) > 2:
            wrong_names.append((source_name, target_name, top_target_name))
            wrong_count += 1
            continue
        else:
            cleaned_value[target_name] = count
    cleaned_latin_to_arabic_name_map[source_name] = cleaned_value

print("Cleaned Words: ", wrong_count)
# %%
cleaned_arabic_to_latin_name_map = {}
wrong_count = 0
wrong_names = [("source_name", "target_name", "top_target_name")]
for source_name, value in arabic_to_latin_name_map.items():
    value = dict(sorted(value.items(), key=lambda item: item[1], reverse=True))
    cleaned_value = {}
    for idx, (target_name, count) in enumerate(value.items()):
        if idx == 0:
            cleaned_value[target_name] = count
            continue
        top_target_name = list(
            dict(
                sorted(
                    latin_to_arabic_name_map[target_name].items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
            ).keys()
        )[0]
        if editdistance.eval(top_target_name, source_name) > 2:
            wrong_names.append((source_name, target_name, top_target_name))
            wrong_count += 1
            continue
        else:
            cleaned_value[target_name] = count
    cleaned_arabic_to_latin_name_map[source_name] = cleaned_value

print("Cleaned Words: ", wrong_count)

# %%
json.dump(
    cleaned_latin_to_arabic_name_map,
    open("name_maps/latin_to_arabic_map.json", "w", encoding="utf-8"),
)
json.dump(
    cleaned_arabic_to_latin_name_map,
    open("name_maps/arabic_to_latin_map.json", "w", encoding="utf-8"),
)
# %%
print("Total Arabic Names: ", len(cleaned_arabic_to_latin_name_map))
print("Total Latin Names: ", len(cleaned_latin_to_arabic_name_map))
# %%
