from rest_framework import serializers

from habits.models import Habit
from habits.validators import  TimeLimitValidator, \
    SignPleasantHabitValidator


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            TimeLimitValidator('time_limit'),
            SignPleasantHabitValidator('nice_habit', 'reward_habit', 'associated_habit'),
                      ]