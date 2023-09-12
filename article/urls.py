from django.urls import path
from . import views

urlpatterns = [
    path("articles/", views.article, name="articles"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("create/", views.createarticle, name="create"),
    path(
        "edit_article/<int:article_id>/",
        views.edit_article,
        name="edit_article",
    ),
    path(
        "delete_article/<int:article_id>/",
        views.delete_article,
        name="delete_article",
    ),
    path(
        "article_detail/<int:article_id>/",
        views.article_detail,
        name="article_detail",
    ),
    path(
        "article_search/",
        views.article_search,
        name="article_search",
    ),
    path(
        "articles-by-categories/<str:category_names>/",
        views.articles_by_categories,
        name="articles_by_categories",
    ),
    path(
        "like/<int:article_id>/",
        views.like,
        name='like',
    ),
     path(
        "unlike/<int:article_id>/",
        views.unlike,
        name='unlike',
    )
]
