from django.contrib import admin
from .models import Problem
# Register your models here.


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'district',
        'category',
        'status',
        'created_at',
    )

    list_filter = ('district', 'category', 'status')
    search_fields = ('title', 'description', 'location')