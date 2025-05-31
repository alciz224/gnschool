from django.contrib import admin

from django.utils.translation import gettext_lazy as _
# Register your models here.
from core.models import (
     School,
     Grade,
     GradeOption,
     Level,
    # LevelOption,
     SchoolYear,
     SchoolYearLevel,
     Classroom,
    # Subject,
    # ClassroomSubject,
    # Teacher,
    # Student,
    # Enrollment,
    # EvalType,
    # MarkType,
    # Evaluation,
    # Timetable,
    # Timeslot,
    # TimetableEntry,
)


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "ville", "quartier", "foundation_date", "created_at", "updated_at")
    list_filter = ("ville", "quartier", "created_at")
    search_fields = ("name", "ville", "quartier")
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")
    fieldsets = (
        (_("Informations générales"), {
            "fields": ("name", "ville", "quartier", "foundation_date")
        }),
        (_("Identité visuelle"), {
            "fields": ("logo", "document_header")
        }),
        (_("Suivi"), {
            "fields": ("created_at", "created_by", "updated_at", "updated_by")
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)



@admin.register(SchoolYear)
class SchoolYearAdmin(admin.ModelAdmin):
    list_display = (
        "name", "school", "start_date", "end_date", 
        "created_at", "created_by", "updated_at", "updated_by"
    )
    list_filter = ("school", "start_date")
    search_fields = ("school__name", "name")
    readonly_fields = ("name", "created_at", "created_by", "updated_at", "updated_by")

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)



@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = (
        "name", "abbreviation", "school", "order", 
        "created_at", "created_by", "updated_at", "updated_by"
    )
    list_filter = ("school",)
    search_fields = ("name", "abbreviation", "school__name")
    readonly_fields = ("created_at", "created_by", "updated_at", "updated_by")

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)




@admin.register(GradeOption)
class GradeOptionAdmin(admin.ModelAdmin):
    list_display = (
        "name", "abbreviation", "grade", "order",
        "created_at", "created_by", "updated_at", "updated_by"
    )
    list_filter = ("grade",)
    search_fields = ("name", "abbreviation", "grade__name")
    readonly_fields = ("created_at", "created_by", "updated_at", "updated_by")

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = (
        "name", "abbreviation", "grade", "order",
        "created_at", "created_by", "updated_at", "updated_by"
    )
    list_filter = ("grade",)
    search_fields = ("name", "abbreviation", "grade__name")
    readonly_fields = ("created_at", "created_by", "updated_at", "updated_by")

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(SchoolYearLevel)
class SchoolYearLevelAdmin(admin.ModelAdmin):
    list_display = (
        'school_year', 
        'grade', 
        'level', 
        'is_active',
        'created_at', 
        'created_by',
        'updated_at', 
        'updated_by',
    )
    list_filter = ('school_year', 'grade', 'level', 'is_active')
    search_fields = (
        'school_year__name', 
        'grade__name', 
        'level__name',
    )
    readonly_fields = ('created_at', 'created_by', 'updated_at', 'updated_by')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ("__str__", "school_year_level", "grade_option", "created_at")
    list_filter = ("school_year_level__school_year", "school_year_level__grade", "grade_option")
    search_fields = ("name",)
    autocomplete_fields = ("school_year_level", "grade_option", "created_by", "updated_by")
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")
