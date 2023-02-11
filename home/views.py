from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from home.models import Post, BlogComment
from home.templatetags import extras

# Create your views here.

def home(request):
    post = Post.objects.latest('timeStampt')
    return render(request, 'index.html', {'post' : post})

def register(request):
    if request.user.is_authenticated:
        return redirect("/")
    return render(request, 'register.html')

def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    return render(request, 'login.html')

def about(request):
    return render(request, 'about.html')

def blog(request):
    allPosts = Post.objects.all()
    context = {'allPosts' : allPosts}
    return render(request, 'blog.html', context)

def error_404(request, exception):
    return render(request, 'error404.html')

def handleRegister(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            return redirect("/")
        
        username = request.POST['username'].lower()
        email = request.POST['email']
        password = request.POST['password']

        if len(username) > 15:
            messages.error(request, "Username you have entered is more than 15 albhabets. Please Try Again")
            return redirect("register")
        
        if username.isalnum() != True:
            messages.error(request, "Username should only contain letters and numbers")
            return redirect("register")
        
        if get_user_model().objects.filter(username=username).exists():
            messages.error(request, "This Username Already Exists")
            return redirect('register')
        
        if get_user_model().objects.filter(email=email).exists():
            messages.error(request, "This Email Already Exists")
            return redirect('register')

        user = User.objects.create_user(username, email, password)
        user.save()

        messages.success(request, "Your DebCoders Account Has Been Successfuly Created")
        return redirect('/')

    else:
        return render(request, "error404.html")
    
def handleLogin(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            return redirect("/")
        
        username = request.POST['username'].lower()
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Successfully Logged In As {username}")
            return redirect('/')
        
        else:
            messages.error(request, "Invalid Credentials, Please Try Again")
            return redirect("login")

    else:
        return render(request, "error404.html")

@login_required
def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out!")
    return redirect("/")

@login_required
def account_info(request):
    email = request.user.email
    username = request.user.username
    context = {'email' : email, 'username' : username}
    return render(request, 'account_info.html', context)

def blogPost(request, sno):
    post = Post.objects.filter(sno=sno).first()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
            
        else:
            replyDict[reply.parent.sno].append(reply)

    context = {'post' : post, 'comments' : comments, 'replyDict' : replyDict}
    return render(request, "blogPost.html", context)
    
def search(request):
    query = request.GET['search']
    if len(query) > 89:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)

    params = {'allPosts' : allPosts, 'query' : query}
    return render(request, "search.html", params)

def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get("parentSno")

        if parentSno == "":
            comment_c = BlogComment(comment=comment, user=user, post=post)
            comment_c.save()

            messages.success(request, "Your comment has been posted successfully")
        
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment_reply = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment_reply.save()

            messages.success(request, "Your reply has been posted successfully")
    
    return redirect(f'/blogPost/{postSno}')

@login_required
def deleteComment(request):
    if request.method == "POST":
        comment_sno = request.POST.get('comment_sno')
        blog_sno = request.POST.get('blog_sno')
        comment_obj = BlogComment.objects.filter(sno=comment_sno).first()
        comment_obj.delete()
        messages.success(request, "Your comment has been deleted successfully")
        return redirect(f"/blogPost/{blog_sno}")
    
    else:
        return render(request, "error404.html")