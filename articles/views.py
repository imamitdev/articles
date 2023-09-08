from django.shortcuts import render
from article.models import Article, Category
from django.core.paginator import Paginator


def home(request):
    articles = Article.objects.all()
    category = Category.objects.all()

    paginator = Paginator(
        articles, 2
    )  # You can adjust the number of articles per page as needed
    page_number = request.GET.get("page")
    pages = paginator.get_page(page_number)
    context = {
        "articles": pages,
        "category": category,
    }
    return render(request, "home.html", context)
