from django.urls import path
from . import views

app_name = "transport"   # 👈 IMPORTANT

urlpatterns = [
    path("apply/", views.apply_pass, name="apply"),
    path("status/", views.check_status, name="status"),
    path("admin/applications/", views.admin_applications, name="admin_applications"),
    path("admin/assign/<int:pass_id>/", views.assign_pass, name="assign_pass"),
    path("admin/reject/<int:pass_id>/", views.reject_pass, name="reject_pass"),
    path("admin/allocations/", views.route_allocations, name="allocations"),
    path("admin/export/", views.export_csv, name="export_csv"),
    path("routes/", views.route_list, name="route_list"),
    path("routes/add/", views.add_route, name="add_route"),
]
