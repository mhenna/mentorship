from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import LoginSerializer, RegisterationSerializer
from users.serializers import CreateUserSerializer


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


class AdminView(APIView)

    @api_view(['POST'])
    @permission_classes([IsAdmin])
    def invite(request):
        data = {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'email': request.data.get('email'),
            'is_Mentor': True
        }
        serializer = CreateUserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            template = Template(
                '<p>You have been invited as a Mentor at ' +
                'Dell Mentorship Program. ' +
                'Please sign-up using the following ' +
                '<a href="{{loginUrl}}">link</a>.')
            context = Context(
                {'loginUrl': settings.Mentor_URL,
                 })
            body = template.render(context)
            emailMessage = EmailMessage('Dell Mentorship Portal', body,
                                        'mentorship@dell.com',
                                        [request.data.get('email')])
            emailMessage.content_subtype = "html"
            emailMessage.send()
            if request.data.get('is_Mentor') == True:
                return Response({'detail': 'Mentor has been invited.'},
                            status=status.HTTP_200_OK)
           
        except SMTPException:
            return Response({'detail': 'Internal Server Error.'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)
 