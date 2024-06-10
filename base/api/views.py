from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import NoteSerializer
from .serializers import DoctorSerializer
from .serializers import DoctorScheduleSerializer
from base.models import Doctor_Schedule, Note
from base.models import Doctor, DoctorSchedule
from rest_framework import status
from datetime import datetime, timedelta

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getNotes(request):
    user = request.user
    notes = user.note_set.all().order_by('-created_date')
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def getPostDoctorList(request):
    if request.method == 'GET':
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getDoctor(request, pk):
    try:
        print(pk)
        doctor = Doctor.objects.get(id=pk)
    except Doctor.DoesNotExist:
        return Response({'error': 'Doctor not found'}, status=404)
    
    serializer = DoctorSerializer(doctor, many=False)
    return Response(serializer.data)





@api_view(['POST'])
def postDoctorSchedule(request):
    # Get data from the request body
    data = request.data
    doctor_id = data.get('doctor_id')
    days = data.get('day', [])
    times = data.get('time', [])

    if doctor_id is None:
        return Response({'error': 'Doctor_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    if not days:
        return Response({'error': 'At least one day is required'}, status=status.HTTP_400_BAD_REQUEST)

    if not times:
        return Response({'error': 'At least one time slot is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

    schedule_objects = []
    for day in days:
        for time_str in times:
            try:
                # Parse the time
                time = datetime.strptime(time_str, '%I:%M %p').time()

                # Create a DoctorSchedule instance
                schedule = Doctor_Schedule(
                    doctor=doctor,
                    day=day,
                    time=time
                )
                schedule_objects.append(schedule)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Bulk create all the schedules
    Doctor_Schedule.objects.bulk_create(schedule_objects)

    # Serialize the created objects
    serializer = DoctorScheduleSerializer(schedule_objects, many=True)
    return Response({'message': 'Doctor schedules created successfully', 'schedules': serializer.data}, status=status.HTTP_201_CREATED)
    # Get data from the request body
   


@api_view(['GET'])
def getDoctorSchedule(request, doctor_id):
    if doctor_id is None:
        return Response({'error': 'Doctor_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    schedules = Doctor_Schedule.objects.filter(doctor_id=doctor_id)
    serializer = DoctorScheduleSerializer(schedules, many=True)

    list = []
    for schedule in schedules:
        list.append(schedule.day)
    days_list = set(list)

    return Response({'schedules': serializer.data, 'day': days_list})



@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh'
    ]
    return Response(routes)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        
        # ...

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer