from django.db import models


# Create your models here.
class Classes(models.Model):
    caption = models.CharField(max_length=64)


class Teacher(models.Model):
    name = models.CharField(max_length=32)
    cls = models.ForeignKey('Classes')  # 如果Classes在后面定义需要使用'Classes'


class Student(models.Model):
    name = models.CharField(max_length=32)
    cls = models.ForeignKey('Classes')


class Administrator(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
