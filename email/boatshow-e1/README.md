# ML-17 · Boat Show — E1 (envio qui 15/10, 10:30 ET)

Conta **Malbor**. Primeiro disparo da campanha de temporada do Boat Show.
Mesma estrutura técnica da peça BOGO (`email/automotive/`): 600px, tabelas,
CSS inline, media query em `max-width:600px`, botões com fallback VML.

| Arquivo | O que é |
|---|---|
| `index.html` | HTML de e-mail |
| `plain-text.txt` | Versão texto puro |
| `assets/` | 8 imagens (ver *Arte pendente*) |
| `check.mjs` | Verificador da campanha |
| `build-zip.sh` | Monta `boatshow-e1-mailchimp.zip` para o *Import zip* |

## Configuração no Mailchimp

| Campo | Valor |
|---|---|
| Subject | `Buy the gallon, get the small one free` |
| Preheader | `Hydro Coat, Nano Polymer Spray, Max Pro Shampoo and Deep Cleaning APC — through Nov 1.` |
| From name | **a definir** (não afeta o HTML) |
| Audience | Malbor — segmentação pendente do Fernando |
| Envio | qui 15/10/2026, 10:30 (horário da Flórida) |

**Nada foi criado nem agendado no Mailchimp.** O agendamento é qua 14/10, com
o seu ok.

## Oferta

Compra do galão 3.78L → leva a embalagem pequena do mesmo produto, grátis,
de 15/10 a 01/11/2026. Desconto automático, já agendado na Shopify.

| Produto | Galão | Brinde | Valor do brinde |
|---|---|---|---|
| Hydro Coat | 3.78L $89 | 473ml | $19 |
| Nano Polymer Spray | 3.78L $139 | 473ml | $29 |
| Max Pro Shampoo | 3.78L $45 | 946ml | $19 |
| Deep Cleaning APC | 3.78L $39 | 473ml | $12 |

Preços e valores conferidos contra o catálogo ao vivo da loja em 07/10/2026.
Perfect Glass e Max Shield ficam fora — o `check.mjs` falha se forem citados.

## Arte pendente

Cinco imagens são **placeholders** e estão marcadas no HTML com comentário
`<!-- PLACEHOLDER: ... -->`; o `check.mjs` conta e avisa quantas restam.

- `hero-boatshow.jpg` (1200x540) — abertura marine, emprestada da peça náutica
- `product-*.jpg` (516x380, 4 arquivos) — galão + embalagem pequena

As fotos da loja existem e estão mapeadas em `build/make-boatshow-assets.py`
(`STORE_PHOTOS`), mas `cdn.shopify.com` está bloqueado pela política de rede
desta sessão. De uma máquina com acesso:

```bash
python3 build/fetch-product-images.py   # baixa e compõe as 4 imagens de produto
```

Isso sobrescreve só os `product-*.jpg`, nas duas peças, com os mesmos nomes e
dimensões — **nenhuma mudança no HTML**. Quando a arte final do Borges chegar
(seg 12/10), basta gravar os arquivos por cima dos mesmos nomes.

## Links

Todos os destinos:

```
https://bogo.malborcoatings.com/?utm_source=mailchimp&utm_medium=email&utm_campaign=boatshow_oct2026&utm_content=malbor
```

## Verificação

```bash
npm install playwright-core   # uma vez, na raiz do repo
node check.mjs
```

Confere host e os 4 UTMs de cada link (inclusive os do VML), `*|UNSUB|*` como
âncora, endereço CAN-SPAM da Malbor, assunto e preheader, CTAs, `alt`/`width`
das imagens, assets referenciados vs. presentes, URLs do texto puro, a janela
15/10–01/11, os **termos proibidos** (`permanent`, `booth`, `visit us`,
`see us at`, `delivery`, `September`, `Buy 1`, `alternative to ceramic
coating`), ausência de número de durabilidade, de alegação ambiental e de
comparação com concorrente, e produtos fora da oferta. Roda offline.
