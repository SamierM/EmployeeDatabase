from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from django.core.mail import send_mail
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
from django.template.loader import render_to_string
from django.core.mail import send_mail

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


class WorkRecordUpdateView(SuccessMessageMixin, generic.UpdateView):
    """ Display WorkRecord update form, for use inside a modal """
    model = WorkRecord
    fields = '__all__'
    template_name_suffix = '_update'
    success_message = "Update successful."

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


class WorkRecordCreate(SuccessMessageMixin, generic.CreateView):
    """ Create a new WorkRecord, via modal """
    model = WorkRecord
    fields = '__all__'
    template_name_suffix = '_create_form'

    def get_success_message(self, cleaned_data):
        return "Work Record \"%s\" was added successfully." % self.object

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

# ------------------------------------------------------------
# -------------------- Employee Views ------------------------
# ------------------------------------------------------------


class EmployeeCreate(SuccessMessageMixin, generic.CreateView):
    """ Create a new Employee """
    model = Employee
    fields = '__all__'
    template_name_suffix = '_create_form'

    def get_success_message(self, cleaned_data):
        return "Employee \"%s\" was added successfully." % self.object

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


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


def project_list(request):
    """ Display list view showing all Projects """

    return render(request, 'pewad/project_list.html', {'list_title': 'Project'})


def project_json_table_data(request):
    """ GET JSON data for all Projects list view """
    projs = get_list_or_404(Project)
    data = serialize('json', projs)

    return HttpResponse(data, content_type="json")


class ProjectUpdateView(SuccessMessageMixin, generic.UpdateView):
    """ Display view for updating a Project """
    model = Project
    fields = '__all__'
    template_name_suffix = '_update'
    success_message = "Update successful."


def project_json_records(request, pk):
    """ Get the WorkRecords data in JSON for a Project """
    records = WorkRecord.objects.filter(proj=pk)
    data = workrecord_models_to_json(records)

    return JsonResponse(data, safe=False)

# ------------------------------------------------------------
# -------------------- Email Stuffs --------------------------
# ------------------------------------------------------------


def create_email_message(work_records):
    """ Creates a email body string from a template """
    table_rows = ""
    for rec in work_records:
        rd = {'cont': rec.cont, 'proj': rec.proj.abbr,
              'lead': rec.lead, 'hours': rec.hours, 'task': rec.task}
        table_rows += render_to_string("email/tablerow.html", rd)
    msgparams = {'name': work_records[0].emp, 'rows': table_rows}

    return render_to_string("email/email.html", msgparams)


def email_single_employee(request, pk):
    """ Email an Employee's WorkRecords to the employee """
    recip = get_object_or_404(Employee, pk=pk)

    # TODO obviously this needs to be fixed
    SENDER = 'camico@gblsys.com'

    records = WorkRecord.objects.filter(emp=pk).order_by('-hours')
    msg = create_email_message(records)

    return send_mail(
        '%s Work Assignment' % recip.lname,  # Subject line
        msg,  # Message body
        SENDER,  # Sender
        [recip.email],  # Recipient List
        fail_silently=False,
    )

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
        "pk": workrecord.pk,
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
