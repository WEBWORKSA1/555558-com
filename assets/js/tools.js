/* 555558 Prosperity Lab — number tools. Pure client-side; nothing leaves the browser. */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var fmt = function (n) { return Number(n).toLocaleString("en-US"); };

  /* ---------- core number analysis ---------- */
  function factorize(n) {
    var f = [], d = 2;
    while (n % 2 === 0 && n > 1) { f.push(2); n /= 2; }
    d = 3;
    while (d * d <= n) { while (n % d === 0) { f.push(d); n /= d; } d += 2; }
    if (n > 1) f.push(n);
    return f;
  }
  function factorString(f) {
    var m = {}; f.forEach(function (p) { m[p] = (m[p] || 0) + 1; });
    return Object.keys(m).map(function (p) { return m[p] > 1 ? p + "<sup>" + m[p] + "</sup>" : p; }).join(" × ");
  }
  function divisorCount(f) {
    var m = {}; f.forEach(function (p) { m[p] = (m[p] || 0) + 1; });
    return Object.keys(m).reduce(function (a, p) { return a * (m[p] + 1); }, 1);
  }
  function isPrime(n) { if (n < 2) return false; return factorize(n).length === 1; }
  function digitRoot(s) { var t = s.split("").reduce(function (a, c) { return a + (+c); }, 0); while (t > 9 && t !== 11 && t !== 22 && t !== 33) t = String(t).split("").reduce(function (a, c) { return a + (+c); }, 0); return t; }
  var ONES = ["zero","one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen"];
  var TENS = ["","","twenty","thirty","forty","fifty","sixty","seventy","eighty","ninety"];
  function words(n) {
    if (n < 20) return ONES[n];
    if (n < 100) return TENS[Math.floor(n / 10)] + (n % 10 ? "-" + ONES[n % 10] : "");
    if (n < 1000) return ONES[Math.floor(n / 100)] + " hundred" + (n % 100 ? " " + words(n % 100) : "");
    var units = [[1e12, "trillion"], [1e9, "billion"], [1e6, "million"], [1e3, "thousand"]];
    for (var i = 0; i < units.length; i++) if (n >= units[i][0]) return words(Math.floor(n / units[i][0])) + " " + units[i][1] + (n % units[i][0] ? " " + words(n % units[i][0]) : "");
    return String(n);
  }

  /* pattern + memorability scoring, shared by phone, domain and analyzer tools */
  function patterns(s) {
    var tags = [], L = s.length;
    if (/^(\d)\1+$/.test(s)) tags.push("Repdigit (all one digit)");
    if (s === s.split("").reverse().join("") && L > 2) tags.push("Palindrome");
    if (/^(\d)\1+(\d)$/.test(s) && L > 3) tags.push("Run + kicker (AAAAB)");
    if (/^(\d\d)\1+$/.test(s) && L >= 4) tags.push("Repeating pair (ABAB)");
    if (/^(\d{3})\1+$/.test(s)) tags.push("Repeating triple (ABCABC)");
    if ("0123456789".indexOf(s) >= 0 && L > 2) tags.push("Ascending run");
    if ("9876543210".indexOf(s) >= 0 && L > 2) tags.push("Descending run");
    var simple = /^(\d)\1+$/.test(s) || /^(\d)\1+(\d)$/.test(s);
    if (!simple && /(\d)\1\1\1/.test(s)) tags.push("Contains a quad");
    else if (!simple && /(\d)\1\1/.test(s)) tags.push("Contains a triple");
    return tags;
  }
  function memorability(s) {
    var L = s.length, uniq = new Set(s.split("")).size, score = 100;
    score -= Math.max(0, L - 4) * 5;
    score -= (uniq - 1) * 7;
    var runs = (s.match(/(\d)\1+/g) || []).reduce(function (a, r) { return a + r.length; }, 0);
    score += runs * 3;
    var p = patterns(s);
    if (p.length) score += 8 * p.length;
    return Math.max(1, Math.min(100, Math.round(score)));
  }
  function prosperity(s) {
    var e = (s.match(/8/g) || []).length, f = (s.match(/4/g) || []).length,
        six = (s.match(/6/g) || []).length, nine = (s.match(/9/g) || []).length;
    var score = 50 + e * 12 + six * 4 + nine * 3 - f * 15;
    if (s.slice(-1) === "8") score += 10;
    if (s.slice(-1) === "4") score -= 12;
    return { score: Math.max(0, Math.min(100, score)), eights: e, fours: f };
  }
  window.N8 = { factorize: factorize, patterns: patterns, memorability: memorability, prosperity: prosperity, digitRoot: digitRoot, words: words };

  /* ---------- hero analyzer (home) ---------- */
  var heroIn = $("#hero-num");
  if (heroIn) {
    var digitsBox = $("#hero-digits");
    var render = function () {
      var s = (heroIn.value || "").replace(/\D/g, "").slice(0, 12) || "555558";
      digitsBox.innerHTML = s.split("").map(function (d) {
        return '<span class="digit' + (d === "8" ? " lucky" : d === "4" ? " four" : "") + '">' + d + "</span>";
      }).join("");
      var n = Number(s), p = prosperity(s), m = memorability(s), f = factorize(n), tags = patterns(s);
      $("#r-root").textContent = digitRoot(s);
      $("#r-sum").textContent = s.split("").reduce(function (a, c) { return a + (+c); }, 0);
      $("#r-fact").innerHTML = n > 1 ? factorString(f) : "—";
      $("#r-div").textContent = n > 1 ? divisorCount(f) : "—";
      $("#r-8").textContent = p.eights + " eight" + (p.eights === 1 ? "" : "s") + ", " + p.fours + " four" + (p.fours === 1 ? "" : "s");
      $("#r-mem").textContent = m + "/100";
      $("#r-pros").textContent = p.score + "/100";
      $("#m-mem").style.width = m + "%";
      $("#m-pros").style.width = p.score + "%";
      var v;
      if (p.fours > 0) v = "Contains a 4, the digit many Chinese-speaking buyers avoid. Worth swapping in prices, phone lines and addresses aimed at those markets.";
      else if (p.eights >= 2) v = "Strong prosperity signal: multiple 8s. This pattern sells at a premium in Chinese-speaking markets for phone numbers, plates and price tags.";
      else if (s.slice(-1) === "8") v = "Ends on 8, the same move Asian retailers use where Western shops end on 9. A culturally fluent price ending.";
      else if (s.slice(-1) === "9") v = "Ends on 9, the classic Western charm-price ending that makes a price read as lower than it is.";
      else v = "Neutral on the lucky-digit scale. Its memorability score says more about how well it works as a phone number or domain.";
      if (tags.length) v += " Pattern: " + tags.join(", ") + ".";
      $("#r-verdict").textContent = v;
      $("#hero-more").href = "tools/number-analyzer.html?n=" + s;
    };
    heroIn.addEventListener("input", render);
    render();
  }

  /* ---------- full number analyzer ---------- */
  var anForm = $("#an-form");
  if (anForm) {
    var run = function (s) {
      s = String(s).replace(/\D/g, "").replace(/^0+(?=\d)/, "").slice(0, 15);
      if (!s) return;
      $("#an-in").value = s;
      var n = Number(s), f = n > 1 ? factorize(n) : [], p = prosperity(s), m = memorability(s), tags = patterns(s);
      var rows = [
        ["In words", n <= 999999999999999 ? words(n) : "—"],
        ["Prime?", isPrime(n) ? "Yes" : "No"],
        ["Prime factors", n > 1 ? factorString(f) : "—"],
        ["Number of divisors", n > 1 ? divisorCount(f) : "—"],
        ["Digit sum", s.split("").reduce(function (a, c) { return a + (+c); }, 0)],
        ["Numerology root", digitRoot(s)],
        ["Even / odd", n % 2 ? "Odd" : "Even"],
        ["Binary", n.toString(2)],
        ["Octal", n.toString(8)],
        ["Hexadecimal", n.toString(16).toUpperCase()],
        ["Square root", Math.sqrt(n).toFixed(4)],
        ["Eights / fours", p.eights + " / " + p.fours],
        ["Memorability", m + "/100"],
        ["Prosperity (8/4) score", p.score + "/100"]
      ];
      $("#an-out").innerHTML = "<h3>" + fmt(n) + "</h3><p>" + (tags.length ? tags.map(function (t) { return '<span class="pill">' + esc(t) + "</span>"; }).join(" ") : '<span class="pill">No special digit pattern</span>') + "</p><table>" +
        rows.map(function (r) { return "<tr><td>" + r[0] + "</td><td>" + r[1] + "</td></tr>"; }).join("") + "</table>" +
        '<p class="mt"><a class="btn gold sm" href="?n=' + (n - 1) + '">Previous: ' + fmt(n - 1) + '</a> <a class="btn gold sm" href="?n=' + (n + 1) + '">Next: ' + fmt(n + 1) + "</a></p>";
      try { history.replaceState(null, "", "?n=" + s); } catch (x) {}
    };
    anForm.addEventListener("submit", function (e) { e.preventDefault(); run($("#an-in").value); });
    var q = new URLSearchParams(location.search).get("n");
    run(q || "555558");
  }

  /* ---------- lucky price / charm pricing ---------- */
  var lp = $("#lp-form");
  if (lp) {
    var calc = function () {
      var base = parseFloat($("#lp-price").value), mkt = $("#lp-market").value;
      if (!(base > 0)) { $("#lp-out").innerHTML = "<p>Enter a price above zero to see endings.</p>"; return; }
      var whole = Math.floor(base), mag = whole >= 1000 ? 100 : whole >= 100 ? 10 : 1;
      var round = Math.round(base / mag) * mag;
      var opts = [];
      var add = function (v, label, why) { if (v > 0 && !opts.some(function (o) { return o.v === v; })) opts.push({ v: v, label: label, why: why }); };
      if (mkt === "west" || mkt === "global") {
        add(Math.ceil(base) - 0.01, "Charm .99", "Left-digit effect: the first digit drives the perceived price.");
        add(round - mag * 0.01 > 0 ? +(round - (mag === 1 ? 0.01 : 1)).toFixed(2) : round, "Just-below round", "Sits under a round threshold shoppers anchor on.");
        add(Math.ceil(base) - 0.05, ".95 ending", "Softer discount cue used by grocery and mass retail.");
      }
      if (mkt === "china" || mkt === "global") {
        add(Math.floor(base / 10) * 10 + 8, "Ends in 8", "8 (ba) sounds like 'prosper' (fa) in Mandarin and Cantonese.");
        add(Math.floor(base / 100) * 100 + 88, "Ends in 88", "Double 8: a stronger prosperity cue used in gifting and luxury.");
        add(Math.floor(base / 1000) * 1000 + 888, "Ends in 888", "Triple 8: reserved for flagship or celebration pricing.");
        add(Math.floor(base / 100) * 100 + 68, "Ends in 68", "6 (liu) suggests things flowing smoothly; 68 reads as 'smooth prosperity'.");
      }
      if (mkt === "india") {
        add(Math.floor(base / 100) * 100 + 99, "Ends in 99", "Charm ending (₹x99) is standard in Indian retail.");
        add(Math.floor(base / 10) * 10 + 1, "Ends in 1 (shagun)", "Gift amounts ending in 1 (101, 501, 1,001) are customary for auspicious occasions.");
      }
      if (mkt === "premium" || mkt === "global") {
        add(round, "Round number", "Round prices read as quality and are processed as a feeling rather than a calculation.");
      }
      opts = opts.filter(function (o) { return o.v > 0 && Math.abs(o.v - base) / base < 0.35; });
      var hasFour = /4/.test(String(Math.floor(base)));
      $("#lp-out").innerHTML = "<h3>Suggested price points</h3>" + (hasFour && (mkt === "china" || mkt === "global") ? '<p><span class="pill red">Your base price contains a 4</span> Avoid it for Chinese-speaking buyers.</p>' : "") +
        '<div class="price-cards">' + opts.map(function (o) { return "<div><b>" + o.v.toLocaleString("en-US", { minimumFractionDigits: o.v % 1 ? 2 : 0, maximumFractionDigits: 2 }) + "</b><span>" + esc(o.label) + "</span></div>"; }).join("") + "</div>" +
        "<table class='mt'>" + opts.map(function (o) { return "<tr><td>" + esc(o.label) + "</td><td style='text-align:left;font-weight:400'>" + esc(o.why) + "</td></tr>"; }).join("") + "</table>";
    };
    lp.addEventListener("input", calc);
    lp.addEventListener("submit", function (e) { e.preventDefault(); calc(); });
    calc();
  }

  /* ---------- margin / markup: fill any two ---------- */
  var mm = $("#mm-form");
  if (mm) {
    mm.addEventListener("submit", function (e) {
      e.preventDefault();
      var c = parseFloat($("#mm-cost").value), p = parseFloat($("#mm-price").value), g = parseFloat($("#mm-margin").value), k = parseFloat($("#mm-markup").value);
      var have = [c, p, g, k].filter(function (x) { return !isNaN(x); }).length;
      var out = $("#mm-out");
      if (have < 2) { out.innerHTML = "<p>Fill in any two fields, then calculate.</p>"; return; }
      if (isNaN(c) || isNaN(p)) {
        if (!isNaN(c) && !isNaN(g)) p = c / (1 - g / 100);
        else if (!isNaN(c) && !isNaN(k)) p = c * (1 + k / 100);
        else if (!isNaN(p) && !isNaN(g)) c = p * (1 - g / 100);
        else if (!isNaN(p) && !isNaN(k)) c = p / (1 + k / 100);
        else { out.innerHTML = "<p>Margin and markup alone can't set a price. Add the cost or the price.</p>"; return; }
      }
      var profit = p - c; g = profit / p * 100; k = profit / c * 100;
      out.innerHTML = "<h3>Result</h3><table><tr><td>Cost</td><td>" + c.toFixed(2) + "</td></tr><tr><td>Selling price</td><td>" + p.toFixed(2) + "</td></tr><tr><td>Profit</td><td>" + profit.toFixed(2) + "</td></tr><tr><td>Gross margin</td><td>" + g.toFixed(2) + "%</td></tr><tr><td>Markup</td><td>" + k.toFixed(2) + "%</td></tr></table>" +
        '<p class="mt">Try a charm ending on this price: <a class="btn gold sm" href="lucky-price.html?p=' + p.toFixed(2) + '">Find a lucky price</a></p>';
    });
    mm.addEventListener("reset", function () { $("#mm-out").innerHTML = "<p>Fill in any two fields, then calculate.</p>"; });
  }
  var lpq = new URLSearchParams(location.search).get("p");
  if (lpq && $("#lp-price")) { $("#lp-price").value = lpq; $("#lp-form").dispatchEvent(new Event("input")); }

  /* ---------- phone number scorer + keypad converter ---------- */
  var KEY = { a: 2, b: 2, c: 2, d: 3, e: 3, f: 3, g: 4, h: 4, i: 4, j: 5, k: 5, l: 5, m: 6, n: 6, o: 6, p: 7, q: 7, r: 7, s: 7, t: 8, u: 8, v: 8, w: 9, x: 9, y: 9, z: 9 };
  var ph = $("#ph-form");
  if (ph) {
    ph.addEventListener("submit", function (e) {
      e.preventDefault();
      var raw = $("#ph-in").value.trim();
      var digits = raw.toLowerCase().replace(/[a-z]/g, function (ch) { return KEY[ch]; }).replace(/\D/g, "");
      if (digits.length < 4) { $("#ph-out").innerHTML = "<p>Enter at least four digits or letters.</p>"; return; }
      var tail = digits.slice(-7), m = memorability(tail), p = prosperity(digits), tags = patterns(tail);
      var overall = Math.round(m * 0.6 + p.score * 0.4);
      $("#ph-out").innerHTML = '<h3>Number score</h3><div class="big-score">' + overall + '</div><p>out of 100</p><table>' +
        "<tr><td>Keypad digits</td><td>" + digits + "</td></tr>" +
        "<tr><td>Memorability (last 7)</td><td>" + m + "/100</td></tr>" +
        "<tr><td>Prosperity (8/4)</td><td>" + p.score + "/100</td></tr>" +
        "<tr><td>Eights / fours</td><td>" + p.eights + " / " + p.fours + "</td></tr>" +
        "<tr><td>Patterns</td><td>" + (tags.length ? esc(tags.join(", ")) : "None") + "</td></tr></table>" +
        (p.fours ? '<p class="mt"><span class="pill red">Contains 4</span> Consider an alternative if you serve Chinese-speaking customers.</p>' : "");
    });
  }

  /* ---------- numeric domain grader ---------- */
  var dm = $("#dm-form");
  if (dm) {
    dm.addEventListener("submit", function (e) {
      e.preventDefault();
      var v = $("#dm-in").value.trim().toLowerCase().replace(/^https?:\/\//, "").replace(/^www\./, "");
      var parts = v.split("."), name = parts[0], tld = parts.slice(1).join(".") || "com";
      if (!/^\d{1,12}$/.test(name)) { $("#dm-out").innerHTML = "<p>Enter a numbers-only name such as 555558.com. Letters and hyphens are outside this grader.</p>"; return; }
      var L = name.length, m = memorability(name), p = prosperity(name), tags = patterns(name);
      var cls = L <= 3 ? "N" + L + " (" + L + "-digit, scarce)" : L + "-digit (" + (L === 4 ? "NNNN" : L === 5 ? "NNNNN" : L === 6 ? "NNNNNN" : "long-form") + ")";
      var noZero = !/0/.test(name), noFour = !/4/.test(name);
      var chip = noZero && noFour ? "Yes — no 0 or 4 (a \"Chinese premium\" or chip-style name)" : "No";
      var lenScore = Math.max(0, 100 - (L - 3) * 14);
      var tldScore = tld === "com" ? 100 : /^(net|cn|co)$/.test(tld) ? 60 : 35;
      var total = Math.round(lenScore * 0.35 + m * 0.25 + p.score * 0.2 + tldScore * 0.2);
      $("#dm-out").innerHTML = '<h3>' + esc(name + "." + tld) + '</h3><div class="big-score">' + total + '</div><p>quality score out of 100</p><table>' +
        "<tr><td>Length class</td><td>" + cls + "</td></tr>" +
        "<tr><td>Extension</td><td>." + esc(tld) + " (" + tldScore + ")</td></tr>" +
        "<tr><td>Memorability</td><td>" + m + "/100</td></tr>" +
        "<tr><td>Prosperity (8/4)</td><td>" + p.score + "/100</td></tr>" +
        "<tr><td>No 0 or 4</td><td>" + chip + "</td></tr>" +
        "<tr><td>Patterns</td><td>" + (tags.length ? esc(tags.join(", ")) : "None") + "</td></tr></table>" +
        '<p class="mt" style="font-size:.95rem">This score compares structure only. Real prices depend on comparable sales, buyer demand and the market at the time.</p>';
    });
  }

  /* ---------- lucky launch date finder ---------- */
  var ld = $("#ld-form");
  if (ld) {
    var today = new Date(); $("#ld-start").value = today.toISOString().slice(0, 10);
    ld.addEventListener("submit", function (e) {
      e.preventDefault();
      var start = new Date($("#ld-start").value + "T12:00:00"), days = parseInt($("#ld-days").value, 10), avoidWeekend = $("#ld-wk").checked;
      var res = [];
      for (var i = 0; i < days; i++) {
        var d = new Date(start.getTime() + i * 864e5);
        var y = d.getFullYear(), mo = d.getMonth() + 1, da = d.getDate(), wd = d.getDay();
        if (avoidWeekend && (wd === 0 || wd === 6)) continue;
        var s = "" + da + mo + y, sc = 50;
        sc += (s.match(/8/g) || []).length * 10 - (s.match(/4/g) || []).length * 12;
        if (da === 8 || da === 18 || da === 28) sc += 12;
        if (mo === 8) sc += 10;
        if (da === 4 || da === 14 || da === 24) sc -= 10;
        if (da === mo) sc += 6;
        res.push({ d: d, sc: Math.max(0, Math.min(100, sc)) });
      }
      res.sort(function (a, b) { return b.sc - a.sc || a.d - b.d; });
      var top = res.slice(0, 8);
      $("#ld-out").innerHTML = "<h3>Top 8 dates</h3><table>" + top.map(function (r) {
        return "<tr><td>" + r.d.toLocaleDateString("en-US", { weekday: "short", year: "numeric", month: "short", day: "numeric" }) + "</td><td>" + r.sc + "</td></tr>";
      }).join("") + "</table>";
    });
  }

  /* ---------- life path + name number (entertainment) ---------- */
  var lpth = $("#life-form");
  if (lpth) {
    var reduce = function (n) { while (n > 9 && n !== 11 && n !== 22 && n !== 33) n = String(n).split("").reduce(function (a, c) { return a + (+c); }, 0); return n; };
    var MEAN = { 1: "Initiator: starts things, works best with autonomy.", 2: "Diplomat: partnerships, negotiation, timing.", 3: "Communicator: content, voice, creative output.", 4: "Builder: systems, process, reliability.", 5: "Change-maker: adaptability, travel, many projects at once.", 6: "Steward: service, community, responsibility.", 7: "Analyst: research, depth, quiet expertise.", 8: "Executive: money, scale, authority and material results.", 9: "Humanitarian: broad vision, completion, generosity.", 11: "Master 11: intuition and inspiration at high intensity.", 22: "Master 22: large-scale builder.", 33: "Master 33: teacher and caretaker." };
    var PY = { a: 1, j: 1, s: 1, b: 2, k: 2, t: 2, c: 3, l: 3, u: 3, d: 4, m: 4, v: 4, e: 5, n: 5, w: 5, f: 6, o: 6, x: 6, g: 7, p: 7, y: 7, h: 8, q: 8, z: 8, i: 9, r: 9 };
    lpth.addEventListener("submit", function (e) {
      e.preventDefault();
      var dob = $("#life-dob").value, name = $("#life-name").value.toLowerCase();
      if (!dob) return;
      var lp = reduce(dob.replace(/\D/g, "").split("").reduce(function (a, c) { return a + (+c); }, 0));
      var ex = name ? reduce(name.replace(/[^a-z]/g, "").split("").reduce(function (a, c) { return a + PY[c]; }, 0)) : null;
      $("#life-out").innerHTML = "<h3>Your numbers</h3><table><tr><td>Life path</td><td>" + lp + "</td></tr>" + (ex ? "<tr><td>Expression (name)</td><td>" + ex + "</td></tr>" : "") + "</table>" +
        "<p class='mt'><b>" + lp + ":</b> " + MEAN[lp] + "</p>" + (ex ? "<p><b>" + ex + ":</b> " + MEAN[ex] + "</p>" : "") +
        "<p style='font-size:.9rem;opacity:.8'>Numerology is a cultural and recreational tradition, not a scientific prediction.</p>";
    });
  }

  /* ---------- daily number widget ---------- */
  var dn = $("#daily-num");
  if (dn) {
    var t = new Date(), seed = t.getFullYear() * 1000 + t.getMonth() * 40 + t.getDate();
    var x = Math.abs(Math.sin(seed) * 1e6), num = String(Math.floor(x) % 900000 + 100000).replace(/4/g, "8");
    dn.textContent = num;
    var dl = $("#daily-link"); if (dl) dl.href = "tools/number-analyzer.html?n=" + num;
  }

  /* ---------- helpful poll ---------- */
  document.querySelectorAll("[data-poll]").forEach(function (b) {
    b.addEventListener("click", function () { b.parentNode.innerHTML = "<p>Thanks — noted.</p>"; });
  });
})();
