import pickle
from problem_scraper import Problem, Contest
import os


def update_problems(contests):
    diff_dict = {"A": 800, "B": 1100, "C": 1600, "D": 2200, "E": 2600, "F": 2900, "G": 3000, "H": 3100, "I": 3400,
                 "J": 3500, "K": 3500}
    tags = set()
    for cont in contests:
        # print(cont.name)
        for pro in cont.problems:
            if pro.difficulty == 0:
                try:
                    pro.difficulty = diff_dict[pro.id[0]]
                except Exception as e:
                    pass
            tags.add(pro.difficulty)
    with open("data/final_data1525-500.pickle", "wb") as file:
        pickle.dump(contests, file)
    return contests, sorted(tags)


def get_lst():
    lst = []
    pst = os.listdir("data/")
    for x in pst:
        if not x.startswith("data"):
            continue
        with open("data/" + x, "rb") as file:
            lst += pickle.load(file)
    return lst


def rating_sort(contests, tags):
    tdict = {}
    for tag in tags:
        tdict[tag] = []
        for cont in contests:
            for pro in cont.problems:
                if pro.difficulty == tag:
                    tdict[tag].append(pro)
        tdict[tag].sort()
    tag_dict = {
        "CodeForces Rating < 1100": sorted(tdict[800] + tdict[900] + tdict[1000]),
        "1100 <= Codeforces Rating <= 1299": sorted(tdict[1100] + tdict[1200]),
        "1300 <= Codeforces Rating <= 1499": sorted(tdict[1300] + tdict[1400]),
        "1500 <= Codeforces Rating <= 1699": sorted(tdict[1500] + tdict[1600]),
        "1700 <= Codeforces Rating <= 1899": sorted(tdict[1700] + tdict[1800]),
        "1900 <= Codeforces Rating <= 2099": sorted(tdict[1900] + tdict[2000]),
        "2100 <= Codeforces Rating <= 2299": sorted(tdict[2100] + tdict[2200]),
        "2300 <= Codeforces Rating <= 2499": sorted(tdict[2300] + tdict[2400]),
        "2500 <= Codeforces Rating <= 2699": sorted(tdict[2500] + tdict[2600]),
        "2700 <= Codeforces Rating <= 2899": sorted(tdict[2700] + tdict[2800]),
        "Codeforces Rating >= 2900": sorted(
            tdict[2900] + tdict[3000] + tdict[3100] + tdict[3200] + tdict[3300] + tdict[3400] +
            tdict[3500])
    }
    for tag, num in tag_dict.items():
        print(tag, len(num))
    return tag_dict


def div_id_sort(contests):
    div2_dict = {
        "A": [],
        "B": [],
        "C": [],
        "D": [],
        "E": [],
        "F": []
    }
    div1_dict = {
        "A": [],
        "B": [],
        "C": [],
        "D": [],
        "E": [],
        "F": []
    }
    for cont in contests:
        if "Div. 2" not in cont.name and "Div. 1" in cont.name:
            for pro in cont.problems:
                try:
                    div1_dict[pro.id[0]].append(pro)
                except Exception as e:
                    pass
        else:
            for pro in cont.problems:
                try:
                    div2_dict[pro.id[0]].append(pro)
                except Exception as e:
                    pass
    tag_dict = {
        "CodeForces Div.2-A": sorted(div2_dict["A"]),
        "CodeForces Div.2-B": sorted(div2_dict["B"]),
        "CodeForces Div.2-C": sorted(div2_dict["C"]),
        "CodeForces Div.2-D": sorted(div2_dict["D"]),
        "CodeForces Div.2-E": sorted(div2_dict["E"]),
        "CodeForces Div.2-F": sorted(div2_dict["F"]),
        "CodeForces Div.1-A": sorted(div1_dict["A"]),
        "CodeForces Div.1-B": sorted(div1_dict["B"]),
        "CodeForces Div.1-C": sorted(div1_dict["C"]),
        "CodeForces Div.1-D": sorted(div1_dict["D"]),
        "CodeForces Div.1-E": sorted(div1_dict["E"]),
        "CodeForces Div.1-F": sorted(div1_dict["F"]),
    }
    for tag, num in tag_dict.items():
        print(tag, len(num))
    return tag_dict


if __name__ == "__main__":
    lst = get_lst()
    contests, tags = update_problems(lst)
    # with open("data/final_data1525-500.pickle", "rb") as file:
    #     contests = pickle.load(file)
    tag_dict = {**rating_sort(contests, tags), **div_id_sort(contests)}
    # for tag, num in tag_dict.items():
    #     print(tag, len(num))
    with open("data/ladder_sorted_dict.pickle", "wb") as file:
        pickle.dump(tag_dict, file)
