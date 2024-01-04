import requests
import json

from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny

from django.contrib.auth.models import User


@api_view(["POST"])
@permission_classes([AllowAny])
def create(request):
    email=request.data['email']
    password=request.data['password']
    first_name=request.data['first_name']
    last_name=request.data['last_name']
    print(email)

    if not User.objects.filter(username=email).exists():
        User.objects.create_user(
            username=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        headers={
            "Content-Type":"application/json",
        }
        data={
            "username":email,
            "password":password,
        }

        protocol="http://"
        if request.is_secure():
            protocol="https://"

        host=request.get_host()

        url=protocol+host+"/api/v1/auth/token/"
        response=requests.post(url,headers=headers,data=json.dumps(data))

        if response.status_code==200:
            response_data={
                "status":6000,
                "data":response.json(),
                "message":"Account created"
            }
        else:
            response_data={
                "status":6001,
                "data":"An error occured"
            }
    else:
        response_data={
            "status":6001,
            "data":"User already exists"
        }
    return Response(response_data)