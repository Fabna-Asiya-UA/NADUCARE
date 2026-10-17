from django.contrib import admin
from .models import Solution, SolutionVote


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('id', 'problem', 'user', 'created_at')
    search_fields = ('description', 'problem__title', 'user__username')


@admin.register(SolutionVote)
class SolutionVoteAdmin(admin.ModelAdmin):
    list_display = ('solution', 'user', 'created_at')