# bhagyank-calculator.online - static HTML version

Plain HTML, CSS and JavaScript. No framework, no build step.

```
public/                      <- everything the website serves
  index.html                 /                        Bhagyank Calculator (English)
  hi.html                    /hi                      भाग्यांक कैलकुलेटर (Hindi)
  moolank-calculator.html    /moolank-calculator
  namank-calculator.html     /namank-calculator
  gemstone-recommendation.html
  about.html, contact.html, privacy-policy.html, terms-and-conditions.html
  bhagyank/1.html ... 9.html /bhagyank/1 ... /bhagyank/9  meaning page for each destiny number
  404.html                   shown for any missing page
  sitemap.xml, robots.txt, ads.txt, _headers (cache rules)
  favicon.ico, favicon.svg, apple-touch-icon.png, icon-192/512.png, site.webmanifest
  assets/style.css           all styles
  assets/app.js              all four calculators + the Bhagyank 1-9 data (English + Hindi)
  images/                    logo, icons, share image, reviewer photo
wrangler.jsonc               Cloudflare config: serves ./public as static files
```

## Editing
- Text on a page: edit that page's `.html` file.
- Header or footer links: they are repeated in every `.html` file - change all of them.
- Results text for Bhagyank / Moolank: the `DATA` object at the top of `assets/app.js`.
- Colours and fonts: the `:root` block at the top of `assets/style.css`.
- New page: copy an existing `.html` file, change the title, description and canonical link,
  then add it to `sitemap.xml`.

## Deploying on Cloudflare (Workers)
Connect this repo in Cloudflare and use:
- Build command: *(leave empty)*
- Deploy command: `npx wrangler deploy`

Cloudflare serves `/hi` from `hi.html` automatically (and redirects `/hi.html` to `/hi`).

## Preview locally
```
npx wrangler dev
```
Then open http://localhost:8787
