from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from snippets.models import Users, UsersLocation
from snippets.serializers import UserSerializer, LocationSerializer
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.permissions import IsAdminUser
from snippets.predict import prediction
from django.contrib.auth import logout

renderer_classes = [TemplateHTMLRenderer]
template_name = 'index.html'


def index(request):
    # logout(request)
    # print(request.user)
    user = request.user
    print(user)
    if user.is_authenticated:
        location_object = UsersLocation.objects.get(account=user)
        test_list = []
        test_list.append(location_object.location_1)
        test_list.append(location_object.location_2)
        test_list.append(location_object.location_3)
        test_list.append(location_object.location_4)
        test_list.append(location_object.location_5)
        context = {'test_list': test_list, 'username': user}
        return render(request, 'snippets/index.html', context)
    test_list = Users.objects.all()
    # context = {'test_list': test_list}
    return render(request, 'snippets/index.html')


def login(request):
    print(request.user)
    logout(request)
    test_list = Users.objects.all()
    context = {'test_list': test_list}
    return render(request, 'snippets/login.html', context)


def test(request):
    return render(request, 'snippets/location.html')


def result(name):
    test_list = Users.objects.all()
    context = {'test_list': test_list}
    # location_data_save = ['us', 'de', 'fr', 'ot', 'au']
    location_data_save = prediction()
    print(location_data_save)
    serializer_loc = LocationSerializer(
        data={'account': name, 'location_1': location_data_save[0], 'location_2': location_data_save[1],
              'location_3': location_data_save[2], 'location_4': location_data_save[3],
              'location_5': location_data_save[4]})
    if serializer_loc.is_valid():
        serializer_loc.save()
        return True
    return False


class UserList(generics.ListCreateAPIView):
    model = Users
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def perform_create(self, serializer):
        serializer.save()
        result(self.request.data['account'])
        # print(self.request.data['account'])


class UserDetail(generics.RetrieveAPIView):
    model = Users
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'account'
    permission_classes = [
        permissions.AllowAny
    ]


class LocationDetail(generics.RetrieveAPIView):
    model = UsersLocation
    queryset = UsersLocation.objects.all()
    lookup_field = 'account'
    serializer_class = LocationSerializer
    permission_classes = [
        permissions.AllowAny
    ]


# Temporary function for demo of sprint3
# TODO: use user's authorization method and session to render index.html
# This method is to be dropped in sprint 4
def userinfo(request, account_in):
    location_object = UsersLocation.objects.get(account=account_in)
    test_list = []
    test_list.append(location_object.location_1)
    test_list.append(location_object.location_2)
    test_list.append(location_object.location_3)
    test_list.append(location_object.location_4)
    test_list.append(location_object.location_5)
    context = {'test_list': test_list, 'username': account_in}
    return render(request, 'snippets/index.html', context)
