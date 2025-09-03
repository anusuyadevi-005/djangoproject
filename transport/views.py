from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
import csv

from .models import Route, Student, BusPass
from .forms import BusPassApplyForm, RouteForm
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST

# ---------------- Bus Pass Application ----------------
def apply_pass(request):
    if request.method == 'POST':
        form = BusPassApplyForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            route = form.cleaned_data['route']
            
            # prevent duplicate applications for same route
            existing = BusPass.objects.filter(student=student, route=route).first()
            if existing:
                messages.info(request, f"You already applied/assigned for route {route.route_no} (status: {existing.status}).")
                return redirect('transport:status') 
            
            BusPass.objects.create(student=student, route=route, status=BusPass.STATUS_APPLIED)
            messages.success(request, "Application submitted!")
            return redirect('transport:status')
    else:
        form = BusPassApplyForm()
    return render(request, 'transport/apply.html', {'form': form})

def check_status(request):
    passes = None
    if request.method == 'POST':
        regno = request.POST.get('regno', '').strip()
        if regno:
            student = Student.objects.filter(regno__iexact=regno).first()
            if student:
                passes = BusPass.objects.filter(student=student).order_by('-applied_at')
            else:
                messages.error(request, "No student found with that register number.")
    return render(request, 'transport/status.html', {'passes': passes})

# ---------------- Admin Views ----------------
@staff_member_required
def admin_applications(request):
    applications = BusPass.objects.filter(status=BusPass.STATUS_APPLIED).order_by('applied_at')
    return render(request, 'transport/admin_applications.html', {'applications': applications})

@staff_member_required
@require_POST
def assign_pass(request, pass_id):
    bp = get_object_or_404(BusPass, id=pass_id)
    assigned_count = BusPass.objects.filter(route=bp.route, status=BusPass.STATUS_ASSIGNED).count()
    if assigned_count < bp.route.capacity:
        bp.status = BusPass.STATUS_ASSIGNED
        bp.save()
        messages.success(request, f"Assigned {bp.student.regno} to route {bp.route.route_no}.")
    else:
        messages.error(request, "Cannot assign: route capacity reached.")
    return redirect('transport:admin_applications')

@staff_member_required
@require_POST
def reject_pass(request, pass_id):
    bp = get_object_or_404(BusPass, id=pass_id)
    bp.status = BusPass.STATUS_REJECTED
    bp.save()
    messages.success(request, "Application rejected.")
    return redirect('transport:admin_applications')

@staff_member_required
def route_allocations(request):
    routes = Route.objects.all()
    allocations = []
    for r in routes:
        assigned = BusPass.objects.filter(route=r, status=BusPass.STATUS_ASSIGNED).select_related('student')
        allocations.append((r, assigned))
    return render(request, 'transport/allocations.html', {'allocations': allocations})

@staff_member_required
def export_csv(request):
    routes = Route.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="allocations.csv"'
    writer = csv.writer(response)
    writer.writerow(['Route No', 'Start', 'End', 'Student Regno', 'Student Name', 'Status'])
    for r in routes:
        bps = BusPass.objects.filter(route=r)
        for bp in bps:
            writer.writerow([r.route_no, r.start_point, r.end_point, bp.student.regno, bp.student.name, bp.status])
    return response

# ---------------- Route Management ----------------
@staff_member_required
def route_list(request):
    routes = Route.objects.all()
    return render(request, "transport/route_list.html", {"routes": routes})

@staff_member_required
def add_route(request):
    if request.method == "POST":
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Route added successfully!")
            return redirect("transport:route_list")  # Fixed: added transport: namespace
    else:
        form = RouteForm()
    return render(request, "transport/add_route.html", {"form": form})