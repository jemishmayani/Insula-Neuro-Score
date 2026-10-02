"""Insula Neuro Score — Phase 2 score content.
Writes app/assets/content/scores/<id>.json for each score.
All descriptors are paraphrased in original wording from the cited sources.
Run: python3 content_src/build_scores.py"""
import json, os

REVIEWED = "2026-10-01"
REVIEW = "Drafted from primary sources; pending independent clinician review before clinical release."
CV = "2.0.0"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "app", "assets", "content")

def o(value, label, points, code=None, detail=None):
    d = {"value": str(value), "label": label, "points": points}
    if code is not None: d["code"] = code
    if detail: d["detail"] = detail
    return d

def base(**kw):
    d = {"contentVersion": CV, "lastReviewed": REVIEWED, "reviewStatus": REVIEW, "scoringRules": [], "consistencyRules": [], "aliases": []}
    d.update(kw); return d

scores = []

# =====================================================================  GCS
# Verified: Glasgow structured approach (glasgowcomascale.org; Teasdale et al. 2014) — criteria, ratings,
# NT definitions, and "if any component is non-testable, do not provide a total".
GCS_NOTICE = {"tone": "info", "title": "Document E, V and M separately",
  "message": "If a component cannot be tested, record it as non-testable (NT) with the reason. Do not substitute a score of 1, and do not report a total."}
scores.append(base(
  id="gcs", name="Glasgow Coma Scale", abbreviation="GCS", aliases=["glasgow", "coma", "consciousness", "evm"],
  category="consciousness", subcategory="Level of consciousness", specialties=["Neurology", "Neurosurgery", "Neurocritical Care", "Emergency Medicine", "Trauma"],
  version={"label": "Adult GCS, Glasgow structured approach", "detail": "Teasdale & Jennett (1974) scale as assessed with the Glasgow structured approach (Teasdale et al. 2014; glasgowcomascale.org), including non-testable (NT) ratings. The paediatric GCS is a separate instrument and is not implemented."},
  purpose="A standardised, communicable description of a patient's level of consciousness, based on the best eye, verbal and motor responses.",
  intendedPopulation="Adults and older children with impaired consciousness from any cause. The 3–8 / 9–12 / 13–15 categories come from traumatic brain injury.",
  resultPresentation={"type": "severity", "typeLabel": "Level of consciousness", "meter": True},
  calculatorNotice=GCS_NOTICE,
  components=[{"id": "eye", "label": "Eye opening (E)", "inputs": ["e"]}, {"id": "verbal", "label": "Verbal response (V)", "inputs": ["v"]}, {"id": "motor", "label": "Best motor response (M)", "inputs": ["m"]}],
  inputDefinitions=[
    {"id": "e", "type": "single", "label": "Eye opening (E)", "short": "E", "help": "Check for factors that interfere, observe, then stimulate: sound before physical pressure.",
     "notTestable": {"label": "Non-testable", "code": "ENT", "description": "Closed by local factor.", "reasons": ["Periorbital swelling", "Dressing or bandage", "Other local factor"]},
     "options": [o(4, "Spontaneous", 4, "E4", "Open before stimulus."), o(3, "To sound", 3, "E3", "After spoken or shouted request."),
                 o(2, "To pressure", 2, "E2", "After fingertip stimulus."), o(1, "None", 1, "E1", "No opening at any time, no interfering factor.")]},
    {"id": "v", "type": "single", "label": "Verbal response (V)", "short": "V",
     "notTestable": {"label": "Non-testable", "code": "VNT", "description": "Factor interfering with communication.", "reasons": ["Endotracheal tube or tracheostomy", "Other factor interfering with communication"]},
     "options": [o(5, "Orientated", 5, "V5", "Correctly gives name, place and date."), o(4, "Confused", 4, "V4", "Not orientated but communicates coherently."),
                 o(3, "Words", 3, "V3", "Intelligible single words."), o(2, "Sounds", 2, "V2", "Only moans or groans."), o(1, "None", 1, "V1", "No audible response, no interfering factor.")]},
    {"id": "m", "type": "single", "label": "Best motor response (M)", "short": "M", "help": "Record the best response; test the arms.",
     "notTestable": {"label": "Non-testable", "code": "MNT", "description": "Paralysed or other limiting factor.", "reasons": ["Paralysed", "Other limiting factor"]},
     "options": [o(6, "Obeys commands", 6, "M6", "Obeys a two-part request."), o(5, "Localising", 5, "M5", "Brings hand above clavicle to stimulus on head or neck."),
                 o(4, "Normal flexion", 4, "M4", "Bends arm at elbow rapidly; features not predominantly abnormal."), o(3, "Abnormal flexion", 3, "M3", "Bends arm at elbow; features clearly predominantly abnormal."),
                 o(2, "Extension", 2, "M2", "Extends arm at elbow."), o(1, "None", 1, "M1", "No movement in arms or legs, no interfering factor.")]}],
  calculationMethod={"type": "sum", "notTestablePolicy": "block", "range": {"min": 3, "max": 15}, "formula": "{e_code} + {v_code} + {m_code}", "display": "{total}",
                     "share": "GCS {e_code} {v_code} {m_code} = {total}"},
  notTestable={"label": "No total: component non-testable", "summary": "At least one component is non-testable, so no total is reported. The components are the result.",
               "detail": "Communicate the components with the reason for NT (e.g. E3 VNT M6, intubated). Assigning 1 to a non-testable component would make the patient appear worse than observed.",
               "display": "No total", "share": "GCS {e_code} {v_code} {m_code} (no total: component non-testable)"},
  interpretationRules=[{"when": "total == 15", "state": "none"}, {"when": "total >= 13", "state": "mild"}, {"when": "total >= 9", "state": "moderate"}, {"state": "severe"}],
  resultStates=[
    {"id": "severe", "tone": "high", "min": 3, "max": 8, "label": "Severe impairment", "range": "3–8", "summary": "Severe impairment of consciousness (GCS 3–8).",
     "detail": "Correlate with airway, respiratory, neurological and systemic assessment, according to the clinical situation and local protocol."},
    {"id": "moderate", "tone": "moderate", "min": 9, "max": 12, "label": "Moderate impairment", "range": "9–12", "summary": "Moderate impairment of consciousness (GCS 9–12).",
     "detail": "Assess the cause, trajectory and associated findings according to the clinical situation and local protocol."},
    {"id": "mild", "tone": "low", "min": 13, "max": 14, "label": "Mild impairment", "range": "13–14", "summary": "Mild impairment of consciousness (within the TBI mild category, 13–15).", "detail": "Reassess serially; small changes can matter."},
    {"id": "none", "tone": "favorable", "min": 15, "max": 15, "label": "No impairment measured", "range": "15", "summary": "No impairment of consciousness measured by GCS at this assessment.",
     "detail": "A GCS of 15 does not exclude intracranial pathology, focal deficits or later deterioration."}],
  clinicalContext=[
    {"text": "Describes level of consciousness from the best eye, verbal and motor responses at one point in time.", "importance": "major"},
    {"text": "Most informative as a trend: serial assessments with the same structured method show improvement or deterioration."},
    {"text": "Provides a shared language for handover and an input to other scores (e.g. WFNS, GCS-Pupils)."}],
  clinicalInsights=[
    {"text": "Report E, V and M with the total; the same total can arise from different combinations of responses."},
    {"when": "m <= 3", "importance": "major", "text": "The motor response is the component most closely related to outcome. Abnormal flexion, extension or no response warrants close attention to the trajectory."},
    {"when": "total <= 8 && m >= 5", "text": "Low total with a relatively preserved motor response: the components describe this patient better than the total."},
    {"when": "total == 15", "text": "A GCS of 15 does not exclude intracranial pathology, focal deficits or later deterioration; correlate with history, focal examination and other findings."},
    {"on": "notTestable", "when": "v_nt", "importance": "major", "text": "Verbal response is non-testable. The FOUR score has no verbal component and adds brainstem reflexes and respiration."},
    {"on": "notTestable", "when": "e_nt", "text": "Eye opening is non-testable. Verbal and motor responses still describe responsiveness."}],
  limitations=[
    {"importance": "major", "text": "Does not assess pupils, brainstem reflexes or lateralising signs."},
    {"importance": "major", "text": "Verbal response cannot be assessed when intubated or with severe aphasia."},
    "The 3–8 / 9–12 / 13–15 categories derive from traumatic brain injury.",
    "Agreement between raters is lower in the intermediate range and without the structured approach.",
    {"on": "always", "when": "nt_count > 0", "importance": "major", "text": "{nt_count} component(s) non-testable: no total can be reported.", "guideText": "When any component is non-testable, no total can be reported."}],
  confounders=[
    {"factor": "Sedative or paralysing drugs", "effect": "Can lower E, V and M independently of brain injury.", "importance": "major"},
    {"factor": "Intubation or tracheostomy", "effect": "Prevents verbal assessment; record V as NT.", "importance": "major"},
    {"factor": "Intoxication", "effect": "Alcohol or drugs can depress responses."},
    {"factor": "Hypoxia, hypotension or hypoglycaemia", "effect": "Reversible physiological causes can lower the score."},
    {"factor": "Post-ictal state", "effect": "Responses can be temporarily depressed after a seizure."},
    {"factor": "Hypothermia", "effect": "Can depress responsiveness."},
    {"factor": "Periorbital swelling", "effect": "Can prevent eye opening; record E as NT."},
    {"factor": "Language barrier, deafness or aphasia", "effect": "Can lower V or responses to command without reduced consciousness."},
    {"factor": "Spinal cord or limb injury", "effect": "Can limit motor response; record M as NT if paralysed."}],
  whatItDoesNotTellYou=["The cause of impaired consciousness.", "Whether a focal, brainstem or structural lesion is present.", "The need for any specific intervention.", "An individual patient's prognosis on its own."],
  commonErrors=["Scoring 1 for a component that could not be tested (record NT).", "Reporting a total when any component is NT.", "Recording the worst instead of the best motor response.",
                "Testing motor response in the legs (spinal reflexes can mislead).", "Applying physical pressure before checking the response to sound.", "Scoring 'localising' when the hand does not cross the clavicle."],
  relatedScores=[{"id": "gcsp", "relation": "GCS with pupil reactivity"}, {"id": "four", "relation": "No verbal component"}, {"id": "wfns", "relation": "SAH grade using GCS"}],
  guideSections={"what": "A scale describing level of consciousness from three components: eye opening (1–4), verbal response (1–5) and best motor response (1–6). The sum ranges 3–15 when all components are testable.",
    "whenToUse": "Initial and serial assessment of consciousness, handover, trauma triage, and as an input to other scores (WFNS, ICH Score, GCS-Pupils).",
    "howToPerform": "Use the structured approach. Check for factors that interfere with each response (e.g. intubation, swelling, paralysis). Observe for spontaneous behaviour. Stimulate in sequence: spoken or shouted request, then physical pressure (fingertip, trapezius or supraorbital). Rate the best response for each component. Record NT for a component that cannot be tested. Report E, V and M, and the total only when all three are testable.",
    "clinicalContext": "Trends matter more than a single value. Always communicate the components, which carry more information than the total."},
  sources=[{"citation": "Teasdale G, Jennett B. Assessment of coma and impaired consciousness. A practical scale. Lancet. 1974;2(7872):81-84.", "doi": "10.1016/S0140-6736(74)91639-0"},
           {"citation": "Teasdale G, Maas A, Lecky F, Manley G, Stocchetti N, Murray G. The Glasgow Coma Scale at 40 years: standing the test of time. Lancet Neurol. 2014;13(8):844-854.", "doi": "10.1016/S1474-4422(14)70120-6"},
           {"citation": "The Glasgow structured approach to assessment of the Glasgow Coma Scale. Royal College of Physicians and Surgeons of Glasgow.", "url": "https://www.glasgowcomascale.org"}],
  licensing={"status": "Criteria with attribution", "note": "The official GCS aid, charts, videos and translations (glasgowcomascale.org) are not reproduced."}))

# =====================================================================  NIHSS
# Verified: NINDS NIH Stroke Scale (updated Feb 2024) — item definitions, UN rules (5a/5b/6a/6b/7/10 only;
# item 11 never untestable), coma rules (item 8 = 2, item 9 = 3), item 9 = 3 only if mute and follows no
# one-step commands, ataxia absent in a paralysed patient.
UN_LIMB = {"label": "Untestable (UN)", "code": "UN", "requireReason": True, "reasons": ["Amputation", "Joint fusion"],
           "description": "Only for amputation or joint fusion; record the reason."}
def motor(id_, label, short, secs, joint, arm):
    pos = "90° (sitting) or 45° (supine)" if arm else "30° (always supine)"
    return {"id": id_, "type": "single", "label": label, "short": short,
            "help": f"Position the {'arm' if arm else 'leg'} at {pos}. Drift is scored if it falls before {secs} seconds. Begin with the non-paretic limb. UN only for amputation or joint fusion at the {joint}.",
            "notTestable": UN_LIMB,
            "options": [o(0, "No drift", 0, detail=f"Holds position for the full {secs} seconds."),
                        o(1, "Drift", 1, detail=f"Drifts down before {secs} seconds; does not hit the bed or other support."),
                        o(2, "Some effort against gravity", 2, detail="Cannot get to or maintain position; falls to bed, but some effort against gravity."),
                        o(3, "No effort against gravity", 3, detail="Limb falls."), o(4, "No movement", 4)]}
scores.append(base(
  id="nihss", name="NIH Stroke Scale", abbreviation="NIHSS", aliases=["stroke scale", "national institutes of health", "nih"],
  category="stroke", subcategory="Stroke deficit quantification", specialties=["Stroke", "Neurology", "Emergency Medicine"],
  version={"label": "NINDS NIH Stroke Scale (2024 update), 15 items", "detail": "Items 1a–11 as defined by NINDS (updated February 2024). Total 0–42. The language stimulus pictures, naming sheet and reading lists are not reproduced. Optional add-on items (e.g. distal motor function) are not part of the scale total and are not included."},
  purpose="Standardised quantification of selected neurological deficits after stroke, for assessment, monitoring and communication.",
  intendedPopulation="Adults with suspected or confirmed acute stroke, examined by a clinician trained in the NIHSS.",
  resultPresentation={"type": "deficit", "typeLabel": "Measured stroke deficit", "meter": False},
  calculatorNotice={"tone": "warning", "title": "Not a complete neurological examination",
    "message": "NIHSS scores 15 selected items. Disabling deficits such as gait or truncal ataxia, vertigo, dysphagia, isolated hand weakness and cognitive impairment are not captured. A low score, including 0, does not exclude stroke."},
  components=[
    {"id": "consciousness", "label": "Level of consciousness", "inputs": ["item_1a", "item_1b", "item_1c"]},
    {"id": "eye_movement", "label": "Best gaze", "inputs": ["item_2"]},
    {"id": "visual_fields", "label": "Visual", "inputs": ["item_3"]},
    {"id": "face", "label": "Facial palsy", "inputs": ["item_4"]},
    {"id": "arms", "label": "Motor arm", "inputs": ["item_5a", "item_5b"]},
    {"id": "legs", "label": "Motor leg", "inputs": ["item_6a", "item_6b"]},
    {"id": "coordination", "label": "Limb ataxia", "inputs": ["item_7"]},
    {"id": "sensation", "label": "Sensory", "inputs": ["item_8"]},
    {"id": "speech_language", "label": "Best language", "inputs": ["item_9"]},
    {"id": "articulation", "label": "Dysarthria", "inputs": ["item_10"]},
    {"id": "attention", "label": "Extinction and inattention", "inputs": ["item_11"]}],
  inputDefinitions=[
    {"id": "item_1a", "type": "single", "label": "1a. Level of consciousness", "short": "1a LOC",
     "help": "A response must be chosen even if evaluation is limited (e.g. endotracheal tube, language barrier). Score 3 only if no movement other than reflexive posturing to noxious stimulation.",
     "options": [o(0, "Alert; keenly responsive", 0), o(1, "Not alert; arousable by minor stimulation", 1, detail="To obey, answer or respond."),
                 o(2, "Not alert; requires repeated stimulation", 2, detail="Or obtunded, requiring strong or painful stimulation to make movements (not stereotyped)."),
                 o(3, "Reflex responses only, or totally unresponsive", 3, detail="Reflex motor or autonomic effects only, or flaccid and areflexic.")]},
    {"id": "item_1b", "type": "single", "label": "1b. LOC questions", "short": "1b Questions",
     "help": "Ask the month and the patient's age; grade only the initial answer, with no partial credit. Aphasic or stuporous patients who do not comprehend score 2. Patients unable to speak for reasons other than aphasia (e.g. intubation) score 1.",
     "options": [o(0, "Answers both questions correctly", 0), o(1, "Answers one question correctly", 1), o(2, "Answers neither question correctly", 2)]},
    {"id": "item_1c", "type": "single", "label": "1c. LOC commands", "short": "1c Commands",
     "help": "Open and close the eyes; grip and release the non-paretic hand. Credit an unequivocal attempt limited by weakness. Pantomime if no response. Only the first attempt is scored.",
     "options": [o(0, "Performs both tasks correctly", 0), o(1, "Performs one task correctly", 1), o(2, "Performs neither task correctly", 2)]},
    {"id": "item_2", "type": "single", "label": "2. Best gaze", "short": "2 Gaze",
     "help": "Horizontal eye movements only; voluntary or oculocephalic, no caloric testing. Conjugate deviation overcome by voluntary or reflexive activity, or an isolated CN III, IV or VI paresis, scores 1.",
     "options": [o(0, "Normal", 0), o(1, "Partial gaze palsy", 1, detail="Gaze abnormal in one or both eyes; no forced deviation or total gaze paresis."),
                 o(2, "Forced deviation or total gaze paresis", 2, detail="Not overcome by the oculocephalic manoeuvre.")]},
    {"id": "item_3", "type": "single", "label": "3. Visual", "short": "3 Visual",
     "help": "Confrontation testing of upper and lower quadrants. Score 1 only for clear-cut asymmetry, including quadrantanopia. Blind from any cause scores 3.",
     "options": [o(0, "No visual loss", 0), o(1, "Partial hemianopia", 1), o(2, "Complete hemianopia", 2), o(3, "Bilateral hemianopia", 3, detail="Blind, including cortical blindness.")]},
    {"id": "item_4", "type": "single", "label": "4. Facial palsy", "short": "4 Face",
     "options": [o(0, "Normal symmetrical movements", 0), o(1, "Minor paralysis", 1, detail="Flattened nasolabial fold, asymmetry on smiling."),
                 o(2, "Partial paralysis", 2, detail="Total or near-total paralysis of the lower face."), o(3, "Complete paralysis of one or both sides", 3, detail="No facial movement in upper and lower face.")]},
    motor("item_5a", "5a. Motor arm, left", "5a Left arm", 10, "shoulder", True),
    motor("item_5b", "5b. Motor arm, right", "5b Right arm", 10, "shoulder", True),
    motor("item_6a", "6a. Motor leg, left", "6a Left leg", 5, "hip", False),
    motor("item_6b", "6b. Motor leg, right", "6b Right leg", 5, "hip", False),
    {"id": "item_7", "type": "single", "label": "7. Limb ataxia", "short": "7 Ataxia",
     "help": "Finger-nose-finger and heel-shin on both sides, eyes open. Scored only if out of proportion to weakness. Ataxia is absent in a patient who cannot understand or is paralysed.",
     "notTestable": UN_LIMB, "options": [o(0, "Absent", 0), o(1, "Present in one limb", 1), o(2, "Present in two limbs", 2)]},
    {"id": "item_8", "type": "single", "label": "8. Sensory", "short": "8 Sensory",
     "help": "Pinprick, or withdrawal in the obtunded or aphasic patient. Only stroke-related loss counts. Bilateral loss from brainstem stroke scores 2; unresponsive and quadriplegic scores 2; coma (1a = 3) scores 2.",
     "options": [o(0, "Normal; no sensory loss", 0), o(1, "Mild-to-moderate sensory loss", 1, detail="Pinprick less sharp or dull, or loss of superficial pain but aware of being touched."),
                 o(2, "Severe or total sensory loss", 2, detail="Not aware of being touched in face, arm and leg.")]},
    {"id": "item_9", "type": "single", "label": "9. Best language", "short": "9 Language",
     "help": "Uses the NINDS picture, naming and reading materials (not reproduced here). Coma (1a = 3) scores 3. Score 3 only if the patient is mute and follows no one-step commands.",
     "options": [o(0, "No aphasia; normal", 0), o(1, "Mild-to-moderate aphasia", 1, detail="Some loss of fluency or comprehension; examiner can still identify the material from the response."),
                 o(2, "Severe aphasia", 2, detail="Fragmentary expression; examiner cannot identify the material from the response."),
                 o(3, "Mute, global aphasia", 3, detail="No usable speech or auditory comprehension.")]},
    {"id": "item_10", "type": "single", "label": "10. Dysarthria", "short": "10 Dysarthria",
     "help": "Obtain an adequate speech sample (NINDS word list, not reproduced). UN only if intubated or another physical barrier to producing speech.",
     "notTestable": {"label": "Untestable (UN)", "code": "UN", "requireReason": True, "reasons": ["Intubated", "Other physical barrier to speech"], "description": "Only if intubated or another physical barrier to speech; record the reason."},
     "options": [o(0, "Normal", 0), o(1, "Mild-to-moderate dysarthria", 1, detail="Slurs at least some words; at worst understood with some difficulty."),
                 o(2, "Severe dysarthria", 2, detail="Unintelligible out of proportion to any dysphasia, or mute/anarthric.")]},
    {"id": "item_11", "type": "single", "label": "11. Extinction and inattention", "short": "11 Extinction",
     "help": "Never untestable. Severe visual loss with normal cutaneous stimuli scores normal; an aphasic patient who attends to both sides scores normal.",
     "options": [o(0, "No abnormality", 0), o(1, "Inattention or extinction in one modality", 1, detail="Visual, tactile, auditory, spatial or personal."),
                 o(2, "Profound hemi-inattention or extinction to more than one modality", 2, detail="Does not recognise own hand, or orients to only one side of space.")]}],
  calculationMethod={"type": "sum", "notTestablePolicy": "exclude", "range": {"min": 0, "max": 42}, "display": "{total}", "share": "NIHSS {total}"},
  consistencyRules=[
    {"when": "item_1a == 3 && item_8 != 2", "severity": "warning", "inputs": ["item_8"], "message": "Item 1a = 3 (coma): NINDS instructions automatically score item 8 (sensory) as 2."},
    {"when": "item_1a == 3 && item_9 != 3", "severity": "warning", "inputs": ["item_9"], "message": "Item 1a = 3 (coma): NINDS instructions automatically score item 9 (language) as 3."},
    {"when": "item_9 == 3 && item_1c <= 1", "severity": "warning", "inputs": ["item_9", "item_1c"], "message": "Item 9 = 3 is used only if the patient is mute and follows no one-step commands, but item 1c records at least one command performed."},
    {"when": "item_5a == 4 && item_5b == 4 && item_6a == 4 && item_6b == 4 && item_7 >= 1", "severity": "warning", "inputs": ["item_7"], "message": "No movement in all four limbs: NINDS instructions score ataxia as absent in a paralysed patient."}],
  interpretationRules=[{"when": "total == 0 && nt_count == 0", "state": "zero"}, {"state": "scored"}],
  resultStates=[
    {"id": "zero", "tone": "favorable", "label": "No measurable deficit", "range": "0", "summary": "No measurable deficit on the NIHSS at the time of assessment.",
     "detail": "This does not exclude stroke: deficits outside the scale's 15 items are not captured."},
    {"id": "scored", "tone": "informational", "label": "NIHSS {total}", "range": "1–42", "summary": "Higher scores indicate more measured neurological deficit.",
     "detail": "NINDS defines no severity categories, and bands used in studies differ. Interpret the item profile and trend with imaging and the full examination."}],
  clinicalContext=[
    {"text": "Quantifies 15 selected neurological deficits after stroke.", "importance": "major"},
    {"text": "Used for serial monitoring; change between assessments by trained examiners is often more informative than one value."},
    {"text": "Provides a common language between emergency, stroke and research teams."}],
  clinicalInsights=[
    {"text": "Report the total with the item breakdown; the same total can reflect very different deficits."},
    {"when": "total == 0 && nt_count == 0", "importance": "major", "text": "Deficits outside the scale, such as gait or truncal ataxia, vertigo, nystagmus or dysphagia, can be present with a score of 0."},
    {"when": "item_9 >= 1 || item_1b >= 1 || item_1c >= 1", "text": "Language-dependent items contribute to this total. For similar lesion volume, left-hemisphere strokes tend to score higher than right-hemisphere strokes."},
    {"when": "item_11 >= 1", "text": "Inattention or extinction is present. Neglect may be under-weighted relative to its functional impact."},
    {"when": "total >= 1 && total <= 4", "text": "Low scores can accompany disabling deficits, particularly in posterior circulation stroke."}],
  limitations=[
    {"importance": "major", "text": "Not a complete neurological examination: gait and truncal ataxia, vertigo, nystagmus, dysphagia, isolated distal hand weakness and cognition are not scored."},
    {"importance": "major", "text": "Under-represents posterior circulation stroke; a score of 0 does not exclude stroke."},
    "Language-weighted: right-hemisphere strokes may score lower than left-hemisphere strokes of similar size.",
    "The total does not show which deficits are disabling for this patient.",
    "Reliability depends on trained, certified examiners following the item rules.",
    {"on": "always", "when": "nt_count > 0", "importance": "major", "text": "{nt_count} item(s) untestable and contributing no points: the total may underestimate the deficit.", "guideText": "Untestable (UN) items contribute no points, so the total may underestimate the deficit."}],
  confounders=[
    {"factor": "Sedation or intubation", "effect": "Limits consciousness, language and dysarthria items.", "importance": "major"},
    {"factor": "Pre-existing deficits", "effect": "Old deficits are scored unless documented separately."},
    {"factor": "Aphasia", "effect": "Affects comprehension of commands and questions (items 1b, 1c)."},
    {"factor": "Visual or hearing impairment", "effect": "Can affect visual field, command and language items."},
    {"factor": "Amputation or joint fusion", "effect": "Motor or ataxia items recorded as UN."},
    {"factor": "Seizure or post-ictal state", "effect": "Can produce transient deficits."},
    {"factor": "Hypoglycaemia and other stroke mimics", "effect": "Can produce scorable deficits without stroke."}],
  whatItDoesNotTellYou=["Whether the deficit is caused by stroke or a mimic.", "Stroke mechanism, vessel occlusion or infarct size.", "Eligibility for any specific treatment.",
                        "The full neurological picture, including posterior circulation signs and cognition.", "Functional outcome (see mRS)."],
  commonErrors=["Coaching the patient, or scoring a later rather than the first attempt (1b, 1c).", "Going back to change earlier item scores.", "Scoring ataxia that is explained by weakness or paralysis.",
                "Using UN for reasons the instrument does not allow (only amputation or joint fusion for limbs; intubation or physical barrier for dysarthria).", "Scoring a pre-existing deficit as new without documenting it."],
  relatedScores=[{"id": "mrs", "relation": "Functional outcome"}, {"id": "aspects", "relation": "Early ischaemic change on CT"}, {"id": "gcs", "relation": "Level of consciousness"}],
  guideSections={"what": "A 15-item examination that quantifies selected neurological deficits after stroke. Totals range 0–42.",
    "whenToUse": "Initial assessment of suspected stroke, serial monitoring for change, communication between teams, and research outcomes.",
    "howToPerform": "Administer the items in the listed order and record each score immediately. Do not go back and change scores. Score what the patient does, not what you think they can do. Do not coach unless an item allows it. Use UN only where the instrument allows it, and record the reason.",
    "clinicalContext": "The NIHSS supports, but does not replace, the full neurological examination and imaging. Treatment decisions combine it with timing, imaging, patient factors and local protocol."},
  sources=[{"citation": "National Institute of Neurological Disorders and Stroke. NIH Stroke Scale (updated February 2024).", "url": "https://www.ninds.nih.gov/sites/default/files/documents/NIH-Stroke-Scale_updatedFeb2024_508.pdf"},
           {"citation": "Brott T, Adams HP Jr, Olinger CP, et al. Measurements of acute cerebral infarction: a clinical examination scale. Stroke. 1989;20(7):864-870.", "doi": "10.1161/01.STR.20.7.864"},
           {"citation": "Martin-Schild S, Albright KC, Tanksley J, et al. Zero on the NIHSS does not equal the absence of stroke. Ann Emerg Med. 2011;57(1):42-45.", "doi": "10.1016/j.annemergmed.2010.06.564"},
           {"citation": "Woo D, et al. Does the National Institutes of Health Stroke Scale favor left hemisphere strokes? NINDS t-PA Stroke Study Group. Stroke. 1999."}],
  licensing={"status": "Public domain (NINDS)", "note": "The NIHSS is public domain. The picture, naming and reading stimulus pages (marked © Apex Innovations in the NINDS document) and official training/certification materials are not reproduced."}))

# =====================================================================  mRS
# Verified: standard van Swieten 1988 (UK-TIA) wording with grade 6 'Dead', as reproduced in trial protocols.
scores.append(base(
  id="mrs", name="Modified Rankin Scale", abbreviation="mRS", aliases=["rankin", "disability", "functional outcome", "dependence"],
  category="functional", subcategory="Global disability and dependence", specialties=["Stroke", "Neurology", "Neurosurgery", "Rehabilitation"],
  version={"label": "Modified Rankin Scale 0–6 (van Swieten et al. 1988)", "detail": "Standard UK-TIA wording with grade 6 (dead), as used in stroke trials. Variant wordings (e.g. adding 'neurological' to each grade) are not combined. Structured interview instruments are not reproduced."},
  purpose="A global measure of disability and dependence in daily activities. It describes functional status, not the severity of a neurological deficit.",
  intendedPopulation="Adults after stroke and other neurological conditions, typically at baseline (pre-morbid), discharge and follow-up.",
  resultPresentation={"type": "functional-status", "typeLabel": "Functional status", "meter": True},
  calculatorNotice={"tone": "info", "title": "Functional outcome scale",
    "message": "mRS grades disability and dependence in daily life. It is not a neurological severity score, and it reflects function from all causes, not only the neurological condition."},
  components=[{"id": "function", "label": "Functional level", "inputs": ["grade"]}],
  inputDefinitions=[{"id": "grade", "type": "single", "label": "Functional level", "short": "mRS",
    "help": "Choose the single grade that best describes the person's current function across all activities. A structured interview improves reliability.",
    "options": [o(0, "No symptoms at all", 0, "0"),
                o(1, "No significant disability despite symptoms", 1, "1", "Able to carry out all usual duties and activities."),
                o(2, "Slight disability", 2, "2", "Unable to carry out all previous activities, but able to look after own affairs without assistance."),
                o(3, "Moderate disability", 3, "3", "Requiring some help, but able to walk without assistance."),
                o(4, "Moderately severe disability", 4, "4", "Unable to walk without assistance and unable to attend to own bodily needs without assistance."),
                o(5, "Severe disability", 5, "5", "Bedridden, incontinent and requiring constant nursing care and attention."),
                o(6, "Dead", 6, "6")]}],
  calculationMethod={"type": "select", "input": "grade", "range": {"min": 0, "max": 6}, "display": "mRS {total}", "share": "mRS {total}"},
  interpretationRules=[{"when": "total == %d" % i, "state": "g%d" % i} for i in range(7)],
  resultStates=[
    {"id": "g0", "tone": "favorable", "min": 0, "max": 0, "label": "No symptoms", "range": "0", "summary": "Functional status: no symptoms at all at this assessment.", "detail": "Describes function at this timepoint, not the underlying condition."},
    {"id": "g1", "tone": "informational", "min": 1, "max": 1, "label": "No significant disability", "range": "1", "summary": "Functional status: symptoms present; able to carry out all usual duties and activities."},
    {"id": "g2", "tone": "informational", "min": 2, "max": 2, "label": "Slight disability", "range": "2", "summary": "Functional status: independent in own affairs, but unable to carry out all previous activities."},
    {"id": "g3", "tone": "informational", "min": 3, "max": 3, "label": "Moderate disability", "range": "3", "summary": "Functional status: requires some help; walks without assistance."},
    {"id": "g4", "tone": "informational", "min": 4, "max": 4, "label": "Moderately severe disability", "range": "4", "summary": "Functional status: cannot walk or attend to bodily needs without assistance."},
    {"id": "g5", "tone": "informational", "min": 5, "max": 5, "label": "Severe disability", "range": "5", "summary": "Functional status: bedridden, incontinent, requires constant nursing care."},
    {"id": "g6", "tone": "informational", "min": 6, "max": 6, "label": "Dead", "range": "6", "summary": "Outcome: dead."}],
  clinicalContext=[
    {"text": "Describes global disability and dependence in daily activities, from all causes.", "importance": "major"},
    {"text": "Used to document pre-morbid function, discharge status and follow-up outcomes."},
    {"text": "A common outcome in stroke trials, analysed either across all grades or split at a defined cut-off."}],
  clinicalInsights=[
    {"text": "Record the timepoint and source (pre-morbid, discharge, follow-up; patient, carer or records). Pre-morbid mRS changes how later grades are read."},
    {"text": "'Favourable outcome' cut-offs differ between studies (0–1, 0–2, or full ordinal shift). State the definition when comparing results."},
    {"when": "total >= 1 && total <= 3", "text": "Grades 1–3 have the most inter-rater disagreement; a structured interview improves reliability."},
    {"when": "total == 0", "text": "Grade 0 describes function at this assessment; it does not describe the underlying neurological condition."}],
  limitations=[
    {"importance": "major", "text": "Measures global disability, not neurological severity or a specific deficit."},
    "Moderate inter-rater reliability without a structured assessment.",
    "Weighted toward mobility and self-care; cognition, mood and communication may be under-represented.",
    "Reflects disability from all causes, including non-neurological comorbidity."],
  confounders=[
    {"factor": "Pre-morbid disability", "effect": "Existing dependence is included unless pre-morbid mRS is recorded.", "importance": "major"},
    {"factor": "Non-neurological comorbidity", "effect": "Cardiac, respiratory or orthopaedic limits raise the grade."},
    {"factor": "Proxy versus patient report", "effect": "Different informants may give different grades."},
    {"factor": "Timing of assessment", "effect": "Function changes during recovery; grades are timepoint-specific."}],
  whatItDoesNotTellYou=["The neurological deficit or its severity (see NIHSS).", "Which impairment causes the disability.", "Quality of life or rehabilitation potential."],
  commonErrors=["Treating mRS as a measure of neurological severity.", "Not recording the pre-morbid mRS.", "Grading from mobility alone.", "Assigning 0 when minor symptoms persist (grade 1)."],
  relatedScores=[{"id": "nihss", "relation": "Neurological deficit"}, {"id": "gose", "relation": "Outcome after brain injury"}],
  guideSections={"what": "A 7-grade ordinal scale from 0 (no symptoms) to 6 (dead) describing global disability and dependence.",
    "whenToUse": "Documenting pre-morbid function, discharge status and follow-up outcomes after stroke and other neurological conditions; trial outcomes.",
    "howToPerform": "Establish the person's usual activities and current level of help needed. Choose the single grade that best fits overall function. Record the timepoint and information source. Structured interviews improve consistency.",
    "clinicalContext": "A functional outcome measure, used alongside measures of neurological deficit (e.g. NIHSS) rather than in place of them."},
  sources=[{"citation": "van Swieten JC, Koudstaal PJ, Visser MC, Schouten HJ, van Gijn J. Interobserver agreement for the assessment of handicap in stroke patients. Stroke. 1988;19(5):604-607.", "doi": "10.1161/01.STR.19.5.604"},
           {"citation": "Rankin J. Cerebral vascular accidents in patients over the age of 60. II. Prognosis. Scott Med J. 1957;2(5):200-215."}],
  licensing={"status": "Widely published grade definitions", "note": "Structured mRS interview instruments (e.g. mRS-9Q, Rankin Focused Assessment) have their own terms and are not reproduced."}))

# =====================================================================  SINS
# Verified: Fisher et al. Spine 2010 (SOSG); Fourney et al. JCO 2011; AJR 2014 reliability study (worked examples).
scores.append(base(
  id="sins", name="Spinal Instability Neoplastic Score", abbreviation="SINS", aliases=["spinal instability", "metastasis", "neoplastic", "sosg", "spine tumour"],
  category="spine", subcategory="Neoplastic spinal instability", specialties=["Neurosurgery", "Spine Surgery", "Radiation Oncology", "Radiology", "Oncology"],
  version={"label": "SOSG SINS (Fisher et al. 2010)", "detail": "Six components, total 0–18. Categories: stable 0–6, indeterminate (possibly impending) instability 7–12, unstable 13–18."},
  purpose="Classification of tumour-related spinal instability, to standardise communication and support referral for specialist assessment.",
  intendedPopulation="Adults with primary or metastatic neoplastic involvement of the spine, scored per affected level using clinical history and CT/MRI.",
  resultPresentation={"type": "stability", "typeLabel": "Stability category", "meter": True},
  calculatorNotice={"tone": "info", "title": "Assessment tool, not a surgical decision",
    "message": "SINS classifies mechanical stability only. Treatment decisions also depend on neurological status, tumour histology, systemic disease, prognosis and patient choice, in multidisciplinary discussion."},
  components=[
    {"id": "spinal_location", "label": "Location", "inputs": ["location"]},
    {"id": "mechanical_pain", "label": "Pain", "inputs": ["pain"]},
    {"id": "bone_quality", "label": "Bone lesion", "inputs": ["lesion"]},
    {"id": "radiographic_alignment", "label": "Radiographic spinal alignment", "inputs": ["alignment"]},
    {"id": "body_collapse", "label": "Vertebral body collapse", "inputs": ["collapse"]},
    {"id": "posterior_involvement", "label": "Posterolateral involvement", "inputs": ["posterolateral"]}],
  inputDefinitions=[
    {"id": "location", "type": "single", "label": "Location", "short": "Location",
     "options": [o(3, "Junctional", 3, detail="Occiput–C2, C7–T2, T11–L1, L5–S1"), o(2, "Mobile spine", 2, detail="C3–C6, L2–L4"), o(1, "Semi-rigid", 1, detail="T3–T10"), o(0, "Rigid", 0, detail="S2–S5")]},
    {"id": "pain", "type": "single", "label": "Pain", "short": "Pain", "help": "Mechanical pain: relief with recumbency and/or pain with movement or loading of the spine.",
     "options": [o(3, "Yes (mechanical pain)", 3), o(1, "No (occasional pain but not mechanical)", 1), o(0, "Pain-free lesion", 0)]},
    {"id": "lesion", "type": "single", "label": "Bone lesion", "short": "Bone lesion",
     "options": [o(2, "Lytic", 2), o(1, "Mixed (lytic/blastic)", 1), o(0, "Blastic", 0)]},
    {"id": "alignment", "type": "single", "label": "Radiographic spinal alignment", "short": "Alignment",
     "options": [o(4, "Subluxation or translation present", 4), o(2, "De novo deformity (kyphosis or scoliosis)", 2), o(0, "Normal alignment", 0)]},
    {"id": "collapse", "type": "single", "label": "Vertebral body collapse", "short": "Collapse",
     "options": [o(3, "More than 50% collapse", 3), o(2, "Less than 50% collapse", 2), o(1, "No collapse with more than 50% of the body involved", 1), o(0, "None of the above", 0)]},
    {"id": "posterolateral", "type": "single", "label": "Posterolateral involvement of spinal elements", "short": "Posterolateral",
     "help": "Facet, pedicle or costovertebral joint fracture, or replacement with tumour.",
     "options": [o(3, "Bilateral", 3), o(1, "Unilateral", 1), o(0, "None of the above", 0)]}],
  calculationMethod={"type": "sum", "range": {"min": 0, "max": 18}, "display": "{total}", "share": "SINS {total}"},
  interpretationRules=[{"when": "total <= 6", "state": "stable"}, {"when": "total <= 12", "state": "potential"}, {"state": "unstable"}],
  resultStates=[
    {"id": "stable", "tone": "favorable", "min": 0, "max": 6, "label": "Stable", "range": "0–6", "summary": "Stability category: stable (0–6) at this assessment.",
     "detail": "Classifies mechanical stability only; neurological status and oncological factors are assessed separately."},
    {"id": "potential", "tone": "moderate", "min": 7, "max": 12, "label": "Potentially unstable", "range": "7–12", "summary": "Stability category: indeterminate, possibly impending instability (7–12).",
     "detail": "The SINS authors considered scores of 7–18 to warrant surgical consultation. This is a referral threshold for specialist assessment, not a decision to operate."},
    {"id": "unstable", "tone": "high", "min": 13, "max": 18, "label": "Unstable", "range": "13–18", "summary": "Stability category: unstable (13–18).",
     "detail": "The SINS authors considered scores of 7–18 to warrant surgical consultation. Management depends on neurology, histology, systemic disease, prognosis and patient goals."}],
  clinicalContext=[
    {"text": "Classifies tumour-related mechanical instability at one spinal level.", "importance": "major"},
    {"text": "Provides a shared language between oncology, radiation oncology, radiology and spine surgery."},
    {"text": "In the original publication, scores of 7–18 identified patients considered to warrant surgical consultation."}],
  clinicalInsights=[
    {"text": "SINS addresses mechanical stability only. Neurological compression, tumour histology, systemic disease and prognosis are assessed separately."},
    {"when": "total >= 7 && total <= 12", "importance": "major", "text": "Intermediate scores show the most inter-observer variation. Reviewing the components helps multidisciplinary discussion."},
    {"when": "pain == 3", "text": "Mechanical pain is a clinical finding; confirm it from the history, not imaging alone."},
    {"when": "total <= 6", "text": "A stable category describes mechanical stability only; other indications for specialist input are assessed separately."}],
  limitations=[
    {"importance": "major", "text": "Not a standalone surgical decision tool."},
    {"importance": "major", "text": "Designed for neoplastic disease, not trauma, infection or degenerative disease."},
    "Agreement between raters is lowest in the 7–12 range.",
    "Scored per level; multi-level disease needs level-by-level assessment.",
    "Does not include neurological status, histology or prognosis."],
  confounders=[
    {"factor": "Prior surgery or instrumentation", "effect": "Alters alignment, collapse and posterolateral assessment.", "importance": "major"},
    {"factor": "Osteoporotic fracture at the same level", "effect": "Collapse may not be tumour-related."},
    {"factor": "Imaging modality, quality and position", "effect": "Supine imaging can under-show deformity or translation."},
    {"factor": "Pain from other causes", "effect": "Non-lesional pain can be mislabelled as mechanical."}],
  whatItDoesNotTellYou=["Whether neural compression or deficit is present.", "Tumour radiosensitivity, systemic disease or prognosis.", "Which treatment is appropriate."],
  commonErrors=["Labelling non-mechanical pain as mechanical.", "Using the wrong junctional boundaries (occiput–C2, C7–T2, T11–L1, L5–S1).", "Treating a score of 7 or more as an indication for surgery rather than for consultation.", "Combining several levels into one score."],
  relatedScores=[{"id": "tokuhashi", "relation": "Prognosis in spinal metastasis"}, {"id": "tomita", "relation": "Prognosis in spinal metastasis"}, {"id": "kps", "relation": "Performance status"}],
  guideSections={"what": "A six-component classification of tumour-related spinal instability: location, pain, bone lesion, alignment, vertebral body collapse and posterolateral involvement. Totals range 0–18 in three stability categories.",
    "whenToUse": "Communicating instability between oncology, radiation oncology, radiology and spine surgery, and identifying patients for surgical consultation.",
    "howToPerform": "For the affected level, take the history (mechanical pain) and review CT/MRI for the five imaging components. Score each component and sum. Score each involved level separately.",
    "clinicalContext": "SINS is one input to multidisciplinary decisions, alongside neurological status, oncological factors, systemic disease, prognosis and patient preference."},
  sources=[{"citation": "Fisher CG, DiPaola CP, Ryken TC, et al. A novel classification system for spinal instability in neoplastic disease: an evidence-based approach and expert consensus from the Spine Oncology Study Group. Spine. 2010;35(22):E1221-E1229.", "doi": "10.1097/BRS.0b013e3181e16ae2"},
           {"citation": "Fourney DR, Frangou EM, Ryken TC, et al. Spinal instability neoplastic score: an analysis of reliability and validity from the Spine Oncology Study Group. J Clin Oncol. 2011;29(22):3072-3077.", "doi": "10.1200/JCO.2010.34.3897"}],
  licensing={"status": "Published classification", "note": "Criteria in original wording with attribution. No reproduction restrictions identified."}))

# ====================================================  Input-types demo (non-clinical, design system only)
demo = base(
  id="demo-inputs", name="Input types demonstration", abbreviation="Demo", category="demo", subcategory="Design system", specialties=["None"],
  version={"label": "Non-clinical demo", "detail": "Exercises every engine input type. Not a clinical score."},
  resultPresentation={"type": "severity", "typeLabel": "Demo"}, clinicalContext=[{"text": "Demonstration only."}],
  purpose="Demonstrates every input control and result state. Not for clinical use.", intendedPopulation="Not applicable.",
  components=[{"id": "choices", "label": "Choice inputs", "inputs": ["single", "dropdown", "yes_no", "multi"]},
              {"id": "numbers", "label": "Numeric inputs", "inputs": ["integer", "decimal", "number", "temperature"]}],
  inputDefinitions=[
    {"id": "single", "type": "single", "label": "Single choice", "short": "Single", "notTestable": {"label": "Not testable", "code": "NT"},
     "options": [o("a", "Option A", 0), o("b", "Option B", 1), o("c", "Option C", 2)]},
    {"id": "dropdown", "type": "dropdown", "label": "Dropdown", "short": "Dropdown", "options": [o("x", "First", 0), o("y", "Second", 1), o("z", "Third", 2)]},
    {"id": "yes_no", "type": "yesno", "label": "Yes / No", "short": "Yes/No", "points": {"yes": 1, "no": 0}},
    {"id": "multi", "type": "multi", "label": "Multiple choice", "short": "Multiple", "help": "Select all that apply.", "maxPoints": 3,
     "options": [o("p", "Finding P", 1), o("q", "Finding Q", 1), o("r", "Finding R", 1), {"value": "none", "label": "None of these", "points": 0, "exclusive": True}]},
    {"id": "integer", "type": "integer", "label": "Integer", "short": "Integer", "min": 0, "max": 10, "pointBands": [{"max": 3, "points": 0}, {"min": 4, "max": 7, "points": 1}, {"min": 8, "points": 2}]},
    {"id": "decimal", "type": "decimal", "label": "Decimal (1 dp)", "short": "Decimal", "min": 0, "max": 5, "decimals": 1, "pointBands": [{"max": 2.4, "points": 0}, {"min": 2.5, "points": 1}]},
    {"id": "number", "type": "number", "label": "Number", "short": "Number", "unit": "units", "min": 0, "max": 100, "required": False, "pointBands": [{"max": 49.999, "points": 0}, {"min": 50, "points": 1}]},
    {"id": "temperature", "type": "measurement", "label": "Clinical measurement", "short": "Temperature", "min": 30, "max": 43,
     "units": [{"id": "C", "label": "°C", "factor": 1}, {"id": "F", "label": "°F", "factor": 0.5555555556, "offset": -17.7777777778}],
     "pointBands": [{"max": 37.9, "points": 0}, {"min": 38, "points": 1}]}],
  calculationMethod={"type": "sum", "notTestablePolicy": "block", "range": {"min": 0, "max": 13}, "display": "{total}", "share": "Demo {total}"},
  interpretationRules=[{"when": "total == 0", "state": "s0"}, {"when": "total <= 2", "state": "s1"}, {"when": "total <= 4", "state": "s2"}, {"when": "total <= 6", "state": "s3"},
                       {"when": "total <= 8", "state": "s4"}, {"when": "total <= 10", "state": "s5"}, {"state": "s6"}],
  resultStates=[{"id": "s0", "tone": "favorable", "label": "Normal tone", "summary": "Demo state."}, {"id": "s1", "tone": "low", "label": "Low tone", "summary": "Demo state."},
                {"id": "s2", "tone": "mild", "label": "Mild tone", "summary": "Demo state."}, {"id": "s3", "tone": "moderate", "label": "Moderate tone", "summary": "Demo state."},
                {"id": "s4", "tone": "high", "label": "High tone", "summary": "Demo state."}, {"id": "s5", "tone": "critical", "label": "Critical tone", "summary": "Demo state."},
                {"id": "s6", "tone": "informational", "label": "Informational tone", "summary": "Demo state."}],
  notTestable={"label": "Not interpretable", "summary": "Demo of the not-interpretable state.", "display": "–"},
  clinicalInsights=[{"text": "Demonstration only."}], limitations=["Not a clinical score."], confounders=[], commonErrors=[], whatItDoesNotTellYou=[],
  relatedScores=[], guideSections={"what": "Demo."}, sources=[{"citation": "Not applicable (design-system demonstration)."}])

if __name__ == "__main__":
    import subprocess
    os.makedirs(os.path.join(OUT, "scores"), exist_ok=True); os.makedirs(os.path.join(OUT, "dev"), exist_ok=True)
    for s in scores:
        json.dump(s, open(os.path.join(OUT, "scores", s["id"] + ".json"), "w"), ensure_ascii=False, indent=1)
    json.dump(demo, open(os.path.join(OUT, "dev", "demo-inputs.json"), "w"), ensure_ascii=False, indent=1)
    # mark implemented scores in the catalogue
    cat_path = os.path.join(OUT, "catalog.json"); cat = json.load(open(cat_path))
    ids = {s["id"] for s in scores}
    for c in cat["scores"]:
        c["status"] = "implemented" if c["id"] in ids else "placeholder"
    cat["contentVersion"] = CV
    cat["note"] = "Catalogue. Scores with status 'implemented' have a content file in content/scores/; placeholders contain no scoring criteria."
    json.dump(cat, open(cat_path, "w"), ensure_ascii=False, indent=1)
    print("wrote", ", ".join(sorted(ids)), "+ demo")
