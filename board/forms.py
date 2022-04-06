from xml.etree.ElementTree import Comment
from django.contrib.auth.hashers import check_password

from django import forms
from board.models import Post, Comment, Photo


class BoardForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'name',
            'title',
            'contents',
        ]

    name_choices = (('직업리뷰', '직업리뷰'), ('학과리뷰', '학과리뷰'))

    name = forms.ChoiceField(error_messages={
        'required': '게시판명을 선택하세요.'},
        choices=name_choices, label="게시판명")

    title = forms.CharField(error_messages={
        'required': '제목을 입력하세요.'
    }, max_length=100, label="게시글 제목")

    contents = forms.CharField(error_messages={
        'required': '내용을 입력하세요.'
    }, widget=forms.Textarea, label="게시글 내용")

# 기존 BoardForm에 있던 img를 ImageForm으로 따로 떼어냄


class ImageForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['img']


# 이미지를 가져와 엮어서 폼셋을 만들어주는 역할
# 여기서 Post와 Photo 가 1:N 관계를 형성하고 form=폼 이름과 extra=이미지 갯수를 지정해줌
ImageFormSet = forms.inlineformset_factory(
    Post, Photo, form=ImageForm, extra=3)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment

        fields = ['comment_contents', ]
