#!/usr/bin/env python3
"""Editing and checking helper for the static site. Standard library only.

It is not a build step: the committed HTML is what gets served. The tool only
rewrites the marked shared regions of each page and checks the translations.

  python3 -I tools/site.py chrome          rewrite the shared regions (head, top bar, nav, footer)
  python3 -I tools/site.py check           report stale, missing and extra translated blocks; exit 1 on problems
  python3 -I tools/site.py mark            set or clear data-stale on translated blocks, then rewrite the regions
  python3 -I tools/site.py stamp LANG SLUG [ID ...] [--rev REV]
                                           record the EN hash on translated blocks (all of them if no ID);
                                           --rev: the EN text as of git revision REV, the one the translation was made from

Page format (see README.md): every top-level block inside <article> starts at
column 0 with an id="..." attribute. Nested lines are indented. A translated
block carries the same id and data-src="<hash of the EN block>".
"""
import hashlib, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(ROOT, 'tools', 'site.json'), encoding='utf-8'))
UI = json.load(open(os.path.join(ROOT, 'i18n', 'ui.json'), encoding='utf-8'))
LANGS = CFG['langs']
BASE = CFG['base']

ART_RE = re.compile(r'(<article\b[^>]*>)(.*?)(</article>)', re.S)
BLOCK_START = re.compile(r'^<([a-zA-Z][a-zA-Z0-9]*)\b([^>]*)>', re.M)
ID_RE = re.compile(r'\sid="([^"]+)"')
SRC_RE = re.compile(r'\sdata-src="([0-9a-f]*)"')
STALE_RE = re.compile(r'\sdata-stale="1"')


def path_of(lang, slug):
    return os.path.join(ROOT, lang, slug, 'index.html') if slug else os.path.join(ROOT, lang, 'index.html')


def url_of(lang, slug):
    return f'/{lang}/{slug}/' if slug else f'/{lang}/'


def read(p):
    return open(p, encoding='utf-8').read()


def write(p, s):
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write(s)


def norm_text(fragment):
    refs = re.findall(r'\s(?:href|src)="([^"]*)"', fragment)
    t = re.sub(r'<[^>]+>', ' ', fragment)
    t = html.unescape(t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t + ('|' + ' '.join(refs) if refs else '')


def h12(fragment):
    return hashlib.sha256(norm_text(fragment).encode('utf-8')).hexdigest()[:12]


def blocks(page_html):
    """[(id, start, end, opening-tag attrs, fragment)] for the top-level article blocks."""
    m = ART_RE.search(page_html)
    if not m:
        return []
    body, off = m.group(2), m.start(2)
    starts = list(BLOCK_START.finditer(body))
    out = []
    for i, s in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(body)
        frag = body[s.start():end].rstrip()
        idm = ID_RE.search(' ' + s.group(2))
        out.append((idm.group(1) if idm else None, off + s.start(), off + s.start() + len(frag), s.group(2), frag))
    return out


def article_meta(page_html):
    m = ART_RE.search(page_html)
    a = m.group(1) if m else ''
    get = lambda k: (re.search(k + r'="([^"]*)"', a) or [None, ''])[1]
    h1 = re.search(r'<h1\b[^>]*>(.*?)</h1>', page_html, re.S)
    title = html.unescape(re.sub(r'<[^>]+>', '', h1.group(1))).strip() if h1 else ''
    return {'title': title, 'desc': html.unescape(get('data-desc')), 'nav': html.unescape(get('data-nav')) or title}


def esc(s):
    return html.escape(s, quote=True)


def pages():
    return CFG['pages']


# ---------------------------------------------------------------- chrome

def region(s, name, content):
    a, b = f'<!-- chrome:{name} -->', f'<!-- /chrome:{name} -->'
    i, j = s.find(a), s.find(b)
    if i < 0 or j < 0:
        raise SystemExit(f'missing chrome:{name} markers')
    return s[:i + len(a)] + '\n' + content + '\n' + s[j:]


def render(lang, page, meta_by_lang, stale_ids):
    slug = page['slug']
    ui = UI[lang]
    meta = meta_by_lang[lang][slug]
    site = ui['site_name']
    title = f"{meta['title']} — {site}" if slug else site
    alt = '\n'.join(f'<link rel="alternate" hreflang="{CFG["html_lang"][l]}" href="{BASE}{url_of(l, slug)}">' for l in LANGS)
    head = (f'<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            f'<meta http-equiv="Content-Security-Policy" content="{CFG["csp"]}">\n'
            f'<title>{esc(title)}</title>\n<meta name="description" content="{esc(meta["desc"])}">\n'
            f'<link rel="canonical" href="{BASE}{url_of(lang, slug)}">\n{alt}\n'
            f'<link rel="alternate" hreflang="x-default" href="{BASE}{url_of("en", slug)}">\n'
            f'<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">\n'
            f'<link rel="stylesheet" href="/assets/site.css">\n<script src="/assets/lang.js" defer></script>')
    sw = ' · '.join(
        (f'<a class="lang" href="{url_of(l, slug)}" hreflang="{CFG["html_lang"][l]}" lang="{CFG["html_lang"][l]}" data-lang="{l}"'
         + (' aria-current="true"' if l == lang else '') + f'>{CFG["lang_names"][l]}</a>') for l in LANGS)
    nav_items = []
    for p in pages():
        if not p.get('nav', True):
            continue
        m = meta_by_lang[lang][p['slug']]
        cur = ' aria-current="page"' if p['slug'] == slug else ''
        nav_items.append(f'<li><a href="{url_of(lang, p["slug"])}"{cur}>{esc(m["nav"])}</a></li>')
    notes = []
    state = CFG['review'].get(lang)
    if state and state != 'reviewed':
        notes.append(f'<p class="note review">{esc(ui["review_" + state])} <a href="{url_of("en", slug)}" lang="en" hreflang="en">English</a></p>')
    if stale_ids:
        notes.append(f'<p class="note stale" id="stale-banner">{esc(ui["stale_banner"])} <a href="{url_of("en", slug)}" lang="en" hreflang="en">English</a></p>')
    top = (f'<a class="skip" href="#main">{esc(ui["skip"])}</a>\n<header class="top">\n'
           f'<a class="brand" href="{url_of(lang, "")}">{esc(site)}</a>\n'
           f'<nav class="langs" aria-label="{esc(ui["language"])}">{sw}</nav>\n</header>\n'
           f'<nav class="site" aria-label="{esc(ui["contents"])}"><ul>\n' + '\n'.join(nav_items) + '\n</ul></nav>'
           + ('\n' + '\n'.join(notes) if notes else ''))
    attr = page.get('attr', 'technocore')
    foot = (f'<footer class="foot">\n<p>{ui["attr_" + attr]}</p>\n'
            f'<p>{esc(ui["checked"].format(tag=CFG["c2pool_tag"], date=CFG["checked_date"]))}</p>\n</footer>')
    return head, top, foot


def all_meta():
    out = {}
    for l in LANGS:
        out[l] = {}
        for p in pages():
            fp = path_of(l, p['slug'])
            if os.path.exists(fp):
                out[l][p['slug']] = article_meta(read(fp))
            else:  # fall back to EN so a partial language still renders its nav
                ep = path_of('en', p['slug'])
                out[l][p['slug']] = article_meta(read(ep)) if os.path.exists(ep) else {'title': p['slug'], 'desc': '', 'nav': p['slug']}
    return out


def cmd_chrome():
    meta = all_meta()
    n = 0
    for l in LANGS:
        for p in pages():
            fp = path_of(l, p['slug'])
            if not os.path.exists(fp):
                continue
            s = read(fp)
            stale = [b[0] for b in blocks(s) if STALE_RE.search(' ' + b[3])]
            head, top, foot = render(l, p, meta, stale)
            s2 = region(region(region(s, 'head', head), 'top', top), 'foot', foot)
            if s2 != s:
                write(fp, s2); n += 1
    write_sitemap()
    print(f'chrome: {n} file(s) rewritten')


def write_sitemap():
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for p in pages():
        for l in LANGS:
            if not os.path.exists(path_of(l, p['slug'])):
                continue
            lines.append(f'<url><loc>{BASE}{url_of(l, p["slug"])}</loc>')
            for l2 in LANGS:
                if os.path.exists(path_of(l2, p['slug'])):
                    lines.append(f'  <xhtml:link rel="alternate" hreflang="{CFG["html_lang"][l2]}" href="{BASE}{url_of(l2, p["slug"])}"/>')
            lines.append('</url>')
    lines.append('</urlset>')
    write(os.path.join(ROOT, 'sitemap.xml'), '\n'.join(lines) + '\n')


# ---------------------------------------------------------------- check / mark / stamp

def en_hashes(slug, rev=None):
    if rev is None:
        src = read(path_of('en', slug))
    else:  # the English text as it was at a git revision (stamp a translation made from it)
        import subprocess
        rel = os.path.relpath(path_of('en', slug), ROOT)
        src = subprocess.run(['git', '-C', ROOT, 'show', f'{rev}:{rel}'], check=True, capture_output=True).stdout.decode('utf-8')
    return {b[0]: h12(b[4]) for b in blocks(src)}


def analyse():
    problems, rows = [], []
    for p in pages():
        slug = p['slug']
        ep = path_of('en', slug)
        if not os.path.exists(ep):
            problems.append(f'missing EN page {slug or "(home)"}'); continue
        eb = blocks(read(ep))
        ids = [b[0] for b in eb]
        if None in ids:
            problems.append(f'en/{slug}: a top-level block has no id')
        if len(set(ids)) != len(ids):
            problems.append(f'en/{slug}: duplicate block ids')
        eh = en_hashes(slug)
        for l in LANGS[1:]:
            fp = path_of(l, slug)
            if not os.path.exists(fp):
                rows.append((slug, l, 'missing page', len(eh), 0, 0, 0)); problems.append(f'{l}/{slug or "(home)"}: page missing'); continue
            tb = blocks(read(fp))
            tid = {b[0]: b for b in tb}
            stale = [i for i, b in tid.items() if i in eh and (SRC_RE.search(' ' + b[3]) or [None, ''])[1] != eh[i]]
            missing = [i for i in eh if i not in tid]
            extra = [i for i in tid if i not in eh]
            unmarked = [i for i in stale if not STALE_RE.search(' ' + tid[i][3])]
            wrongmark = [i for i, b in tid.items() if STALE_RE.search(' ' + b[3]) and i not in stale]
            rows.append((slug, l, 'ok' if not (stale or missing or extra) else 'behind', len(eh), len(stale), len(missing), len(extra)))
            for i in missing: problems.append(f'{l}/{slug}: missing block {i}')
            for i in extra: problems.append(f'{l}/{slug}: extra block {i}')
            for i in unmarked: problems.append(f'{l}/{slug}: stale block {i} not marked (run mark)')
            for i in wrongmark: problems.append(f'{l}/{slug}: block {i} marked stale but current (run mark)')
    return problems, rows


def check_links():
    problems = []
    for dp, _, fs in os.walk(ROOT):
        rel = os.path.relpath(dp, ROOT)
        if rel.startswith('.git') or rel.startswith('tools'):
            continue
        for f in fs:
            if not f.endswith('.html'):
                continue
            fp = os.path.join(dp, f)
            s = read(fp)
            for u in re.findall(r'\s(?:href|src)="(/[^"#?]*)', s):
                t = os.path.join(ROOT, u.lstrip('/'))
                if not (os.path.isfile(t) or os.path.isfile(os.path.join(t, 'index.html'))):
                    problems.append(f'{os.path.relpath(fp, ROOT)}: broken internal link {u}')
            for frag in re.findall(r'\shref="#([^"]+)"', s):
                if not re.search(rf'\sid="{re.escape(frag)}"', s):
                    problems.append(f'{os.path.relpath(fp, ROOT)}: broken anchor #{frag}')
            if re.search(r'\sstyle="', s) or re.search(r'<script(?![^>]*\ssrc=)', s) or re.search(r'\son[a-z]+="', s):
                problems.append(f'{os.path.relpath(fp, ROOT)}: inline style/script/handler (blocked by the CSP)')
    return problems


def write_status(rows):
    out = ['# Translation status', '',
           'Generated by `tools/site.py check`. "behind" means at least one block changed in English since it was translated.', '',
           '| page | lang | state | EN blocks | stale | missing | extra |', '|---|---|---|---|---|---|---|']
    for r in rows:
        out.append(f'| {r[0] or "(home)"} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} |')
    write(os.path.join(ROOT, 'i18n', 'STATUS.md'), '\n'.join(out) + '\n')


def cmd_check():
    problems, rows = analyse()
    problems += check_links()
    write_status(rows)
    for p in problems:
        print(p)
    print(f'check: {len(problems)} problem(s)')
    return 1 if problems else 0


def set_attr(tag_attrs, name, value):
    a = re.sub(rf'\s{name}="[^"]*"', '', tag_attrs)
    return a + (f' {name}="{value}"' if value is not None else '')


def rewrite_blocks(fp, fn):
    s = read(fp)
    for bid, start, end, attrs, frag in reversed(blocks(s)):
        new_attrs = fn(bid, attrs)
        if new_attrs != attrs:
            m = BLOCK_START.match(frag)
            s = s[:start] + f'<{m.group(1)}{new_attrs}>' + frag[m.end():] + s[end:]
    write(fp, s)


def cmd_mark():
    for p in pages():
        eh = en_hashes(p['slug'])
        for l in LANGS[1:]:
            fp = path_of(l, p['slug'])
            if not os.path.exists(fp):
                continue
            def fn(bid, attrs, eh=eh):
                cur = (SRC_RE.search(' ' + attrs) or [None, ''])[1]
                return set_attr(attrs, 'data-stale', '1' if bid in eh and cur != eh[bid] else None)
            rewrite_blocks(fp, fn)
    cmd_chrome()


def cmd_stamp(lang, slug, ids, rev=None):
    slug = '' if slug in ('home', '-') else slug
    eh = en_hashes(slug, rev)
    def fn(bid, attrs):
        if bid in eh and (not ids or bid in ids):
            return set_attr(set_attr(attrs, 'data-src', eh[bid]), 'data-stale', None)
        return attrs
    rewrite_blocks(path_of(lang, slug), fn)
    cmd_chrome()


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        print(__doc__); sys.exit(2)
    if a[0] == 'chrome': cmd_chrome()
    elif a[0] == 'check': sys.exit(cmd_check())
    elif a[0] == 'mark': cmd_mark()
    elif a[0] == 'stamp':
        rev = None
        if '--rev' in a:
            i = a.index('--rev'); rev = a[i + 1]; a = a[:i] + a[i + 2:]
        cmd_stamp(a[1], a[2], a[3:], rev)
    else: print(__doc__); sys.exit(2)
