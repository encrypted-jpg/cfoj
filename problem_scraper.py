import requests
from bs4 import BeautifulSoup
import pickle
import time


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class Contest:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.problems = []

    def __str__(self):
        ptr = "Name: " + self.name + "\n"
        ptr += "URL: " + self.url + "\n"
        ptr += "PROBLEMS: " + "\n\n"
        for x in self.problems:
            ptr += str(x) + "\n"
        return ptr

    def __lt__(self, other):
        url = "https://codeforces.com/contest/"
        num = self.url.replace(url, "")
        num = int(num)
        onum = other.url
        onum = int(onum.replace(url, ""))
        return num < onum


class Problem:
    def __init__(self, name, url, id, num_submissions):
        self.name = name
        self.url = url
        self.id = id
        self.submissions = num_submissions
        self.tags = []
        self.difficulty = 0

    def __str__(self):
        ptr = "Name:" + self.name + "\n"
        ptr += "URL:" + self.url + "\n"
        ptr += "ID:" + self.id + "\n"
        ptr += "Num Submissions:" + str(self.submissions) + "\n"
        ptr += "TAGS:" + ", ".join(self.tags) + "\n"
        return ptr

    def __lt__(self, other):
        return self.submissions > other.submissions


def updateProblems(contest):
    print("[+] Fetching Problem Tags from....", contest.url)
    plist = contest.problems
    for pro in plist:
        purl = pro.url
        data = requests.get(purl)
        soup = BeautifulSoup(data.text, "html.parser")
        divs = soup.find_all("span", {"class": "tag-box"})
        for x in divs:
            pro.tags.append(x.text.strip())
        try:
            pro.difficulty = int(pro.tags[-1][1:])
        except:
            pass
    print(f"{bcolors.OKGREEN}[+] Success....{bcolors.ENDC}")
    return contest


def getProblemUrls(url=""):
    print("[+] Fetching Problem Urls from...", url)
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")
    tab = soup.find("table", {"class": "problems"})
    trs = soup.find_all("tr")
    tr = trs[3]
    link_letter = tr.find_all("td", {"class": "id"})
    tds = tr.find_all("td")
    base_url = "https://codeforces.com"
    plist = []
    for x in range(0, len(tds), 4):
        l = tds[x].find("a")
        curl = base_url + l.get("href")
        cid = l.text.strip()
        l = tds[x + 1].find("a")
        cname = l.text
        num = tds[x + 3].text.strip().replace("x", "").split()[0]
        num = int(num)
        plist.append(Problem(cname, curl, cid, num))
    rt = soup.find("table", {"class": "rtable"})
    tr = rt.find("tr").text.strip()
    contest = Contest(tr, url)
    contest.problems = plist
    print(f"{bcolors.OKGREEN}[+] Success....{bcolors.ENDC}")
    return updateProblems(contest)


if __name__ == "__main__":
    start = time.time()
    url = "https://codeforces.com/contest/"
    contests = []
    for x in range(1299, 1099, -1):
        try:
            cont = getProblemUrls(url + str(x))
            contests.append(cont)
        except:
            print(
                f"{bcolors.FAIL}[-] Fetching Problem Urls Failed from.... ",
                url + str(x),
                bcolors.ENDC,
            )

    file = open("data1299-1100.pickle", "wb")
    pickle.dump(contests, file)
    file.close()
    print(f"{bcolors.OKGREEN}[+] Data Saved to data.pickle....{bcolors.ENDC}")
    print(
        f"{bcolors.OKGREEN}[+] Time Taken = ",
        round(time.time() - start, 2),
        f"sec{bcolors.ENDC}",
    )
