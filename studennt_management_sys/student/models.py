from django.db import models

class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Block(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Village(models.Model):
    name = models.CharField(max_length=100)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Program(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    program = models.CharField(max_length=100)
    block = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    enrollment_number = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        if not self.pk:
           
            last_student = Student.objects.order_by('-enrollment_number').first()
            if last_student:
                self.enrollment_number = last_student.enrollment_number + 1
            else:
                self.enrollment_number = 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.enrollment_number} {self.first_name} {self.last_name}"
    
    


