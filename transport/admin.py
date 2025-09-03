from django.contrib import admin
from .models import Route, Student, BusPass


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('route_no', 'start_point', 'end_point', 'capacity')
    search_fields = ('route_no', 'start_point', 'end_point')
    list_filter = ('start_point', 'end_point')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('regno', 'name')
    search_fields = ('regno', 'name')


@admin.register(BusPass)
class BusPassAdmin(admin.ModelAdmin):
    list_display = ('student', 'route', 'status', 'applied_at')
    list_filter = ('status', 'route')
    search_fields = ('student__regno', 'student__name', 'route__route_no')
    list_editable = ('status',)  # lets you change status directly in list view
