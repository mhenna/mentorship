from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CycleListSerializer, CycleSerializer, DeadlineListSerializer, SkillsListSerializer, StartDateListSerializer
from rest_framework.decorators import api_view, permission_classes
from .models import Cycle, Deadline, Skill, Startdate
from django.http  import JsonResponse
from admins.permissions import IsAdmin
from django.db import IntegrityError


class CycleListCreateView(ListCreateAPIView):
    queryset = Cycle.objects.all()
  
    serializer_class = CycleSerializer
    # permission_classes = (IsAdmin,)


class CycleListView(ListAPIView):
    queryset = Cycle.objects.all()
    serializer_class = CycleSerializer
    # permission_classes = (IsAdmin,)



class SkillListCreateView(ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillsListSerializer



class AddSkill(UpdateAPIView):
    queryset= Cycle.objects.all() 
    serializer_class = CycleListSerializer
    # permission_classes = (IsAdmin,)
    def put(self, data, format=None):
        queryset = Cycle.objects.get(id=self.request.data['id'])
        try:
            queryset.skills.add(self.request.data['skill'])
        except IntegrityError as e:
            print(e)
            return Response({'message':'Skill already exists'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'message':'Something went wrong.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_200_OK)

class AddDeadline(ListCreateAPIView):
    queryset = Deadline.objects.all()
    serializer_class= DeadlineListSerializer

class EditDeadline(UpdateAPIView):
    queryset = Deadline.objects.all()
    serializer_class = DeadlineListSerializer

    def put(self, data, format=None):
        try:
            queryset = Deadline.objects.get(cycle=self.request.data['cycle'])
            try:
                queryset.mentor_DeadlineRegistration = self.request.data['mentor']
                queryset.mentee_DeadlineRegistration = self.request.data['mentee']
                queryset.save(update_fields=['mentor_DeadlineRegistration','mentee_DeadlineRegistration'])
            except IntegrityError as e:
                return Response({'message':'Skill already exists'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                print (e)
                return Response({'message':'Something went wrong.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print (e)
            cycle = Cycle.objects.get(id=self.request.data['cycle'])
            create = Deadline(mentor_DeadlineRegistration = self.request.data['mentor'], mentee_DeadlineRegistration = self.request.data['mentee'], cycle = cycle)
            create.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK)

class AddStartDate(ListCreateAPIView):
    queryset = Startdate.objects.all()
    serializer_class = StartDateListSerializer

class EditStartDate(UpdateAPIView):
    queryset = Startdate.objects.all()
    serializer_class = StartDateListSerializer

    def put(self, data, format=None):
        try:
            queryset = Startdate.objects.get(cycle=self.request.data['cycle'])
            try:
                queryset.mentor_StartRegistration = self.request.data['mentor']
                queryset.mentee_StartRegistration = self.request.data['mentee']
                queryset.save(update_fields=['mentor_StartRegistration','mentee_StartRegistration'])
            except IntegrityError as e:
                return Response({'message':'Skill already exists'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                print (e)
                return Response({'message':'Something went wrong.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print (e)
            cycle = Cycle.objects.get(id=self.request.data['cycle'])
            create = Startdate(mentor_StartRegistration = self.request.data['mentor'], mentee_StartRegistration = self.request.data['mentee'], cycle = cycle)
            create.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK)

class CycleEditView(APIView):

    @api_view(['DELETE'])
    @permission_classes([IsAdmin])
    def DeleteCycle(request):
        queryset = Cycle.objects.all()
        queryset = queryset.filter(id=request.data['id'])
        try:
            queryset.delete()
        except Exception as e:
            return Response({'message':'Something went wrong.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_204_NO_CONTENT)

class EditCycle(UpdateAPIView):
    queryset = Cycle.objects.all()
    serializer_class = CycleListSerializer

    def put(self, data, format=None):
        queryset = Cycle.objects.get(id=self.request.data['id'])
        try:
            queryset.start_date = self.request.data['start_date']
            queryset.end_date = self.request.data['end_date']
            queryset.name = self.request.data['name']
            queryset.save(update_fields=['start_date','end_date', 'name'])
        except IntegrityError as e:
            return Response({'message':'Something went wrong.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print (e)
            return Response({'message':'Something went wrong.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_200_OK)

class CycleRetrieveView(RetrieveAPIView):
    queryset = Cycle.objects.all()
    serializer_class = CycleSerializer
    # permission_classes = (IsAdmin,)
  

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())
        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        queryset = queryset.filter(**filter_kwargs)
        if not queryset:
            raise Http404('Not found.')
        queryset = queryset.prefetch_related('employee')
        obj = queryset[0]
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj