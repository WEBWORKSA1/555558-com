# 555558.com — 555558 Prosperity Lab

Free tools and guides on how numbers sell: price endings, lucky digits, phone numbers, numeric domains and launch dates. Static site for GitHub Pages (free plan).

## Structure
- `index.html`, `tools.html`, `guides.html`, `555558-meaning.html`, `audit.html`, `advertise.html`, `community.html`, `support.html`, `videos.html`, legal pages — generated
- `tools/` — 7 calculators; `guides/` — 9 guides
- `assets/` — CSS, JS (`main.js` site behaviour, `tools.js` calculators), images
- `_src/` — the generator (`build.py`, `layout.py`, `guides.py`)

## Edit and rebuild
```
python3 _src/build.py
```
- Add a guide: append to `GUIDES` in `_src/guides.py`.
- Add YouTube videos: put the 11-character id in `VIDEOS` in `_src/build.py`.
- Add direct donation links: fill `DONATE_LINKS` in `_src/build.py`.

## Forms
All forms post through FormSubmit to a single inbox that is assembled at runtime and never written in the HTML. The first submission triggers a one-time FormSubmit activation email to that inbox; confirm it once.

## Hosting
GitHub Pages → Settings → Pages → Deploy from branch `main`, folder `/ (root)`. Custom domain `555558.com` (see `CNAME`). DNS: A records `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`; `www` CNAME `webworksa1.github.io`. Enable "Enforce HTTPS".

## Monetisation
Google AdSense (ca-pub-6620975821265271, auto ads; `ads.txt` included), free-audit lead generation, sponsorships, supporter pledges, contests.

See `PROMPTS.md` for the phase-wise build prompts and `trademark-copyright.html` for the trademark notice.
