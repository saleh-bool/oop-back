from main.pagination import CustomPageNumberPagination
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from main.serializers import *
from core.models import *
from datetime import datetime, date, timedelta
from django.db.models import Q
from django.contrib.auth import get_user_model
from main.send_mail import send_mail
import globals

User = get_user_model()


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    @action(detail=True, methods=['get'],)   
    def service(self, request, pk):
        service = Service.objects.get(pk=pk)
        shifts = service.shift_set.filter(start_date__gte=datetime.now()).order_by('-start_date')

        page = self.paginate_queryset(shifts)
        if page is not None:
            serializer = ShiftSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ShiftSerializer(shifts, many=True)
        return Response(serializer.data)
        
            

    @action(detail=True, methods=['get'], url_path='free_time/(?P<serv_id>\w+)')   
    def free_time(self, request, pk, serv_id):
        shift = Shift.objects.get(pk=pk)
        service = Service.objects.get(pk=serv_id)
        reserved = Reservation.objects.filter(shift=shift).order_by('time_date')
        startAvailable = shift.start_date
        available_times = []
        if reserved:
            for reservation in reserved:
                difft = reservation.time_date - startAvailable
                if difft.seconds >= service.duration.seconds:
                    x = startAvailable
                    while reservation.time_date >= x+service.duration:
                        available_times.append({'start': x})
                        x = x+service.duration
                startAvailable = reservation.time_date + reservation.service.duration
        x = startAvailable
        while x+service.duration <= shift.end_date:
            available_times.append({'start': x}) 
            x = x + service.duration
      
        return Response(available_times)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        super().destroy(request)
        return Response({"msg": "deleted"})
            
    def get_queryset(self):
        return self.queryset.filter(reserver = self.request.user)

    def perform_create(self, serializer):
        t= serializer.save(reserver = self.request.user)

        return t


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]