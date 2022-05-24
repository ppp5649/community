from django.http import cookie, response
from django.shortcuts import get_object_or_404, render, redirect
from user.models import BoardMember
from board.models import Post, Comment, Photo
from board.forms import BoardForm, CommentForm, ImageForm, ImageFormSet
from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta
from django.db import transaction


def job(request):
    job_models = Post.objects.filter(name='직업리뷰').order_by('-id')
    return render(request, 'board.html', {'post': job_models, 'board_name': '직업'})


def major(request):
    major_models = Post.objects.filter(name='학과리뷰').order_by('-id')
    # name이 major인 모델을 조회해서 쿼리셋으로 반환 (역순으로 노출)
    return render(request, 'board.html', {'post': major_models, 'board_name': '학과'})


def board_detail(request, pk):
    try:
        photo = Photo()
        # No Such Column 오류 해결 -> DB 관련 문제같음
        # (마이그레이션 수시로 하면서 사이트 작동 잘 되는지 확인하기)
        context = dict()
        post = Post.objects.get(pk=pk)
        comment_form = CommentForm()
        context['post'] = post
        context['comment_form'] = comment_form

        response = render(request, 'board_detail.html', context)
        # 'post' 과 'comment_form'을 따로 render에 넣어줬을 땐 html 화면에
        # 코드가 그대로 출력되는 오류가 발생했었는데
        # context로 묶어주고 각각 딕셔너리 형태로 넣어주니 해결 되었다.

        # 조회수 기능 (쿠키이용)
        expire_date, now = datetime.now(), datetime.now()
        expire_date += timedelta(days=1)
        # 이 부분 수정해야 할 수도 있음
        expire_date = expire_date.replace(
            hour=0, minute=0, second=0, microsecond=0)
        expire_date -= now
        max_age = expire_date.total_seconds()

        cookie_value = request.COOKIES.get('view_count', '_')

        if f'_{pk}_' not in cookie_value:
            cookie_value += f'{pk}_'
            response.set_cookie('view_count', value=cookie_value,
                                max_age=max_age, httponly=True)
            post.view_count += 1
            post.save()

        return response

    except Post.DoesNotExist:
        return render(request, 'board_erased.html')
      # 삭제 된 게시글은 삭제 게시글 안내 페이지로 이동


def board_write(request):
    if not request.session.get('user'):
        return redirect('/user/login/')
    # 세션에 'user' 키를 불러올 수 없으면, 로그인하지 않은 사용자이므로 로그인 페이지로 리다이렉트 한다.

    if request.method == "POST":
        form = BoardForm(request.POST)
        image_formset = ImageFormSet(request.POST, request.FILES)
        if form.is_valid() and image_formset.is_valid():
            # form의 모든 validators 호출 유효성 검증 수행
            user_id = request.session.get('user')  # 유저 고유의 id값
            user = BoardMember.objects.get(pk=user_id)
            post = Post()

            with transaction.atomic():
                post.title = form.cleaned_data['title']
                post.contents = form.cleaned_data['contents']
                post.name = form.cleaned_data['name']

                # 검증에 성공한 값들은 사전타입으로 제공 (form.cleaned_data)
                # 검증에 실패시 form.error 에 오류 정보를 저장
                post.writer = user
                post.save()
                image_formset.instance = post
                image_formset.save()

                return redirect(f'/board/{post.pk}')

    else:
        form = BoardForm()
        image_formset = ImageFormSet()

    return render(request, 'board_write.html', {'form': form, 'image_formset': image_formset})


def board_update(request, pk):
    if not request.session.get('user'):
        return redirect('/user/login/')
    # 세션에 'user' 키를 불러올 수 없으면, 로그인하지 않은 사용자이므로 로그인 페이지로 리다이렉트 한다.
    user_id = request.session.get('user')
    post = get_object_or_404(Post, pk=pk)

    if post.writer == BoardMember.objects.get(pk=user_id):

        if request.method == "POST":
            form = BoardForm(request.POST, request.FILES, instance=post)

            if form.is_valid():
                # form의 모든 validators 호출 유효성 검증 수행
                form.save()

                # 기존 글 작성 form을 다 지우고 form.save()만 넣었더니 정상적으로 이전 글 반영됨

                return redirect(f'/board/{post.pk}')

        else:
            form = BoardForm(instance=post)

        return render(request, 'board_update.html', {'form': form, 'post': post})

    else:
        return render(request, 'user_mismatch.html')


def board_delete(request, pk):
    if not request.session.get('user'):
        return redirect('/user/login/')
    # 세션에 'user' 키를 불러올 수 없으면, 로그인하지 않은 사용자이므로 로그인 페이지로 리다이렉트 한다.
    user_id = request.session.get('user')  # 유저 고유의 id값
    post = get_object_or_404(Post, pk=pk)

    # 로그인 한 사용자와 글쓴이가 일치하는 경우
    if post.writer == BoardMember.objects.get(pk=user_id):
        post.delete()

        return redirect('/')

    else:
        return render(request, 'user_mismatch.html')


def comment_write(request, pk):

    if not request.session.get('user'):
        return redirect('/user/login/')
    # 세션에 'user' 키를 불러올 수 없으면, 로그인하지 않은 사용자이므로 로그인 페이지로 리다이렉트 한다.

    filled_form = CommentForm(request.POST)

    if filled_form.is_valid():
        user_id = request.session.get('user')
        user = BoardMember.objects.get(pk=user_id)
        # User 정보 불러오기 -> Board_write 참고했음

        temp_form = filled_form.save(commit=False)
        temp_form.comment_writer = user
        temp_form.comment = Post.objects.get(id=pk)
        temp_form.save()

    return redirect('board_detail', pk)


""" def comment_update(request, com_id, pk):
    post = get_object_or_404(Post, pk=pk)
    my_com = Comment.objects.get(id=com_id)

    if request.method == "POST":
        update_form = CommentForm(request.POST, instance=my_com)
        # instance를 사용해 줌으로써 이전의 댓글이 남아있게 끔 해야함
        if update_form.is_valid():
            update_form.save()

            return redirect(f'/board/{post.pk}')

    return render(request, 'comment_update.html', {'my_com': my_com, 'post': post}) """


def comment_delete(request, com_id, pk):
    if not request.session.get('user'):
        return redirect('/user/login/')

    user_id = request.session.get('user')
    post = Post.objects.get(pk=pk)
    my_com = Comment.objects.get(id=com_id)

    if my_com.comment_writer == BoardMember.objects.get(pk=user_id):

        my_com.delete()

        return redirect(f'/board/{post.pk}')

    else:
        return render(request, 'user_mismatch.html')
