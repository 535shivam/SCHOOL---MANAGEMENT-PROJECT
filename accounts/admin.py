from django.contrib import admin
from .models import (
    Profile,
    StudentInfoModel,
    TeacherInfoModel,
    ClassRoomModel,
    StudentMarksModel,
    AttendanceModel,
    AssignmentModel,
    StudentNoticeModel,
    GeneralNoticeModel,
)

admin.site.register(Profile)
admin.site.register(StudentInfoModel)
admin.site.register(TeacherInfoModel)
admin.site.register(ClassRoomModel)
admin.site.register(StudentMarksModel)
admin.site.register(AttendanceModel)
admin.site.register(AssignmentModel)
admin.site.register(StudentNoticeModel)
admin.site.register(GeneralNoticeModel)