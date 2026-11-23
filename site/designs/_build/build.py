#!/usr/bin/env python3
"""Five designs of dns.tool.sovereignweb.site's home page. design.c@SovereignWebsite.dinis, round 1.
Same words and the same working checker: each design keeps the form's ids (#check, #name, #type, #summary,
#results) and loads the site's own /assets/dns.js. Usage: build.py <site dir>"""
import json, os, sys, html

SITE = sys.argv[1]
OUT = os.path.join(SITE, "designs")
HOST = "https://dns.tool.sovereignweb.site"
e = html.escape
REG = json.load(open(os.path.join(SITE, "data", "regions.json")))["regions"]
AREAS = {}
for r in REG:
    AREAS.setdefault(r["area"], []).append(r)

H1 = "DNS, around the world"
MARK = "dns.tool.sovereignweb.site"
INTRO = ("Type a name and a record type. Your browser asks three public resolvers, then asks Google Public DNS as if "
         "from 26 countries. Nothing goes through this site: no server, no cookies, no ads, no tracking.")
HOW = [
    'The three resolvers (<a href="https://developers.google.com/speed/public-dns/docs/doh/json">Google Public DNS</a>, '
    '<a href="https://developers.cloudflare.com/1.1.1.1/encryption/dns-over-https/make-api-requests/dns-json/">Cloudflare</a> '
    'and AliDNS) answer DNS over HTTPS and allow calls from a web page. Each answers from its server nearest to you.',
    'For the countries, the page sends Google Public DNS a client subnet: a /24 inside an address block that the '
    'country’s registry allocated to it, as listed by <a href="https://stat.ripe.net/">RIPEstat</a> '
    '(<a href="/data/regions.json">the list</a>). A name served by a CDN answers as it would for a visitor in that '
    'country. A name that does not answer by location gives the same answer everywhere.',
    'So this shows what each resolver holds and what each country is told. It is not yet a lookup from each '
    'country’s own resolvers: that needs checkers placed in those countries, a later step.',
    'Who owns a name: <a href="https://whois.tool.sovereignweb.site/">whois.tool.sovereignweb.site</a>.',
]
SENT = ("When you press Check, your browser sends the name to dns.google, cloudflare-dns.com and dns.alidns.com, "
        "and nothing else; this page names only those hosts in its security policy.")
TYPES = ["A", "AAAA", "CNAME", "MX", "NS", "TXT", "SOA", "CAA"]
DESIGNS = [
    (1, "Zone File", "The page written as a DNS zone file: comments for the words, the form as one record line."),
    (2, "Departures", "A departures board of the 26 countries and three resolvers, dark first, the answer as the arrival."),
    (3, "The Path", "The journey of one question, drawn step by step from your browser to the resolvers and back."),
    (4, "Atlas", "An atlas: the countries by continent, and the check as the legend that colours them in."),
    (5, "Brief", "Everything on one plain page, for reading fast or printing."),
]
FAMILY = [("https://sovereignwebsite.ai/", "Sovereign Website"), ("https://sovereignwebsite.org/", "Principles"),
          ("https://sovereignwebsite.site/", "Hosted"), ("https://hub.sovereignweb.site/", "Hub"),
          ("https://agents.sovereignweb.site/", "Agents"), ("https://vault.sovereignwebsite.site/", "Vault"),
          ("https://agenticcells.ai/", "AgentiCCells"), ("https://riskmandate.ai/", "RiskMandate"),
          ("https://newsroom.sgit.ai/", "Newsroom")]
CSP = ("default-src 'self'; connect-src 'self' https://dns.google https://cloudflare-dns.com https://dns.alidns.com; "
       "img-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self'; base-uri 'none'; form-action 'self'")

BASE = """
*{box-sizing:border-box}
html{color-scheme:light dark;-webkit-text-size-adjust:100%}
body{margin:0;font:1.0625rem/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--fg);overflow-wrap:break-word}
a{color:var(--link)}
:focus-visible{outline:3px solid var(--focus);outline-offset:2px}
.skip{position:absolute;left:-999px;top:.5rem;z-index:99;background:var(--bg);color:var(--fg);padding:.5rem .9rem;border:2px solid var(--focus)}
.skip:focus{left:1rem}
main *{min-width:0}
.chrome{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;justify-content:flex-end;position:relative;z-index:5;padding-top:.5rem}
.chrome details{position:relative}
.chrome summary{cursor:pointer;list-style:none;min-height:44px;display:inline-flex;align-items:center;padding:.35rem .8rem;border:1px solid var(--ctl);border-radius:999px;font-size:.9rem;background:var(--bg);color:var(--fg)}
.chrome summary::-webkit-details-marker{display:none}
.chrome summary::after{content:"";width:.45rem;height:.45rem;margin-left:.5rem;border-right:2px solid currentColor;border-bottom:2px solid currentColor;transform:rotate(45deg) translateY(-2px)}
.chrome details[open] summary::after{transform:rotate(-135deg)}
.chrome ul{position:absolute;right:0;top:calc(100% + .35rem);margin:0;padding:.4rem;list-style:none;min-width:15rem;max-width:calc(100vw - 2rem);background:var(--bg);color:var(--fg);border:1px solid var(--ctl);border-radius:.6rem;box-shadow:0 .6rem 1.6rem rgba(0,0,0,.25)}
.chrome li a{display:block;padding:.55rem .7rem;border-radius:.4rem;color:var(--fg);text-decoration:none;font-size:.95rem}
.chrome li a:hover,.chrome li a:focus-visible{background:var(--hover)}
.chrome li a[aria-current]{font-weight:700;text-decoration:underline}
.chrome .gap{border-top:1px solid var(--ctl);margin-top:.3rem;padding-top:.3rem}
.chrome small{display:block;font-size:.85rem;color:var(--muted);font-weight:400}
.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.check{display:grid;grid-template-columns:1fr auto auto;gap:.4rem .6rem;align-items:end;margin:1.25rem 0 .5rem}
.check label{font-size:.9rem;color:var(--muted);grid-row:1}
.check label[for=type]{grid-column:2}
.check input,.check select,.check button{font:inherit;font-size:1rem;padding:.55rem .7rem;border:1px solid var(--ctl);border-radius:6px;background:var(--field);color:var(--fg);min-height:44px}
.check input{grid-column:1;grid-row:2}.check select{grid-column:2;grid-row:2}
.check button{grid-column:3;grid-row:2;background:var(--accent);color:var(--on-accent);border-color:var(--accent);font-weight:700;cursor:pointer}
@media (max-width:30rem){.check{grid-template-columns:1fr auto}.check button{grid-column:1/-1;grid-row:3}}
.summary{font-weight:700;min-height:1.6em}
.scroll{overflow-x:auto;margin:1rem 0}
#results table{border-collapse:collapse;width:100%;font-size:.95rem}
#results caption{text-align:left;font-weight:700;padding:.4rem 0}
#results th,#results td{text-align:left;vertical-align:top;padding:.45rem .6rem;border-bottom:1px solid var(--line)}
#results thead th{color:var(--muted);font-size:.9rem}
#results th .sub{display:block;font-weight:400;color:var(--muted);font-size:.875rem}
#results tr.group th{background:var(--hover);font-size:.875rem;letter-spacing:.06em;text-transform:uppercase}
#results td.vals{white-space:pre-wrap;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;overflow-wrap:anywhere}
#results td.ok{color:var(--ok);font-weight:700;white-space:nowrap}
#results td.bad{color:var(--bad);font-weight:700}
#results td.num{text-align:right;font-variant-numeric:tabular-nums}
.sent{font-size:.9rem;color:var(--muted)}
footer{padding:2rem 0 3rem;font-size:.95rem}
footer nav{display:flex;flex-wrap:wrap;gap:.25rem 1.25rem}
footer nav a{min-height:44px;display:inline-flex;align-items:center}
@media print{.chrome,.skip,.check{display:none}}
"""


def head(n, css):
    name, idea = (DESIGNS[n - 1][1], DESIGNS[n - 1][2]) if n else ("", "")
    title = f"{name}, design {n} of DNS" if n else "Five designs, DNS"
    desc = (f"Design {n} of dns.tool.sovereignweb.site, {name}: {idea}" if n else
            "Five designs of dns.tool.sovereignweb.site, the same checker in five ideas, side by side.")
    url = f"{HOST}/designs/{n}/" if n else f"{HOST}/designs/"
    img = f"{HOST}/assets/share/card-1200x630.jpg"
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="DNS">
<meta property="og:locale" content="en_GB">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="DNS">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{img}">
<link rel="canonical" href="{url}">
<style>{BASE}{css}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def chrome(n):
    d = "".join(f'<li><a href="/designs/{i}/"{" aria-current=\"page\"" if i == n else ""}>{i}. {nm}<small>{idea}</small></a></li>' for i, nm, idea in DESIGNS)
    fam = "".join(f'<li><a href="{u}">{t}</a></li>' for u, t in FAMILY)
    return f"""<nav class="chrome" aria-label="Designs and the Sovereign Website family">
<details><summary>Choose a design</summary><ul>{d}<li class="gap"><a href="/designs/">All five, side by side</a></li><li><a href="/">The site as it is now</a></li></ul></details>
<details><summary>Sovereign Website</summary><ul><li><a href="/start/">Start here</a></li><li><a href="/agents/">Use with your AI</a></li><li><a href="/admin/">How this site was made</a></li><li class="gap"><a href="/policy/">How this site is governed</a></li>{fam}</ul></details>
</nav>"""


def own(cls="own"):
    return f'<nav class="{cls}" aria-label="This site"><a href="#check">Check a name</a><a href="#how">How it works</a><a href="/start/">Start here</a><a href="/agents/">Use with your AI</a></nav>'


def form(btn="Check"):
    opts = "".join(f"<option>{t}</option>" for t in TYPES)
    return f"""<form id="check" class="check">
<label for="name">Domain name</label>
<input id="name" name="name" type="text" inputmode="url" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="sovereignweb.site" required>
<label for="type">Record type</label>
<select id="type" name="type">{opts}</select>
<button type="submit">{btn}</button>
</form>
<p class="sent">{SENT}</p>
<p id="summary" class="summary" role="status" aria-live="polite"></p>
<div id="results"></div>"""


def how(cls="how"):
    return f'<ul class="{cls}">' + "".join(f"<li>{x}</li>" for x in HOW) + "</ul>"


def footer():
    return f"""<footer>
<nav aria-label="About this site"><a href="/start/">Start here</a> <a href="/agents/">Use with your AI</a> <a href="/admin/">How this site was made</a> <a href="/policy/">How this site is governed</a></nav>
<p>A sovereign website, made with the <a href="https://sovereignwebsite.org/">open pattern</a>. Source: <a href="https://github.com/SovereignWebsite/Site__Tool__DNS">github.com/SovereignWebsite/Site__Tool__DNS</a>.</p>
</footer>
<script src="/assets/dns.js" defer></script>
</body>
</html>
"""


def countries(cls="countries", tag="h3"):
    out = []
    for area, rs in AREAS.items():
        items = "".join(f'<li><span class="cc">{r["cc"]}</span> {e(r["name"])}</li>' for r in rs)
        out.append(f'<div class="area"><{tag}>{e(area)}</{tag}><ul>{items}</ul></div>')
    return f'<div class="{cls}">' + "".join(out) + "</div>"


# ---------------------------------------------------------------- 1. Zone File
CSS1 = """
:root{--bg:#fbfaf6;--fg:#1c1c1a;--muted:#55544e;--link:#1f5c45;--focus:#1f5c45;--ctl:#7a786f;--hover:#efede6;--field:#ffffff;--accent:#1f5c45;--on-accent:#ffffff;--line:#dedbd1;--ok:#1f5c45;--bad:#a13a2a;--cm:#6a5f3c}
@media (prefers-color-scheme:dark){:root{--bg:#121311;--fg:#ecebe6;--muted:#b3b1a8;--link:#8fd3b0;--focus:#8fd3b0;--ctl:#85837a;--hover:#1f201d;--field:#1a1b18;--accent:#8fd3b0;--on-accent:#0b1410;--line:#30312c;--ok:#8fd3b0;--bad:#ff9b8a;--cm:#d8c88f}}
body{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:1rem}
.wrap{max-width:62rem;margin:0 auto;padding:0 1rem}
.mast{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:.5rem 1rem;padding:.5rem 0;border-bottom:1px dashed var(--ctl)}
.brand{font-weight:800;color:var(--fg);text-decoration:none;min-height:44px;display:inline-flex;align-items:center}
.brand::before{content:"$ORIGIN ";color:var(--muted);font-weight:400;margin-right:.4rem}
.own{display:flex;flex-wrap:wrap;gap:.25rem 1rem;font-size:.95rem}.own a{color:var(--fg);min-height:44px;display:inline-flex;align-items:center}
.zone{padding:clamp(1.5rem,5vw,3rem) 0}
.cm{color:var(--cm);margin:.2rem 0}
.cm::before{content:"; ";}
h1{font-size:clamp(1.9rem,6vw,3.2rem);line-height:1.1;margin:.6rem 0 1rem;font-weight:800}
.lede{max-width:44rem}
.rec{border:1px solid var(--ctl);border-radius:.4rem;padding:1rem;margin:1.5rem 0;background:var(--field)}
.rec .check{margin-top:0}
h2{font-size:1.45rem;margin:2.5rem 0 .5rem}
h2::before{content:";; ";color:var(--muted)}
.how{list-style:none;padding:0;margin:0}
.how li{padding:.5rem 0 .5rem 1.5rem;position:relative;border-bottom:1px dashed var(--line);max-width:46rem}
.how li::before{content:";";position:absolute;left:0;color:var(--cm)}
footer{border-top:1px dashed var(--ctl)}
"""


def d1():
    return head(1, CSS1) + f"""<div class="wrap">{chrome(1)}
<header class="mast"><a class="brand" href="/">DNS</a>{own()}</header>
<main id="main"><div class="zone">
<p class="cm">{MARK}</p>
<h1>{H1}</h1>
<p class="lede">{INTRO}</p>
<div class="rec">{form()}</div>
<h2 id="how">How it works</h2>
{how()}
</div></main>
""" + footer().replace("</body>", "</div></body>")


# ---------------------------------------------------------------- 2. Departures (dark first)
CSS2 = """
:root{--bg:#0b0c0e;--fg:#f3f3f0;--muted:#b9b8b1;--link:#ffd166;--focus:#ffd166;--ctl:#8a8981;--hover:#1b1c20;--field:#16171b;--accent:#ffd166;--on-accent:#141006;--line:#2b2c31;--ok:#7fe0a8;--bad:#ff9b8a;--board:#111216;--flap:#1c1d22}
@media (prefers-color-scheme:light){:root{--bg:#f1f1ee;--fg:#121214;--muted:#4c4c48;--link:#6b4a00;--focus:#6b4a00;--ctl:#76766f;--hover:#e2e2dd;--field:#ffffff;--accent:#121214;--on-accent:#ffd166;--line:#cfcfc8;--ok:#1d6b45;--bad:#a13a2a;--board:#ffffff;--flap:#f1f1ee}}
.wrap{max-width:80rem;margin:0 auto;padding:0 1rem}
.mast{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:.5rem 1rem;padding:.5rem 0}
.brand{font:800 1.2rem/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.2em;color:var(--fg);text-decoration:none;min-height:44px;display:inline-flex;align-items:center}
.own{display:flex;flex-wrap:wrap;gap:.25rem 1rem;font-size:.95rem}.own a{color:var(--fg);min-height:44px;display:inline-flex;align-items:center}
.top{display:grid;gap:1.5rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,24rem),1fr));padding:clamp(1.5rem,4vw,2.5rem) 0;align-items:end}
.k{font:700 .85rem ui-monospace,Menlo,Consolas,monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin:0}
h1{font-size:clamp(2.1rem,6vw,3.8rem);line-height:1.02;margin:.4rem 0 1rem;letter-spacing:-.02em}
.gate{background:var(--board);border:1px solid var(--line);border-radius:.8rem;padding:1rem 1.2rem}
.gate .check{margin-top:.25rem}
.board{background:var(--board);border:1px solid var(--line);border-radius:.8rem;padding:1rem;margin:1rem 0}
.board h2{font:800 1rem ui-monospace,Menlo,Consolas,monospace;letter-spacing:.16em;text-transform:uppercase;margin:0 0 .75rem;color:var(--accent)}
.countries{display:grid;gap:.75rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,15rem),1fr))}
.area h3{font:700 .9rem ui-monospace,Menlo,Consolas,monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:0 0 .35rem}
.area ul{list-style:none;margin:0;padding:0;display:grid;gap:.25rem}
.area li{background:var(--flap);border:1px solid var(--line);border-radius:.3rem;padding:.3rem .5rem;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.95rem}
.cc{display:inline-block;min-width:2.2rem;color:var(--accent);font-weight:800}
.res{display:flex;flex-wrap:wrap;gap:.5rem;list-style:none;margin:0 0 1rem;padding:0}
.res li{background:var(--flap);border:1px solid var(--line);border-radius:.3rem;padding:.3rem .6rem;font:700 .95rem ui-monospace,Menlo,Consolas,monospace}
h2.plain{font-size:clamp(1.45rem,3.4vw,2rem);margin:2rem 0 .5rem}
.how{max-width:50rem;padding-left:1.2rem}.how li{margin:.5rem 0}
footer{border-top:1px solid var(--line)}
"""


def d2():
    return head(2, CSS2) + f"""<div class="wrap">{chrome(2)}
<header class="mast"><a class="brand" href="/">DNS</a>{own()}</header>
<main id="main">
<div class="top"><div><p class="k">{MARK}</p><h1>{H1}</h1><p>{INTRO}</p></div>
<div class="gate">{form()}</div></div>
<section class="board" aria-labelledby="h-dep"><h2 id="h-dep">Asked on every check</h2>
<ul class="res"><li>Google Public DNS</li><li>Cloudflare</li><li>AliDNS</li></ul>
{countries()}</section>
<h2 class="plain" id="how">How it works</h2>
{how()}
</main>
""" + footer().replace("</body>", "</div></body>")


# ---------------------------------------------------------------- 3. The Path
CSS3 = """
:root{--bg:#f5f7fb;--fg:#121826;--muted:#465066;--link:#1d4ed8;--focus:#1d4ed8;--ctl:#6b7488;--hover:#e5eaf3;--field:#ffffff;--accent:#1d4ed8;--on-accent:#ffffff;--line:#d3dae6;--ok:#166b45;--bad:#a13a2a;--node:#ffffff}
@media (prefers-color-scheme:dark){:root{--bg:#0c111c;--fg:#e9edf5;--muted:#aab4c8;--link:#9db8ff;--focus:#9db8ff;--ctl:#76819a;--hover:#182033;--field:#131a29;--accent:#9db8ff;--on-accent:#0c111c;--line:#273049;--ok:#86ddb3;--bad:#ff9b8a;--node:#131a29}}
.wrap{max-width:70rem;margin:0 auto;padding:0 1rem}
.mast{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:.5rem 1rem;padding:.5rem 0}
.brand{font-weight:800;font-size:1.2rem;color:var(--fg);text-decoration:none;min-height:44px;display:inline-flex;align-items:center}
.own{display:flex;flex-wrap:wrap;gap:.25rem 1rem;font-size:.95rem}.own a{color:var(--fg);min-height:44px;display:inline-flex;align-items:center}
.k{font-size:.85rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:1.5rem 0 .3rem}
h1{font-size:clamp(2.1rem,6vw,3.6rem);line-height:1.05;margin:0 0 1rem;letter-spacing:-.02em}
.lede{max-width:44rem;font-size:1.1rem}
.path{list-style:none;margin:2rem 0;padding:0;display:grid;gap:0;counter-reset:s}
.path>li{counter-increment:s;position:relative;display:grid;grid-template-columns:3rem 1fr;gap:1rem;padding:0 0 1.75rem}
.path>li::before{content:counter(s);display:grid;place-items:center;width:3rem;height:3rem;border-radius:50%;background:var(--accent);color:var(--on-accent);font-weight:800;font-size:1.2rem;z-index:1}
.path>li:not(:last-child)::after{content:"";position:absolute;left:1.45rem;top:3rem;bottom:0;width:3px;background:var(--line)}
.node{background:var(--node);border:1px solid var(--line);border-radius:.8rem;padding:1rem 1.2rem}
.node h2{font-size:1.25rem;margin:0 0 .3rem}
.node p{margin:.3rem 0}
.node .check{margin-bottom:0}
.how{padding-left:1.2rem;margin:.5rem 0 0}.how li{margin:.45rem 0}
footer{border-top:1px solid var(--line)}
"""


def d3():
    return head(3, CSS3) + f"""<div class="wrap">{chrome(3)}
<header class="mast"><a class="brand" href="/">DNS</a>{own()}</header>
<main id="main">
<p class="k">{MARK}</p><h1>{H1}</h1><p class="lede">{INTRO}</p>
<ol class="path">
<li><div class="node"><h2>Your browser asks</h2>{form()}</div></li>
<li><div class="node"><h2>Three public resolvers answer</h2><p>{HOW[0]}</p></div></li>
<li><div class="node"><h2>Google Public DNS, as if from 26 countries</h2><p>{HOW[1]}</p></div></li>
<li><div class="node" id="how"><h2>What it shows, and what it does not</h2><p>{HOW[2]}</p><p>{HOW[3]}</p></div></li>
</ol>
</main>
""" + footer().replace("</body>", "</div></body>")


# ---------------------------------------------------------------- 4. Atlas
CSS4 = """
:root{--bg:#f4efe3;--fg:#211d16;--muted:#5a5144;--link:#0e5a6b;--focus:#0e5a6b;--ctl:#857a67;--hover:#e9e1cf;--field:#fffdf8;--accent:#0e5a6b;--on-accent:#ffffff;--line:#d6cbb3;--ok:#1d6b45;--bad:#a13a2a;--sea:#d8e6e3;--land:#fffdf8}
@media (prefers-color-scheme:dark){:root{--bg:#15130f;--fg:#efe8da;--muted:#c2b8a4;--link:#8fd1df;--focus:#8fd1df;--ctl:#8e8471;--hover:#24201a;--field:#1d1a15;--accent:#8fd1df;--on-accent:#0b1416;--line:#3b352b;--ok:#86ddb3;--bad:#ff9b8a;--sea:#14262a;--land:#1d1a15}}
.wrap{max-width:74rem;margin:0 auto;padding:0 1rem}
.mast{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:.5rem 1rem;padding:.5rem 0;border-bottom:2px solid var(--fg)}
.brand{font:italic 700 1.3rem Georgia,"Iowan Old Style","Times New Roman",serif;color:var(--fg);text-decoration:none;min-height:44px;display:inline-flex;align-items:center}
.own{display:flex;flex-wrap:wrap;gap:.25rem 1rem;font-size:.95rem}.own a{color:var(--fg);min-height:44px;display:inline-flex;align-items:center}
.plate{display:grid;gap:2rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,24rem),1fr));padding:clamp(1.5rem,4vw,3rem) 0}
.k{font-size:.85rem;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:0}
h1,h2{font-family:Georgia,"Iowan Old Style","Times New Roman",serif}
h1{font-size:clamp(2.2rem,6.4vw,4rem);line-height:1.02;margin:.4rem 0 1rem}
.legend{background:var(--land);border:2px solid var(--fg);padding:1rem 1.2rem;box-shadow:.5rem .5rem 0 var(--sea)}
.legend h2{font-size:1.2rem;margin:0}
.map{background:var(--sea);border-radius:1rem;padding:clamp(1rem,3vw,2rem);margin:0 0 2rem}
.map>h2{font-size:clamp(1.45rem,3.4vw,2rem);margin:0 0 1rem}
.countries{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,14rem),1fr))}
.area{background:var(--land);border:1px solid var(--line);border-radius:40% 12% 30% 18%/18% 30% 12% 40%;padding:1rem 1.2rem}
.area h3{font:italic 700 1.1rem Georgia,serif;margin:0 0 .4rem}
.area ul{list-style:none;margin:0;padding:0}
.area li{padding:.15rem 0}
.cc{display:inline-block;min-width:2rem;font:700 .875rem ui-monospace,Menlo,Consolas,monospace;color:var(--accent)}
h2.plain{font-size:clamp(1.45rem,3.4vw,2rem);margin:1rem 0 .5rem}
.how{max-width:48rem;padding-left:1.2rem}.how li{margin:.5rem 0}
footer{border-top:2px solid var(--fg)}
"""


def d4():
    return head(4, CSS4) + f"""<div class="wrap">{chrome(4)}
<header class="mast"><a class="brand" href="/">DNS</a>{own()}</header>
<main id="main">
<div class="plate"><div><p class="k">{MARK}</p><h1>{H1}</h1><p>{INTRO}</p></div>
<div class="legend"><h2>Check a name</h2>{form()}</div></div>
<section class="map" aria-labelledby="h-map"><h2 id="h-map">The 26 countries, by continent</h2>{countries()}</section>
<h2 class="plain" id="how">How it works</h2>
{how()}
</main>
""" + footer().replace("</body>", "</div></body>")


# ---------------------------------------------------------------- 5. Brief
CSS5 = """
:root{--bg:#ffffff;--fg:#111111;--muted:#4a4a4a;--link:#0b4f8a;--focus:#0b4f8a;--ctl:#767676;--hover:#f0f0f0;--field:#ffffff;--accent:#0b4f8a;--on-accent:#ffffff;--line:#d6d6d6;--ok:#1d6b45;--bad:#a13a2a}
@media (prefers-color-scheme:dark){:root{--bg:#121212;--fg:#f1f1f1;--muted:#bdbdbd;--link:#8cc4ff;--focus:#8cc4ff;--ctl:#8a8a8a;--hover:#222;--field:#1a1a1a;--accent:#8cc4ff;--on-accent:#0b0b0b;--line:#333;--ok:#86ddb3;--bad:#ff9b8a}}
.wrap{max-width:42rem;margin:0 auto;padding:0 1rem}
.brand{font:700 1.1rem Georgia,"Times New Roman",serif;color:var(--fg);text-decoration:none;min-height:44px;display:inline-flex;align-items:center}
.own{display:flex;flex-wrap:wrap;gap:0 1rem;font-size:.95rem}.own a{min-height:44px;display:inline-flex;align-items:center}
h1{font:700 clamp(2rem,6vw,2.6rem)/1.15 Georgia,serif;margin:1.25rem 0 .75rem}
h2{font:700 1.45rem Georgia,serif;margin:2rem 0 .4rem;padding-top:1rem;border-top:1px solid var(--line)}
.how{padding-left:1.2rem}.how li{margin:.4rem 0}
footer{border-top:1px solid var(--line);margin-top:2rem}
"""


def d5():
    return head(5, CSS5) + f"""<div class="wrap">{chrome(5)}
<header><a class="brand" href="/">DNS</a>{own()}</header>
<main id="main"><p>{MARK}</p><h1>{H1}</h1><p>{INTRO}</p>{form()}
<h2 id="how">How it works</h2>{how()}</main>
""" + footer().replace("</body>", "</div></body>")


CSSI = """
:root{--bg:#f6f5f2;--fg:#151515;--muted:#4f4c47;--link:#1f5c45;--focus:#1f5c45;--ctl:#77736c;--hover:#e9e6df;--card:#fff;--line:#dcd8cf;--field:#fff;--accent:#1f5c45;--on-accent:#fff;--ok:#1f5c45;--bad:#a13a2a}
@media (prefers-color-scheme:dark){:root{--bg:#121212;--fg:#efede8;--muted:#bdb9b1;--link:#8fd3b0;--focus:#8fd3b0;--ctl:#85817a;--hover:#222;--card:#1c1c1c;--line:#333;--field:#1a1a1a;--accent:#8fd3b0;--on-accent:#0b1410;--ok:#8fd3b0;--bad:#ff9b8a}}
.wrap{max-width:76rem;margin:0 auto;padding:0 1rem}
.brand{font-weight:800;color:var(--fg);text-decoration:none;min-height:44px;display:inline-flex;align-items:center}
h1{font:700 clamp(2rem,5.5vw,3rem)/1.1 Georgia,serif;margin:1rem 0 .75rem}
.cards{list-style:none;margin:1.5rem 0 3rem;padding:0;display:grid;gap:1.25rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,20rem),1fr))}
.cards li{background:var(--card);border:1px solid var(--line);border-radius:.6rem;overflow:hidden}
.cards img{display:block;max-width:100%;height:auto;aspect-ratio:16/10;object-fit:cover;object-position:top;width:100%;border-bottom:1px solid var(--line)}
.cards .b{padding:1rem}.cards h2{font-size:1.2rem;margin:0 0 .3rem}.cards p{margin:.3rem 0}
footer{border-top:1px solid var(--line)}
"""


def index(rec):
    cards = "".join(f'<li><img src="/designs/{i}/shot-1366.webp" alt="Design {i}, {nm}, at desktop width" width="1366" height="854" loading="lazy"><div class="b"><h2><a href="/designs/{i}/">{i}. {nm}</a></h2><p>{idea}</p>{"<p><strong>Recommended by the designer.</strong></p>" if i == rec else ""}</div></li>' for i, nm, idea in DESIGNS)
    f = footer().replace('<script src="/assets/dns.js" defer></script>\n', "")
    return head(0, CSSI) + f"""<div class="wrap">{chrome(0)}
<header><a class="brand" href="/">DNS</a></header>
<main id="main"><h1>Five designs of this site</h1>
<p>The same checker and the same words, in five ideas from the world of DNS. Each one works: type a name and press Check. The owner picks one; the keeper makes it the site.</p>
<ul class="cards">{cards}</ul></main>
""" + f.replace("</body>", "</div></body>")


if __name__ == "__main__":
    for i, f in {1: d1, 2: d2, 3: d3, 4: d4, 5: d5}.items():
        os.makedirs(f"{OUT}/{i}", exist_ok=True)
        open(f"{OUT}/{i}/index.html", "w").write(f())
    open(f"{OUT}/index.html", "w").write(index(int(os.environ.get("RECOMMEND", "3"))))
    print("built", OUT)
