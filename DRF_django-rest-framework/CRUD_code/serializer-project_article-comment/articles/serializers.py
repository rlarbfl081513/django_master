from rest_framework import serializers 
from .models import Article, Comment


# 게시글의 일부 필드를 직렬화 하는 클래스
class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'content',)


# 게시글의 전체 필드를 직렬화 하는 클래스
class ArticleSerializer(serializers.ModelSerializer):


    # comment_set에 활용할 댓글 데이터를 가공하는 도구
    class CommentDetialSerializer(serializers.ModelSerializer):
         class Meta:
              model = Comment
              fields = ('id', 'content',)

    # 기존에 있던 역참조 매니저인 comment_set의 값을 덮어쓰기하자
    comments = CommentDetialSerializer(read_only=True, many=True)

    # 새로운 필드 생성 (댓글 개수를 담기위하 새로운 필드)
    num_of_comments = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'

    # SerializerMethodField의 값을 채울 함수
    def get_num_of_comments(self,obj):
         # 뷰에서 annotate 안쓰고 여기서 그냥 바로 계산해서 리턴되게 할 수도 있음

         # 여기서 obj는 득정 게시글 인스턴스 (3번 게시글이면 3번객체를 가져오게 하는)
         # view함수에서 annotate 해서 생긴 새로운 속성 결과를 사용할수 있게 
         return obj.num_of_comments


# 댓글 
class CommentSerilizer(serializers.ModelSerializer):
        # 외래키  필드 article의 데이터를 재구성하기 위한 도구 
        class ArticleTitleSerializer(serializers.ModelSerializer):
             class Meta:
                  model = Article
                  fields = ('id','title',)
        
        # 외래키 필드인 article의 데이터를 재구성
        article = ArticleTitleSerializer(read_only=True)

        class Meta:
            model = Comment
            fields = '__all__'
            # 외래키를 유효성 검사에서 목록에서 빼야함
            # 그런데 응답 데이터를 포함되어있어햐마
            # 읽기전용 필등로 설정

            # 위에서 재구성을 해버리면 여기 아래의 meta가 적용이 안되서 아래의 코드는 주석처리하고 위에처럼 read-inly를 true처리해야함
            # read_only_fields=('article',)