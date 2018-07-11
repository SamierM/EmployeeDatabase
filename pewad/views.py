from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from django.core.mail import send_mail
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize

from .models import Contract, Employee, Project, WorkRecord


# ------------------------------------------------------------
# -------------------- Main (index) Views --------------------
# ------------------------------------------------------------


def index(request):
    """ Display the default PEWAD landing page"""
    context = {'passedValue': "MADROX", }
    return render(request, 'pewad/index.html', context)


def index_json_table_data(request):
    """ GET JSON data for table view; WorkRecords """
    dbRecs = get_list_or_404(WorkRecord)
    data = workrecord_models_to_json(dbRecs)

    return JsonResponse(data, safe=False)

# ------------------------------------------------------------
# -------------------- Employee Views ------------------------
# ------------------------------------------------------------


def employee_list(request):
    """ Display list view showing all Employees """

    return render(request, 'pewad/employee_list.html', {'list_title': 'Employee'})


def employee_json_table_data(request):
    """ GET JSON data for all Employees list view """
    dbrecs = get_list_or_404(Employee)
    data = serialize('json', dbrecs, cls=LazyEncoder)

    return HttpResponse(data, content_type="json")


class EmployeeUpdateView(SuccessMessageMixin, generic.UpdateView):
    """ Display view for updating an Employee  """
    model = Employee
    fields = '__all__'
    template_name_suffix = '_update'
    success_message = "Update successful."


def employee_json_records(request, emp_id):
    """ Get the WorkRecords data in JSON for an Employee """
    records = WorkRecord.objects.filter(emp=emp_id)
    data = workrecord_models_to_json(records)

    return JsonResponse(data, safe=False)


# ------------------------------------------------------------
# -------------------- Contract Views ------------------------
# ------------------------------------------------------------

def contract_list(request):
    """ Display list view showing all Contracts """

    return render(request, 'pewad/contract_list.html', {'list_title': 'Contracts'})


def contract_json_table_data(request):
    """ GET JSON data for all Contracts list view """
    conts = get_list_or_404(Contract)
    data = serialize('json', conts)

    return HttpResponse(data, content_type="json")


class ContractUpdateView(SuccessMessageMixin, generic.UpdateView):
    """ Display view for updating a Contract """
    model = Contract
    fields = '__all__'
    template_name_suffix = '_update'
    success_message = "Update successful."


def contact_json_records(request, pk):
    """ Get the WorkRecords data in JSON for a Contact """
    records = WorkRecord.objects.filter(cont=pk)
    data = workrecord_models_to_json(records)

    return JsonResponse(data, safe=False)

# ------------------------------------------------------------
# -------------------- Project Views -------------------------
# ------------------------------------------------------------


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


class ProjectListView(ListView):
    """ Generic display list view showing all Projects """

    def get_queryset(self):
        return Project.objects.order_by('name')


class ProjectDetailView(generic.DetailView):
    model = Project
    template_name = 'pewad/project_detail.html'

# ------------------------------------------------------------
# -------------------- JSON helper functions -----------------
# ------------------------------------------------------------


def workrecord_models_to_json(db_recs):
    """ Convert WorkRecord database models to JSON array """
    json_recs = []
    for rec in db_recs:
        jsn = make_json_workrecord(rec)
        json_recs.append(jsn)
    return json_recs


def make_json_workrecord(workrecord):
    """ Get a JSON object representation of a WorkRecord model """
    # TODO Unfortunatley need to do this manually... unless a better way is figured out
    return {
        "conNum": workrecord.cont.number,
        "conName": workrecord.cont.name,
        "proj": workrecord.proj.abbr,
        "leadLast": workrecord.lead.lname,
        "leadFirst": workrecord.lead.fname,
        "empLast": workrecord.emp.lname,
        "empFirst": workrecord.emp.fname,
        "hours": workrecord.hours,
        "assig": workrecord.task,
    }


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Employee):
            return str(obj)
        return super().default(obj)
