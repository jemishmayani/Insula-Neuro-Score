/* =========================================================================
   Insula Neuro Score — Calculator & Guide renderer (UI layer)
   Renders input controls from inputDefinitions and displays the engine's
   ResultModel. Contains NO scoring rules: every number, state and message
   shown here comes from InsulaEngine.engine.calculate().
   ========================================================================= */
(function (global) {
  "use strict";
  var UI = global.UI, esc = UI.esc, Engine = global.InsulaEngine.engine;
  var Android = global.Android || null;

  /* ---------------- input controls ---------------- */
  function ntValue(a) { return a && typeof a === "object" && !Array.isArray(a) && a.nt; }
  function fieldId(d) { return "in-" + d.id; }

  function controlHTML(d, a) {
    var nt = ntValue(a), html = "";
    var help = d.help ? '<p class="field-help" id="' + fieldId(d) + '-help">' + esc(d.help) + "</p>" : "";
    var described = (d.help ? fieldId(d) + "-help " : "") + fieldId(d) + "-err";
    switch (d.type) {
      case "single":
        html = '<div class="choice-list" role="radiogroup" aria-labelledby="' + fieldId(d) + '-l" aria-describedby="' + described + '">' +
          d.options.map(function (o) { return choiceRow(d, "radio", o, !nt && a != null && String(a) === String(o.value)); }).join("") +
          (d.notTestable ? choiceRow(d, "radio", { value: "__nt", label: d.notTestable.label || "Not testable", detail: d.notTestable.description, code: d.notTestable.code || "NT", isNT: true }, !!nt) : "") + "</div>";
        break;
      case "multi":
        var sel = Array.isArray(a) ? a.map(String) : [];
        html = '<div class="choice-list" role="group" aria-labelledby="' + fieldId(d) + '-l" aria-describedby="' + described + '">' +
          d.options.map(function (o) { return choiceRow(d, "checkbox", o, sel.indexOf(String(o.value)) >= 0); }).join("") + "</div>";
        break;
      case "yesno":
        var labels = d.labels || { yes: "Yes", no: "No" }, cur = a === true ? "yes" : a === false ? "no" : a;
        html = '<div class="segmented choice-seg" role="radiogroup" aria-labelledby="' + fieldId(d) + '-l">' + ["no", "yes"].map(function (v) {
          return '<label' + (cur === v ? ' class="is-on"' : "") + '><input type="radio" class="vh" name="' + esc(d.id) + '" value="' + v + '" data-input="' + esc(d.id) + '"' + (cur === v ? " checked" : "") + ">" + esc(labels[v]) + "</label>";
        }).join("") + "</div>";
        break;
      case "dropdown":
        html = '<div class="select-wrap"><select id="' + fieldId(d) + '" data-input="' + esc(d.id) + '" aria-describedby="' + described + '"' + (nt ? " disabled" : "") + '><option value="">Select…</option>' +
          d.options.map(function (o) { return '<option value="' + esc(o.value) + '"' + (!nt && String(a) === String(o.value) ? " selected" : "") + ">" + esc(o.label) + "</option>"; }).join("") + "</select>" + UI.icon("down", "select-chev") + "</div>";
        break;
      case "number": case "integer": case "decimal":
        var step = d.type === "integer" ? 1 : d.type === "decimal" ? Math.pow(10, -(d.decimals || 1)) : "any";
        html = '<div class="number-field">' +
          (d.type === "integer" ? '<button type="button" class="stepper" data-step="-1" data-input="' + esc(d.id) + '" aria-label="Decrease ' + esc(d.short || d.label) + '"' + (nt ? " disabled" : "") + ">−</button>" : "") +
          '<input id="' + fieldId(d) + '" type="text" inputmode="' + (d.type === "integer" ? "numeric" : "decimal") + '" enterkeyhint="next" autocomplete="off" data-input="' + esc(d.id) + '" data-step-size="' + step + '" value="' + (nt || a == null ? "" : esc(a)) + '" aria-describedby="' + described + '"' + (nt ? " disabled" : "") + ">" +
          (d.type === "integer" ? '<button type="button" class="stepper" data-step="1" data-input="' + esc(d.id) + '" aria-label="Increase ' + esc(d.short || d.label) + '"' + (nt ? " disabled" : "") + ">+</button>" : "") +
          '<span class="unit">' + esc(d.unit || "") + " " + rangeText(d) + "</span></div>";
        break;
      case "measurement":
        var m = a && typeof a === "object" && !nt ? a : {}, unit = m.unit || d.units[0].id;
        html = '<div class="number-field"><input id="' + fieldId(d) + '" type="text" inputmode="decimal" autocomplete="off" data-input="' + esc(d.id) + '" data-part="value" value="' + esc(m.value == null ? "" : m.value) + '" aria-describedby="' + described + '"' + (nt ? " disabled" : "") + ">" +
          '<div class="select-wrap unit-select"><select data-input="' + esc(d.id) + '" data-part="unit" aria-label="Unit for ' + esc(d.short || d.label) + '"' + (nt ? " disabled" : "") + ">" +
          d.units.map(function (u) { return '<option value="' + esc(u.id) + '"' + (u.id === unit ? " selected" : "") + ">" + esc(u.label || u.id) + "</option>"; }).join("") + "</select>" + UI.icon("down", "select-chev") + "</div>" +
          '<span class="unit">' + rangeText(d, d.units[0].label) + "</span></div>";
        break;
    }
    if (d.notTestable && d.type !== "single") {
      html += '<label class="nt-toggle"><input type="checkbox" data-input="' + esc(d.id) + '" data-part="nt"' + (nt ? " checked" : "") + "> " + esc(d.notTestable.label || "Not testable") + "</label>";
    }
    if (d.notTestable && d.notTestable.reasons && nt) {
      html += '<div class="nt-reason"><label for="' + fieldId(d) + '-reason">Reason</label><div class="select-wrap"><select id="' + fieldId(d) + '-reason" data-input="' + esc(d.id) + '" data-part="reason"><option value="">Select reason…</option>' +
        d.notTestable.reasons.map(function (r) { return '<option' + (a.reason === r ? " selected" : "") + ">" + esc(r) + "</option>"; }).join("") + "</select>" + UI.icon("down", "select-chev") + "</div></div>";
    }
    var labelTag = (d.type === "dropdown" || ["number", "integer", "decimal", "measurement"].indexOf(d.type) >= 0) ? 'label for="' + fieldId(d) + '"' : "span";
    return '<fieldset class="field" id="f-' + esc(d.id) + '" data-field="' + esc(d.id) + '"><legend class="vh">' + esc(d.label) + "</legend>" +
      '<div class="field-head"><' + labelTag + ' class="field-label" id="' + fieldId(d) + '-l">' + esc(d.label) + "</" + labelTag.split(" ")[0] + ">" + (d.required === false ? '<span class="field-opt">Optional</span>' : "") + "</div>" +
      help + html + '<p class="field-error" id="' + fieldId(d) + '-err" role="alert"></p></fieldset>';
  }
  function rangeText(d, unitLabel) { return d.min != null && d.max != null ? "(" + d.min + "–" + d.max + (unitLabel ? " " + unitLabel : "") + ")" : ""; }
  var TYPE_LABEL = { score: "Score", grade: "Grade", classification: "Classification", measurement: "Measurement" };
  /** Range as the clinician reads it: grades and classes by their codes (MAS 0–4, Cognard I–V), not internal ordinals. */
  function rangeLabel(score) {
    var cm = score.calculationMethod;
    if (cm.type === "select") {
      var d = score.inputDefinitions.filter(function (x) { return x.id === cm.input; })[0], os = (d && d.options) || [];
      if (os.length && os.some(function (o) { return o.code != null && String(o.code) !== String(o.points); })) {
        if (os.every(function (o) { return String(o.code).toLowerCase() === String(o.label).toLowerCase(); })) return os.length + " categories";
        var codes = os.map(function (o) { return String(o.code); });
        return codes[0] + "–" + codes[codes.length - 1];
      }
    }
    return cm.range.min + "–" + cm.range.max;
  }
  /** The code/points tag beside an option; empty when it would only repeat the option's label (e.g. "Flexor"). */
  function optTag(o) {
    var t = o.code != null ? o.code : o.points;
    return t != null && String(t).toLowerCase() === String(o.label).toLowerCase() ? "" : t;
  }
  function choiceRow(d, kind, o, checked) {
    var tag = o.isNT ? (o.code || "NT") : optTag(o);
    return '<label class="choice' + (checked ? " is-on" : "") + (o.isNT ? " is-nt" : "") + '"><input type="' + kind + '" class="vh" name="' + esc(d.id) + '" value="' + esc(o.value) + '" data-input="' + esc(d.id) + '"' + (checked ? " checked" : "") + ">" +
      '<span class="mark ' + kind + '" aria-hidden="true"></span><span class="choice-text"><span class="choice-label">' + esc(o.label) + "</span>" + (o.detail ? '<span class="choice-detail">' + esc(o.detail) + "</span>" : "") + "</span>" +
      (tag != null && tag !== "" ? '<span class="choice-pts" aria-hidden="true">' + esc(tag) + "</span>" : "") + "</label>";
  }

  /* ---------------- result panel (renders ResultModel only) ---------------- */
  /** Avoid "7 · NIHSS 7": if the state label only restates the value, show the tone name. */
  function stateLabel(r) {
    var l = String(r.state.label || ""), d = String(r.display);
    return l && d !== "–" && l.indexOf(d) >= 0 && l.replace(d, "").replace(/[^A-Za-z]/g, "").length <= 6 ? UI.TONE_LABEL[r.state.tone] : l;
  }
  /* Result order: Score → Breakdown → Interpretation → Context → Considerations → Limitations → Confounders → Boundaries → Related */
  /** Short form for the narrow points column; the full wording is already in the middle column. */
  function ptsCell(r) {
    var d = String(r.status !== "complete" ? "–" : r.display);
    if (d.length <= 6) return d;
    var last = d.split(" ").pop();
    return last.length <= 6 && /[0-9IVX+\-]/.test(last) ? last : "–";
  }
  function resultHTML(score, r, links, guideHref) {
    var tone = r.state.tone, pres = r.presentation || {};
    var meter = r.bands ? UI.ScaleMeter({ min: r.range.min, max: r.range.max, value: r.status === "complete" ? r.total : null, bands: r.bands, label: score.abbreviation }) : "";
    var h = UI.ResultCard({ tone: tone, label: stateLabel(r), value: r.display, typeLabel: pres.typeLabel,
      formula: r.formula, formulaJoin: r.formula && r.status === "complete" && r.formulaEquals !== false ? "=" : null,
      meta: UI.TONE_LABEL[tone] + " · " + score.abbreviation + " range " + rangeLabel(score), summary: r.state.summary, meter: meter });
    if (r.warnings.length) h += '<div class="result-block" data-block="warnings">' + r.warnings.map(function (w) { return UI.WarningBanner({ title: "Check", message: w.message }); }).join("") + "</div>";
    // Breakdown
    h += '<div class="result-block" data-block="breakdown"><h3 class="result-h">Breakdown</h3><table class="breakdown result-breakdown"><colgroup><col class="c-item"><col class="c-value"><col class="c-pts"></colgroup><tbody>' + r.breakdown.map(function (c) {
      var shown = c.items.filter(function (it) { var d = score.inputDefinitions.filter(function (x) { return x.id === it.inputId; })[0]; return !(d && d.detail && it.status === "empty"); });
      if (!shown.length) return "";
      var rows = shown.map(function (it) {
        var tag = it.status === "ok" ? (it.code != null ? it.code : it.points) : it.status === "nt" ? it.code : "–";
        if (tag != null && String(tag).toLowerCase() === String(it.display).toLowerCase()) tag = "";
        return '<tr class="bd-' + it.status + '"><th scope="row">' + esc(it.short) + "</th><td>" + esc(it.display) + (it.reason ? " (" + esc(it.reason) + ")" : "") +
          '</td><td class="pts">' + esc(tag) + "</td></tr>";
      }).join("");
      var head = shown.length > 1 && c.showSubtotal !== false ? '<tr class="bd-group"><th scope="rowgroup" colspan="2">' + esc(c.label) + '</th><td class="pts">' + (c.subtotal == null ? "–" : c.subtotal) + "</td></tr>" : "";
      return head + rows;
    }).join("") + '<tr class="bd-total"><th scope="row">Result</th><td>' + esc(r.state.label) + '</td><td class="pts">' + esc(ptsCell(r)) + "</td></tr></tbody></table></div>";
    // Interpretation
    var interpItems = [];
    if (r.state.detail) interpItems.push({ text: r.state.detail, importance: tone === "high" || tone === "critical" ? "major" : "standard" });
    if (pres.describes) interpItems.push({ title: "Result type: " + pres.typeLabel, text: pres.describes });
    if (interpItems.length) h += '<div class="result-block" data-block="interpretation">' + UI.InsightSection({ section: { type: "interpretation", title: "Interpretation", question: "What does the result represent?", items: interpItems } }) + "</div>";
    // Insight sections (same structured content as the guide)
    (r.insightSet ? r.insightSet.sections : []).forEach(function (sec) {
      h += '<div class="result-block" data-block="' + sec.type + '">' + UI.InsightSection({ section: sec, collapseAfter: 2 }) + "</div>";
    });
    if (r.related.length) h += '<div class="result-block" data-block="related"><h3 class="result-h">Related scores</h3><div class="chip-row">' + r.related.map(function (x) {
      var l = links(x.id); return l ? '<a class="chip" href="' + l.href + '" data-nav>' + esc(l.label) + ' <span class="n">' + esc(x.relation) + "</span></a>" : ""; }).join("") + "</div></div>";
    var canShare = r.status === "complete" || r.status === "not-interpretable";
    h += '<div class="result-block btn-row">' + (guideHref ? UI.SecondaryButton({ label: "Guide", icon: "guide", href: guideHref, replace: true, data: { role: "open-guide" } }) : "") +
      UI.SecondaryButton({ label: "Reset", icon: "reset", act: "calc-reset" }) +
      UI.SecondaryButton({ label: "Copy result", icon: "copy", act: "calc-copy", disabled: !canShare }) +
      UI.SecondaryButton({ label: "Share", icon: "share", act: "calc-share", disabled: !canShare }) + "</div>";
    h += '<p class="fineprint">' + esc(score.version.label) + " · content v" + esc(score.contentVersion) + ". Calculation and reference support; it does not diagnose or recommend treatment.</p>";
    return h;
  }
  function shareText(score, r) {
    var lines = [r.shareText || (score.abbreviation + " " + r.display)];
    r.breakdown.forEach(function (c) { c.items.forEach(function (it) { if (it.status === "ok" || it.status === "nt") lines.push(it.short + ": " + it.display + (it.reason ? " (" + it.reason + ")" : "") + " [" + (it.status === "nt" ? it.code : (it.code != null ? it.code : it.points)) + "]"); }); });
    r.warnings.forEach(function (w) { lines.push("Note: " + w.message); });
    lines.push(score.version.label + ". Calculated with Insula Neuro Score; interpret in clinical context.");
    return lines.join("\n");
  }

  /* ---------------- mount ---------------- */
  /** mount(el, score, answers, opts) — answers object is mutated in place (session memory only). */
  function mount(el, score, answers, opts) {
    opts = opts || {};
    var links = opts.links || function () { return null; };
    var details = score.inputDefinitions.filter(function (d) { return d.detail; });
    var grouped = score.components.map(function (c) {
      var defs = c.inputs.map(function (id) { return score.inputDefinitions.filter(function (d) { return d.id === id; })[0]; }).filter(function (d) { return !d.detail; });
      if (!defs.length) return "";
      var inner = defs.map(function (d) { return controlHTML(d, answers[d.id]); }).join("");
      return score.components.length > 1 && defs.length > 1 ? '<section class="input-group"><h3 class="input-group-h">' + esc(c.label) + "</h3>" + inner + "</section>" : inner;
    }).join("") +
      (details.length ? '<section class="input-group input-details"><h3 class="input-group-h">Details for your note</h3><p class="field-help">Optional. Added to the copied result; they never change the result.</p>' +
        details.map(function (d) { return controlHTML(d, answers[d.id]); }).join("") + "</section>" : "");
    el.innerHTML = '<div class="detail-grid two calc"><form class="calc-inputs" novalidate onsubmit="return false" aria-label="' + esc(score.abbreviation) + ' inputs">' +
      (score.calculatorNotice ? '<div class="calc-notice">' + (score.calculatorNotice.tone === "warning" ? UI.WarningBanner : UI.InfoBanner)({ title: score.calculatorNotice.title, message: score.calculatorNotice.message }) + "</div>" : "") +
      '<div class="calc-progress" aria-live="polite"></div>' + grouped + '</form><div class="aside"><section id="result" aria-label="Result" tabindex="-1"></section></div></div>' +
      '<button type="button" class="result-bar" data-act="calc-jump" aria-label="Jump to result"></button>';

    var last = null, lastSig = null, barHidden = false;
    function update(changedId) {
      var r = Engine.calculate(score, answers); last = r;
      // Avoid unnecessary DOM work: rebuild the result panel only when the result actually changed.
      var sig = JSON.stringify([r.status, r.display, r.formula, r.state, r.warnings, r.insights, r.limitations, r.breakdown]);
      if (sig !== lastSig) { document.getElementById("result").innerHTML = resultHTML(score, r, links, opts.guideHref); lastSig = sig; }
      // per-field errors & warning highlights
      score.inputDefinitions.forEach(function (d) {
        var f = el.querySelector('[data-field="' + d.id + '"]'); if (!f) return;
        var err = r.errors.filter(function (e) { return e.inputId === d.id; })[0];
        var warn = r.warnings.some(function (w) { return (w.inputs || []).indexOf(d.id) >= 0; });
        var errEl = f.querySelector(".field-error");
        // don't nag while a number is mid-entry
        errEl.textContent = err && !(changedId === d.id && opts.typing) ? err.message : "";
        f.classList.toggle("has-error", !!err); f.classList.toggle("has-warning", warn && !err);
        var miss = r.missing.indexOf(d.id) >= 0; f.classList.toggle("is-missing", miss);
      });
      var total = score.inputDefinitions.filter(function (d) { return d.required !== false; }).length, done = total - r.missing.length;
      el.querySelector(".calc-progress").innerHTML = '<span class="bar"><i style="width:' + Math.round(done / total * 100) + '%"></i></span>' + done + " of " + total + " answered";
      var bar = el.querySelector(".result-bar");
      if (bar) bar.className = "result-bar tone-" + r.state.tone + (barHidden ? " is-hidden" : "");
      // Compact only code-style formulas (e.g. "E3 + V4 + M5" → "E3 V4 M5"); other formulas are not shown in the bar.
      var compact = r.formula && /^[A-Z]+[A-Z0-9]*( \+ [A-Z]+[A-Z0-9]*)+$/.test(r.formula) ? r.formula.replace(/ \+ /g, " ") : null;
      var barValue = compact ? (r.status === "complete" ? compact + " = " + r.display : compact) : r.display;
      if (bar) bar.innerHTML = UI.stateIcon(r.state.tone) + '<span class="rb-value' + (compact ? " has-formula" : "") + '">' + esc(barValue) + '</span><span class="rb-label">' + esc(r.status === "incomplete" ? done + " of " + total + " answered" : stateLabel(r)) + "</span>" + UI.icon("down");
      if (opts.onResult) opts.onResult(r);
    }
    function setAnswer(id, v) { if (v === undefined) delete answers[id]; else answers[id] = v; }
    function def(id) { return score.inputDefinitions.filter(function (d) { return d.id === id; })[0]; }
    function rerenderField(id) {
      var d = def(id), f = el.querySelector('[data-field="' + id + '"]'), tmp = document.createElement("div");
      tmp.innerHTML = controlHTML(d, answers[id]); f.replaceWith(tmp.firstChild);
    }

    el.addEventListener("keydown", function (ev) {
      var t = ev.target; if (ev.key !== "Enter" || t.tagName !== "INPUT" || t.type !== "text") return;
      ev.preventDefault();
      var all = [].slice.call(el.querySelectorAll('input[type=text][data-input]:not([disabled])')), i = all.indexOf(t);
      if (i >= 0 && i < all.length - 1) all[i + 1].focus(); else t.blur();
    });
    /* Minimal taps: after answering a choice, bring the next unanswered question into view (scroll only; focus stays put). */
    var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
    function revealNext(id) {
      var f = el.querySelector('[data-field="' + id + '"]'); if (!f) return;
      var fields = [].slice.call(el.querySelectorAll(".field")), i = fields.indexOf(f);
      for (var j = i + 1; j < fields.length; j++) {
        var nid = fields[j].getAttribute("data-field");
        if (answers[nid] === undefined) {
          var r = fields[j].getBoundingClientRect(), barH = (document.querySelector(".result-bar:not(.is-hidden)") || { offsetHeight: 0 }).offsetHeight + 72;
          if (r.top > window.innerHeight - barH - 40) window.scrollBy({ top: r.top - 120, behavior: reduce ? "auto" : "smooth" });
          return;
        }
      }
    }
    el.addEventListener("change", function (ev) {
      var t = ev.target, id = t.getAttribute("data-input"); if (!id) return;
      var d = def(id), part = t.getAttribute("data-part");
      if (part === "nt") { setAnswer(id, t.checked ? { nt: true } : undefined); rerenderField(id); }
      else if (part === "reason") { setAnswer(id, { nt: true, reason: t.value || undefined }); }
      else if (part === "unit") { var cur = answers[id] && !ntValue(answers[id]) ? answers[id] : {}; setAnswer(id, { value: cur.value, unit: t.value }); }
      else if (d.type === "single") { setAnswer(id, t.value === "__nt" ? { nt: true } : t.value); rerenderField(id); if (t.value !== "__nt") setTimeout(function () { revealNext(id); }, 0); }
      else if (d.type === "multi") {
        var checked = [].slice.call(el.querySelectorAll('input[name="' + id + '"]:checked')).map(function (x) { return x.value; });
        setAnswer(id, checked.length ? checked : undefined); rerenderField(id);
      }
      else if (d.type === "yesno") { setAnswer(id, t.value); rerenderField(id); }
      else if (d.type === "dropdown") setAnswer(id, t.value || undefined);
      else return;
      var nf = el.querySelector('[data-field="' + id + '"] [data-input="' + id + '"]' + (part ? '[data-part="' + part + '"]' : ':checked') ) || el.querySelector('[data-field="' + id + '"] [data-input]');
      if (nf && (part || d.type !== "dropdown")) nf.focus({ preventScroll: true });
      opts.typing = false; update(id);
    });
    el.addEventListener("input", function (ev) {
      var t = ev.target, id = t.getAttribute("data-input"); if (!id || t.tagName !== "INPUT" || t.type !== "text") return;
      var d = def(id);
      if (d.type === "measurement") { var cur = answers[id] && !ntValue(answers[id]) ? answers[id] : {}; setAnswer(id, t.value === "" && !cur.unit ? undefined : { value: t.value, unit: cur.unit || d.units[0].id }); }
      else setAnswer(id, t.value === "" ? undefined : t.value);
      opts.typing = true; update(id);
    });
    el.addEventListener("focusout", function (ev) {
      if (ev.target.getAttribute && ev.target.getAttribute("data-input") && ev.target.type === "text") { opts.typing = false; update(); }
    });
    el.addEventListener("click", function (ev) {
      var b = ev.target.closest("button"); if (!b) return;
      if (b.hasAttribute("data-step")) {
        var id = b.getAttribute("data-input"), d = def(id), inp = el.querySelector("#" + fieldId(d)), cur = Number(inp.value);
        var next = inp.value === "" || isNaN(cur) ? (Number(b.getAttribute("data-step")) > 0 ? d.min : d.max) : Math.round(cur) + Number(b.getAttribute("data-step"));
        next = Math.max(d.min, Math.min(d.max, next)); inp.value = next; setAnswer(id, String(next)); opts.typing = false; update(id); return;
      }
      var act = b.getAttribute("data-act");
      if (act === "calc-reset") {
        var snap = JSON.parse(JSON.stringify(answers));
        Object.keys(answers).forEach(function (k) { delete answers[k]; }); mount(el, score, answers, opts);
        if (opts.toast) opts.toast("Inputs cleared", { label: "Undo", run: function () { Object.keys(snap).forEach(function (k) { answers[k] = snap[k]; }); mount(el, score, answers, opts); } });
        var first = el.querySelector("[data-input]"); if (first) first.focus({ preventScroll: true }); window.scrollTo(0, 0);
      }
      else if (act === "calc-copy" && last) { var txt = shareText(score, last); try { if (Android && Android.copy) Android.copy(txt); else navigator.clipboard.writeText(txt); if (opts.toast) opts.toast("Result copied"); } catch (e) { if (opts.toast) opts.toast("Copy failed"); } }
      else if (act === "calc-share" && last) { var tx = shareText(score, last); try { if (Android && Android.share) Android.share(tx); else if (navigator.share) navigator.share({ text: tx }); else { navigator.clipboard.writeText(tx); if (opts.toast) opts.toast("Result copied"); } } catch (e) {} }
      else if (act === "calc-jump") { var res = document.getElementById("result"); res.scrollIntoView({ block: "start" }); res.focus({ preventScroll: true }); }
    });
    if (opts.noBar) { var nb = el.querySelector(".result-bar"); if (nb) nb.remove(); }
    update();
    // Show the sticky result bar only while the result panel is out of view (any layout, any text size).
    var bar0 = el.querySelector(".result-bar"), resEl = document.getElementById("result");
    if (window.IntersectionObserver && bar0 && resEl) {
      var io = new IntersectionObserver(function (es) { es.forEach(function (e) { barHidden = e.isIntersecting; bar0.classList.toggle("is-hidden", barHidden); }); }, { threshold: [0, 0.15] });
      io.observe(resEl);
    }
    return { result: function () { return last; } };
  }

  /* ---------------- guide (renders model data only) ---------------- */
  var SELECT_TEXT = { grade: "The result is the single grade selected.", classification: "The result is the single category selected." };
  var COMP_HEAD = { score: "Scoring components", grade: "Grade definitions", classification: "Category definitions", measurement: "Inputs" };
  var METHOD_TEXT = { sum: "The result is the sum of the item points.", select: "The result is the single level selected.", expression: "The result is derived from the item points using the published formula." };
  var NT_TEXT = { block: "If any item is not testable, no total is reported; the testable components are shown instead.",
    exclude: "Items marked untestable contribute no points and are flagged; the total may underestimate the true value." };
  /** The 14 Guide sections, in order. `id` is a stable anchor (g-<id>). */
  var GUIDE = [["overview", "Overview"], ["purpose", "Purpose"], ["population", "Intended population"], ["when", "When to use"], ["calculation", "Calculation"],
    ["interpretation", "Interpretation"], ["context", "Clinical context"], ["limitations", "Limitations"], ["confounders", "Confounders"], ["mistakes", "Common mistakes"],
    ["boundaries", "What it does not tell you"], ["related", "Related scores"], ["version", "Version"], ["sources", "Sources"]];
  function sentences(t) { return String(t || "").split(/(?<=[.;])\s+(?=[A-Z0-9])/).map(function (x) { return x.trim(); }).filter(Boolean); }
  function infoBox(title, html, tone) { return '<div class="g-box tone-' + (tone || "info") + '">' + (title ? '<b class="g-box-title">' + esc(title) + "</b>" : "") + html + "</div>"; }
  function factTable(rows) {
    return '<table class="g-facts"><tbody>' + rows.filter(function (r) { return r[1]; }).map(function (r) { return '<tr><th scope="row">' + esc(r[0]) + "</th><td>" + r[1] + "</td></tr>"; }).join("") + "</tbody></table>";
  }

  /** guideHTML(score, links, calcHref, ctx) — ctx: { clusters: [...], entry: id → catalogue entry } */
  function guideHTML(score, links, calcHref, ctx) {
    ctx = ctx || {}; var entry = ctx.entry || function () { return null; };
    var g = score.guideSections || {}, cm = score.calculationMethod, I = global.InsulaEngine.insights;
    var GI = I.forGuide(score), pres = I.presentation(score);
    var sec = function (t) { return GI.filter(function (x) { return x.type === t; })[0]; };
    var cards = function (t) { var x = sec(t); return x && x.items.length ? UI.InsightSection({ section: x, hideTitle: true }) : '<p class="lede">None listed.</p>'; };
    var notice = score.calculatorNotice ? (score.calculatorNotice.tone === "warning" ? UI.WarningBanner : UI.InfoBanner)({ title: score.calculatorNotice.title, message: score.calculatorNotice.message }) : "";
    var noticeKey = score.calculatorNotice ? score.calculatorNotice.title.toLowerCase().slice(0, 30) : null;
    var majors = sec("limitation").items.filter(function (i) { return i.importance === "major" && !(noticeKey && i.text.toLowerCase().indexOf(noticeKey) === 0); });
    var allLims = sec("limitation").items.length;

    /* 1 Overview: highlight box, at-a-glance table, key warnings (limitations surfaced at the top) */
    var overview = infoBox(null, "<p>" + esc(g.what) + "</p>", "primary") +
      factTable([["Type", esc(TYPE_LABEL[score.itemType] || "Score")], ["Result type", pres ? esc(pres.typeLabel) : ""], ["Range", esc(rangeLabel(score))],
                 ["Components", (function () { var n = score.inputDefinitions.filter(function (d) { return !d.detail; }).length; return n + (score.itemType === "score" ? " scored input" : " input") + (n === 1 ? "" : "s"); })()],
                 ["Version", esc(score.version.label)], ["Category", esc(score.subcategory)], ["Review", /pending/i.test(score.reviewStatus) ? "Pending independent clinician review" : esc(score.reviewStatus)]]) +
      '<div class="guide-warnings" data-block="key-warnings"><h4 class="sub-h">' + UI.icon("warning") + " Key warnings and limitations</h4>" + (notice || "") +
      (majors.length ? '<ul class="insight-list">' + majors.map(function (i) { return UI.InsightCard({ type: "limitation", item: { text: i.text, importance: "major" } }); }).join("") + "</ul>" : "") +
      '<a class="g-jump" href="#" data-jump="g-limitations">See all ' + allLims + " limitation" + (allLims === 1 ? "" : "s") + " →</a></div>";

    /* 4 When to use: bullet points */
    var whenList = sentences(g.whenToUse);
    var when = whenList.length > 1 ? '<ul class="g-points">' + whenList.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + "</ul>" : "<p>" + esc(g.whenToUse) + "</p>";

    /* 5 Calculation: numbered steps, method box, component tables */
    var steps = sentences(g.howToPerform);
    var TYPE_COL = { score: "Value", grade: "Grade", classification: "Class", measurement: "Value" };
    var colHead = function (d) {
      if (d.type === "multi" || d.pointBands) return "Points";
      var asCode = (d.options || []).some(function (o) { return o.code != null && String(o.code) !== String(o.points); });
      if (!asCode) return "Points";
      return cm.type === "select" && cm.input === d.id ? (TYPE_COL[score.itemType] || "Value") : "Code";
    };
    var detailDefs = score.inputDefinitions.filter(function (d) { return d.detail; });
    var comps = score.components.map(function (c) {
      var defs = c.inputs.map(function (id) { return score.inputDefinitions.filter(function (x) { return x.id === id; })[0]; }).filter(function (d) { return !d.detail; });
      if (!defs.length) return "";
      var plain = defs.length > 1 && defs.every(function (d) { return !d.options && !d.pointBands && d.min != null; });
      if (plain) return '<div class="guide-comp"><h4>' + esc(c.label) + '</h4><div class="table-scroll"><table class="breakdown"><thead><tr><th scope="col">Input</th><th scope="col" class="pts">Range</th></tr></thead><tbody>' +
        defs.map(function (d) { return "<tr><td>" + esc(d.label) + (d.help ? '<br><span class="choice-detail">' + esc(d.help) + "</span>" : "") + '</td><td class="pts">' + d.min + "–" + d.max + (d.unit ? " " + esc(d.unit) : "") + "</td></tr>"; }).join("") +
        "</tbody></table></div></div>";
      return '<div class="guide-comp"><h4>' + esc(defs.length === 1 ? defs[0].label : c.label) + "</h4>" + defs.map(function (d) {
        var rows;
        if (d.options) rows = d.options.map(function (o) {
          return "<tr><td>" + esc(o.label) + (o.detail ? '<br><span class="choice-detail">' + esc(o.detail) + "</span>" : "") + '</td><td class="pts">' + esc(o.exclusive ? "—" : optTag(o)) + "</td></tr>"; }).join("") +
          (d.notTestable ? '<tr class="bd-nt"><td><i>' + esc(d.notTestable.label) + "</i>" + (d.notTestable.reasons ? '<br><span class="choice-detail">Allowed for: ' + esc(d.notTestable.reasons.join(", ")) + "</span>" : "") + '</td><td class="pts">' + esc(d.notTestable.code || "NT") + "</td></tr>" : "");
        else if (d.pointBands) rows = d.pointBands.map(function (bd) { return "<tr><td>" + (bd.min == null ? "≤ " + bd.max : bd.max == null ? "≥ " + bd.min : bd.min === bd.max ? bd.min : bd.min + "–" + bd.max) + (d.unit ? " " + esc(d.unit) : "") + '</td><td class="pts">' + bd.points + "</td></tr>"; }).join("");
        else rows = "<tr><td>Whole number " + d.min + "–" + d.max + (d.unit ? " " + esc(d.unit) : "") + '</td><td class="pts">value</td></tr>';
        var oneCol = d.options && !d.notTestable && d.options.every(function (o) { return optTag(o) === "" || optTag(o) == null; });
        if (oneCol) rows = rows.replace(/<td class="pts">[^<]*<\/td>/g, "");
        return (defs.length > 1 ? '<p class="guide-item">' + esc(d.label) + (d.required === false ? " (optional)" : "") + "</p>" : "") + (d.help ? '<p class="field-help">' + esc(d.help) + "</p>" : "") +
          '<div class="table-scroll"><table class="breakdown"><thead><tr><th scope="col">' + (d.type === "multi" ? "Select all that apply" : oneCol ? "Category" : "Option") + "</th>" + (oneCol ? "" : '<th scope="col" class="pts">' + (d.options || d.pointBands ? colHead(d) : "Value") + "</th>") + "</tr></thead><tbody>" + rows + "</tbody></table></div>";
      }).join("") + "</div>";
    }).join("") +
      (detailDefs.length ? '<p class="lede">Optional details for your note (not scored): ' + esc(detailDefs.map(function (d) { return d.label.toLowerCase(); }).join(", ")) + ".</p>" : "");
    var calculation = (steps.length ? '<ol class="g-steps">' + steps.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + "</ol>" : "") +
      infoBox("Method", "<p>" + esc(cm.type === "select" ? (SELECT_TEXT[score.itemType] || METHOD_TEXT.select) : METHOD_TEXT[cm.type]) + " Range: " + esc(rangeLabel(score)) + "." + (cm.formula ? " Components are reported individually alongside the result." : "") + "</p>" +
        (score.inputDefinitions.some(function (d) { return d.notTestable; }) ? "<p>" + esc(NT_TEXT[cm.notTestablePolicy || "block"]) + "</p>" : ""), "info") +
      '<h4 class="sub-h">' + esc(cm.type === "select" ? (COMP_HEAD[score.itemType] || "Scoring components") : "Scoring components") + "</h4>" + comps;

    /* 6 Interpretation: result type card + state cards */
    var interp = (pres ? UI.InsightSection({ section: { type: "interpretation", title: "Result type", question: "", items: [{ title: pres.typeLabel, text: pres.describes }] }, hideTitle: true }) : "") +
      '<h4 class="sub-h">Result states</h4><ul class="insight-list">' + score.resultStates.map(function (st) {
        return UI.StateCard({ tone: st.tone, range: st.range, label: st.label.replace(/\{[^}]+\}/g, "").trim() || UI.TONE_LABEL[st.tone], summary: st.summary, detail: st.detail }); }).join("") + "</ul>";

    /* 7 Clinical context */
    var context = (g.clinicalContext ? infoBox(null, "<p>" + esc(g.clinicalContext) + "</p>", "primary") : "") +
      '<h4 class="sub-h">What it helps describe</h4>' + cards("context") + '<h4 class="sub-h">Important considerations</h4>' + cards("consideration");

    /* 12 Related scores: own list with relation + clinical clusters */
    var relRow = function (id, relation, current) {
      var e = entry(id); if (!e) return "";
      var gl = links(id, "guide"), cl = e.status === "implemented" ? links(id, "calculate") : null;
      var badge = e.status === "implemented" ? "" : UI.StatusBadge({ tone: "neutral", label: "Placeholder", icon: false });
      return '<li class="score-card related-row' + (current ? " is-current" : "") + '" data-related="' + esc(id) + '"><a class="open" href="' + gl.href + '" data-nav><span class="row-icon" aria-hidden="true">' + UI.icon("guide") + '</span><span class="text"><span class="title">' + esc(e.abbreviation) + " " + badge + '</span><span class="sub">' + esc(relation || e.name) + "</span></span></a>" +
        (cl ? '<a class="alt-view" href="' + cl.href + '" data-nav aria-label="Open ' + esc(e.abbreviation) + ' calculator">' + UI.icon("calculate") + '<span aria-hidden="true">Calculate</span></a>' : "") + "</li>";
    };
    var own = score.relatedScores.map(function (r) { return relRow(r.id, r.relation); }).filter(Boolean);
    var groups = (ctx.clusters || []).filter(function (c) { return c.members.indexOf(score.id) >= 0; });
    var related = (own.length ? '<h4 class="sub-h">Directly related</h4><ul class="card-list">' + own.join("") + "</ul>" : "") +
      groups.map(function (c) {
        var shownIds = score.relatedScores.map(function (r) { return r.id; });
        var rest = c.members.filter(function (m) { return m !== score.id && shownIds.indexOf(m) < 0; });
        var members = rest.map(function (m) { return relRow(m, null); }).filter(Boolean);
        return '<div class="g-cluster" data-cluster="' + esc(c.id) + '"><h4 class="sub-h">' + UI.icon("compass") + " " + esc(c.title) + '</h4><p class="lede">' + esc(c.description) + "</p>" +
          (members.length ? '<ul class="card-list">' + members.join("") + "</ul>" : '<p class="lede">All other scores in this group are listed above.</p>') + "</div>";
      }).join("");

    var version = factTable([["Version", esc(score.version.label)], ["Details", esc(score.version.detail)], ["Specialties", esc(score.specialties.join(", "))], ["Content", "v" + esc(score.contentVersion)],
      ["Last reviewed", esc(score.lastReviewed)], ["Review status", esc(score.reviewStatus)], ["Licensing", score.licensing ? esc(score.licensing.status) + ". " + esc(score.licensing.note) : ""]]);
    var sources = '<ol class="sources">' + score.sources.map(function (src) {
      var href = src.doi ? "https://doi.org/" + src.doi : src.url; return "<li>" + esc(src.citation) + (href ? ' <a href="' + esc(href) + '" data-ext>' + esc(src.doi ? "doi:" + src.doi : "Source") + "</a>" : "") + "</li>"; }).join("") + "</ol>";

    var body = { overview: overview, purpose: infoBox(null, "<p>" + esc(score.purpose) + "</p>", "info"), population: "<p>" + esc(score.intendedPopulation) + "</p>", when: when,
      calculation: calculation, interpretation: interp, context: context, limitations: cards("limitation"), confounders: cards("confounder"),
      mistakes: '<ul class="insight-list">' + score.commonErrors.map(function (t) { return UI.InsightCard({ type: "warning", item: { text: t } }); }).join("") + "</ul>",
      boundaries: cards("boundary"), related: related || '<p class="lede">None listed.</p>', version: version, sources: sources };
    var toc = '<nav class="toc" aria-label="Guide sections">' + GUIDE.map(function (x, i) {
      return '<a href="#" data-jump="g-' + x[0] + '"' + (x[0] === "limitations" ? ' class="toc-warn"' : "") + ">" + (i + 1) + ". " + esc(x[1]) + "</a>"; }).join("") + "</nav>";
    return '<div class="guide-nav top" data-block="guide-nav-top">' + UI.PrimaryButton({ label: "Calculate", icon: "calculate", href: calcHref, replace: true }) +
        '<a class="g-jump" href="#" data-jump="g-related">Related scores →</a></div>' +
      UI.Section({ id: "contents", title: "Contents", body: toc }) + '<div class="section guide-body">' +
      GUIDE.map(function (x, i) { return UI.SectionCard({ id: "g-" + x[0], number: i + 1, title: x[1], body: body[x[0]] }); }).join("") + "</div>" +
      '<div class="section guide-nav bottom" data-block="guide-nav-bottom">' + UI.PrimaryButton({ label: "Calculate this score", icon: "calculate", href: calcHref, replace: true, block: true }) + "</div>";
  }
  guideHTML.SECTIONS = GUIDE;

  global.Calculator = { mount: mount, guideHTML: guideHTML };
})(window);
