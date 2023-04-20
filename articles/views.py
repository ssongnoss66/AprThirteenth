from django.shortcuts import render, redirect
from .models import Article, Comment, Emote
from .forms import ArticleForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

EMOTIONS = [
    {'label': '재밌어요', 'value': 1},
    {'label': '싫어요', 'value': 2},
    {'label': '화나요', 'value': 3},
]

# Create your views here.
def index(request):
    articles = Article.objects.order_by('-pk')
    """
        [int] page
        현재 주소의 페이지 번호를 할당받는 변수
        주소에 page(키)에 대한 값이 없으면 1 할당
    """
    page = request.GET.get('page', '1')
    """
        [int] per_page
        페이지를 나누는 기준
        e.g. 10 -> 데이터를 10개를 기준으로 나눔.
    """
    per_page = 5
    """
        [Paginator 인스턴스] paginator
        첫 번째 인자 : 페이지네이션을 적용할 데이터(queryset)
        두 번째 인자 : per_page
    """
    paginator = Paginator(articles, per_page)
    """
        [Page 인스턴스] page_obj
        출력할 데이터 및 페이지네이션을 구현을 위한 데이터가 저장된 변수
        반복문으로 순회하면 페이징 처리가 된 데이터가 요소가 됨.
    """
    page_obj = paginator.get_page(page)
    last_pg = paginator.num_pages
    context = {
        'articles': page_obj,
        'last_pg': last_pg,
    }
    return render(request, 'articles/index.html', context)

@login_required
def create(request):
    if request.method == "POST":
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:index')
    else:
        article_form = ArticleForm()
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/create.html', context)

def detail(request, pk):
    article = Article.objects.get(pk=pk)
    emotions = []
    for emotion in EMOTIONS:
        label = emotion['label']
        value = emotion['value']
        count = Emote.objects.filter(article=article, emotion=value).count()
        exist = Emote.objects.filter(article=article, emotion=value, user=request.user)
        emotions.append(
            {
                'label': label,
                'value': value,
                'count': count,
                'exist': exist,
            }
        )
    comments = article.comment_set.all()
    comment_form = CommentForm()
    context = {
        'comment_form':comment_form,
        'emotions':emotions,
        'comments':comments,
        'article':article
    }
    return render(request, 'articles/detail.html', context)

@login_required
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user == article.user:
        if request.method == "POST":
            article_form = ArticleForm(request.POST, instance=article)
            if article_form.is_valid():
                article_form.save()
                return redirect('articles:detail', article.pk)
        else:
            article_form = ArticleForm(instance=article)
    else:
        return redirect('articles:index')
    context = {
        'article': article,
        'article_form': article_form,
    }
    return render(request, 'articles/update.html', context)

@login_required
def delete(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user == article.user:
        article.delete()
    return redirect('articles:index')

@login_required
def comments(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.user = request.user
        comment.save()
        return redirect('articles:detail', article.pk)
    context = {
        'article':article,
        'comment_form':comment_form,
    }
    return render(request, 'articles/detail.html', context)

@login_required
def comments_delete(request, article_pk, comment_pk):
    article = Article.objects.get(pk=article_pk)
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('articles:detail', article.pk)

@login_required
def likes(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if article.like_users.filter(pk=request.user.pk).exists():
        article.like_users.remove(request.user)
    else:
        article.like_users.add(request.user)
    return redirect('articles:index')

@login_required
def comments_likes(request, article_pk, comment_pk):
    article = Article.objects.get(pk=article_pk)
    comment = Comment.objects.get(pk=comment_pk)
    if comment.like_users.filter(pk=request.user.pk).exists():
        comment.like_users.remove(request.user)
    else:
        comment.like_users.add(request.user)
    return redirect('articles:detail', article.pk)

def emotes(request, article_pk, emotion):
    article = Article.objects.get(pk=article_pk)
    filter_query = Emote.objects.filter(
        article=article,
        user=request.user,
        emotion=emotion,
    )
    if filter_query.exists():
        filter_query.delete()
    else:
        Emote.objects.create(article=article, user=request.user, emotion=emotion)
    return redirect('articles:detail', article_pk)