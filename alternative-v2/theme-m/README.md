# ITD2027/M — the SELCA-style look

Live: https://ariongj.github.io/ITD2027/M/

The same 54 pages as ITD2027 (SQ / EN / DE, same text, same links, same forms and measurement), dressed in
the design language of the SELCA site:

- **Type:** Fraunces for headlines, with one word in red italic on the home hero (`punën` / `work` / `Arbeit`);
  Manrope for text. Both are self-hosted variable fonts under the SIL Open Font License (`fonts/*-OFL.txt`),
  the same files the SELCA site uses.
- **Colour:** cream paper `#f7f3ee`, ink `#1c1a17`, wine red `#a51d24` (darker `#86161c` on hover), sand `#efe7dc`.
  Product pages keep their own colours (Kraken blue, AURA violet, ITD Labs green).
- **Header:** a dark top bar (phone, hours and place, email), then a light header with a dark-text version of the
  logo (`logo-ink.png`: the white letters of `logo-original.png` turned to ink, the shield unchanged). On the home
  page the header lies over the picture in white.
- **Home:** a full-width hero slideshow (IT Department, Kraken OS, Creative studio): picture, pill label, large serif
  headline, two pill buttons, a `01 / 03` counter, 10-second progress bars, arrows and a pause button. It is the
  same `slider.js` as ITD2027, so pause on hover, keyboard focus and touch, reduced motion and the no-JavaScript
  fallback behave the same. Below it, a floating white bar with four facts (30-minute meeting, a clear plan,
  IT support from €99 a month, three languages), then numbered service rows, a dark band for the work examples,
  partners, prices and the closing box.
- **Pictures:** made from ITD's own material — the red light texture, the real Kraken OS dashboard, the NEXUS and
  HYPERLINK brandbooks. No stock photography. To use real photos, replace `hero-*.webp` (1920 × 1080) and keep the names.

Files: `../theme_m.py` (top bar, header logo, hero, facts bar), `m.css` (all styling), `fonts/`, `logo-ink.png`,
`hero-itd.webp`, `hero-kraken.webp`, `hero-creative.webp`.
