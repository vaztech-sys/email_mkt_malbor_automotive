import { chromium } from "playwright-core";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

// ML-41 Black Friday — blackfriday-e4
// Regras portadas de black-friday/emails/check.mjs (vaztech-sys/marketing-malbor).
const DIR = path.dirname(fileURLToPath(import.meta.url)) + "/";
// Resolve o Chromium sem caminho fixo: a versão em /opt/pw-browsers muda a
// cada imagem de container, e um caminho cravado quebra silenciosamente.
function findChrome() {
  if (process.env.CHROME_PATH && fs.existsSync(process.env.CHROME_PATH)) return process.env.CHROME_PATH;
  const base = process.env.PLAYWRIGHT_BROWSERS_PATH || "/opt/pw-browsers";
  if (fs.existsSync(base)) {
    for (const dir of fs.readdirSync(base).filter(d => d.startsWith("chromium")).sort().reverse()) {
      for (const sub of ["chrome-linux64/chrome", "chrome-linux/chrome"]) {
        const c = path.join(base, dir, sub);
        if (fs.existsSync(c)) return c;
      }
    }
  }
  for (const c of ["/usr/bin/google-chrome", "/usr/bin/chromium"]) if (fs.existsSync(c)) return c;
  throw new Error("Chromium não encontrado — defina CHROME_PATH");
}
const CHROME = findChrome();
const CFG = {
  "conta": "malbor",
  "utm_content": "bf-malbor",
  "endereco": "4634 Waycross Dr, Coconut Creek, FL 33073",
  "titulo": "Ends tonight: 25% off the Professional Line",
  "preheader": "35% when you buy 5, plus a free SiO2 Top Sealant.",
  "datas": [
    "November 30"
  ],
  "provisorias": []
};
const html = fs.readFileSync(DIR + "index.html", "utf8");
const txt  = fs.readFileSync(DIR + "plain-text.txt", "utf8");
const LP = "bogo.malborcoatings.com";
const UTM = { utm_source:"mailchimp", utm_medium:"email", utm_campaign:"blackfriday_nov2026", utm_content: CFG.utm_content };

// Regras do jurídico da Malbor + campanha
const PROIBIDOS = ["permanent", "lifetime", "months", "years", "delivery", "free shipping",
  "ceramic coating alternative", "alternative to ceramic coating", "eco-friendly", "environment",
  "for your car", "for your boat", "with your order", "Buy 1", "booth", "visit us"];
const ANTIGOS = /September|October|bogo_sept2026|boatshow_oct2026|\[DATAS\]|\[PER[IÍ]ODO\]/;

let fail = 0, warn = 0;
const ok  = m => console.log("  \x1b[32mOK\x1b[0m    " + m);
const bad = m => { fail++; console.log("  \x1b[31mFALHA\x1b[0m " + m); };
const wrn = m => { warn++; console.log("  \x1b[33mAVISO\x1b[0m " + m); };
const checkUrl = (u, where) => {
  let p; try { p = new URL(u); } catch { bad(`${where}: URL inválida ${u}`); return false; }
  if (p.hostname !== LP) { bad(`${where}: host ${p.hostname}`); return false; }
  for (const [k, v] of Object.entries(UTM)) if (p.searchParams.get(k) !== v) { bad(`${where}: ${k}=${p.searchParams.get(k)} (esperado ${v})`); return false; }
  return true;
};

console.log(`\n=== blackfriday-e4 (${CFG.conta}) ===`);
const b = await chromium.launch({ executablePath: CHROME, args:["--no-sandbox"] });
const pg = await b.newPage();
await pg.route("**/*", r => r.abort());   // offline
await pg.setContent(html);
const body = await pg.evaluate(() => document.body.innerText);

const anchors = await pg.$$eval("a[href]", as => as.map(a => ({ href: a.getAttribute("href"), text: (a.innerText || "").trim().slice(0, 40) })));
let lp = 0;
for (const a of anchors) {
  if (a.href.startsWith("*|")) continue;
  if (checkUrl(a.href, `link "${a.text || "(imagem)"}"`)) lp++;
}
ok(`${lp} links para a LP com UTM completo (utm_content=${CFG.utm_content})`);

const vml = [...html.matchAll(/<v:roundrect[^>]*href="([^"]+)"/g)].map(m => m[1].replace(/&amp;/g, "&"));
vml.length ? (vml.every((u, i) => checkUrl(u, `VML #${i + 1}`)) && ok(`${vml.length} botões VML com UTM`)) : bad("nenhum botão VML");
/myshopify\.com/i.test(html + txt) ? bad("myshopify.com encontrado") : ok("sem myshopify.com");

html.includes("*|UNSUB|*") && txt.includes("*|UNSUB|*") ? ok("*|UNSUB|* no HTML e no texto") : bad("*|UNSUB|* ausente");
const unsubAnchor = anchors.find(a => a.href === "*|UNSUB|*");
unsubAnchor ? ok(`âncora de descadastro: "${unsubAnchor.text}"`) : bad("descadastro não é um <a> clicável");
body.includes(CFG.endereco) && txt.includes(CFG.endereco) ? ok(`endereço ${CFG.conta} no rodapé (HTML e texto)`) : bad("endereço CAN-SPAM ausente");
/Fort Lauderdale, FL 33315/.test(html) ? bad("endereço da YachtPro na peça da Malbor") : ok("sem endereço da outra conta");

(await pg.title()) === CFG.titulo ? ok("title = subject") : bad(`title = "${await pg.title()}"`);
html.includes(CFG.preheader) ? ok("preheader presente") : bad("preheader ausente");

const imgs = await pg.$$eval("img", is => is.map(i => ({ src: i.getAttribute("src"), alt: i.getAttribute("alt"), w: i.getAttribute("width") })));
imgs.some(i => i.alt === null) ? bad("imagem sem alt") : ok(`${imgs.length} imagens com alt`);
imgs.some(i => !i.w) ? bad("imagem sem width") : ok("todas com width");
const files = fs.readdirSync(DIR + "assets");
const refd = [...new Set(imgs.map(i => i.src.split("/").pop()))];
const falt = refd.filter(f => !files.includes(f));
falt.length ? bad(`ausentes em assets/: ${falt.join(", ")}`) : ok(`${refd.length} arquivos referenciados, todos presentes`);
const sobra = files.filter(f => !refd.includes(f));
sobra.length ? wrn(`assets não usados: ${sobra.join(", ")}`) : ok("nenhum asset órfão");

for (const d of CFG.datas) (body.includes(d) && txt.includes(d)) ? ok(`"${d}" no HTML e no texto`) : bad(`"${d}" faltando no HTML ou no texto`);
ANTIGOS.test(body + txt + html) ? bad("data, campanha antiga ou placeholder [DATAS] remanescente") : ok("sem campanha antiga nem [DATAS]");

let achou = 0;
for (const t of PROIBIDOS) {
  const re = new RegExp(t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "i");
  if (re.test(body) || re.test(txt)) { achou++; bad(`termo proibido "${t}"`); }
}
achou || ok(`nenhum dos ${PROIBIDOS.length} termos proibidos`);

const tu = [...txt.matchAll(/https?:\/\/\S+/g)].map(m => m[0]);
tu.length && tu.every((u, i) => checkUrl(u, `texto #${i + 1}`)) ? ok(`${tu.length} URLs no texto puro com UTM`) : bad("URLs do texto puro");

const ph = (html.match(/ASSET-BASE-REPLACE-ME/g) || []).length;
ph ? wrn(`${ph} ocorrências de ASSET-BASE-REPLACE-ME (build-zip.sh troca por images/)`) : ok("sem placeholders de asset base");
const prov = CFG.provisorias || [];
prov.length ? wrn(`${prov.length} imagem(ns) provisória(s): ${prov.join(", ")} — exportar do Figma em JPG 1200w`) : ok("imagens finais do Figma");

await b.close();
console.log("\n" + "=".repeat(60));
console.log(fail ? `\x1b[31m${fail} FALHA(S)\x1b[0m, ${warn} aviso(s)` : `\x1b[32mTODAS AS VERIFICAÇÕES PASSARAM\x1b[0m (${warn} aviso(s) esperado(s))`);
process.exit(fail ? 1 : 0);
