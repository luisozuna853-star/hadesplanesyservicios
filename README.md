# Hades Photo Studio — sitio web

- `index.html` es el sitio completo (un solo archivo, con las imágenes incluidas). Es lo que se publica.
- `fuente/` contiene los archivos con los que se generó el index (para editarlo después):
  - `build2.py` genera el index a partir de `plans.json`, `style2.css` e `imgs.css`.
  - Para regenerarlo: `python3 build2.py` (necesita Python 3 y Pillow).

Para publicar en Vercel: el `index.html` tiene que estar en la raíz del repositorio.
