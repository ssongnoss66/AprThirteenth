from django.shortcuts import render, redirect
from .models import Review, Comment
from .forms import ReviewForm, CommentForm

# Create your views here.
def index(request):
    reviews = Review.objects.all()
    context = {
        'reviews': reviews
    }
    return render(request, 'reviews/index.html', context)

def create(request):
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('reviews:index')
    else:
        review_form = ReviewForm()
    context = {
        'review_form':review_form,
    }
    return render(request, 'reviews/create.html', context)

def detail(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    comments = review.comment_set.all()
    comment_form = CommentForm()
    context = {
        'review': review,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'reviews/detail.html', context)

def update(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        if request.method == "POST":
            review_form = ReviewForm(request.POST, instance = review)
            if review_form.is_valid():
                review_form.save()
                return redirect('reviews:detail', review.pk)
        else:
            review_form = ReviewForm(instance=review)
    else:
        return redirect('reviews:index')
    context = {
        'review':review,
        'review_form':review_form
    }
    return render(request, 'reviews/update.html', context)

def delete(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        review.delete()
    return redirect('reviews:index')

def comment_create(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment_form.save()
        return redirect('reviews:detail', review.pk)
    context = {
        'review':review,
        'comment_form':comment_form
    }
    return render(request, 'reviews/detail.html', context)

def comment_delete(request, review_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if comment.user == request.user:
        comment.delete()
    return redirect('reviews:detail', review_pk)