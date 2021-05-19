import pickle

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
import submission_scraper
from submission_scraper import submission_scraper, update_submissions, Submission
from json import JSONEncoder, JSONDecoder
import json
import datetime


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def datetime_option(value):
    if isinstance(value, datetime.date):
        return value.timestamp()
    else:
        return value.__dict__


def handle_data(request):
    if request.POST.get("handle") is not None:
        handle = request.POST.get("handle")
        try:
            logout(request)
            user = authenticate(request, username=handle, password="1")
            if user is not None:
                submissions = update_submissions(handle=handle)
                login(request, user)
            else:
                submissions = submission_scraper(handle=handle)
                if not submissions:
                    raise Exception
                User.objects.create(username=handle, password="1")
                user = User.objects.get(username=handle)
                user.set_password("1")
                user.save()
                login(request, user)
            head = "Hello, " + handle
            status = True
        except Exception as e:
            print(e)
            head = "Invalid Handle!! Enter Valid Handle.."
            status = False
    data = {
        "head": head,
        "success": status
    }
    return JsonResponse(data)


def update_handle(request):
    tag = request.POST.get("tag")
    tag = tag.replace("Tag:", "").strip()
    with open("data/tag_sorted_dict.pickle", "rb") as file:
        tag_dict = pickle.load(file)
    lst = tag_dict[tag]
    tag_lst = list(zip(list(range(1, len(lst) + 1)), lst))
    handle = request.POST.get("handle")
    submissions, change = update_submissions(handle=handle)
    if not change:
        data = {
            "change": False
        }
        return JsonResponse(data)
    plist = tag_lst.copy()
    tag_lst = []
    for i, x in plist:
        done = False
        for sub in submissions:
            if x.url == sub.problem:
                tag_lst.append((i, x, sub))
                done = True
                break
        if not done:
            tag_lst.append((i, x, None))
    data = {
        "tag_lst": tag_lst,
    }
    data = json.dumps(data, cls=MyEncoder, default=datetime_option)
    return JsonResponse(json.loads(data))


def index(request):
    head = "Enter CodeForces Handle to View Submissions"
    if request.user.username is not None and request.user.username != "":
        handle = request.user.username
        head = "Hello, " + handle
    context = {
        "handle": head,
    }
    return render(request, "homepage.html", context=context)


def tag_problem(request, tag_dict, tag):
    lst = tag_dict[tag]
    lst.sort()
    tag_lst = list(zip(list(range(1, len(lst) + 1)), lst))
    head = "Enter CodeForces Handle to View Submissions"
    if request.POST.get("handle") is not None:
        handle = request.POST.get("handle")
        try:
            logout(request)
            submissions = submission_scraper(handle=handle)
            if not submissions:
                raise Exception
            head = "Hello, " + handle
            user = authenticate(request, username=handle, password="1")
            if user is not None:
                login(request, user)
            else:
                User.objects.create(username=handle, password="1")
                user = User.objects.get(username=handle)
                user.set_password("1")
                user.save()
                login(request, user)
        except Exception as e:
            print(e)
            head = "Invalid Handle!! Enter Valid Handle.."
    if request.user.username is not None and request.user.username != "":
        handle = request.POST.get("handle") if request.POST.get("handle") is not None else request.user.username
        head = "Hello, " + handle
        with open("user_data/" + handle + ".pickle", "rb") as file:
            submissions = pickle.load(file)
        plist = tag_lst.copy()
        tag_lst = []
        for i, x in plist:
            done = False
            for sub in submissions:
                if x.url == sub.problem:
                    tag_lst.append((i, x, sub))
                    done = True
                    break
            if not done:
                tag_lst.append((i, x, None))
        context = {
            "handle": head,
            "handle_name": handle,
            "head": "Tag: " + tag,
            "table_head": ("S.No", "Problem Name", "ID", "No. of Submissions", "Your Submission"),
            "tag_lst": tag_lst,
        }
    else:
        context = {
            "handle": head,
            "handle_name": "",
            "head": "Tag: " + tag,
            "table_head": ("S.No", "Problem Name", "ID", "Number of Submissions"),
            "tag_lst": tag_lst,
        }
    return render(request, "problems.html", context=context)


def categories(request):
    with open("data/tag_sorted_dict.pickle", "rb") as file:
        tag_dict = pickle.load(file)
    if request.GET.get("tag") is not None:
        return tag_problem(request, tag_dict, request.GET.get("tag"))
    lst = []
    i = 1
    for key, value in tag_dict.items():
        lst.append((i, key, len(value)))
        i += 1
    head = "Enter CodeForces Handle to View Submissions"
    if request.POST.get("handle") is not None:
        handle = request.POST.get("handle")
        try:
            logout(request)
            submissions = submission_scraper(handle=handle)
            if not submissions:
                raise Exception
            head = "Hello, " + handle
            user = authenticate(request, username=handle, password="1")
            if user is not None:
                login(request, user)
            else:
                User.objects.create(username=handle, password="1")
                user = User.objects.get(username=handle)
                user.set_password("1")
                user.save()
                login(request, user)
        except Exception as e:
            print(e)
            head = "Invalid Handle!! Enter Valid Handle.."
    if request.user.username is not None and request.user.username != "":
        handle = request.user.username
        head = "Hello, " + handle
    context = {
        "handle": head,
        "head": "Categories",
        "table_head": ("S.No", "Category Name", "Number of Problems"),
        "tag_lst": lst,
    }
    return render(request, "categories.html", context=context)
