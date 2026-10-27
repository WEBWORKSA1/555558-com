"""Shared layout for the 555558 Prosperity Lab static site.
Every page is built from page() so header, inquiry ribbon, ads code, footer and
legal links stay identical across the site. Run `python3 _src/build.py` from the repo root."""
import json, html

SITE = "https://555558.com"
NAME = "555558 Prosperity Lab"
ADSENSE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>'
UPDATED = "October 27, 2026"

NAV = [
    ("index.html", "Home"),
    ("tools.html", "Tools"),
    ("guides.html", "Guides"),
    ("555558-meaning.html", "555558 decoded"),
    ("videos.html", "Videos"),
    ("community.html", "Contests & careers"),
    ("support.html", "Support"),
]


def nav_html(root, current):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'<a href="{root}{href}"{cur}>{label}</a>')
    items.append(f'<a class="cta" href="{root}audit.html">Free audit</a>')
    return "\n      ".join(items)


def footer_html(root):
    return f'''
<section class="block dark" aria-labelledby="nl-h">
  <div class="wrap two-col">
    <div>
      <h2 id="nl-h">One lucky number, every Monday</h2>
      <p class="section-intro">A short email with a number worth knowing: a pricing experiment, a numeric domain sale, a cultural fact you can use in your next launch. Unsubscribe in one click.</p>
    </div>
    <form class="card" data-form="Newsletter" aria-label="Newsletter signup">
      <div class="field"><label for="nl-email">Email address</label><input id="nl-email" name="email" type="email" required autocomplete="email" placeholder="you@company.com"></div>
      <div class="field"><label for="nl-int">I mostly care about</label>
        <select id="nl-int" name="interest"><option>Pricing psychology</option><option>Numeric domains</option><option>Lucky numbers & culture</option><option>All of it</option></select></div>
      <label class="consent"><input type="checkbox" name="consent" value="yes" required> I agree to receive the newsletter and accept the <a href="{root}privacy.html">privacy policy</a>.</label>
      <div class="hp"><input name="_gotcha" tabindex="-1" autocomplete="off"></div>
      <button class="btn gold" type="submit">Subscribe</button>
      <p class="form-status" role="status"></p>
    </form>
  </div>
</section>
<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="{root}index.html" style="color:#fff"><span>55555<span class="eight">8</span></span></a>
        <p class="mt">Free tools and plain-English guides on how numbers move money: price endings, lucky digits, phone numbers, numeric domains and launch timing.</p>
        <p><a href="#" data-mail="Inquiry from 555558.com">Email the team</a></p>
      </div>
      <div><h4>Tools</h4><ul>
        <li><a href="{root}tools/number-analyzer.html">Number analyzer</a></li>
        <li><a href="{root}tools/lucky-price.html">Lucky price finder</a></li>
        <li><a href="{root}tools/margin-markup.html">Margin & markup</a></li>
        <li><a href="{root}tools/phone-number-scorer.html">Phone number scorer</a></li>
        <li><a href="{root}tools/domain-grader.html">Numeric domain grader</a></li>
        <li><a href="{root}tools/launch-date.html">Launch date finder</a></li>
        <li><a href="{root}tools/life-path.html">Life path number</a></li></ul></div>
      <div><h4>Learn</h4><ul>
        <li><a href="{root}guides.html">All guides</a></li>
        <li><a href="{root}555558-meaning.html">555558 decoded</a></li>
        <li><a href="{root}glossary.html">Glossary</a></li>
        <li><a href="{root}videos.html">Videos</a></li>
        <li><a href="{root}faq.html">FAQ</a></li></ul></div>
      <div><h4>Work with us</h4><ul>
        <li><a href="{root}audit.html">Free number audit</a></li>
        <li><a href="{root}advertise.html">Advertise & sponsor</a></li>
        <li><a href="{root}community.html#contests">Contests</a></li>
        <li><a href="{root}community.html#careers">Careers</a></li>
        <li><a href="{root}support.html">Support the lab</a></li>
        <li><a href="{root}contact.html">Contact</a></li></ul></div>
      <div><h4>Policies</h4><ul>
        <li><a href="{root}about.html">About</a></li>
        <li><a href="{root}editorial-policy.html">Editorial policy</a></li>
        <li><a href="{root}privacy.html">Privacy</a></li>
        <li><a href="{root}terms.html">Terms</a></li>
        <li><a href="{root}cookies.html">Cookies</a></li>
        <li><a href="{root}disclaimer.html">Disclaimer</a></li>
        <li><a href="{root}trademark-copyright.html">Trademark & copyright</a></li></ul></div>
    </div>
    <div class="foot-legal">
      <p>&copy; <span data-year>2026</span> 555558.com. Original content and tools of this website. The numeral string "555558" is used descriptively as a domain name; no exclusive trademark rights in the number itself are claimed, and no affiliation with any company using similar numbers is implied. See <a href="{root}trademark-copyright.html">trademark &amp; copyright notice</a>.</p>
      <p>Tools and guides are educational and for entertainment. Numerology and lucky-number traditions are cultural beliefs, not scientific predictions or financial advice.</p>
    </div>
  </div>
</footer>
<div class="cookie" role="dialog" aria-label="Cookie notice">
  We use cookies for essential site functions and, with your consent, for Google AdSense ads and measurement. <a href="{root}cookies.html">Cookie policy</a>.
  <div class="acts"><button class="btn sm" data-cookie="all">Accept all</button><button class="btn ghost sm" data-cookie="essential">Essential only</button></div>
</div>
<a class="sticky-support" href="{root}support.html">Support the lab</a>
'''


def page(*, path, title, desc, body, root="", current="", schema=None, tools_js=False, og_type="website"):
    url = SITE + "/" + ("" if path == "index.html" else path)
    ld = [{
        "@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": SITE + "/",
        "potentialAction": {"@type": "SearchAction", "target": SITE + "/tools/number-analyzer.html?n={query}", "query-input": "required name=query"}
    }, {"@context": "https://schema.org", "@type": "Organization", "name": NAME, "url": SITE + "/", "logo": SITE + "/assets/img/logo.svg"}]
    if schema:
        ld.extend(schema if isinstance(schema, list) else [schema])
    ld_html = "\n".join(f'<script type="application/ld+json">{json.dumps(x)}</script>' for x in ld)
    t = html.escape(title)
    d = html.escape(desc)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0E3B34">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/og.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="google-adsense-account" content="ca-pub-6620975821265271">
<link rel="icon" href="{root}assets/img/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="{root}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,500;12..96,600;12..96,700;12..96,800&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/css/style.css">
{ADSENSE}
{ld_html}
</head>
<body data-root="{root}">
<a class="skip" href="#main">Skip to content</a>
<div class="ribbon">Contact, if you are interested in this website/domain name/Sponsorship/Advertisement/Partnership &mdash; <a href="https://web.works/contact" target="_blank" rel="noopener">web.works/contact</a></div>
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="{root}index.html" aria-label="{NAME} home">
      <span>55555<span class="eight">8</span><small>Prosperity Lab</small></span>
    </a>
    <button class="menu-btn" aria-expanded="false" aria-controls="mainnav">Menu</button>
    <nav class="main" id="mainnav" aria-label="Main">
      {nav_html(root, current)}
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
{footer_html(root)}
<script src="{root}assets/js/main.js" defer></script>
{f'<script src="{root}assets/js/tools.js" defer></script>' if tools_js else ''}
</body>
</html>
'''


def page_head(title, intro, crumbs, root=""):
    c = f'<a href="{root}index.html">Home</a>' + "".join(
        f' / <a href="{root}{h}">{l}</a>' if h else f" / {l}" for h, l in crumbs)
    return f'''<div class="page-head"><div class="wrap">
  <div class="crumbs">{c}</div>
  <h1>{title}</h1>
  <p class="muted narrow" style="font-size:1.2rem">{intro}</p>
</div></div>'''


def faq_block(items):
    out = "".join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in items)
    schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": html.unescape(q), "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)}} for q, a in items]}
    return out, schema


def form_tail(root):
    return f'''<label class="consent"><input type="checkbox" name="consent" value="yes" required> I agree that 555558.com may contact me about this request, as described in the <a href="{root}privacy.html">privacy policy</a>.</label>
<div class="hp"><input name="_gotcha" tabindex="-1" autocomplete="off"></div>'''
