from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseForbidden
from django.contrib.contenttypes.models import ContentType
from .models import Article
# Create your views here.

@permission_required('your_app_name.can_edit', raise_exception=True)
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    # Logic for editing the article
    return HttpResponse(f"Editing article: {article.title}")

@permission_required('your_app_name.can_view', raise_exception=True)
def view_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return HttpResponse(f"Viewing article: {article.title}")

