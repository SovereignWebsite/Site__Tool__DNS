// Builds site/data/regions.json: for each country, one IPv4 /24 inside a prefix that the
// country's regional internet registry allocated to it, as listed by RIPEstat
// (country-resource-list). The page sends that /24 to Google Public DNS as the EDNS client
// subnet, so a CDN answers as it would for a client in that country. Run by hand or by CI:
//   node docs/regions.mjs > site/data/regions.json
const COUNTRIES = [
  ['US','United States','North America'],['CA','Canada','North America'],['MX','Mexico','North America'],
  ['BR','Brazil','South America'],['AR','Argentina','South America'],['CL','Chile','South America'],
  ['GB','United Kingdom','Europe'],['PT','Portugal','Europe'],['ES','Spain','Europe'],['FR','France','Europe'],
  ['DE','Germany','Europe'],['NL','Netherlands','Europe'],['SE','Sweden','Europe'],['PL','Poland','Europe'],
  ['ZA','South Africa','Africa'],['NG','Nigeria','Africa'],['KE','Kenya','Africa'],['EG','Egypt','Africa'],
  ['AE','United Arab Emirates','Asia'],['IN','India','Asia'],['SG','Singapore','Asia'],['JP','Japan','Asia'],
  ['KR','South Korea','Asia'],['HK','Hong Kong','Asia'],['AU','Australia','Oceania'],['NZ','New Zealand','Oceania'],
];
const out = { source: 'https://stat.ripe.net/docs/data-api/api-endpoints/country-resource-list', built: new Date().toISOString().slice(0,10), regions: [] };
for (const [cc, name, area] of COUNTRIES) {
  const r = await fetch(`https://stat.ripe.net/data/country-resource-list/data.json?resource=${cc}&v4_format=prefix`);
  const v4 = (await r.json()).data.resources.ipv4.filter(p => +p.split('/')[1] <= 24);
  if (!v4.length) continue;
  const prefix = v4[Math.floor(v4.length / 2)];
  out.regions.push({ cc, name, area, prefix, subnet: prefix.split('/')[0] + '/24' });
}
console.log(JSON.stringify(out, null, 2));
