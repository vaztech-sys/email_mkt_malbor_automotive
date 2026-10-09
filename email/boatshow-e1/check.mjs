import { chromium } from "playwright-core";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

// ML-17 Boat Show — boatshow-e1
const DIR = path.dirname(fileURLToPath(import.meta.url)) + "/";
const CHROME = process.env.CHROME_PATH || "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";
const html = fs.readFileSync(DIR + "index.html", "utf8");
const txt  = fs.readFileSync(DIR + "plain-text.txt", "utf8");
const LP = "bogo.malborcoatings.com";
const UTM = { utm_source:"mailchimp", utm_medium:"email", utm_campaign:"boatshow_oct2026", utm_content:"malbor" };

let fail = 0, warn = 0;
const ok  = m => console.log("  \x1b[32mOK\x1b[0m   " + m);
const bad = m => { fail++; console.log("  \x1b[31mFALHA\x1b[0m " + m); };
const wrn = m => { warn++; console.log("  \x1b[33mAVISO\x1b[0m " + m); };
const flat = t => t.replace(/\s+/g, " ");

function checkUrl(u, where) {
  let p; try { p = new URL(u); } catch { bad(`${where}: URL invalida -> ${u}`); return; }
  if (p.hostname !== LP) { bad(`${where}: host ${p.hostname} != ${LP}`); return; }
  for (const [k, v] of Object.entries(UTM)) {
    const got = p.searchParams.get(k);
    if (got !== v) { bad(`${where}: ${k}="${got}" (esperado "${v}")`); return; }
  }
  return true;
}

const b = await chromium.launch({ executablePath: CHROME, args:["--no-sandbox"] });
const pg = await b.newPage();
await pg.route("**/*", r => r.abort());   // offline
await pg.setContent(html);
const bodyText = await pg.evaluate(() => document.body.innerText);

console.log("\n1) LINKS NO DOM");
const anchors = await pg.$$eval("a[href]", as => as.map(a => ({ href: a.getAttribute("href"), text: (a.innerText||"").trim().slice(0,42) })));
let lpCount = 0;
for (const a of anchors) {
  const h = a.href;
  if (h.startsWith("*|")) { ok(`merge tag ${h}`); continue; }
  if (h.startsWith("mailto:") || h.startsWith("tel:")) { ok(`${h}`); continue; }
  if (checkUrl(h, `link "${a.text||"(imagem)"}"`)) lpCount++;
}
console.log(`  -> ${anchors.length} links no DOM, ${lpCount} para a LP com UTM completo`);

console.log("\n2) LINKS NO VML (OUTLOOK)");
const vml = [...html.matchAll(/<v:roundrect[^>]*href="([^"]+)"/g)].map(m => m[1].replace(/&amp;/g, "&"));
vml.length === 2 ? ok(`${vml.length} botao(oes) VML`) : bad(`${vml.length} botoes VML (esperado 2)`);
vml.forEach((u, i) => { if (checkUrl(u, `VML #${i+1}`)) ok(`VML #${i+1} com UTM completo`); });

console.log("\n3) SHOPIFY INTERNO");
(/myshopify\.com/i.test(html) || /myshopify\.com/i.test(txt))
  ? bad("referencia a myshopify.com encontrada") : ok("nenhuma referencia a myshopify.com");

console.log("\n4) DESCADASTRO");
html.includes("*|UNSUB|*") ? ok("*|UNSUB|* no HTML") : bad("*|UNSUB|* ausente no HTML");
txt.includes("*|UNSUB|*")  ? ok("*|UNSUB|* no texto") : bad("*|UNSUB|* ausente no texto");
const unsubAnchor = anchors.find(a => a.href === "*|UNSUB|*");
unsubAnchor ? ok(`ancora de descadastro: "${unsubAnchor.text}"`) : bad("descadastro nao e um <a> clicavel");

console.log("\n5) ENDERECO FISICO (CAN-SPAM)");
const ADDR = "4634 Waycross Dr, Coconut Creek, FL 33073";
bodyText.includes(ADDR) ? ok("endereco Malbor no rodape") : bad("endereco ausente no HTML");
txt.includes(ADDR) ? ok("endereco Malbor no texto puro") : bad("endereco ausente no texto");

console.log("\n6) ASSUNTO / PREHEADER");
const TITLE = "Buy the gallon, get the small one free";
const title = await pg.title();
title === TITLE ? ok(`title = "${title}"`) : bad(`title = "${title}" (esperado "${TITLE}")`);
const PRE = "Hydro Coat, Nano Polymer Spray, Max Pro Shampoo and Deep Cleaning APC &mdash; through Nov 1.";
html.includes(PRE) ? ok("preheader presente e oculto") : bad("preheader ausente ou alterado");

console.log("\n7) CTAs");
for (const label of ["SHOP THE GALLONS", "SHOP NOW"]) {
  bodyText.includes(label) ? ok(`CTA "${label}"`) : bad(`CTA "${label}" ausente`);
}

console.log("\n8) IMAGENS");
const imgs = await pg.$$eval("img", is => is.map(i => ({ src: i.getAttribute("src"), alt: i.getAttribute("alt"), w: i.getAttribute("width") })));
const noAlt = imgs.filter(i => i.alt === null);
noAlt.length ? bad(`${noAlt.length} imagem(ns) sem alt`) : ok(`${imgs.length} imagens, todas com alt (${imgs.filter(i=>i.alt==="").length} decorativas)`);
const noW = imgs.filter(i => !i.w);
noW.length ? wrn(`${noW.length} imagem(ns) sem width`) : ok("todas com width explicito");
const files = fs.readdirSync(DIR + "assets");
const refd = [...new Set(imgs.map(i => i.src.split("/").pop()))];
const orfas = refd.filter(f => !files.includes(f));
orfas.length ? bad(`referenciadas mas ausentes: ${orfas.join(", ")}`) : ok(`${refd.length} arquivos referenciados, todos em assets/`);
const naoUsadas = files.filter(f => !refd.includes(f));
naoUsadas.length ? wrn(`em assets/ mas nao usadas: ${naoUsadas.join(", ")}`) : ok("nenhum asset orfao");

console.log("\n9) TEXTO PURO");
const txtUrls = [...txt.matchAll(/https?:\/\/\S+/g)].map(m => m[0]);
txtUrls.forEach((u, i) => checkUrl(u, `texto puro #${i+1}`));
txtUrls.length >= 2 ? ok(`${txtUrls.length} URLs no texto puro, todas com UTM`) : bad("poucas URLs no texto puro");

console.log("\n10) JANELA DA CAMPANHA (15/10 - 01/11/2026)");
const WIN = /October 15\s*[-–]\s*November 1, 2026/;
WIN.test(flat(bodyText)) ? ok("HTML: \"October 15 - November 1, 2026\"") : bad("HTML: janela de datas ausente/incorreta");
WIN.test(flat(txt)) ? ok("texto puro: \"October 15 - November 1, 2026\"") : bad("texto puro: janela ausente/incorreta");
/November 1/.test(bodyText) ? ok("HTML: encerramento em November 1") : bad("HTML: sem November 1");

console.log("\n11) TERMOS PROIBIDOS");
const BANNED = [
  [/permanent/i, "claim de permanencia"],
  [/\bbooth\b/i, "estande (sem estande no FLIBS)"],
  [/visit us/i, "convite presencial"],
  [/see us at/i, "convite presencial"],
  [/\bdeliver(y|ies|ed|s)?\b/i, "entrega (so retirada local)"],
  [/September/i, "mes da campanha anterior"],
  [/Buy 1/i, "linguagem da campanha BOGO anterior"],
  [/alternative to ceramic coating/i, "comparacao/claim herdado"],
];
let hits = 0;
for (const [re, label] of BANNED) {
  const m = flat(bodyText).match(re) || flat(txt).match(re);
  if (m) { bad(`${label}: "${m[0]}"`); hits++; }
}
if (!hits) ok(`nenhum dos ${BANNED.length} termos proibidos`);

console.log("\n12) CLAIMS DE DURABILIDADE (nenhum numero)");
const DUR = /\b\d+\s*(month|months|year|years|hora|horas)\b/i;
const dm = flat(bodyText).match(DUR) || flat(txt).match(DUR);
dm ? bad(`numero de durabilidade presente: "${dm[0]}"`) : ok("nenhum numero de durabilidade");
const ENV = /\b(eco[- ]friendly|biodegradable|environmentally friendly|non[- ]toxic)\b/i;
(ENV.test(bodyText) || ENV.test(txt)) ? bad("alegacao ambiental") : ok("nenhuma alegacao ambiental");
const COMP = /\b(better than|outperforms|superior to|best .{0,24} on the market)\b/i;
(COMP.test(bodyText) || COMP.test(txt)) ? bad("comparacao com concorrente") : ok("nenhuma comparacao com concorrente");

console.log("\n13) PRODUTOS FORA DA OFERTA");
const OUT_OF_SCOPE = [/Perfect Glass/i, /Max Shield/i];
let oos = 0;
for (const re of OUT_OF_SCOPE) {
  const m = bodyText.match(re) || txt.match(re);
  if (m) { bad(`produto fora da campanha citado: "${m[0]}"`); oos++; }
}
if (!oos) ok("sem Perfect Glass nem Max Shield");

console.log("\n14) ARTE PENDENTE");
const ph = (html.match(/ASSET-BASE-REPLACE-ME/g) || []).length;
ph ? wrn(`${ph} ocorrencias de ASSET-BASE-REPLACE-ME (build-zip.sh troca por images/)`) : ok("sem placeholders de asset base");
const art = (html.match(/PLACEHOLDER:/g) || []).length;
art ? wrn(`${art} imagem(ns) 100% placeholder — trocar pela arte do Borges (12/10)`) : ok("nenhuma arte totalmente placeholder");
const partial = (html.match(/ARTE PARCIAL:/g) || []).length;
partial ? wrn(`${partial} imagem(ns) com arte parcial — galao real, falta a foto do brinde`) : ok("nenhuma arte parcial");

await b.close();
console.log("\n" + "=".repeat(60));
console.log(fail ? `\x1b[31m${fail} FALHA(S)\x1b[0m, ${warn} aviso(s)` : `\x1b[32mTODAS AS VERIFICACOES PASSARAM\x1b[0m (${warn} aviso(s) esperado(s))`);
process.exit(fail ? 1 : 0);
