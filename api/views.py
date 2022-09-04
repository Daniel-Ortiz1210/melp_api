from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Restaurant
from django.shortcuts import get_object_or_404
from .serializers import RestaurantSerializer
from django.db import connection



class RestaurantDetailView(APIView):
    def get(self, request, id):
        obj = get_object_or_404(Restaurant, id=id)
        serializer = RestaurantSerializer(obj, many=False)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        obj = get_object_or_404(Restaurant, id=id)
        obj.delete()
        return Response(status=status.HTTP_200_OK)
    
    def put(self, request, id):
        obj = get_object_or_404(Restaurant, id=id)
        serializer = RestaurantSerializer(obj, request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, id):
        obj = get_object_or_404(Restaurant, id=id)
        serializer = RestaurantSerializer(obj, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)



class RestaurantsView(APIView):
    def get(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)



class StatisticsView(APIView):

    def get(self, request):
        
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')
        radius = request.query_params.get('radius')
        
        if None in [latitude, radius, longitude]:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(*) as total, AVG(rating) as rating, STDDEV(rating) as std_dev from api_restaurant as coor WHERE ST_Covers(ST_Buffer(ST_Point(%s, %s)::geography, %s), ST_Point(coor.lng, coor.lat)::geography);', [float(longitude), float(latitude), float(radius)])
        row = cursor.fetchone()

        ret = {
            'count': row[0],
            'avg': row[1],
            'std': row[2]
        }


        return Response(ret, status=status.HTTP_200_OK)