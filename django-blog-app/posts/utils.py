
from .models import Post
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import redirect


def search(request):
    search_value = request.GET.get('search')
    all_posts = Post.objects.filter(
        Q(body__icontains=search_value) |
        Q(title__icontains=search_value) |
        Q(created__icontains=search_value) |
        Q(owner__username__icontains=search_value)
    )

    # search_value = ''
    paginator = Paginator(all_posts, 2)

    return {
        'paginator': paginator,
        'search_value': search_value
    }

