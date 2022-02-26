from django.db import models


# 게시판 관련 모델
class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="제목")
    contents = models.TextField(verbose_name="내용")
    img = models.ImageField(verbose_name="이미지", null=True, blank=True)
    writer = models.ForeignKey(
        'user.BoardMember', on_delete=models.CASCADE, null=True, verbose_name="작성자")
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, verbose_name="작성일")
    updated_at = models.DateTimeField(
        auto_now=True, null=True, verbose_name="최종수정일")
    view_count = models.PositiveIntegerField(default=0, verbose_name="조회수")
    like_count = models.IntegerField(null=True, verbose_name="좋아요수")
    name_choices = (('직업리뷰', '직업리뷰'), ('학과리뷰', '학과리뷰'))
    name = models.CharField(
        max_length=200, null=True, choices=name_choices, verbose_name="게시판명")
    # choiceField는 존재하지않음 튜플 형태로 charField에 넣어주는 형태로 만들 수 있음

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'boards'
        verbose_name = '게시판'
        verbose_name_plural = '게시판'


class Comment(models.Model):
    comment = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    # comment : 게시글과 댓글이 연결되어 게시글이 삭제되면 댓글도 삭제 됨 (on_delete)
    comment_writer = models.ForeignKey(
        'user.BoardMember', on_delete=models.CASCADE, null=True, verbose_name="댓글작성자")
    comment_contents = models.CharField('댓글작성', max_length=100)
    # '댓글작성'으로 준 이유는 Forms 에서 label을 '댓글작성'으로 주기 위해
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, verbose_name="작성일")
    updated_at = models.DateTimeField(
        auto_now=True, null=True, verbose_name="최종수정일")

    def __str__(self):
        return self.comment_contents
    # __str__ 함수는 문자열로 리턴해주는 함수이다.
