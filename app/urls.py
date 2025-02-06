from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("contact/", contact, name="contact"),
    path("blog/", blog, name="blog"),
    path("signin/", signin, name="signin"),
    path("logout/", logout_view, name="logout"),
    path("admin_panel/", admin_panel, name="admin_panel"),
    path("edit/<slug:slug>/", edit_article, name="edit_article"),
    path("delete/<slug:slug>/", delete_article, name="delete_article"),
    path("<slug:slug>/", article_detail, name="article_detail"),
]
