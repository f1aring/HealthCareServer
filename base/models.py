from django.db import models

class Note(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title  # Return the title or another suitable attribute


class Doctor(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    occupation = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    rating = models.IntegerField()

    def __str__(self):
        return self.name  # Return the doctor's name or another suitable attribute
    

class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day = models.CharField(max_length=200)
    time = models.TimeField()

    def __str__(self):
        return f"{self.doctor.name} - {self.day}"
    


class Doctor_Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day = models.CharField(max_length=200)
    time = models.TimeField()

    def __str__(self):
        return f"{self.doctor.name} - {self.day}"
    
