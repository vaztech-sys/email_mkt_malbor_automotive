#!/usr/bin/env python3
"""Instala as artes do Figma nas peças do Black Friday (ML-41).

O build.py do repositório de origem copia o JPG do Figma como veio. Os exports
chegam com 440-720 KB cada, o que daria ~2,7 MB só de imagem no E2. Aqui eles
são recomprimidos em JPEG progressivo q86 sem subamostragem de croma (4:4:4),
que nesta arte — tipografia branca sobre gradiente escuro — fica visualmente
idêntico ao original e corta o peso em cerca de 4x. Sem 4:4:4 o laranja sobre
preto sangra nas bordas.

As dimensões não mudam: os frames têm 1080 de largura e são exportados em
escala 1,1111 para dar os 1200 que o HTML espera.

Exportar do Figma (arquivo "[MALBOR] Email_mkt", página BLACK FRIDAY, seção
"E-mails Black Friday — imagens (exportar)"):

    fileKey w963vkkHw77eIJtVseKOIH
    email-hero-malbor  163:146      email-boat  163:165
    email-car          163:185      email-interior  163:208
    email-gift         163:234

Uso: python3 build/make-blackfriday-assets.py <dir-com-os-jpg-do-figma>
"""
import sys
from pathlib import Path
from PIL import Image

QUALITY = 86
E2 = Path("email/blackfriday-e2/assets")
E4 = Path("email/blackfriday-e4/assets")
# arquivo -> pastas que o usam
DESTINOS = {
    "email-hero-malbor.jpg": [E2, E4],
    "email-boat.jpg": [E2],
    "email-car.jpg": [E2],
    "email-interior.jpg": [E2],
    "email-gift.jpg": [E2],
}


def main(src_dir):
    src = Path(src_dir)
    faltando = [n for n in DESTINOS if not (src / n).exists()]
    if faltando:
        sys.exit("faltando no diretório de origem: " + ", ".join(faltando))

    total_antes = total_depois = 0
    for nome, pastas in DESTINOS.items():
        origem = src / nome
        im = Image.open(origem).convert("RGB")
        if im.width != 1200:
            sys.exit(f"{nome}: {im.width}px de largura, esperado 1200 "
                     f"(exportar os frames de 1080 em escala 1,1111)")
        antes = origem.stat().st_size
        for pasta in pastas:
            destino = pasta / nome
            im.save(destino, quality=QUALITY, optimize=True,
                    progressive=True, subsampling=0)
            depois = destino.stat().st_size
        total_antes += antes
        total_depois += depois * len(pastas)
        print(f"  {nome:26} {im.size}  {antes//1024:4} KB -> {depois//1024:4} KB"
              f"  ({', '.join(p.parts[1] for p in pastas)})")
    print(f"\ntotal gravado: {total_depois//1024} KB "
          f"(exports do Figma somavam {total_antes//1024} KB)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else sys.exit(__doc__))
