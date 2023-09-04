from django.shortcuts import render
from article.models import Article
from django.core.paginator import Paginator


def home(request):
    articles = Article.objects.all()
    paginator = Paginator(
        articles, 3
    )  # You can adjust the number of articles per page as needed
    page_number = request.GET.get("page")
    pages = paginator.get_page(page_number)
    context = {
        "articles": pages,
    }
    return render(request, "home.html", context)
