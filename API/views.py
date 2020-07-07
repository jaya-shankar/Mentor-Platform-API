from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers


from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.renderers import JSONRenderer


from .models import Course,Chats, Doubts

from .serializers import GroupNameSerializer,CourseSerializer,UsersSerializer,UserSerializer,ChatSerializer,RegistrationSerializer
from .serializers import DoubtsSerializer,NewCourseSerializer,MessageSerializer, AskDoubtSerializer
# Create your views here.


class get_all_groups_view(generics.ListAPIView):
    """
    GET all courses
    """
    queryset=Course.objects
    serializer_class = GroupNameSerializer

    def get(self,request,*args, **kwargs):
        return Response(GroupNameSerializer(self.queryset.all(),many=True).data)
    


class get_course_info_view(generics.ListAPIView):
    """
    GET course info
    """
    queryset=Course.objects.all()

    def get(self,request,*args, **kwargs):
        course=valdiate_course(kwargs)
        if(not course):
            return Response(
                data={
                    "message": "Course does not exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        else:
            return Response(CourseSerializer(course).data)

class get_users_view(generics.ListAPIView):
    """
    GET all users
    """

    queryset=User.objects.all()
    serializer_class = UsersSerializer


class get_user_info_view(generics.ListAPIView):
    """
    GET user info
    """

    queryset=User.objects.all()
    courses=Course.objects.all()
   
    def get(self,request,*args, **kwargs):
        user = valdiate_user(kwargs)
        if(not user):
            return Response(
                data={
                    "message": "User does not exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(UserSerializer(user).data)
        
class get_messages_view(generics.ListAPIView):

    queryset=Chats.objects.all()
    serializer_class=ChatSerializer
    
    def get(self,request,*args,**kwargs):
        course=valdiate_course(kwargs)
        if(not course):
            return Response(
                data={
                    "message": "Course does not exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        chat=self.queryset.filter(course=course)
        return Response(ChatSerializer(chat,many=True).data)

    serializer_class=MessageSerializer
    def post(self,request,*args,**kwargs):

        course=valdiate_course(kwargs)
        if(not course):
            return Response(
                data={
                    "message": "Course does not exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        if(course.creator!=request.user):
            return Response(
                data={
                    "message": "Only creator of the groups can post message"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        message=request.data.get("message")
        image=request.data.get("image")
        chat = Chats(course=course,message=message,image=image)
        chat.save()
        chats=self.queryset.filter(course=course)
        
        return Response(ChatSerializer(chats,many=True).data, status=status.HTTP_201_CREATED)

        

    


class RegisterUsers_view(generics.CreateAPIView):
    """
    POST register new users
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateGroup(generics.CreateAPIView):
    """
    POST create new groups
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class=NewCourseSerializer
    def post(self, request, *args, **kwargs):
        course_details=dict(request.data)
        del course_details['csrfmiddlewaretoken']
        course_details['creator']=request.user
        course=Course.create(course_details)
        #course.add_details(course_details)
        course.save()
        return Response(CourseSerializer(course).data, status=status.HTTP_201_CREATED)
        

class get_doubts_user_view(generics.CreateAPIView):
    queryset = Doubts.objects.all()
    serializer_class = DoubtsSerializer

    def get(self,request,*args,**kwargs):
        user = valdiate_user(kwargs)
        if(not user):
            return Response(
                data={
                    "message": "User does not exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        doubts=self.queryset.filter(sender=user)
        return Response(DoubtsSerializer(doubts,many=True).data)


class get_doubts_course_view(generics.CreateAPIView):
    queryset = Doubts.objects.all()
    serializer_class = DoubtsSerializer

    def get(self,request,*args,**kwargs):
        course = valdiate_course(kwargs)
        if(not course):
            return Response(
                data={
                    "message": "Course does not exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        doubts=self.queryset.all().filter(course=course)
        return Response(DoubtsSerializer(doubts,many=True).data,)

    serializer_class = AskDoubtSerializer

    def post(self,request,*args,**kwargs):
        course=valdiate_course(kwargs)
        if(not course):
            return Response(
                data={
                    "message": "Course does not exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        new_doubt = Doubts.create(request.user,course,request.data["message"])
        new_doubt.save()
        doubts=self.queryset.all().filter(course=course)
        return Response(DoubtsSerializer(doubts,many=True).data,)

    
def valdiate_course(kwargs):
    print(kwargs)
    print(kwargs["id"])
    try:
        a_course = Course.objects.get(pk=(kwargs["id"]))
        return a_course
    except KeyError:
        a_course = Course.objects.get(title=kwargs["name"])
        return a_course
        
    except Course.DoesNotExist:
        return None

def valdiate_user(kwargs):
    try:
         user = User.objects.get(pk=int(kwargs["id"]))
    except KeyError:
        user = User.objects.get(username=kwargs["name"])
    except User.DoesNotExist:
        return None
    return user
