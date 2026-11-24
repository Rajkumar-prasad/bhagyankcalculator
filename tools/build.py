#!/usr/bin/env python3
"""Site generator for bhagyank-calculator.online.

Usage (from the repo root):  python3 tools/build.py
Writes every page into public/. Blog posts live in tools/posts/*.json (see tools/CONTENT_GUIDE.md).
Images, icons, _headers and other hand-made files in public/ are left alone.
"""
import html
import json
import re
import shutil
import sys
from pathlib import Path

HERE_ = Path(__file__).resolve().parent
OUT = HERE_.parent
PUB = OUT / "public"
HERE = Path(__file__).resolve().parent
SITE = "https://www.bhagyank-calculator.online"
GTM_ID = "GTM-WFC7XXW5"
ADSENSE = "ca-pub-7904206080765704"

data = json.loads((HERE / "data.json").read_text())
EN, HI = data["en"], data["hi"]

e = html.escape


FAQ_EN = [tuple(x) for x in data["faq_en"]]
FAQ_HI = [tuple(x) for x in data["faq_hi"]]
assert len(FAQ_EN) == 7 and len(FAQ_HI) == 7, (len(FAQ_EN), len(FAQ_HI))

AUTHOR = {
    "name": "Ananya Sharma",
    "name_hi": "अनन्या शर्मा",
    "image": "/images/ananya-sharma.jpg",
    "url": "/author/ananya-sharma",
    "short": ("Ananya Sharma (अनन्या शर्मा) is the pen name behind the numerology guides on Bhagyank Calculator. "
              "She explains how to calculate your Bhagyank and Mulank from your date of birth and what each number "
              "traditionally represents in numerology."),
}

AUTHOR_BIO = {
    "en": [
        "Ananya Sharma (अनन्या शर्मा) is the pen name behind the numerology guides on Bhagyank Calculator. "
        "She writes about Bhagyank (destiny number), Mulank (birth number) and Namank (name number), and explains "
        "what each number from 1 to 9 traditionally represents in Vedic numerology - its ruling planet, nature, "
        "lucky colors, lucky days and gemstone.",
        "Her guides show the full calculation step by step, with worked date-of-birth examples, so you can check "
        "every result yourself instead of taking a number on trust. She writes in both English and Hindi, so the "
        "same method is easy to follow in either language.",
    ],
    "hi": [
        "अनन्या शर्मा (Ananya Sharma) भाग्यांक कैलकुलेटर पर अंक ज्योतिष गाइड लिखने वाली लेखिका का उपनाम है। "
        "वे जन्मतिथि से भाग्यांक और मूलांक निकालने का तरीका समझाती हैं, और बताती हैं कि पारंपरिक वैदिक अंक ज्योतिष में "
        "1 से 9 तक हर अंक का क्या अर्थ है - उसका स्वामी ग्रह, स्वभाव, शुभ रंग, शुभ दिन और रत्न।",
        "उनकी गाइड में हर गणना उदाहरण के साथ चरण-दर-चरण दिखाई जाती है, ताकि आप अपना परिणाम खुद जाँच सकें। "
        "वे हिंदी और अंग्रेज़ी दोनों भाषाओं में लिखती हैं।",
    ],
}


def author_schema():
    return {"@type": "Person", "@id": f"{SITE}{AUTHOR['url']}#person", "name": AUTHOR["name"],
            "alternateName": AUTHOR["name_hi"], "url": SITE + AUTHOR["url"], "image": SITE + AUTHOR["image"],
            "description": AUTHOR["short"], "knowsAbout": ["Numerology", "Vedic numerology", "Bhagyank", "Mulank", "Namank"],
            "knowsLanguage": ["en", "hi"], "worksFor": {"@id": f"{SITE}/#organization"}}

SPARKLE = (
    '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2l1.9 5.6L19.5 9.5l-5.6 1.9L12 17l-1.9-5.6'
    'L4.5 9.5l5.6-1.9L12 2zM19 14l.9 2.6 2.6.9-2.6.9L19 21l-.9-2.6-2.6-.9 2.6-.9L19 14z" fill="currentColor"/></svg>'
)
GEM = (
    '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3h12l4 6-10 12L2 9l4-6zm.9 2L4.6 8.5h4.2L10 5H6.9z'
    'm6.1 0l1.2 3.5h4.2L17.1 5H13zm-3 0L8.8 8.5h6.4L14 5h-4zM4.9 10.5l6.1 7.4-2.5-7.4H4.9zm5.7 0L12 15l1.4-4.5h-2.8zm4.9 0'
    'L13 17.9l6.1-7.4h-3.6z" fill="currentColor"/></svg>'
)

NAV = [
    ("/", "Bhagyank Calculator"),
    ("/moolank-calculator", "Moolank Calculator"),
    ("/namank-calculator", "Namank Calculator"),
    ("/lo-shu-grid-calculator", "Lo Shu Grid"),
    ("/blog", "Blog"),
    ("/about", "About Us"),
]
FOOTER = [
    ("/", "Bhagyank Calculator"),
    ("/moolank-calculator", "Moolank Calculator"),
    ("/namank-calculator", "Namank Calculator"),
    ("/about", "About Us"),
    ("/contact", "Contact Us"),
    ("/gemstone-recommendation", "Gemstone Guide"),
    ("/lo-shu-grid-calculator", "Lo Shu Grid Calculator"),
    ("/hi", "भाग्यांक कैलकुलेटर (हिंदी)"),
    ("/author/ananya-sharma", "Our Author"),
    ("/blog", "Blog"),
    ("/privacy-policy", "Privacy Policy"),
    ("/terms-and-conditions", "Terms &amp; Conditions"),
]


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


def page(*, path, title, description, body, lang="en", og_title=None, og_desc=None,
         hreflang=False, schema=None, noindex=False, scripts=True):
    url = SITE + path if path != "/" else SITE
    alt = ""
    if hreflang:
        en_p, hi_p = ("/", "/hi") if hreflang is True else hreflang
        en_u = SITE if en_p == "/" else SITE + en_p
        alt = (f'<link rel="alternate" hreflang="en" href="{en_u}">\n'
               f'<link rel="alternate" hreflang="hi" href="{SITE}{hi_p}">\n'
               f'<link rel="alternate" hreflang="x-default" href="{en_u}">\n')
    og_title = og_title or title
    og_desc = og_desc or description
    locale = "hi_IN" if lang == "hi" else "en_IN"
    robots = "noindex, follow" if noindex else "index, follow"
    head = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
{alt}<meta name="theme-color" content="#1a1636">
<meta name="color-scheme" content="dark">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(og_title)}">
<meta property="og:description" content="{e(og_desc)}">
<meta property="og:site_name" content="Bhagyank Calculator">
<meta property="og:locale" content="{locale}">
<meta property="og:image" content="{SITE}/images/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(og_title)}">
<meta name="twitter:description" content="{e(og_desc)}">
<meta name="twitter:image" content="{SITE}/images/og-image.png">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Marcellus&amp;family=Poppins:wght@300;400;500;600;700&amp;display=swap">
<link rel="stylesheet" href="/assets/style.css">
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{GTM_ID}');</script>
<!-- End Google Tag Manager -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE}" crossorigin="anonymous"></script>
{jsonld(schema) if schema else ""}
{'<script src="/assets/app.js" defer></script>' if scripts else ""}
</head>
<body>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" style="display:none;visibility:hidden" title="Google Tag Manager"></iframe></noscript>
"""
    return head + header() + body + footer() + "\n</body>\n</html>\n"


def header():
    links = "".join(f'<a href="{h}">{t}</a>' for h, t in NAV)
    return f"""<header class="site-header">
  <div class="container header-inner">
    <a href="/" class="logo"><span class="logo-mark">{SPARKLE}</span><span>Bhagyank<span class="gold">Calculator</span></span></a>
    <nav class="nav-desktop" aria-label="Primary">{links}</nav>
    <details class="nav-mobile">
      <summary aria-label="Open navigation menu"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></summary>
      <nav aria-label="Mobile primary">{links}</nav>
    </details>
  </div>
</header>
"""


def footer():
    links = "".join(f'<a href="{h}">{t}</a>' for h, t in FOOTER)
    nums = "".join(f'<a href="/bhagyank/{n}" aria-label="Bhagyank {n} meaning">{n}</a>' for n in range(1, 10))
    return f"""<footer class="site-footer">
  <div class="container footer-inner">
    <a href="/" class="footer-logo">{SPARKLE} Bhagyank Calculator</a>
    <nav aria-label="Footer" class="footer-nav">{links}</nav>
    <nav aria-label="Bhagyank meanings" class="footer-nums"><span>Bhagyank meanings:</span>{nums}</nav>
    <p class="small">&copy; <span data-year>2026</span> Bhagyank Calculator. For informational purposes only.</p>
    <p class="small">Website developed by Raj Prasad.</p>
  </div>
</footer>"""


def hero(badge, h1, intro, extra="", icon=SPARKLE, stars=False):
    cls = "hero stars" if stars else "hero"
    return f"""<section id="calculator" class="{cls}">
  <div class="container hero-inner">
    <div class="hero-text">
      <span class="badge">{icon} {badge}</span>
      <h1>{h1}</h1>
      <p class="lead">{intro}</p>
      {extra}
    </div>
"""


def reviewed_by(lang="en"):
    """Author box shown at the end of the Bhagyank pages."""
    if lang == "hi":
        label, name, link = "लेखिका", "अनन्या शर्मा (Ananya Sharma)", "लेखिका के बारे में और जानें"
        alt = "अनन्या शर्मा, भाग्यांक कैलकुलेटर की लेखिका"
    else:
        label, name, link = "Written by", "Ananya Sharma (अनन्या शर्मा)", "More about the author"
        alt = "Ananya Sharma, author of the Bhagyank Calculator numerology guides"
    paras = "".join(f'<p class="muted small">{e(x)}</p>' for x in AUTHOR_BIO[lang])
    return f"""<section class="container narrow" aria-labelledby="author-box">
  <div class="reviewer">
    <img src="{AUTHOR['image']}" alt="{alt}" width="96" height="96" loading="lazy">
    <div>
      <p class="eyebrow">{label}</p>
      <h2 id="author-box" class="h-card">{name}</h2>
      {paras}
      <a href="{AUTHOR['url']}" class="link small">{link}</a>
    </div>
  </div>
</section>
"""


def faq_block(faqs):
    items = "".join(
        f'<details class="faq"><summary><span>{e(q)}</span><span class="plus" aria-hidden="true">+</span></summary>'
        f'<p>{e(a)}</p></details>' for q, a in faqs)
    return f'<div class="faq-list">{items}</div>'


def bhagyank_schema(path, lang, name, description, faqs):
    url = SITE + path if path != "/" else SITE
    crumbs = [{"@type": "ListItem", "position": 1, "name": "Bhagyank Calculator", "item": SITE}]
    if path != "/":
        crumbs.append({"@type": "ListItem", "position": 2, "name": name, "item": url})
    return {
        "@context": "https://schema.org",
        "@graph": [
            author_schema(),
            {"@type": "Organization", "@id": f"{SITE}/#organization", "name": "Bhagyank Calculator",
             "url": SITE, "logo": f"{SITE}/icon-512.png"},
            {"@type": "WebSite", "@id": f"{SITE}/#website", "url": SITE, "name": "Bhagyank Calculator",
             "inLanguage": ["en", "hi"], "publisher": {"@id": f"{SITE}/#organization"}},
            {"@type": "WebPage", "@id": f"{url}#webpage", "url": url, "name": name, "description": description,
             "inLanguage": lang, "isPartOf": {"@id": f"{SITE}/#website"},
             "author": {"@id": f"{SITE}{AUTHOR['url']}#person"}, "dateModified": TODAY.isoformat(),
             "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": crumbs}},
            {"@type": "WebApplication", "name": name, "url": url, "applicationCategory": "LifestyleApplication",
             "operatingSystem": "Web", "inLanguage": lang, "description": description,
             "offers": {"@type": "Offer", "price": "0", "priceCurrency": "INR"},
             "publisher": {"@id": f"{SITE}/#organization"}},
            {"@type": "FAQPage", "@id": f"{url}#faq", "inLanguage": lang,
             "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                            for q, a in faqs]},
        ],
    }


def bhagyank_form(lang):
    t = {
        "en": dict(h="Enter Your Date of Birth", d="Day", m="Month", y="Year", b="Calculate My Bhagyank",
                   n="100% free · No sign-up · Instant result", et="Your Destiny Awaits",
                   ex='Select your date of birth and tap “Calculate My Bhagyank” to instantly reveal your destiny number, ruling planet, strengths and lucky traits.'),
        "hi": dict(h="अपनी जन्मतिथि चुनें", d="दिन", m="महीना", y="वर्ष", b="मेरा भाग्यांक निकालें",
                   n="100% मुफ़्त · कोई साइन-अप नहीं · तुरंत परिणाम", et="आपका भाग्य आपका इंतज़ार कर रहा है",
                   ex="अपनी जन्मतिथि चुनें और “मेरा भाग्यांक निकालें” दबाएँ। आपका भाग्यांक, स्वामी ग्रह, खूबियाँ और शुभ रंग तुरंत दिखेंगे।"),
    }[lang]
    return f"""    <div class="calc-grid" data-calc="bhagyank" data-lang="{lang}">
      <form class="card calc-form" novalidate>
        <div class="form-title">{SPARKLE}<h2>{t['h']}</h2></div>
        <div class="dob-row">
          <label>{t['d']}<select name="day" data-dob="day"><option value="">DD</option></select></label>
          <label>{t['m']}<select name="month" data-dob="month"><option value="">MM</option></select></label>
          <label>{t['y']}<select name="year" data-dob="year"><option value="">YYYY</option></select></label>
        </div>
        <p class="error" role="alert" hidden></p>
        <button type="submit" class="btn">{t['b']}</button>
        <p class="note">{t['n']}</p>
      </form>
      <div class="result" id="bhagyank-result" aria-live="polite">
        <div class="card empty">
          <div class="empty-icon">{SPARKLE}</div>
          <h3>{t['et']}</h3>
          <p>{t['ex']}</p>
        </div>
      </div>
    </div>
  </div>
</section>
"""


def section(id_, title, inner):
    return f'<section id="{id_}" class="content-section"><h2>{title}</h2>{inner}</section>'


def meanings_grid(lang):
    cards = []
    for n in range(1, 10):
        if lang == "en":
            i = EN[str(n)]
            cards.append(
                f'<article class="card mini"><div class="num-row"><span class="num">{n}</span><div>'
                f'<h3>Bhagyank {n} - {e(i["title"])}</h3><p class="xs muted">Ruled by {e(i["planet"])} ({e(i["planetHindi"])})</p>'
                f'</div></div><p class="small muted">{e(i["summary"])}</p>'
                f'<p class="xs"><span class="gold">Lucky colors:</span> <span class="muted">{e(", ".join(i["luckyColors"]))}</span></p>'
                f'<p class="xs"><a class="link" href="/bhagyank/{n}">Read the full Bhagyank {n} meaning</a></p></article>')
        else:
            i = HI[str(n)]
            cards.append(
                f'<article class="card mini"><div class="num-row"><span class="num">{n}</span><div>'
                f'<h3>भाग्यांक {n} - {e(i["title"])}</h3><p class="xs muted">स्वामी ग्रह: {e(i["planet"])}</p>'
                f'</div></div><p class="small muted">{e(i["summary"])}</p>'
                f'<p class="xs"><span class="gold">उपयुक्त करियर:</span> <span class="muted">{e(i["career"])}</span></p>'
                f'<p class="xs"><a class="link" href="/hi/bhagyank/{n}">भाग्यांक {n} का पूरा अर्थ पढ़ें</a></p></article>')
    return f'<div class="grid-2">{"".join(cards)}</div>'


def compare_table(rows, heads):
    th = "".join(f"<th>{h}</th>" for h in heads)
    trs = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in rows)
    return f'<div class="table-wrap"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


# ---------------------------------------------------------------- pages

def home():
    desc = ("Free Bhagyank Calculator (Destiny Number / Bhagya Ank) based on your date of birth. Instantly find your "
            "Bhagyank in Vedic numerology, its ruling planet, meaning, lucky traits and how it shapes your life path.")
    extra = ('<p class="small muted">हिंदी में पढ़ें: <a href="/hi" hreflang="hi" lang="hi" class="link">भाग्यांक कैलकुलेटर</a></p>')
    content = f"""<div class="container narrow content">
{section("what-is-bhagyank", "What is Bhagyank (Destiny Number)?", '''
<p><strong>Bhagyank</strong> - also known as the <strong>Destiny Number</strong> or <strong>Bhagya Ank</strong> - is one of the most important numbers in Vedic numerology. It is derived from your complete date of birth and reveals the path your life is destined to follow: your purpose, opportunities, lessons and the direction in which your journey naturally unfolds.</p>
<p>While your personality can be shaped by many factors, your Bhagyank acts like a hidden blueprint of your karma. Understanding it helps you make better decisions about your career, relationships and personal growth - because you start moving <em>with</em> your destiny instead of against it.</p>''')}
{section("how-to-calculate", "How to Calculate Your Bhagyank", '''
<p>Calculating your Bhagyank is simple. You add up <strong>every digit</strong> of your full date of birth (day + month + year) and then reduce the total to a single digit between 1 and 9.</p>
<div class="card example"><p class="gold strong">Example: Date of Birth = 15 August 1990</p><ol>
<li>Write the full date in numbers: 1, 5, 0, 8, 1, 9, 9, 0</li>
<li>Add all digits: 1 + 5 + 0 + 8 + 1 + 9 + 9 + 0 = 33</li>
<li>Reduce to a single digit: 3 + 3 = 6</li>
<li><strong>Bhagyank = 6</strong></li></ol></div>
<p>You don't have to do the math by hand - our <a href="#calculator" class="link">Bhagyank Calculator</a> above does it instantly and also tells you your ruling planet and traits. You can also compare it with our <a href="/moolank-calculator" class="link">Moolank Calculator</a> or explore our <a href="/gemstone-recommendation" class="link">free gemstone recommendation</a> for traditional numerology guidance.</p>''')}
{section("mulank-vs-bhagyank", "Mulank vs Bhagyank: What's the Difference?",
         "<p>People often confuse Mulank and Bhagyank. Both come from your birth date, but they describe different things:</p>"
         + compare_table([("Based on", "Only the day of birth", "The full date of birth"),
                          ("Represents", "Core nature &amp; personality", "Life path &amp; destiny"),
                          ("Answers", "Who am I?", "Where is my life heading?")],
                         ["Aspect", "Mulank (Radical Number)", "Bhagyank (Destiny Number)"])
         + "<p>Read together, Mulank and Bhagyank give a complete picture of your character and your fate - which is why serious numerology readings always consider both.</p>")}
{section("meanings", "Bhagyank 1 to 9: Meanings &amp; Ruling Planets",
         "<p>Each Bhagyank is governed by a planet that colours your destiny. Here is a quick guide to all nine destiny numbers in Vedic numerology.</p>" + meanings_grid("en"))}
{section("bhagyank-chart", "Bhagyank Chart: Planet, Lucky Color, Day and Gemstone", chart_table())}
{section("why-it-matters", "Why Your Bhagyank Matters", '''
<p>Your destiny number influences the big themes of your life - the type of work you thrive in, the relationships that suit you, and the challenges you are meant to grow through. When you align your daily choices with your Bhagyank's energy (through lucky colors, favourable days and suitable careers), life tends to flow more smoothly.</p>
<p>Think of your Bhagyank as a compass rather than a cage. It doesn't decide everything for you, but it points you toward the direction where your natural talents and karma can shine the brightest.</p>''')}
{section("faq", "Frequently Asked Questions", faq_block(FAQ_EN))}
<p class="card disclaimer">Disclaimer: This Bhagyank Calculator and its content are provided for informational and entertainment purposes based on traditional Vedic numerology. They are not a substitute for professional advice.</p>
</div>"""
    body = ("<main>" + hero("Free Vedic Numerology Tool", "Bhagyank Calculator - Find Your Destiny Number",
                            'Discover your <strong>Bhagyank (Destiny Number)</strong> instantly from your date of birth. '
                            'Learn your ruling planet, personality traits, lucky colors and the life path written in your numbers.',
                            extra, stars=True)
            + bhagyank_form("en") + content + reviewed_by("en") + updated_line("en") + "</main>")
    return page(path="/", title="Bhagyank Calculator - Free Destiny Number by Date of Birth",
                description=desc, body=body, hreflang=True,
                og_title="Bhagyank Calculator - Find Your Destiny Number Free",
                og_desc="Calculate your Bhagyank (Destiny Number) from your date of birth and discover your ruling planet, personality and life path in Vedic numerology.",
                schema=bhagyank_schema("/", "en", "Bhagyank Calculator",
                                       "Free Bhagyank (Destiny Number) Calculator based on Vedic numerology and your date of birth.",
                                       FAQ_EN))


def hindi():
    desc = ("मुफ़्त भाग्यांक कैलकुलेटर: अपनी जन्मतिथि से तुरंत भाग्यांक (डेस्टिनी नंबर) निकालें। जानें भाग्यांक कैसे निकालें, "
            "भाग्यांक 1 से 9 का अर्थ, स्वामी ग्रह, शुभ रंग और शुभ दिन।")
    extra = '<p class="small muted" lang="en">Read in English: <a href="/" hreflang="en" class="link">Bhagyank Calculator</a></p>'
    content = f"""<div class="container narrow content">
{section("bhagyank-kya-hai", "भाग्यांक क्या है?", '''
<p><strong>भाग्यांक</strong> (Bhagyank), जिसे <strong>डेस्टिनी नंबर</strong> या <strong>भाग्य अंक</strong> भी कहते हैं, वैदिक अंक ज्योतिष के सबसे महत्वपूर्ण अंकों में से एक है। यह आपकी पूरी जन्मतिथि से निकाला जाता है और बताता है कि आपका जीवन किस दिशा में आगे बढ़ेगा - आपका उद्देश्य, अवसर, सीख और संघर्ष।</p>
<p>आपका स्वभाव कई चीज़ों से बनता है, लेकिन भाग्यांक आपके कर्म का एक छिपा हुआ नक्शा है। इसे समझकर आप करियर, रिश्तों और व्यक्तिगत विकास से जुड़े फ़ैसले बेहतर तरीके से ले सकते हैं।</p>''')}
{section("bhagyank-kaise-nikale", "भाग्यांक कैसे निकालें?", '''
<p>भाग्यांक निकालना बहुत आसान है। अपनी पूरी जन्मतिथि (दिन + महीना + वर्ष) के <strong>हर अंक</strong> को जोड़ें और योग को 1 से 9 के बीच एक अंक तक घटाएँ।</p>
<div class="card example"><p class="gold strong">उदाहरण: जन्मतिथि = 15 अगस्त 1990</p><ol>
<li>जन्मतिथि के अंक लिखें: 1, 5, 0, 8, 1, 9, 9, 0</li>
<li>सभी अंक जोड़ें: 1 + 5 + 0 + 8 + 1 + 9 + 9 + 0 = 33</li>
<li>एक अंक बनाएँ: 3 + 3 = 6</li>
<li><strong>भाग्यांक = 6</strong></li></ol></div>
<p>आपको यह गणना हाथ से करने की ज़रूरत नहीं है - ऊपर दिया गया <a href="#calculator" class="link">भाग्यांक कैलकुलेटर</a> तुरंत आपका भाग्यांक, स्वामी ग्रह और शुभ रंग बता देता है। आप हमारे <a href="/moolank-calculator" class="link">मूलांक कैलकुलेटर</a> से अपना मूलांक भी निकाल सकते हैं, या <a href="/gemstone-recommendation" class="link">रत्न सुझाव (Gemstone Guide)</a> देख सकते हैं।</p>''')}
{section("mulank-vs-bhagyank", "मूलांक और भाग्यांक में अंतर",
         "<p>लोग अक्सर मूलांक और भाग्यांक को एक ही समझ लेते हैं। दोनों जन्मतिथि से निकलते हैं, लेकिन अलग-अलग बातें बताते हैं:</p>"
         + compare_table([("किससे निकलता है", "केवल जन्म का दिन", "पूरी जन्मतिथि"),
                          ("क्या दर्शाता है", "स्वभाव और व्यक्तित्व", "जीवन पथ और भाग्य"),
                          ("किस सवाल का जवाब", "मैं कौन हूँ?", "मेरा जीवन किस दिशा में जा रहा है?")],
                         ["पहलू", "मूलांक", "भाग्यांक"])
         + "<p>मूलांक और भाग्यांक को साथ में पढ़ने से आपके चरित्र और भाग्य की पूरी तस्वीर मिलती है, इसलिए हर अच्छी अंक ज्योतिष रीडिंग में दोनों को देखा जाता है।</p>")}
{section("bhagyank-arth", "भाग्यांक 1 से 9: अर्थ और स्वामी ग्रह",
         "<p>हर भाग्यांक का एक स्वामी ग्रह होता है जो आपके भाग्य को प्रभावित करता है। नीचे सभी नौ भाग्यांकों का संक्षिप्त परिचय है।</p>" + meanings_grid("hi"))}
{section("faq", "अक्सर पूछे जाने वाले सवाल", faq_block(FAQ_HI))}
<p class="card disclaimer">अस्वीकरण: यह भाग्यांक कैलकुलेटर और इसकी सामग्री पारंपरिक वैदिक अंक ज्योतिष पर आधारित है और केवल जानकारी व मनोरंजन के लिए है। इसे किसी पेशेवर सलाह का विकल्प न मानें।</p>
</div>"""
    body = ('<main lang="hi">' + hero("मुफ़्त वैदिक अंक ज्योतिष टूल", "भाग्यांक कैलकुलेटर - जन्मतिथि से अपना भाग्यांक जानें",
                                     'अपनी जन्मतिथि से तुरंत अपना <strong>भाग्यांक (Destiny Number)</strong> निकालें। जानें आपका स्वामी ग्रह, स्वभाव, खूबियाँ, शुभ रंग और जीवन पथ।',
                                     extra, stars=True)
            + bhagyank_form("hi") + content + reviewed_by("hi") + updated_line("hi") + "</main>")
    return page(path="/hi", lang="hi",
                title="भाग्यांक कैलकुलेटर - जन्मतिथि से भाग्यांक कैसे निकालें (Bhagyank Calculator in Hindi)",
                description=desc, body=body, hreflang=True,
                og_title="भाग्यांक कैलकुलेटर - जन्मतिथि से अपना भाग्यांक जानें",
                schema=bhagyank_schema("/hi", "hi", "भाग्यांक कैलकुलेटर", desc, FAQ_HI))


def moolank():
    meanings = [("1", "Sun", "Independent, confident and born to lead."), ("2", "Moon", "Sensitive, intuitive and naturally diplomatic."),
                ("3", "Jupiter", "Optimistic, expressive and drawn to knowledge."), ("4", "Rahu", "Practical, unconventional and hardworking."),
                ("5", "Mercury", "Adaptable, clever and freedom-loving."), ("6", "Venus", "Caring, artistic and harmony-seeking."),
                ("7", "Ketu", "Thoughtful, spiritual and analytical."), ("8", "Saturn", "Disciplined, responsible and resilient."),
                ("9", "Mars", "Courageous, energetic and compassionate.")]
    cards = "".join(f'<div class="card mini"><p class="h-num">{n} <span class="small muted">- {p}</span></p><p class="small muted">{m}</p></div>'
                    for n, p, m in meanings)
    calc = f"""    <div class="calc-grid" data-calc="moolank">
      <form class="card calc-form" novalidate>
        <div class="form-title">{SPARKLE}<h2>Enter Your Birth Date</h2></div>
        <div class="dob-row two">
          <label>Day<select name="day" data-dob="day"><option value="">DD</option></select></label>
          <label>Month<select name="month" data-dob="month"><option value="">MM</option></select></label>
        </div>
        <p class="error" role="alert" hidden></p>
        <button type="submit" class="btn">Calculate My Moolank</button>
        <p class="note">100% free · No sign-up · Instant result</p>
      </form>
      <div class="result" id="moolank-result" aria-live="polite">
        <div class="card empty"><div class="empty-icon">{SPARKLE}</div><h3>Discover Your Moolank</h3>
        <p>Enter the day you were born to reveal your birth number and its numerology meaning.</p></div>
      </div>
    </div>
  </div>
</section>
"""
    content = f"""<section class="band"><div class="container mid">
<p class="eyebrow">Moolank guide</p>
<h2>What is Moolank in numerology?</h2>
<p class="muted">Moolank, also called the Birth Number or Radical Number, is the single digit derived from the day of your birth. It describes your natural personality, habits, instincts and the way you respond to life.</p>
<div class="grid-2 gap-lg">
<article><h3>How to calculate Moolank</h3><p class="muted">Only your birth day is used. If you were born on the 7th, your Moolank is 7. If you were born on the 28th, add 2 + 8 = 10, then 1 + 0 = 1. Your Moolank is therefore 1.</p></article>
<article><h3>Moolank and Bhagyank</h3><p class="muted">Moolank reflects your inner nature and day-to-day personality. Bhagyank uses your complete date of birth to describe your broader life direction. Reading both together offers a more complete numerology profile. After finding your Moolank, use our <a href="/" class="link">Bhagyank Calculator</a> to calculate your destiny number, then visit our <a href="/gemstone-recommendation" class="link">free gemstone recommendation page</a> for a traditional gemstone guide.</p></article>
</div>
<h3 class="mt-lg">Moolank meanings from 1 to 9</h3>
<div class="grid-3">{cards}</div>
<p class="small muted mt-lg">Numerology is a reflective and spiritual practice. Use your Moolank as a tool for self-understanding and personal reflection, not as a substitute for professional advice.</p>
</div></section>"""
    body = ("<main>" + hero("Free Vedic Numerology Tool", "Moolank (Mulank) Calculator - Find Your Birth Number",
                            "Calculate your Moolank from the day you were born and discover your natural personality, ruling planet, strengths and ideal career direction.")
            + calc + content + "</main>")
    return page(path="/moolank-calculator", title="Moolank (Mulank) Calculator - Find Your Birth Number by Date",
                description="Free Moolank (Mulank) Calculator: find your Birth Number from your date of birth and understand its Vedic numerology meaning, ruling planet and traits.",
                body=body)


def namank():
    nums = [("1", "Leadership and initiative"), ("2", "Partnership and intuition"), ("3", "Creativity and expression"),
            ("4", "Structure and reliability"), ("5", "Freedom and adaptability"), ("6", "Care and harmony"),
            ("7", "Wisdom and introspection"), ("8", "Ambition and management"), ("9", "Compassion and courage")]
    cards = "".join(f'<div class="card mini"><p class="h-num">{n}</p><p class="small muted">{m}</p></div>' for n, m in nums)
    calc = f"""    <section class="card tool" aria-label="Namank calculator" data-calc="namank">
      <div class="tool-head">
        <div class="tool-icon">{SPARKLE}</div>
        <h2>Calculate Your Namank</h2>
        <p class="muted">Enter your full name in English to find its traditional numerology number.</p>
        <form class="tool-form" novalidate>
          <label for="namank-name">Full name</label>
          <input id="namank-name" name="name" type="text" placeholder="Enter your name" autocomplete="name">
          <button type="submit" class="btn" disabled>{SPARKLE} Calculate My Namank</button>
        </form>
      </div>
      <div class="tool-result" aria-live="polite"></div>
    </section>
  </div>
</section>
"""
    content = f"""<div class="container narrow content">
<div><p class="eyebrow">Namank numerology guide</p><h2>What is Namank?</h2><p class="muted">Namank, also called Name Number, is the single digit calculated from the letters in your name. In traditional numerology, your name is connected with your public identity, communication style and the way others experience your energy. This free Namank Calculator converts each English letter into a number and reduces the total to 1-9.</p></div>
<div class="grid-2 gap-lg">
<article><h3>How to calculate Namank</h3><p class="muted">Write your commonly used full name, assign a value to each letter using the Chaldean-style chart, add the values and reduce the total to a single digit. Use the result as a reflective numerology insight rather than a fixed prediction.</p></article>
<article><h3>Namank, Moolank and Bhagyank</h3><p class="muted">Namank is based on your name, while Moolank comes from your birth day and Bhagyank uses your complete date of birth. For a broader reading, try our <a href="/moolank-calculator" class="link">Moolank Calculator</a> and <a href="/" class="link">Bhagyank Calculator</a>, then explore the <a href="/gemstone-recommendation" class="link">free gemstone recommendation</a> guide.</p></article>
</div>
<div><h2>Namank numbers 1 to 9</h2><div class="grid-3">{cards}</div></div>
<p class="small muted">Name numerology is a traditional spiritual practice for self-reflection. Results can vary by numerology system and spelling, so use this Namank reading as educational guidance and consider your lived experience.</p>
</div>"""
    body = ("<main>" + hero("Free Name Numerology Tool", "Namank Calculator - Find Your Name Number",
                            "Calculate your Namank from your name and discover the traditional numerology qualities connected with your public identity.")
            + calc + content + "</main>")
    return page(path="/namank-calculator", title="Namank Calculator - Find Your Name Number | Bhagyank Calculator",
                description="Use our free Namank Calculator to find your Name Number and understand its traditional numerology meaning.",
                body=body)


def gemstone():
    stones = [("1", "Ruby", "Leadership, confidence and vitality"), ("2", "Pearl", "Calmness, sensitivity and emotional balance"),
              ("3", "Yellow Sapphire", "Wisdom, optimism and prosperity"), ("4", "Hessonite", "Focus, courage and practical stability"),
              ("5", "Emerald", "Communication, learning and creativity"), ("6", "Diamond", "Love, harmony and artistic expression"),
              ("7", "Cat's Eye", "Intuition, protection and spiritual insight"), ("8", "Blue Sapphire", "Discipline, patience and responsibility"),
              ("9", "Red Coral", "Energy, courage and determination")]
    cards = "".join(f'<article class="card mini bg"><div class="num-row"><span class="num sm">{n}</span><h3>{e(s)}</h3></div>'
                    f'<p class="small muted">{m}</p></article>' for n, s, m in stones)
    calc = f"""    <section class="card tool" aria-label="Free gemstone recommendation calculator" data-calc="gemstone">
      <div class="tool-head">
        <div class="tool-icon">{GEM}</div>
        <h2>Find Your Gemstone</h2>
        <p class="muted">Enter your date of birth to get a traditional numerology-based gemstone suggestion.</p>
        <form class="tool-form" novalidate>
          <label for="gemstone-date">Date of birth</label>
          <input id="gemstone-date" name="date" type="date">
          <button type="submit" class="btn" disabled>{SPARKLE} Get My Recommendation</button>
        </form>
      </div>
      <div class="tool-result" aria-live="polite"></div>
    </section>
  </div>
</section>
"""
    content = f"""<section class="band"><div class="container">
<div class="center mid">
<span class="eyebrow">{SPARKLE} Vedic numerology guide</span>
<h2>How gemstone recommendations work</h2>
<p class="muted">In numerology, each number is associated with a planetary energy. A gemstone is traditionally chosen to symbolically support that energy and its positive qualities. For a fuller reading, first calculate your <a href="/moolank-calculator" class="link">Moolank</a> and <a href="/" class="link">Bhagyank</a> using your date of birth.</p>
</div>
<div class="grid-3 mt-lg">{cards}</div>
<div class="grid-2 narrow-grid mt-lg">
<div class="card mini bg"><h3>Choose thoughtfully</h3><p class="small muted">A recommendation is a starting point, not a substitute for a qualified astrologer or gemologist. Always verify quality, authenticity and suitability before buying.</p></div>
<div class="card mini bg"><h3>A traditional practice</h3><p class="small muted">Gemstone meanings come from traditional Vedic numerology and are provided for educational and spiritual interest only.</p></div>
</div>
</div></section>"""
    body = ("<main>" + hero("Free gemstone guide", "Free Gemstone Recommendation",
                            "Discover a traditional numerology-based gemstone recommendation from your date of birth and learn what its energy represents.",
                            icon=GEM)
            + calc + content + "</main>")
    return page(path="/gemstone-recommendation", title="Free Gemstone Recommendation by Date of Birth | Bhagyank Calculator",
                description="Get a free traditional Vedic numerology gemstone recommendation using your date of birth.", body=body)


def shell(path, title, h1, intro, inner, description, schema=None):
    body = f"""<main class="container narrow prose-page">
<h1>{h1}</h1>
<p class="lead-left muted">{intro}</p>
<div class="prose">{inner}</div>
</main>"""
    return page(path=path, title=title, description=description, body=body, scripts=True, schema=schema)


def about():
    inner = f"""<p><strong>Bhagyank Calculator</strong> is a free online tool built to help you discover your <strong>Bhagyank (Destiny Number)</strong> using the principles of Vedic numerology. By entering your date of birth, you can instantly learn your ruling planet, core personality traits, strengths, and the lucky colors and days associated with your number.</p>
<section class="reviewer" aria-labelledby="about-author">
<img src="{AUTHOR['image']}" alt="Ananya Sharma, author of the Bhagyank Calculator numerology guides" width="128" height="128" loading="lazy">
<div><p class="eyebrow">Our author</p><h2 id="about-author">Ananya Sharma (अनन्या शर्मा)</h2>
<p>{e(AUTHOR["short"])}</p>
<a href="{AUTHOR['url']}">Read Ananya Sharma's author profile</a></div>
</section>
<h2>Our Mission</h2>
<p>Numerology has guided people for thousands of years. Our mission is to make this ancient knowledge simple, accessible, and accurate for a modern audience. We believe understanding the numbers behind your birth date can offer meaningful insight into your life path and decisions.</p>
<h2>What We Offer</h2>
<p>Alongside our instant calculator, we provide clear, easy-to-understand explanations of what each destiny number means, how Bhagyank differs from Mulank, and how to calculate your numbers by hand. All of our content is written to be beginner-friendly and free of jargon.</p>
<h2>A Note on Accuracy</h2>
<p>Our calculations follow traditional Vedic numerology methods. However, numerology is intended for guidance and self-reflection, not as a substitute for professional advice. Please treat all insights as informational and for entertainment purposes.</p>"""
    return shell("/about", "About Us | Bhagyank Calculator", "About Us",
                 "Bringing the timeless wisdom of Vedic numerology to everyone, for free.", inner,
                 "Learn about Bhagyank Calculator and author Ananya Sharma (अनन्या शर्मा), who writes our guides on calculating Bhagyank and Mulank from your date of birth.",
                 schema={"@context": "https://schema.org", "@type": "AboutPage", "url": f"{SITE}/about",
                         "dateModified": TODAY.isoformat(), "author": author_schema()})


def contact():
    inner = """<p>Have a question about your Bhagyank, spotted something that needs fixing, or want to share feedback? We're happy to help. Reach out to us using the details below and we'll get back to you as soon as we can.</p>
<h2>Email</h2>
<p>For all queries, please email us at <a href="mailto:support@bhagyank-calculator.online">support@bhagyank-calculator.online</a>.</p>
<h2>Feedback &amp; Suggestions</h2>
<p>Your feedback helps us improve. If you have ideas for new features or notice any inaccuracies in our numerology content, let us know and we'll review them carefully.</p>
<h2>Response Time</h2>
<p>We typically respond to messages within 2-3 business days. Thank you for your patience and for using Bhagyank Calculator.</p>"""
    return shell("/contact", "Contact Us | Bhagyank Calculator", "Contact Us",
                 "We would love to hear your questions, feedback, and suggestions.", inner,
                 "Get in touch with the Bhagyank Calculator team for questions, feedback, or suggestions about our free Vedic numerology tool.")


def privacy():
    inner = """<p>This Privacy Policy describes how <strong>Bhagyank Calculator</strong> ("we", "us", or "our") handles information when you visit <strong>www.bhagyank-calculator.online</strong>.</p>
<h2>Information We Collect</h2>
<p>Our calculators work entirely in your browser. The date of birth or name you enter is used only to calculate your result and is <strong>not stored or sent to our servers</strong>. We do not require you to create an account or submit personal information to use the tools.</p>
<h2>Cookies &amp; Analytics</h2>
<p>We use Google Tag Manager and analytics tools to understand how visitors use our site. These services may set cookies to collect anonymous usage data such as pages visited and device type. This helps us improve the website. You can disable cookies in your browser settings at any time.</p>
<h2>Advertising</h2>
<p>We use Google AdSense to show ads. Google and its partners may use cookies to serve ads based on your previous visits to this and other websites. You can opt out of personalised advertising at <a href="https://adssettings.google.com" target="_blank" rel="noreferrer">Google Ads Settings</a>.</p>
<h2>Third-Party Services</h2>
<p>Third-party services such as Google may use cookies to serve content and measure traffic. Their use of data is governed by their own privacy policies.</p>
<h2>Changes to This Policy</h2>
<p>We may update this Privacy Policy from time to time. Any changes will be posted on this page with an updated revision date.</p>
<h2>Contact</h2>
<p>If you have questions about this policy, please contact us at <a href="mailto:support@bhagyank-calculator.online">support@bhagyank-calculator.online</a>.</p>"""
    return shell("/privacy-policy", "Privacy Policy | Bhagyank Calculator", "Privacy Policy",
                 "Your privacy matters to us. This policy explains how we handle information on our website.", inner,
                 "Read the privacy policy for Bhagyank Calculator to understand how we handle data and use cookies on our free numerology website.")


def terms():
    inner = """<p>By accessing and using <strong>Bhagyank Calculator</strong> at www.bhagyank-calculator.online, you agree to be bound by these Terms &amp; Conditions. If you do not agree, please do not use the website.</p>
<h2>Use of the Website</h2>
<p>Bhagyank Calculator is provided as a free tool for personal, non-commercial use. You agree to use the website lawfully and not to misuse, copy, or redistribute our content without permission.</p>
<h2>Informational Purpose Only</h2>
<p>All numerology results and content are provided for informational and entertainment purposes only. They should not be treated as professional, medical, financial, or legal advice. Any decisions you make based on the information are your own responsibility.</p>
<h2>Accuracy of Content</h2>
<p>We strive to keep our calculations and content accurate, but we make no guarantees regarding completeness or reliability. The website is provided on an "as is" basis without warranties of any kind.</p>
<h2>Limitation of Liability</h2>
<p>We shall not be liable for any loss or damage arising from the use of this website or reliance on its content.</p>
<h2>Changes to These Terms</h2>
<p>We may revise these Terms &amp; Conditions at any time. Continued use of the website after changes constitutes acceptance of the updated terms.</p>"""
    return shell("/terms-and-conditions", "Terms & Conditions | Bhagyank Calculator", "Terms &amp; Conditions",
                 "Please read these terms carefully before using our website.", inner,
                 "Read the terms and conditions for using Bhagyank Calculator, our free Vedic numerology and destiny number tool.")


def not_found():
    body = """<main class="container narrow prose-page center">
<h1>Page not found</h1>
<p class="muted">Sorry, this page doesn't exist. Try one of our free calculators instead.</p>
<p><a class="btn inline" href="/">Bhagyank Calculator</a></p>
<p class="small"><a class="link" href="/moolank-calculator">Moolank Calculator</a> · <a class="link" href="/namank-calculator">Namank Calculator</a> · <a class="link" href="/hi">भाग्यांक कैलकुलेटर</a></p>
</main>"""
    return page(path="/404", title="Page not found | Bhagyank Calculator", description="This page could not be found.",
                body=body, noindex=True)


import datetime as _dt
TODAY = _dt.date.today()
MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
             "October", "November", "December"]
MONTHS_HI = ["जनवरी", "फ़रवरी", "मार्च", "अप्रैल", "मई", "जून", "जुलाई", "अगस्त", "सितंबर", "अक्टूबर", "नवंबर", "दिसंबर"]

STONES = {1: ("Ruby", "माणिक्य"), 2: ("Pearl", "मोती"), 3: ("Yellow Sapphire", "पुखराज"), 4: ("Hessonite", "गोमेद"),
          5: ("Emerald", "पन्ना"), 6: ("Diamond", "हीरा"), 7: ("Cat's Eye", "लहसुनिया"), 8: ("Blue Sapphire", "नीलम"),
          9: ("Red Coral", "मूंगा")}


def reduce_num(n):
    while n > 9:
        n = sum(int(c) for c in str(n))
    return n


def updated_line(lang):
    if lang == "hi":
        txt = f"अंतिम अपडेट: {TODAY.day} {MONTHS_HI[TODAY.month - 1]} {TODAY.year}"
    else:
        txt = f"Last updated: {TODAY.day} {MONTHS_EN[TODAY.month - 1]} {TODAY.year}"
    return f'<p class="container narrow updated xs muted"><time datetime="{TODAY.isoformat()}">{txt}</time></p>'


def chart_table():
    rows = "".join(
        f'<tr><td><a class="link" href="/bhagyank/{n}">Bhagyank {n}</a></td><td>{e(EN[str(n)]["planet"])} ({e(EN[str(n)]["planetHindi"])})</td>'
        f'<td>{e(", ".join(EN[str(n)]["luckyColors"]))}</td><td>{e(", ".join(EN[str(n)]["luckyDays"]))}</td>'
        f'<td>{e(STONES[n][0])}</td></tr>' for n in range(1, 10))
    return ('<p>Use this quick reference to see the ruling planet, lucky colors, lucky days and traditional gemstone '
            'for every destiny number from 1 to 9.</p>'
            '<div class="table-wrap"><table><thead><tr><th>Bhagyank</th><th>Ruling planet</th><th>Lucky colors</th>'
            f'<th>Lucky days</th><th>Gemstone</th></tr></thead><tbody>{rows}</tbody></table></div>')


def example_dates(n, count=3):
    """Real dates of birth whose Bhagyank is n, spread across decades."""
    out, d = [], _dt.date(1975, 1, 1)
    while len(out) < count:
        digits = f"{d.day}{d.month}{d.year}"
        total = sum(int(c) for c in digits)
        if reduce_num(total) == n:
            out.append((d, digits, total))
            d = _dt.date(d.year + 11, (d.month % 12) + 1, 1)
        else:
            d += _dt.timedelta(days=37)
    return out


def number_page(n):
    i, h = EN[str(n)], HI[str(n)]
    stone, stone_hi = STONES[n]
    planet = f'{i["planet"]} ({i["planetHindi"]})'
    title = f"Bhagyank {n} Meaning: Personality, Career & Lucky Colors"
    desc = (f"Bhagyank {n} is ruled by {i['planet']}. Learn the meaning of destiny number {n} in Vedic numerology: "
            f"personality, strengths, challenges, best careers, lucky colors, lucky days and gemstone.")
    ex_rows = "".join(
        f'<li>{d.day} {MONTHS_EN[d.month - 1]} {d.year}: {" + ".join(digits)} = {total}'
        + (f' → {" + ".join(str(total))} = {sum(int(c) for c in str(total))}' if total > 9 else "")
        + (f' → {reduce_num(sum(int(c) for c in str(total)))}' if sum(int(c) for c in str(total)) > 9 else "")
        + f' → <strong>Bhagyank {n}</strong></li>' for d, digits, total in example_dates(n))
    faqs = [
        (f"What is the ruling planet of Bhagyank {n}?",
         f"Bhagyank {n} is ruled by {i['planet']} ({i['planetHindi']}) in Vedic numerology. Its energy shapes the "
         f"life path of people whose full date of birth adds up to {n}."),
        (f"What are the lucky colors and days for Bhagyank {n}?",
         f"The lucky colors for Bhagyank {n} are {', '.join(i['luckyColors'])}, and the favourable days are "
         f"{' and '.join(i['luckyDays'])}."),
        (f"Which careers suit Bhagyank {n}?", f"Careers that traditionally suit Bhagyank {n} include: {i['career']}"),
        (f"Which gemstone is linked with Bhagyank {n}?",
         f"In traditional numerology, {stone} ({stone_hi}) is associated with number {n} and its planet {i['planet']}. "
         f"Please consult a qualified astrologer before wearing any gemstone."),
        (f"How do I know if my Bhagyank is {n}?",
         f"Add every digit of your full date of birth (day, month and year) and keep adding the digits of the total until "
         f"one digit is left. If the final digit is {n}, your Bhagyank is {n}. You can also use the free Bhagyank Calculator."),
    ]
    others = " ".join(
        f'<a class="pill{" active" if k == n else ""}" href="/bhagyank/{k}"{" aria-current=\"page\"" if k == n else ""}>{k}</a>'
        for k in range(1, 10))
    prev_n, next_n = (n - 2) % 9 + 1, n % 9 + 1
    body = f"""<main>
<div class="container narrow num-page">
<nav class="crumbs xs muted" aria-label="Breadcrumb"><a href="/">Bhagyank Calculator</a> <span aria-hidden="true">›</span> <span>Bhagyank {n}</span></nav>
<div class="num-hero">
  <div class="circle"><span>{n}</span><small>Bhagyank</small></div>
  <div>
    <h1>Bhagyank {n} Meaning - {e(i["title"])}</h1>
    <p class="muted">Ruling planet: {e(planet)} · भाग्यांक {n} - {e(h["title"])}</p>
  </div>
</div>
<p class="lead-left">{e(i["summary"])}</p>
<p><a class="btn inline" href="/#calculator">Calculate your Bhagyank</a></p>

<div class="content">
{section("personality", f"Bhagyank {n} personality", f'<p>People with destiny number {n} carry the energy of {e(i["planet"])}. The core themes of this number are {e(", ".join(k.lower() for k in i["keywords"]))}. {e(IDIOM_EN[n])}</p><div class="info-grid"><div class="info"><h4>Strengths</h4>{"<ul>" + "".join(f"<li>{e(x)}</li>" for x in i["strengths"]) + "</ul>"}</div><div class="info"><h4 class="accent">Challenges to watch</h4>{"<ul>" + "".join(f"<li>{e(x)}</li>" for x in i["challenges"]) + "</ul>"}</div></div>')}
{section("career", f"Best careers for Bhagyank {n}", f'<p>{e(i["career"])}</p><p>These fields reward the natural qualities of number {n}. Your Mulank (birth number) and Namank (name number) can add other strengths, so read them together with your Bhagyank before making a big career decision.</p>')}
{section("lucky", f"Lucky colors, days and gemstone for Bhagyank {n}", f'<div class="table-wrap"><table><tbody><tr><td>Ruling planet</td><td>{e(planet)}</td></tr><tr><td>Lucky colors</td><td>{e(", ".join(i["luckyColors"]))}</td></tr><tr><td>Lucky days</td><td>{e(", ".join(i["luckyDays"]))}</td></tr><tr><td>Traditional gemstone</td><td>{e(stone)} ({stone_hi})</td></tr></tbody></table></div><p class="small">Gemstones are a traditional practice. See our <a class="link" href="/gemstone-recommendation">gemstone guide</a> and consult a qualified astrologer before wearing one.</p>')}
{section("examples", f"Examples: dates of birth with Bhagyank {n}", f'<p>Your Bhagyank is {n} when all the digits of your full date of birth reduce to {n}. A few examples:</p><div class="card example"><ul>{ex_rows}</ul></div><p>Not sure about yours? Use the free <a class="link" href="/#calculator">Bhagyank Calculator</a> - it takes your date of birth and shows your number instantly.</p>')}
{section("trust", "Should you trust your Bhagyank?", STAT_EN)}
{section("hindi", f"भाग्यांक {n} (हिंदी में)", f'<p lang="hi">{e(h["summary"])}</p><p class="small"><a class="link" href="/hi/bhagyank/{n}" hreflang="hi">भाग्यांक {n} का पूरा अर्थ हिंदी में पढ़ें</a></p>')}
{section("faq", f"Bhagyank {n}: frequently asked questions", faq_block(faqs))}
<section class="content-section"><h2>Other destiny numbers</h2><nav class="pills" aria-label="Bhagyank numbers">{others}</nav>
<p class="small"><a class="link" href="/bhagyank/{prev_n}">← Bhagyank {prev_n}</a> · <a class="link" href="/bhagyank/{next_n}">Bhagyank {next_n} →</a></p></section>
<p class="card disclaimer">Disclaimer: This content is based on traditional Vedic numerology and is provided for informational and entertainment purposes. It is not a substitute for professional advice.</p>
</div>
</div>
{reviewed_by("en")}
{updated_line("en")}
</main>"""
    url = f"{SITE}/bhagyank/{n}"
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Article", "@id": f"{url}#article", "headline": f"Bhagyank {n} Meaning - {i['title']}",
             "description": desc, "url": url, "inLanguage": "en", "image": f"{SITE}/images/og-image.png",
             "datePublished": TODAY.isoformat(), "dateModified": TODAY.isoformat(),
             "author": author_schema(),
             "publisher": {"@type": "Organization", "name": "Bhagyank Calculator", "url": SITE,
                           "logo": {"@type": "ImageObject", "url": f"{SITE}/icon-512.png"}},
             "mainEntityOfPage": url},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Bhagyank Calculator", "item": SITE},
                {"@type": "ListItem", "position": 2, "name": f"Bhagyank {n}", "item": url}]},
            {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
        ],
    }
    return page(path=f"/bhagyank/{n}", title=title, description=desc, body=body, schema=schema,
                hreflang=(f"/bhagyank/{n}", f"/hi/bhagyank/{n}"))


FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<rect width="64" height="64" rx="14" fill="#1a1636"/>
<circle cx="32" cy="32" r="23" fill="none" stroke="#e8b94a" stroke-width="3.5"/>
<path d="M32 15.5 L35.9 28.1 L48.5 32 L35.9 35.9 L32 48.5 L28.1 35.9 L15.5 32 L28.1 28.1 Z" fill="#e8b94a"/>
</svg>
"""


def author_page():
    url = SITE + AUTHOR["url"]
    guides = "".join(f'<li><a class="link" href="/bhagyank/{n}">Bhagyank {n} meaning - {e(EN[str(n)]["title"])}</a></li>' for n in range(1, 10))
    body = f"""<main class="container narrow prose-page">
<nav class="crumbs xs muted" aria-label="Breadcrumb"><a href="/">Bhagyank Calculator</a> <span aria-hidden="true">›</span> <a href="/about">About</a> <span aria-hidden="true">›</span> <span>Ananya Sharma</span></nav>
<div class="author-hero">
  <img src="{AUTHOR['image']}" alt="Ananya Sharma, author of the Bhagyank Calculator numerology guides" width="160" height="160">
  <div>
    <p class="eyebrow">Author</p>
    <h1>Ananya Sharma <span lang="hi">(अनन्या शर्मा)</span></h1>
    <p class="muted">Writer of the numerology guides on Bhagyank Calculator · English and Hindi</p>
  </div>
</div>
<div class="prose">
<h2>About Ananya</h2>
{"".join(f"<p>{e(x)}</p>" for x in AUTHOR_BIO["en"])}
<h2 lang="hi">अनन्या शर्मा के बारे में</h2>
{"".join(f'<p lang="hi">{e(x)}</p>' for x in AUTHOR_BIO["hi"])}
<h2>What she writes about</h2>
<ul>
<li><a class="link" href="/">Bhagyank Calculator</a> - how to find your destiny number from your full date of birth</li>
<li><a class="link" href="/hi">भाग्यांक कैलकुलेटर (हिंदी)</a> - the same guide in Hindi</li>
<li><a class="link" href="/moolank-calculator">Moolank (Mulank) Calculator</a> - your birth number from the day you were born</li>
<li><a class="link" href="/namank-calculator">Namank Calculator</a> - your name number</li>
<li><a class="link" href="/gemstone-recommendation">Gemstone guide</a> - the traditional gemstone for each number</li>
</ul>
<h2>Bhagyank 1 to 9 guides</h2>
<ul>{guides}</ul>
<h2>How she writes the guides</h2>
<p>Every guide follows the traditional Vedic numerology method: add every digit of the date of birth and reduce the total to a single number from 1 to 9. Each guide shows the full working with real date-of-birth examples, so you can check the result yourself. The guides explain what each number traditionally represents and do not make promises about your future.</p>
<h2>Corrections and contact</h2>
<p>If you spot a mistake or have a question about a guide, please write to <a href="mailto:support@bhagyank-calculator.online">support@bhagyank-calculator.online</a> or use our <a href="/contact">contact page</a>. Corrections are reviewed and the page is updated.</p>
</div>
</main>
{updated_line("en")}"""
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "ProfilePage", "@id": f"{url}#profile", "url": url, "name": "Ananya Sharma - Author",
         "dateModified": TODAY.isoformat(), "inLanguage": "en", "mainEntity": author_schema(),
         "isPartOf": {"@id": f"{SITE}/#website"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Bhagyank Calculator", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": "About", "item": f"{SITE}/about"},
            {"@type": "ListItem", "position": 3, "name": "Ananya Sharma", "item": url}]}]}
    return page(path=AUTHOR["url"], title="Ananya Sharma (अनन्या शर्मा) - Author | Bhagyank Calculator",
                description=("Ananya Sharma (अनन्या शर्मा) writes the numerology guides on Bhagyank Calculator, explaining how "
                             "to calculate Bhagyank and Mulank from your date of birth and what each number means."),
                body=body, schema=schema)

# ---------------------------------------------------------------- Hindi Bhagyank pages + shared facts

PEW_URL = "https://www.pewresearch.org/religion/2021/06/29/religious-beliefs-2/"

STAT_EN = ('<p>You are far from alone in checking your numbers. In a <a class="link" href="' + PEW_URL +
           '" target="_blank" rel="noopener">Pew Research Center survey</a> of 29,999 Indian adults, 49% of Hindus said '
           'they believe in astrology. Numerology comes from the same tradition. Still, treat your Bhagyank as a guide, '
           'not a rule. It can point out your natural strengths, but your choices and hard work decide the result.</p>')

STAT_HI = ('<p>अंक ज्योतिष में रुचि रखने वाले आप अकेले नहीं हैं। भारत के 29,999 वयस्कों पर हुए <a class="link" href="' + PEW_URL +
           '" target="_blank" rel="noopener">Pew Research के सर्वे</a> में 49% हिंदुओं ने कहा कि वे ज्योतिष पर विश्वास करते हैं। '
           'फिर भी भाग्यांक को एक मार्गदर्शक की तरह देखें, पक्के नियम की तरह नहीं। यह आपकी खूबियाँ दिखा सकता है, '
           'लेकिन आखिरी फैसला आपकी मेहनत और आपके चुनाव ही करते हैं।</p>')

# one natural idiom per page, placed in the personality section
IDIOM_EN = {
    1: "Leaders need people too, though - no man is an island, so a good team makes a 1 even stronger.",
    2: "People with this number often wear their heart on their sleeve, so kind words matter a lot to them.",
    3: "For a 3, knowledge really is power - they grow fastest when they keep learning and sharing.",
    4: "A 4 likes to march to the beat of their own drum, even when others take the easy road.",
    5: "Many 5s are a jack of all trades. The trick is picking one or two things and sticking with them.",
    6: "For a 6, home is where the heart is - family and close friends come first.",
    7: "Still waters run deep: a 7 may look quiet, but there is a lot going on inside.",
    8: "Slow and steady wins the race for an 8. Success may come late, but it tends to last.",
    9: "A 9 can have a short fuse, so counting to ten before reacting saves a lot of trouble.",
}
IDIOM_HI = {
    1: "पर याद रखें, अकेला चना भाड़ नहीं फोड़ सकता - अच्छी टीम के साथ भाग्यांक 1 और आगे जाता है।",
    2: "इन पर 'जैसी संगत वैसी रंगत' वाली बात खूब लागू होती है, इसलिए अच्छे लोगों का साथ इनके लिए ज़रूरी है।",
    3: "ये मानते हैं कि ज्ञान बाँटने से बढ़ता है, इसलिए दूसरों को सिखाने में इन्हें खुशी मिलती है।",
    4: "ये अक्सर लीक से हटकर चलते हैं और वही रास्ता चुनते हैं जो इन्हें सही लगता है।",
    5: "ऐसे लोग अक्सर हरफनमौला होते हैं, बस इन्हें एक-दो कामों पर टिककर मेहनत करना सीखना चाहिए।",
    6: "ये अपनी बातों और व्यवहार से जल्दी ही सबका दिल जीत लेते हैं।",
    7: "कभी-कभी ये बाल की खाल निकालने लगते हैं, इसलिए हर बात पर ज़्यादा सोचने से बचना चाहिए।",
    8: "इनके लिए 'देर आए दुरुस्त आए' बिल्कुल सही बैठता है - सफलता देर से मिलती है, पर टिकती है।",
    9: "गुस्से में ये ईंट का जवाब पत्थर से दे देते हैं, इसलिए जवाब देने से पहले थोड़ा रुकना अच्छा रहता है।",
}


def example_dates_hi(n):
    rows = []
    for d, digits, total in example_dates(n):
        steps = f'{" + ".join(digits)} = {total}'
        t = total
        while t > 9:
            nxt = sum(int(c) for c in str(t))
            steps += f' → {" + ".join(str(t))} = {nxt}'
            t = nxt
        rows.append(f'<li>{d.day} {MONTHS_HI[d.month - 1]} {d.year}: {steps} → <strong>भाग्यांक {n}</strong></li>')
    return "".join(rows)


def updated_line_hi():
    return updated_line("hi")


def number_page_hi(n):
    i, en = HI[str(n)], EN[str(n)]
    stone, stone_hi = STONES[n]
    title = f"भाग्यांक {n} का अर्थ: स्वभाव, करियर, शुभ रंग और शुभ दिन"
    desc = (f"भाग्यांक {n} का स्वामी ग्रह {i['planet']} है। जानें भाग्यांक {n} वाले लोगों का स्वभाव, खूबियाँ, कमज़ोरियाँ, "
            f"सही करियर, शुभ रंग, शुभ दिन और रत्न - आसान हिंदी में, उदाहरण के साथ।")
    faqs = [
        (f"भाग्यांक {n} का स्वामी ग्रह कौन सा है?",
         f"भाग्यांक {n} का स्वामी ग्रह {i['planet']} है। जिन लोगों की पूरी जन्मतिथि का योग {n} आता है, उन पर इसी ग्रह की ऊर्जा का असर माना जाता है।"),
        (f"भाग्यांक {n} के लिए शुभ रंग और शुभ दिन कौन से हैं?",
         f"भाग्यांक {n} के लिए शुभ रंग {', '.join(i['luckyColors'])} हैं, और शुभ दिन {' और '.join(i['luckyDays'])} माने जाते हैं।"),
        (f"भाग्यांक {n} वालों के लिए कौन सा करियर अच्छा है?", f"भाग्यांक {n} के लिए ये क्षेत्र अच्छे माने जाते हैं: {i['career']}"),
        (f"भाग्यांक {n} का रत्न कौन सा है?",
         f"पारंपरिक अंक ज्योतिष में {stone_hi} ({stone}) को अंक {n} से जोड़ा जाता है। कोई भी रत्न पहनने से पहले किसी जानकार ज्योतिषी से सलाह ज़रूर लें।"),
        (f"कैसे पता करें कि मेरा भाग्यांक {n} है?",
         f"अपनी पूरी जन्मतिथि (दिन, महीना और साल) के सभी अंक जोड़ें। जब तक एक अंक न बचे, योग के अंकों को फिर से जोड़ते रहें। आखिर में {n} आए तो आपका भाग्यांक {n} है।"),
    ]
    others = " ".join(
        f'<a class="pill{" active" if k == n else ""}" href="/hi/bhagyank/{k}"{" aria-current=\"page\"" if k == n else ""}>{k}</a>'
        for k in range(1, 10))
    prev_n, next_n = (n - 2) % 9 + 1, n % 9 + 1
    ul = lambda xs: "<ul>" + "".join(f"<li>{e(x)}</li>" for x in xs) + "</ul>"
    body = f"""<main lang="hi">
<div class="container narrow num-page">
<nav class="crumbs xs muted" aria-label="Breadcrumb"><a href="/hi">भाग्यांक कैलकुलेटर</a> <span aria-hidden="true">›</span> <span>भाग्यांक {n}</span></nav>
<div class="num-hero">
  <div class="circle"><span>{n}</span><small>भाग्यांक</small></div>
  <div>
    <h1>भाग्यांक {n} का अर्थ - {e(i["title"])}</h1>
    <p class="muted">स्वामी ग्रह: {e(i["planet"])} · <span lang="en">Bhagyank {n} - {e(en["title"])}</span></p>
  </div>
</div>
<p class="lead-left">{e(i["summary"])}</p>
<p><a class="btn inline" href="/hi#calculator">अपना भाग्यांक निकालें</a></p>

<div class="content">
{section("kaise-banta-hai", f"भाग्यांक {n} कैसे बनता है?", f'<p>जब आपकी पूरी जन्मतिथि के सभी अंकों का योग घटाते-घटाते {n} पर आकर रुकता है, तब आपका भाग्यांक {n} होता है। नीचे कुछ असली तारीखों के उदाहरण देखें:</p><div class="card example"><ul>{example_dates_hi(n)}</ul></div><p>अपनी तारीख़ खुद जोड़ना मुश्किल लगे, तो <a class="link" href="/hi#calculator">भाग्यांक कैलकुलेटर</a> में जन्मतिथि डालें। जवाब एक सेकंड में मिल जाएगा।</p>')}
{section("swabhav", f"भाग्यांक {n} वाले लोगों का स्वभाव", f'<p>भाग्यांक {n} वाले लोगों में {e(i["planet"])} ग्रह की ऊर्जा साफ दिखती है। इनकी कुछ खूबियाँ इन्हें भीड़ से अलग बनाती हैं, और कुछ बातों पर इन्हें ध्यान देना पड़ता है। {e(IDIOM_HI[n])}</p><div class="info-grid"><div class="info"><h4>खूबियाँ</h4>{ul(i["strengths"])}</div><div class="info"><h4 class="accent">किन बातों का ध्यान रखें</h4>{ul(i["challenges"])}</div></div>')}
{section("career", f"भाग्यांक {n} के लिए सही करियर", f'<p>{e(i["career"])}</p><p>ये क्षेत्र भाग्यांक {n} के स्वभाव से मेल खाते हैं। करियर का बड़ा फैसला लेने से पहले अपना <a class="link" href="/moolank-calculator">मूलांक</a> और <a class="link" href="/namank-calculator">नामांक</a> भी देख लें, क्योंकि तीनों अंक साथ में ज़्यादा साफ तस्वीर दिखाते हैं।</p>')}
{section("shubh", f"भाग्यांक {n} के शुभ रंग, शुभ दिन और रत्न", f'<div class="table-wrap"><table><tbody><tr><td>स्वामी ग्रह</td><td>{e(i["planet"])}</td></tr><tr><td>शुभ रंग</td><td>{e(", ".join(i["luckyColors"]))}</td></tr><tr><td>शुभ दिन</td><td>{e(", ".join(i["luckyDays"]))}</td></tr><tr><td>रत्न</td><td>{stone_hi} ({e(stone)})</td></tr></tbody></table></div><p class="small">रत्न पहनना एक पारंपरिक उपाय है। पहनने से पहले किसी जानकार ज्योतिषी से सलाह ज़रूर लें। ज़्यादा जानकारी के लिए हमारी <a class="link" href="/gemstone-recommendation">रत्न गाइड</a> देखें।</p>')}
{section("bharosa", "क्या भाग्यांक पर भरोसा करना चाहिए?", STAT_HI)}
{section("faq", f"भाग्यांक {n}: अक्सर पूछे जाने वाले सवाल", faq_block(faqs))}
<section class="content-section"><h2>बाकी भाग्यांक</h2><nav class="pills" aria-label="भाग्यांक">{others}</nav>
<p class="small"><a class="link" href="/hi/bhagyank/{prev_n}">← भाग्यांक {prev_n}</a> · <a class="link" href="/hi/bhagyank/{next_n}">भाग्यांक {next_n} →</a> · <a class="link" href="/bhagyank/{n}" hreflang="en" lang="en">Read in English</a></p></section>
<p class="card disclaimer">अस्वीकरण: यह जानकारी पारंपरिक वैदिक अंक ज्योतिष पर आधारित है और केवल जानकारी के लिए है। इसे किसी पेशेवर सलाह का विकल्प न मानें।</p>
</div>
</div>
{reviewed_by("hi")}
{updated_line("hi")}
</main>"""
    url = f"{SITE}/hi/bhagyank/{n}"
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": f"{url}#article", "headline": title, "description": desc, "url": url,
         "inLanguage": "hi", "image": f"{SITE}/images/og-image.png", "datePublished": TODAY.isoformat(),
         "dateModified": TODAY.isoformat(), "author": author_schema(),
         "publisher": {"@type": "Organization", "name": "Bhagyank Calculator", "url": SITE,
                       "logo": {"@type": "ImageObject", "url": f"{SITE}/icon-512.png"}}, "mainEntityOfPage": url},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "भाग्यांक कैलकुलेटर", "item": f"{SITE}/hi"},
            {"@type": "ListItem", "position": 2, "name": f"भाग्यांक {n}", "item": url}]},
        {"@type": "FAQPage", "inLanguage": "hi", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}]}
    return page(path=f"/hi/bhagyank/{n}", lang="hi", title=title, description=desc, body=body, schema=schema,
                hreflang=(f"/bhagyank/{n}", f"/hi/bhagyank/{n}"))

# ---------------------------------------------------------------- Lo Shu grid calculator page

LOSHU_NUMS = [
    (1, "Sun", "Communication and career", "You may find it harder to explain your feelings or speak up for yourself."),
    (2, "Moon", "Feelings and intuition", "You may trust your gut less and second-guess people's intentions."),
    (3, "Jupiter", "Learning and imagination", "You may need more effort to stay creative or keep learning new things."),
    (4, "Rahu", "Order and hard work", "You may struggle with routines, planning and keeping things tidy."),
    (5, "Mercury", "Balance and focus", "You may find it harder to stay steady when life gets busy."),
    (6, "Venus", "Family, home and comforts", "You may need to give more time to family and to your own comfort."),
    (7, "Ketu", "Inner growth and luck", "You may learn some lessons the hard way before things click."),
    (8, "Saturn", "Money handling and patience", "You may need to work on saving money and being patient."),
    (9, "Mars", "Energy and ambition", "You may need a push to start things and keep your energy up."),
]
LOSHU_PLANES = [
    ("Mental plane", "4 - 9 - 2", "Thinking, memory and planning"),
    ("Emotional plane", "3 - 5 - 7", "Feelings, kindness and sensitivity"),
    ("Practical plane", "8 - 1 - 6", "Hands-on skills and everyday life"),
    ("Thought plane", "4 - 3 - 8", "Ideas and how you plan them"),
    ("Will plane", "9 - 5 - 1", "Determination and staying power"),
    ("Action plane", "2 - 7 - 6", "Turning ideas into action"),
    ("Golden Yog", "4 - 5 - 6", "Success and growth"),
    ("Silver Yog", "2 - 5 - 8", "Property and steady wealth"),
]

LOSHU_FAQ = [
    ("How do you calculate a Lo Shu Grid from date of birth?",
     "Write your full date of birth as digits and drop the zeros. Place each digit in its fixed box on the 4-9-2, 3-5-7, "
     "8-1-6 grid. Most Indian numerologists also add your Mulank (birth day reduced to one digit) and your Bhagyank "
     "(full date reduced to one digit). Repeated digits go in the same box."),
    ("What does a missing number in the Lo Shu Grid mean?",
     "A missing number points to a quality that does not come naturally to you, so you may need to work on it. "
     "It is not a bad sign. Almost every date of birth has some missing numbers."),
    ("Why are zeros not used in the Lo Shu Grid?",
     "The grid only has boxes for the numbers 1 to 9, so there is no place for 0. That is why a date like 10-10-2000 "
     "leaves many boxes empty."),
    ("Is the Lo Shu Grid the same as Bhagyank?",
     "No. Your Bhagyank is one number that comes from adding your whole date of birth. The Lo Shu Grid looks at every "
     "digit separately and shows which numbers are present, repeated or missing. Together they give a fuller reading."),
    ("Does Kua number go in the Lo Shu Grid?",
     "Some numerologists also add the Kua number, which depends on your birth year and gender. This calculator uses the "
     "more common method with your birth date digits, Mulank and Bhagyank."),
]


def lo_shu_page():
    num_rows = "".join(f'<tr><td>{n}</td><td>{p}</td><td>{a}</td><td>{m}</td></tr>' for n, p, a, m in LOSHU_NUMS)
    plane_rows = "".join(f'<tr><td>{n}</td><td>{nums}</td><td>{m}</td></tr>' for n, nums, m in LOSHU_PLANES)
    grid_demo = "".join(f'<div class="ls-cell{"" if v else " ls-empty"}"><span class="ls-pos">{k}</span><span class="ls-val">{v}</span></div>'
                        for k, v in [(4, ""), (9, "99"), (2, ""), (3, ""), (5, "5"), (7, ""), (8, "8"), (1, "11"), (6, "66")])
    calc = f"""    <div class="calc-grid" data-calc="loshu">
      <form class="card calc-form" novalidate>
        <div class="form-title">{SPARKLE}<h2>Enter Your Date of Birth</h2></div>
        <div class="dob-row">
          <label>Day<select name="day" data-dob="day"><option value="">DD</option></select></label>
          <label>Month<select name="month" data-dob="month"><option value="">MM</option></select></label>
          <label>Year<select name="year" data-dob="year"><option value="">YYYY</option></select></label>
        </div>
        <p class="error" role="alert" hidden></p>
        <button type="submit" class="btn">Make My Lo Shu Grid</button>
        <p class="note">100% free · No sign-up · Instant result</p>
      </form>
      <div class="result" id="loshu-result" aria-live="polite">
        <div class="card empty"><div class="empty-icon">{SPARKLE}</div><h3>Your Grid Will Appear Here</h3>
        <p>Pick your date of birth to see your Lo Shu Grid, your missing and repeated numbers, and which planes are complete.</p></div>
      </div>
    </div>
  </div>
</section>
"""
    loshu_stat = ('<p>Number-based readings are popular for a reason. In a <a class="link" href="' + PEW_URL +
                  '" target="_blank" rel="noopener">Pew Research Center survey</a> of 29,999 Indian adults, 49% of Hindus '
                  'said they believe in astrology, and numerology tools like the Lo Shu Grid come from that same family '
                  'of traditions. Use your grid as a mirror for self-reflection, not as a final verdict on your life.</p>')
    content = f"""<div class="container narrow content">
{section("what-is-lo-shu", "What is a Lo Shu Grid?", '''
<p>A Lo Shu Grid is a 3 x 3 box of numbers from 1 to 9. In numerology, you fill it with the digits of your date of birth to see which numbers you have plenty of, and which ones are missing.</p>
<p>The grid comes from an old Chinese story. A turtle came out of the Luo River with a pattern of dots on its shell. The dots made a "magic square" where every row, column and diagonal adds up to 15. Today the grid is widely used in Indian numerology, often next to your Mulank and Bhagyank.</p>''')}
{section("how-to-make", "How to Make Your Lo Shu Grid (Example)", f'''
<p>Let's use a real date: <strong>15 August 1990</strong>.</p>
<div class="card example"><ol>
<li>Write the date as digits: 1, 5, 0, 8, 1, 9, 9, 0</li>
<li>Drop the zeros: 1, 5, 8, 1, 9, 9</li>
<li>Add the Mulank (birth day 15 → 1 + 5 = <strong>6</strong>)</li>
<li>Add the Bhagyank (1+5+0+8+1+9+9+0 = 33 → 3 + 3 = <strong>6</strong>)</li>
<li>Put each digit in its box. Repeated digits share a box.</li>
</ol></div>
<div class="ls-wrap"><div class="ls-grid demo" aria-label="Example Lo Shu Grid for 15 August 1990">{grid_demo}</div>
<p class="small muted">Example grid for 15 August 1990. Missing numbers: 2, 3, 4, 7. The Will plane (9-5-1) and the Practical plane (8-1-6) are complete.</p></div>''')}
{section("how-to-read", "How to Read Your Lo Shu Grid", '''
<p>Look at three things:</p>
<ul>
<li><strong>Present numbers</strong> - qualities that come easily to you.</li>
<li><strong>Repeated numbers</strong> - extra strength in that area. Too many repeats (four or more) can tip into overdoing it.</li>
<li><strong>Missing numbers</strong> - qualities you may need to build on purpose.</li>
</ul>
<p>Then check the planes below. A plane is "complete" when all three of its numbers are in your grid.</p>''')}
{section("planes", "The 8 Planes of the Lo Shu Grid",
         '<div class="table-wrap"><table><thead><tr><th>Plane</th><th>Numbers</th><th>What it shows</th></tr></thead><tbody>' + plane_rows + '</tbody></table></div>')}
{section("numbers", "What Each Number Means in the Grid",
         '<div class="table-wrap"><table><thead><tr><th>No.</th><th>Planet</th><th>Area of life</th><th>If it is missing</th></tr></thead><tbody>' + num_rows + '</tbody></table></div>')}
{section("missing", "Missing Numbers: Should You Worry?", '''
<p>No. Almost every date of birth leaves a few boxes empty, because a date only has eight digits and many of them repeat. So don't make a mountain out of a molehill if your grid looks gappy.</p>
<p>A missing number simply shows where you may need a little more effort. For example, a missing 4 can mean you find routines boring, so a simple daily to-do list may help you more than it helps others.</p>''')}
{section("trust", "How Much Should You Rely on It?", loshu_stat)}
{section("lo-shu-vs-bhagyank", "Lo Shu Grid vs Bhagyank", '''
<p>Your <a class="link" href="/">Bhagyank</a> is a single number that shows the overall direction of your life. The Lo Shu Grid breaks your date into pieces and shows the mix of strengths behind that number. Start with your Bhagyank, then use the grid to see the details. You can also read the meaning of each <a class="link" href="/bhagyank/1">Bhagyank from 1 to 9</a>.</p>''')}
{section("faq", "Lo Shu Grid: Frequently Asked Questions", faq_block(LOSHU_FAQ))}
<p class="card disclaimer">Disclaimer: The Lo Shu Grid is a traditional numerology tool shared for information and self-reflection. It is not a substitute for professional advice.</p>
</div>"""
    body = ("<main>" + hero("Free Numerology Tool", "Lo Shu Grid Calculator by Date of Birth",
                            "Make your Lo Shu Grid in one click. See your missing and repeated numbers, your Mulank and Bhagyank, "
                            "and which of the 8 planes are complete - explained in plain words.", stars=True)
            + calc + content + reviewed_by("en") + updated_line("en") + "</main>")
    url = f"{SITE}/lo-shu-grid-calculator"
    desc = ("Free Lo Shu Grid calculator: make your numerology grid from your date of birth, find missing and repeated "
            "numbers, Mulank, Bhagyank and the 8 planes, with simple meanings.")
    schema = {"@context": "https://schema.org", "@graph": [
        author_schema(),
        {"@type": "WebApplication", "name": "Lo Shu Grid Calculator", "url": url, "applicationCategory": "LifestyleApplication",
         "operatingSystem": "Web", "description": desc, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "INR"}},
        {"@type": "WebPage", "@id": f"{url}#webpage", "url": url, "name": "Lo Shu Grid Calculator by Date of Birth",
         "author": {"@id": f"{SITE}{AUTHOR['url']}#person"}, "dateModified": TODAY.isoformat(),
         "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
             {"@type": "ListItem", "position": 1, "name": "Bhagyank Calculator", "item": SITE},
             {"@type": "ListItem", "position": 2, "name": "Lo Shu Grid Calculator", "item": url}]}},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in LOSHU_FAQ]}]}
    return page(path="/lo-shu-grid-calculator", title="Lo Shu Grid Calculator by Date of Birth - Free Numerology Chart",
                description=desc, body=body, schema=schema)

# ---------------------------------------------------------------- blog

PLANET_OF = {1: "Sun", 2: "Moon", 3: "Jupiter", 4: "Rahu", 5: "Mercury", 6: "Venus", 7: "Ketu", 8: "Saturn", 9: "Mars"}
PLANET_HI = {1: "सूर्य", 2: "चंद्र", 3: "गुरु", 4: "राहु", 5: "बुध", 6: "शुक्र", 7: "केतु", 8: "शनि", 9: "मंगल"}

# Natural friendships (naisargika maitri) of classical Vedic astrology. Rahu uses the common view; Ketu is left open.
FRIENDS = {1: {2, 9, 3}, 2: {1, 5}, 9: {1, 2, 3}, 5: {1, 6}, 3: {1, 2, 9}, 6: {5, 8}, 8: {5, 6}, 4: {5, 6, 8}}
ENEMIES = {1: {6, 8}, 2: set(), 9: {5}, 5: {2}, 3: {5, 6}, 6: {1, 2}, 8: {1, 2, 9}, 4: {1, 2, 9}}


def relation(a, b):
    """'same' | 'friendly' | 'mixed' | 'challenging' | 'open' for numbers a and b."""
    if a == b:
        return "same"
    if 7 in (a, b):
        return "open"
    if a == 4 or b == 4:
        r, o = (a, b) if a == 4 else (b, a)
        return "friendly" if o in FRIENDS[4] else "challenging" if o in ENEMIES[4] else "mixed"
    fa, fb = b in FRIENDS[a], a in FRIENDS[b]
    ea, eb = b in ENEMIES[a], a in ENEMIES[b]
    if (fa or fb) and not (ea or eb):
        return "friendly"
    if (ea or eb) and not (fa or fb):
        return "challenging"
    return "mixed"


REL_LABEL = {
    "en": {"same": "Same", "friendly": "Friendly", "mixed": "Mixed", "challenging": "Tricky", "open": "Varies"},
    "hi": {"same": "एक जैसे", "friendly": "मित्र", "mixed": "मिला-जुला", "challenging": "चुनौती", "open": "मत अलग"},
}


def combo_chart(lang):
    lab = REL_LABEL[lang]
    head_l = "मूलांक ↓ / भाग्यांक →" if lang == "hi" else "Mulank ↓ / Bhagyank →"
    th = "".join(f"<th>{n}</th>" for n in range(1, 10))
    rows = ""
    for a in range(1, 10):
        cells = "".join(f'<td class="rel rel-{relation(a, b)}">{lab[relation(a, b)]}</td>' for b in range(1, 10))
        rows += f"<tr><th>{a}</th>{cells}</tr>"
    return (f'<div class="table-wrap"><table class="combo"><thead><tr><th>{head_l}</th>{th}</tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')


PEW_US_URL = "https://www.pewresearch.org/religion/2025/05/21/3-in-10-americans-consult-astrology-tarot-cards-or-fortune-tellers/"

POSTS = []
for _f in sorted((Path(__file__).resolve().parent / "posts").glob("*.json")):
    _p = json.loads(_f.read_text())
    _p["faqs"] = [tuple(x) for x in _p["faqs"]]
    _p["related"] = [tuple(x) for x in _p["related"]]
    POSTS.append(_p)
POSTS.sort(key=lambda p: p["published"], reverse=True)


def render_body(p):
    """Fill tokens and add a table of contents built from the post's <section id=..><h2> headings."""
    body = (p["body"].replace("{{CHART_EN}}", combo_chart("en")).replace("{{CHART_HI}}", combo_chart("hi"))
            .replace("{{PEW_US_URL}}", PEW_US_URL).replace("{{PEW_IN_URL}}", PEW_URL))
    heads = re.findall(r'<section id="([^"]+)" class="content-section"><h2>(.*?)</h2>', body)
    if len(heads) >= 3:
        label = "इस लेख में" if p["lang"] == "hi" else "In this guide"
        lis = "".join(f'<li><a href="#{i}">{re.sub("<[^>]+>", "", t)}</a></li>' for i, t in heads)
        body = f'<nav class="toc card" aria-label="Contents"><p class="eyebrow">{label}</p><ol>{lis}</ol></nav>\n' + body
    return body


def post_url(p):
    return ("/hi/blog/" if p["lang"] == "hi" else "/blog/") + p["slug"]


def post_page(p):
    url_path = post_url(p)
    url = SITE + url_path
    hi = p["lang"] == "hi"
    pub = _dt.date.fromisoformat(p["published"])
    date_txt = (f"{pub.day} {MONTHS_HI[pub.month - 1]} {pub.year}" if hi else f"{pub.day} {MONTHS_EN[pub.month - 1]} {pub.year}")
    rel = "".join(f'<li><a class="link" href="{h}">{e(t)}</a></li>' for h, t in p["related"])
    crumbs_home = ("/hi", "भाग्यांक कैलकुलेटर") if hi else ("/", "Bhagyank Calculator")
    body = f"""<main{' lang="hi"' if hi else ''}>
<article class="container narrow num-page blog-post">
<nav class="crumbs xs muted" aria-label="Breadcrumb"><a href="{crumbs_home[0]}">{crumbs_home[1]}</a> <span aria-hidden="true">›</span> <a href="/blog">{"ब्लॉग" if hi else "Blog"}</a> <span aria-hidden="true">›</span> <span>{e(p["h1"])}</span></nav>
<h1 class="post-title">{e(p["h1"])}</h1>
<p class="post-meta xs muted">{"लेखिका" if hi else "By"} <a class="link" href="{AUTHOR['url']}">{"अनन्या शर्मा" if hi else "Ananya Sharma"}</a> · <time datetime="{p['published']}">{date_txt}</time></p>
<p class="lead-left">{e(p["intro"])}</p>
<div class="content">
{render_body(p)}
{section("faq", "अक्सर पूछे जाने वाले सवाल" if hi else "Frequently Asked Questions", faq_block(p["faqs"]))}
<section class="content-section"><h2>{"ये भी पढ़ें" if hi else "Related tools and guides"}</h2><ul>{rel}</ul></section>
<p class="card disclaimer">{"अस्वीकरण: यह लेख पारंपरिक अंक ज्योतिष पर आधारित है और केवल जानकारी के लिए है। इसे पेशेवर सलाह का विकल्प न मानें।" if hi else "Disclaimer: This article is based on traditional numerology and is for information only. It is not a substitute for professional advice."}</p>
</div>
</article>
{reviewed_by(p["lang"])}
{updated_line(p["lang"])}
</main>"""
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "@id": f"{url}#article", "headline": p["h1"], "description": p["desc"], "url": url,
         "inLanguage": p["lang"], "image": f"{SITE}/images/og-image.png", "datePublished": p["published"],
         "dateModified": TODAY.isoformat(), "author": author_schema(),
         "publisher": {"@type": "Organization", "name": "Bhagyank Calculator", "url": SITE,
                       "logo": {"@type": "ImageObject", "url": f"{SITE}/icon-512.png"}}, "mainEntityOfPage": url},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": crumbs_home[1], "item": SITE + (crumbs_home[0] if crumbs_home[0] != "/" else "")},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE}/blog"},
            {"@type": "ListItem", "position": 3, "name": p["h1"], "item": url}]},
        {"@type": "FAQPage", "inLanguage": p["lang"], "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faqs"]]}]}
    return page(path=url_path, lang=p["lang"], title=p["title"], description=p["desc"], body=body, schema=schema)


def blog_index():
    cards = "".join(
        f'<article class="card mini"><p class="eyebrow">{"हिंदी" if p["lang"] == "hi" else "English"}</p>'
        f'<h2 class="h-card"><a href="{post_url(p)}"{" lang=hi" if p["lang"] == "hi" else ""}>{e(p["h1"])}</a></h2>'
        f'<p class="small muted"{" lang=hi" if p["lang"] == "hi" else ""}>{e(p["desc"])}</p>'
        f'<p class="xs"><a class="link" href="{post_url(p)}">{"पूरा लेख पढ़ें" if p["lang"] == "hi" else "Read the guide"}</a></p></article>'
        for p in POSTS)
    body = f"""<main class="container narrow prose-page">
<h1>Numerology Blog</h1>
<p class="lead-left muted">Simple, step-by-step guides on Bhagyank, Mulank, Lo Shu Grid and number matching - in English and Hindi.</p>
<div class="grid-2 mt-lg">{cards}</div>
</main>"""
    schema = {"@context": "https://schema.org", "@type": "Blog", "url": f"{SITE}/blog", "name": "Bhagyank Calculator Blog",
              "author": author_schema(),
              "blogPost": [{"@type": "BlogPosting", "headline": p["h1"], "url": SITE + post_url(p)} for p in POSTS]}
    return page(path="/blog", title="Numerology Blog - Bhagyank, Mulank and Lo Shu Guides",
                description="Simple numerology guides in English and Hindi: Mulank and Bhagyank combinations, marriage matching, Lo Shu Grid and more.",
                body=body, schema=schema)

PAGES = {
    "index.html": home, "hi.html": hindi, "moolank-calculator.html": moolank, "namank-calculator.html": namank,
    "gemstone-recommendation.html": gemstone, "lo-shu-grid-calculator.html": lo_shu_page, "about.html": about, "contact.html": contact,
    "privacy-policy.html": privacy, "terms-and-conditions.html": terms, "404.html": not_found,
}

SITEMAP = [("", "1.0", "weekly"), ("/hi", "0.9", "weekly"), ("/moolank-calculator", "0.9", "weekly"),
           ("/namank-calculator", "0.8", "weekly"), ("/gemstone-recommendation", "0.8", "weekly"),
           ("/about", "0.5", "monthly"), ("/contact", "0.5", "monthly"),
           ("/privacy-policy", "0.3", "yearly"), ("/terms-and-conditions", "0.3", "yearly")] + \
          [(f"/bhagyank/{n}", "0.7", "monthly") for n in range(1, 10)] + \
          [(f"/hi/bhagyank/{n}", "0.7", "monthly") for n in range(1, 10)] + \
          [("/lo-shu-grid-calculator", "0.9", "weekly"), ("/author/ananya-sharma", "0.5", "monthly"),
           ("/blog", "0.6", "weekly")] + [(post_url(p), "0.7", "monthly") for p in POSTS]


def lang_pair(p):
    if p in ("", "/hi"):
        return (SITE, SITE + "/hi")
    m = re.fullmatch(r"(/hi)?/bhagyank/(\d)", p)
    if m:
        return (f"{SITE}/bhagyank/{m.group(2)}", f"{SITE}/hi/bhagyank/{m.group(2)}")
    return None


def sitemap(lastmod):
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for p, pr, cf in SITEMAP:
        out.append("<url>")
        out.append(f"<loc>{SITE}{p}</loc>")
        pair = lang_pair(p)
        if pair:
            out.append(f'<xhtml:link rel="alternate" hreflang="en" href="{pair[0]}"/>')
            out.append(f'<xhtml:link rel="alternate" hreflang="hi" href="{pair[1]}"/>')
            out.append(f'<xhtml:link rel="alternate" hreflang="x-default" href="{pair[0]}"/>')
        out.append(f"<lastmod>{lastmod}</lastmod><changefreq>{cf}</changefreq><priority>{pr}</priority>")
        out.append("</url>")
    out.append("</urlset>")
    return "\n".join(out) + "\n"


def main():
    import datetime
    (PUB / "assets").mkdir(parents=True, exist_ok=True)
    (PUB / "images").mkdir(parents=True, exist_ok=True)
    for name, fn in PAGES.items():
        (PUB / name).write_text(fn())
    (PUB / "bhagyank").mkdir(exist_ok=True)
    (PUB / "hi" / "bhagyank").mkdir(parents=True, exist_ok=True)
    for n in range(1, 10):
        (PUB / "bhagyank" / f"{n}.html").write_text(number_page(n))
        (PUB / "hi" / "bhagyank" / f"{n}.html").write_text(number_page_hi(n))
    (PUB / "author").mkdir(exist_ok=True)
    (PUB / "author" / "ananya-sharma.html").write_text(author_page())
    (PUB / "blog").mkdir(exist_ok=True)
    (PUB / "hi" / "blog").mkdir(parents=True, exist_ok=True)
    (PUB / "blog.html").write_text(blog_index())
    for p in POSTS:
        (PUB / (post_url(p).lstrip("/") + ".html")).write_text(post_page(p))
    (PUB / "favicon.svg").write_text(FAVICON_SVG)
    (PUB / "site.webmanifest").write_text(json.dumps({
        "name": "Bhagyank Calculator", "short_name": "Bhagyank", "start_url": "/", "display": "standalone",
        "background_color": "#1a1636", "theme_color": "#1a1636",
        "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=2))
    (PUB / "ads.txt").write_text(f"google.com, {ADSENSE.replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n")
    (PUB / "sitemap.xml").write_text(sitemap(datetime.date.today().isoformat()))
    (PUB / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    # data for the calculators
    js = (HERE / "app.js").read_text().replace(
        "/*__DATA__*/", "const DATA = " + json.dumps({"en": EN, "hi": HI}, ensure_ascii=False) + ";")
    (PUB / "assets" / "app.js").write_text(js)
    shutil.copy(HERE / "style.css", PUB / "assets" / "style.css")
    for f in ["og-image.png", "ananya-sharma.jpg"]:
        assert (PUB / "images" / f).exists(), f"missing public/images/{f}"


if __name__ == "__main__":
    main()
