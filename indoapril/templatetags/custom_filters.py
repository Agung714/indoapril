from django import template

register = template.Library()

@register.filter
def dot_separator(value):
    try:
        value = float(value)  # Pastikan nilainya float
        return f"{value:,.0f}".replace(",", ".")  # Format dengan titik sebagai pemisah ribuan
    except (ValueError, TypeError):
        return value  # Jika tidak bisa diformat, kembalikan nilai asli
