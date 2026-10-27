/* 555558 Prosperity Lab — shared site script (no dependencies) */
(function () {
  "use strict";

  /* ---- contact address: assembled at runtime, never written in page source ---- */
  var _k = [116,118,106,53,115,112,104,116,110,71,56,104,122,114,121,118,126,105,108,126];
  function addr() { return _k.slice().reverse().map(function (c) { return String.fromCharCode(c - 7); }).join(""); }
  window.__inbox = function () { return addr(); };

  /* links marked data-mail open the mail client without exposing the address in HTML */
  document.querySelectorAll("[data-mail]").forEach(function (a) {
    a.addEventListener("click", function (e) {
      e.preventDefault();
      var subj = a.getAttribute("data-mail") || "Inquiry from 555558.com";
      window.location.href = "mai" + "lto:" + addr() + "?subject=" + encodeURIComponent(subj);
    });
  });

  /* ---- mobile menu ---- */
  var btn = document.querySelector(".menu-btn"), nav = document.querySelector("nav.main");
  if (btn && nav) btn.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  });

  /* ---- forms: every [data-form] posts to the hidden inbox via FormSubmit ---- */
  function serialize(form) {
    var data = {};
    new FormData(form).forEach(function (v, k) {
      if (data[k]) data[k] += ", " + v; else data[k] = v;
    });
    return data;
  }
  document.querySelectorAll("form[data-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var status = form.querySelector(".form-status");
      if (form.querySelector(".hp input") && form.querySelector(".hp input").value) return; // bot
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var data = serialize(form);
      delete data._gotcha;
      data._subject = "[555558.com] " + form.getAttribute("data-form") + " submission";
      data._template = "table";
      data._captcha = "false";
      data.page = location.pathname;
      data.submitted = new Date().toISOString();
      var b = form.querySelector("button[type=submit]");
      if (b) { b.disabled = true; b.dataset.label = b.textContent; b.textContent = "Sending…"; }
      fetch("https://formsubmit.co/ajax/" + addr(), {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(data)
      }).then(function (r) { return r.json(); }).then(function () {
        try { sessionStorage.setItem("lastForm", form.getAttribute("data-form")); } catch (x) {}
        window.location.href = (document.body.dataset.root || "") + "thank-you.html";
      }).catch(function () {
        if (status) { status.className = "form-status err"; status.textContent = "Your message didn't send. Check your connection and try again, or use the email link in the footer."; }
        if (b) { b.disabled = false; b.textContent = b.dataset.label; }
      });
    });
  });

  /* ---- multi-step lead form ---- */
  document.querySelectorAll("[data-steps]").forEach(function (form) {
    var steps = form.querySelectorAll(".step"), bars = form.querySelectorAll(".steps span"), i = 0;
    function show(n) {
      steps.forEach(function (s, j) { s.classList.toggle("on", j === n); });
      bars.forEach(function (s, j) { s.classList.toggle("on", j <= n); });
      i = n;
    }
    form.querySelectorAll("[data-next]").forEach(function (b) {
      b.addEventListener("click", function () {
        var ok = true;
        steps[i].querySelectorAll("input,select,textarea").forEach(function (f) { if (!f.checkValidity()) { f.reportValidity(); ok = false; } });
        if (ok) show(Math.min(i + 1, steps.length - 1));
      });
    });
    form.querySelectorAll("[data-prev]").forEach(function (b) { b.addEventListener("click", function () { show(Math.max(i - 1, 0)); }); });
    show(0);
  });

  /* ---- click-to-load YouTube (privacy-enhanced) ---- */
  document.querySelectorAll(".video .frame[data-yt]").forEach(function (f) {
    function load() {
      var id = f.getAttribute("data-yt"), q = f.getAttribute("data-q");
      if (!id) { window.open("https://www.youtube.com/results?search_query=" + encodeURIComponent(q), "_blank", "noopener"); return; }
      f.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1" title="' + (f.getAttribute("aria-label") || "Video") + '" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen loading="lazy"></iframe>';
    }
    f.addEventListener("click", load);
    f.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); load(); } });
  });

  /* ---- cookie notice ---- */
  var c = document.querySelector(".cookie");
  try {
    if (c && !localStorage.getItem("cookieChoice")) c.classList.add("show");
  } catch (x) { if (c) c.classList.add("show"); }
  document.querySelectorAll("[data-cookie]").forEach(function (b) {
    b.addEventListener("click", function () {
      try { localStorage.setItem("cookieChoice", b.getAttribute("data-cookie")); } catch (x) {}
      if (b.getAttribute("data-cookie") === "essential") { (window.adsbygoogle = window.adsbygoogle || []).requestNonPersonalizedAds = 1; }
      c.classList.remove("show");
    });
  });

  /* ---- year ---- */
  document.querySelectorAll("[data-year]").forEach(function (y) { y.textContent = new Date().getFullYear(); });

  /* ---- thank-you personalization ---- */
  var ty = document.getElementById("ty-what");
  if (ty) { try { var f = sessionStorage.getItem("lastForm"); if (f) ty.textContent = f; } catch (x) {} }
})();
