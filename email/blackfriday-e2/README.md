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
| `assets/` | 7 arquivos, 779 KB (artes finais do Figma) |
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

## Imagens

As 5 imagens são as **artes finais do Figma**, exportadas em JPG 1200w.

Arquivo `[MALBOR] Email_mkt` (`w963vkkHw77eIJtVseKOIH`), página BLACK FRIDAY,
seção "E-mails Black Friday — imagens (exportar)":

| Frame | Node | Arquivo | Export |
|---|---|---|---|
| `email-hero-malbor` | `163:146` | `email-hero-malbor.jpg` | 1200×1189 |
| `email-boat` | `163:165` | `email-boat.jpg` | 1200×723 |
| `email-car` | `163:185` | `email-car.jpg` | 1200×645 |
| `email-interior` | `163:208` | `email-interior.jpg` | 1200×617 |
| `email-gift` | `163:234` | `email-gift.jpg` | 1200×745 |

Os frames têm 1080 de largura, então o export sai em **escala 1,1111** para dar
os 1200 que o HTML espera.

Para reexportar, salve os JPG num diretório e rode:

```bash
python3 build/make-blackfriday-assets.py <dir-com-os-jpg>
```

O script confere a largura, recomprime em JPEG progressivo q86 sem subamostragem
de croma e grava nas duas peças. A recompressão não é opcional: os exports do
Figma somam 2,7 MB, o que deixaria o E2 pesado demais para abrir no celular; a
q86 em 4:4:4 o conjunto cai para 779 KB sem diferença visível no gradiente
escuro nem sangramento do laranja.

### Defeito conhecido no `email-gift`

O frame começa 10 unidades abaixo do topo da linha *"with every Professional
Line bottle."*, então os ascendentes dessa linha saem cortados no export. A
frase é redundante — a legenda logo abaixo da imagem já diz *"Free with every
Professional Line bottle."* Duas saídas, as duas no Figma: descer o frame uns
60px para deixar só os frascos, ou subir 10px para encaixar a linha inteira.
Depois é só reexportar e rodar o script acima.

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
