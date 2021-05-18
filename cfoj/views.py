from django.shortcuts import render, redirect
import pickle
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from submission_scraper import submission_scraper, Submission


def handle_data(request):
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
    tag_lst = list(zip(list(range(1, len(lst)+1)), lst))
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
        file = open("user_data/" + handle + ".pickle", "rb")
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
            "head": "Tag: " + tag,
            "table_head": ("S.No", "Problem Name", "ID", "No. of Submissions", "Your Submission"),
            "tag_lst": tag_lst,
        }
    else:
        context = {
            "handle": head,
            "head": "Tag: " + tag,
            "table_head": ("S.No", "Problem Name", "ID", "Number of Submissions"),
            "tag_lst": tag_lst,
        }
    return render(request, "problems.html", context=context)


def categories(request):
    file = open("cfoj/tag_sorted_dict.pickle", "rb")
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