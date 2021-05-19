import pickle
import requests
from bs4 import BeautifulSoup
from problem_scraper import Contest, Problem, bcolors
import concurrent.futures
import time
from datetime import datetime,timedelta


class Submission:
    def __init__(self, url, time, date, user, problem, verdict):
        self.url = url
        self.user = user
        self.time_str = time
        self.date = date
        self.problem = problem
        self.verdict = verdict

    def __str__(self):
        ptr = "Submission URL: " + self.url + "\n"
        ptr += "User: " + self.user + "\n"
        ptr += "Time: " + self.time_str + "\n"
        ptr += "Problem: " + self.problem + "\n"
        ptr += "Verdict: " + self.verdict + "\n"
        return ptr

    def __lt__(self, other):
        return self.date > other.date


def operation(url, handle):
    submissions = []
    print("[+] Fetching Submissions from URL...." + url)
    try:
        data = requests.get(url).text
        soup = BeautifulSoup(data, "html.parser")
        table = soup.find("table", {"class": "status-frame-datatable"})
        trs = table.find_all("tr")[1:]
        base_url = "https://codeforces.com"
        for x in trs:
            td = x.find_all("td")
            hidden = td[0].find('span', {"class": 'hiddenSource'})
            if hidden is not None:
                continue
            slink = td[0].find("a").get("href")
            stime = td[1].text.strip()
            dtime = datetime.strptime(stime, '%b/%d/%Y %H:%M')
            dtime += timedelta(hours=2, minutes=30)
            stime = datetime.strftime(dtime, '%b/%d/%Y %H:%M')
            suser = td[2].text.strip().replace('#', '')
            sproblem = td[3].find("a").get("href")
            sjudge = td[5].text.strip()
            if sjudge == "Accepted" and suser == handle:
                submissions.append(
                    Submission(base_url + slink, stime, dtime, suser, base_url + sproblem, sjudge)
                )
        print(f"{bcolors.OKGREEN}[+] Success....{bcolors.ENDC}")
    except Exception as e:
        raise e
    return submissions


def submission_scraper(handle):
    start = time.time()
    url = "https://codeforces.com/submissions/" + handle + "/page/1"
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")
    divs = soup.find_all('div', {'class': 'pagination'})[-1]
    spans = divs.find_all('span', {'class': 'page-index'})
    n = []
    for x in spans:
        n.append(int(x.text.strip()))
    n = max(n)
    try:
        submissions = operation(url, handle)
    except Exception:
        return []
    URLS = ["https://codeforces.com/submissions/" + handle + "/page/" + str(i) for i in range(2, n + 1)]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(operation, url, handle): url for url in URLS}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                submissions += future.result()
            except Exception as exc:
                print(exc)
                print(f"{bcolors.FAIL} [-] Fetching Submissions from URL Failed...." + url, bcolors.ENDC)
                break
    submissions.sort()
    with open("user_data/" + handle + ".pickle", "wb") as file:
        pickle.dump(submissions, file)
    print("[+]", time.time() - start, "sec")
    return submissions


def update_submissions(handle):
    start = time.time()
    url = "https://codeforces.com/submissions/" + handle + "/page/1"
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")
    divs = soup.find_all('div', {'class': 'pagination'})[-1]
    spans = divs.find_all('span', {'class': 'page-index'})
    n = []
    for x in spans:
        n.append(int(x.text.strip()))
    n = max(n)
    try:
        submissions = operation(url, handle)
    except Exception as e:
        print(e)
        return []
    got = False
    change = False
    try:
        with open("user_data/" + handle + ".pickle", "rb") as file:
            lst = pickle.load(file)
    except Exception as e:
        return submission_scraper(handle)
    first = lst[0]
    for x in submissions:
        if x.date == first.date:
            got = True
            break
        else:
            lst.append(x)
            change = True
    i = 2
    while not got:
        url = "https://codeforces.com/submissions/" + handle + "/page/" + str(i)
        submissions = operation(url, handle)
        for x in submissions:
            if x.date == first.date:
                got = True
                break
            else:
                lst.append(x)
        i += 1
    lst.sort()
    with open("user_data/" + handle + ".pickle", "wb") as file:
        pickle.dump(lst, file)
    print("[+]", time.time() - start, "sec")
    return lst, change


if __name__ == "__main__":
    handle = "encrypted_jpg"
    # submissions = submission_scraper(handle=handle)
    # print(len(submissions))
    # updated = update_submissions(handle=handle)
    # print(len(updated))
    print(f"{bcolors.OKGREEN}[+] Data Saved to", handle + ".pickle File", bcolors.ENDC)
