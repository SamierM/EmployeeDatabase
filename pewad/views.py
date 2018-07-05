from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.contrib import messages
from django.views import generic
from django.core.mail import send_mail

from .models import Contract, Employee, Project, WorkRecord


def index(request):
    ''' Display the default PEWAD landing page'''
    context = {
        'passedValue': "TEAM",
    }
    return render(request, 'pewad/index.html', context)


def tableData(request):
    ''' GET JSON data for table view; WorkRecords '''
    dbRecs = get_list_or_404(WorkRecord)
    data = beerMeItAll(dbRecs)

    return JsonResponse(data, safe=False)


def jsonRecordsForEmp(request, emp_id):
    ''' Get the WorkRecords data in JSON for an employee '''
    records = WorkRecord.objects.filter(emp=emp_id)
    data = beerMeItAll(records)

    return JsonResponse(data, safe=False)


def empList(request):
    ''' Generic display list view showing all Employees'''
    all = get_list_or_404(Employee)

    return render(request, 'pewad/employee_list.html', {'all_items': all, 'list_title': 'Employee'})


def empDetails(request, emp_id):
    ''' Display view showing details about an Employee'''
    employee = get_object_or_404(Employee, pk=emp_id)

    return render(request, 'pewad/employee.html', {'employee': employee})


def empUpdate(request, emp_id):
    ''' POST: Update an Employee record '''
    employee = get_object_or_404(Employee, pk=emp_id)
    first = request.POST['first']
    last = request.POST['last']
    employee.fname = first
    employee.lname = last
    employee.save()

    messages.success(request, 'Update successful.')

    return HttpResponseRedirect(reverse('pewad:employee', args=(emp_id,)))


def contDetails(request, cont_id):
    response = "you looking at contract #%s"
    return HttpResponse(response % cont_id)


def projList(request):
    all = get_list_or_404(Project)

    return render(request, 'pewad/list.html', {'all_items': all, 'title': 'Project'})


def projDetails(request, proj_id):
    response = "you looking at project #%s"
    return HttpResponse(response % proj_id)


def emailEmployee(request, emp_id):
    # TODO fix or remove this
    None
    # records = WorkRecord.objects.filter(emp=emp_id)

    # send_email(
    #     'Work Assignment',  # Subject line
    #     '',  # Message body
    #     EMAIL_SENDER,  # Sender
    #     [],  # Recipient List
    #     fail_silently=False,
    # )


class ListView(generic.ListView):
    model = None
    template_name = 'pewad/list.html'
    context_object_name = 'all_items'


class ContractListView(ListView):
    # TODO how do I send this bit of data?
    # title = "Contract"

    def get_queryset(self):
        return Contract.objects.order_by('number')


class ContractDetailView(generic.DetailView):
    model = Contract
    template_name = 'pewad/contract_detail.html'


class ProjectListView(ListView):
    ''' Generic display list view showing all Projects'''

    def get_queryset(self):
        return Project.objects.order_by('name')


class ProjectDetailView(generic.DetailView):
    model = Project
    template_name = 'pewad/project_detail.html'


def beerMeItAll(dbRecords):
    rows = []
    for rec in dbRecords:
        jso = beerMeThatJsonWR(rec)
        rows.append(jso)
    return rows


def beerMeThatJsonWR(wr):
    return {
        "conNum": wr.cont.number,
        "conName": wr.cont.name,
        "proj": wr.proj.abbr,
        "leadLast": wr.lead.lname,
        "leadFirst": wr.lead.fname,
        "empLast": wr.emp.lname,
        "empFirst": wr.emp.fname,
        "hours": wr.hours,
        "assig": wr.task,
    }
