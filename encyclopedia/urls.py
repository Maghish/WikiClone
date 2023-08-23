from django.urls import path

from . import views

urlpatterns = [
    path("wiki/", views.index, name="index"),
    path("", views.redirect_user, name="redirect_user"),
    path("wiki/<str:name>", views.entry , name="entries_page"),
    path("search/", views.search_entry, name="search_entry"),
    path("new/", views.new_page, name="new_page"),
    path("edit/", views.edit_page, name="edit_page"),
    path("save/", views.save_page, name="save_page"),
    path("random/", views.random_page, name="random_page")
]
