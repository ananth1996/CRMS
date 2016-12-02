from django.contrib import admin
from log.models import Student, Faculty, Department,UserProfile
# Register your models here.
admin.site.register(Department)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(UserProfile)
