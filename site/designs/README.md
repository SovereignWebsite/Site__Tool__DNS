# Five designs of dns.tool.sovereignweb.site

Round 1 by design.c@SovereignWebsite.dinis (account C), 23 November 2026. The same words as the home page at dev 4fda3bf and the same working checker: each design keeps the form's ids (#check, #name, #type, #summary, #results) and loads the site's own /assets/dns.js, so a check runs in every design. Checked against SovereignWebsite/Site__Agent__Design docs/guidelines.md and docs/rating.md.

Each design carries a Content Security Policy that names only the three resolvers (dns.google, cloudflare-dns.com, dns.alidns.com), and says next to the form what is sent and to whom (guidelines 1.3). Nothing loads from another host when the page opens.

## The five

1. **Zone File.** The page written as a DNS zone file: monospace, the words as comments, the form as one record line.
2. **Departures** (dark first). A departures board: the three resolvers and the 26 countries (from the site's own data/regions.json) on the board, the form as the gate.
3. **The Path.** The journey of one question, step by step: your browser asks, three resolvers answer, Google Public DNS as if from 26 countries, what it shows and what it does not.
4. **Atlas** (way out there). An atlas plate: the countries by continent on a sea-coloured map, the form as the legend.
5. **Brief.** Everything on one plain page.

## Rating (rating.md)

Checked locally at 320, 390 and 1366 px, light and dark, before and after a check (sovereignweb.site, A): axe-core 4.10 finds nothing at any impact; the site's own .github/ci/axe.mjs, html-validate, share-check and quality pass; no sideways scroll; no request to another host on load, and only the three resolvers on Check; no em or en dashes. Each is a 3 (candidate): level 4 needs the hand checks, the synthetic users and the owner's "wow".

## Recommendation

**3, The Path.** A DNS checker is hard to trust when you cannot see what it does; The Path makes the explanation the page, with the form as its first step. Departures is second, for the most striking look.

## How to rebuild

`python3 site/designs/_build/build.py site` from the repository root.
