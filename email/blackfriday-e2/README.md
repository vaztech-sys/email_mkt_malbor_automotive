# ML-41 · Black Friday — E2 (envio sex 27/11, 10:30 ET)

Conta **Malbor**. Primeiro dos dois disparos do Black Friday.

HTML portado de `black-friday/emails/e2-malbor/` no repositório
`vaztech-sys/marketing-malbor`, branch `claude/black-friday-2026`, **sem
alteração no texto**. A estrutura da pasta segue as peças do Boat Show deste
repositório: 600px, tabelas, CSS inline, media query em `max-width:600px`,
botões com VML para o Outlook, entrega por *Import zip*.

| Arquivo | O que é |
|---|---|
| `index.html` | HTML de e-mail |
| `plain-text.txt` | Versão texto puro |
| `assets/` | 7 arquivos (5 imagens ainda provisórias — ver abaixo) |
| `check.mjs` | Verificador da campanha |
| `build-zip.sh` | Monta `blackfriday-e2-mailchimp.zip` |

## Configuração no Mailchimp

| Campo | Valor |
|---|---|
| Subject | `Black Friday: 25% off the Professional Line` |
| Preheader | `35% off when you buy 5, plus a free SiO2 Top Sealant. Nov 27–30.` |
| Envio | sex 27/11/2026, 10:30 (horário da Flórida) |
| Audience | Malbor — **suprimir quem também está na lista da Yacht Pro** |

**Nada foi criado nem agendado no Mailchimp.**

## Oferta

27 a 30/11/2026. 25% em todo frasco da linha Professional, 35% na compra de 5
ou mais (podem ser misturados) e 1 SiO2 Top Sealant grátis por frasco.
Desconto automático no checkout, sem cupom. Só retirada local em Pompano Beach
e no Safe Harbor Lauderdale Marine Center.

## Imagens provisórias

As 5 imagens de conteúdo ainda são **placeholders** — um quadro escuro escrito
"TROCAR". O `check.mjs` avisa enquanto estiverem lá.

| Frame no Figma | Arquivo | Origem |
|---|---|---|
| `email-hero-malbor` | `email-hero-malbor.jpg` | slide 1 do carrossel |
| `email-boat` | `email-boat.jpg` | slide 2 (For the boat) |
| `email-car` | `email-car.jpg` | slide 3 (For the car) |
| `email-interior` | `email-interior.jpg` | slide 4 (Interior & trim) |
| `email-gift` | `email-gift.jpg` | story do brinde de 24/11 |

Arquivo "[MALBOR] Redes Sociais", página "Calendário (BLACK FRIDAY)", seção
"E-mails Black Friday — imagens (exportar)". Exportar em **JPG 1200w** e gravar
por cima dos mesmos nomes em `assets/` — o HTML não muda. Depois rodar
`node check.mjs` e `./build-zip.sh`.

## Links

Todos os destinos:

```
https://bogo.malborcoatings.com/?utm_source=mailchimp&utm_medium=email&utm_campaign=blackfriday_nov2026&utm_content=bf-malbor
```

A peça da Yacht Pro usa `utm_content=bf-marine`.

## Verificação

```bash
npm install playwright-core   # uma vez, na raiz do repo
node check.mjs
```

Portado de `black-friday/emails/check.mjs`, com a configuração embutida (estas
pastas não têm `config.json`), rodando offline e resolvendo o Chromium sem
caminho fixo. Confere: host e os 4 UTMs de cada link, inclusive os de dentro
dos comentários VML do Outlook; ausência de `myshopify.com`; `*|UNSUB|*` como
âncora clicável; endereço CAN-SPAM da Malbor e ausência do endereço da Yacht
Pro; `title` igual ao subject e preheader presente; `alt` e `width` em todas as
imagens; assets referenciados vs. presentes; as datas da oferta e nenhuma
campanha antiga; URLs do texto puro; e os 16 termos proibidos — `permanent`,
`lifetime`, `months`, `years`, `delivery`, `free shipping`, alegação ambiental,
`for your car` / `for your boat`, entre outros.

## Antes de agendar

- **Domínio da Malbor autenticado** e teste de caixa de entrada no Gmail,
  Outlook e iCloud. O automotivo do BOGO teve zero aberturas.
- **Estoque** dos produtos citados no texto — ver o levantamento no corpo da
  conversa e o README da raiz.
- **Supressão** de quem está nas duas listas.
