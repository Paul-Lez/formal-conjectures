#!/usr/bin/env python3
"""
Post-process Verso literate HTML output to fix deployment issues.

Fixes:
1. Adds KaTeX for LaTeX rendering in docstrings
2. Creates stub JS files for missing search infrastructure
3. Fixes domain-mappers.js module syntax
4. Adds the Formal Conjectures source-page styles and navigation helpers

Usage: python3 fix_literate_html.py <literate-html-dir>
"""

import os
import re
import shutil
import sys

KATEX_HEAD = '''
    <!-- KaTeX for LaTeX in docstrings -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.21/dist/katex.min.css" crossorigin="anonymous">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.21/dist/katex.min.js" crossorigin="anonymous"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.21/dist/contrib/auto-render.min.js" crossorigin="anonymous"></script>
'''

KATEX_BODY_SCRIPT = '''
<script>
document.addEventListener("DOMContentLoaded", function() {
  if (typeof renderMathInElement === 'function') {
    renderMathInElement(document.body, {
      delimiters: [
        {left: '$$', right: '$$', display: true},
        {left: '$', right: '$', display: false},
      ],
      throwOnError: false
    });
  }
});
</script>
'''

SITE_HEAD = '''
    <link rel="stylesheet" href="formal-conjectures.css">
    <script defer src="formal-conjectures.js"></script>
'''

SITE_HOME_LINK = '''
          <a class="site-home-link" href="../" title="Return to the Formal Conjectures website">← Main site</a>'''

SITE_NAV_FILTER = '''
            <label class="module-filter-label" for="module-filter">Filter modules</label>
            <input class="module-filter" id="module-filter" type="search"
              placeholder="Filter modules…" autocomplete="off">'''


def fix_html_file(path):
    """Inject site assets and KaTeX into a Verso HTML file."""
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    modified = False

    # Add KaTeX CSS+JS before </head>
    if 'katex' not in html.lower() and '</head>' in html:
        html = html.replace('</head>', KATEX_HEAD + '  </head>')
        modified = True

    # Add auto-render script before </body>
    if 'renderMathInElement(document.body' not in html and '</body>' in html:
        html = html.replace('</body>', KATEX_BODY_SCRIPT + '</body>')
        modified = True

    if 'formal-conjectures.css' not in html and '</head>' in html:
        html = html.replace('</head>', SITE_HEAD + '  </head>')
        modified = True

    if 'site-home-link' not in html:
        html = html.replace(
            '<header class="title-bar">',
            '<header class="title-bar">' + SITE_HOME_LINK,
            1,
        )
        modified = True

    if 'module-filter' not in html:
        html = re.sub(
            r'(<div class="nav-title">\s*FormalConjectures</div>)',
            r'\1' + SITE_NAV_FILTER,
            html,
            count=1,
        )
        modified = True

    if modified:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
    return modified


def copy_site_assets(literate_dir):
    """Copy the source-page stylesheet and script to the literate root."""
    source_dir = os.path.dirname(__file__)
    assets = {
        os.path.join(source_dir, 'src', 'css', 'literate.css'): 'formal-conjectures.css',
        os.path.join(source_dir, 'src', 'js', 'literate.js'): 'formal-conjectures.js',
    }
    for source, name in assets.items():
        shutil.copyfile(source, os.path.join(literate_dir, name))


def create_stubs(literate_dir):
    """Create stub files for missing Verso search infrastructure."""
    search_dir = os.path.join(literate_dir, '-verso-search')
    os.makedirs(search_dir, exist_ok=True)

    stubs = {
        'searchIndex.js': '// Stub: search index not available for literate pages\n',
        'search-init.js': '// Stub: search not available for literate pages\n',
        'elasticlunr.min.js': '// Stub\n',
    }
    for name, content in stubs.items():
        path = os.path.join(search_dir, name)
        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write(content)
            print(f'  Created stub: -verso-search/{name}')

    # Fix domain-mappers.js: remove export statements that cause syntax errors
    # when loaded without type="module"
    dm_path = os.path.join(search_dir, 'domain-mappers.js')
    if os.path.exists(dm_path):
        with open(dm_path, 'r') as f:
            content = f.read()
        if 'export ' in content:
            # Wrap in IIFE and remove exports
            fixed = content.replace('export ', '')
            with open(dm_path, 'w') as f:
                f.write(fixed)
            print('  Fixed domain-mappers.js (removed export statements)')


def main():
    if len(sys.argv) < 2:
        print('Usage: python3 fix_literate_html.py <literate-html-dir>', file=sys.stderr)
        sys.exit(1)

    literate_dir = sys.argv[1]
    if not os.path.isdir(literate_dir):
        print(f'  Warning: {literate_dir} not found, skipping.', file=sys.stderr)
        return

    # Create stubs for missing JS files
    create_stubs(literate_dir)
    copy_site_assets(literate_dir)

    # Fix all HTML files
    count = 0
    for dirpath, _, filenames in os.walk(literate_dir):
        for f in filenames:
            if f == 'index.html':
                path = os.path.join(dirpath, f)
                if fix_html_file(path):
                    count += 1

    print(f'  Styled {count} Verso HTML files.')


if __name__ == '__main__':
    main()
