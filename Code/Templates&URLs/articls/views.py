from django.shortcuts import render
import random

# Create your views here.
def index(request):
    query = request.GET.get('query')
    context = {'query': query}
    # print(request)          # <WSGIRequest: GET '/articls/?query=ssafy'>
    # print(type(request))    # <class 'django.core.handlers.wsgi.WSGIRequest'>
    # print(dir(request))
    # print(request.GET)      # <QueryDict: {'query': ['ssafy']}>
    # print(request.GET.get('query'))  # ssafy
    
    # context라는 딕셔너리값을 articls/index.html여기서 활용할 수 있게 해주는 거임
    return render(request, 'articls/index.html',context)

    # "사용자의 요청(request)을 받아서, 템플릿(html)을 context 데이터와 함께 렌더링해서, 브라우저에 보여주는 것!"
        # 사용자가 요청하면
        # → 서버(Django)가 응답할 html을 렌더링(render)해서
        # → 변수(context)를 넣고
        # → 완성된 페이지를 사용자에게 보내주는 구조
        
    # render()함수는 "HTML + 데이터"를 합쳐서 브라우저에 보여주는 역할
    # 3가지 인자 설명
        # request : 사용자가 보낸 HTTP 요청 정보가 담긴 객체야
        # html경로 : 어떤 템플릿 파일을 사용할지 알려주는 경로, Django는 이걸 찾아서 HTML 구조를 읽고 -> 그 안에 들어갈 데이터와 같이 "렌더링"해줌
        # context : 템플릿에서 사용할 **데이터(변수들)**를 담은 딕셔너리

def dinner(request):
    foods = ['국밥','국수','카레','탕수육']
    picked = random.choice(foods)
    
    goods = {
        '한식' : ['밥','국','김치'],
        '양식' : ['스테이크','스파게티','리조토'],
        '중식' : ['탕수육','자장면','마라탕'],
        '일식' : ['오사카','도쿄','초밥'],
    }
    goods_pick = random.choice(list(goods.keys()))
    pickes_good = goods[goods_pick]
    
    context = {
        'foods' : foods,
        'picked' : picked,
        'goods_pick' : goods_pick,
        'pickes_good' : pickes_good,
    }
    
    return render(request, 'articls/dinner.html',context)

def search(request):
    return render(request, 'articls/search.html')

def detail(request, num):
    context = {
        'num' : num,
    }
    return render(request, 'articls/detail.html', context)