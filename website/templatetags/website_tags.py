from django import template
from django.utils import timezone

from blog.models import Post

register = template.Library()


@register.inclusion_tag("website/website-recent-blog-area.html")
def latestposts(arg=6):
    posts = Post.objects.filter(status=1, published_date__lte=timezone.now()).order_by(
        "published_date"
    )[:arg]
    return {"posts": posts}
