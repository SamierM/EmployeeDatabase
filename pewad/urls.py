from django.urls import path
from . import views

app_name = 'pewad'
urlpatterns = [
    # ex: /pewad/ -- List of all Work Records
    path('', views.index, name='index'),
    # ex: /pewad/data -- List of all Work Records (table data call)
    path('data', views.index_json_table_data, name='loadtable'),

    # ex: /pewad/employee/list -- List of all employees
    path('employee/list', views.employee_list, name='employeelist'),
    # ex: /pewad/employee/list/data -- List of all employees (table data call)
    path('employee/list/data', views.employee_json_table_data,
         name='employeelistdata'),
    # ex: /pewad/employee/4 -- Detail/Update view of a single employee
    path('employee/<int:pk>/', views.EmployeeUpdateView.as_view(), name='employee'),
    # ex: /pewad/employee/4/records -- Detail/Update view of a single employee (table data call)
    path('employee/<int:emp_id>/records',
         views.employee_json_records, name='employeerecords'),

    # ex: /pewad/contract/list
    path('contract/list', views.ContractListView.as_view(), name='contractlist'),
    # ex: /pewad/contract/12
    path('contract/<int:pk>/', views.ContractDetailView.as_view(), name='contract'),

    # ex: /pewad/project/list
    path('project/list', views.ProjectListView.as_view(), name='projectlist'),
    # ex: /pewad/project/42
    path('project/<int:proj_id>/', views.projDetails, name='project'),
]
