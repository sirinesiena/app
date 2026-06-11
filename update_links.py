import os
import glob

files = glob.glob('*.html')
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the sentence if it still exists
    content = content.replace(' - pour créer avec ceux qui font le luxe', '')
    content = content.replace('pour créer avec ceux qui font le luxe', '')
    
    # Update CV link base
    content = content.replace('href="assets/documents/CV-SIRINE-GHERBAOUI-26.pdf"', 'href="assets/documents/CV-Sirine-Gherbaoui.pdf" download="CV-Sirine-Gherbaoui.pdf"')
    
    # Add Portfolio to nav
    nav_cv_str = '<a href="assets/documents/CV-Sirine-Gherbaoui.pdf" class="nav-cv" target="_blank" rel="noopener" download="CV-Sirine-Gherbaoui.pdf">CV</a>'
    if nav_cv_str in content:
        content = content.replace(
            nav_cv_str,
            nav_cv_str + '\n        <a href="assets/documents/Portfolio-Sirine-Gherbaoui.pdf" class="nav-cv" target="_blank" rel="noopener" download="Portfolio-Sirine-Gherbaoui.pdf">Portfolio</a>'
        )
    
    # Add Portfolio to footer
    footer_cv_str = '<a href="assets/documents/CV-Sirine-Gherbaoui.pdf" target="_blank" rel="noopener" download="CV-Sirine-Gherbaoui.pdf">CV PDF</a>'
    if footer_cv_str in content:
        content = content.replace(
            footer_cv_str,
            footer_cv_str + '\n            <a href="assets/documents/Portfolio-Sirine-Gherbaoui.pdf" target="_blank" rel="noopener" download="Portfolio-Sirine-Gherbaoui.pdf">Portfolio PDF</a>'
        )
        
    # Add Portfolio to footer (English)
    footer_cv_str_en = '<a href="assets/documents/CV-Sirine-Gherbaoui.pdf" target="_blank" rel="noopener" download="CV-Sirine-Gherbaoui.pdf">CV (PDF)</a>'
    if footer_cv_str_en in content:
        content = content.replace(
            footer_cv_str_en,
            footer_cv_str_en + '\n            <a href="assets/documents/Portfolio-Sirine-Gherbaoui.pdf" target="_blank" rel="noopener" download="Portfolio-Sirine-Gherbaoui.pdf">Portfolio PDF</a>'
        )

    # Update drive links in index.html and index-en.html
    content = content.replace('href="https://drive.google.com/file/d/14OA_WPc_7rlD-Xvg9fXyvrwlT3iEa15U/view?usp=drive_link"', 'href="assets/documents/Portfolio-Sirine-Gherbaoui.pdf" download="Portfolio-Sirine-Gherbaoui.pdf"')

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("HTML files updated successfully.")
