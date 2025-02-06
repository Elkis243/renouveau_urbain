from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import InMemoryUploadedFile

MAX_IMAGE_SIZE = 5 * 1024 * 1024


def home(request):
    current_link = "home"
    recent_articles = Article.objects.filter(published=True).order_by(
        "-publication_date"
    )[:4]
    return render(
        request,
        "app/home.html",
        {"recent_articles": recent_articles, "current_link": current_link},
    )


def about(request):
    current_link = "about"
    return render(request, "app/about.html", {"current_link": current_link})


def contact(request):
    current_link = "contact"
    if request.method == "POST":
        recipient = request.POST.get("email")
        subject = request.POST.get("objet")
        message = request.POST.get("message")
        sender = settings.EMAIL_HOST_USER

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=sender,
                recipient_list=[recipient],
                fail_silently=False,
            )
            messages.success(
                request,
                "Votre message a été envoyé avec succès. Nous vous répondrons bientôt !",
            )
        except Exception as e:
            messages.error(
                request,
                f"Une erreur s'est produite lors de l'envoi de votre message : {str(e)}",
            )

        return HttpResponseRedirect("/about/")

    return render(request, "app/contact.html", {"current_link": current_link})


def blog(request):
    current_link = "blog"
    articles_list = Article.objects.filter(published=True).order_by("-publication_date")
    paginator = Paginator(articles_list, 8)

    page_number = request.GET.get("page")
    articles = paginator.get_page(page_number)

    return render(
        request, "app/blog.html", {"articles": articles, "current_link": current_link}
    )


def signin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
    return render(request, "app/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, published=True)
    return render(
        request,
        "app/article_detail.html",
        {"article": article, "object_or_url": request.build_absolute_uri()},
    )


@login_required
def admin_panel(request):
    current_link = "Article"
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        image = request.FILES.get("image")

        slug = slugify(title)

        if Article.objects.filter(slug=slug).exists():
            messages.error(request, "Le slug est déjà utilisé. Veuillez choisir un autre titre !")
            return redirect("admin_panel")

        if image:
            if isinstance(image, InMemoryUploadedFile) and image.size > MAX_IMAGE_SIZE:
                messages.error(request, "L'image est trop lourde ! Taille maximale autorisée : 5 Mo !")
                return redirect("admin_panel")

        Article.objects.create(
            title=title,
            description=content,
            image=image,
            published=True,
            user=request.user,
            slug=slug,
        )

        messages.success(request, "Article ajouté avec succès, consulter la page blog !")
        return HttpResponseRedirect("/admin_panel/")

    return render(request, "app/admin.html", {"current_link": current_link})


@login_required
def delete_article(request, slug):
    article = get_object_or_404(Article, slug=slug, published=True)
    article.published = False
    article.save()
    return HttpResponseRedirect("/blog/")


@login_required
def edit_article(request, slug):
    article = get_object_or_404(Article, slug=slug, published=True)

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        image = request.FILES.get("image")

        if image:
            if isinstance(image, InMemoryUploadedFile) and image.size > MAX_IMAGE_SIZE:
                messages.error(
                    request,
                    "L'image est trop lourde ! Taille maximale autorisée : 5 Mo.",
                )
        article.title = title
        article.description = content
        article.image = image

        article.save()
        return HttpResponseRedirect("/blog/")

    return render(request, "app/article_edit.html", {"article": article})
