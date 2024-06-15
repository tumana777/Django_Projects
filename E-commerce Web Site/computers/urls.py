from django.urls import path
from .views import PCListView

urlpatterns = [
    path("computers/personal_computers/", PCListView.as_view(), name="personal_computers")
]