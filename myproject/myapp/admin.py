from django.contrib import admin
from .models import Course, Enrollment, Instructor, Student

# Register your models here.
class EnrollmentInline(admin.TabularInline):
    model = Enrollment 
    extra = 1

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "email", "department",  "admission_date", "is_active")
    search_fields = ("name", "email", "department")
    list_filter = ("department","age", "is_active")
    ordering = ("name","age")
    inlines = [EnrollmentInline]

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "description", "credits", "is_active", "instructor")
    search_fields = ("code", "name", "description")
    list_filter = ("credits", "is_active")
    ordering = ("code","name")

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "enrollment_date", "status")
    search_fields = ("student__name", "course__name")
    list_filter = ("status",)
    ordering = ("enrollment_date",)
    actions = ["mark_as_completed", "mark_as_dropped"]


    @admin.action(permissions=['change'], description="Mark selected enrollments as completed")
    def mark_as_completed(self, request, queryset):
        updated_count = queryset.update(status=Enrollment.Status.COMPLETED)
        self.message_user(request, f"{updated_count} enrollment(s) marked as completed.")

    @admin.action(permissions=['change'], description="Mark selected enrollments as dropped")
    def mark_as_dropped(self, request, queryset):
        updated_count = queryset.update(status=Enrollment.Status.DROPPED)
        self.message_user(request, f"{updated_count} enrollment(s) marked as dropped.")   

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "department")
    search_fields = ("name", "email", "department")
    list_filter = ("department",)
    ordering = ("name",)
