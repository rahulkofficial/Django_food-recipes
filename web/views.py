import requests
import json

from django.shortcuts import render
from django.urls import reverse
from django.http.response import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout


headers={
            "Content-Type":"application/json",
        }
tk={}
fvs={"fav":False}
def main(request):
    context={}
    return HttpResponseRedirect('login')


def login(request):
    if request.method=='POST':
        username=request.POST.get('email')
        password=request.POST.get('password')
        if username and password:
            data={
            "username":username,
            "password":password,
            }
            response=requests.post("http://127.0.0.1:8000/api/v1/auth/token/",headers=headers,data=json.dumps(data))
            if response.status_code==200:
                res=response.json()
                token=res["access"]
                tk["token"]=token
                user=authenticate(request,username=username,password=password)
                if user is not None:
                    auth_login(request,user)
                    return HttpResponseRedirect("recipes")
        context={
            "error":True,
            "message":"Invalid email or password"
        }
        return HttpResponse(render(request,'login.html',context=context))
    context={
        
    }
    return HttpResponse(render(request,'login.html',context=context))


def signup(request):
    if request.method=='POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('email')
        password=request.POST.get('password')
        if username and password:
            data={
            "first_name":first_name,
            "last_name":last_name,
            "email":username,
            "password":password,
            }
            response=requests.post("http://127.0.0.1:8000/api/v1/auth/create",headers=headers,data=json.dumps(data))
            res=response.json()
            if res['status']==6000:
                token=res["data"]["access"]
                tk["token"]=token
                user=authenticate(request,username=username,password=password)
                if user is not None:
                    auth_login(request,user)
                    return HttpResponseRedirect("recipes")
        context={
            "error":True,
            "message":res['data']
        }
        return HttpResponse(render(request,'signup.html',context=context))
    context={
        
    }
    return HttpResponse(render(request,'signup.html',context=context))


def recipes(request):
    headersAPI = {
        "Authorization": "Bearer "+tk["token"],
    }
    q=request.POST.get('q')
    v=request.POST.get('v')
    current_user=request.user
    user_id=current_user.id
    params={
        "q":q,
        "v":v,
    }
    response=requests.get("http://127.0.0.1:8000/api/v1/recipes",headers=headersAPI,params=params).json()
    res=requests.get("http://127.0.0.1:8000/api/v1/recipes/categories",headers=headersAPI).json()
    r=requests.get("http://127.0.0.1:8000/api/v1/recipes/fav",headers=headersAPI,).json()
    recipes=response["data"]
    categories=res["data"]
    favs=r["data"]
    rcp_id=[]
    for fav in favs:
        if fav["user"] == user_id:
            rcp_id.append(fav["recipe"])
    
    context={
        "recipes":recipes,
        "categories":categories,
        "favs":favs,
        "fav_id":rcp_id,
        "user_id":user_id,
        "fav":fvs["fav"],
    }
    return HttpResponse(render(request,'recipes.html',context=context))


def recipes_detailed(request,id):
    current_user=request.user
    user_id=current_user.id
    headersAPI = {
        "Authorization": "Bearer "+tk["token"],
    }
    url=f"http://127.0.0.1:8000/api/v1/recipes/details/{id}"
    response=requests.get(url,headers=headersAPI).json()
    recipe=response["data"]
    context={
        "recipe":recipe,
        "user_id":user_id
    }
    return HttpResponse(render(request,'recipes_detailed.html',context=context))


def add(request):
    context = {
                "token": "Bearer "+tk["token"],
            }
    return HttpResponse(render(request,'add.html',context=context))
    


def update(request,id):
    headersAPI = {
        "Authorization": "Bearer "+tk["token"],
        "Content-Type":"application/json"
    }
    url=f"http://127.0.0.1:8000/api/v1/recipes/details/{id}"
    response=requests.get(url,headers=headersAPI).json()
    recipe=response["data"]
    print(response["data"]["image"])
    if response["data"]["image"]:
        res=response["data"]["image"].split("/")
        image=res[5]
    else:
        image="No"
    context={
        "recipe":recipe,
        "token": "Bearer "+tk["token"],
        "image":image
    }
    return HttpResponse(render(request,'update.html',context=context))


def delete(request,id):
    headersAPI = {
        "Authorization": "Bearer "+tk["token"],
    }
    url=f"http://127.0.0.1:8000/api/v1/recipes/delete/{id}"
    requests.post(url,headers=headersAPI,)
    context={}
    return HttpResponseRedirect(reverse("web:recipes"))


def add_fav(request,id):
    headersAPI = {
        "Authorization": "Bearer "+tk["token"],
    }
    url=f"http://127.0.0.1:8000/api/v1/recipes/add_fav/{id}"
    requests.post(url,headers=headersAPI,)
    context={}
    return HttpResponseRedirect(reverse("web:recipes"))


def remove_fav(request,id):
    headersAPI = {
        "Authorization": "Bearer "+tk["token"],
    }
    url=f"http://127.0.0.1:8000/api/v1/recipes/remove_fav/{id}"
    requests.post(url,headers=headersAPI,)
    context={}
    return HttpResponseRedirect(reverse("web:recipes"))


def favs(request):
    fvs["fav"]= not fvs["fav"]
    return HttpResponseRedirect(reverse("web:recipes"))


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

