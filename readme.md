```python
# reviews/views.py
def create(request):
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False) # commit=False 사용하는 이유
            review.user = request.user
            review.save()
            return redirect('reviews:index')
    else:
        review_form = ReviewForm()
    context = {
        'review_form':review_form,
    }
    return render(request, 'reviews/create.html', context)

def update(request, review_pk):
    review = Review.objects.get(pk=review_pk) #update에서는 호출 먼저
    if request.user == review.user:
        if request.method == "POST":
            review_form = ReviewForm(request.POST, request.FILES, instance=review)  #instance=review
            if review_form.is_valid():
                review_form.save()
                return redirect('reviews:detail', review.pk)
        else:
            review_form = ReviewForm(instance=review)
    else:
        return redirect('reviews:index')
    context = {
        'review': review,
        'review_form': review_form,
    }
    return render(request, 'reviews/update.html', context)

def comments_create(request, review_pk):
    review = Review.objects.get(pk=review_pk) #리뷰 호출부터해야됨
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment_form.save()
        return redirect('reviews:detail', review.pk)
    context = {
        'review': review,
        'comment_form': comment_form,
    }
    return render(request, 'reviews/detail.html', context)

def detail(request, pk):
    article = Article.objects.get(pk=pk)
    comments = article.comment_set.all()    # 댓글 전체 조회
    context = {
        'comments':comments,
        'article':article
    }
    return render(request, 'articles/detail.html', context)

def likes(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if article.like_users.filter(pk=request.user.pk).exists():  # 냅다 pk=request.pk 하면 안 됨 > request(요청한).user(사용자의).pk를 가져와야 됨
        article.like_users.remove(request.user.pk)
    else:
        article.like_users.add(request.user)
    return redirect('articles:index')
```