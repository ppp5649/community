from django.http import cookie, response
from django.shortcuts import render, redirect
from user.models import BoardMember
from board.models import Post
from board.forms import BoardForm, CommentForm
from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta

# Create your views here.


def job(request):
    job_models = Post.objects.filter(name='직업리뷰').order_by('-id')
    return render(request, 'board.html', {'post': job_models, 'board_name': '직업'})


def major(request):
    major_models = Post.objects.filter(name='학과리뷰').order_by('-id')
    # name이 major인 모델을 조회해서 쿼리셋으로 반환 (역순으로 노출)
    return render(request, 'board.html', {'post': major_models, 'board_name': '학과'})


def board_detail(request, pk):
    try:
        # No such Column 오류 해결 -> DB 관련 문제같음 (마이그레이션)
        context = dict()
        board_detail = Post.objects.get(pk=pk)
        comment_form = CommentForm()

        context['board_detail'] = board_detail
        context['comment_form'] = comment_form

        response = render(request, 'board_detail.html', context)
        # 'board_detail' 과 'comment_form'을 따로 render에 넣어줬을 땐 html 화면에 코드가 그대로 출력되는 오류가
        # 발생했었는데 context로 묶어주고 딕셔너리 형태로 넣어주니 해결 되었다.

        # 조회수 기능 (쿠키이용)
        expire_date, now = datetime.now(), datetime.now()
        expire_date += timedelta(days=1)
        # 이 부분 수정해야 할 수도 있음
        expire_date = expire_date.replace(
            hour=0, minute=0, second=0, microsecond=0)
        expire_date -= now
        max_age = expire_date.total_seconds()

        cookie_value = request.COOKIES.get('viewCount', '_')

        if f'_{pk}_' not in cookie_value:
            cookie_value += f'{pk}_'
            response.set_cookie('viewCount', value=cookie_value,
                                max_age=max_age, httponly=True)
            board_detail.viewCount += 1
            board_detail.save()

        return response

    except Post.DoesNotExist:
        return render(request, 'board_erased.html')
      # 삭제 된 게시글은 삭제 게시글 안내 페이지로 이동


def comment_write(request, pk):
    filled_form = CommentForm(request.POST)

    if filled_form.is_valid():
        temp_form = filled_form.save(commit=False)
        temp_form.connect = Post.objects.get(id=pk)
        temp_form.save()

    return redirect('board_detail', pk)


def board_write(request):
    if not request.session.get('user'):
        return redirect('/user/login/')
    # 세션에 'user' 키를 불러올 수 없으면, 로그인하지 않은 사용자이므로 로그인 페이지로 리다이렉트 한다.

    if request.method == "POST":
        form = BoardForm(request.POST)

        if form.is_valid():
            # form의 모든 validators 호출 유효성 검증 수행
            user_id = request.session.get('user')
            user = BoardMember.objects.get(pk=user_id)

            post = Post()
            post.title = form.cleaned_data['title']
            post.contents = form.cleaned_data['contents']
            post.name = form.cleaned_data['name']
            # 검증에 성공한 값들은 사전타입으로 제공 (form.cleaned_data)
            # 검증에 실패시 form.error 에 오류 정보를 저장

            post.writer = user
            post.save()

            return redirect(f'/board/{post.pk}')

    else:
        form = BoardForm()

    return render(request, 'board_write.html', {'form': form})
