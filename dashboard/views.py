import json
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from core.models import (
    FontSettings,
    HeroSlide,
    HomeVideoSection,
    NavigationItem,
    FooterColumn,
    FooterLink,
    SEOSettings,
    SiteSettings,
)
from menu.models import MenuCategory, MenuItem, AddOn


# ── Auth ──────────────────────────────────────────────────────────────────────

def dashboard_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard_home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard_home')
        messages.error(request, 'მომხმარებლის სახელი ან პაროლი არასწორია.')
    return render(request, 'dashboard/login.html')


def dashboard_logout(request):
    logout(request)
    return redirect('dashboard_login')


# ── Home ──────────────────────────────────────────────────────────────────────

@login_required
def dashboard_home(request):
    stats = {
        'menu_items': MenuItem.objects.count(),
        'categories': MenuCategory.objects.count(),
        'slides': HeroSlide.objects.count(),
        'nav_items': NavigationItem.objects.count(),
    }
    return render(request, 'dashboard/home.html', {'stats': stats})


# ── Site Settings ─────────────────────────────────────────────────────────────

@login_required
def site_settings(request):
    settings = SiteSettings.get_settings()
    if request.method == 'POST':
        fields = [
            'tagline_ka', 'tagline_en', 'phone', 'address_ka', 'address_en',
            'opening_hours_ka', 'opening_hours_en', 'instagram', 'whatsapp',
            'email', 'google_maps_url', 'wolt_url', 'glovo_url',
            'delivery_wolt_icon', 'delivery_glovo_icon', 'delivery_call_icon',
            'delivery_maps_icon', 'delivery_whatsapp_icon', 'menu_iframe_url',
            'about_title_ka', 'about_title_en', 'about_text_ka', 'about_text_en',
        ]
        for field in fields:
            setattr(settings, field, request.POST.get(field, ''))

        settings.menu_loader_enabled = request.POST.get('menu_loader_enabled') == 'on'

        if settings.menu_iframe_url and not settings.menu_iframe_url.startswith('https://'):
            messages.error(request, 'Iframe URL უნდა იწყებოდეს https://-ით.')
            return render(request, 'dashboard/site_settings.html', {'settings': settings})

        for img_field in ['logo', 'logo_dark', 'favicon', 'about_image']:
            if img_field in request.FILES:
                setattr(settings, img_field, request.FILES[img_field])

        settings.save()
        messages.success(request, 'პარამეტრები შენახულია.')
        return redirect('site_settings')
    return render(request, 'dashboard/site_settings.html', {'settings': settings})


@login_required
def font_settings(request):
    settings = FontSettings.get_settings()
    if request.method == 'POST':
        text_fields = [
            'heading_font_en_name', 'heading_font_en_url',
            'body_font_en_name', 'body_font_en_url',
            'heading_font_ka_name', 'body_font_ka_name',
        ]
        for field in text_fields:
            setattr(settings, field, request.POST.get(field, '').strip())

        if request.POST.get('heading_font_ka_file_clear') == 'on':
            settings.heading_font_ka_file = None
        if request.POST.get('body_font_ka_file_clear') == 'on':
            settings.body_font_ka_file = None
        if 'heading_font_ka_file' in request.FILES:
            settings.heading_font_ka_file = request.FILES['heading_font_ka_file']
        if 'body_font_ka_file' in request.FILES:
            settings.body_font_ka_file = request.FILES['body_font_ka_file']

        for url_field in ['heading_font_en_url', 'body_font_en_url']:
            url_value = getattr(settings, url_field)
            if url_value and not url_value.startswith('https://'):
                messages.error(request, 'Google Fonts URL უნდა იწყებოდეს https://-ით.')
                return render(request, 'dashboard/font_settings.html', {'settings': settings})

        try:
            settings.full_clean()
        except ValidationError as exc:
            for messages_list in exc.message_dict.values():
                for message in messages_list:
                    messages.error(request, message)
            return render(request, 'dashboard/font_settings.html', {'settings': settings})

        settings.save()
        messages.success(request, 'ფონტების პარამეტრები შენახულია.')
        return redirect('font_settings')

    return render(request, 'dashboard/font_settings.html', {'settings': settings})


@login_required
def home_video_settings(request):
    section = HomeVideoSection.get_settings()
    if request.method == 'POST':
        section.title_ka = request.POST.get('title_ka', '').strip()
        section.title_en = request.POST.get('title_en', '').strip()
        section.subtitle_ka = request.POST.get('subtitle_ka', '').strip()
        section.subtitle_en = request.POST.get('subtitle_en', '').strip()
        section.effect = request.POST.get('effect', 'split')
        section.is_active = request.POST.get('is_active') == 'on'

        if request.POST.get('video_file_clear') == 'on':
            section.video_file = None
        if 'video_file' in request.FILES:
            section.video_file = request.FILES['video_file']

        try:
            section.full_clean()
        except ValidationError as exc:
            for messages_list in exc.message_dict.values():
                for message in messages_list:
                    messages.error(request, message)
            return render(request, 'dashboard/home_video_settings.html', {'section': section})

        section.save()
        messages.success(request, 'ვიდეო სექცია შენახულია.')
        return redirect('home_video_settings')

    return render(request, 'dashboard/home_video_settings.html', {'section': section})


# ── Sliders ───────────────────────────────────────────────────────────────────

@login_required
def sliders(request):
    slides = HeroSlide.objects.all()
    return render(request, 'dashboard/sliders.html', {'slides': slides})


@login_required
def slider_add(request):
    if request.method == 'POST':
        slide = HeroSlide()
        _save_slide(slide, request)
        messages.success(request, 'სლაიდი დამატებულია.')
        return redirect('sliders')
    return render(request, 'dashboard/slider_form.html', {'slide': None})


@login_required
def slider_edit(request, pk):
    slide = get_object_or_404(HeroSlide, pk=pk)
    if request.method == 'POST':
        _save_slide(slide, request)
        messages.success(request, 'სლაიდი განახლებულია.')
        return redirect('sliders')
    return render(request, 'dashboard/slider_form.html', {'slide': slide})


@login_required
def slider_delete(request, pk):
    slide = get_object_or_404(HeroSlide, pk=pk)
    slide.delete()
    messages.success(request, 'სლაიდი წაშლილია.')
    return redirect('sliders')


def _save_slide(slide, request):
    slide.title_ka = request.POST.get('title_ka', '')
    slide.title_en = request.POST.get('title_en', '')
    slide.subtitle_ka = request.POST.get('subtitle_ka', '')
    slide.subtitle_en = request.POST.get('subtitle_en', '')
    slide.cta_text_ka = request.POST.get('cta_text_ka', '')
    slide.cta_text_en = request.POST.get('cta_text_en', '')
    slide.cta_url = request.POST.get('cta_url', '')
    slide.order = int(request.POST.get('order', 0))
    slide.is_active = request.POST.get('is_active') == 'on'
    if 'image' in request.FILES:
        slide.image = request.FILES['image']
    if request.POST.get('product_image_clear') == 'on':
        slide.product_image = None
    if 'product_image' in request.FILES:
        slide.product_image = request.FILES['product_image']
    slide.save()


# ── Navigation ────────────────────────────────────────────────────────────────

@login_required
def navigation(request):
    items = NavigationItem.objects.all()
    return render(request, 'dashboard/navigation.html', {'items': items})


@login_required
def nav_add(request):
    if request.method == 'POST':
        NavigationItem.objects.create(
            label_ka=request.POST.get('label_ka', ''),
            label_en=request.POST.get('label_en', ''),
            url=request.POST.get('url', ''),
            order=int(request.POST.get('order', 0)),
            is_active=request.POST.get('is_active') == 'on',
            open_new_tab=request.POST.get('open_new_tab') == 'on',
        )
        messages.success(request, 'ნავიგაციის ელემენტი დამატებულია.')
    return redirect('navigation')


@login_required
def nav_edit(request, pk):
    item = get_object_or_404(NavigationItem, pk=pk)
    if request.method == 'POST':
        item.label_ka = request.POST.get('label_ka', '')
        item.label_en = request.POST.get('label_en', '')
        item.url = request.POST.get('url', '')
        item.order = int(request.POST.get('order', 0))
        item.is_active = request.POST.get('is_active') == 'on'
        item.open_new_tab = request.POST.get('open_new_tab') == 'on'
        item.save()
        messages.success(request, 'განახლებულია.')
        return redirect('navigation')
    return render(request, 'dashboard/nav_form.html', {'item': item})


@login_required
def nav_delete(request, pk):
    get_object_or_404(NavigationItem, pk=pk).delete()
    messages.success(request, 'ელემენტი წაშლილია.')
    return redirect('navigation')


@require_POST
@login_required
def nav_reorder(request):
    data = json.loads(request.body)
    for item_data in data:
        NavigationItem.objects.filter(pk=item_data['id']).update(order=item_data['order'])
    return JsonResponse({'status': 'ok'})


# ── Footer ────────────────────────────────────────────────────────────────────

@login_required
def footer(request):
    columns = FooterColumn.objects.prefetch_related('links').all()
    return render(request, 'dashboard/footer.html', {'columns': columns})


@login_required
def footer_column_add(request):
    if request.method == 'POST':
        FooterColumn.objects.create(
            title_ka=request.POST.get('title_ka', ''),
            title_en=request.POST.get('title_en', ''),
            order=int(request.POST.get('order', 0)),
        )
        messages.success(request, 'სვეტი დამატებულია.')
    return redirect('footer')


@login_required
def footer_column_delete(request, pk):
    get_object_or_404(FooterColumn, pk=pk).delete()
    messages.success(request, 'სვეტი წაშლილია.')
    return redirect('footer')


@login_required
def footer_link_add(request):
    if request.method == 'POST':
        FooterLink.objects.create(
            column_id=request.POST.get('column_id') or None,
            label_ka=request.POST.get('label_ka', ''),
            label_en=request.POST.get('label_en', ''),
            url=request.POST.get('url', ''),
            order=int(request.POST.get('order', 0)),
            is_active=request.POST.get('is_active') == 'on',
            open_new_tab=request.POST.get('open_new_tab') == 'on',
        )
        messages.success(request, 'ლინკი დამატებულია.')
    return redirect('footer')


@login_required
def footer_link_delete(request, pk):
    get_object_or_404(FooterLink, pk=pk).delete()
    messages.success(request, 'ლინკი წაშლილია.')
    return redirect('footer')


# ── SEO ───────────────────────────────────────────────────────────────────────

@login_required
def seo_settings(request):
    pages = ['home', 'menu', 'salumeria']
    seo_objects = {}
    for p in pages:
        obj, _ = SEOSettings.objects.get_or_create(page=p)
        seo_objects[p] = obj

    if request.method == 'POST':
        page = request.POST.get('page')
        if page in pages:
            obj = seo_objects[page]
            obj.title_ka = request.POST.get('title_ka', '')
            obj.title_en = request.POST.get('title_en', '')
            obj.description_ka = request.POST.get('description_ka', '')
            obj.description_en = request.POST.get('description_en', '')
            obj.keywords = request.POST.get('keywords', '')
            if 'og_image' in request.FILES:
                obj.og_image = request.FILES['og_image']
            obj.save()
            messages.success(request, f'SEO ({page}) შენახულია.')
        return redirect('seo_settings')

    return render(request, 'dashboard/seo_settings.html', {'seo_objects': seo_objects})


# ── Menu Categories ───────────────────────────────────────────────────────────

@login_required
def menu_categories(request):
    cats = MenuCategory.objects.all()
    return render(request, 'dashboard/menu_categories.html', {'categories': cats})


@login_required
def category_add(request):
    if request.method == 'POST':
        MenuCategory.objects.create(
            name_ka=request.POST.get('name_ka', ''),
            name_en=request.POST.get('name_en', ''),
            slug=request.POST.get('slug', ''),
            description_ka=request.POST.get('description_ka', ''),
            description_en=request.POST.get('description_en', ''),
            page=request.POST.get('page', 'menu'),
            order=int(request.POST.get('order', 0)),
            is_active=request.POST.get('is_active') == 'on',
        )
        messages.success(request, 'კატეგორია დამატებულია.')
    return redirect('menu_categories')


@login_required
def category_edit(request, pk):
    cat = get_object_or_404(MenuCategory, pk=pk)
    if request.method == 'POST':
        cat.name_ka = request.POST.get('name_ka', '')
        cat.name_en = request.POST.get('name_en', '')
        cat.slug = request.POST.get('slug', '')
        cat.description_ka = request.POST.get('description_ka', '')
        cat.description_en = request.POST.get('description_en', '')
        cat.page = request.POST.get('page', 'menu')
        cat.order = int(request.POST.get('order', 0))
        cat.is_active = request.POST.get('is_active') == 'on'
        cat.save()
        messages.success(request, 'კატეგორია განახლებულია.')
        return redirect('menu_categories')
    return render(request, 'dashboard/category_form.html', {'cat': cat})


@login_required
def category_delete(request, pk):
    get_object_or_404(MenuCategory, pk=pk).delete()
    messages.success(request, 'კატეგორია წაშლილია.')
    return redirect('menu_categories')


@require_POST
@login_required
def category_reorder(request):
    data = json.loads(request.body)
    for item in data:
        MenuCategory.objects.filter(pk=item['id']).update(order=item['order'])
    return JsonResponse({'status': 'ok'})


# ── Menu Items ────────────────────────────────────────────────────────────────

@login_required
def menu_items(request, category_pk=None):
    categories = MenuCategory.objects.all()
    if category_pk:
        category = get_object_or_404(MenuCategory, pk=category_pk)
        items = MenuItem.objects.filter(category=category)
    else:
        category = None
        items = MenuItem.objects.select_related('category').all()
    return render(request, 'dashboard/menu_items.html', {
        'items': items,
        'categories': categories,
        'active_category': category,
    })


@login_required
def item_add(request):
    categories = MenuCategory.objects.all()
    if request.method == 'POST':
        item = MenuItem()
        _save_item(item, request)
        messages.success(request, 'პროდუქტი დამატებულია.')
        return redirect('menu_items')
    return render(request, 'dashboard/item_form.html', {'item': None, 'categories': categories})


@login_required
def item_edit(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    categories = MenuCategory.objects.all()
    if request.method == 'POST':
        _save_item(item, request)
        messages.success(request, 'პროდუქტი განახლებულია.')
        return redirect('menu_items')
    return render(request, 'dashboard/item_form.html', {'item': item, 'categories': categories})


@login_required
def item_delete(request, pk):
    get_object_or_404(MenuItem, pk=pk).delete()
    messages.success(request, 'პროდუქტი წაშლილია.')
    return redirect('menu_items')


@require_POST
@login_required
def item_reorder(request):
    data = json.loads(request.body)
    for i in data:
        MenuItem.objects.filter(pk=i['id']).update(order=i['order'])
    return JsonResponse({'status': 'ok'})


def _save_item(item, request):
    item.category_id = request.POST.get('category')
    item.name_ka = request.POST.get('name_ka', '')
    item.name_en = request.POST.get('name_en', '')
    item.description_ka = request.POST.get('description_ka', '')
    item.description_en = request.POST.get('description_en', '')
    item.price = request.POST.get('price', 0)
    item.price_unit = request.POST.get('price_unit', '')
    item.order = int(request.POST.get('order', 0))
    item.is_available = request.POST.get('is_available') == 'on'
    item.is_featured = request.POST.get('is_featured') == 'on'
    item.tags = request.POST.get('tags', '')
    item.badge_ka = request.POST.get('badge_ka', '')
    item.badge_en = request.POST.get('badge_en', '')
    if 'image' in request.FILES:
        item.image = request.FILES['image']
    item.save()


# ── Add-ons ───────────────────────────────────────────────────────────────────

@login_required
def addons(request):
    addon_list = AddOn.objects.all()
    return render(request, 'dashboard/addons.html', {'addons': addon_list})


@login_required
def addon_add(request):
    if request.method == 'POST':
        AddOn.objects.create(
            name_ka=request.POST.get('name_ka', ''),
            name_en=request.POST.get('name_en', ''),
            price=request.POST.get('price', 0),
            is_available=request.POST.get('is_available') == 'on',
            order=int(request.POST.get('order', 0)),
        )
        messages.success(request, 'Add-on დამატებულია.')
    return redirect('addons')


@login_required
def addon_delete(request, pk):
    get_object_or_404(AddOn, pk=pk).delete()
    messages.success(request, 'Add-on წაშლილია.')
    return redirect('addons')
