"""Translation layer: turns the built Italian pages into other languages.

How it works
1. `extract()` reads the Italian pages in docs/ and collects every translatable piece once:
   block texts (with their inline markup), attributes people see or hear (alt, title, aria-label,
   placeholder, meta descriptions), user-facing strings inside scripts and JSON data.
2. Each language has a dictionary in src/i18n/<code>.json: {Italian source: translation}.
3. `render(code)` writes docs/<code>/*.html from the Italian pages using that dictionary,
   fixing paths, language tags, canonical URLs and the language menu.

Adding a language: translate src/i18n/segments.json into src/i18n/<code>.json, set the language to
True in LANGS (src/common.py), rebuild. Missing entries fall back to Italian and are listed.
"""
import json, os, re, glob, html as htmlmod
from bs4 import BeautifulSoup, NavigableString, Comment, Tag

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HERE, "..", "docs")
I18N = os.path.join(HERE, "i18n")
BASE = "https://www.sunlines.it"

INLINE = {"a", "strong", "em", "b", "i", "span", "small", "br", "code", "abbr", "mark", "sup", "sub", "time", "svg", "output", "u"}
SKIP = {"script", "style", "svg", "noscript", "template"}
ATTRS = ("alt", "title", "aria-label", "placeholder", "data-subject")
META = {"description", "og:title", "og:description", "twitter:title", "twitter:description"}
HIDDEN_VALUES = {"_subject", "_autoresponse", "Modulo"}
# JSON keys never translated (codes, ids, urls, colours)
JSON_KEEP = re.compile(r"^(#[0-9A-Fa-f]{3,8}|https?://.*|[a-z0-9\-]+\.html.*|[a-z0-9_\-]{1,20}|[A-Z0-9_\-]{1,12}|\d[\d.,: ]*)$")
ITALIAN_HINT = re.compile(r"[A-Za-zÀ-ÿ]{2,}")
SVG_RX = re.compile(r"<svg\b.*?</svg>", re.S)


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def _is_leaf_block(el):
    """Element whose content is text plus inline tags only, and has some text."""
    if not isinstance(el, Tag) or el.name in SKIP or el.name in INLINE:
        return False
    has_text = False
    for d in el.descendants:
        if isinstance(d, Tag):
            if d.name not in INLINE and d.name not in ("path", "circle", "rect", "g", "line", "polyline", "polygon", "text", "title", "desc", "defs", "pattern"):
                return False
        elif isinstance(d, NavigableString) and not isinstance(d, Comment) and d.strip():
            has_text = True
    return has_text


def _inner(el):
    return "".join(str(c) for c in el.contents)


def _mask_svg(s):
    svgs = []
    def rep(m):
        svgs.append(m.group(0)); return f"⟦{len(svgs)-1}⟧"
    return SVG_RX.sub(rep, s), svgs


def _unmask(s, svgs):
    for i, sv in enumerate(svgs):
        s = s.replace(f"⟦{i}⟧", sv)
    return s


def _wanted(text):
    t = norm(BeautifulSoup(text, "lxml").get_text()) if "<" in text else norm(text)
    return bool(ITALIAN_HINT.search(t))


def _js_literals(code):
    """User-facing single-quoted strings in inline scripts."""
    out = []
    for m in re.finditer(r"'((?:[^'\\\n]|\\.)*)'", code):
        s = m.group(1)
        if len(s) < 3 or not re.search(r"[a-zà-ù]{3,}", s):
            continue
        if re.search(r"^[\w\-\[\]=\"\.#:\(\) ,>~*^$|]+$", s) and " " not in s.strip():
            continue  # selectors, identifiers
        if re.match(r"^(input|button|select|textarea|\.|#|\[|a\[|svg|li\[|figure|section|\(prefers)", s):
            continue
        if any(k in s for k in ("function", "querySelector", "=>", "addEventListener")):
            continue
        if not (" " in s or "<" in s or re.search(r"[àèéìòù…’]", s)):
            continue
        out.append(s)
    return out


def _json_strings(obj, acc):
    if isinstance(obj, dict):
        for v in obj.values(): _json_strings(v, acc)
    elif isinstance(obj, list):
        for v in obj: _json_strings(v, acc)
    elif isinstance(obj, str):
        if not JSON_KEEP.match(obj) and ITALIAN_HINT.search(obj) and " " in obj:
            acc.append(obj)


def _walk_blocks(soup, fn):
    """Call fn(element) for leaf blocks, then fn(textnode) for leftover text nodes."""
    done = set()
    body = soup.body or soup
    for el in body.find_all(True):
        if any(id(p) in done for p in el.parents):
            continue
        if el.name in SKIP or any(p.name in SKIP for p in el.parents if isinstance(p, Tag)):
            continue
        if _is_leaf_block(el):
            done.add(id(el)); fn(el)
    for t in body.find_all(string=True):
        if isinstance(t, Comment) or not t.strip():
            continue
        if any(id(p) in done for p in t.parents) or any(isinstance(p, Tag) and p.name in SKIP for p in t.parents):
            continue
        fn(t)


def extract():
    segs = {}
    def add(s, kind, page):
        s = s.strip()
        if s and _wanted(s):
            segs.setdefault(s, {"kind": kind, "pages": set()})["pages"].add(page)
    for f in sorted(glob.glob(os.path.join(DOCS, "*.html"))):
        page = os.path.basename(f)
        soup = BeautifulSoup(open(f, encoding="utf-8").read(), "lxml")
        if soup.title and soup.title.string:
            add(soup.title.string, "title", page)
        for m in soup.find_all("meta"):
            k = m.get("name") or m.get("property")
            if k in META and m.get("content"):
                add(m["content"], "meta", page)
        def onb(node):
            if isinstance(node, Tag):
                masked, _ = _mask_svg(_inner(node)); add(norm(masked), "html", page)
            else:
                add(norm(str(node)), "text", page)
        _walk_blocks(soup, onb)
        for el in soup.find_all(True):
            if el.name in ("svg",) or any(isinstance(p, Tag) and p.name == "svg" for p in el.parents):
                if el.name in ("title", "desc", "text") and el.string:
                    add(norm(el.string), "svgtext", page)
            for a in ATTRS:
                if el.has_attr(a):
                    add(el[a], "attr", page)
            if el.name == "input" and el.get("type") == "hidden" and el.get("name") in HIDDEN_VALUES and el.get("value"):
                add(el["value"], "attr", page)
        for sc in soup.find_all("script"):
            code = sc.string or ""
            if sc.get("type") in ("application/json", "application/ld+json"):
                acc = []
                try: _json_strings(json.loads(code), acc)
                except Exception: pass
                for s in acc: add(s, "json", page)
            else:
                for s in _js_literals(code): add(s, "js", page)
    return segs


def write_segments():
    segs = extract()
    os.makedirs(I18N, exist_ok=True)
    data = [{"it": k, "kind": v["kind"], "pages": sorted(v["pages"])} for k, v in segs.items()]
    json.dump(data, open(os.path.join(I18N, "segments.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return data


# ------------------------------------------------------------------ render
def _lang_list(code, file, langs, prefix_to_root):
    items = []
    for c, name, ok in langs:
        if c == code:
            items.append(f'<li><a href="{file}" lang="{c}" hreflang="{c}" aria-current="true">{name}' + "{CHECK}" + '</a></li>')
        elif ok:
            href = (prefix_to_root + file) if c == "it" else (prefix_to_root + f"{c}/" + file)
            items.append(f'<li><a href="{href}" lang="{c}" hreflang="{c}">{name}</a></li>')
        else:
            items.append(f'<li><span lang="{c}" aria-disabled="true">{name}<small>in arrivo</small></span></li>')
    return "".join(items)


from urllib.parse import quote
WA_EN = {
    "ho una domanda:": "Hello Sun Lines, I have a question: ",
}
LANG_UI = {
    "en": {"wa": {
        "vorrei%20un%20preventivo%20per%20un%20autobus": "https://wa.me/393463206740?text=" + quote("Hello Sun Lines, I would like a quote for a coach with driver.\nNumber of people: \nDate: \nFrom: \nTo: \nNotes: "),
        "vorrei%20un%20preventivo%20per%20un%27auto": "https://wa.me/393463206740?text=" + quote("Hello Sun Lines, I would like a quote for a car with driver.\nPassengers: \nDate and time: \nPick-up: \nDestination: "),
        "informazioni%20sul%20parcheggio": "https://wa.me/393463206740?text=" + quote("Hello Sun Lines, I would like information about parking.\nFrom: \nTo: \nVehicle (car / camper): "),
        "domanda%20sull%27Airbus": "https://wa.me/393463206740?text=" + quote("Hello Sun Lines, I have a question about the Airbus Olbia–Sassari–Alghero (line 90): "),
        "ho%20una%20domanda%3A": "https://wa.me/393463206740?text=" + quote("Hello Sun Lines, I have a question: "),
    },"menu_label": "Language: English. Change language", "soon": "coming soon", "locale": "en_GB", "bigo": "en",
           "drawer": "Lingua / Language"},
}


def render(code, langs):
    tr = json.load(open(os.path.join(I18N, f"{code}.json"), encoding="utf-8"))
    ui = LANG_UI[code]
    out_dir = os.path.join(DOCS, code)
    os.makedirs(out_dir, exist_ok=True)
    missing = {}

    def T(s, page):
        k = s.strip()
        if not k or not _wanted(k):
            return s
        if k in tr and tr[k]:
            return tr[k]
        missing.setdefault(k, set()).add(page)
        return s

    for f in sorted(glob.glob(os.path.join(DOCS, "*.html"))):
        file = os.path.basename(f)
        src = open(f, encoding="utf-8").read()
        soup = BeautifulSoup(src, "lxml")
        if soup.title and soup.title.string:
            soup.title.string = T(soup.title.string, file)
        for m in soup.find_all("meta"):
            k = m.get("name") or m.get("property")
            if k in META and m.get("content"):
                m["content"] = T(m["content"], file)
            if m.get("property") == "og:locale":
                m["content"] = ui["locale"]
            if m.get("property") == "og:url" and m.get("content", "").startswith(BASE):
                m["content"] = BASE + f"/{code}" + m["content"][len(BASE):]

        def onb(node):
            if isinstance(node, Tag):
                masked, svgs = _mask_svg(_inner(node))
                key = norm(masked)
                t = T(key, file)
                if t is not key and t != key:
                    node.clear()
                    frag = BeautifulSoup(_unmask(t, svgs), "html.parser")
                    for c in list(frag.contents):
                        node.append(c)
            else:
                key = norm(str(node))
                t = T(key, file)
                if t != key:
                    lead = " " if str(node)[:1].isspace() else ""
                    trail = " " if str(node)[-1:].isspace() else ""
                    node.replace_with(NavigableString(lead + t + trail))
        _walk_blocks(soup, onb)

        for el in soup.find_all(True):
            if el.name in ("title", "desc", "text") and any(isinstance(p, Tag) and p.name == "svg" for p in el.parents) and el.string:
                el.string = T(norm(el.string), file)
            for a in ATTRS:
                if el.has_attr(a):
                    el[a] = T(el[a], file)
            if el.name == "input" and el.get("type") == "hidden" and el.get("name") in HIDDEN_VALUES and el.get("value"):
                el["value"] = T(el["value"], file)
            # relative asset paths move one level up
            for a in ("src", "href"):
                v = el.get(a)
                if not v or v.startswith(("http", "mailto:", "tel:", "#", "data:", "/")):
                    continue
                if a == "href" and el.name == "a" and v.split("#")[0].endswith(".html"):
                    continue  # page links stay inside /<code>/
                if el.name == "a" and v.endswith(".html"):
                    continue
                el[a] = "../" + v
            if el.name == "link" and el.get("rel") == ["canonical"] and el.get("href", "").startswith(BASE):
                el["href"] = BASE + f"/{code}" + el["href"][len(BASE):]
            if el.name == "a" and el.get("href", "").startswith("https://wa.me/") and "text=" in el.get("href", ""):
                for k, v in ui.get("wa", {}).items():
                    if k in el["href"]:
                        el["href"] = v; break
            if el.name == "a" and el.get("href", "").startswith("https://sites.bigosolutions.it/sunlines/it"):
                el["href"] = el["href"].replace("/sunlines/it", "/sunlines/" + ui["bigo"])

        for sc in soup.find_all("script"):
            code_s = sc.string or ""
            if sc.get("type") in ("application/json", "application/ld+json"):
                try:
                    obj = json.loads(code_s)
                except Exception:
                    continue
                def tj(o):
                    if isinstance(o, dict): return {k: (code if (k == "inLanguage" and v == "it") else tj(v)) for k, v in o.items()}
                    if isinstance(o, list): return [tj(v) for v in o]
                    if isinstance(o, str) and not JSON_KEEP.match(o) and " " in o: return T(o, file)
                    return o
                sc.string = json.dumps(tj(obj), ensure_ascii=False)
            elif code_s:
                new = code_s
                for lit in sorted(set(_js_literals(code_s)), key=len, reverse=True):
                    t = T(lit, file)
                    if t != lit:
                        t = lit[:len(lit) - len(lit.lstrip())] + t.strip() + lit[len(lit.rstrip()):]
                        new = new.replace("'" + lit + "'", "'" + t.replace("\\", "\\\\").replace("'", "\\'") + "'")
                sc.string = new
        for st in soup.find_all("style"):
            if st.string:
                st.string = st.string.replace("url(fonts/", "url(../fonts/")

        out = str(soup)
        out = out.replace('<html lang="it">', f'<html lang="{code}">', 1)
        # language menus (header + drawer)
        check = '<svg class="i" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l4 4 10-10"/></svg>'
        new_list = _lang_list(code, file, langs, "../").replace("{CHECK}", check).replace("in arrivo", ui["soon"])
        out = re.sub(r'(<ul class="lang-list">).*?(</ul>)', lambda m: m.group(1) + new_list + m.group(2), out, flags=re.S)
        out = re.sub(r'(<summary aria-label=")[^"]*(">)', lambda m: m.group(1) + ui["menu_label"] + m.group(2), out, count=1)
        out = re.sub(r'(<summary aria-label="[^"]*">.*?<span>)IT(</span>)', lambda m: m.group(1) + code.upper() + m.group(2), out, count=1, flags=re.S)
        open(os.path.join(out_dir, file), "w", encoding="utf-8").write(out)
    return missing


def fix_italian_lang_menu(langs):
    """Point the Italian pages' language menu at the same page in each language."""
    for f in glob.glob(os.path.join(DOCS, "*.html")):
        file = os.path.basename(f)
        s = open(f, encoding="utf-8").read()
        for c, _, ok in langs:
            if c != "it" and ok:
                s = s.replace(f'href="{c}/index.html" lang="{c}"', f'href="{c}/{file}" lang="{c}"')
        s = s.replace('href="index.html" lang="it" hreflang="it" aria-current="true"', f'href="{file}" lang="it" hreflang="it" aria-current="true"')
        open(f, "w", encoding="utf-8").write(s)


if __name__ == "__main__":
    d = write_segments()
    from collections import Counter
    print(len(d), "segments", Counter(x["kind"] for x in d))
