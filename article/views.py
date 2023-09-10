from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm
from django.contrib import messages, auth
from .models import Article, Category
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.


def article(request):
    articles = Article.objects.all()
    category = Category.objects.all()
    paginator = Paginator(
        articles, 3
    )  # You can adjust the number of articles per page as needed
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "article": page,
        "category": category,
    }
    return render(request, "article/articles.html", context)


@login_required(login_url="login")
def dashboard(request):
    articles = Article.objects.filter(author=request.user)
    paginator = Paginator(
        articles, 3
    )  # You can adjust the number of articles per page as needed
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    context = {
        "articles": page,
    }
    return render(request, "article/dashboard.html", context)


@login_required(login_url="login")
def createarticle(request):
    user = request.user
    if request.method == "POST":
        form = ArticleForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            form.instance.author = user
            form.save()
            messages.success(request, "Article Successfully submit.")
            return redirect("dashboard")
        else:
            messages.error(request, "something went wrong.")
            return redirect("create")
    else:
        form = ArticleForm()
    context = {
        "form": form,
    }
    return render(request, "article/create_article.html", context)


@login_required(login_url="login")
def edit_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.error(request, "Article edit successfully")
            return redirect("dashboard")
    else:
        form = ArticleForm(instance=article)
    context = {
        "article": article,
        "form": form,
    }

    return render(request, "article/edit_article.html", context)


def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    context = {
        "article": article,
    }
    return render(request, "article/article_detail.html", context)


@login_required(login_url="login")
def delete_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    article.delete()
    return redirect("dashboard")


def article_search(request):
    category = Category.objects.all()
    context = {}
    if "query" in request.GET:
        query = request.GET.get("query")

        if query:
            search_result = Article.objects.order_by("-created_at").filter(
                Q(content__icontains=query) | Q(title__icontains=query)
            )

            paginator = Paginator(
                search_result, 2
            )  # You can adjust the number of articles per page as needed
            page_number = request.GET.get("page")
            page = paginator.get_page(page_number)
            context = {
                "query": query,
                "articles": page,
                "category": category,
            }

    return render(request, "article/article_search.html", context)


def articles_by_categories(request, category_names):
    categories = category_names.split()
    articles = Article.objects.filter(category__category__in=categories)
    paginator = Paginator(
        articles, 2
    )  # You can adjust the number of articles per page as needed
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    category = Category.objects.all()
    context = {
        "articles": page,
        "selected_categories": categories[0],
        "category": category,
        
    }

    return render(request, "article/article_category.html", context)
