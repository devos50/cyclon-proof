#!/usr/bin/env python3
"""Check portable repository structure, current-document links, and TeX labels."""
from collections import Counter
import ast
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    errors = []
    docs = [ROOT / 'README.md', ROOT / 'AGENTS.md', ROOT / 'archive/README.md', *sorted((ROOT / 'docs').glob('*.md'))]
    links = 0
    for path in docs:
        for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)', path.read_text()):
            if target.startswith(('https:', 'http:', 'mailto:', '#')):
                continue
            filename = target.split('#')[0]
            if filename and not (path.parent / filename).resolve().exists():
                errors.append(f'Broken link in {path.relative_to(ROOT)}: {target}')
            links += 1
    source = (ROOT / 'paper/main.tex').read_text()
    labels = re.findall(r'\\label\{([^}]+)\}', source)
    duplicates = [key for key, count in Counter(labels).items() if count > 1]
    errors += ['Duplicate TeX label: ' + key for key in duplicates]
    for key in set(re.findall(r'\\(?:ref|eqref|pageref)\{([^}]+)\}', source)) - set(labels):
        errors.append('Missing TeX reference target: ' + key)
    for path in docs:
        for key in re.findall(r'`((?:thm|lem|prop|cor|sec):[A-Za-z0-9_-]+)`', path.read_text()):
            if key not in labels:
                errors.append(f'Missing documented label in {path.name}: {key}')
    scripts = list((ROOT / 'verification').rglob('*.py')) + list((ROOT / 'tools').glob('*.py'))
    for path in scripts:
        try:
            ast.parse(path.read_text(), filename=str(path))
        except SyntaxError as error:
            errors.append(str(error))
        if path != Path(__file__) and ('/Users/' in path.read_text() or '/private/tmp/' in path.read_text()):
            errors.append('Machine path in maintained source: ' + str(path.relative_to(ROOT)))
    for item in json.loads((ROOT / 'docs/MIGRATION-MANIFEST.json').read_text())['files']:
        if not (ROOT / item['saved_as']).exists():
            errors.append('Missing migrated artifact: ' + item['saved_as'])
    if errors:
        raise SystemExit('\n'.join(errors))
    subprocess.run([sys.executable, '-B', str(ROOT / 'tools/build_index.py'), '--check'], cwd=ROOT, check=True)
    print(f'PASS repository: {links} local links, {len(labels)} labels, {len(scripts)} maintained Python files, preserved-artifact presence')


if __name__ == '__main__':
    main()
