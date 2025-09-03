from django.db import models


class Route(models.Model):
    route_no = models.CharField(max_length=20)
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.route_no} ({self.start_point} → {self.end_point})"


class Student(models.Model):
    regno = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.regno} - {self.name}"


class BusPass(models.Model):
    STATUS_APPLIED = 'Applied'
    STATUS_ASSIGNED = 'Assigned'
    STATUS_REJECTED = 'Rejected'

    STATUS_CHOICES = [
        (STATUS_APPLIED, 'Applied'),
        (STATUS_ASSIGNED, 'Assigned'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_APPLIED
    )
    applied_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ('student', 'route')

    def __str__(self):
        return f"{self.student.regno} - {self.route.route_no} [{self.status}]"
