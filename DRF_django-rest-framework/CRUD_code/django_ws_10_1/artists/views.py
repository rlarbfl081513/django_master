from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Artists
from .serializers import ArtistsSerializer,ArtistsListSerializer, ArtistsEditSerializer

# Create your views here.
@api_view(['POST'])
def artists_create(request):
  # post는 생성을 말함
  # 만약 보낸 요청이 post라면 
  if request.method == 'POST':
    # 1. ArtistsSerializer는 클래스임 
      # forms.ModelForm처럼 
      # DRF에서는 serilzers.ModelSerializer를 상속한 클래스를 만들어서 도델데이터와 JSON데이터를 변환해줌 
      # reuqest.data는 사용자가 요청으로 보낸 데이터(post 요청의본문문)
      # ArtistsSerializer(data=request.data)는 인스턴스를 생성하는 코드임 
    serializer = ArtistsSerializer(data=request.data)
    # 작성된 데이터가 유효하다면 저장하라 
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      # 데이터 생성에 성공했다는 http
      # JSON의 응답으로 다시 사용자에게 돌려준다
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
    
    

@api_view(['GET'])    
def artists_list(request):
  # 요청이 get일떄떄
  if request.method == 'GET':
      # Artists라는 querySet의 데이터를 다 받아와와
      artist = Artists.objects.all()
      # 그 다 받아온 정보는 이제 JSON으로 변환하는 거지
      # many라는 옵션으로 여러개의 데이터를변환할수 있도록 한거지지
      all_info = ArtistsListSerializer(artist, many=True)
      # 그렇게 변환한 데이터를 응답으로 보내는 거지 
      return Response(all_info.data)
  
## 상세 페이지 
@api_view(['GET','PUT','DELETE'])    
def artists_detail(request,page_pk):
  artist = Artists.objects.get(pk=page_pk)

  # 디테일 페이지 보기
  if request.method == 'GET':
      serializer = ArtistsSerializer(artist)
      return Response(serializer.data)
  
  # 정보 수정하기, agnecy와 debut_data만 수정가능하게 하기 
  elif request.method == 'PUT':
     serializer = ArtistsEditSerializer(artist, request.data)
     if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
     return Response(status=status.HTTP_400_BAD_REQUEST)
  
  # 삭제 하기 
  elif request.method == 'DELETE':
     # 삭제되기전 정보를 저장해서 아래의 메시지를 전달할떄 쓸수 있도록하기 
     pk = artist.pk
     name = artist.name
     # 삭제하기 
     artist.delete()
     # 응답 메시지 전달하기 
     return Response(
        {'delete' : f"'{pk}'번의 '{name}'을 삭제하였습니다."},
        status=status.HTTP_204_NO_CONTENT
     )