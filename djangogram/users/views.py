from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .forms import SignUpForm

@csrf_exempt
def main(request):
    print("ㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎ")

    if request.method =='GET':
        return render(request,'users/main.html')
    elif request.method =='POST':

        username = request.POST["username"]
        password = request.POST["password"]
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("posts:index")
            # return HttpResponseRedirect(reverse('posts:index'))
           
        else:
            return render(request, 'users/main.html')
def signup(request):
    if request.method == "GET":
        form = SignUpForm()
        return render(request,'users/signup.html',{'form':form})


    elif request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save() #User DB에 바로 저장
            #저장 후 유효한 데이터는 cleaned_data 에 저장
            username=form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("posts:index")
                # return HttpResponseRedirect(reverse('posts:index'))
            
      
        return render(request, 'users/main.html')

            
         

    