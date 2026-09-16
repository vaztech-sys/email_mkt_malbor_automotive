# E-mail automotivo — Campanha BOGO (conta Malbor)

HTML de e-mail pronto para o Mailchimp, convertido do export do Figma Make
(`EMAIL_MKT_Automotive`, React + Tailwind). Peça irmã da náutica em
`vaztech-sys/email_mkt_malbor_marines` (`email/marines/`), construída com a
mesma estrutura técnica e a mesma geometria.

| Arquivo | O que é |
|---|---|
| `index.html` | HTML de e-mail — tabelas, CSS inline, responsivo |
| `plain-text.txt` | Versão texto puro |
| `assets/` | 9 imagens otimizadas (184 KB no total) |
| `check.mjs` | Verificador automático (links/UTM, descadastro, endereço, datas, claims) |
| `build-zip.sh` | Monta o pacote do *Import zip* |

## Configuração da campanha no Mailchimp

| Campo | Valor |
|---|---|
| Subject | `Buy 1, Get 1: 3.78L gallons of Max Shield, Max Pro and Deep Cleaning` |
| Preheader | `Two weeks only. Discount applies automatically at checkout.` |
| From name | `Malbor Coatings` |
| From e-mail | **a definir** — usar um domínio autenticado da Malbor |
| Audience | Malbor — **conferir a contagem antes de enviar** (ver Pendências) |

O preheader também está embutido no HTML como bloco oculto, para clientes que
ignoram o campo do Mailchimp.

## Como publicar — use *Import zip*, não *Paste in Code*

```bash
./build-zip.sh          # gera bogo-automotive-mailchimp.zip
```

O script copia `assets/` para `images/`, troca o placeholder
`https://ASSET-BASE-REPLACE-ME/` por caminhos relativos `images/` e trava se
sobrar algum placeholder ou se algum `src` referenciar arquivo ausente.

1. *Campaigns → Email → Regular → Content → Code your own → **Import zip***
   e suba o zip. O Mailchimp hospeda as imagens no CDN e reescreve os `src`
   sozinho — dispensa Content Studio e find-replace.
2. Cole `plain-text.txt` na aba *Plain-Text Email* (a versão automática do
   Mailchimp é pior).
3. Na aba **Settings**:
   - **não** marcar o *CSS Inliner* — o layout já é inline e as classes `.em-*`
     vivem dentro da media query, que o inliner ignora e pode quebrar;
   - **não** colar o snippet de unsubscribe — já está no código;
   - **não** usar `*|REWARDS|*` — a conta é Essentials (plano pago), o selo
     não é exigido.
4. Rode um **Inbox Preview** e salve como rascunho.

## Links

Todos os destinos apontam para a landing page com o UTM completo:

```
https://bogo.malborcoatings.com/?utm_source=mailchimp&utm_medium=email&utm_campaign=bogo_sept2026&utm_content=automotive
```

São 12 links no DOM (2 botões CTA, logo do header, hero, 3 imagens de produto,
3 títulos de produto, logo Malbor do miolo, badge BOGO) mais 2 dentro dos
comentários condicionais VML do Outlook, além de `mailto:`, `tel:`, `*|UNSUB|*`
e `*|UPDATE_PROFILE|*`. O `utm_content=automotive` é o **único** separador de
público nesta campanha — não há cupom. A náutica usa `utm_content=marine`.

## Verificação

```bash
npm install playwright-core   # uma vez
node check.mjs                # CHROME_PATH=<binario> se o Chromium estiver noutro caminho
```

Cobre: host e os 4 UTMs de cada link (inclusive os do Outlook/VML, que ficam em
comentário e não aparecem no DOM), ausência de `myshopify.com`, `*|UNSUB|*` como
âncora clicável, endereço CAN-SPAM da Malbor, ausência do endereço da YachtPro,
título e preheader, `alt` e `width` em todas as imagens, assets referenciados vs.
presentes, URLs do texto puro, a janela de datas (16–30 de setembro, e nenhum
resquício de 15–29) e as restrições de conteúdo. Roda offline — aborta qualquer
requisição de rede.

## Restrições de conteúdo

Proibido e checado automaticamente: alegação ambiental, comparação com
concorrente, promessa de proteção permanente. A única alegação de durabilidade
autorizada está no card do Max Shield Polymer, no texto exato *"Up to 6 months of
protection on vehicles maintained on a biweekly wash schedule"* — o `check.mjs`
falha se essa frase for alterada.

## Decisões e limitações

- **Endereço do rodapé** está fixo no HTML
  (`4634 Waycross Dr, Coconut Creek, FL 33073`) em vez de `*|LIST:ADDRESS|*`,
  para garantir o endereço da Malbor mesmo que a audience esteja configurada
  de outro jeito. *"Local pickup in Pompano Beach"* é o ponto de retirada, não
  o endereço da empresa — são coisas diferentes, como na peça náutica.
- **Largura 600px.** Geometria reescalada em 0,75 a partir dos 800px do design;
  a tipografia **não** acompanha linearmente e tem piso: corpo 14px, texto
  auxiliar e bullets de produto 12px (subiram dos 11px do design original, que
  já estavam abaixo do mínimo), botões com 48px de altura de toque. Breakpoint
  em `max-width:600px`.
- **Altura dos cards não é fixada.** `height` em `<td>` dimensiona a caixa de
  conteúdo e o padding soma por cima, então o padding e o texto é que definem a
  altura. Os três cards ficam desiguais porque as descrições têm tamanhos
  diferentes — mesmo comportamento da peça náutica.
- **Fotos de produto** ficam na largura nativa da arte (248px) e são exibidas a
  168px; `.em-img-prod` trava em 248px no mobile para não subirem 1,4x e
  borrarem. Elas têm alfa no PNG original e são achatadas sobre `#f4f4f2`, nunca
  sobre branco, senão aparece um retângulo branco dentro da célula do card.
- **Demais assets em 2x exato** da dimensão de exibição. Total de 184 KB contra
  2,0 MB do export original.
- **Logos** eram SVG inline (sem suporte em e-mail) e foram rasterizados em PNG
  a partir dos dados vetoriais do Figma, via `build/` na raiz do repositório.
- **Cantos arredondados** usam `border-radius`; o Outlook desktop ignora e mostra
  cantos retos. Degradação aceitável.
- **Fontes** (Montserrat, Poppins, Work Sans) vêm por `@import` do Google Fonts,
  que só funciona em Apple Mail/iOS. Os demais clientes caem para
  Helvetica/Arial, já declarado em cada `font-family`.

## Pendências antes de enviar

- **Contagem de contatos.** No náutico o briefing dizia 230 e a audience tinha
  590 — a hipótese em aberto é que os 230 fossem um *segmento*, não a audience
  inteira. Se o briefing do automotivo falar em 78 contatos, confirmar na conta
  se é audience ou segmento **antes** de disparar.
- **From e-mail** em domínio autenticado da Malbor.
- **Destino da LP**: `bogo.malborcoatings.com` precisa estar no ar e aceitando
  os UTMs antes do envio.

## Regenerar

```bash
# na raiz do repositório
node    build/make-logos.mjs    # dados vetoriais do Figma -> build/svg/*.svg
python3 build/rasterize.py      # SVG -> PNG (clientes de e-mail não renderizam SVG)
python3 build/make-assets.py    # -> email/automotive/assets/

# preview local
sed 's#https://ASSET-BASE-REPLACE-ME/#assets/#g' index.html > _preview.html
```
