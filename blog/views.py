from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Post
from .forms import PostForm

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == 'POST':
        # significa que ya se envio la informacion del formulario a traves de post
        form = PostForm(request.POST)
        # reconstruyo el formulario con los datos que me llegan a traves de post

        if form.is_valid():
            post = form.save(commit=False) 
            # guarda el formulario pero con commit=false todavia no lo ingresa a la BD (falta guardar el usuario)
            post.author = request.user
            post.save()
            #ya esta ingresado el post al sitio

            return redirect('post_detail',pk=post.pk)
            # redirige a la pagina detalle del nuevo post
    else:
        form = PostForm()
    return render(request,'blog/post_edit.html',{'form':form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
        return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
