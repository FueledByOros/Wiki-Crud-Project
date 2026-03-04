import markdown
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.html import escape

def markdown_to_html(markdown_text):
    safe_text = escape(markdown_text)
    
    html = markdown.markdown(safe_text)

    return mark_safe(html)

def recent_check(article):
    if article.updated_at < timezone.now() - timezone.timedelta(days=2):
        return True
    return False