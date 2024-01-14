from datetime import timedelta

from rest_framework.exceptions import ValidationError


class SignPleasantHabitValidator:
    """В связанные привычки могут попадать только привычки с признаком приятной привычки.
    У приятной привычки не может быть вознаграждения или связанной привычки."""

    def __init__(self, nice_habit, reward_habit, associated_habit):
        self.nice_habit = nice_habit
        self.reward_habit = reward_habit
        self.associated_habit = associated_habit

    def __call__(self, values):
        nice_habit = values.get(self.nice_habit) # Признак приятной привычки
        reward_habit = values.get(self.reward_habit) # Награда за выполнение привычки
        associated_habit = values.get(self.associated_habit) # Связанная привычка

        if not nice_habit:
            if not reward_habit:
                if not associated_habit:
                    raise ValidationError('По завершении задачи обязательно должно быть вознаграждение либо приятная '
                                          'привычка!')

        else:
            if reward_habit or associated_habit:
                raise ValidationError('У приятной привычки не может быть вознаграждения.')


class TimeLimitValidator:
    """Время выполнения должно быть не больше 120 секунд"""

    def __init__(self, time_limit):
        self.duration = time_limit

    def __call__(self, value):
        duration = value.get(self.duration)
        time = int(duration)
        if int(time) > 120:
            raise ValidationError('Длительность выполнения не может превышать 120 секунд')



