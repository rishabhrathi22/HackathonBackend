from django.db import models

# Create your models here.
class Chat(models.Model):
    student_email  = models.EmailField()
    classroom_id = models.IntegerField()
    conversation = models.TextField()
    last_msg = models.CharField(max_length=10)

    def __str__(self):
        return self.student_email + ' classroomID: ' + str(self.classroom_id)   


    