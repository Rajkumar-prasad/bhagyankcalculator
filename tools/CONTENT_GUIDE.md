# Content guide - bhagyank-calculator.online blog

Every blog post exists to help a real reader **and** to support one of the tool pages so it ranks.
Follow this guide exactly. Owner: Raj. Author shown on posts: Ananya Sharma (अनन्या शर्मा), a pen name.

## 1. Workflow for one post (do the steps in order)
1. **Pick the topic**: take the first unchecked line in `tools/TOPICS.md`. Check `tools/posts/` and the
   site pages (section 4) so the new post does not compete with a page that already targets the same keyword.
   If it would, adjust the angle or skip to the next topic and note why in TOPICS.md.
2. **Research**: search the web for the keyword. Read the top results and the "People also ask" style questions.
   Note what searchers want (intent), what the top pages cover, and what they miss.
3. **Content strategy**: decide the one main keyword, 4-8 related terms/entities (planets, Hindi and English
   spellings, related numbers), the tool page this post supports, and the 1 statistic you will use.
4. **Outline**: H1, a 2-4 sentence intro that answers the question directly, 5-7 H2 sections written as the
   questions people ask, then FAQ (3-5 questions). Plan the internal links before writing.
5. **Write** the post as a JSON file (section 3), then update internal links (section 5), then build and check (section 6).

## 2. Writing rules (mandatory)
- Write like a real person for a 6th-7th grade reader: short sentences, everyday words, one idea per paragraph,
  paragraphs of 1-3 sentences. Talk to the reader as "you". Mix sentence lengths so it reads naturally.
- Answer the main question in the first 2-4 sentences (no long warm-up). Each H2 answers one real question.
- Follow Google's helpful-content guidance: original value (examples, worked calculations, tables), no fluff,
  no keyword stuffing, no made-up facts, no promises about the future. Present numerology as traditional
  guidance, not guaranteed truth. Never invent credentials, studies, quotes or personal stories.
- Style: semantic SEO (cover the topic's entities and sub-questions fully, use the Hindi and English spellings
  people search: Bhagyank/भाग्यांक, Mulank/Moolank/मूलांक), Backlinko/Neil Patel clarity (scannable, examples,
  lists, tables), Koray-style topical structure (headings follow the searcher's questions in a logical order).
- **Idioms**: add 1-2 natural idioms or sayings per post, only where they fit. Not in every section.
  Never reuse the idioms already used on the site: "no man is an island", "wear their heart on their sleeve",
  "knowledge is power", "march to the beat of their own drum", "jack of all trades", "home is where the heart is",
  "still waters run deep", "slow and steady wins the race", "short fuse", "smooth seas never made a skilled
  sailor", "don't make a mountain out of a molehill", "ताली दोनों हाथों से बजती है", "देर आए दुरुस्त आए",
  "लीक से हटकर", "अकेला चना भाड़ नहीं फोड़ सकता", "जैसी संगत वैसी रंगत", "बाल की खाल", "ईंट का जवाब पत्थर से", "एकीचे बळ", "संगत तशी रंगत", "ज्ञान वाटल्याने वाढते", "चाकोरीबाहेर", "हरहुन्नरी",
  "मन जिंकणे", "कीस पाडणे", "धीर धरी रे धीरापोटी", "रागाच्या भरात बोललेले शब्द".
- **Exactly 1 statistic** per post that shows authority, linked on a 3-4 word anchor (e.g. "Pew Research Center
  survey", "Pew Research के सर्वे") to the page that proves it. Verify the number on the source page yourself
  before using it. Prefer a different verified statistic from the previous posts when one fits; the Pew figures
  already verified are: India 2021 - 29,999 adults surveyed, 49% of Hindus believe in astrology
  (`{{PEW_IN_URL}}`, Marathi anchor "Pew Research च्या सर्वेक्षणात"); US 2024 - 3 in 10 adults consult astrology, tarot cards or fortune tellers (`{{PEW_US_URL}}`).
- Use regular hyphens " - ", never em dashes.
- Length: 1,000-1,500 words. Language: as listed in TOPICS.md (Hindi posts in simple Hindi; English
  words like "numerology" are fine where people actually use them).
- Hindi posts: `lang` "hi", slug in romanised Hindi (e.g. `mulank-aur-bhagyank-me-antar`). Marathi posts: `lang` "mr"
  (simple, natural Marathi; e.g. `bhagyank-kasa-kadhaycha`). Live URLs: EN `/blog/<slug>`, HI `/hi/blog/<slug>`, MR `/mr/blog/<slug>`.

## 3. Post file format
Create `tools/posts/YYYY-MM-DD-<slug>.json` (date = today, IST):
```json
{
 "slug": "lucky-number-by-date-of-birth",
 "lang": "en",
 "published": "2026-11-25",
 "title": "SEO title, max ~60 characters, main keyword first",
 "desc": "Meta description, 140-160 characters, says what the reader gets",
 "h1": "Reader-facing headline",
 "intro": "2-4 sentence direct answer (plain text, no HTML)",
 "body": "<section id=\"short-id\" class=\"content-section\"><h2>Question?</h2><p>...</p></section> ...",
 "faqs": [["Question?", "Answer in plain text."]],
 "related": [["/lo-shu-grid-calculator", "Lo Shu Grid Calculator"], ["/blog/mulank-bhagyank-combination", "..."]]
}
```
Body rules: only `<section id=".." class="content-section"><h2>..</h2> ... </section>` blocks (the table of contents
is built automatically from them). Allowed inside: `p, ul, ol, li, strong, em, a, table` (wrap tables in
`<div class="table-wrap">`), `<div class="card example">` for worked examples, `<p class="small">` for notes.
Links: internal `<a class="link" href="/path">`; the statistic link adds `target="_blank" rel="noopener"`.
Tokens you may use: `{{CHART_EN}}` / `{{CHART_HI}}` (the 9x9 Mulank-Bhagyank chart), `{{PEW_IN_URL}}`, `{{PEW_US_URL}}`.
Do not add the FAQ, author box, disclaimer or related list to the body - the template adds them.

## 4. Site map (link targets)
Tool pages (the money pages - every post must link to its target tool at least twice, with varied anchors):
- `/` Bhagyank Calculator (EN) · `/hi` भाग्यांक कैलकुलेटर (HI) · `/mr` भाग्यांक कॅल्क्युलेटर (MR) · calculator anchors: `/#calculator`, `/hi#calculator`, `/mr#calculator`
- `/moolank-calculator` Moolank (Mulank) Calculator · `/namank-calculator` Namank (name number) Calculator
- `/lo-shu-grid-calculator` Lo Shu Grid Calculator · `/gemstone-recommendation` gemstone guide
Meaning pages: `/bhagyank/1` ... `/bhagyank/9` (EN), `/hi/bhagyank/1` ... `/hi/bhagyank/9` (HI), `/mr/bhagyank/1` ... `/mr/bhagyank/9` (MR)
Author: `/author/ananya-sharma` · Blog index: `/blog` · existing posts: see `tools/posts/`.

## 5. Internal linking (every post)
- 4-8 internal links in the body: 2+ to the target tool page, 1-3 to the matching `/bhagyank/N` or
  `/hi/bhagyank/N` pages, 1-2 to related posts. Use descriptive anchors (3-6 words), vary them, never
  "click here", and don't repeat the exact same anchor twice in one post.
- Hindi posts link to Hindi pages, Marathi posts to Marathi pages (`/mr`, `/mr/bhagyank/N`), English posts to English pages.
- Marathi posts: `lang` "mr", slug in romanised Marathi; they are published at `/mr/blog/<slug>`.
- After writing, add a link **to the new post** from 1-2 older related posts: add it to their `related` list and,
  where it reads naturally, one in-text link in a body paragraph.
- `related` in the new post: 3-5 entries (tool page first).

## 6. Build, check, publish
From the repo root:
```
python3 tools/build.py && cp tools/style.css public/assets/style.css && python3 tools/check.py
```
`check.py` must print `ALL CHECKS PASSED`. Fix anything it reports. Then commit (message: `Blog: <title>`) and
push to `main`. Cloudflare deploys `main` automatically (Workers build for project `bhagyankcalculator`).
Finally tick the topic in `tools/TOPICS.md` with the date and URL (commit that in the same commit).
The build records each page's real last-changed date in `tools/lastmod.json` (used for `sitemap.xml`, the
"Last updated" line and `dateModified`). Always commit that file too, and never edit dates in it by hand.
New pages are added to `sitemap.xml` and the `/sitemap` page automatically.
