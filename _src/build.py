"""Builds every HTML page of 555558.com into the repo root.
Usage (from repo root):  python3 _src/build.py
Edit content here or in guides.py, rebuild, commit. GitHub Pages serves the output."""
import os, sys, datetime
sys.path.insert(0, os.path.dirname(__file__))
from layout import page, page_head, faq_block, form_tail, SITE, UPDATED
from guides import GUIDES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = []

# Optional direct payment links. Leave empty and supporters use the pledge form;
# the team replies with payment details. Paste a Stripe Payment Link, PayPal.me,
# Buy Me a Coffee or Ko-fi URL here to show a direct "Pay now" button.
DONATE_LINKS = {
    # "PayPal": "https://paypal.me/yourname",
    # "Card (Stripe)": "https://buy.stripe.com/xxxx",
}

# YouTube library. Add an 11-character video id to embed it in place;
# with no id the card opens a curated YouTube search instead.
VIDEOS = [
    ("Pricing psychology", "Why prices end in .99", "How the left-digit effect shapes what shoppers think a price is.", "", "charm pricing left digit effect explained"),
    ("Pricing psychology", "Price anchoring in practice", "Decoy tiers, reference prices and why the middle option sells.", "", "price anchoring decoy effect explained"),
    ("Culture", "Why 8 is lucky in China", "The sound, the history and where you see it in daily life.", "", "why is 8 a lucky number in chinese culture"),
    ("Culture", "Lucky and unlucky numbers around the world", "4, 7, 8, 13 and 17 across cultures.", "", "lucky and unlucky numbers around the world"),
    ("Domains", "How numeric domains are valued", "Length, extension and buyer demand in the all-number market.", "", "numeric domain names value chinese premium"),
    ("Branding", "Memorable phone numbers for business", "Vanity and pattern numbers compared.", "", "vanity phone number business marketing"),
    ("AI", "How dynamic pricing algorithms work", "From airline fares to e-commerce repricers.", "", "how dynamic pricing algorithms work"),
    ("Math", "Number facts that feel like magic", "Repdigits, palindromes and why patterns are easy to remember.", "", "repdigit numbers palindromes numberphile"),
    ("Strategy", "Choosing a launch date", "Practical and cultural timing for a product launch.", "", "best day to launch a product strategy"),
]

TOOLS = [
    ("number-analyzer", "#", "Number analyzer", "Factorisation, bases, words, digit root, patterns and a prosperity score for any number."),
    ("lucky-price", "$", "Lucky price finder", "Charm, 8-ending, shagun and round price points for the market you sell to."),
    ("margin-markup", "%", "Margin & markup", "Fill any two of cost, price, margin or markup; the rest solves itself."),
    ("phone-number-scorer", "☎", "Phone number scorer", "Memorability and lucky-digit score, plus a word-to-keypad converter."),
    ("domain-grader", ".", "Numeric domain grader", "Score an all-number domain on length, extension, pattern and digits."),
    ("launch-date", "8", "Launch date finder", "Rank dates in any window by 8s, 4s and patterns, with weekends optional."),
    ("life-path", "∞", "Life path number", "Life path and name numbers, for fun and reflection."),
]


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    OUT.append(path)


def tool_rows(root):
    return "".join(f'<a class="tool-row" href="{root}tools/{s}.html"><span class="glyph" aria-hidden="true">{g}</span><span><h3>{t}</h3><p>{d}</p></span></a>' for s, g, t, d in TOOLS)


def guide_cards(root, items=None):
    items = items or GUIDES
    return "".join(f'<a class="guide" href="{root}guides/{g["slug"]}.html"><span class="meta">{g["tag"]}, {g["minutes"]} min read</span><h3>{g["title"]}</h3><p>{g["desc"]}</p></a>' for g in items)


def audit_form(root, compact=False):
    return f'''<form class="card" data-form="Number Audit lead" data-steps aria-label="Free number audit request">
  <div class="steps" aria-hidden="true"><span></span><span></span><span></span></div>
  <div class="step">
    <h3>What should we look at?</h3>
    <div class="field"><span class="field-label" style="font:600 .92rem var(--display);color:var(--jade);display:block;margin-bottom:8px">Pick everything that applies</span>
      <div class="chips">
        <label><input type="checkbox" name="audit_items" value="Price points"> Price points</label>
        <label><input type="checkbox" name="audit_items" value="Phone number"> Phone number</label>
        <label><input type="checkbox" name="audit_items" value="Domain name"> Domain name</label>
        <label><input type="checkbox" name="audit_items" value="Launch date"> Launch date</label>
        <label><input type="checkbox" name="audit_items" value="Address or unit number"> Address</label>
        <label><input type="checkbox" name="audit_items" value="AI pricing rules"> AI pricing rules</label>
      </div></div>
    <div class="field"><label for="a-market">Main customers</label>
      <select id="a-market" name="market" required><option value="">Choose one</option><option>North America / Europe</option><option>Chinese-speaking markets</option><option>India / South Asia</option><option>Southeast Asia</option><option>Global / mixed</option></select></div>
    <button type="button" class="btn" data-next>Continue</button>
  </div>
  <div class="step">
    <h3>About your business</h3>
    <div class="row2">
      <div class="field"><label for="a-biz">Business or project name</label><input id="a-biz" name="business" required></div>
      <div class="field"><label for="a-site">Website (optional)</label><input id="a-site" name="website" type="url" placeholder="https://"></div>
    </div>
    <div class="row2">
      <div class="field"><label for="a-ind">Industry</label><select id="a-ind" name="industry"><option>Retail / e-commerce</option><option>Real estate</option><option>Restaurants & hospitality</option><option>Professional services</option><option>SaaS / software</option><option>Domains / digital assets</option><option>Other</option></select></div>
      <div class="field"><label for="a-rev">Monthly revenue</label><select id="a-rev" name="revenue"><option>Pre-launch</option><option>Under $10k</option><option>$10k–$100k</option><option>$100k–$1M</option><option>Over $1M</option></select></div>
    </div>
    <div class="field"><label for="a-goal">What would a win look like?</label><textarea id="a-goal" name="goal" placeholder="Example: pick prices for our Lunar New Year gift sets that convert better than last year."></textarea></div>
    <button type="button" class="btn ghost" data-prev>Back</button> <button type="button" class="btn" data-next>Continue</button>
  </div>
  <div class="step">
    <h3>Where should we send it?</h3>
    <div class="row2">
      <div class="field"><label for="a-name">Your name</label><input id="a-name" name="name" required autocomplete="name"></div>
      <div class="field"><label for="a-email">Work email</label><input id="a-email" name="email" type="email" required autocomplete="email"></div>
    </div>
    <div class="field"><label for="a-phone">Phone or WhatsApp (optional)</label><input id="a-phone" name="phone" type="tel" autocomplete="tel"></div>
    {form_tail(root)}
    <button type="button" class="btn ghost" data-prev>Back</button> <button class="btn gold" type="submit">Get my free audit</button>
    <p class="form-status" role="status"></p>
  </div>
</form>'''


# ---------------------------------------------------------------- home
def build_home():
    faq_items = [
        ("What is 555558.com?", "A free lab of tools and guides about how numbers influence buying decisions: price endings, lucky and unlucky digits, memorable phone numbers, numeric domains and launch timing."),
        ("Are the tools really free?", "Yes. Every calculator runs in your browser, needs no account and sends nothing to a server. The site is funded by advertising, sponsors and supporters."),
        ("Is any of this scientific?", "The pricing tools are based on published consumer research and plain arithmetic. Lucky-number and numerology content describes cultural beliefs and is offered for interest and entertainment, not as prediction."),
        ("Who is the free audit for?", "Businesses choosing prices, phone numbers, domains or launch dates, especially when selling across cultures. You get a short written review of the numbers you send us."),
    ]
    faq, faq_schema = faq_block(faq_items)
    body = f'''
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <h1>Numbers sell. Find out how yours read.</h1>
      <p class="lede">Five fives for change, one eight for prosperity. Type a price, phone number, domain or date to see how buyers in different markets will read it.</p>
      <div class="digits num" id="hero-digits" aria-live="polite" aria-label="Your number"></div>
      <div class="analyzer">
        <label class="skip" for="hero-num">Type any number</label>
        <input id="hero-num" inputmode="numeric" maxlength="12" value="555558" aria-describedby="hero-help" autocomplete="off">
        <a class="btn gold" id="hero-more" href="tools/number-analyzer.html?n=555558">Full analysis</a>
      </div>
      <p id="hero-help" class="muted" style="font-size:.95rem;margin-top:10px">Up to 12 digits. Everything runs in your browser.</p>
    </div>
    <aside class="readout" aria-label="Live readout">
      <h2>Live readout</h2>
      <dl>
        <dt>Digit sum</dt><dd id="r-sum"></dd>
        <dt>Numerology root</dt><dd id="r-root"></dd>
        <dt>Prime factors</dt><dd id="r-fact"></dd>
        <dt>Divisors</dt><dd id="r-div"></dd>
        <dt>Lucky / unlucky</dt><dd id="r-8"></dd>
        <dt>Memorability</dt><dd><span id="r-mem"></span><div class="meter"><span id="m-mem"></span></div></dd>
        <dt>Prosperity</dt><dd><span id="r-pros"></span><div class="meter"><span id="m-pros"></span></div></dd>
      </dl>
      <p class="verdict" id="r-verdict"></p>
    </aside>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <div class="facts">
      <div class="fact"><b>2.25M ¥</b><span>paid at auction in 2020 for a phone number ending in five 8s</span></div>
      <div class="fact"><b>$39 &gt; $34</b><span>a 9-ending outsold a cheaper price in a classic catalogue test</span></div>
      <div class="fact"><b>100,000</b><span>five-digit .com names exist, and every one is registered</span></div>
      <div class="fact"><b>8:08 pm</b><span>start time of the Beijing Olympics, on 08/08/08</span></div>
    </div>
  </div>
</section>

<section class="block alt" aria-labelledby="tools-h">
  <div class="wrap">
    <h2 id="tools-h">Seven free tools</h2>
    <p class="section-intro">Each one answers a real decision: what to charge, which number to print on the van, whether a domain is any good, which day to open.</p>
    <div class="tool-list">{tool_rows("")}</div>
  </div>
</section>

<section class="block" aria-labelledby="lead-h" id="audit">
  <div class="wrap lead">
    <div>
      <h2 id="lead-h">Get a free number audit for your business</h2>
      <p class="section-intro">Send us your prices, phone number, domain or launch window. Within two business days you get a written review of how each one reads to your customers, with specific alternatives.</p>
      <ul class="ticks">
        <li>Price endings matched to your market: 9, 8, 88, round or shagun</li>
        <li>Phone and domain memorability, with 4s and other red flags called out</li>
        <li>Three ranked launch dates inside the window that suits you</li>
        <li>Plain-English notes you can act on the same day</li>
      </ul>
      <p class="muted" style="font-size:1rem">No sales call required. We review a limited number each week.</p>
    </div>
    {audit_form("")}
  </div>
</section>

<section class="block alt" aria-labelledby="guides-h">
  <div class="wrap">
    <h2 id="guides-h">Guides</h2>
    <p class="section-intro">Research-backed, written for people who set prices and choose names.</p>
    <div class="guide-grid">{guide_cards("", GUIDES[:6])}</div>
    <p class="mt"><a class="btn ghost" href="guides.html">All guides</a></p>
  </div>
</section>

<section class="block" aria-labelledby="daily-h">
  <div class="wrap two-col">
    <div>
      <h2 id="daily-h">Today's number</h2>
      <p class="section-intro">A new six-digit number each day, with no 4s. Open it in the analyzer and see what it says.</p>
      <p class="num" style="font:800 3.4rem/1 var(--display);color:var(--jade)" id="daily-num">555558</p>
      <a class="btn" id="daily-link" href="tools/number-analyzer.html">Analyze today's number</a>
    </div>
    <div>
      <h2>Questions</h2>
      {faq}
    </div>
  </div>
</section>

<section class="block alt" aria-labelledby="sup-h">
  <div class="wrap two-col">
    <div>
      <h2 id="sup-h">Keep the lab free</h2>
      <p class="section-intro">Supporters pay for new tools, research, monthly contests and the writers and developers who build them.</p>
      <a class="btn gold" href="support.html">Support the lab</a>
    </div>
    <div>
      <h2>Sponsor or partner</h2>
      <p class="section-intro">Reach founders, marketers and domain investors who care about pricing and naming. Sponsorships, tool placements and partnerships are open.</p>
      <a class="btn gold" href="advertise.html">See sponsorship options</a>
    </div>
  </div>
</section>'''
    write("index.html", page(path="index.html", title="555558 Prosperity Lab — free tools on how numbers sell",
                             desc="Free tools and guides on pricing psychology, lucky numbers, memorable phone numbers, numeric domains and launch dates. Type any number to see how buyers read it.",
                             body=body, current="index.html", schema=faq_schema, tools_js=True))


# ---------------------------------------------------------------- tools
TOOL_PAGES = {
"number-analyzer": dict(
    title="Number analyzer", desc="Analyze any number: prime factors, divisors, binary, hex, words, digit sum, numerology root, digit patterns and an 8/4 prosperity score.",
    intro="Enter any whole number up to 15 digits. Get its math profile, its digit patterns and how it reads in lucky-number cultures.",
    form='''<form id="an-form" class="panel"><div class="field"><label for="an-in">Number</label><input id="an-in" inputmode="numeric" maxlength="15" required></div><button class="btn" type="submit">Analyze</button></form>''',
    out='<div class="panel result" id="an-out" aria-live="polite"></div>',
    explain="""<h2>How the analyzer works</h2>
<p>The math side is exact: trial division finds the prime factors, the divisor count comes from the exponents of those factors, and bases are standard conversions. The numerology root adds the digits repeatedly until one digit remains, keeping 11, 22 and 33 as master numbers.</p>
<p>The <b>memorability</b> score rewards fewer distinct digits, runs and recognisable patterns, and penalises length. The <b>prosperity</b> score adds points for 8 (and a little for 6 and 9) and subtracts for 4, based on Chinese sound-alike meanings. Both are comparative guides, not absolute measures.</p>
<h2>Worked example: 555558</h2>
<p>555558 factors as 2 × 3 × 92,593, so it has 8 divisors. Its digits add to 33, a master number in numerology. It is a run-plus-kicker pattern, scores high on memorability, and contains one 8 and no 4s.</p>""",
    faq=[("What's the largest number I can enter?", "Up to 15 digits. Larger numbers lose precision in browser arithmetic."), ("Can I share a result?", "Yes. The page address updates with your number, so copy and send the link.")]),
"lucky-price": dict(
    title="Lucky price finder", desc="Turn any price into charm (.99), 8-ending, 88, shagun and round price points matched to Western, Chinese, Indian or premium buyers.",
    intro="Enter the price you have in mind and who you sell to. Get price points that read well to that audience, with the reason for each.",
    form='''<form id="lp-form" class="panel"><div class="field"><label for="lp-price">Your price</label><input id="lp-price" type="number" min="0.01" step="0.01" value="47.20" required></div>
<div class="field"><label for="lp-market">Main buyers</label><select id="lp-market"><option value="global">Global / mixed</option><option value="west">North America / Europe</option><option value="china">Chinese-speaking</option><option value="india">India / South Asia</option><option value="premium">Luxury / premium</option></select></div>
<button class="btn" type="submit">Find price points</button></form>''',
    out='<div class="panel result" id="lp-out" aria-live="polite"></div>',
    explain="""<h2>Why these endings</h2>
<ul><li><b>.99 and just-below</b> use the left-digit effect: buyers anchor on the first digit.</li>
<li><b>8, 88, 888 and 68</b> carry prosperity meaning for Chinese-speaking buyers; 4 is avoided.</li>
<li><b>Endings in 1</b> follow the Indian shagun custom for auspicious amounts (101, 501, 1,001).</li>
<li><b>Round numbers</b> signal quality in luxury and professional services.</li></ul>
<p>Only suggestions within about 35% of your price are shown. Read the full <a href="../guides/charm-pricing-9-vs-8.html">charm pricing guide</a>.</p>""",
    faq=[("Will an 8-ending hurt sales with Western buyers?", "It mostly goes unnoticed, but it gives up the left-digit benefit of a 9. For mixed audiences, test both."), ("Does this include tax?", "No. Apply your ending to the price customers actually see, after tax where prices are shown tax-inclusive.")]),
"margin-markup": dict(
    title="Margin & markup calculator", desc="Fill in any two of cost, price, margin and markup to solve the rest. Avoid the common mistake of confusing markup with margin.",
    intro="Enter any two values. The calculator solves the others and links to price endings for the result.",
    form='''<form id="mm-form" class="panel"><div class="row2"><div class="field"><label for="mm-cost">Cost</label><input id="mm-cost" type="number" step="0.01" min="0"></div><div class="field"><label for="mm-price">Selling price</label><input id="mm-price" type="number" step="0.01" min="0"></div></div>
<div class="row2"><div class="field"><label for="mm-margin">Gross margin %</label><input id="mm-margin" type="number" step="0.01" max="99.99"></div><div class="field"><label for="mm-markup">Markup %</label><input id="mm-markup" type="number" step="0.01" min="0"></div></div>
<button class="btn" type="submit">Calculate</button> <button class="btn ghost" type="reset">Clear</button></form>''',
    out='<div class="panel result" id="mm-out" aria-live="polite"><p>Fill in any two fields, then calculate.</p></div>',
    explain="""<h2>Formulas</h2>
<p><b>Markup</b> = (price − cost) ÷ cost. <b>Margin</b> = (price − cost) ÷ price. Price from margin = cost ÷ (1 − margin). Price from markup = cost × (1 + markup).</p>
<p>Example: cost 60 with a 40% target margin needs a price of 100, not 84. Read <a href="../guides/margin-vs-markup.html">margin vs markup</a> for the full table.</p>""",
    faq=[("Can margin be 100%?", "No. A 100% margin would mean zero cost. Markup has no upper limit."), ("Which should I report?", "Accountants and investors usually talk margin; buyers and wholesalers often talk markup. Say which one you mean.")]),
"phone-number-scorer": dict(
    title="Phone number scorer", desc="Score a phone number for memorability and lucky digits, and convert vanity words to keypad digits.",
    intro="Type a number, or letters like 1-800-GET-LUCK. We convert letters to keypad digits and score how easy the number is to remember.",
    form='''<form id="ph-form" class="panel"><div class="field"><label for="ph-in">Phone number or vanity word</label><input id="ph-in" value="555-5558" required></div><button class="btn" type="submit">Score it</button></form>''',
    out='<div class="panel result" id="ph-out" aria-live="polite"><p>Your score appears here.</p></div>',
    explain="""<h2>What the score measures</h2>
<p>Memorability is computed on the last seven digits, the part people actually remember. The overall score weights memorability at 60% and the prosperity (8/4) score at 40%. A high score is most valuable when customers find you through radio, outdoor or vehicle ads rather than a tap-to-call link.</p>
<p>More in our guide to <a href="../guides/vanity-phone-numbers.html">vanity and lucky phone numbers</a>.</p>""",
    faq=[("Does this check if a number is available?", "No. It only scores the number you type. Ask your carrier or a number provider about availability."), ("Why ignore the area code?", "Customers usually know or assume the area code; the local part is what they must remember.")]),
"domain-grader": dict(
    title="Numeric domain grader", desc="Grade an all-number domain name on length, extension, memorability, patterns and lucky digits.",
    intro="Enter a numbers-only domain such as 555558.com. The grader scores its structure the way investors and end users compare names.",
    form='''<form id="dm-form" class="panel"><div class="field"><label for="dm-in">Domain</label><input id="dm-in" value="555558.com" required></div><button class="btn" type="submit">Grade it</button></form>''',
    out='<div class="panel result" id="dm-out" aria-live="polite"><p>Your grade appears here.</p></div>',
    explain="""<h2>How the grade is built</h2>
<table><tr><th>Factor</th><th>Weight</th></tr><tr><td>Length (fewer digits is better)</td><td>35%</td></tr><tr><td>Memorability</td><td>25%</td></tr><tr><td>Prosperity digits (8 up, 4 down)</td><td>20%</td></tr><tr><td>Extension (.com highest)</td><td>20%</td></tr></table>
<p>This is a structural score for comparing names. Market value depends on comparable sales, buyer demand and timing. See the <a href="../guides/numeric-domains-guide.html">numeric domain guide</a> and <a href="../glossary.html">glossary</a>.</p>""",
    faq=[("Is this an appraisal?", "No. It compares structure. For a sale price, look at recent comparable sales and talk to a broker."), ("Why is 0 treated as weaker?", "Many Chinese buyers prefer names without 0 or 4; 0 can also be confused with the letter O.")]),
"launch-date": dict(
    title="Launch date finder", desc="Find the best dates in any window for a launch, opening or signing, ranked by 8s, 4s and date patterns.",
    intro="Choose a start date and how far ahead to look. We rank the dates by lucky-digit rules used in Chinese-speaking markets, with weekends optional.",
    form='''<form id="ld-form" class="panel"><div class="row2"><div class="field"><label for="ld-start">Start from</label><input id="ld-start" type="date" required></div>
<div class="field"><label for="ld-days">Look ahead</label><select id="ld-days"><option value="30">30 days</option><option value="60">60 days</option><option value="90" selected>90 days</option><option value="180">180 days</option><option value="365">1 year</option></select></div></div>
<label class="consent" style="margin-bottom:16px"><input type="checkbox" id="ld-wk" checked> Skip weekends</label>
<button class="btn" type="submit">Find dates</button></form>''',
    out='<div class="panel result" id="ld-out" aria-live="polite"><p>Your ranked dates appear here.</p></div>',
    explain="""<h2>Scoring rules</h2>
<p>Each 8 in the day, month and year adds points; each 4 removes them. The 8th, 18th and 28th and the month of August get a bonus; the 4th, 14th and 24th get a penalty; dates where day equals month get a small bonus. Pick a window that works practically first, then let the tool rank inside it. Read <a href="../guides/launch-on-a-lucky-date.html">launching on a lucky date</a>.</p>""",
    faq=[("Does this use the Chinese almanac?", "No. It applies simple digit rules. For traditional almanac or muhurat dates, consult a practitioner."), ("Can I include weekends?", "Yes, untick Skip weekends.")]),
"life-path": dict(
    title="Life path number calculator", desc="Calculate your life path number from your birth date and your expression number from your name, with short meanings.",
    intro="A popular numerology tradition, offered for reflection and fun. Nothing you enter leaves your browser.",
    form='''<form id="life-form" class="panel"><div class="field"><label for="life-dob">Date of birth</label><input id="life-dob" type="date" required></div><div class="field"><label for="life-name">Full name (optional)</label><input id="life-name" autocomplete="off"></div><button class="btn" type="submit">Calculate</button></form>''',
    out='<div class="panel result" id="life-out" aria-live="polite"><p>Your numbers appear here.</p></div>',
    explain="""<h2>How it's calculated</h2>
<p><b>Life path</b>: add every digit of your birth date and reduce to one digit, keeping master numbers 11, 22 and 33. <b>Expression</b>: convert each letter to a number using the Pythagorean table (A=1 … I=9, J=1 …) and reduce the same way.</p>
<p>Numerology is a cultural and recreational tradition. It is not a scientific method and should not guide financial, medical or legal decisions.</p>""",
    faq=[("Why keep 11, 22 and 33?", "Numerology treats them as master numbers with their own meanings."), ("Is my date stored?", "No. The calculation runs in your browser and nothing is sent anywhere.")]),
}


def build_tools():
    for slug, t in TOOL_PAGES.items():
        faq, fs = faq_block(t["faq"])
        app = {"@context": "https://schema.org", "@type": "WebApplication", "name": t["title"], "url": f"{SITE}/tools/{slug}.html",
               "applicationCategory": "BusinessApplication", "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
        others = [x for x in TOOLS if x[0] != slug][:4]
        related = "".join(f'<li><a href="{s}.html">{n}</a></li>' for s, g, n, d in others)
        body = page_head(t["title"], t["intro"], [("tools.html", "Tools"), ("", t["title"])], "../") + f'''
<div class="wrap" style="padding:36px 20px 10px">
  <div class="tool-shell">{t["form"]}{t["out"]}</div>
</div>
<div class="wrap article-wrap">
  <article class="prose">{t["explain"]}<h2>Questions</h2>{faq}
    <div class="callout mt"><b>Want a person to look at your numbers?</b> Our <a href="../audit.html">free number audit</a> reviews your prices, phone number, domain and launch window in writing.</div>
    <div class="mt"><b>Was this tool helpful?</b> <span><button class="btn ghost sm" data-poll>Yes</button> <button class="btn ghost sm" data-poll>Not really</button></span></div>
  </article>
  <aside class="side"><div class="box"><h3>More tools</h3><ul>{related}</ul></div>
    <div class="box"><h3>Last updated</h3><p>{UPDATED}. Reviewed under our <a href="../editorial-policy.html">editorial policy</a>.</p></div></aside>
</div>'''
        write(f"tools/{slug}.html", page(path=f"tools/{slug}.html", title=f"{t['title']} — free tool | 555558", desc=t["desc"], body=body, root="../", current="tools.html", schema=[fs, app], tools_js=True))
    body = page_head("Free number tools", "Seven calculators for pricing, naming and timing decisions. No sign-up, nothing leaves your browser.", [("", "Tools")]) + f'''
<section class="block"><div class="wrap"><div class="tool-list">{tool_rows("")}</div>
<div class="callout mt"><b>Need a tool we haven't built?</b> <a href="contact.html">Suggest it</a>. Popular requests get built first, and sponsors can fund a tool under their name — see <a href="advertise.html">sponsorship</a>.</div></div></section>'''
    write("tools.html", page(path="tools.html", title="Free number tools — pricing, phone, domain and date | 555558", desc="Seven free calculators: number analyzer, lucky price finder, margin and markup, phone number scorer, numeric domain grader, launch date finder and life path.", body=body, current="tools.html"))


# ---------------------------------------------------------------- guides
def build_guides():
    for i, g in enumerate(GUIDES):
        nxt = GUIDES[(i + 1) % len(GUIDES)]
        art = {"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["desc"],
               "datePublished": "2026-10-27", "dateModified": "2026-10-27", "author": {"@type": "Organization", "name": "555558 Editorial Team"},
               "publisher": {"@type": "Organization", "name": "555558 Prosperity Lab"}, "mainEntityOfPage": f"{SITE}/guides/{g['slug']}.html"}
        body = page_head(g["title"], g["desc"], [("guides.html", "Guides"), ("", g["tag"])], "../") + f'''
<div class="wrap article-wrap">
  <article class="prose">
    <p class="muted" style="font:500 .92rem var(--display)">By the 555558 Editorial Team. Updated {UPDATED}. {g["minutes"]} min read.</p>
    {g["body"]}
    <div class="callout mt"><b>Get this applied to your business.</b> Request a <a href="../audit.html">free number audit</a> and we'll review your prices, phone number, domain or launch dates.</div>
    <p class="mt">Next guide: <a href="{nxt["slug"]}.html">{nxt["title"]}</a></p>
  </article>
  <aside class="side">
    <div class="box"><h3>Try the tools</h3><ul><li><a href="../tools/number-analyzer.html">Number analyzer</a></li><li><a href="../tools/lucky-price.html">Lucky price finder</a></li><li><a href="../tools/domain-grader.html">Numeric domain grader</a></li><li><a href="../tools/launch-date.html">Launch date finder</a></li></ul></div>
    <div class="box"><h3>Sponsor this guide</h3><p>Put your brand beside readers who set prices and pick names.</p><a class="btn gold sm" href="../advertise.html">Sponsorship options</a></div>
  </aside>
</div>'''
        write(f"guides/{g['slug']}.html", page(path=f"guides/{g['slug']}.html", title=f"{g['title']} | 555558", desc=g["desc"], body=body, root="../", current="guides.html", schema=art, og_type="article"))
    body = page_head("Guides", "Research-backed reading on pricing psychology, number culture, numeric domains and launch timing.", [("", "Guides")]) + f'''
<section class="block"><div class="wrap"><div class="guide-grid">{guide_cards("")}</div></div></section>'''
    write("guides.html", page(path="guides.html", title="Guides on pricing psychology, lucky numbers and numeric domains | 555558", desc="Plain-English guides: charm pricing, the number 8 in business, numeric domains, vanity phone numbers, AI pricing, launch dates and more.", body=body, current="guides.html"))


# ---------------------------------------------------------------- 555558 meaning
def build_meaning():
    faq, fs = faq_block([
        ("Is 555558 a prime number?", "No. 555558 = 2 × 3 × 92,593, so it has 8 divisors: 1, 2, 3, 6, 92,593, 185,186, 277,779 and 555,558."),
        ("What is 555558 in numerology?", "Its digits add to 33, which numerology treats as a master number. Reduced fully, 3 + 3 = 6."),
        ("Is 555558 lucky?", "In Chinese number culture it ends on 8, the prosperity digit, and contains no 4. In angel-number culture, five 5s stand for major change. Together: change that ends in prosperity. These are cultural meanings, not predictions."),
        ("Is 555558 a trademark?", "This site claims no exclusive rights in the number itself. See our trademark & copyright notice."),
    ])
    body = page_head("555558 decoded", "The math, the culture and the business story inside one six-digit number.", [("", "555558 decoded")]) + f'''
<div class="wrap article-wrap">
<article class="prose">
<h2>The number at a glance</h2>
<table>
<tr><th>Property</th><th>Value</th></tr>
<tr><td>In words</td><td>five hundred fifty-five thousand five hundred fifty-eight</td></tr>
<tr><td>Prime factorisation</td><td>2 × 3 × 92,593</td></tr>
<tr><td>Number of divisors</td><td>8</td></tr>
<tr><td>Sum of divisors</td><td>1,111,128</td></tr>
<tr><td>Euler's totient</td><td>185,184</td></tr>
<tr><td>Digit sum</td><td>33 (a master number), reducing to 6</td></tr>
<tr><td>Binary</td><td>10000111101000100110</td></tr>
<tr><td>Hexadecimal</td><td>87A26</td></tr>
<tr><td>Neighbours</td><td>555,557 is prime; the next prime is 555,589</td></tr>
<tr><td>Pattern</td><td>AAAAAB: a run of five 5s plus a kicker</td></tr>
</table>
<p>Two details stand out. The number has exactly 8 divisors, an echo of its final digit. And the sum of its divisors, 1,111,128, is itself a long repdigit run plus a kicker.</p>

<h2>In commerce</h2>
<p>The final 8 is the prosperity digit for Chinese-speaking buyers, used in price endings, phone numbers and addresses. The absence of 4 matters as much as the presence of 8: the number has nothing a cautious buyer would avoid. As a phone number tail (555-5558) or a price (5,558), it is easy to remember and culturally positive.</p>

<h2>In business and branding</h2>
<p>Run-plus-kicker numbers compress in memory to two ideas: "five fives" and "an eight". That makes 555558 easy to say on radio, easy to type and easy to recall after one exposure, the three things a business number has to do. Read <a href="guides/repdigits-in-branding.html">repdigits in branding</a>.</p>

<h2>In AI and the economy</h2>
<p>Pricing increasingly runs through algorithms, and those systems still format their final prices for human readers. A model can set the price level; a rule decides whether it ends in 9, 8 or a round number. Numbers like 555558 sit exactly where machine pricing meets human reading. See <a href="guides/ai-pricing-and-number-psychology.html">AI pricing meets number psychology</a>.</p>

<h2>For people</h2>
<p>In angel-number culture, 5 means change, freedom and movement; repeated, the theme is amplified. In Western numerology 8 means achievement and material success. Read together, 555558 tells a story of a big change that ends in prosperity. We present this as culture and storytelling, not prediction. More in <a href="guides/angel-number-55555.html">55555 and 555558</a>.</p>

<h2>Questions</h2>
{faq}
</article>
<aside class="side"><div class="box"><h3>Analyze your own number</h3><p>Get the same profile for any number.</p><a class="btn sm" href="tools/number-analyzer.html?n=555558">Open the analyzer</a></div>
<div class="box"><h3>Interested in this domain?</h3><p>For acquisition, sponsorship or partnership inquiries, <a href="https://web.works/contact" target="_blank" rel="noopener">contact web.works</a>.</p></div></aside>
</div>'''
    write("555558-meaning.html", page(path="555558-meaning.html", title="555558 meaning: math facts, lucky-number culture and business use", desc="555558 decoded: prime factors (2 × 3 × 92,593), 8 divisors, digit sum 33, and what five 5s and an 8 mean in commerce, branding, AI pricing and number culture.", body=body, current="555558-meaning.html", schema=fs, og_type="article"))


# ---------------------------------------------------------------- videos
def build_videos():
    cards = ""
    for topic, title, desc, vid, q in VIDEOS:
        label = "Play video" if vid else "Watch on YouTube"
        cards += f'''<div class="video"><div class="frame" role="button" tabindex="0" data-yt="{vid}" data-q="{q}" aria-label="{title}: {label}"><div><div class="play" aria-hidden="true">▶</div>{label}</div></div>
<div class="body"><span class="pill">{topic}</span><h3 class="mt" style="margin-top:10px">{title}</h3><p>{desc}</p></div></div>'''
    body = page_head("Videos", "Short watches on pricing psychology, number culture, domains and AI pricing. Videos load only when you click, from YouTube's privacy-enhanced player.", [("", "Videos")]) + f'''
<section class="block"><div class="wrap"><div class="video-grid">{cards}</div></div></section>
<section class="block alt"><div class="wrap lead">
  <div><h2>Suggest a video or feature yours</h2><p class="section-intro">Made a useful video on pricing, naming or number culture? Send it. Creators can also sponsor a featured slot.</p></div>
  <form class="card" data-form="Video suggestion">
    <div class="row2"><div class="field"><label for="v-name">Your name</label><input id="v-name" name="name" required></div><div class="field"><label for="v-email">Email</label><input id="v-email" name="email" type="email" required></div></div>
    <div class="field"><label for="v-url">YouTube link</label><input id="v-url" name="video_url" type="url" required placeholder="https://www.youtube.com/watch?v="></div>
    <div class="field"><label for="v-why">Why it belongs here</label><textarea id="v-why" name="why"></textarea></div>
    {form_tail("")}
    <button class="btn" type="submit">Send suggestion</button><p class="form-status" role="status"></p>
  </form></div></section>'''
    write("videos.html", page(path="videos.html", title="Videos on pricing psychology, lucky numbers and domains | 555558", desc="Curated videos on charm pricing, the number 8, numeric domains, vanity phone numbers and AI pricing.", body=body, current="videos.html"))


# ---------------------------------------------------------------- audit (lead gen landing)
def build_audit():
    faq, fs = faq_block([
        ("Is the audit really free?", "Yes. We review a limited number of requests each week. If you want deeper work afterwards, we'll tell you what that would involve; there's no obligation."),
        ("How fast will I hear back?", "Usually within two business days, by email."),
        ("What do you do with my details?", "We use them only to prepare and send your audit and to follow up about it. See the privacy policy."),
        ("Can agencies request audits for clients?", "Yes. Mention the client in the goal field. For volume, ask about partnership on the advertise page."),
    ])
    body = page_head("Free number audit", "Prices, phone numbers, domains and launch dates, reviewed by a person and returned as clear written recommendations.", [("", "Free audit")]) + f'''
<section class="block"><div class="wrap lead">
  <div>
    <h2>What you get</h2>
    <ul class="ticks">
      <li>Your price points, with endings matched to each market you sell into</li>
      <li>A memorability and lucky-digit review of your phone number</li>
      <li>A structural review of your domain, with naming alternatives if useful</li>
      <li>Ranked launch or opening dates inside your preferred window</li>
      <li>Flags for anything that reads badly to a specific culture</li>
    </ul>
    <h2 class="mt">How it works</h2>
    <ol><li>Answer three short steps.</li><li>We review your numbers.</li><li>You get a written audit by email.</li></ol>
  </div>
  {audit_form("")}
</div></section>
<section class="block alt"><div class="wrap narrow"><h2>Questions</h2>{faq}</div></section>'''
    write("audit.html", page(path="audit.html", title="Free number audit for your prices, phone, domain and launch date | 555558", desc="Request a free written audit of your price points, phone number, domain and launch dates, matched to the markets you sell into.", body=body, current="audit.html", schema=fs))


# ---------------------------------------------------------------- advertise / sponsor / partner
def build_advertise():
    body = page_head("Advertise, sponsor or partner", "Reach founders, marketers, retailers and domain investors at the moment they're deciding on prices and names.", [("", "Advertise")]) + f'''
<section class="block"><div class="wrap">
  <div class="tiers">
    <div class="tier"><h3>Guide sponsor</h3><div class="amt">Monthly</div><p>Your brand and link in the sidebar of one guide, clearly labelled as sponsored.</p></div>
    <div class="tier feature"><h3>Tool sponsor</h3><div class="amt">Monthly</div><p>"Powered by" placement on a calculator, beside the result your audience came for.</p></div>
    <div class="tier"><h3>Newsletter</h3><div class="amt">Per issue</div><p>One sponsored slot in the Monday email, written with you and marked as sponsored.</p></div>
    <div class="tier"><h3>Contest partner</h3><div class="amt">Per contest</div><p>Fund the prize for a monthly contest and get named in every announcement.</p></div>
  </div>
  <p class="muted mt">All sponsored content is labelled. We don't accept sponsors whose products we wouldn't describe honestly, and sponsors don't edit our guides.</p>
</div></section>
<section class="block alt"><div class="wrap lead">
  <div><h2>Tell us what you have in mind</h2><p class="section-intro">Sponsorship, advertising, content partnership, tool integration, affiliate partnership, or interest in acquiring the website or domain. We reply within two business days.</p>
  <p>For domain or website acquisition you can also <a href="https://web.works/contact" target="_blank" rel="noopener">contact web.works directly</a>.</p></div>
  <form class="card" data-form="Advertising / Partnership inquiry">
    <div class="row2"><div class="field"><label for="ad-name">Name</label><input id="ad-name" name="name" required></div><div class="field"><label for="ad-co">Company</label><input id="ad-co" name="company" required></div></div>
    <div class="row2"><div class="field"><label for="ad-email">Email</label><input id="ad-email" name="email" type="email" required></div><div class="field"><label for="ad-type">Interest</label>
      <select id="ad-type" name="interest"><option>Sponsorship</option><option>Advertisement</option><option>Partnership</option><option>Website / domain acquisition</option><option>Affiliate program</option><option>Other</option></select></div></div>
    <div class="field"><label for="ad-budget">Budget range (optional)</label><select id="ad-budget" name="budget"><option>Not sure yet</option><option>Under $500</option><option>$500–$2,000</option><option>$2,000–$10,000</option><option>Over $10,000</option></select></div>
    <div class="field"><label for="ad-msg">Message</label><textarea id="ad-msg" name="message" required></textarea></div>
    {form_tail("")}
    <button class="btn gold" type="submit">Send inquiry</button><p class="form-status" role="status"></p>
  </form></div></section>'''
    write("advertise.html", page(path="advertise.html", title="Advertise, sponsor or partner with 555558", desc="Sponsorship, advertising, newsletter, contest and partnership options on 555558.com, plus website and domain acquisition inquiries.", body=body, current="advertise.html"))


# ---------------------------------------------------------------- contests + careers
def build_community():
    body = page_head("Contests & careers", "Win prizes for sharp ideas about numbers and pricing, or join the people who build the lab.", [("", "Contests & careers")]) + f'''
<section class="block" id="contests"><div class="wrap lead">
  <div>
    <h2>Monthly contest: the best-priced idea</h2>
    <p class="section-intro">Each month we set a pricing or naming challenge. Example: "Price a Lunar New Year gift box for three markets and explain why." The clearest, best-reasoned entry wins.</p>
    <ul class="ticks">
      <li>First prize: a cash or gift-card prize announced with each challenge</li>
      <li>Runners-up: a featured write-up on the site and in the newsletter</li>
      <li>Free to enter; one entry per person per month</li>
      <li>Judged on reasoning, clarity and originality</li>
    </ul>
    <p class="muted" style="font-size:.98rem">No purchase necessary. Open to adults where permitted by law. Full rules are published with each challenge and in our <a href="terms.html">terms</a>. Void where prohibited.</p>
  </div>
  <form class="card" data-form="Contest entry">
    <div class="row2"><div class="field"><label for="c-name">Name</label><input id="c-name" name="name" required></div><div class="field"><label for="c-email">Email</label><input id="c-email" name="email" type="email" required></div></div>
    <div class="field"><label for="c-country">Country</label><input id="c-country" name="country" required></div>
    <div class="field"><label for="c-entry">Your entry</label><textarea id="c-entry" name="entry" required placeholder="Your prices or names, and the reasoning behind them."></textarea></div>
    <label class="consent"><input type="checkbox" name="age" value="18+" required> I am 18 or older and accept the contest rules.</label>
    {form_tail("")}
    <button class="btn gold" type="submit">Submit entry</button><p class="form-status" role="status"></p>
  </form>
</div></section>
<section class="block alt" id="careers"><div class="wrap lead">
  <div>
    <h2>Work with the lab</h2>
    <p class="section-intro">We hire freelancers and part-time contributors, remote, paid per project.</p>
    <table style="width:100%;border-collapse:collapse;font:500 1rem var(--display)">
      <tr><td style="padding:10px 0;border-bottom:1px solid var(--line)"><b>Pricing & consumer-research writer</b></td><td style="border-bottom:1px solid var(--line)">Freelance</td></tr>
      <tr><td style="padding:10px 0;border-bottom:1px solid var(--line)"><b>Front-end developer (vanilla JS)</b></td><td style="border-bottom:1px solid var(--line)">Project-based</td></tr>
      <tr><td style="padding:10px 0;border-bottom:1px solid var(--line)"><b>Video creator / editor</b></td><td style="border-bottom:1px solid var(--line)">Freelance</td></tr>
      <tr><td style="padding:10px 0;border-bottom:1px solid var(--line)"><b>Chinese / Hindi localisation reviewer</b></td><td style="border-bottom:1px solid var(--line)">Per project</td></tr>
      <tr><td style="padding:10px 0;border-bottom:1px solid var(--line)"><b>Partnerships & ad sales</b></td><td style="border-bottom:1px solid var(--line)">Commission</td></tr>
    </table>
  </div>
  <form class="card" data-form="Talent application">
    <div class="row2"><div class="field"><label for="j-name">Name</label><input id="j-name" name="name" required></div><div class="field"><label for="j-email">Email</label><input id="j-email" name="email" type="email" required></div></div>
    <div class="field"><label for="j-role">Role</label><select id="j-role" name="role"><option>Pricing & consumer-research writer</option><option>Front-end developer</option><option>Video creator / editor</option><option>Localisation reviewer</option><option>Partnerships & ad sales</option><option>Something else</option></select></div>
    <div class="field"><label for="j-port">Portfolio or LinkedIn</label><input id="j-port" name="portfolio" type="url" required placeholder="https://"></div>
    <div class="field"><label for="j-msg">Why you</label><textarea id="j-msg" name="message"></textarea></div>
    {form_tail("")}
    <button class="btn" type="submit">Apply</button><p class="form-status" role="status"></p>
  </form>
</div></section>'''
    write("community.html", page(path="community.html", title="Contests with prizes and careers at 555558", desc="Enter the monthly pricing and naming contest for prizes, or apply to write, build, film or sell for the 555558 Prosperity Lab.", body=body, current="community.html"))


# ---------------------------------------------------------------- support / donations
def build_support():
    links = "".join(f'<a class="btn gold" href="{u}" target="_blank" rel="noopener">{n}</a> ' for n, u in DONATE_LINKS.items())
    direct = f'<p class="mt">{links}</p>' if links else ""
    body = page_head("Support the lab", "Every tool here is free. Supporters keep it that way and fund what comes next.", [("", "Support")]) + f'''
<section class="block"><div class="wrap">
  <div class="tiers">
    <div class="tier"><h3>Coffee</h3><div class="amt">$8</div><p>Covers a day of hosting, fonts and email delivery.</p></div>
    <div class="tier"><h3>Supporter</h3><div class="amt">$18 /mo</div><p>Funds one new guide each quarter. Your name on the supporters list, if you want it.</p></div>
    <div class="tier feature"><h3>Patron</h3><div class="amt">$88 /mo</div><p>Funds a new tool every few months and the monthly contest prize pool.</p></div>
    <div class="tier"><h3>Custom</h3><div class="amt">Any</div><p>One-off or recurring, in your currency.</p></div>
  </div>
  <h2 class="mt">Where the money goes</h2>
  <div class="uses"><div>Operations & hosting</div><div>Promotion & marketing</div><div>Hiring writers and developers</div><div>Contest prizes</div><div>New tools & research</div></div>
  {direct}
</div></section>
<section class="block alt"><div class="wrap lead">
  <div><h2>Pledge your support</h2><p class="section-intro">Tell us the amount and how you'd like to pay (card, PayPal, bank transfer or UPI). We'll reply with a secure payment link. We never ask for card details by email or form.</p>
  <p class="muted" style="font-size:.98rem">Contributions support an independent website and are not tax-deductible charitable donations.</p></div>
  <form class="card" data-form="Support pledge">
    <div class="row2"><div class="field"><label for="s-name">Name</label><input id="s-name" name="name" required></div><div class="field"><label for="s-email">Email</label><input id="s-email" name="email" type="email" required></div></div>
    <div class="row2"><div class="field"><label for="s-tier">Tier</label><select id="s-tier" name="tier"><option>Coffee — $8</option><option>Supporter — $18/mo</option><option selected>Patron — $88/mo</option><option>Custom</option></select></div>
    <div class="field"><label for="s-amt">Custom amount and currency</label><input id="s-amt" name="custom_amount" placeholder="e.g. 50 CAD"></div></div>
    <div class="field"><label for="s-pay">Preferred payment</label><select id="s-pay" name="payment_method"><option>Card</option><option>PayPal</option><option>Bank transfer</option><option>UPI</option></select></div>
    <div class="field"><label for="s-for">Direct it to (optional)</label><select id="s-for" name="direct_to"><option>Wherever it's needed</option><option>Operations</option><option>Promotion & marketing</option><option>Hiring talent</option><option>Contest prizes</option></select></div>
    <label class="consent"><input type="checkbox" name="list_name" value="yes"> List my name on the supporters page</label>
    {form_tail("")}
    <button class="btn gold" type="submit">Send pledge</button><p class="form-status" role="status"></p>
  </form></div></section>'''
    write("support.html", page(path="support.html", title="Support the 555558 Prosperity Lab", desc="Support free number tools and guides. Funds operations, promotion, hiring, contest prizes and new research.", body=body, current="support.html"))


# ---------------------------------------------------------------- contact
def build_contact():
    body = page_head("Contact", "Questions, corrections, tool ideas or press. We read everything and reply within two business days.", [("", "Contact")]) + f'''
<section class="block"><div class="wrap lead">
  <div>
    <h2>Other ways to reach us</h2>
    <p><b>Website, domain, sponsorship, advertising or partnership:</b> <a href="https://web.works/contact" target="_blank" rel="noopener">web.works/contact</a></p>
    <p><b>Email:</b> <a href="#" data-mail="Inquiry from 555558.com">Send us an email</a></p>
    <p><b>Free audit:</b> <a href="audit.html">Request one here</a></p>
    <p><b>Corrections:</b> tell us the page and what's wrong; see our <a href="editorial-policy.html">editorial policy</a>.</p>
  </div>
  <form class="card" data-form="Contact">
    <div class="row2"><div class="field"><label for="ct-name">Name</label><input id="ct-name" name="name" required autocomplete="name"></div><div class="field"><label for="ct-email">Email</label><input id="ct-email" name="email" type="email" required autocomplete="email"></div></div>
    <div class="field"><label for="ct-topic">Topic</label><select id="ct-topic" name="topic"><option>General question</option><option>Correction</option><option>Tool idea</option><option>Press</option><option>Sponsorship / advertising</option><option>Website / domain interest</option></select></div>
    <div class="field"><label for="ct-msg">Message</label><textarea id="ct-msg" name="message" required></textarea></div>
    {form_tail("")}
    <button class="btn" type="submit">Send message</button><p class="form-status" role="status"></p>
  </form>
</div></section>'''
    write("contact.html", page(path="contact.html", title="Contact 555558", desc="Contact the 555558 Prosperity Lab team about tools, corrections, press, sponsorship or the domain.", body=body, current="contact.html"))


# ---------------------------------------------------------------- simple text pages
def text_page(path, title, intro, html_body, desc, crumb=None):
    body = page_head(title, intro, [("", crumb or title)]) + f'<div class="wrap" style="padding:40px 20px 64px"><article class="prose narrow">{html_body}</article></div>'
    write(path, page(path=path, title=f"{title} | 555558", desc=desc, body=body, current=path))


def build_text_pages():
    text_page("about.html", "About the lab", "Why a website named after a number, and who's behind it.", f'''
<p>555558.com is an independent publication and toolset about one idea: numbers carry meaning, and that meaning affects what people buy, remember and trust. The name says it: five 5s, the digit of change, followed by an 8, the digit of prosperity.</p>
<h2>What we publish</h2>
<ul><li>Free calculators for pricing, naming and timing decisions.</li><li>Guides grounded in consumer research and clearly separated from cultural belief.</li><li>A weekly newsletter and a monthly contest.</li></ul>
<h2>How we're funded</h2>
<p>Advertising through Google AdSense, labelled sponsorships, and supporters. Sponsors never edit our guides. See the <a href="editorial-policy.html">editorial policy</a>.</p>
<h2>Who we are</h2>
<p>The 555558 Editorial Team is a small group of writers and developers working across pricing, branding and digital assets. The site is part of the web.works network of independent websites.</p>
<p><a class="btn" href="contact.html">Contact us</a></p>''', "About the 555558 Prosperity Lab: an independent site of free tools and guides on how numbers influence buying decisions.", "About")

    text_page("editorial-policy.html", "Editorial policy", "How we research, write, review and correct.", '''
<h2>Sources</h2><p>Pricing and consumer-behaviour claims are based on published research or verifiable reporting, and we name the study or outlet in the text. Where evidence is mixed, we say so.</p>
<h2>Belief versus evidence</h2><p>Numerology, angel numbers and lucky-number traditions are presented as cultural beliefs. We never present them as predictions, and we never connect them to medical, legal or investment decisions.</p>
<h2>Tools</h2><p>Every calculator shows its method on the same page. Scores such as memorability and prosperity are comparative, not absolute.</p>
<h2>Independence</h2><p>Sponsored placements are labelled. Sponsors and advertisers have no say over guide content or tool results.</p>
<h2>Corrections</h2><p>Spot an error? Tell us through the <a href="contact.html">contact page</a>. We fix confirmed errors promptly and update the date on the page.</p>
<h2>Use of AI</h2><p>We use software, including AI tools, to help draft and check content and code. A person reviews everything before publication and is responsible for it.</p>''', "How 555558.com researches, writes, reviews and corrects its guides and tools.")

    text_page("privacy.html", "Privacy policy", f"Last updated {UPDATED}.", '''
<h2>What we collect</h2><ul><li><b>Forms:</b> when you submit a form (audit, contact, newsletter, contest, application, pledge) we receive what you type. Forms are delivered to our inbox through FormSubmit, a form-relay service.</li><li><b>Tools:</b> calculators run in your browser. Numbers, dates and names you enter are not sent to us.</li><li><b>Cookies and ads:</b> see below.</li></ul>
<h2>Advertising</h2><p>We use Google AdSense. Google and its partners use cookies to serve ads based on your visits to this and other websites. You can opt out of personalised advertising at <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener">Google Ads Settings</a> or <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener">aboutads.info</a>. Learn how Google uses data at <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">policies.google.com/technologies/partner-sites</a>.</p>
<h2>Embedded videos</h2><p>Videos load only when you click, from YouTube's privacy-enhanced domain (youtube-nocookie.com).</p>
<h2>How we use your information</h2><p>Only to respond to your request, send what you asked for (an audit, the newsletter), run contests and process applications. We don't sell personal information.</p>
<h2>Retention</h2><p>We keep form submissions as long as needed for the purpose, then delete them. Ask us to delete your data any time.</p>
<h2>Your rights</h2><p>Depending on where you live (including under GDPR, UK GDPR, PIPEDA, Quebec Law 25, CCPA and India's DPDP Act) you may access, correct, delete or object to processing of your data. Use the <a href="contact.html">contact page</a>.</p>
<h2>Children</h2><p>This site is not directed to children under 13, and contests are for adults.</p>''', "Privacy policy for 555558.com: forms, cookies, Google AdSense, embedded videos and your rights.")

    text_page("terms.html", "Terms of use", f"Last updated {UPDATED}.", '''
<h2>Use of the site</h2><p>You may use the tools and read the guides for personal and business purposes. Don't copy the site wholesale, scrape it at scale or misuse forms.</p>
<h2>No professional advice</h2><p>Content is general information. It is not financial, legal, tax or investment advice. Lucky-number and numerology content is cultural and for entertainment.</p>
<h2>Tool results</h2><p>Results are provided as is. Check important calculations independently.</p>
<h2>Contests</h2><p>No purchase necessary. Entrants must be 18+ and entry must be lawful where they live. Each challenge publishes its prize, dates and judging criteria. Winners are notified by email and must respond within 14 days. We may publish winning entries with credit. Void where prohibited.</p>
<h2>Supporter contributions</h2><p>Contributions are voluntary support for an independent website, are non-refundable except where required by law, and are not charitable donations.</p>
<h2>Intellectual property</h2><p>See the <a href="trademark-copyright.html">trademark & copyright notice</a>.</p>
<h2>Liability</h2><p>To the extent permitted by law, we are not liable for losses arising from use of the site.</p>
<h2>Changes</h2><p>We may update these terms; the date above shows the latest version.</p>''', "Terms of use for 555558.com, including contests, supporter contributions and tool results.")

    text_page("cookies.html", "Cookie policy", "What we store in your browser and why.", '''
<table><tr><th>Cookie or storage</th><th>Purpose</th><th>Type</th></tr>
<tr><td>cookieChoice (local storage)</td><td>Remembers your cookie choice</td><td>Essential</td></tr>
<tr><td>lastForm (session storage)</td><td>Personalises the thank-you page</td><td>Essential</td></tr>
<tr><td>Google AdSense cookies</td><td>Serving and measuring ads</td><td>Advertising</td></tr>
<tr><td>YouTube (only after you click a video)</td><td>Playing embedded videos</td><td>Functional</td></tr></table>
<p>Choose "Essential only" in the cookie notice to request non-personalised ads. You can also clear cookies in your browser at any time.</p>''', "Cookie policy for 555558.com.")

    text_page("disclaimer.html", "Disclaimer & affiliate disclosure", "Please read before relying on anything here.", '''
<h2>General</h2><p>All content is for general information and entertainment. It is not professional advice. Make important decisions with a qualified adviser.</p>
<h2>Cultural content</h2><p>Lucky numbers, numerology and angel numbers are traditions and beliefs. We describe them; we don't claim they predict outcomes.</p>
<h2>Numbers and prices</h2><p>Figures quoted from public reports were accurate when published by their sources. Markets change.</p>
<h2>Affiliate and sponsored links</h2><p>Some pages may include sponsored placements or affiliate links. They are labelled. If you buy through an affiliate link we may earn a commission at no extra cost to you. It never changes what we recommend.</p>''', "Disclaimer and affiliate disclosure for 555558.com.")

    text_page("trademark-copyright.html", "Trademark & copyright notice", "Who owns what on this site.", '''
<h2>The number 555558</h2><p>"555558" is a numeral string used on this website descriptively and as a domain name. 555558.com does not claim exclusive trademark rights in the number itself, and does not seek to prevent anyone from using the number in its ordinary meaning. Any company, product or service that uses the same or a similar number is unrelated to this website, and no affiliation, sponsorship or endorsement is implied.</p>
<h2>Third-party marks</h2><p>Names of companies, publications and products mentioned in our guides belong to their owners and are used for identification and commentary only.</p>
<h2>Copyright</h2><p>Original text, tools, code and design on 555558.com are &copy; 555558.com. Quoted research is summarised in our own words and credited to its authors. Short quotations, if any, are used for commentary.</p>
<h2>Videos</h2><p>Embedded videos remain the property of their creators and are shown through YouTube's standard embed player.</p>
<h2>Reporting a concern</h2><p>If you believe content here infringes your rights, tell us through the <a href="contact.html">contact page</a> with the URL and details, and we'll review it promptly.</p>''', "Trademark and copyright notice for 555558.com. No exclusive rights claimed in the number 555558 itself.", "Trademark & copyright")

    gl = [("AAAAB", "A number made of a run of one digit plus one different final digit, e.g. 555558."), ("Anchoring", "Judging a price relative to a reference price shown first."),
          ("Charm pricing", "Ending prices just below a round number, e.g. 9.99."), ("Chips / Chinese premium", "Numeric domain names with no 0 or 4."),
          ("Digit root", "Repeatedly summing digits until one digit remains."), ("End user", "A buyer who will use a domain or number, not resell it."),
          ("Left-digit effect", "The bias toward judging a number by its first digit."), ("Margin", "Profit as a percentage of the selling price."),
          ("Markup", "Profit as a percentage of cost."), ("Master number", "In numerology, 11, 22 and 33, which are not reduced further."),
          ("NNN / NNNN", "Three- or four-digit numeric domain names."), ("Palindrome", "A number that reads the same backwards, e.g. 12321."),
          ("Repdigit", "A number made of one repeated digit, e.g. 88888."), ("Shagun", "Indian custom of gifting amounts ending in 1, such as 101 or 501."),
          ("Tetraphobia", "Avoidance of the number 4 in East Asian cultures.")]
    text_page("glossary.html", "Glossary", "The vocabulary of pricing psychology, number culture and numeric domains.",
              "<table><tr><th>Term</th><th>Meaning</th></tr>" + "".join(f"<tr><td><b>{a}</b></td><td>{b}</td></tr>" for a, b in gl) + "</table>",
              "Glossary of pricing psychology, number culture and numeric domain terms: charm pricing, left-digit effect, repdigit, chips, shagun and more.")

    faq, fs = faq_block([
        ("Do I need an account?", "No. Every tool works without signing up."), ("Do you store the numbers I type?", "No. Tools run in your browser."),
        ("How do I get the free audit?", "Fill in the three-step form on the audit page. We reply by email within two business days."),
        ("How can I advertise?", "See the advertise page for sponsorship options and send an inquiry."), ("How do I support the site?", "Choose a tier on the support page and send a pledge; we reply with a secure payment link."),
        ("Is the domain for sale?", "For website, domain, sponsorship, advertising or partnership interest, contact web.works/contact."),
    ])
    body = page_head("FAQ", "Quick answers about the site, the tools and working with us.", [("", "FAQ")]) + f'<div class="wrap" style="padding:40px 20px 64px"><div class="narrow">{faq}</div></div>'
    write("faq.html", page(path="faq.html", title="FAQ | 555558", desc="Frequently asked questions about 555558.com, its free tools, the audit, advertising and support.", body=body, schema=fs))

    body = '''<section class="block"><div class="wrap narrow center">
<h1>Thank you</h1><p style="font-size:1.25rem">We received your <b id="ty-what">message</b>. You'll hear from us by email within two business days.</p>
<p class="muted">While you wait, try a tool or read a guide.</p>
<p class="mt"><a class="btn" href="tools.html">Browse tools</a> <a class="btn ghost" href="guides.html">Read guides</a></p></div></section>'''
    write("thank-you.html", page(path="thank-you.html", title="Thank you | 555558", desc="Your submission was received.", body=body).replace('content="index, follow, max-image-preview:large"', 'content="noindex, follow"'))

    body = '''<section class="block"><div class="wrap narrow center">
<div class="digits num" style="justify-content:center"><span class="digit four">4</span><span class="digit">0</span><span class="digit four">4</span></div>
<h1>This page doesn't exist</h1><p>The link may be old or mistyped. Try the home page or the tools.</p>
<p class="mt"><a class="btn" href="/index.html">Go home</a> <a class="btn ghost" href="/tools.html">Browse tools</a></p></div></section>'''
    write("404.html", page(path="404.html", title="Page not found | 555558", desc="Page not found.", body=body, root="/").replace('content="index, follow, max-image-preview:large"', 'content="noindex"'))


def build_meta():
    urls = [p for p in OUT if p not in ("thank-you.html", "404.html")]
    today = datetime.date(2026, 10, 27).isoformat()
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in sorted(urls, key=lambda x: (x != "index.html", x)):
        loc = SITE + "/" + ("" if u == "index.html" else u)
        pr = "1.0" if u == "index.html" else "0.8" if u.startswith(("tools", "guides", "555558", "audit")) else "0.5"
        sm += f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>\n"
    sm += "</urlset>\n"
    write("sitemap.xml", sm)


if __name__ == "__main__":
    build_home(); build_tools(); build_guides(); build_meaning(); build_videos(); build_audit()
    build_advertise(); build_community(); build_support(); build_contact(); build_text_pages(); build_meta()
    print(f"Built {len(OUT)} files")
