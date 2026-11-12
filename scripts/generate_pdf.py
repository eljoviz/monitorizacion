import os
import re
import base64
import subprocess
import markdown

REPO_DIR = '/home/2asird/monitorizacion'
IMG_DIR = os.path.join(REPO_DIR, 'img')
HTML_OUT = '/tmp/monitorizacion_completa.html'
PDF_OUT = os.path.join(REPO_DIR, 'Monitorizacion_Sistemas_Linux_Jose_Vizuete.pdf')
GITHUB_URL = 'https://github.com/eljoviz/monitorizacion/tree/main'

def img_to_b64(match):
    src = match.group(1)
    basename = os.path.basename(src)
    full_path = os.path.join(IMG_DIR, basename)
    if not os.path.exists(full_path):
        print(f"Warning: Image not found: {full_path}")
        return match.group(0)
    
    with open(full_path, 'rb') as f:
        data = f.read()
    
    ext = os.path.splitext(basename)[1].lower()
    mime = 'image/svg+xml' if ext == '.svg' else 'image/png'
    b64 = base64.b64encode(data).decode('utf-8')
    return f'src="data:{mime};base64,{b64}"'

def read_md(filename):
    with open(os.path.join(REPO_DIR, filename), 'r', encoding='utf-8') as f:
        return f.read()

# Build Cover Page
cover_html = f"""
<div class="cover-page">
  <div class="cover-banner">
    <img src="img/banner.svg" alt="Monitorización en Linux" style="max-width: 100%; border: none; box-shadow: none;">
  </div>
  
  <h1 class="cover-title">Monitorización de Sistemas Linux</h1>
  <p class="cover-subtitle">Administración de Sistemas Informáticos en Red (ASIR) • Herramientas y Técnicas DevOps</p>
  
  <div class="github-box">
    <div class="github-icon">
      <svg height="28" width="28" viewBox="0 0 16 16" fill="currentColor">
        <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
      </svg>
    </div>
    <div class="github-content">
      <span class="github-label">Repositorio Oficial en GitHub:</span>
      <a href="{GITHUB_URL}" class="github-url">{GITHUB_URL}</a>
    </div>
  </div>

  <div class="cover-meta">
    <p><strong>Autor:</strong> Jose Vizuete</p>
    <p><strong>Especialidad:</strong> Administración de Sistemas Operativos Linux (ASIR 2)</p>
    <p><strong>Módulos:</strong> Procesos, Memoria/Swap, E/S Disco, Tráfico de Red y Tarea Práctica</p>
    <p><strong>Fecha de Compilación:</strong> Noviembre 2026</p>
  </div>
</div>
"""

# Build Table of Contents
index_html = f"""
<div id="indice-general">
  <h2>📑 Índice General del Proyecto</h2>
  
  <div class="index-card">
    <h3>1. <a href="#capitulo-1">Procesos y Rendimiento de CPU</a></h3>
    <p>Estados de los procesos, filtrado con <code>ps</code> (<code>ps a</code>, <code>ps au</code>, <code>ps aux</code>, <code>ps -C</code>, <code>ps -u</code>), monitorización interactiva en tiempo real con <code>top</code> y <code>htop</code>, captura en batch a fichero y eliminación de procesos en bucle.</p>
  </div>

  <div class="index-card">
    <h3>2. <a href="#capitulo-2">Memoria, Espacio y Rendimiento de Disco</a></h3>
    <p>Gestión de memoria RAM física, Buffers, Page Cache y Swap con <code>free</code> (modificadores <code>-h</code>, <code>-m</code>, <code>-s</code>, <code>-w</code>, <code>-t</code>), estadísticas con <code>vmstat</code>, control de particiones Swap (<code>swapon</code>/<code>swapoff</code>), rendimiento de E/S con <code>iostat</code> (métrica <code>%util</code>) y diagnóstico con <code>df -h</code>.</p>
  </div>

  <div class="index-card">
    <h3>3. <a href="#capitulo-3">Tráfico y Monitorización de Red</a></h3>
    <p>Interfaces y estadísticas con <code>ip link</code>/<code>ip -s</code>, sockets y puertos en escucha con <code>ss -plunt</code>, conexiones TCP activas con <code>ss -tnp</code>, titularidad IP con <code>whois</code>, auditoría con <code>nmap</code> (<code>-sn</code>, <code>-sV</code>), tabla <code>arp</code>, ancho de banda con <code>iptraf</code>, <code>tcptrack</code> y <code>bmon</code>, y diagnóstico con <code>tcpdump</code>, <code>ping</code> y <code>traceroute</code>.</p>
  </div>

  <div class="index-card">
    <h3>4. <a href="#capitulo-4">Tarea Práctica: Análisis de Red Local</a></h3>
    <p>Práctica de laboratorio evaluable paso a paso: Configuración IPv4 de red (<code>ip a</code>, <code>ip r</code>), gestión y renovación de la caché de vecinos ARP (<code>arp -a</code>, <code>arp -n</code>, <code>ip neigh</code>, eliminación y regeneración), descubrimiento de red con Nmap (<code>-sn</code>) y auditoría de puertos y versiones de servicios (<code>-sV</code>).</p>
  </div>
</div>
"""

ch1_md = read_md('1.md')
ch2_md = read_md('2.md')
ch3_md = read_md('3.md')
ch4_md = read_md('4.md')

ch1_html = markdown.markdown(ch1_md.replace('[⬅️ Volver al Índice Principal](README.md)', '<a href="#indice-general" class="back-link">⬅️ Volver al Índice General</a>'), extensions=['tables', 'fenced_code'])
ch2_html = markdown.markdown(ch2_md.replace('[⬅️ Volver al Índice Principal](README.md)', '<a href="#indice-general" class="back-link">⬅️ Volver al Índice General</a>'), extensions=['tables', 'fenced_code'])
ch3_html = markdown.markdown(ch3_md.replace('[⬅️ Volver al Índice Principal](README.md)', '<a href="#indice-general" class="back-link">⬅️ Volver al Índice General</a>'), extensions=['tables', 'fenced_code'])
ch4_html = markdown.markdown(ch4_md.replace('[⬅️ Volver al Índice Principal](README.md)', '<a href="#indice-general" class="back-link">⬅️ Volver al Índice General</a>'), extensions=['tables', 'fenced_code'])

document_body = f"""
{cover_html}

<div class="page-break"></div>

<table class="document-layout">
  <thead>
    <tr>
      <td>
        <div class="page-running-header">
          <span class="header-left">🐧 Monitorización de Sistemas Linux — <strong>Jose Vizuete</strong></span>
          <span class="header-right">
            <svg height="12" width="12" viewBox="0 0 16 16" fill="#0969da" style="vertical-align: middle; margin-right: 3px;">
              <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
            </svg>
            <a href="{GITHUB_URL}" class="repo-link">{GITHUB_URL}</a>
          </span>
        </div>
      </td>
    </tr>
  </thead>
  <tfoot>
    <tr>
      <td>
        <div class="page-running-footer">
          <span>Administración de Sistemas Informáticos en Red (ASIR 2)</span>
          <span>GitHub: <a href="{GITHUB_URL}">{GITHUB_URL}</a></span>
        </div>
      </td>
    </tr>
  </tfoot>
  <tbody>
    <tr>
      <td>
        {index_html}

        <div class="page-break"></div>

        <section id="capitulo-1" class="chapter">
          {ch1_html}
        </section>

        <div class="page-break"></div>

        <section id="capitulo-2" class="chapter">
          {ch2_html}
        </section>

        <div class="page-break"></div>

        <section id="capitulo-3" class="chapter">
          {ch3_html}
        </section>

        <div class="page-break"></div>

        <section id="capitulo-4" class="chapter">
          {ch4_html}
        </section>
      </td>
    </tr>
  </tbody>
</table>
"""

# Convert images to base64
document_body = re.sub(r'src="([^"]+)"', img_to_b64, document_body)

css = f"""
@charset "UTF-8";

@page {{
  size: A4;
  margin: 14mm 14mm 16mm 14mm;
}}

body {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  font-size: 12.5px;
  line-height: 1.55;
  color: #24292f;
  background-color: #ffffff;
  margin: 0;
  padding: 0;
}}

/* Table Layout for Repeating Header & Footer */
table.document-layout {{
  width: 100%;
  border-collapse: collapse;
  border: none;
}}

table.document-layout > thead {{
  display: table-header-group;
}}

table.document-layout > tfoot {{
  display: table-footer-group;
}}

table.document-layout > thead > tr > td {{
  border: none;
  padding: 0 0 10px 0;
}}

table.document-layout > tfoot > tr > td {{
  border: none;
  padding: 10px 0 0 0;
}}

table.document-layout > tbody > tr > td {{
  border: none;
  padding: 0;
}}

.page-running-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1.5px solid #0969da;
  padding-bottom: 5px;
  margin-bottom: 12px;
  font-size: 10px;
  color: #57606a;
}}

.page-running-header a.repo-link {{
  color: #0969da;
  font-weight: 600;
  text-decoration: underline;
}}

.page-running-footer {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #d0d7de;
  padding-top: 5px;
  font-size: 9px;
  color: #57606a;
}}

.page-running-footer a {{
  color: #0969da;
  text-decoration: none;
}}

.page-break {{
  page-break-before: always;
}}

/* Cover Page */
.cover-page {{
  text-align: center;
  padding: 40px 20px 20px 20px;
}}

.cover-banner img {{
  max-width: 100%;
  height: auto;
  margin-bottom: 25px;
}}

.cover-title {{
  font-size: 32px;
  font-weight: 800;
  color: #1f2328;
  margin: 15px 0 10px 0;
  border: none;
}}

.cover-subtitle {{
  font-size: 14px;
  color: #57606a;
  margin-bottom: 35px;
}}

.github-box {{
  display: inline-flex;
  align-items: center;
  background-color: #f6f8fa;
  border: 1.5px solid #d0d7de;
  border-radius: 8px;
  padding: 14px 22px;
  margin: 20px auto 30px auto;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}}

.github-icon {{
  margin-right: 14px;
  display: flex;
  align-items: center;
  color: #24292f;
}}

.github-content {{
  display: flex;
  flex-direction: column;
  text-align: left;
}}

.github-label {{
  font-size: 11px;
  font-weight: 600;
  color: #57606a;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}}

.github-url {{
  font-size: 13.5px;
  font-weight: 600;
  color: #0969da;
  text-decoration: none;
}}

.cover-meta {{
  margin-top: 40px;
  padding-top: 25px;
  border-top: 1px solid #d0d7de;
  font-size: 12px;
  color: #57606a;
  text-align: center;
}}

.cover-meta p {{
  margin: 5px 0;
}}

/* Index Page */
#indice-general {{
  padding: 5px 0;
}}

#indice-general h2 {{
  font-size: 20px;
  color: #1f2328;
  border-bottom: 2px solid #0969da;
  padding-bottom: 8px;
  margin-bottom: 20px;
}}

.index-card {{
  background: #f6f8fa;
  border-left: 4px solid #0969da;
  border-radius: 0 6px 6px 0;
  padding: 12px 16px;
  margin-bottom: 14px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}}

.index-card h3 {{
  margin: 0 0 6px 0;
  font-size: 15px;
}}

.index-card h3 a {{
  color: #0969da;
  text-decoration: none;
}}

.index-card p {{
  margin: 0;
  font-size: 12px;
  color: #57606a;
}}

/* Headings */
h1 {{
  font-size: 21px;
  font-weight: 700;
  color: #0969da;
  border-bottom: 2px solid #eaecef;
  padding-bottom: 8px;
  margin-top: 25px;
  margin-bottom: 15px;
  page-break-after: avoid;
}}

h2 {{
  font-size: 16px;
  font-weight: 600;
  color: #1f2328;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 5px;
  margin-top: 20px;
  margin-bottom: 10px;
  page-break-after: avoid;
}}

h3 {{
  font-size: 14px;
  font-weight: 600;
  color: #24292f;
  margin-top: 16px;
  margin-bottom: 8px;
  page-break-after: avoid;
}}

/* Links */
a {{
  color: #0969da;
  text-decoration: none;
}}

/* Images */
img {{
  max-width: 90%;
  height: auto;
  border: 1px solid #d0d7de;
  border-radius: 6px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
  margin: 10px auto;
  display: block;
  page-break-inside: avoid;
}}

div[align="center"] {{
  text-align: center;
  margin: 14px 0;
  page-break-inside: avoid;
}}

/* Tables (Markdown data tables) */
.chapter table,
#indice-general table {{
  border-collapse: collapse;
  width: 100%;
  margin: 14px 0;
  font-size: 12px;
  page-break-inside: avoid;
}}

.chapter th, .chapter td,
#indice-general th, #indice-general td {{
  border: 1px solid #d0d7de;
  padding: 6px 10px;
  text-align: left;
}}

.chapter th, #indice-general th {{
  background-color: #f6f8fa;
  font-weight: 600;
}}

.chapter tr:nth-child(2n) {{
  background-color: #fbfcfd;
}}

/* Code & Preformatted */
code {{
  font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
  font-size: 85%;
  background-color: rgba(175, 184, 193, 0.2);
  padding: 0.2em 0.4em;
  border-radius: 4px;
}}

pre {{
  font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
  font-size: 11px;
  background-color: #f6f8fa;
  border: 1px solid #d0d7de;
  border-radius: 6px;
  padding: 10px 14px;
  overflow-x: auto;
  line-height: 1.45;
  page-break-inside: avoid;
}}

pre code {{
  background-color: transparent;
  padding: 0;
  border-radius: 0;
  font-size: inherit;
}}

/* Blockquotes */
blockquote {{
  border-left: 4px solid #0969da;
  padding: 8px 14px;
  color: #57606a;
  background-color: #f6f8fa;
  border-radius: 0 6px 6px 0;
  margin: 12px 0;
  font-size: 12.5px;
  page-break-inside: avoid;
}}

blockquote p {{
  margin: 4px 0;
}}

/* Keyboard tags */
kbd {{
  display: inline-block;
  padding: 2px 5px;
  font-size: 10px;
  line-height: 10px;
  color: #24292f;
  vertical-align: middle;
  background-color: #f6f8fa;
  border: solid 1px rgba(175, 184, 193, 0.4);
  border-bottom-color: rgba(175, 184, 193, 0.6);
  border-radius: 4px;
  box-shadow: inset 0 -1px 0 rgba(175, 184, 193, 0.4);
}}

/* Horizontal Rule */
hr {{
  height: 1px;
  background-color: #d0d7de;
  border: none;
  margin: 20px 0;
}}

/* Back link */
.back-link {{
  display: inline-block;
  margin-top: 15px;
  font-weight: 500;
}}
"""

html_document = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Monitorización de Sistemas Linux - Jose Vizuete</title>
  <style>
{css}
  </style>
</head>
<body>
{document_body}
</body>
</html>
"""

with open(HTML_OUT, 'w', encoding='utf-8') as f:
    f.write(html_document)

print(f"HTML generado con éxito en: {HTML_OUT} ({os.path.getsize(HTML_OUT)} bytes)")

# Convert HTML to PDF using Google Chrome headless
cmd = [
    'google-chrome',
    '--headless=new',
    '--no-pdf-header-footer',
    '--generate-pdf-document-outline',
    f'--print-to-pdf={PDF_OUT}',
    HTML_OUT
]

print("Generando PDF con Google Chrome...")
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0:
    print(f"PDF generado con éxito: {PDF_OUT} ({os.path.getsize(PDF_OUT)} bytes)")
else:
    print(f"Error generando PDF: {res.stderr}")
