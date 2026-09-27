from django.db import models


class Employee(models.Model):
    empid = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    salary = models.CharField(max_length=10)
    address = models.TextField()
    picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}-{self.empid}"