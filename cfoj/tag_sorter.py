import pickle
from problem_scraper import Contest, Problem

tags = set()
file = open("data1521-1400.pickle", "rb")
lst = pickle.load(file)
file.close()
file = open("data1399-1300.pickle", "rb")
lst += pickle.load(file)
file.close()
file = open("data1299-1100.pickle", "rb")
lst += pickle.load(file)
file.close()
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
print(len(contests))
print(len(problems))
for key, value in tag_dict.items():
    print(key, len(value))
file = open("tag_sorted_dict.pickle", "wb")
pickle.dump(tag_dict, file)
file.close()