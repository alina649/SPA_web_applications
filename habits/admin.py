from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """Представление раздела - "Привычки" в админке"""

    list_display = ('owner', 'get_habit', 'period_habit', 'time_habit', 'time_limit', 'create_time')
    search_fields = ('owner', 'get_habit', 'period_habit', 'time_habit', 'time_limit', 'create_time')
