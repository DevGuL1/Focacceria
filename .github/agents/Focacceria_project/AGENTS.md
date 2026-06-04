# Focacceria_project — Agent Notes

> Standalone Django project. This codebase is **not related to OreonCMS**.

## Core conventions

- Public site templates live in `templates/public/`.
- Dashboard templates live in `templates/dashboard/`.
- Global site configuration is stored in the singleton model `core.models.SiteSettings`.
- Site-wide shared context comes from `core.context_processors.site_context`.
- The public theme uses Tailwind CDN config in `templates/public/base.html`.

## Current frontend behavior

- The homepage hero in `templates/public/home.html` now uses the first active `HeroSlide` as the main framed visual and overlays a single large rotating hero product object on top of it.
- That hero product can be uploaded per slide via `HeroSlide.product_image`; when empty, the site falls back to a branded burger placeholder.
- The hero scene responds to scroll by fading/translating downward so the eye is pulled into the next section, with reduced-motion safeguards for accessibility.
- The homepage can also render a dedicated cinematic video section between the hero and menu area via the singleton `core.models.HomeVideoSection`.
- The public typography is now driven by `core.models.FontSettings` through CSS variables in `templates/public/base.html`, so public headings/body copy can switch per language without hardcoded font stacks.
- If no items are marked `is_featured`, the homepage falls back to available menu items so both the orbit cards and featured grid still render content.
- A **Delivery Bar** is rendered globally under the main header from `templates/public/includes/delivery_bar.html`.
- Delivery Bar chips can now render **admin-configurable icon + text** combinations via `SiteSettings.delivery_*_icon` fields.
- Public light/dark theme switching is handled in `templates/public/base.html` with:
  - early theme initialization from `localStorage`
  - runtime CSS variables
  - Tailwind colors defined as `rgb(var(--token) / <alpha-value>)` so opacity utilities keep working
  - extra dark-theme overrides for shared `bg-foca-ink`, header, and footer surfaces so text remains readable on the green-toned dark palette
- The `/menu/` and `/en/menu/` pages now prefer an admin-configured iframe URL from `SiteSettings.menu_iframe_url`.
- If the iframe URL is empty, the local Django-rendered menu remains the fallback.
- The iframe loading overlay is controlled by `SiteSettings.menu_loader_enabled`.

## Dashboard settings

The dashboard site settings page now controls:

- `menu_iframe_url`
- `menu_loader_enabled`
- `delivery_wolt_icon`
- `delivery_glovo_icon`
- `delivery_call_icon`
- `delivery_maps_icon`
- `delivery_whatsapp_icon`

Validation rule:

- iframe URLs should start with `https://`

## Dedicated dashboard pages

- `/dashboard/fonts/` manages English Google Fonts plus Georgian custom heading/body font files.
- `/dashboard/home-video/` manages the homepage reveal video file, effect style, active toggle, and localized texts.

## Hero slider note

- The public homepage currently uses the **first active slide** as its hero source.
- `HeroSlide.image` remains the framed background visual.
- `HeroSlide.product_image` is the large rotating foreground object intended for transparent burger/product cutouts.

## Important note

If future work touches this project, keep documentation here under the dedicated `Focacceria_project` agent folder so it does not get mixed with OreonCMS notes.
