from django.urls import path
from .views import RunningStatView, RunningStatDetailView, RunningStatSummaryView, RunningStatMonthlyStatsView, RunningStatWeeklyStatsView
from .views import ChallengeCreateView, ChallengeListView, ChallengeDetailView, TopRunningStatsView

urlpatterns = [
    path('stats/', RunningStatView.as_view(), name='running_stats'),
    path('stats/<int:stat_id>/', RunningStatDetailView.as_view(), name='running_stat_detail'),
    path('summary/', RunningStatSummaryView.as_view(), name='running_stat_summary'),
    path('challenges/', ChallengeCreateView.as_view(), name='create_challenge'),
    path('challenges/list/', ChallengeListView.as_view(), name='list_challenges'),
    path('challenges/<int:challenge_id>/', ChallengeDetailView.as_view(), name='challenge_detail'),
    path('stats/monthly/', RunningStatMonthlyStatsView.as_view(), name='monthly_stats'),
    path('stats/weekly/', RunningStatWeeklyStatsView.as_view(), name='weekly_stats'),
    path('stats/top/', TopRunningStatsView.as_view(), name='top_stats'),
]

