import json,re,html as H
from urllib.parse import quote
P=json.load(open('/tmp/plans.json'))
ALL=P['cats']+P['retratos']
NAV=ALL[3]
OTH=[c for i,c in enumerate(ALL) if i!=3]
OTHIDX=[i for i in range(len(ALL)) if i!=3]
def esc(s): return H.escape(str(s),quote=True)
WA='https://wa.me/18294974585?text='
BASE_FOTOS='https://hadesplanesyservicios.vercel.app/fotos-planes'
SLUG={'Newborn':'newborn','Primer año':'primer-ano','Familiar':'familiar','Prebodas':'prebodas','Parejas':'parejas','Individuales':'individuales','Graduaciones':'graduaciones','Ejecutivas':'ejecutivas','XV años':'xv-anos','Navidad':'navidad','Navidad en casa':'navidad-casa'}
def wa_plan(cat_name, p, rows):
    lines=[f"Hola, quiero reservar el plan {p['name']} ({p['tier'].title()}) de {cat_name}.",
           f"Precio: {p['price']} {p.get('unit','por sesión')}.", "Detalles del plan:"]
    lines+= [f"- {k}: {v}" for k,v in rows]
    if p.get('extras'): lines.append("Incluye: " + ", ".join(p['extras']))
    lines.append("Miniatura: "+BASE_FOTOS+"/"+SLUG.get(cat_name,'')+".jpg")
    lines.append("¿Me pueden confirmar disponibilidad? Gracias.")
    return WA+quote("\n".join(lines))
def rows_of(p): return [(r['k'], ''.join(x['t'] for x in r['parts'])) for r in p['rows']]
def pnum(p):
    m=re.search(r'([\d,]+)',p); return int(m.group(1).replace(',','')) if m else 0
def fprice(c): return min(pnum(p['price']) for p in c['plans'])
IMG={'Newborn':'newborn','Primer año':'primer','Familiar':'familiar','Navidad':'nav1','Prebodas':'prebodas','Parejas':'parejas','Individuales':'individuales','Graduaciones':'grad2','Ejecutivas':'ejecutivas'}
nplans=sum(len(c['plans']) for c in ALL)
ncat=len(ALL)
# tiles (explore)
tile_cats=[2,4,6,7,8,5]
tiles=''.join(f'''<a class="tile img-{IMG[ALL[i]['name']]}" href="#planes" data-go="{i}"><span><b>{esc(ALL[i]['name'])}</b></span><small>Ver planes →</small></a>''' for i in tile_cats)
# session cards
cards=''.join(f'''
  <a class="card cat" href="#planes" data-go="{i}" data-cat="{i}" data-price="{fprice(c)}">
    <div class="card-img img-{IMG[c['name']]}"></div>
    <div class="card-body">
      <h3>{esc(c['name'])}</h3>
      <span class="price">Desde RD$ {fprice(c):,}</span>
    </div>
  </a>''' for i,c in zip(OTHIDX,OTH))
cat_opts=''.join(f'<option value="{i}">{esc(c["name"])}</option>' for i,c in zip(OTHIDX,OTH))
NAVROWS=lambda p: [(('Duración' if r['k']=='Duración' else r['k']), ('1 hora' if r['k']=='Duración' else (({'Villancico':'De 2 a 4 personas','Nochebuena':'De 4 a 6 personas','Gran Navidad':'De 4 a 6 personas'}.get(p['name'],'De 2 a 4 personas')) if r['k']=='Personas' else ('Solo en estudio' if r['k']=='Locación' else ''.join(x['t'] for x in r['parts']))))) for r in p['rows']]
_nr=NAVROWS
NAVROWS=lambda p: _nr(p)+[('Disponibilidad','Solo temporada navideña')]
navplans=''.join(f'''<div class="plan{' featured' if p.get('featured') else ''}">
  {'<span class="reco">Recomendado</span>' if p.get('featured') else ''}
  <div class="tier">{esc(p['tier'])}</div>
  <div class="pname">{esc(p['name'])}</div>
  <div class="lead">{esc(p['lead'])}</div>
  <div class="price">{esc(p['price'])}<small>por sesión</small></div>
  <div class="rows">{''.join(f'<div class="row"><span>{esc(k)}</span><b>{esc(v)}</b></div>' for k,v in NAVROWS(p))}</div>
  <a class="btn btn-k btn-plan" href="{wa_plan('Navidad', {**p,'extras':[]}, NAVROWS(p))}" target="_blank" rel="noopener">Reservar Navidad →</a>
</div>''' for p in NAV['plans'])
CASA=[
 {'tier':'PLAN BÁSICO','name':'Chimenea','price':'RD$ 8,000','lead':'Tu casa decorada, con una sesión sencilla y bonita.','featured':False,
  'rows':[('Duración','1 hora'),('Fotografías','10 editadas'),('Digitales','Alta resolución'),('Impresas','No incluye'),('Locación','En tu hogar'),('Entrega','Galería online privada'),('Tiempo','2 días desde la elección'),('Disponibilidad','Solo temporada navideña')]},
 {'tier':'PLAN ESPECIAL','name':'Hogar Iluminado','price':'RD$ 12,500','lead':'Tu hogar navideño como protagonista, con familia incluida.','featured':True,
  'rows':[('Duración','1 hora'),('Fotografías','15 editadas'),('Digitales','Alta resolución + versión web'),('Impresas','5 fotos impresas'),('Locación','En tu hogar'),('Entrega','Galería privada + 5 fotos impresas'),('Tiempo','4 días desde la elección'),('Disponibilidad','Solo temporada navideña')]},
 {'tier':'PLAN PREMIUM','name':'Casa de Navidad','price':'RD$ 17,000','lead':'Toda la casa en tus fotos, para guardarlas por años.','featured':False,
  'rows':[('Duración','1 hora'),('Fotografías','20 editadas'),('Digitales','Alta resolución + selección en B/N'),('Impresas','Todas las fotos + enmarcado 11×14'),('Locación','En tu hogar'),('Entrega','Galería privada + todas impresas + enmarcado 11×14'),('Tiempo','6 días desde la elección'),('Disponibilidad','Solo temporada navideña')]},
]
casaplans=''.join(f'''<div class="plan{' featured' if p['featured'] else ''}">
  {'<span class="reco">Recomendado</span>' if p['featured'] else ''}
  <div class="tier">{esc(p['tier'])}</div>
  <div class="pname">{esc(p['name'])}</div>
  <div class="lead">{esc(p['lead'])}</div>
  <div class="price">{esc(p['price'])}<small>por sesión</small></div>
  <div class="rows">{''.join(f'<div class="row"><span>{esc(k)}</span><b>{esc(v)}</b></div>' for k,v in p['rows'])}</div>
  <a class="btn btn-k btn-plan" href="{wa_plan('Navidad en casa', p, p['rows'])}" target="_blank" rel="noopener">Reservar en casa →</a>
</div>''' for p in CASA)
XVADD=3500
XVRAW=[('Vip',10500,['Vestido largo y vestido corto','Corona','Cretona','Peinado','Maquillaje','Accesorios','Ramo','Sombrilla para fotos'],True),
       ('Premium',8700,['Vestido largo','Corona','Cretona','Peinado','Maquillaje','Accesorios','Ramo','Sombrilla para fotos'],False),
       ('Básico',7000,['Vestido largo','Corona','Cretona','Peinado','Maquillaje','Ramo','Accesorios','Sombrilla para fotos'],False)]
PHOTO={
 'Básico':[('Duración','1.5 horas'),('Fotografías','15 editadas'),('Digitales','Alta resolución'),('Impresas','No incluye'),('Cambios','No incluye'),('Personas','Quinceañera y familia directa'),('Locación','Estudio o 1 exterior'),('Entrega','Galería online privada'),('Tiempo','2 días desde la elección')],
 'Premium':[('Duración','2 horas'),('Fotografías','25 editadas'),('Digitales','Alta resolución'),('Impresas','5 fotos impresas'),('Cambios','No incluye'),('Personas','Quinceañera y familia directa'),('Locación','Estudio o exterior a elección'),('Entrega','Galería privada + 5 fotos impresas'),('Tiempo','4 días desde la elección')],
 'Vip':[('Duración','2.5 horas'),('Fotografías','35 editadas'),('Digitales','Alta resolución + selección en B/N'),('Impresas','Todas las fotos + enmarcado 11×14'),('Cambios','2 (vestido largo y corto)'),('Personas','Quinceañera y familia extendida'),('Locación','Estudio o 2 exteriores'),('Entrega','Galería privada + impresas + enmarcado 11×14'),('Tiempo','6 días desde la elección')],
}
XVPLANS=[]
for name,base,items,feat in XVRAW:
    rows=PHOTO[name]+[('Vestuario y accesorios',', '.join(items))]
    XVPLANS.append({'tier':'PLAN '+name.upper(),'name':name,'price':f'RD$ {base+XVADD:,}','unit':'por paquete','lead':'Vestuario completo y sesión fotográfica para tu día de XV años.','featured':feat,
      'rows':rows})
xvplans=''.join(f'''<div class="plan{' featured' if p['featured'] else ''}">
  {'<span class="reco">Recomendado</span>' if p['featured'] else ''}
  <div class="tier">{esc(p['tier'])}</div>
  <div class="pname">{esc(p['name'])}</div>
  <div class="lead">{esc(p['lead'])}</div>
  <div class="price">{esc(p['price'])}<small>{esc(p['unit'])}</small></div>
  <div class="rows">{''.join(f'<div class="row"><span>{esc(k)}</span><b>{esc(v)}</b></div>' for k,v in p['rows'])}</div>
  <a class="btn btn-y btn-plan" href="{wa_plan('XV años', p, p['rows'])}" target="_blank" rel="noopener">Reservar este plan →</a>
</div>''' for p in XVPLANS)

def plan_cards(cat_name, plans, btn_cls, btn_text, cls='plans'):
    out=''
    for p in plans:
        feat=p.get('featured')
        rows=''.join('<div class="row"><span>%s</span><b>%s</b></div>' % (esc(k),esc(v)) for k,v in p['rows'])
        ex=''.join('<li>%s</li>' % esc(x) for x in p.get('extras',[]))
        out+=('<div class="plan%s" data-price="%d">%s<div class="tier">%s</div><div class="pname">%s</div>'
              '<div class="lead">%s</div><div class="price">%s<small>%s</small></div><div class="rows">%s</div>%s'
              '<a class="btn %s btn-plan" href="%s" target="_blank" rel="noopener">%s</a></div>') % (
              ' featured' if feat else '', pnum(p['price']),
              ('<span class="reco">Recomendado</span>' if feat else ''),
              esc(p['tier']), esc(p['name']), esc(p.get('lead','')), esc(p['price']), esc(p.get('unit','por sesión')),
              rows, ('<ul class="extras">'+ex+'</ul>' if ex else ''),
              btn_cls, wa_plan(cat_name,p,p['rows']), esc(btn_text))
    return '<div class="%s">%s</div>' % (cls,out)

navplans=plan_cards('Navidad',[dict(p,rows=NAVROWS(p),extras=[]) for p in NAV['plans']],'btn-k','Reservar Navidad →','plans xmas-plans')
casaplans=plan_cards('Navidad en casa',CASA,'btn-k','Reservar en casa →','plans xmas-plans')
xvplans=plan_cards('XV años',XVPLANS,'btn-y','Reservar este plan →','plans xv-plans')
XVCAT={'num':'05','kicker':'PAQUETES','name':'XV años','desc':'Vestido, corona, cretona, peinado, maquillaje, accesorios, ramo y sombrilla para tus fotos, en un solo paquete.',
       'plans':[dict(p,rows=[{'k':k,'parts':[{'t':v}]} for k,v in p['rows']]) for p in XVPLANS]}
ALL.append(XVCAT); OTH.append(XVCAT); OTHIDX.append(len(ALL)-1)
IMG['XV años']='xv'
# navidad slider
gal=''.join(f'<figure class="slide img-nav{i}"><figcaption>{i:02d} / 10</figcaption></figure>' for i in range(1,11))
# plan tabs
tabs=''.join(f'<button class="tab{" active" if i==OTHIDX[0] else ""}" data-tab="{i}">{esc(c["name"])}</button>' for i,c in zip(OTHIDX,OTH))
panels=[]
for i,c in zip(OTHIDX,OTH):
    pc=[]
    for p in c['plans']:
        rows=''.join(f'<div class="row"><span>{esc(r["k"])}</span><b>{esc("".join(x["t"] for x in r["parts"]))}</b></div>' for r in p['rows'])
        ex=''.join(f'<li>{esc(x)}</li>' for x in p.get('extras',[]))
        feat=p.get('featured')
        pc.append(f'''<div class="plan{' featured' if feat else ''}" data-price="{pnum(p['price'])}">
          {'<span class="reco">Recomendado</span>' if feat else ''}
          <div class="tier">{esc(p['tier'])}</div>
          <div class="pname">{esc(p['name'])}</div>
          <div class="lead">{esc(p['lead'])}</div>
          <div class="price">{esc(p['price'])}<small>por sesión</small></div>
          <div class="rows">{rows}</div>
          {'<ul class="extras">'+ex+'</ul>' if ex else ''}
          <a class="btn btn-y btn-plan" href="{wa_plan(c['name'], p, rows_of(p))}" target="_blank" rel="noopener">Reservar este plan →</a>
        </div>''')
    panels.append(f'''<div class="panel{' active' if i==OTHIDX[0] else ''}" data-panel="{i}">
      <div class="panel-head"><div><div class="eyebrow">{esc(c['num'])} · {esc(c['kicker'])}</div><h3>{esc(c['name'])}</h3></div><p>{esc(c['desc'])}</p></div>
      {plan_cards(c['name'], [dict(p,rows=rows_of(p)) for p in c['plans']], 'btn-y', 'Reservar este plan →')}</div>''')
extras=[('Fotografía adicional','Editada, en alta resolución','RD$ 500'),('Cuadro enmarcado','Tamaño 11×14, listo para colgar','RD$ 1,500'),('Cambio de ropa adicional','O set adicional en estudio','RD$ 300'),('Persona adicional','Abuelos, tíos, mascotas','RD$ 500'),('Entrega exprés','Galería en 24 horas','RD$ 2,500'),('Maquillaje y peinado','Bajo solicitud, con aliada profesional','Desde RD$ 3,500')]
extras_html=''.join(f'<div class="extra"><b>{esc(a)}</b><span>{esc(b)}</span><em>{esc(c)}</em></div>' for a,b,c in extras)
pol=[('01','Reserva','La fecha se aparta con un anticipo del 50% del plan. El restante se paga el día de la sesión, antes de comenzar.'),
('02','Cancelaciones y devoluciones','Las devoluciones solo se aceptan dentro de las 24 horas siguientes al pago. Pasado ese plazo, el anticipo deja de ser reembolsable.'),
('03','Reprogramación','Puedes cambiar la fecha una vez sin costo avisando con al menos 48 horas. Cambios con menos tiempo pueden perder el anticipo.'),
('04','Clima y salud','Si llueve en una sesión de exterior o el bebé o niño se enferma, reprogramamos sin costo adicional.'),
('05','Puntualidad','Hay 15 minutos de tolerancia. Los retrasos se descuentan del tiempo de la sesión.'),
('06','Newborn','Se reserva durante el embarazo con fecha tentativa y se confirma tras el nacimiento. Lo ideal es entre los 5 y 15 días de nacido.'),
('07','Selección y entrega','Los días de entrega cuentan desde que eliges tus fotos. La galería privada estará disponible por 30 días para descargarlas.'),
('08','Archivos y edición','Se entregan solo fotos editadas; no se entregan archivos sin editar (RAW). Los retoques especiales se cotizan aparte.'),
('09','Uso de imágenes','Todas las fotografías pueden ser utilizadas por el fotógrafo en su portafolio, redes sociales y material promocional.'),
('10','Locaciones externas','Para fotos en el Jardín Botánico o el Mirador Norte, los costos de entrada y demás gastos de acceso corren por cuenta del cliente.')]
pol_html=''.join(f'<div class="pol"><span>{a}</span><div><b>{esc(b)}</b><p>{esc(c)}</p></div></div>' for a,b,c in pol)
css=open('style2.css').read()
css_imgs=open('imgs.css').read()
cards=''.join(f'''
  <a class="card cat" href="#planes" data-go="{i}" data-cat="{i}" data-price="{fprice(c)}">
    <div class="card-img img-{IMG[c['name']]}"></div>
    <div class="card-body">
      <h3>{esc(c['name'])}</h3>
      <span class="price">Desde RD$ {fprice(c):,}</span>
    </div>
  </a>''' for i,c in zip(OTHIDX,OTH))
cat_opts=''.join(f'<option value="{i}">{esc(c["name"])}</option>' for i,c in zip(OTHIDX,OTH))
page=f'''<!DOCTYPE html>
<html lang="es"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hades Photo Studio</title>
<style>
{css}
{css_imgs}
</style>
</head><body>

<header class="top">
  <a href="#inicio" class="logo">HADES PHOTO STUDIO</a>
  <nav>
    <a href="#inicio" class="on">Inicio</a>
    <a href="#sesiones">Sesiones</a>
    <a href="#navidad">Navidad</a>
    <a href="#planes">Planes</a>
    <a href="#extras">Extras</a>
    <a href="#politicas">Políticas</a>
  </nav>
  <div class="tools">
    <a href="https://instagram.com/hadez_photo" aria-label="Instagram">◎</a>
    <a class="btn btn-y" href="#reservar">Reservar</a>
  </div>
</header>

<section id="inicio" class="hero img-nav2">
  <div class="hero-in">
    <div class="hey">Hola, somos HADES PHOTO STUDIO</div>
    <h1>Momentos reales que se quedan</h1>
    <p class="lead">Retratos de familia, parejas, graduaciones, imagen profesional y temporada navideña. Guardar momentos que cambian demasiado rápido.</p>
    <div class="ctas">
      <a class="btn btn-y" href="#planes">Ver planes →</a>
      <a class="btn btn-w" href="#navidad">Sesiones de Navidad · limitadas</a>
    </div>
  </div>
  
</section>



<section class="about sec-off">
  <div class="wrap">
        </div>
    <div>
      <span class="eyebrow">Sobre nosotros</span><span class="yline"></span>
      <h2>Hola, somos HADES PHOTO STUDIO</h2>
      <p>Cada sesión se adapta a ti y a los tuyos: un retrato tranquilo, una celebración o una foto de familia, con la calma que necesitas para que se vean naturales.</p>
      <div class="stats">
        <div><b>{ncat}</b><span>Tipos de sesión</span></div>
        <div><b>{nplans}</b><span>Planes disponibles</span></div>
        <div><b>10</b><span>Fotos de Navidad</span></div>
      </div>
    </div>
  </div>
</section>

<section id="sesiones">
  <div class="wrap">
    <div class="tiles-head">
      <div><span class="eyebrow">Sesiones</span><span class="yline"></span><h2 style="margin-top:14px">Elige tu sesión</h2></div>
      <p style="max-width:380px;color:#6b6b6b;font-size:14px">Tenemos opciones para cada etapa de la vida, desde el primer día hasta la graduación.</p>
    </div>
    <div class="finder">
      <label>Categoría<select id="fCat"><option value="all">Todas</option>{cat_opts}</select></label>
      <label>Presupuesto<select id="fPrice"><option value="all">Cualquiera</option><option value="5000">Hasta RD$ 5,000</option><option value="8000">Hasta RD$ 8,000</option><option value="12000">Hasta RD$ 12,000</option></select></label>
      
      <button id="fGo" class="go">Buscar</button>
    </div>
    <p id="status" class="noRes" style="margin:-8px 0 22px"></p>
    <div class="cards" id="cards">{cards}</div>
    <p id="noRes" class="noRes" hidden>No hay sesiones con esos filtros. Prueba con otro presupuesto.</p>
  </div>
</section>

<section id="navidad" class="xmas">
  <div class="wrap">
    <div class="xmas-top">
      <div>
        <span class="xmas-tag">Temporada limitada</span>
        <h2>Sesiones de Navidad</h2>
        <p>Solo disponibles durante la temporada navideña. Sesiones en estudio, de 1 hora, para 2 a 6 personas.</p>
      </div>
      <a class="btn btn-k" href="#navidad-planes">Ver planes de Navidad →</a>
    </div>
    <p class="swipe-hint">Desliza para ver las 10 fotos →</p>
    <div class="slider">{gal}</div>
    <div id="navidad-planes">
    {navplans}
    <div class="casa-head"><span class="xmas-tag">Navidad en casa · temporada limitada</span><h3>Nosotros llegamos a tu hogar</h3><p>Hacemos tus fotos navideñas en la casa que tú decoraste. Solo disponibles durante la temporada navideña. Sesiones de 1 hora.</p></div>
    {casaplans}
    </div>
  </div>
</section>


<section id="planes">
  <div class="wrap">
    <div class="sec-title">
      <div><span class="eyebrow">Planes y precios</span><span class="yline"></span><h2>Tres niveles para cada etapa</h2></div>
      <p>Elige la categoría y compara los planes. Los precios son por sesión.</p>
    </div>
    <div class="tabs">{tabs}</div>
    {''.join(panels)}
  </div>
</section>

<section class="band">
  <span class="eyebrow">La experiencia</span>
  <h2 style="margin-top:14px">Sin prisa, a su ritmo</h2>
  <p>Pausas, conversación y tiempo para que las fotos se vean naturales, sea cual sea la sesión.</p>
</section>

<section id="extras">
  <div class="wrap">
    <div class="sec-title">
      <div><span class="eyebrow">Extras</span><span class="yline"></span><h2>Más allá de la pantalla</h2></div>
      <p>Complementa tu sesión con impresiones, productos y servicios adicionales.</p>
    </div>
    <div class="extra-grid">{extras_html}</div>
  </div>
</section>

<section id="politicas" class="sec-off">
  <div class="wrap">
    <div class="sec-title">
      <div><span class="eyebrow">Políticas</span><span class="yline"></span><h2>Antes de reservar</h2></div>
      <p>Reglas claras para que la experiencia sea tranquila para todos.</p>
    </div>
    <div class="pols">{pol_html}</div>
  </div>
</section>

<section id="reservar">
  <div class="wrap">
    <div class="reserve">
      <div>
        <span class="eyebrow" style="color:var(--y)">Reserva tu sesión</span>
        <h2 style="margin-top:12px">Mañana ya serán un poco más grandes</h2>
        <p>Fechas limitadas. Para newborn, recomendamos reservar durante el embarazo y confirmar el día tras el nacimiento.</p>
        <div style="margin-top:24px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-y" href="https://wa.me/18294974585">Escribir por WhatsApp →</a><a class="btn btn-w" href="https://instagram.com/hadez_photo">Ver Instagram</a></div>
      </div>
      <dl>
        <dt>WhatsApp</dt><dd>+1 (829) 497-4585</dd>
        <dt>Instagram</dt><dd>@hadez_photo</dd>
        <dt>Teléfono</dt><dd>+1 (829) 497-4585</dd>
        <dt>Dirección</dt><dd>Los Humildes, Calle Principal Flor de Cayena #18</dd>
      </dl>
    </div>
  </div>
</section>



<footer>
  <div class="cols">
    <div><div class="logo" style="font-size:22px">HADES PHOTO STUDIO</div><p style="margin-top:14px;font-size:14px;color:#6b6b6b;max-width:260px">Guardar momentos que cambian demasiado rápido.</p></div>
    <div><h4>Páginas</h4><ul><li><a href="#inicio">Inicio</a></li><li><a href="#sesiones">Sesiones</a></li><li><a href="#navidad">Navidad</a></li><li><a href="#planes">Planes</a></li><li><a href="#extras">Extras</a></li><li><a href="#politicas">Políticas</a></li></ul></div>
    <div><h4>Sesiones</h4><ul><li><a href="#navidad">Navidad (temporada limitada)</a></li>{''.join(f'<li><a href="#planes" data-go="{i}">{esc(c["name"])}</a></li>' for i,c in zip(OTHIDX,OTH))}</ul></div>
    <div><h4>Contacto</h4><ul><li>+1 (829) 497-4585</li><li>@hadez_photo</li><li>Los Humildes, Calle Principal Flor de Cayena #18</li></ul></div>
  </div>
  <div class="bottom"><span>© Hades Photo Studio</span><span>Hecho en República Dominicana</span></div>
</footer>

<script>
(function(){{
  var tabs=document.querySelectorAll('.tab');
  function show(i){{
    tabs.forEach(function(t){{t.classList.toggle('active',t.dataset.tab==i)}});
    document.querySelectorAll('.panel').forEach(function(p){{p.classList.toggle('active',p.dataset.panel==i)}});
  }}
  tabs.forEach(function(t){{t.addEventListener('click',function(){{show(t.dataset.tab)}})}});
  document.querySelectorAll('[data-go]').forEach(function(a){{a.addEventListener('click',function(){{show(a.dataset.go)}})}});
  var cards=[].slice.call(document.querySelectorAll('#cards .card'));
  var plans=[].slice.call(document.querySelectorAll('.panel .plan'));
  var fmt=function(n){{return n.toLocaleString('en-US')}};
  function apply(){{
    var cat=document.getElementById('fCat').value, pr=document.getElementById('fPrice').value;
    var budget=pr==='all'?null:+pr, shown=0;
    /* categories: keep those with at least one plan within the budget */
    cards.forEach(function(c){{
      var ok=(cat==='all'||c.dataset.cat===cat)&&(budget===null||+c.dataset.price<=budget);
      c.hidden=!ok; if(ok) shown++;
    }});
    /* plans: same budget rule, so the prices shown match the search */
    var planCount=0;
    plans.forEach(function(p){{
      var ok=budget===null||+p.dataset.price<=budget;
      p.hidden=!ok; if(ok) planCount++;
    }});
    document.getElementById('noRes').hidden=shown>0;
    var msg=shown+' categoría(s)'+(budget===null?'':' con planes hasta RD$ '+fmt(budget))+(cat==='all'?'':'');
    document.getElementById('status').textContent=(cat==='all'&&budget===null)?'':msg;
    /* tabs only for categories that match; open the right panel */
    var tabEls=[].slice.call(document.querySelectorAll('.tab'));
    tabEls.forEach(function(t){{
      var c=document.querySelector('#cards .card[data-cat="'+t.dataset.tab+'"]');
      t.hidden=c?c.hidden:false;
    }});
    if(cat!=='all'){{ show(cat); }}
    else{{
      var first=tabEls.filter(function(t){{return !t.hidden}})[0];
      if(first) show(first.dataset.tab);
    }}
  }}
  document.getElementById('fCat').addEventListener('change',apply);
  document.getElementById('fPrice').addEventListener('change',apply);
  document.getElementById('fGo').addEventListener('click',function(){{apply();var t=(document.getElementById('fCat').value==='all')?'sesiones':'planes';document.getElementById(t).scrollIntoView({{behavior:'smooth'}})}});
}})();
</script>
</body></html>'''
open('index2.html','w',encoding='utf-8').write(page)
print('KB',len(page)//1024)
