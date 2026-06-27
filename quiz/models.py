from django.db import models

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.TextField()

    def __str__(self):
        return self.question[:50]
class Option(models.Model):
    question = models.ForeignKey(Question, related_name="options", on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.option_text 