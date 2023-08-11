from django.shortcuts import render,get_object_or_404
from djangogram.users.models import User as user_model
from . import models,serializers
from .forms import CreatePostForm
from django.db.models import Q
# Create your views here.
def index(request):
    if request.method =="GET":
        if request.user.is_authenticated:
            user = get_object_or_404(user_model, pk=request.user.id)
            following = user.following.all()
            posts = models.Post.objects.filter(
                Q(author__in=following) | Q(author=user)
            )
            serializer = serializers.PostSerializer(posts, many=True)
            print(serializer.data)
            #following 이 여러면이면 다 가져옴 -> __in (contain ,gt ,starstwith)
            return render(request,'posts/main.html', {"posts": serializer.data})

def post_create(request):
    if request.method == 'GET': #사용자 페이즈 요청
        form = CreatePostForm()
        return render(request, 'posts/post_create.html',{"form":form})
    elif request.method =='POST':
        if request.user.is_authenticated: #로그인이 되었으면 
            user = get_object_or_404(user_model, pk=request.user.id)
            # image = request.FILES['image']
            # caption = request.POST['caption']

            # new_post =models.Post.objects.create(
            #     author = user,
            #     image = image,
            #     caption = caption
            # )
            # new_post.save()
            form = CreatePostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = user
                post.save() #데이터 베이스 내부에 저장 됨
            else:
                print(form.errors)

            return render(request, 'posts/main.html')
        else:
            return render(request,'users/main.html')