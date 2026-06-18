from django.shortcuts import render, redirect
from .models import HomeVideoSection, SiteSettings, HeroSlide, SEOSettings
from menu.models import MenuCategory, MenuItem


def set_language(request, lang):
    if lang in ('ka', 'en'):
        request.session['lang'] = lang
    referer = request.META.get('HTTP_REFERER', '/')
    return redirect(referer)


def home(request):
    lang = request.session.get('lang', 'ka')
    slides = list(HeroSlide.objects.filter(is_active=True))
    home_video_section = HomeVideoSection.get_settings()
    featured_items = list(
        MenuItem.objects.filter(is_featured=True, is_available=True).select_related('category')[:8]
    )
    if not featured_items:
        featured_items = list(
            MenuItem.objects.filter(is_available=True).select_related('category')[:8]
        )
    seo = SEOSettings.objects.filter(page='home').first()

    return render(request, 'public/home.html', {
        'slides': slides,
        'hero_slide': slides[0] if slides else None,
        'home_video_section': home_video_section,
        'featured_items': featured_items,
        'seo': seo,
        'lang': lang,
    })


def menu_page(request):
    lang = request.session.get('lang', 'ka')
    categories = MenuCategory.objects.filter(
        is_active=True, page='menu'
    ).prefetch_related('items')
    seo = SEOSettings.objects.filter(page='menu').first()

    return render(request, 'public/menu.html', {
        'categories': categories,
        'seo': seo,
        'lang': lang,
    })


def contact_page(request):
    lang = request.session.get('lang', 'ka')
    return render(request, 'public/contact.html', {'lang': lang})


def salumeria_page(request):
    lang = request.session.get('lang', 'ka')
    categories = MenuCategory.objects.filter(
        is_active=True, page='salumeria'
    ).prefetch_related('items')
    seo = SEOSettings.objects.filter(page='salumeria').first()

    return render(request, 'public/salumeria.html', {
        'categories': categories,
        'seo': seo,
        'lang': lang,
    })
