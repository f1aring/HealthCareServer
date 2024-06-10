from rest_framework.serializers import ModelSerializer
from base.models import Doctor_Schedule, Note, Doctor, DoctorSchedule

class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

class DoctorSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'



class DoctorScheduleSerializer(ModelSerializer):
    class Meta:
        model = Doctor_Schedule
        fields = '__all__'