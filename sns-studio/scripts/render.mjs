// 카드/표지를 PNG로 뽑는다.  node render.mjs <spec.json> <출력폴더>
// spec.json = { brand: "zaoseon", size: "card"|"reel"|"square", guides: true|false,
//               cards: [ { id, layout: "L1".."L5", tech: ["T1","T2","T3","T4"],
//                          label, title, sub, lines:[3줄], photo, character,
//                          serial: {chip, no}, cta } ] }
import { chromium } from "playwright";
import { readFileSync, mkdirSync, writeFileSync } from "fs";
import { dirname, resolve, join } from "path";
import { fileURLToPath, pathToFileURL } from "url";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(HERE, "..");
const spec = JSON.parse(readFileSync(process.argv[2], "utf8"));
const outDir = resolve(process.argv[3] || join(ROOT, "out"));
mkdirSync(outDir, { recursive: true });

const brand = JSON.parse(
  readFileSync(join(ROOT, "brands", `${spec.brand}.json`), "utf8"));
const css = readFileSync(join(ROOT, "templates", "layouts.css"), "utf8");
const assetRoot = spec.assetRoot || "/home/claude/zaoseon/sns-images";

const SIZES = { reel: [1080, 1920], card: [1080, 1440], square: [1080, 1080] };
const [W, H] = SIZES[spec.size || "card"];

const fileUrl = (p) => (p ? pathToFileURL(resolve(assetRoot, p)).href : null);
const esc = (s = "") => String(s).replace(/[&<>]/g, (c) =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));

function cardHtml(c) {
  const tech = c.tech || [];
  const photo = fileUrl(c.photo);
  const chara = fileUrl(c.character);
  const cls = [spec.size || "card", c.layout, ...tech,
    c.scrimTop ? "topscrim" : "", c.cta ? "has-cta" : "",
    spec.guides ? "guides" : ""].filter(Boolean).join(" ");

  const stage = c.layout === "L5"
    ? (c.lines || []).map((t, i) =>
        `<div class="t ln${i + 1} ${i === 1 ? "accent" : ""}">${esc(t)}</div>`).join("")
    : [
        c.label ? `<div class="label">${esc(c.label)}</div>` : "",
        c.title ? `<div class="t title">${esc(c.title)}</div>` : "",
        c.sub ? `<div class="t sub">${esc(c.sub)}</div>` : "",
      ].join("");

  return `<div class="canvas ${cls}">
  <div class="layer tint"></div>
  ${photo ? `<div class="layer photo" style="background-image:url('${photo}')"></div>` : ""}
  ${(c.layout === "L3" || c.layout === "L4") ? `<div class="band"></div>` : ""}
  ${tech.includes("T2") ? `<div class="scrim"></div>` : ""}
  ${chara ? `<img class="chara" style="position:absolute;right:0;bottom:0;height:62%;object-fit:contain;object-position:bottom right;z-index:4" src="${chara}">` : ""}
  <div class="fixedbar"><div class="b-name">${esc(brand.fixed.topLeft)}</div>
    <div class="b-tag">${esc(brand.fixed.topRight)}</div></div>
  ${tech.includes("T3") && c.serial ? `<div class="serial">
    <div class="chip">${esc(c.serial.chip)}</div><div class="rule"></div>
    <div class="no">${esc(c.serial.no)}</div></div>` : ""}
  <div class="stage">${stage}</div>
  ${c.cta ? `<div class="cta-pill">${esc(c.cta)}</div>` : ""}
  ${chara && brand.character ? `<div class="ai-notice">${esc(brand.character.notice)}</div>` : ""}
  ${spec.guides ? `<div class="g top"></div><div class="g bottom"></div>` : ""}
</div>`;
}

const vars = Object.entries(brand.color)
  .map(([k, v]) => `--${k.replace(/[A-Z]/g, (m) => "-" + m.toLowerCase())}:${v};`).join("");

const page1 = (c) => `<!doctype html><html lang="ko"><head><meta charset="utf-8">
<style>
@font-face{font-family:"Pretendard";src:url("file://${ROOT}/assets/fonts/PRETENDARD-MEDIUM.OTF");font-weight:500}
@font-face{font-family:"Pretendard";src:url("file://${ROOT}/assets/fonts/PRETENDARD-SEMIBOLD.OTF");font-weight:600}
@font-face{font-family:"Pretendard";src:url("file://${ROOT}/assets/fonts/PRETENDARD-BOLD.OTF");font-weight:700}
@font-face{font-family:"Pretendard";src:url("file://${ROOT}/assets/fonts/PRETENDARD-EXTRABOLD.OTF");font-weight:800}
*{margin:0;padding:0;box-sizing:border-box}html,body{background:#000}
:root{${vars}}
${css}
</style></head><body>${cardHtml(c)}</body></html>`;

const browser = await chromium.launch({
  executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
  args: ["--no-sandbox", "--font-render-hinting=none",
    "--allow-file-access-from-files"],
});
const page = await browser.newPage({ viewport: { width: W, height: H },
  deviceScaleFactor: 1 });

const made = [];
for (const c of spec.cards) {
  // setContent 로 만든 문서는 파일 이미지를 못 불러온다. 파일로 적고 열어야 한다.
  const tmp = join(outDir, `_${c.id}.html`);
  writeFileSync(tmp, page1(c), "utf8");
  await page.goto(pathToFileURL(tmp).href, { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  // 글이 자리를 넘치면 자동으로 줄인다. 넘친 채로 잘리는 일을 막는다.
  await page.evaluate(() => {
    const stage = document.querySelector(".stage");
    if (!stage) return;
    const els = [...stage.querySelectorAll(".t, .label")];
    let guard = 0;
    while (stage.scrollHeight > stage.clientHeight + 1 && guard++ < 60) {
      els.forEach((e) => {
        const fs = parseFloat(getComputedStyle(e).fontSize);
        e.style.fontSize = fs * 0.96 + "px";
      });
    }
  });
  const out = join(outDir, `${c.id}.png`);
  await page.locator(".canvas").screenshot({ path: out });
  made.push(out);
  console.log("만듦:", out);
}
await browser.close();
console.log(`총 ${made.length}장`);
