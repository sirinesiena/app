import re, glob

# 1. Fix og:image to absolute URL in all HTML files
# 2. Add og:title and og:description on pages that lack them
# 3. Fix sitemap.xml (remove .html extensions)
# 4. Add robots.txt
# 5. Remove @import from styles.css
# 6. Fix EN page links (no phantom 404 pages - redirect to FR pages)
# 7. Add hreflang on index.html and index-en.html

domain = "https://sirinegherbaoui.com"

og_metas = {
    "projets.html": {
        "title": "Projets — Sirine Gherbaoui",
        "description": "Études de cas de Sirine Gherbaoui : Typology Matcha Ritual, Chloé Love Letters, La Minute Droit et Sirine Siena.",
        "image": f"{domain}/assets/images/typology-collection.webp"
    },
    "galerie.html": {
        "title": "Galerie — Sirine Siena · Sirine Gherbaoui",
        "description": "Peintures originales de Sirine Siena, exposante à la Galerie Image In'Air, Paris. Acrylique, feuilles d'or, intérieurs parisiens.",
        "image": f"{domain}/assets/images/painting-blue-console.webp"
    },
    "profil.html": {
        "title": "Profil — Sirine Gherbaoui",
        "description": "B3 Marketing Digital & Branding, Sup de Pub. Droit, art, luxe. Disponible en alternance dès septembre 2026.",
        "image": f"{domain}/assets/images/sirine-gherbaoui.jpg"
    },
    "contact.html": {
        "title": "Contact — Sirine Gherbaoui",
        "description": "Contactez Sirine Gherbaoui pour une alternance en marketing digital, branding ou communication culturelle. Disponible dès septembre 2026.",
        "image": f"{domain}/assets/images/painting-blue-desk.webp"
    }
}

hreflang_fr = f'  <link rel="alternate" hreflang="fr" href="{domain}/" />\n  <link rel="alternate" hreflang="en" href="{domain}/index-en" />\n  <link rel="alternate" hreflang="x-default" href="{domain}/" />'
hreflang_en = f'  <link rel="alternate" hreflang="fr" href="{domain}/" />\n  <link rel="alternate" hreflang="en" href="{domain}/index-en" />\n  <link rel="alternate" hreflang="x-default" href="{domain}/" />'

json_ld = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "Sirine Gherbaoui",
    "alternateName": "Sirine Siena",
    "url": "https://sirinegherbaoui.com",
    "email": "sirinesiena@gmail.com",
    "jobTitle": "Étudiante Marketing Digital & Branding",
    "alumniOf": [
      { "@type": "EducationalOrganization", "name": "Sup de Pub" },
      { "@type": "EducationalOrganization", "name": "Université Paris X" },
      { "@type": "EducationalOrganization", "name": "École du Louvre" }
    ],
    "sameAs": [
      "https://www.linkedin.com/in/sirine-gherbaoui-715437168"
    ]
  }
  </script>'''

for filepath in glob.glob('*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix og:image to absolute URL
    content = content.replace(
        'content="assets/images/painting-blue-desk.webp"',
        f'content="{domain}/assets/images/painting-blue-desk.webp"'
    )

    # Add og: metas to pages missing them
    if filepath in og_metas and f'og:title' not in content:
        m = og_metas[filepath]
        og_block = f'''    <meta property="og:type" content="website" />
    <meta property="og:title" content="{m['title']}" />
    <meta property="og:description" content="{m['description']}" />
    <meta property="og:image" content="{m['image']}" />'''
        content = content.replace('<link rel="stylesheet" href="styles.css" />', og_block + '\n    <link rel="stylesheet" href="styles.css" />')

    # Add hreflang on index pages
    if filepath == 'index.html' and 'hreflang' not in content:
        content = content.replace('  </head>', hreflang_fr + '\n  </head>')
    if filepath == 'index-en.html' and 'hreflang' not in content:
        content = content.replace('  </head>', hreflang_en + '\n  </head>')

    # Add JSON-LD on index.html
    if filepath == 'index.html' and 'application/ld+json' not in content:
        content = content.replace('  </head>', json_ld + '\n  </head>')

    # Fix EN links — point to existing pages instead of phantom EN pages
    if filepath == 'index-en.html':
        content = content.replace('href="projets-en.html"', 'href="projets.html"')
        content = content.replace('href="galerie-en.html"', 'href="galerie.html"')
        content = content.replace('href="profil-en.html"', 'href="profil.html"')
        content = content.replace('href="contact-en.html"', 'href="contact.html"')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated: {filepath}")

# Fix sitemap.xml - remove .html extensions
with open('sitemap.xml', 'r', encoding='utf-8') as f:
    sitemap = f.read()

sitemap = sitemap.replace('/index.html', '/')
sitemap = sitemap.replace('/projets.html', '/projets')
sitemap = sitemap.replace('/galerie.html', '/galerie')
sitemap = sitemap.replace('/profil.html', '/profil')
sitemap = sitemap.replace('/contact.html', '/contact')

# Add index-en if missing
if 'index-en' not in sitemap:
    sitemap = sitemap.replace('</urlset>', f'  <url><loc>{domain}/index-en</loc></url>\n</urlset>')

with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap)
print("Fixed: sitemap.xml")

# Create robots.txt
with open('robots.txt', 'w', encoding='utf-8') as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {domain}/sitemap.xml\n")
print("Created: robots.txt")

# Remove @import from styles.css
with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()
css = re.sub(r"@import url\('https://fonts\.googleapis\.com[^']+'\);\n?\n?", '', css)
with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(css)
print("Fixed: styles.css (@import removed)")

print("\nAll critical fixes applied!")
