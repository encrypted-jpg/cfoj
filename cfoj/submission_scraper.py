import pickle
import requests
from bs4 import BeautifulSoup
from problem_scraper import Contest, Problem, bcolors
import concurrent.futures
import time


class Submission:
    def __init__(self, url, time, user, problem, verdict):
        self.url = url
        self.user = user
        self.time = time
        self.problem = problem
        self.verdict = verdict

    def __str__(self):
        ptr = "Submission URL: " + self.url + "\n"
        ptr += "User: " + self.user + "\n"
        ptr += "Time: " + self.time + "\n"
        ptr += "Problem: " + self.problem + "\n"
        ptr += "Verdict: " + self.verdict + "\n"
        return ptr


def submission_scraper(handle):
    url = "https://codeforces.com/submissions/" + handle + "/page/1"
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")
    divs = soup.find_all('div', {'class': 'pagination'})[-1]
    spans = divs.find_all('span', {'class': 'page-index'})
    n = []
    for x in spans:
        n.append(int(x.text.strip()))
    n = max(n)
    n = min(n, 10)
    submissions = []
    for i in range(1, n + 1):
        url = "https://codeforces.com/submissions/" + handle + "/page/" + str(i)
        print("[+] Fetching Submissions from URL...." + url)
        try:
            data = requests.get(url)
            soup = BeautifulSoup(data.text, "html.parser")
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
                suser = td[2].text.strip().replace('#', '')
                sproblem = td[3].find("a").get("href")
                sjudge = td[5].text.strip()
                if sjudge == "Accepted" and suser == handle:
                    submissions.append(
                        Submission(base_url + slink, stime, suser, base_url + sproblem, sjudge)
                    )
            print(f"{bcolors.OKGREEN}[+] Success....{bcolors.ENDC}")
        except Exception as e:
            print(e)
            print(f"{bcolors.FAIL} [-] Fetching Submissions from URL Failed...." + url, bcolors.ENDC)
            if not submissions:
                return []
    file = open("user_data/" + handle + ".pickle", "wb")
    pickle.dump(submissions, file)
    file.close()
    return submissions


def operation(url):
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
            suser = td[2].text.strip().replace('#', '')
            sproblem = td[3].find("a").get("href")
            sjudge = td[5].text.strip()
            if sjudge == "Accepted" and suser == handle:
                submissions.append(
                    Submission(base_url + slink, stime, suser, base_url + sproblem, sjudge)
                )
        print(f"{bcolors.OKGREEN}[+] Success....{bcolors.ENDC}")
    except Exception as e:
        raise e
    return submissions


def optimized_submission_scraper(handle):
    url = "https://codeforces.com/submissions/" + handle + "/page/1"
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")
    divs = soup.find_all('div', {'class': 'pagination'})[-1]
    spans = divs.find_all('span', {'class': 'page-index'})
    n = []
    for x in spans:
        n.append(int(x.text.strip()))
    n = max(n)
    submissions = []
    URLS = ["https://codeforces.com/submissions/" + handle + "/page/" + str(i) for i in range(1, n+1)]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(operation, url): url for url in URLS}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                submissions += future.result()
            except Exception as exc:
                print(exc)
                print(f"{bcolors.FAIL} [-] Fetching Submissions from URL Failed...." + url, bcolors.ENDC)
    file = open("user_data/" + handle + ".pickle", "wb")
    pickle.dump(submissions, file)
    file.close()
    return submissions


if __name__ == "__main__":
    handle = "Um_nik"
    start = time.time()
    # submissions = submission_scraper(handle=handle)
    submissions = optimized_submission_scraper(handle=handle)
    print(len(submissions), "Submissions Extracted....")
    print(time.time() - start, "sec....")
    print(f"{bcolors.OKGREEN}[+] Data Saved to", handle + ".pickle File", bcolors.ENDC)
