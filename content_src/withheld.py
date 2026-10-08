"""Insula Neuro Score — WITHHELD content (not built, not shipped, not shown in the app).

Scores here were verified against their sources but are held back for a non-content reason
(e.g. licensing). build_scores.py never imports this module, so no JSON is generated for them;
the catalogue lists them under `withheld` with the reason. Kept so that reinstatement after review
is a one-line change (move the score back into a built library and remove it from UNDER_REVIEW).
Hand-calculated test cases for these scores live in tests/engine/fixtures-withheld/.
"""
from library import o, single, st, conf, score

def build():
    L = []
    # ================================================================ RASS (licensing)
    rass_opts = [o(4, "+4 Combative", 4, "+4", "Overtly combative or violent; immediate danger to staff."), o(3, "+3 Very agitated", 3, "+3", "Pulls on or removes tubes or catheters; aggressive."),
                 o(2, "+2 Agitated", 2, "+2", "Frequent non-purposeful movement; fights the ventilator."), o(1, "+1 Restless", 1, "+1", "Anxious; movements not aggressive or vigorous."),
                 o(0, "0 Alert and calm", 0, "0"), o(-1, "−1 Drowsy", -1, "-1", "Sustained (>10 s) awakening with eye contact to voice."),
                 o(-2, "−2 Light sedation", -2, "-2", "Briefly (<10 s) awakens with eye contact to voice."), o(-3, "−3 Moderate sedation", -3, "-3", "Movement or eye opening to voice, no eye contact."),
                 o(-4, "−4 Deep sedation", -4, "-4", "No response to voice; movement or eye opening to physical stimulation."), o(-5, "−5 Unarousable", -5, "-5", "No response to voice or physical stimulation.")]
    L.append(score(id="rass", name="Richmond Agitation–Sedation Scale", abbreviation="RASS", aliases=["sedation", "agitation", "richmond", "icu"],
        category="neurocritical", subcategory="Sedation and agitation", specialties=["Neurocritical Care", "Critical Care"],
        version={"label": "RASS (Sessler et al. 2002)", "detail": "10 levels from +4 (combative) to −5 (unarousable)."},
        purpose="Standardised description of agitation and sedation depth.", intendedPopulation="Adult ICU patients.",
        resultPresentation={"type": "classification", "typeLabel": "Arousal level", "meter": False},
        calculatorNotice={"tone": "info", "title": "Compare with the target", "message": "RASS describes arousal. The appropriate level depends on the sedation target set for the patient."},
        inputDefinitions=[single("level", "Observed level", "RASS", rass_opts, help="Observe; if not alert, address by name; use physical stimulation only if there is no response to voice.")],
        calculationMethod={"type": "select", "input": "level", "range": {"min": -5, "max": 4}, "display": "RASS {signed(total)}", "share": "RASS {signed(total)}"},
        interpretationRules=[{"when": "total >= 3", "state": "severe"}, {"when": "total >= 1", "state": "restless"}, {"when": "total == 0", "state": "calm"},
                             {"when": "total >= -3", "state": "sedated"}, {"state": "deep"}],
        resultStates=[st("severe", "high", "Severe agitation", "Agitation with risk to patient or staff safety.", "+3 to +4", "Assess for pain, delirium, hypoxia, withdrawal and other causes according to local protocol."),
                      st("restless", "mild", "Restless to agitated", "Increased activity or agitation.", "+1 to +2"),
                      st("calm", "favorable", "Alert and calm", "Alert and calm at this assessment.", "0", "Delirium can be present in an alert, calm patient; screen separately."),
                      st("sedated", "informational", "Drowsy to moderate sedation", "Responds to voice.", "−1 to −3"),
                      st("deep", "moderate", "Deep sedation or unarousable", "No response to voice.", "−4 to −5", "Whether this is appropriate depends on the sedation target. Delirium screening is not possible at this level.")],
        clinicalContext=[{"text": "A standard ICU arousal scale and the first step of CAM-ICU delirium screening.", "importance": "major"}],
        clinicalInsights=[{"when": "total >= -3", "text": "Delirium screening (e.g. CAM-ICU) is possible at RASS −3 or above."}],
        limitations=[{"importance": "major", "text": "Depends on response to voice: limited in deafness, language barriers or neurological deficits."}, "Validated in adult ICU populations."],
        confounders=conf(("Neuromuscular blockade", "Prevents assessment."), ("Structural brain injury", "Alters arousal independent of sedation."), ("Deafness or language barrier", "Affects response to voice.")),
        whatItDoesNotTellYou=["Presence of delirium.", "Pain level.", "The cause of agitation or reduced arousal."],
        commonErrors=["Using physical stimulation before voice.", "Confusing brief (−2) and sustained (−1) eye contact."],
        relatedScores=[{"id": "gcs", "relation": "Level of consciousness"}],
        guideSections={"what": "A 10-level scale from +4 (combative) to −5 (unarousable).", "whenToUse": "Sedation titration and arousal assessment in ICU.",
            "howToPerform": "Observe for 30 s; address by name; then physical stimulation if no response to voice.", "clinicalContext": "Compared with an individualised sedation target."},
        sources=[{"citation": "Sessler CN, Gosnell MS, Grap MJ, et al. The Richmond Agitation-Sedation Scale: validity and reliability in adult intensive care unit patients. Am J Respir Crit Care Med. 2002;166(10):1338-1344."}],
        licensing={"status": "Withheld: licensing not confirmed", "note": "Virginia Commonwealth University lists RASS as a licensable technology. Not shipped until terms for use in this app are confirmed."}))

    return L
