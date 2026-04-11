from django import template
from django.utils.safestring import mark_safe

register = template.Library()

CATEGORY_ICONS = {
    # Coffee cup with steam lines
    'café':       '<path d="M18 8h1a4 4 0 0 1 0 8h-1"/><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"/><line x1="6" y1="1" x2="6" y2="4"/><line x1="10" y1="1" x2="10" y2="4"/><line x1="14" y1="1" x2="14" y2="4"/>',
    'cafe':       '<path d="M18 8h1a4 4 0 0 1 0 8h-1"/><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"/><line x1="6" y1="1" x2="6" y2="4"/><line x1="10" y1="1" x2="10" y2="4"/><line x1="14" y1="1" x2="14" y2="4"/>',
    # Burger bun + patty
    'fast food':  '<path d="M3 14h18v2a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4v-2z"/><path d="M5 14v-2c0-3.3 3.1-6 7-6s7 2.7 7 6v2"/><line x1="3" y1="10" x2="21" y2="10"/>',
    # Vertical skewer with meat pieces
    'kebab':      '<line x1="12" y1="2" x2="12" y2="22"/><rect x="9" y="5" width="6" height="4" rx="1"/><rect x="9" y="11" width="6" height="4" rx="1"/><rect x="9" y="17" width="6" height="3" rx="1"/>',
    # Chopsticks
    'japanese':   '<line x1="5" y1="3" x2="9" y2="21"/><line x1="19" y1="3" x2="15" y2="21"/><path d="M7 14h10"/><path d="M6 9h12"/>',
    # Pizza slice
    'italian':    '<path d="M12 2L3 21h18L12 2z"/><circle cx="10" cy="14" r="1"/><circle cx="14" cy="14" r="1"/><circle cx="12" cy="17.5" r="1"/>',
    # Fish silhouette
    'seafood':    '<path d="M20 12s-4-7-9-7-7 3-7 7 2 7 7 7 9-7 9-7z"/><path d="M22 7v10l-2-5z"/><circle cx="9" cy="12" r="1.5"/>',
    # Fork and knife (utensils)
    'steakhouse': '<line x1="8" y1="2" x2="8" y2="22"/><path d="M5 2v6a3 3 0 0 0 6 0V2"/><line x1="16" y1="2" x2="16" y2="22"/><path d="M13 2h6l-1 5a3 3 0 0 1-4 0z"/>',
    # Bread loaf
    'bakery':     '<path d="M5 9a7 7 0 0 1 14 0v6H5V9z"/><path d="M3 15h18v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-3z"/><line x1="8" y1="13" x2="8" y2="13"/><line x1="12" y1="11" x2="12" y2="11"/><line x1="16" y1="13" x2="16" y2="13"/>',
}

CATEGORY_COLORS = {
    'café':       ('#fdf6f0', '#c8845a'),
    'cafe':       ('#fdf6f0', '#c8845a'),
    'fast food':  ('#fff8f0', '#d4832a'),
    'kebab':      ('#fef5ee', '#c96a30'),
    'japanese':   ('#f0f5ff', '#4a6fa5'),
    'italian':    ('#f0faf4', '#3a8a5a'),
    'seafood':    ('#f0f7ff', '#3a7abf'),
    'steakhouse': ('#fdf0f0', '#a04040'),
    'bakery':     ('#fffbf0', '#b8922a'),
}
DEFAULT_COLOR = ('#f5f5f7', '#adadb8')
DEFAULT_ICON  = '<circle cx="12" cy="8" r="3"/><path d="M5 20a7 7 0 0 1 14 0"/>'


@register.simple_tag
def category_icon(category_name, size=40, color=None):
    name = (category_name or '').lower().strip()
    paths = CATEGORY_ICONS.get(name, DEFAULT_ICON)
    if color is None:
        color = CATEGORY_COLORS.get(name, DEFAULT_COLOR)[1]
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" '
        f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
        f'{paths}</svg>'
    )
    return mark_safe(svg)


@register.simple_tag
def category_bg(category_name):
    name = (category_name or '').lower().strip()
    bg, _ = CATEGORY_COLORS.get(name, DEFAULT_COLOR)
    return bg
