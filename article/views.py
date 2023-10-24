from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm
from django.contrib import messages, auth
from .models import Article, Category, Like
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    articles = Article.objects.filter(
        Q(content__icontains=q)
        | Q(title__icontains=q)
        | Q(category__category__icontains=q)
    )

    category = Category.objects.all()
    print(articles)

    context = {
        "articles": articles,
        "category": category,
    }
    return render(request, "home.html", context)


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
def create_article(request):
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
    user_liked = False  # Default to False for anonymous users
    liked_count = Like.objects.filter(article_id=article_id).count()

    if request.user.is_authenticated:
        user_liked = Like.objects.filter(
            article_id=article_id, user=request.user
        ).exists()

    context = {
        "article": article,
        "user_liked": user_liked,
        "liked_count": liked_count,
    }
    return render(request, "article/article_detail.html", context)


@login_required(login_url="login")
def delete_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    article.delete()
    return redirect("dashboard")


@login_required(login_url="login")
def like(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    Like.objects.create(article_id=article.id, user=request.user)
    return redirect("article_detail", article_id=article.id)


@login_required(login_url="login")
def unlike(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    Like.objects.filter(article_id=article.id, user=request.user).delete()
    return redirect("article_detail", article_id=article.id)
