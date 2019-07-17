from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from smtplib import SMTPException
from rest_framework.views import APIView
from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.template import Context, Template

from .serializers import LoginSerializer, RegisterationSerializer
from users.models import Employee
from .permissions import IsAdmin

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterationSerializer


class LoginView(CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminView(APIView):

    @api_view(['POST'])
    @permission_classes([IsAdmin])
    def invite(request):
       
        try:
            template = Template(
                '<p>You have been invited as a Mentor at ' +
                'Dell Mentorship Program. ' +
                'Please sign-up using the following ' +
                '<a href="{{loginUrl}}">link</a>.')
            context = Context(
                {'loginUrl': settings.MENTOR_URL,
                 })
            body = template.render(context)
            emailMessage = EmailMessage('Dell Mentorship Portal', body,
                                        to=[request.data.get('email')])
            emailMessage.content_subtype = "html"
            emailMessage.send()
            
            return Response({'detail': 'Mentor has been invited.'},
                            status=status.HTTP_200_OK)
           
        except SMTPException:
            return Response({'detail': 'Internal Server Error.'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)

    @api_view(['DELETE'])
    def delete(request):
        try:
            print("In delete", request.data['id'])
            # queryset = Employee.objects.all()
            # queryset = queryset.filter(id=request.data['id'])
            queryset = Employee.objects.get(id=request.data['id'])
            print("This is the user" , queryset)
            queryset.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response({'detail': 'Failed to delete user'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)


    @api_view(['POST'])
    @permission_classes([IsAdmin])
    def SendEmail(request):
        try:
            mentors = Employee.objects.filter(is_mentor=True)
            mentees = Employee.objects.filter(is_mentor=False)
            emails = request.data.get('email')
            email_list = emails.split(",")
            print("###############################", email_list)
            sending_list = []
            body = request.data.get('emailBody')
           # template = Template(
            #    '<p>{{body}}</p>')
            #context = Context(
             #   {'body': request.data.get('emailBody'),
              #   })
            #body = template.render(context)
            if (request.data.get('type')=='mentors'):
                for email in mentors:
                    sending_list.append(email.email)
                emailMessage = EmailMessage('Dell Mentorship Portal', body,
                                            to=sending_list)
                print('$$$$$$$$$$$$$$$$', sending_list, ' ', body)
            if (request.data.get('type')=='mentees'):
                for email in mentees:
                    sending_list.append(email.email)
                emailMessage = EmailMessage('Dell Mentorship Portal', body,
                                            to=sending_list)
                print('*****************', sending_list, ' ', body)
            if (request.data.get('type')=='seperate'):
                emailMessage = EmailMessage('Dell Mentorship Portal', body,
                                        to=email_list)
                print(request.data)
                print(request.data.get('emailBody'))
            #emailMessage.content_subtype = "html"
            emailMessage.send()
            
            return Response({'detail': 'Email sent'},
                            status=status.HTTP_200_OK)
           
        except SMTPException:
            return Response({'detail': 'Internal Server Error.'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)

