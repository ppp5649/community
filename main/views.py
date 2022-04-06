from django.shortcuts import render
from board.models import Post, Photo


def index(request):

    job_models = Post.objects.filter(name='직업리뷰').order_by('-id')
    major_models = Post.objects.filter(name='학과리뷰').order_by('-id')
    # Filter를 사용하여 name에 해당되는 객체만을 불러옴

    return render(request, 'index.html', {'job_models': job_models, 'major_models': major_models, })
    # index.html 안에서 job_models(템플릿 변수)란 이름으로 job_models(파이썬 변수)를 사용하겠다.
