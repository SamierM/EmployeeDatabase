from django.urls import path
from . import views

app_name = 'pewad'
urlpatterns = [
    # ex: /pewad/
    path('', views.index, name='index'),
    path('data', views.tableData, name='loadtable'),

    # ex: /pewad/employee/list
    path('employee/list', views.empList, name='employeelist'),
    # ex: /pewad/employee/4
    path('employee/<int:emp_id>/', views.empDetails, name='employee'),
    # ex: /pewad/employee/4/records
    path('employee/<int:emp_id>/records', views.jsonRecordsForEmp, name='employeerecords'),
    # ex: /pewad/employee/4/update
    path('employee/<int:emp_id>/update', views.empUpdate, name='employeeupdate'),
    
    # ex: /pewad/contract/list
    path('contract/list', views.ContractListView.as_view(), name='contractlist'),
    # ex: /pewad/contract/12
    path('contract/<int:pk>/', views.ContractDetailView.as_view(), name='contract'),
    
    # ex: /pewad/project/list
    path('project/list', views.ProjectListView.as_view(), name='projectlist'),
    # ex: /pewad/project/42
    path('project/<int:proj_id>/', views.projDetails, name='project'),
]
