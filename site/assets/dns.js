// DNS checker: runs in the visitor's browser only. No server, no cookies, no tracking.
// Each lookup goes straight from the browser to public DNS-over-HTTPS resolvers that allow
// browser calls (checked 22 Nov 2026): Google Public DNS, Cloudflare and AliDNS.
// Per-country answers use Google's edns_client_subnet parameter with a /24 from
// data/regions.json (allocations listed by RIPEstat).
const TYPES = { A: 1, AAAA: 28, CNAME: 5, MX: 15, NS: 2, TXT: 16, SOA: 6, CAA: 257 };
const RESOLVERS = [
  { id: 'google', name: 'Google Public DNS', where: 'Anycast, nearest to you', url: (n, t) => `https://dns.google/resolve?name=${n}&type=${t}` },
  { id: 'cloudflare', name: 'Cloudflare', where: 'Anycast, nearest to you', url: (n, t) => `https://cloudflare-dns.com/dns-query?name=${n}&type=${t}`, headers: { accept: 'application/dns-json' } },
  { id: 'alidns', name: 'AliDNS (Alibaba)', where: 'Anycast, run by Alibaba Cloud', url: (n, t) => `https://dns.alidns.com/resolve?name=${n}&type=${t}` },
];
const STATUS = { 0: 'Resolved', 1: 'Format error', 2: 'Server failure', 3: 'Name does not exist', 5: 'Refused' };

const $ = s => document.querySelector(s);
const form = $('#check'), out = $('#results'), note = $('#summary');
let regions = [];

function cleanName(v) {
  return v.trim().replace(/^[a-z]+:\/\//i, '').replace(/[/?#].*$/, '').replace(/\.$/, '').toLowerCase();
}
function valid(n) {
  return n.length > 0 && n.length <= 253 && /^[a-z0-9_]([a-z0-9_-]{0,62})(\.[a-z0-9_]([a-z0-9_-]{0,62}))*$/i.test(n);
}

async function ask(url, headers) {
  const ctl = new AbortController();
  const timer = setTimeout(() => ctl.abort(), 8000);
  try {
    const r = await fetch(url, { headers: headers || {}, signal: ctl.signal, credentials: 'omit', referrerPolicy: 'no-referrer' });
    if (!r.ok) return { error: `HTTP ${r.status}` };
    return await r.json();
  } catch (e) {
    return { error: e.name === 'AbortError' ? 'No answer in 8 seconds' : 'Could not reach the resolver' };
  } finally { clearTimeout(timer); }
}

function answers(json, code) {
  const list = (json.Answer || []).filter(a => a.type === code).map(a => String(a.data));
  return list.sort();
}

function cell(text, cls) {
  const td = document.createElement('td');
  if (cls) td.className = cls;
  td.textContent = text;
  return td;
}

function verdict(json, code) {
  if (json.error) return { ok: false, text: json.error, values: [] };
  const values = answers(json, code);
  if (json.Status !== 0) return { ok: false, text: STATUS[json.Status] || `Status ${json.Status}`, values };
  if (!values.length) return { ok: false, text: 'No record of this type', values };
  return { ok: true, text: 'Resolved', values };
}

function row(tbody, label, sub, v, ttl) {
  const tr = document.createElement('tr');
  const th = document.createElement('th');
  th.scope = 'row';
  th.textContent = label;
  if (sub) { const s = document.createElement('span'); s.className = 'sub'; s.textContent = sub; th.append(s); }
  tr.append(th);
  tr.append(cell(v.ok ? '✓ ' + v.text : '✗ ' + v.text, v.ok ? 'ok' : 'bad'));
  tr.append(cell(v.values.join('\n') || '-', 'vals'));
  tr.append(cell(ttl == null ? '-' : String(ttl), 'num'));
  tbody.append(tr);
  return tr;
}

function table(caption) {
  const t = document.createElement('table');
  t.innerHTML = '<caption></caption><thead><tr><th scope="col">Resolver or region</th><th scope="col">Result</th><th scope="col">Answer</th><th scope="col">TTL (s)</th></tr></thead><tbody></tbody>';
  t.querySelector('caption').textContent = caption;
  const wrap = document.createElement('div');
  wrap.className = 'scroll';
  wrap.tabIndex = 0;
  wrap.setAttribute('role', 'region');
  wrap.setAttribute('aria-label', caption);
  wrap.append(t);
  out.append(wrap);
  return t.querySelector('tbody');
}

function ttlOf(json, code) {
  const a = (json.Answer || []).find(x => x.type === code);
  return a ? a.TTL : null;
}

async function run(name, type) {
  const code = TYPES[type];
  out.textContent = '';
  note.textContent = `Checking ${type} records for ${name}...`;
  const seen = new Map();
  const tally = v => { const k = v.ok ? v.values.join(',') : '(' + v.text + ')'; seen.set(k, (seen.get(k) || 0) + 1); };

  const t1 = table('Public resolvers');
  const res = await Promise.all(RESOLVERS.map(r => ask(r.url(encodeURIComponent(name), type), r.headers)));
  res.forEach((json, i) => { const v = verdict(json, code); tally(v); row(t1, RESOLVERS[i].name, RESOLVERS[i].where, v, ttlOf(json, code)); });

  const t2 = table('As seen from each country (Google Public DNS, client subnet)');
  let scoped = false;
  const byArea = {};
  regions.forEach(r => { (byArea[r.area] = byArea[r.area] || []).push(r); });
  const jobs = regions.map(r => ask(`https://dns.google/resolve?name=${encodeURIComponent(name)}&type=${type}&edns_client_subnet=${encodeURIComponent(r.subnet)}`));
  const regionRes = await Promise.all(jobs);
  const idx = new Map(regions.map((r, i) => [r.cc, i]));
  for (const area of Object.keys(byArea)) {
    const g = document.createElement('tr');
    g.className = 'group';
    const th = document.createElement('th');
    th.colSpan = 4; th.scope = 'rowgroup'; th.textContent = area;
    g.append(th); t2.append(g);
    for (const r of byArea[area]) {
      const json = regionRes[idx.get(r.cc)];
      const v = verdict(json, code);
      tally(v);
      if (json.edns_client_subnet && !/\/0$/.test(json.edns_client_subnet)) scoped = true;
      row(t2, r.name, r.subnet, v, ttlOf(json, code));
    }
  }

  const distinct = seen.size;
  note.textContent = distinct === 1
    ? `${name} ${type}: every resolver and country gave the same answer.`
    : `${name} ${type}: ${distinct} different answers across ${RESOLVERS.length} resolvers and ${regions.length} countries.` +
      (scoped ? ' The name’s DNS answers by location (it uses the client subnet), so differences by country are expected.' : ' The name does not answer by location, so differences may mean a change still spreading or a resolver problem.');
}

async function init() {
  try { regions = (await (await fetch('/data/regions.json')).json()).regions; } catch { regions = []; }
  const p = new URLSearchParams(location.hash.slice(1));
  if (p.get('name')) {
    form.name.value = p.get('name');
    if (TYPES[p.get('type')]) form.type.value = p.get('type');
    form.requestSubmit();
  }
}

form.addEventListener('submit', e => {
  e.preventDefault();
  const name = cleanName(form.name.value);
  const type = form.type.value;
  if (!valid(name)) { note.textContent = 'Enter a domain name, for example sovereignweb.site.'; form.name.focus(); return; }
  form.name.value = name;
  history.replaceState(null, '', `#name=${encodeURIComponent(name)}&type=${type}`);
  run(name, type);
});

init();
