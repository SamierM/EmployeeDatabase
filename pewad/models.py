from django.db import models
from django.urls import reverse


class Employee(models.Model):
    # Employee database model
    fname = models.CharField("First Name", max_length=200)
    lname = models.CharField("Last Name", max_length=200)
    email = models.EmailField("Email", null=True)

    def __str__(self):
        return "{self.fname} {self.lname}".format(self=self)

    def get_absolute_url(self):
        return reverse('pewad:employee', kwargs={'pk': self.pk})


class Project(models.Model):
    # Project database model
    name = models.CharField("Project Name", max_length=500)
    abbr = models.CharField("Abbr.", max_length=100)
    desc = models.TextField("Description")

    def __str__(self):
        return "{self.name} ({self.abbr})".format(self=self)

    def get_absolute_url(self):
        return reverse('pewad:project', kwargs={'pk': self.pk})


class Contract(models.Model):
    # Contract database model
    name = models.CharField("Contract Name", max_length=200)
    number = models.IntegerField("Contract Number")

    def __str__(self):
        return "{self.number} {self.name}".format(self=self)

    def get_absolute_url(self):
        return reverse('pewad:contract', kwargs={'pk': self.pk})


class WorkRecord(models.Model):
    # Work Record (Tasking) database model
    cont = models.ForeignKey(
        Contract,
        verbose_name="Contract",
        on_delete=models.CASCADE,
    )
    proj = models.ForeignKey(
        Project,
        verbose_name="Project",
        on_delete=models.CASCADE,
    )
    emp = models.ForeignKey(
        Employee,
        verbose_name="Employee",
        on_delete=models.CASCADE,
    )
    lead = models.ForeignKey(
        Employee,
        verbose_name="Lead",
        on_delete=models.CASCADE,
        related_name="Lead",
        null=True,
    )
    hours = models.CharField("Hours", max_length=4)
    task = models.TextField("Assignment")

    def __str__(self):
        return "{self.emp}: {self.proj.abbr} - {self.task}".format(self=self)
