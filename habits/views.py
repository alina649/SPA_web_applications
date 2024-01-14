from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginators import HabitsPaginator
from habits.permissions import IsOwner
from habits.serializer import HabitSerializer


class HabitListAPIView(generics.ListAPIView):
    """вывод списка привычек"""
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]


class HabitCreateView(generics.CreateAPIView):
    """ Generic - класс для создания новой привычки """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = HabitsPaginator

    def perform_create(self, serializer):
        """ Переопределяем метод создания привычки """

        new_habit = serializer.save()
        new_habit.owner = self.request.user
        new_habit.save()


class HabitDetailView(generics.RetrieveAPIView):
    """ Generic - класс для детального просмотра привычки """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class HabitUpdateView(generics.UpdateAPIView):
    """ Generic - класс для изменения (редактирования) привычки """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDeleteView(generics.DestroyAPIView):
    """ Generic - класс для удаления привычки """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class PublicHabitListView(generics.ListAPIView):
    """ Generic - класс для вывода списка публичных привычек """

    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitsPaginator