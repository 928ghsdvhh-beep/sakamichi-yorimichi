"""Verify clean and repeated builds reproduce every committed dist byte.

Run: python scripts/check_build.py
The repository's dist is never modified by this check.
"""
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import tempfile


def snapshot(root):
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in root.rglob('*') if p.is_file()}


def compare(expected, actual, label):
    missing = sorted(expected.keys() - actual.keys())
    extra = sorted(actual.keys() - expected.keys())
    changed = sorted(p for p in expected.keys() & actual.keys()
                     if expected[p] != actual[p])
    if missing or extra or changed:
        raise SystemExit(f'{label}: missing={missing}, extra={extra}, changed={changed}')
    print(f'{label}: {len(actual)} files identical')


def main():
    repo = Path(__file__).resolve().parents[1]
    expected = snapshot(repo / 'dist')
    if not expected:
        raise SystemExit('Committed dist is required as the preservation baseline')
    env = dict(os.environ, SITE_URL='https://sakamichi-yorimichi.pages.dev')
    with tempfile.TemporaryDirectory(prefix='yorimichi-build-') as temporary:
        work = Path(temporary)
        shutil.copytree(repo / 'src', work / 'src')
        shutil.copytree(repo / 'scripts', work / 'scripts')
        for label in ('clean build', 'second build'):
            subprocess.run([sys.executable, 'src/build.py'], cwd=work, env=env, check=True)
            compare(expected, snapshot(work / 'dist'), label)
        shutil.rmtree(work / 'dist')
        shutil.copytree(repo / 'dist', work / 'dist')
        subprocess.run([sys.executable, 'src/build.py'], cwd=work, env=env, check=True)
        compare(expected, snapshot(work / 'dist'), 'existing dist build')
        audit = subprocess.run([sys.executable, 'scripts/check_site.py', '.'], cwd=work,
                               env=env, check=True, capture_output=True, text=True)
        result = json.loads(audit.stdout)
        print(f'Static audit: {result["pages"]} pages, {len(result["issues"])} issues')


if __name__ == '__main__':
    main()
