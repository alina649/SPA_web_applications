from django.urls import path

from habits.apps import HabitsConfig


from habits.views import HabitListAPIView, HabitCreateView, HabitDetailView, HabitUpdateView, HabitDeleteView, \
    PublicHabitListView

app_name = HabitsConfig.name

urlpatterns = [

    path('', HabitListAPIView.as_view(), name='habit_list'),
    path('habit/create/',  HabitCreateView.as_view(), name='habit_create'),
    path('habit/<int:pk>/', HabitDetailView.as_view(), name='habit_get'),
    path('habit/update/<int:pk>/', HabitUpdateView.as_view(), name='habit_update'),
    path('habit/delete/<int:pk>/', HabitDeleteView.as_view(), name='habit_delete'),
    path('habit/public/', PublicHabitListView.as_view(), name='public_habits'),
              ]