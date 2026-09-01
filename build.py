#!/usr/bin/env python3
"""Unpack 'Lost Items Community.html' (a self-extracting bundle) into a plain
static site: assets on disk under public/, index.html referencing them.

The bundle is a loader plus three JSON islands: __bundler/manifest (uuid ->
gzipped base64 asset), __bundler/template (the real HTML, with uuids where
src/href go), and __bundler/ext_resources (React + ReactDOM, which the
dc-runtime in support.js needs on window before it will render anything).

Re-run after re-exporting the bundle. Assets no longer referenced by the
template are pruned, so stale files never accumulate under public/.
"""
import base64, gzip, hashlib, json, os, re

BUNDLE = "Lost Items Community.html"
src = open(BUNDLE, encoding="utf-8").read()


def island(kind):
    m = re.search(r'<script type="__bundler/%s">\s*(.*?)\s*</script>' % kind, src, re.S)
    return json.loads(m.group(1))


manifest, template = island("manifest"), island("template")
ext = {e["uuid"]: e["id"] for e in island("ext_resources")}

# uuid -> bytes
blob = {}
for uuid, a in manifest.items():
    b = base64.b64decode(a["data"])
    blob[uuid] = gzip.decompress(b) if a.get("compressed") else b

# The bundle names every asset by uuid. Restore the original image filenames by
# content hash so the tree stays readable. (The six decorative SVGs in the
# source folder were byte-identical; 100_316.svg is the canonical one.)
IMG_NAMES = {
    "c79be1f43b455e9a4065d216780d98a2791e0392": "100_316.svg",
    "5ad81437611a53ba4639cb03dd9c0931b57cd1a6": "113_115.png",
    "a78a838d2a6574f4d3288059fe3545d68c3c6709": "113_125.png",
    "d072e9a9c10f9794f6ba3d559733847d757c94af": "113_135.png",
    "fef558a6f1858088846f61d9c27bb47476d59fac": "HomePage1.webp",
    "7e9b23dd78b6a556734f65d363b83225093b52b0": "feature-report-found.webp",
    "360b7da8a00a3f92d78d1bd5344ca58803a465bb": "feature-search-system.webp",
    "cd83852de3e5e9bc2b1a222c17ce13a181cae865": "feature-success-stories.webp",
    "0e5db614ccf5fa1f3115d7f844a1736640f9fc93": "hero-boy-with-dog.webp",
    "d2338794e8275e6a61d4281e788c8d5c5c9115c6": "illustration-exchange-item.webp",
    "902c3efbceae85f0f69fc319c9a86dbfd3bc40c9": "illustration-treasure-chest.webp",
    "e59c20c17628a4a2cbb5c6367d61857a50409d98": "logo.png",
}

# Font names come from the @font-face block that references each file. One file
# serves several weights when the family is variable (Public Sans ships one
# variable woff2 per unicode subset covering 400-800) — those must NOT be named
# after a single weight, or the filename lies about what it contains.
faces = re.findall(
    r"font-family: '([^']+)';\s*font-style: normal;\s*font-weight: (\d+);"
    r"\s*font-display: swap;\s*src: url\(\"([0-9a-f-]{36})\"\)", template)
weights, family = {}, {}
for fam, w, uuid in faces:
    weights.setdefault(uuid, set()).add(w)
    family[uuid] = fam

fontnames, seen = {}, {}
for uuid in family:
    slug = re.sub(r"\W+", "-", family[uuid]).lower()
    ws = weights[uuid]
    base = slug if len(ws) > 1 else f"{slug}-{ws.pop()}"
    seen[base] = seen.get(base, 0) + 1
    # the same family+weight repeats once per unicode subset
    fontnames[uuid] = base if seen[base] == 1 else f"{base}-{seen[base]}"

EXT = {"image/svg+xml": ".svg", "image/png": ".png", "image/webp": ".webp"}
DIRS = ("public/images", "public/fonts", "public/js")
for d in DIRS:
    os.makedirs(d, exist_ok=True)

paths = {}
for uuid, a in manifest.items():
    mime, data = a["mime"], blob[uuid]
    if uuid in ext:
        name = os.path.basename(ext[uuid]).replace(".production.min", "").replace(".prod.min", "")
        path = f"public/js/{name}"
    elif mime.startswith("font/"):
        path = f"public/fonts/{fontnames.get(uuid, uuid[:8])}.woff2"
    elif mime.startswith("image/"):
        path = "public/images/" + IMG_NAMES.get(hashlib.sha1(data).hexdigest(),
                                                uuid[:8] + EXT[mime])
    else:
        path = "public/js/support.js"          # the dc-runtime
    open(path, "wb").write(data)
    paths[uuid] = "/" + path

out = template
for uuid, p in paths.items():
    out = out.replace(uuid, p)

# React must be on window before support.js runs (dc-runtime reads window.React).
react = "".join(f'<script src="{paths[u]}"></script>\n'
                for u in sorted(ext, key=lambda u: "dom" in ext[u]))
out = out.replace('<script src="/public/js/support.js"></script>',
                  react + '<script src="/public/js/support.js"></script>')

HEAD = """<title>Lost Items Community</title>
<meta name="description" content="Report found items, search the registry, and reunite people with their lost belongings.">
<meta name="theme-color" content="#16181F">
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="192x192" href="/public/icons/icon-192.png">
<link rel="apple-touch-icon" href="/public/icons/icon-180.png">
<meta name="apple-mobile-web-app-title" content="Lost Items">
<meta name="mobile-web-app-capable" content="yes">
<link rel="manifest" href="/manifest.webmanifest">
<style>.store-btn{min-width:190px;justify-content:center}</style>
"""
out = out.replace('<meta name="viewport" content="width=device-width, initial-scale=1">',
                  '<meta name="viewport" content="width=device-width, initial-scale=1">\n' + HEAD, 1)

# ── Design tweak: store buttons ──────────────────────────────────────────────
# The two badges were a mismatched pair: widths came out 177px vs 166px purely
# because "DOWNLOAD ON THE" is longer than "GET IT ON", and play_arrow (a thin
# triangle) reads optically smaller than phone_iphone at the same 21px. Tag both
# buttons so CSS can equalise them, and size the triangle up to match.
STORE_BTNS = ('<button style="{{ btnAppStore }}"', '<button style="{{ btnPlay }}"')
for b in STORE_BTNS:
    assert b in out, f"store button markup changed upstream: {b}"
    out = out.replace(b, b.replace('<button ', '<button class="store-btn" '))

PLAY_ICON = '<span class="ms" style="font-size:21px">play_arrow</span>'
assert PLAY_ICON in out, "play_arrow icon markup changed upstream"
out = out.replace(PLAY_ICON, PLAY_ICON.replace('21px', '26px'))


# ── Design tweak: header pill shadow ─────────────────────────────────────────
# The nav pill's lift shadow is "0 18px 40px -28px": an 18px downward offset
# with a -28px spread, which shrinks the shadow well inside the element before
# pushing it down — so it only ever escaped past the bottom edge. Keep that lift
# and add an ambient pair (hairline ring + zero-offset blur) so the pill reads as
# floating on all four sides.
OLD_PILL_SHADOW = "box-shadow:0 1px 2px rgba(22,24,31,.06),0 18px 40px -28px rgba(22,24,31,.5)"
NEW_PILL_SHADOW = ("box-shadow:0 0 0 1px rgba(22,24,31,.05),"
                   "0 2px 8px rgba(22,24,31,.08),"
                   "0 10px 30px rgba(22,24,31,.13),"
                   "0 18px 40px -28px rgba(22,24,31,.5)")
assert OLD_PILL_SHADOW in out, "header pill shadow changed upstream"
out = out.replace(OLD_PILL_SHADOW, NEW_PILL_SHADOW)


open("index.html", "w", encoding="utf-8").write(out)

# Prune anything under public/ that this build did not write and index.html does
# not reference, so a re-export that drops an asset does not leave it orphaned.
kept = set(paths.values())
pruned = []
for d in DIRS:
    for f in sorted(os.listdir(d)):
        p = "/" + d + "/" + f
        if p not in kept and p not in out:
            os.remove(d + "/" + f)
            pruned.append(p)

print(f"wrote index.html ({len(out)} bytes), {len(paths)} assets")
if pruned:
    print("pruned: " + ", ".join(pruned))
assert "__bundler" not in out and not re.search(r"[0-9a-f]{8}-[0-9a-f]{4}-", out), "unresolved bundle refs"
assert "unpkg.com" not in out, "external CDN reference left in"
for d in DIRS:
    assert os.listdir(d), f"{d} is empty"
print("ok: no unresolved refs, no external CDN")
