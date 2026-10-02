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
          '<input id="' + fieldId(d) + '" type="text" inputmode="' + (d.type === "integer" ? "numeric" : "decimal") + '" autocomplete="off" data-input="' + esc(d.id) + '" data-step-size="' + step + '" value="' + (nt || a == null ? "" : esc(a)) + '" aria-describedby="' + described + '"' + (nt ? " disabled" : "") + ">" +
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
  function choiceRow(d, kind, o, checked) {
    var tag = o.isNT ? (o.code || "NT") : (o.code != null ? o.code : o.points);
    return '<label class="choice' + (checked ? " is-on" : "") + (o.isNT ? " is-nt" : "") + '"><input type="' + kind + '" class="vh" name="' + esc(d.id) + '" value="' + esc(o.value) + '" data-input="' + esc(d.id) + '"' + (checked ? " checked" : "") + ">" +
      '<span class="mark ' + kind + '" aria-hidden="true"></span><span class="choice-text"><span class="choice-label">' + esc(o.label) + "</span>" + (o.detail ? '<span class="choice-detail">' + esc(o.detail) + "</span>" : "") + "</span>" +
      (tag != null ? '<span class="choice-pts" aria-hidden="true">' + esc(tag) + "</span>" : "") + "</label>";
  }

  /* ---------------- result panel (renders ResultModel only) ---------------- */
  /** Avoid "7 · NIHSS 7": if the state label only restates the value, show the tone name. */
  function stateLabel(r) {
    var l = String(r.state.label || ""), d = String(r.display);
    return l && d !== "–" && l.indexOf(d) >= 0 && l.replace(d, "").replace(/[^A-Za-z]/g, "").length <= 6 ? UI.TONE_LABEL[r.state.tone] : l;
  }
  /* Result order: Score → Breakdown → Interpretation → Context → Considerations → Limitations → Confounders → Boundaries → Related */
  function resultHTML(score, r, links) {
    var tone = r.state.tone, pres = r.presentation || {};
    var meter = r.bands ? UI.ScaleMeter({ min: r.range.min, max: r.range.max, value: r.status === "complete" ? r.total : null, bands: r.bands, label: score.abbreviation }) : "";
    var h = UI.ResultCard({ tone: tone, label: stateLabel(r), value: r.display, typeLabel: pres.typeLabel,
      formula: r.formula, formulaJoin: r.formula && r.status === "complete" && r.formulaEquals !== false ? "=" : null,
      meta: UI.TONE_LABEL[tone] + " · " + score.abbreviation + " range " + r.range.min + "–" + r.range.max, summary: r.state.summary, meter: meter });
    if (r.warnings.length) h += '<div class="result-block" data-block="warnings">' + r.warnings.map(function (w) { return UI.WarningBanner({ title: "Check", message: w.message }); }).join("") + "</div>";
    // Breakdown
    h += '<div class="result-block" data-block="breakdown"><h3 class="result-h">Breakdown</h3><table class="breakdown"><tbody>' + r.breakdown.map(function (c) {
      var rows = c.items.map(function (it) {
        return '<tr class="bd-' + it.status + '"><th scope="row">' + esc(it.short) + "</th><td>" + esc(it.display) + (it.reason ? " (" + esc(it.reason) + ")" : "") +
          '</td><td class="pts">' + esc(it.status === "ok" ? (it.code != null ? it.code : it.points) : it.status === "nt" ? it.code : "–") + "</td></tr>";
      }).join("");
      var head = c.items.length > 1 ? '<tr class="bd-group"><th scope="rowgroup" colspan="2">' + esc(c.label) + '</th><td class="pts">' + (c.subtotal == null ? "–" : c.subtotal) + "</td></tr>" : "";
      return head + rows;
    }).join("") + '<tr class="bd-total"><th scope="row">Result</th><td>' + esc(r.state.label) + '</td><td class="pts">' + esc(r.formula && r.status !== "complete" ? r.formula.replace(/ \+ /g, " ") : r.display) + "</td></tr></tbody></table></div>";
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
    h += '<div class="result-block btn-row">' + UI.SecondaryButton({ label: "Reset", icon: "reset", act: "calc-reset" }) +
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
    var grouped = score.components.map(function (c) {
      var defs = c.inputs.map(function (id) { return score.inputDefinitions.filter(function (d) { return d.id === id; })[0]; });
      var inner = defs.map(function (d) { return controlHTML(d, answers[d.id]); }).join("");
      return score.components.length > 1 && c.inputs.length > 1 ? '<section class="input-group"><h3 class="input-group-h">' + esc(c.label) + "</h3>" + inner + "</section>" : inner;
    }).join("");
    el.innerHTML = '<div class="detail-grid two calc"><form class="calc-inputs" novalidate onsubmit="return false" aria-label="' + esc(score.abbreviation) + ' inputs">' +
      (score.calculatorNotice ? '<div class="calc-notice">' + (score.calculatorNotice.tone === "warning" ? UI.WarningBanner : UI.InfoBanner)({ title: score.calculatorNotice.title, message: score.calculatorNotice.message }) + "</div>" : "") +
      '<div class="calc-progress" aria-live="polite"></div>' + grouped + '</form><div class="aside"><section id="result" aria-label="Result" tabindex="-1"></section></div></div>' +
      '<button type="button" class="result-bar" data-act="calc-jump" aria-label="Jump to result"></button>';

    var last = null;
    function update(changedId) {
      var r = Engine.calculate(score, answers); last = r;
      document.getElementById("result").innerHTML = resultHTML(score, r, links);
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
      bar.className = "result-bar tone-" + r.state.tone;
      // Compact only code-style formulas (e.g. "E3 + V4 + M5" → "E3 V4 M5"); other formulas are not shown in the bar.
      var compact = r.formula && /^[A-Z]+[A-Z0-9]*( \+ [A-Z]+[A-Z0-9]*)+$/.test(r.formula) ? r.formula.replace(/ \+ /g, " ") : null;
      var barValue = compact ? (r.status === "complete" ? compact + " = " + r.display : compact) : r.display;
      bar.innerHTML = UI.stateIcon(r.state.tone) + '<span class="rb-value' + (compact ? " has-formula" : "") + '">' + esc(barValue) + '</span><span class="rb-label">' + esc(r.status === "incomplete" ? done + " of " + total + " answered" : stateLabel(r)) + "</span>" + UI.icon("down");
      if (opts.onResult) opts.onResult(r);
    }
    function setAnswer(id, v) { if (v === undefined) delete answers[id]; else answers[id] = v; }
    function def(id) { return score.inputDefinitions.filter(function (d) { return d.id === id; })[0]; }
    function rerenderField(id) {
      var d = def(id), f = el.querySelector('[data-field="' + id + '"]'), tmp = document.createElement("div");
      tmp.innerHTML = controlHTML(d, answers[id]); f.replaceWith(tmp.firstChild);
    }

    el.addEventListener("change", function (ev) {
      var t = ev.target, id = t.getAttribute("data-input"); if (!id) return;
      var d = def(id), part = t.getAttribute("data-part");
      if (part === "nt") { setAnswer(id, t.checked ? { nt: true } : undefined); rerenderField(id); }
      else if (part === "reason") { setAnswer(id, { nt: true, reason: t.value || undefined }); }
      else if (part === "unit") { var cur = answers[id] && !ntValue(answers[id]) ? answers[id] : {}; setAnswer(id, { value: cur.value, unit: t.value }); }
      else if (d.type === "single") { setAnswer(id, t.value === "__nt" ? { nt: true } : t.value); rerenderField(id); }
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
      if (act === "calc-reset") { Object.keys(answers).forEach(function (k) { delete answers[k]; }); mount(el, score, answers, opts); if (opts.toast) opts.toast("Inputs cleared"); var first = el.querySelector("[data-input]"); if (first) first.focus(); }
      else if (act === "calc-copy" && last) { var txt = shareText(score, last); try { if (Android && Android.copy) Android.copy(txt); else navigator.clipboard.writeText(txt); if (opts.toast) opts.toast("Result copied"); } catch (e) { if (opts.toast) opts.toast("Copy failed"); } }
      else if (act === "calc-share" && last) { var tx = shareText(score, last); try { if (Android && Android.share) Android.share(tx); else if (navigator.share) navigator.share({ text: tx }); else { navigator.clipboard.writeText(tx); if (opts.toast) opts.toast("Result copied"); } } catch (e) {} }
      else if (act === "calc-jump") { var res = document.getElementById("result"); res.scrollIntoView({ block: "start" }); res.focus({ preventScroll: true }); }
    });
    update();
    return { result: function () { return last; } };
  }

  /* ---------------- guide (renders model data only) ---------------- */
  var METHOD_TEXT = { sum: "The result is the sum of the item points.", select: "The result is the single level selected.", expression: "The result is derived from the item points using the published formula." };
  var NT_TEXT = { block: "If any item is not testable, a total is not reported; the testable components are shown instead.",
    exclude: "Items marked untestable contribute no points and are flagged; the total may underestimate the true value." };
  function guideHTML(score, links, calcHref) {
    var g = score.guideSections || {}, cm = score.calculationMethod;
    var GI = window.InsulaEngine.insights.forGuide(score);
    var gsec = function (type, keepTitle) { var sec = GI.filter(function (x) { return x.type === type; })[0]; return sec && sec.items.length ? UI.InsightSection({ section: sec, hideTitle: !keepTitle }) : '<p class="lede">None listed.</p>'; };
    var errorsList = '<ul class="insight-list">' + score.commonErrors.map(function (t) { return UI.InsightCard({ type: "warning", item: { text: t } }); }).join("") + "</ul>";
    var comps = score.components.map(function (c) {
      return '<div class="guide-comp"><h4>' + esc(c.label) + "</h4>" + c.inputs.map(function (id) {
        var d = score.inputDefinitions.filter(function (x) { return x.id === id; })[0];
        var body = d.options ? '<table class="breakdown"><tbody>' + d.options.map(function (o) {
          return "<tr><td>" + esc(o.label) + (o.detail ? '<br><span class="choice-detail">' + esc(o.detail) + "</span>" : "") + '</td><td class="pts">' + esc(o.code != null ? o.code : o.points) + "</td></tr>"; }).join("") +
          (d.notTestable ? '<tr><td><i>' + esc(d.notTestable.label) + "</i>" + (d.notTestable.reasons ? '<br><span class="choice-detail">Allowed for: ' + esc(d.notTestable.reasons.join(", ")) + "</span>" : "") + '</td><td class="pts">' + esc(d.notTestable.code || "NT") + "</td></tr>" : "") + "</tbody></table>"
          : '<p class="lede">' + esc(d.type) + " " + rangeText(d, d.unit) + "</p>";
        return (c.inputs.length > 1 ? '<p class="guide-item">' + esc(d.label) + "</p>" : "") + (d.help ? '<p class="field-help">' + esc(d.help) + "</p>" : "") + body;
      }).join("") + "</div>";
    }).join("");
    var interp = '<ul class="insight-list">' + score.resultStates.map(function (st) { return UI.StateCard({ tone: st.tone, range: st.range, label: st.label.replace(/\{[^}]+\}/g, "").trim() || UI.TONE_LABEL[st.tone], summary: st.summary, detail: st.detail }); }).join("") + "</ul>";
    var noticeKey = score.calculatorNotice ? score.calculatorNotice.title.toLowerCase().slice(0, 30) : null;
    var majorLims = GI.filter(function (x) { return x.type === "limitation"; })[0].items.filter(function (i) {
      return i.importance === "major" && !(noticeKey && i.text.toLowerCase().indexOf(noticeKey) === 0);   // don't repeat the notice
    });
    var notice = score.calculatorNotice ? (score.calculatorNotice.tone === "warning" ? UI.WarningBanner : UI.InfoBanner)({ title: score.calculatorNotice.title, message: score.calculatorNotice.message }) : "";
    var pres = score.resultPresentation;
    var secs = [
      ["What is it?", "<p>" + esc(g.what) + "</p>" + '<div class="guide-warnings" data-block="key-warnings">' + (notice || "") +
        (majorLims.length ? '<ul class="insight-list">' + majorLims.map(function (i) { return UI.InsightCard({ type: "warning", item: { text: i.text, importance: "major" } }); }).join("") + "</ul>" : "") + "</div>"],
      ["Purpose", "<p>" + esc(score.purpose) + "</p>"],
      ["Intended population", "<p>" + esc(score.intendedPopulation) + "</p>"],
      ["When to use", "<p>" + esc(g.whenToUse) + "</p>"],
      ["How to perform / calculate", "<p>" + esc(g.howToPerform) + "</p><p>" + esc(METHOD_TEXT[cm.type]) + " Range " + cm.range.min + "–" + cm.range.max + ".</p>" +
        (cm.formula ? "<p>Components are reported individually before the total.</p>" : "") +
        (score.inputDefinitions.some(function (d) { return d.notTestable; }) ? "<p>" + esc(NT_TEXT[cm.notTestablePolicy || "block"]) + "</p>" : "")],
      ["Scoring components", comps],
      ["Interpretation", (pres ? UI.InsightSection({ section: { type: "interpretation", title: "Result type", question: "", items: [{ title: (window.InsulaEngine.insights.presentation(score) || {}).typeLabel, text: (window.InsulaEngine.insights.presentation(score) || {}).describes }] } }) : "") +
        '<h4 class="sub-h">Result states</h4>' + interp],
      ["Clinical context", "<p>" + esc(g.clinicalContext) + "</p>" + gsec("context", true) + gsec("consideration", true)],
      ["Limitations", gsec("limitation")],
      ["Confounders", gsec("confounder")],
      ["Common mistakes", errorsList],
      ["What the score does not tell you", gsec("boundary")],
      ["Related scores", '<div class="chip-row">' + score.relatedScores.map(function (x) { var l = links(x.id, "guide"); return l ? '<a class="chip" href="' + l.href + '" data-nav>' + esc(l.label) + ' <span class="n">' + esc(x.relation) + "</span></a>" : ""; }).join("") + "</div>"],
      ["Version", '<dl class="vinfo"><dt>Version</dt><dd>' + esc(score.version.label) + "</dd><dt>Details</dt><dd>" + esc(score.version.detail) + "</dd><dt>Category</dt><dd>" + esc(score.subcategory) +
        "</dd><dt>Specialties</dt><dd>" + esc(score.specialties.join(", ")) + "</dd><dt>Content</dt><dd>v" + esc(score.contentVersion) + "</dd><dt>Last reviewed</dt><dd>" + esc(score.lastReviewed) +
        "</dd><dt>Review status</dt><dd>" + esc(score.reviewStatus) + "</dd>" + (score.licensing ? "<dt>Licensing</dt><dd>" + esc(score.licensing.status) + ". " + esc(score.licensing.note) + "</dd>" : "") + "</dl>"],
      ["Sources", '<ol class="sources">' + score.sources.map(function (s) {
        var href = s.doi ? "https://doi.org/" + s.doi : s.url; return "<li>" + esc(s.citation) + (href ? ' <a href="' + esc(href) + '" data-ext>' + esc(s.doi ? "doi:" + s.doi : "Source") + "</a>" : "") + "</li>"; }).join("") + "</ol>"]
    ];
    var toc = '<nav class="toc" aria-label="Guide sections">' + secs.map(function (s, i) { return '<a href="#" data-jump="g' + (i + 1) + '">' + (i + 1) + ". " + esc(s[0].split(" / ")[0]) + "</a>"; }).join("") + "</nav>";
    return '<div class="section">' + UI.PrimaryButton({ label: "Calculate this score →", icon: "calculate", href: calcHref, replace: true, block: true }) + "</div>" +
      UI.Section({ id: "contents", title: "Contents", body: toc }) + '<div class="section">' +
      secs.map(function (s, i) { return UI.SectionCard({ id: "g" + (i + 1), number: i + 1, title: s[0], body: s[1] }); }).join("") + "</div>" +
      '<div class="section">' + UI.PrimaryButton({ label: "Calculate this score →", icon: "calculate", href: calcHref, replace: true, block: true }) + "</div>";
  }

  global.Calculator = { mount: mount, guideHTML: guideHTML };
})(window);
