from django.contrib import admin
from .models import WorkRecord, Contract, Project, Employee

admin.site.site_header = "PEWAD Administration"
admin.site.site_url = "/pewad/"


class WorkRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'emp', 'hours', 'proj', 'cont', 'lead')
    search_fields = ['task']
    list_filter = ['emp', 'proj', 'cont']


admin.site.register(WorkRecord, WorkRecordAdmin)
admin.site.register(Contract)
admin.site.register(Project)
admin.site.register(Employee)
