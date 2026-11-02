"""Genera todas las páginas de la web. Es la única fuente: editar aquí y ejecutar

    python3 tools/build.py

desde la raíz del repo. Los datos que cambian a menudo (contacto, precio, enlaces) están arriba.
"""
import pathlib

R = pathlib.Path(__file__).resolve().parent.parent
BASE = 'https://ama-tus-palabras.github.io/'

# ---------- Datos de contacto y enlaces (vacío = aún no lo tenemos y no se muestra como enlace)
EMAIL = 'federico@fe-derico.com'
WHATSAPP = '34606448325'   # solo dígitos con prefijo
YOUTUBE = 'https://www.youtube.com/@AmaTusPalabras'
REDES = {}             # {'Instagram': 'https://...', 'Facebook': 'https://...'}
LEMA = 'Aprender · Comprender · Sentir · Avanzar · Recordar'
EQUIPO = 'Abel, Cristina, Marisol y Federico José'

# Créate a ti mismo
PRECIO = 400
RESERVA_PCT = 30
NOCHE_EXTRA = '200 €'
IVA = ' + IVA'        # los precios se publican sin IVA

MARK = '<svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="16" r="14.5" fill="none" stroke="currentColor" stroke-width="1.2"/><path d="M10.5 19.5c0-3.6 1.6-6.4 4.4-8l.7 1c-1.7 1.2-2.6 2.6-2.8 4.3.4-.2.8-.3 1.3-.3 1.4 0 2.4 1 2.4 2.4 0 1.5-1.1 2.6-2.6 2.6-2 0-3.4-1.4-3.4-2zM17.6 19.5c0-3.6 1.6-6.4 4.4-8l.7 1c-1.7 1.2-2.6 2.6-2.8 4.3.4-.2.8-.3 1.3-.3 1.4 0 2.4 1 2.4 2.4 0 1.5-1.1 2.6-2.6 2.6-2 0-3.4-1.4-3.4-2z" fill="currentColor"/></svg>'

NAV = [('eventos', 'Eventos'), ('formaciones', 'Formaciones'), ('alimentacion', 'Alimentación'), ('salud', 'Salud'),
       ('testimonios', 'Testimonios'), ('tienda', 'Tienda'), ('contacto', 'Contacto')]

AVISO = ('<strong>Aviso.</strong> Ama tus palabras no es un equipo de personal médico ni sanitario certificado. '
         'Todo lo que se publica en esta web y se comparte en nuestros eventos y formaciones tiene un fin divulgativo y de autoconocimiento: '
         'no es diagnóstico, tratamiento ni consejo médico, nutricional o psicológico, y no sustituye la atención de un profesional cualificado. '
         'Lo que leas o pongas en práctica es bajo tu propia responsabilidad: contrasta la información, investiga por tu cuenta y consulta '
         'con un profesional sanitario antes de cambiar tu alimentación, medicación o tratamiento.')

FOREST = '1448375240586-882707db888b'
DEER = '1472396961693-142e6e269027'


def mailto(asunto, cuerpo=''):
    from urllib.parse import quote
    q = f'subject={quote(asunto)}' + (f'&amp;body={quote(cuerpo)}' if cuerpo else '')
    return f'mailto:{EMAIL}?{q}'


def img(id_, alt, sizes, eager=False, widths=(800, 1600, 2400, 3840)):
    u = lambda w: f'https://images.unsplash.com/photo-{id_}?auto=format&amp;fit=crop&amp;w={w}&amp;q=80'
    srcset = ',\n          '.join(f'{u(w)} {w}w' for w in widths)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img src="{u(1600)}"\n          srcset="{srcset}"\n          sizes="{sizes}" alt="{alt}" {load}>'


def page(path, title, desc, section, body):
    depth = path.count('/') + 1 if path else 0
    root = '../' * depth or './'
    pre = '../' * depth
    links = '\n        '.join(
        f'<a href="{pre}{k}/"' + (' aria-current="page"' if k == section else '') + f'>{v}</a>' for k, v in NAV)
    sub = dict(NAV).get(section)
    brand_sub = f' <small>/ {sub}</small>' if sub else ''
    full_title = f'{title} · Ama tus palabras' if title else 'Ama tus palabras'
    url = BASE + (path + '/' if path else '')
    og = BASE + 'assets/og/' + (path.split('/')[-1] if path else 'portada') + '.jpg'
    og_title = title or 'Ama tus palabras'
    html = f'''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="color-scheme" content="light dark">
  <meta name="theme-color" content="#fafaf8" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#0b0c0b" media="(prefers-color-scheme: dark)">
  <meta name="description" content="{desc}">
  <title>{full_title}</title>
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Ama tus palabras">
  <meta property="og:locale" content="es_ES">
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{og}">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{og_title} · Ama tus palabras">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{og_title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{og}">
  <link rel="icon" href="{pre}assets/mark.svg" type="image/svg+xml">
  <link rel="icon" href="{pre}assets/icon-192.png" type="image/png" sizes="192x192">
  <link rel="apple-touch-icon" href="{pre}assets/apple-touch-icon.png">
  <link rel="manifest" href="{pre}manifest.webmanifest">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="{pre}assets/site.css">
</head>
<body>
  <header class="site-header">
    <div class="wrap">
      <a class="brand" href="{root}" aria-label="Ama tus palabras, inicio">
        {MARK}
        <span>Ama tus palabras{brand_sub}</span>
      </a>
      <button class="menu-toggle" aria-expanded="false" aria-controls="nav">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" aria-hidden="true"><path d="M4 8h16M4 16h16"/></svg>
        <span class="sr-only">Abrir menú</span>
      </button>
      <nav class="nav" id="nav">
        {links}
      </nav>
    </div>
  </header>

  <main>
{body.replace("{pre}", pre)}
  </main>

  <footer class="site-footer">
    <div class="wrap">
      <p class="disclaimer">{AVISO}</p>
      <div class="footer-row">
        <span>© 2026 Ama tus palabras · {LEMA}</span>
        <nav>{' '.join(f'<a href="{pre}{k}/">{v}</a>' for k, v in NAV)}</nav>
      </div>
    </div>
  </footer>
  <script src="{pre}assets/site.js"></script>
</body>
</html>
'''
    out = R / path / 'index.html' if path else R / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)


def hero(eyebrow, h1, lead, actions=''):
    return f'''    <section class="hero wrap">
      <p class="eyebrow reveal">{eyebrow}</p>
      <h1 class="display reveal">{h1}</h1>
      <p class="lead reveal">{lead}</p>{actions}
    </section>'''


def hero_img(id_, alt):
    return f'''    <div class="wrap pull reveal">
      <figure class="hero-media" style="margin:0">
        {img(id_, alt, "(min-width: 1400px) 76rem, 100vw", eager=True)}
      </figure>
    </div>'''


def notice(text):
    return f'''      <p class="notice reveal">{text}</p>'''


def head(eyebrow, h2, p):
    return f'''      <div class="section-head">
        <div>
          <p class="eyebrow reveal">{eyebrow}</p>
          <h2 class="h2 reveal">{h2}</h2>
        </div>
        <p class="reveal">{p}</p>
      </div>'''


def soon(title, text, href='', cta=''):
    link = f'\n          <a class="link" href="{href}">{cta} <span class="arrow">→</span></a>' if href else ''
    return f'''        <div class="card accent reveal" style="justify-content:center">
          <div class="tags"><span class="tag">Próximamente</span></div>
          <h3 class="h3">{title}</h3>
          <p>{text}</p>{link}
        </div>'''


def euros(n):
    return f'{n:,.0f}'.replace(',', '.') + ' €'


CREATE_CARD = f'''        <a class="card reveal" href="{{pre}}formaciones/crea-te-a-ti-mismo/" style="padding:0;overflow:hidden">
          <div class="hero-media" style="aspect-ratio:16/10;border-radius:0">
            {img(DEER, "Ciervos en un prado junto al bosque", "(min-width: 760px) 38rem, 100vw", widths=(800, 1600, 2400))}
          </div>
          <div style="padding:clamp(1.5rem,3vw,2.25rem)">
            <div class="tags"><span class="tag live">Inscripción abierta</span><span class="tag">6–7 dic 2026</span><span class="tag">Bárcena Mayor</span><span class="tag">{euros(PRECIO)}{IVA}</span></div>
            <h3 class="h3">Créate <em>a ti mismo</em></h3>
            <p>Dos días de aprendizaje y naturaleza en favor de tu bienestar físico-emocional: alimentación molecular, duelo y reprogramación mental, con alojamiento y comidas incluidos.</p>
            <span class="link">Ver la formación <span class="arrow">→</span></span>
          </div>
        </a>'''

CONTACT = f'''    <section class="section wrap" id="contacto">
      <div class="section-head" style="margin-bottom:0">
        <div>
          <p class="eyebrow reveal">Contacto</p>
          <h2 class="h2 reveal">Hablemos <em>con calma.</em></h2>
          <div class="actions reveal">
            <a class="button" href="{mailto('Información sobre Ama tus palabras')}">Escríbenos <span class="arrow">→</span></a>
            <a class="button ghost" href="{{pre}}contacto/">Más formas de contacto</a>
          </div>
        </div>
        <p class="reveal">Una propuesta compartida por {EQUIPO}.</p>
      </div>
    </section>'''


def build():
    # ---------- Portada
    areas = [
        ('eventos', '01', 'Eventos', 'Encuentros, paseos y charlas abiertas. Fechas y lugares de lo próximo.'),
        ('formaciones', '02', 'Formaciones', 'Experiencias de aprendizaje con programa completo y herramientas para casa.'),
        ('alimentacion', '03', 'Alimentación', 'La alimentación y el equilibrio del cuerpo, la mente y el alma, sin dietas restrictivas.'),
        ('salud', '04', 'Salud', 'Duelo, emociones y creencias: reflexiones para acompañar los procesos personales.'),
    ]
    area_cards = '\n'.join(f'''        <a class="card reveal" href="{{pre}}{k}/">
          <span class="num">{n}</span>
          <h3 class="h3">{t}</h3>
          <p>{d}</p>
          <span class="link" style="margin-top:auto">Entrar <span class="arrow">→</span></span>
        </a>''' for k, n, t, d in areas)

    page('', '', 'Ama tus palabras: eventos, formaciones y divulgación sobre alimentación y salud para comprender tus procesos y avanzar.', None, f'''{hero(LEMA, "Ama tus<br><em>palabras.</em>",
        "Lo que te dices da forma a cómo vives. Creamos eventos, formaciones y contenidos para parar, comprender, recordar y sentir, y encontrar herramientas para seguir adelante.",
        """
      <div class="actions reveal">
        <a class="button" href="{pre}formaciones/crea-te-a-ti-mismo/">Próxima formación <span class="arrow">→</span></a>
        <a class="button ghost" href="#apartados">Explorar</a>
      </div>""")}

{hero_img(FOREST, "Bosque frondoso con luz entre los árboles")}

    <section class="section wrap" id="apartados">
{head("Apartados", "Todo lo que <em>compartimos.</em>", "Cuatro espacios para encontrar lo que buscas. Todo con fin divulgativo y de autoconocimiento.")}
      <div class="grid grid-4">
{area_cards}
      </div>
    </section>

    <section class="section wrap">
{head("Destacado", "Lo <em>próximo.</em>", "Plazas limitadas. Escríbenos para reservar o recibir información.")}
      <div class="grid grid-2">
{CREATE_CARD}
{soon("Más <em>fechas</em>", "Estamos preparando nuevos eventos y formaciones. Escríbenos y te avisaremos cuando abramos fechas.", "#contacto", "Quiero enterarme")}
      </div>
    </section>

{CONTACT}''')

    # ---------- Eventos
    page('eventos', 'Eventos', 'Próximos eventos de Ama tus palabras: encuentros, paseos y charlas.', 'eventos', f'''{hero("Eventos", "Encuentros <em>en persona.</em>",
        "Paseos, charlas y encuentros para compartir en grupo. Aquí verás las próximas fechas.")}

    <section class="section wrap">
      <div class="agenda">
        <a class="agenda-row reveal" href="{{pre}}formaciones/crea-te-a-ti-mismo/">
          <time datetime="2026-12-06"><strong>6–7</strong> dic 2026</time>
          <div><h3 class="h3">Créate <em>a ti mismo</em></h3><p>Formación de dos días con alojamiento, comidas y paseos por la naturaleza.</p></div>
          <span class="muted small">Bárcena Mayor, Cantabria</span>
          <span class="arrow">→</span>
        </a>
        <div class="agenda-row empty reveal">
          <time>Próximamente</time>
          <div><h3 class="h3">Nuevas <em>fechas</em></h3><p>Estamos preparando más eventos. Escríbenos y te avisaremos.</p></div>
          <span></span><span></span>
        </div>
      </div>
    </section>

{CONTACT}''')

    # ---------- Formaciones
    page('formaciones', 'Formaciones', 'Formaciones de Ama tus palabras: experiencias de aprendizaje con programa completo.', 'formaciones', f'''{hero("Cursos y formaciones", "Aprender <em>con calma.</em>",
        "Experiencias de aprendizaje con un programa completo, en grupo y en un entorno que ayuda a parar. Cada formación tiene su propia página con módulos, fechas, precio y lugar.")}

    <section class="section wrap">
      <div class="grid grid-2">
{CREATE_CARD}
{soon("Nuevas <em>formaciones</em>", "Pronto anunciaremos nuevas formaciones. Escríbenos si quieres que te avisemos.", "#contacto", "Avisadme")}
      </div>
    </section>

{CONTACT}''')

    # ---------- Alimentación y salud
    def topics(items):
        return '\n'.join(f'''        <div class="card reveal">
          <span class="num">{i:02d}</span>
          <h3 class="h3">{t}</h3>
          <p>{d}</p>
          <div class="tags" style="margin-top:auto"><span class="tag">Próximamente</span></div>
        </div>''' for i, (t, d) in enumerate(items, 1))

    page('alimentacion', 'Alimentación', 'Divulgación sobre alimentación de Ama tus palabras. No es consejo médico ni nutricional.', 'alimentacion', f'''{hero("Alimentación", "Lo que comemos <em>también habla.</em>",
        "Contenidos divulgativos sobre cómo se relaciona la alimentación con el equilibrio del cuerpo, la mente y el alma, sin planteamientos de dietas restrictivas.")}

    <section class="section wrap">
{notice("Contenido divulgativo. No somos personal médico ni nutricionistas colegiados: contrasta la información, investiga por tu cuenta y consulta con un profesional antes de cambiar tu alimentación.")}
    </section>

    <section class="section wrap">
{head("Temas", "Por dónde <em>empezar.</em>", "Estamos preparando los primeros artículos. Mientras tanto, lo trabajamos en profundidad en la formación.")}
      <div class="grid grid-3">
{topics([
    ("Funciones de los alimentos", "Identificar los alimentos según su principal efecto en el organismo."),
    ("Variedad y combinación", "Por qué importa combinar y variar lo que comemos."),
    ("Cocina molecular", "Un taller práctico para llevar lo aprendido a la cocina."),
])}
      </div>
      <div class="actions reveal">
        <a class="button ghost" href="{{pre}}formaciones/crea-te-a-ti-mismo/#modulos">Módulo de alimentación molecular <span class="arrow">→</span></a>
      </div>
    </section>''')

    page('salud', 'Salud', 'Divulgación sobre bienestar emocional de Ama tus palabras. No es consejo médico ni psicológico.', 'salud', f'''{hero("Salud", "Cuidar <em>lo que sentimos.</em>",
        "Reflexiones para acompañar los procesos personales: el duelo, las emociones, las relaciones humanas, los hábitos y la relación entre nuestras creencias y nuestra manera de vivir.")}

    <section class="section wrap">
{notice("Contenido divulgativo y de autoconocimiento. No somos personal médico, psicólogos ni terapeutas colegiados: no sustituye la atención sanitaria o psicológica. Investiga por tu cuenta y, si lo necesitas, acude a un profesional.")}
    </section>

    <section class="section wrap">
{head("Temas", "Por dónde <em>empezar.</em>", "Estamos preparando los primeros artículos. Mientras tanto, lo trabajamos en profundidad en la formación.")}
      <div class="grid grid-3">
{topics([
    ("Duelo e integración", "Reconocer, acompañar y transformar el significado que damos a la pérdida."),
    ("Creencias y patrones", "Las creencias aceptadas en la mente subconsciente y cómo influyen en el día a día."),
    ("Bienestar emocional", "Herramientas sencillas para parar, observar y comprender lo que sentimos."),
])}
      </div>
      <div class="actions reveal">
        <a class="button ghost" href="{{pre}}formaciones/crea-te-a-ti-mismo/#seis-pasos">Los seis pasos del duelo <span class="arrow">→</span></a>
      </div>
    </section>''')

    # ---------- Testimonios y tienda
    page('testimonios', 'Testimonios', 'Testimonios de personas que han pasado por los encuentros de Ama tus palabras.', 'testimonios', f'''{hero("Testimonios", "Lo que <em>nos cuentan.</em>",
        "Experiencias de quienes han compartido con nosotros un encuentro o una formación.")}

    <section class="section wrap">
      <div class="grid grid-2">
{soon("Primeros <em>testimonios</em>", "Pronto compartiremos aquí las palabras de quienes nos han acompañado.")}
      </div>
    </section>

{CONTACT}''')

    page('tienda', 'Tienda', 'Libros y recursos de Ama tus palabras.', 'tienda', f'''{hero("Tienda", "Libros <em>para seguir.</em>",
        "La dilogía «Ama tus palabras» y «Créate a ti mismo», para seguir profundizando en casa. Escríbenos y te contamos cómo conseguirlos.")}

    <section class="section wrap">
      <div class="grid grid-2">
        <div class="card reveal">
          <span class="num">Libro</span>
          <h3 class="h3">Ama <em>tus palabras</em></h3>
          <p>Primer libro de la dilogía que da nombre a este proyecto.</p>
          <a class="link" style="margin-top:auto" href="{mailto('Libro: Ama tus palabras')}">Pedir información <span class="arrow">→</span></a>
        </div>
        <div class="card reveal">
          <span class="num">Libro</span>
          <h3 class="h3">Créate <em>a ti mismo</em></h3>
          <p>Segundo libro de la dilogía, que inspira la formación del mismo nombre.</p>
          <a class="link" style="margin-top:auto" href="{mailto('Libro: Créate a ti mismo')}">Pedir información <span class="arrow">→</span></a>
        </div>
      </div>
    </section>

{CONTACT}''')

    # ---------- Contacto
    def canal(nombre, valor, href):
        if href:
            return f'''        <a class="card reveal" href="{href}"{' target="_blank" rel="noopener"' if href.startswith('http') else ''}>
          <span class="num">{nombre}</span>
          <h3 class="h3">{valor}</h3>
          <span class="link" style="margin-top:auto">Abrir <span class="arrow">→</span></span>
        </a>'''
        return f'''        <div class="card reveal">
          <span class="num">{nombre}</span>
          <h3 class="h3">{valor}</h3>
          <div class="tags" style="margin-top:auto"><span class="tag">Próximamente</span></div>
        </div>'''

    canales = [canal('Correo', EMAIL, mailto('Información sobre Ama tus palabras')),
               canal('WhatsApp', ' '.join([WHATSAPP[2:5], WHATSAPP[5:8], WHATSAPP[8:]]) if WHATSAPP else 'Teléfono de contacto', f'https://wa.me/{WHATSAPP}' if WHATSAPP else ''),
               canal('YouTube', '@AmaTusPalabras', YOUTUBE)]
    canales += [canal('Redes sociales', n, u) for n, u in REDES.items()] or [canal('Redes sociales', 'Síguenos', '')]

    page('contacto', 'Contacto', 'Contacto de Ama tus palabras: correo, WhatsApp, YouTube y redes sociales.', 'contacto', f'''{hero("Contacto", "Hablemos <em>con calma.</em>",
        f"Escríbenos para reservar, resolver dudas o recibir información de los próximos encuentros. Una propuesta compartida por {EQUIPO}.")}

    <section class="section wrap">
      <div class="grid grid-2">
{chr(10).join(canales)}
      </div>
    </section>''')

    # ---------- Créate a ti mismo
    reserva = round(PRECIO * RESERVA_PCT / 100)
    incluye = [
        ('Alojamiento', 'Incluido durante los dos días del encuentro.'),
        ('Desayunos, comidas y cena', 'Todas las comidas del encuentro están incluidas.'),
        ('Los 3 módulos', 'Alimentación molecular, duelo e integración y reprogramación mental.'),
        ('Paseos por la naturaleza', 'Paseos por el entorno de Bárcena Mayor para aprender fuera del aula.'),
        ('Taller de cocina molecular', 'Un taller práctico para llevar lo aprendido a la cocina.'),
    ]
    incluye_cards = '\n'.join(f'''        <div class="card reveal">
          <span class="num">{i:02d}</span>
          <h3 class="h3">{t}</h3>
          <p>{d}</p>
        </div>''' for i, (t, d) in enumerate(incluye, 1))
    fila_noche = f'        <div><small>Noche adicional</small><strong>{NOCHE_EXTRA}{IVA}</strong></div>\n' if NOCHE_EXTRA else ''
    pedir = mailto('Reserva: Créate a ti mismo',
                   'Hola, me gustaría reservar plaza en Créate a ti mismo (6 y 7 de diciembre de 2026).')
    wa = (f'\n        <a class="button ghost" href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener">WhatsApp</a>'
          if WHATSAPP else '')

    page('formaciones/crea-te-a-ti-mismo', 'Créate a ti mismo',
         f'Créate a ti mismo: dos días de aprendizaje y naturaleza el 6 y 7 de diciembre de 2026 en Bárcena Mayor, Cantabria. {euros(PRECIO)}{IVA}, con alojamiento y comidas.',
         'formaciones', f'''{hero("Reto de 2 días · 6 y 7 de diciembre de 2026 · Bárcena Mayor, Cantabria", "Créate<br><em>a ti mismo.</em>",
        "Dos días de aprendizaje y naturaleza en favor de tu bienestar físico-emocional.",
        """
      <div class="actions reveal">
        <a class="button" href="#reserva">Reservar plaza <span class="arrow">→</span></a>
        <a class="button ghost" href="#incluye">Qué incluye</a>
      </div>""")}

{hero_img(FOREST, "Bosque frondoso con luz entre los árboles")}

    <section class="section wrap" id="experiencia">
      <div class="section-head">
        <div>
          <p class="eyebrow reveal">Una pausa para mirar hacia dentro</p>
          <h2 class="h2 reveal">Hay momentos en los que necesitamos <em>parar, comprender, recordar y sentir.</em></h2>
        </div>
        <p class="reveal">Este encuentro reúne tres bloques de aprendizaje que abordan la alimentación, los procesos de duelo y la relación entre nuestras creencias aceptadas en la mente subconsciente y nuestra manera de vivir las emociones, las relaciones humanas, los hábitos y los sentimientos.</p>
      </div>
      <div class="tags reveal" aria-label="Situaciones que aborda el encuentro">
        <span class="tag">Crisis</span><span class="tag">Conflictos</span><span class="tag">Heridas sin sanar</span>
        <span class="tag">Duelos que no se cierran</span><span class="tag">Miedos</span><span class="tag">Dinero que no alcanza</span>
      </div>
    </section>

    <section class="section wrap" id="modulos">
      <div class="section-head">
        <div>
          <p class="eyebrow reveal">El programa</p>
          <h2 class="h2 reveal">Estructurado en <em>3 módulos.</em></h2>
        </div>
        <p class="reveal">Te enseñamos cómo aplicar lo que nos funciona: son años de experiencia. Tres áreas de trabajo, con herramientas para llevarte a casa.</p>
      </div>
      <div class="grid grid-3">
        <article class="card reveal">
          <span class="num">Módulo 01</span>
          <h3 class="h3">Alimentación molecular</h3>
          <p class="promise">Restaura el desequilibrio bioquímico y metabólico.</p>
          <p>Sin dietas, sin efectos secundarios y sin dejar de comer. Aprenderás a identificar los alimentos según su principal efecto en nuestro cuerpo, porque lo importante es la combinación de los alimentos, que activan procesos hormonales y metabólicos que construyen o destruyen el estado de salud de las personas. Revisaremos cómo la alimentación se relaciona con el equilibrio del cuerpo, la mente y el alma.</p>
          <ul><li>Reconocer funciones de los alimentos.</li><li>Comprender la importancia de la variedad y la combinación.</li><li>Aprender sin planteamientos de dietas restrictivas.</li><li>Taller de cocina molecular.</li></ul>
          <p class="note">Contenido educativo; no sustituye el consejo médico o nutricional individual.</p>
        </article>
        <article class="card accent reveal" id="duelo">
          <span class="num">Módulo 02</span>
          <h3 class="h3">Duelo, superación e integración</h3>
          <p class="promise">Los seis pasos clave del duelo.</p>
          <p>Incluye el duelo por un familiar, por tu pareja, por una mascota, por un trabajo o negocio, por tu salud e incluso por el dinero. Este módulo propone un recorrido de reflexión para reconocer, acompañar y transformar el significado que percibimos por la pérdida con lo que nos hemos identificado.</p>
          <a class="link" href="#seis-pasos" style="margin-top:auto">Explorar los seis pasos <span class="arrow">→</span></a>
        </article>
        <article class="card reveal">
          <span class="num">Módulo 03</span>
          <h3 class="h3">Reprogramación mental</h3>
          <p class="promise">Traspasa los límites de tu mente con la Hipnoconsciencia.</p>
          <p>Haremos una sesión de Hipnoconsciencia, una técnica desarrollada por nuestro equipo, para encontrar el origen y la raíz de ese conflicto, que puede estar en el dinero, en tus relaciones de pareja o familiares o en tu salud físico-emocional. Desde la raíz transformamos esa creencia o programa que te puede estar impidiendo vivir la vida que deseas.</p>
          <ul><li>No necesitas tener experiencia previa.</li><li>Toda la experiencia la realizarás totalmente consciente: recordarás los hechos del inconsciente y del consciente a la vez.</li><li>Te dejaremos una herramienta para que puedas entrar en tu subconsciente siempre que lo desees.</li></ul>
          <p class="note">La experiencia es formativa y de autoconocimiento; no garantiza resultados ni sustituye atención psicológica o sanitaria.</p>
        </article>
      </div>
    </section>

    <section class="section wrap" id="seis-pasos">
      <div class="section-head">
        <div>
          <p class="eyebrow reveal">Módulo 02 · Profundizamos</p>
          <h2 class="h2 reveal">Los seis pasos <em>del duelo.</em></h2>
        </div>
        <p class="reveal">Un itinerario de reflexión presentado en el material del encuentro.</p>
      </div>
      <div class="steps">
        <article class="reveal"><span>01</span><div><h3 class="h3">Lo siento</h3><p>Realizo la acción de parar y sentir el dolor.</p></div></article>
        <article class="reveal"><span>02</span><div><h3 class="h3">Me arrepiento</h3><p>Porque fui inconsciente de lo que estaba creando; ahora entiendo.</p></div></article>
        <article class="reveal"><span>03</span><div><h3 class="h3">Perdón</h3><p>Reconozco que nos podemos equivocar y me responsabilizo de los efectos que creé.</p></div></article>
        <article class="reveal"><span>04</span><div><h3 class="h3">Gracias</h3><p>Por todo lo que he aprendido durante el proceso del dolor.</p></div></article>
        <article class="reveal"><span>05</span><div><h3 class="h3">Amor</h3><p>El pegamento para que todas las piezas del puzle se unifiquen y se integren en el alma.</p></div></article>
        <article class="reveal"><span>06</span><div><h3 class="h3">Coser</h3><p>El cierre de la herida. Aunque duela, es el momento más dulce: cierras lo que se rompió porque comprendes el proceso que te sanó.</p></div></article>
      </div>
    </section>

    <section class="section wrap band">
      <div class="split">
        <figure class="hero-media reveal" style="margin:0">
          {img(DEER, "Ciervos en un prado junto al bosque", "(min-width: 860px) 40rem, 100vw", widths=(800, 1600, 2400))}
        </figure>
        <div>
          <p class="eyebrow reveal">También fuera del aula</p>
          <h2 class="h2 reveal">Aprender en plena naturaleza <em>y sentirte más cerca de ti.</em></h2>
          <p class="lead reveal">Además de los módulos, compartiremos paseos por la naturaleza y charlas que inspiren. Un espacio para conversar, observar el entorno y compartir aprendizajes.</p>
          <div class="tags reveal" style="margin-top:2rem"><span class="tag">Paseos por la naturaleza</span><span class="tag">Charlas inspiradoras</span><span class="tag">Conexión con el entorno</span></div>
        </div>
      </div>
    </section>

    <section class="section wrap" id="incluye">
{head("Qué incluye", "Todo listo para <em>que solo te ocupes de ti.</em>", "El precio incluye el alojamiento, las comidas, los módulos, los paseos y el taller.")}
      <div class="grid grid-3">
{incluye_cards}
      </div>
    </section>

    <section class="section wrap" id="reserva">
      <span id="encuentro"></span>
      <p class="eyebrow reveal">Reserva tu plaza</p>
      <h2 class="h2 reveal" style="max-width:48rem">Dos días para <em>aprender, sentir y compartir.</em></h2>
      <div class="facts reveal" style="margin-top:3rem">
        <div><small>Precio total</small><strong>{euros(PRECIO)}{IVA}</strong></div>
        <div><small>Reserva</small><strong>{RESERVA_PCT} % al reservar ({euros(reserva)}{IVA})</strong></div>
{fila_noche}        <div><small>Fecha</small><strong>6 y 7 de diciembre de 2026</strong></div>
        <div><small>Lugar</small><strong>Bárcena Mayor, Cantabria</strong></div>
        <div><small>Promotores de la salud</small><strong>{EQUIPO}</strong></div>
      </div>
      <div class="actions reveal">
        <a class="button" href="{pedir}">Reservar por correo <span class="arrow">→</span></a>{wa}
      </div>
      <p class="muted small reveal" style="margin-top:1.25rem">Escríbenos a <a href="{mailto('Información sobre Créate a ti mismo')}">{EMAIL}</a> y te explicamos cómo hacer la reserva.{'' if NOCHE_EXTRA else ' Si necesitas una noche adicional, consúltanos.'}</p>
    </section>''')


if __name__ == '__main__':
    build()
