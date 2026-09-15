import { writeFileSync, readFileSync, mkdirSync } from "node:fs";

// The Figma export ships the path data as a .ts file whose body is already valid ESM.
// Copy it to .mjs so node can import it, rather than keeping a second copy in the repo.
mkdirSync("build/svg", { recursive: true });
writeFileSync("build/svg/svgpaths.mjs", readFileSync("assets/raw/svg-hh7b012ilf.ts"));
const { default: svgPaths } = await import("../build/svg/svgpaths.mjs");

// MALBOR wordmark + tagline lockup, reproduced from the Figma vector export.
const lockup = (wm, tag, colors) => {
  const { w: wmW, h: wmH, vb: wmVb, paths: wmP } = wm;
  const { w: tgW, h: tgH, vb: tgVb, paths: tgP } = tag;
  const gap = wmH * 0.2341; // 6.949 / 29.678, same ratio as the design
  const totalH = wmH + gap + tgH;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${wmW}" height="${totalH}" viewBox="0 0 ${wmW} ${totalH}" fill="none">
  <g transform="translate(0,0)"><svg width="${wmW}" height="${wmH}" viewBox="${wmVb}" fill="none">
    ${wmP.map((p, i) => `<path d="${svgPaths[p]}" fill="${colors.wm[i]}"/>`).join("\n    ")}
  </svg></g>
  <g transform="translate(0,${wmH + gap})"><svg width="${tgW}" height="${tgH}" viewBox="${tgVb}" fill="none">
    ${tgP.map((p) => `<path d="${svgPaths[p]}" fill="${colors.tag}"/>`).join("\n    ")}
  </svg></g>
</svg>`;
};

const wmSmall = {
  w: 152, h: 29.6778, vb: "0 0 152 29.6778",
  paths: ["p17d66a80","p3ba5500","p390a3000","p11f41d80","p1be0dc00","p3c8f9800","p61ba700","p32b6ecf0","p12f88300"],
};
const tagSmall = {
  w: 68.6171, h: 8.33998, vb: "0 0 68.6171 8.33998",
  paths: ["pca6d00","p1d072080","p67ecc00","p13898f80","pa334c00","p2037af80","p8d59d00","p33ff21c0"],
};
const wmLarge = {
  w: 175, h: 34.1685, vb: "0 0 175 34.1685",
  paths: ["p3c147500","p12452b00","p3f8a3800","p3864bd40","p36f33800","p2874df00","p260be040","p98e1a80","p3ccdf900"],
};
const tagLarge = {
  w: 79, h: 9.60196, vb: "0 0 79 9.60196",
  paths: ["p3c7d1400","pfae8c00","p244bde00","p3e56e300","pf73ae00","p2f72ba80","p32e8da80","p15c61000"],
};

const light = { wm: ["white","white","#F4F4F2","#F4F4F2","#F4F4F2","#EA560D","#EA560D","#F4F4F2","#EF7D00"], tag: "#FFF7ED" };
const dark  = { wm: ["#24211E","#24211E","#12100C","#12100C","#12100C","#EA560D","#EA560D","#12100C","#EF7D00"], tag: "#24211E" };

writeFileSync("build/svg/logo-light.svg", lockup(wmSmall, tagSmall, light));
writeFileSync("build/svg/logo-dark.svg", lockup(wmSmall, tagSmall, dark));
writeFileSync("build/svg/logo-footer.svg", lockup(wmLarge, tagLarge, light));
writeFileSync("build/svg/check.svg", `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="${svgPaths.p1e92e80}" fill="#EA560D"/></svg>`);
console.log("svg written");
