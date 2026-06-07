import os, re, glob
from PIL import Image

def get_dimensions(image_path):
    try:
        with Image.open(image_path) as img:
            return img.width, img.height
    except Exception as e:
        return None, None

new_footer = """<footer class="site-footer">
      <div style="display: flex; gap: 40px; margin-bottom: 30px; flex-wrap: wrap; justify-content: space-between;">
        <div style="flex: 1; min-width: 200px;">
          <h4 style="margin-bottom: 12px; font-family: var(--display); font-size: 1.2rem; font-weight: 500;">Sirine Gherbaoui</h4>
          <p style="opacity: 0.7; font-size: 0.9rem; max-width: 250px;">Marketing digital, branding &amp; communication culturelle. Alternance sept. 2026.</p>
        </div>
        <div style="display: flex; gap: 40px; flex-wrap: wrap;">
          <nav aria-label="Plan du site" style="display: flex; flex-direction: column; gap: 8px;">
            <strong style="margin-bottom: 4px; font-weight: 600;">Plan du site</strong>
            <a href="index.html">Accueil</a>
            <a href="projets.html">Projets</a>
            <a href="galerie.html">Galerie</a>
            <a href="profil.html">Profil</a>
            <a href="contact.html">Contact</a>
          </nav>
          <nav aria-label="Réseaux et documents" style="display: flex; flex-direction: column; gap: 8px;">
            <strong style="margin-bottom: 4px; font-weight: 600;">Contact &amp; Réseaux</strong>
            <a href="mailto:sirinesiena@gmail.com">sirinesiena@gmail.com</a>
            <a href="https://www.linkedin.com/in/sirine-gherbaoui-715437168" target="_blank" rel="noopener">LinkedIn</a>
            <a href="assets/documents/CV-SIRINE-GHERBAOUI-26.pdf" target="_blank" rel="noopener">CV PDF</a>
          </nav>
        </div>
      </div>
      <div style="border-top: 1px solid var(--line); padding-top: 20px; font-size: 0.85rem; opacity: 0.6;">
        <p>© 2026 Sirine Gherbaoui</p>
      </div>
    </footer>"""

html_files = glob.glob('*.html')
for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    def replace_img(match):
        img_tag = match.group(0)
        if 'width=' in img_tag and 'height=' in img_tag:
            return img_tag
        
        src_match = re.search(r'src="([^"]+)"', img_tag)
        if not src_match:
            return img_tag
            
        src = src_match.group(1)
        if not src.startswith('assets/images/'):
            return img_tag
            
        w, h = get_dimensions(src)
        if w and h:
            new_tag = re.sub(r'(/?>)$', f' width="{w}" height="{h}" \\1', img_tag)
            return new_tag
        return img_tag

    new_content = re.sub(r'<img[^>]+>', replace_img, content)
    
    # Fix SEO meta tags
    if 'og:url' not in new_content:
        seo_tags = f'<meta property="og:url" content="https://sirinegherbaoui.com/{html_file}" />\n    <link rel="canonical" href="https://sirinegherbaoui.com/{html_file}" />\n    <link rel="preconnect"'
        new_content = new_content.replace('<link rel="preconnect"', seo_tags, 1)
        
    # Fix alt text for the main hero image
    new_content = new_content.replace('alt=""\n            width="1121"', 'alt="Peinture bureau bleu par Sirine Siena"\n            width="1121"')
    
    # Replace footer
    footer_pattern = re.compile(r'<footer class="site-footer.*?</footer>', re.DOTALL)
    
    # For contact page, we need dark footer variant
    if html_file == 'contact.html':
        footer_html = new_footer.replace('class="site-footer"', 'class="site-footer dark-footer"')
        footer_html = footer_html.replace('border-top: 1px solid var(--line)', 'border-top: 1px solid rgba(255,255,255,0.1)')
    else:
        footer_html = new_footer
        
    new_content = footer_pattern.sub(footer_html, new_content)
        
    if new_content != content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Updated {html_file}')
