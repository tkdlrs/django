from django.urls import path 

from . import views 

app_name = "rpg"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("create/", views.create_skill, name="create_skill"),
    path("delete-skill/<int:skill_id>/", views.delete_skill, name="delete_skill"),
    #
    path("train/<int:skill_id>/", views.train_skill, name="train"),
    path("train/<int:pk>/edit/", views.edit_training_session, name="edit_training_session"),
    path("train/<int:pk>/remove-session/", views.remove_training_session, name="remove_training_session"),
]
