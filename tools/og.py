"""Genera las imágenes de vista previa (1200x630) de assets/og/ y los iconos.

    python3 tools/og.py

Descarga fuentes y fotos a ~/.cache/amatuspalabras-og la primera vez. Necesita Pillow y rsvg-convert.
"""
import pathlib, subprocess, urllib.request
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

R = pathlib.Path(__file__).resolve().parent.parent
OUT = R / 'assets' / 'og'
CACHE = pathlib.Path.home() / '.cache' / 'amatuspalabras-og'

FUENTES = {
    'serif.ttf': 'https://raw.githubusercontent.com/google/fonts/main/ofl/instrumentserif/InstrumentSerif-Regular.ttf',
    'serif-i.ttf': 'https://raw.githubusercontent.com/google/fonts/main/ofl/instrumentserif/InstrumentSerif-Italic.ttf',
    'sans.ttf': 'https://raw.githubusercontent.com/google/fonts/main/ofl/inter/Inter%5Bopsz,wght%5D.ttf',
}

K = 2
W, H = 1200 * K, 630 * K
INK, MUTED, FAINT, ACCENT = '#ffffff', (255, 255, 255, 214), (255, 255, 255, 150), '#a7ecd3'


def cache(nombre):
    f = CACHE / nombre
    if not f.exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(FUENTES[nombre], f)
    return str(f)


def sans(size, weight=400):
    f = ImageFont.truetype(cache('sans.ttf'), size * K)
    try:
        f.set_variation_by_axes([14, weight])
    except Exception:
        pass
    return f


MARK_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="{s}" height="{s}">
<rect width="32" height="32" rx="{rx}" fill="{bg}"/>
<g transform="translate({o} {o}) scale({sc})">
<circle cx="16" cy="16" r="14.5" fill="none" stroke="{c}" stroke-width="1.2"/>
<path d="M10.5 19.5c0-3.6 1.6-6.4 4.4-8l.7 1c-1.7 1.2-2.6 2.6-2.8 4.3.4-.2.8-.3 1.3-.3 1.4 0 2.4 1 2.4 2.4 0 1.5-1.1 2.6-2.6 2.6-2 0-3.4-1.4-3.4-2zM17.6 19.5c0-3.6 1.6-6.4 4.4-8l.7 1c-1.7 1.2-2.6 2.6-2.8 4.3.4-.2.8-.3 1.3-.3 1.4 0 2.4 1 2.4 2.4 0 1.5-1.1 2.6-2.6 2.6-2 0-3.4-1.4-3.4-2z" fill="{c}"/>
</g></svg>'''


def mark(size, color=ACCENT, bg='none', pad=0.0, rx=0):
    svg = MARK_SVG.format(s=size, c=color, bg=bg, rx=rx, o=32 * pad, sc=1 - 2 * pad)
    png = subprocess.run(['rsvg-convert', '-f', 'png'], input=svg.encode(), capture_output=True, check=True).stdout
    return Image.open(BytesIO(png)).convert('RGBA')


def fondo():
    """Degradado azul verdoso como las bandas de la web."""
    a, b, c = (12, 50, 71), (17, 80, 95), (25, 96, 79)
    g = Image.new('RGB', (W, H))
    px = g.load()
    for y in range(0, H, 2):
        for x in range(0, W, 2):
            t = (x / W * .65 + y / H * .35)
            if t < .52:
                u = t / .52; col = tuple(round(a[i] + (b[i] - a[i]) * u) for i in range(3))
            else:
                u = (t - .52) / .48; col = tuple(round(b[i] + (c[i] - b[i]) * u) for i in range(3))
            px[x, y] = px[x + 1, y] = px[x, y + 1] = px[x + 1, y + 1] = col
    return g


FONDO = None


def wrap(draw, text, font, width):
    lines, cur = [], ''
    for w in text.split():
        t = f'{cur} {w}'.strip()
        if draw.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return lines


def card(name, eyebrow, t1, t2, sub, photo, focus=0.5):
    global FONDO
    FONDO = FONDO or fondo()
    im = FONDO.copy().convert('RGBA')
    capa = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)

    px0, py0, px1, py1 = 700 * K, 40 * K, 1160 * K, 590 * K
    pw, ph = px1 - px0, py1 - py0
    foto = Image.open(R / 'assets' / 'img' / f'{photo}-1600.jpg').convert('RGB')
    r = max(pw / foto.width, ph / foto.height)
    foto = foto.resize((round(foto.width * r), round(foto.height * r)), Image.LANCZOS)
    left = (foto.width - pw) // 2
    top = round((foto.height - ph) * focus)
    foto = foto.crop((left, top, left + pw, top + ph))
    mask = Image.new('L', (pw, ph), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, pw, ph), radius=28 * K, fill=255)
    im.paste(foto, (px0, py0), mask)

    x = 64 * K
    m = mark(36 * K)
    im.paste(m, (x, 56 * K), m)
    d.text((x + 50 * K, 74 * K), 'Ama tus palabras', font=sans(24, 500), fill=INK, anchor='lm')

    ey = sans(15, 500)
    y = 190 * K
    d.line((x, y, x + 26 * K, y), fill=ACCENT, width=K)
    cx = x + 38 * K
    for ch in eyebrow.upper():
        d.text((cx, y), ch, font=ey, fill=ACCENT, anchor='lm')
        cx += d.textlength(ch, font=ey) + 2.2 * K

    maxw = 590 * K
    size = 104
    while True:
        f1, f2 = ImageFont.truetype(cache('serif.ttf'), size * K), ImageFont.truetype(cache('serif-i.ttf'), size * K)
        if max(d.textlength(t1, font=f1), d.textlength(t2, font=f2)) <= maxw or size <= 60:
            break
        size -= 2
    lh = size * 0.98 * K
    ty = 222 * K
    d.text((x - 3 * K, ty), t1, font=f1, fill=INK, anchor='la')
    d.text((x - 3 * K, ty + lh), t2, font=f2, fill=ACCENT, anchor='la')

    sf = sans(23, 300)
    sy = ty + 2 * lh + 46 * K
    for ln in wrap(d, sub, sf, 560 * K)[:3]:
        d.text((x, sy), ln, font=sf, fill=MUTED, anchor='la')
        sy += 34 * K

    d.text((x, 578 * K), 'ama-tus-palabras.github.io', font=sans(17, 400), fill=FAINT, anchor='ls')

    im = Image.alpha_composite(im, capa).convert('RGB').resize((1200, 630), Image.LANCZOS)
    im.save(OUT / f'{name}.jpg', quality=88, optimize=True, progressive=True)


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    card('portada', 'Aprender · Comprender · Sentir · Avanzar', 'Ama tus', 'palabras.',
         'Eventos, formaciones y contenidos para parar, comprender, recordar y sentir.', 'cascada2', .45)
    card('eventos', 'Eventos', 'Encuentros', 'en persona.',
         'Próximas fechas de paseos, charlas y encuentros para compartir en grupo.', 'paseo2', .55)
    card('formaciones', 'Formaciones', 'Aprender', 'con calma.',
         'Experiencias de aprendizaje con programa completo, en grupo y en la naturaleza.', 'cascada2', .45)
    card('alimentacion', 'Alimentación', 'Lo que comemos', 'también habla.',
         'La alimentación y el equilibrio del cuerpo, la mente y el alma.', 'huerto', .55)
    card('salud', 'Salud', 'Cuidar', 'lo que sentimos.',
         'Reflexiones para acompañar el duelo, las emociones y las creencias.', 'cascada2', .45)
    card('testimonios', 'Testimonios', 'Lo que', 'nos cuentan.',
         'Experiencias de quienes han compartido con nosotros un encuentro o una formación.', 'casa', .55)
    card('tienda', 'Tienda', 'Libros', 'para seguir.',
         'Libros y recursos del equipo para seguir profundizando en casa.', 'cascada2', .45)
    card('contacto', 'Contacto', 'Hablemos', 'con calma.',
         'Escríbenos para reservar, resolver dudas o recibir información.', 'paseo', .55)
    card('crea-te-a-ti-mismo', '6 y 7 dic 2026 · Bárcena Mayor · 400 € + IVA', 'Créate', 'a ti mismo.',
         'Dos días de aprendizaje y naturaleza en favor de tu bienestar físico-emocional.', 'casa', .55)

    for s in (180, 192, 512):
        ic = mark(s, color='#1f6a62', bg='#fafaf8', pad=0.16).convert('RGB')
        ic.save(R / 'assets' / ('apple-touch-icon.png' if s == 180 else f'icon-{s}.png'), optimize=True)


if __name__ == '__main__':
    build()
