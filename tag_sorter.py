import pickle
from problem_scraper import Contest, Problem
import os

tags = set()
lst = []
pst = os.listdir("data/")
for x in pst:
    with open("data/"+x, "rb") as file:
        lst += pickle.load(file)
contests = []
problems = []
for x in lst:
    contests.append(x)
    for y in x.problems:
        problems.append(y)
        for z in y.tags:
            try:
                z = z.replace('*', '')
                k = int(z)
            except:
                tags.add(z)
tags = sorted(tags)
tag_dict = {}
for tag in tags:
    tag_dict[tag] = []
    for x in lst:
        for y in x.problems:
            for z in y.tags:
                z = z.replace("*", "")
                if z == tag:
                    tag_dict[tag].append(y)
                    break
    tag_dict[tag].sort()
print(len(contests))
print(len(problems))
for key, value in tag_dict.items():
    print(key, len(value))
with open("data/tag_sorted_dict.pickle", "wb") as file:
    pickle.dump(tag_dict, file)
