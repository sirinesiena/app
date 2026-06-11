import re, glob

div = '    <div id="scroll-progress" role="progressbar" aria-label="Progression de lecture" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>'

for filepath in glob.glob('*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'scroll-progress' not in content:
        content = re.sub(r'(<body[^>]*>)', r'\1\n' + div, content, count=1)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Added: {filepath}')
    else:
        print(f'Already present: {filepath}')

# Fix typo "emballages de the preliminaires" -> "emballages de the"
for filepath in ['projets.html']:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    fixed = content.replace('emballages de th\u00e9 pr\u00e9liminaires', 'emballages de th\u00e9 japonais')
    if fixed != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed)
        print(f'Fixed typo in: {filepath}')
    else:
        print(f'Typo not found (may already be fixed): {filepath}')

print('Done.')
