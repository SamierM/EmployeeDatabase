from django.urls import path
from . import views

app_name = 'employd'
urlpatterns = [
    # ex: /employd/ -- List of all Work Records
    path('', views.index, name='index'),
    # ex: /employd/data -- List of all Work Records (table data call)
    path('data', views.index_json_table_data, name='loadtable'),
    # ex: /employd/wr/12 -- Update a WorkRecord
    path('wr/<int:pk>/', views.WorkRecordUpdateView.as_view(),
         name='workrecordupdate'),
    # ex: /employd/wr/create -- Create a new WorkRecord
    path('wr/create', views.WorkRecordCreate.as_view(), name='workrecordcreate'),
    # ex: /employd/wr/delete -- Delete an existing WorkRecord
    path('wr/<int:pk>/delete', views.WorkRecordDelete.as_view(), name='workrecorddelete'),

    # ex: /lead/emailall -- Send emails to all Leads with team tasking breakdowns
    path('lead/emailall', views.email_all_leads, name='leademailall'),

    # ex: /employd/employee/list -- List of all employees
    path('employee/list', views.employee_list, name='employeelist'),
    # ex: /employd/employee/list/data -- List of all employees (table data call)
    path('employee/list/data', views.employee_json_table_data,
         name='employeelistdata'),
    # ex: /employd/employee/4 -- Detail/Update view of a single employee
    path('employee/<int:pk>/', views.EmployeeUpdateView.as_view(), name='employee'),
    # ex: /employd/employee/4/records -- Detail/Update view of a single employee (table data call)
    path('employee/<int:emp_id>/records',
         views.employee_json_records, name='employeerecords'),
    # ex: /employd/employee/4/email -- Sends an email to the employee with a WorkRecord table
    path('employee/<int:pk>/email',
         views.email_single_employee, name='employeeemail'),
    # ex: /employd/employee/emailall -- Sends emails to all employee with a WorkRecord table
    path('employee/emailall',
         views.email_all_employees, name='employeeemailall'),
    # ex: /employd/employee/create -- Create a new Employee
    path('employee/create', views.EmployeeCreate.as_view(), name='employeecreate'),

    # ex: /employd/contract/list -- List of all contracts
    path('contract/list', views.contract_list, name='contractlist'),
    # ex: /employd/contract/list/data -- List of all contracts (table data call)
    path('contract/list/data', views.contract_json_table_data,
         name="contractlistdata"),
    # ex: /employd/contract/12 -- Detail/Update view of a single contract
    path('contract/<int:pk>/', views.ContractUpdateView.as_view(), name='contract'),
    # ex: /employd/contract/12/records -- Detail/Update view of a single contract (table data call)
    path('contract/<int:pk>/records',
         views.contact_json_records, name='contractrecords'),

    # ex: /employd/project/list -- List of all projects
    path('project/list', views.project_list, name='projectlist'),
    # ex: /employd/project/list/data -- List of all projects (table data call)
    path('project/list/data', views.project_json_table_data,
         name="projectlistdata"),
    # ex: /employd/project/12 -- Detail/Update view of a single project
    path('project/<int:pk>/', views.ProjectUpdateView.as_view(), name='project'),
    # ex: /employd/project/12/records -- Detail/Update view of a single project (table data call)
    path('project/<int:pk>/records',
         views.contact_json_records, name='projectrecords'),
]
