# Insula Neuro Score — Phase 1 score content.
# Authored here for readability; build step writes app/assets/content/scores/<id>.json and manifest.json.
# All descriptors are written in original wording. Official worksheets/figures are not reproduced.
import json, os, datetime

REVIEWED = "2026-10-01"
REVIEW_STATUS = "Content drafted from primary sources; pending independent clinician review before clinical release."
CV = "1.0.0"

def opt(value, label, points, code=None, detail=None, nt=False):
    o = {"value": value, "label": label, "points": points}
    if code: o["code"] = code
    if detail: o["detail"] = detail
    if nt: o["nt"] = True; o["points"] = None
    return o

def yesno(id, label, short, yes_label="Present", no_label="Absent", help=None, points=1):
    d = {"id": id, "type": "choice", "label": label, "short": short,
         "options": [opt("no", no_label, 0), opt("yes", yes_label, points)]}
    if help: d["help"] = help
    return d

GCS_INPUTS = [
    {"id": "e", "type": "choice", "label": "Eye opening", "short": "Eye (E)",
     "help": "Record the best response. Apply a stimulus only if there is no response to the previous level.",
     "options": [
        opt("4", "Spontaneous", 4, "E4", "Eyes open before any stimulus."),
        opt("3", "To sound", 3, "E3", "Opens after spoken or shouted request."),
        opt("2", "To pressure", 2, "E2", "Opens after fingertip, trapezius or supraorbital pressure."),
        opt("1", "None", 1, "E1", "No eye opening; no interfering factor."),
        opt("NT", "Not testable", None, "ENT", "Closed by a local factor (e.g. swelling, dressing).", nt=True)]},
    {"id": "v", "type": "choice", "label": "Verbal response", "short": "Verbal (V)",
     "options": [
        opt("5", "Oriented", 5, "V5", "Correctly gives name, place and date."),
        opt("4", "Confused", 4, "V4", "Not oriented but communicates coherently."),
        opt("3", "Words", 3, "V3", "Intelligible single words."),
        opt("2", "Sounds", 2, "V2", "Only moans or groans."),
        opt("1", "None", 1, "V1", "No audible response; no interfering factor."),
        opt("NT", "Not testable", None, "VNT", "A factor prevents communication (e.g. intubation, tracheostomy).", nt=True)]},
    {"id": "m", "type": "choice", "label": "Best motor response", "short": "Motor (M)",
     "help": "Record the best response from either upper limb.",
     "options": [
        opt("6", "Obeys commands", 6, "M6", "Performs a two-part request."),
        opt("5", "Localising", 5, "M5", "Hand brought above clavicle toward a head or neck stimulus."),
        opt("4", "Normal flexion", 4, "M4", "Rapid flexion at the elbow, not predominantly abnormal."),
        opt("3", "Abnormal flexion", 3, "M3", "Slow, stereotyped flexion of the arm at the elbow."),
        opt("2", "Extension", 2, "M2", "Extension at the elbow."),
        opt("1", "None", 1, "M1", "No movement; no interfering factor."),
        opt("NT", "Not testable", None, "MNT", "Paralysed or another limiting factor.", nt=True)]},
]

GCS_SOURCES = [
    {"citation": "Teasdale G, Jennett B. Assessment of coma and impaired consciousness. A practical scale. Lancet. 1974;2(7872):81-84.", "doi": "10.1016/S0140-6736(74)91639-0"},
    {"citation": "Teasdale G, Maas A, Lecky F, et al. The Glasgow Coma Scale at 40 years: standing the test of time. Lancet Neurol. 2014;13(8):844-854.", "doi": "10.1016/S1474-4422(14)70120-6"},
    {"citation": "Structured approach and terminology: glasgowcomascale.org (Institute of Neurological Sciences, Glasgow).", "url": "https://www.glasgowcomascale.org"},
]
GCS_LICENSE = {"status": "Implemented in original wording with attribution",
    "note": "The scale criteria are widely published. Official GCS teaching aids, charts and translations from glasgowcomascale.org are not reproduced."}

scores = []

# ---------------------------------------------------------------- GCS
scores.append({
 "id": "gcs", "name": "Glasgow Coma Scale", "abbreviation": "GCS", "aliases": ["glasgow", "coma scale", "consciousness"],
 "category": "consciousness", "specialty": ["Neurology", "Neurosurgery", "Neurocritical Care", "Trauma"],
 "version": {"label": "Adult GCS, structured approach", "detail": "Teasdale & Jennett 1974, with the 2014 structured assessment terminology (e.g. 'To pressure', 'Not testable'). Paediatric GCS is a different instrument and is not implemented here."},
 "contentVersion": CV, "lastReviewed": REVIEWED, "reviewStatus": REVIEW_STATUS,
 "purpose": "Standardised description of level of consciousness using eye, verbal and motor responses.",
 "intendedPopulation": "Adults and older children with impaired consciousness from any cause; most validated in traumatic brain injury.",
 "inputs": GCS_INPUTS,
 "values": [{"id": "total", "expr": "e + v + m"}],
 "primary": "total", "range": "3–15",
 "display": "{total}",
 "share": "GCS {total} ({e_code} {v_code} {m_code})",
 "notTestable": {"label": "Total not reported",
    "summary": "A component is not testable, so a total score should not be reported. Communicate the components instead.",
    "detail": "Substituting a value or summing the testable components misrepresents the patient.",
    "display": "{e_code} {v_code} {m_code}", "share": "GCS {e_code} {v_code} {m_code} (total not reported: component not testable)"},
 "states": [
   {"when": "total == 15", "state": "normal", "label": "No impairment measured", "range": "15",
    "summary": "No impairment of consciousness measured by GCS at this assessment.",
    "detail": "A GCS of 15 does not exclude significant intracranial pathology, focal deficits or later deterioration."},
   {"when": "total >= 13", "state": "low", "label": "Mild impairment range", "range": "13–14",
    "summary": "Within the mild range used in traumatic brain injury classification (GCS 13–15).",
    "detail": "Reassess serially. Subtle changes within this range can be clinically important."},
   {"when": "total >= 9", "state": "moderate", "label": "Moderate impairment", "range": "9–12",
    "summary": "Moderate impairment of consciousness (TBI classification GCS 9–12).",
    "detail": "Assess the cause, trajectory and associated findings according to the clinical situation and local protocol."},
   {"when": "total >= 3", "state": "high", "label": "Severe impairment", "range": "3–8",
    "summary": "Severe impairment of consciousness (TBI classification GCS 3–8).",
    "detail": "Assess airway, ventilation, oxygenation, neurological status and other reversible causes according to the clinical situation and local protocol."}],
 "insights": [
   {"when": "m <= 3", "text": "Motor score is the component most strongly associated with outcome. Abnormal flexion, extension or no motor response warrants close attention to the trajectory."},
   {"when": "total <= 8 && m >= 5", "text": "The total is low while the motor response is relatively preserved. Two patients with the same total can differ substantially; always report the components."},
   {"whenNotTestable": True, "when": "isnull(v)", "text": "With the verbal component not testable (e.g. intubated), the FOUR score includes brainstem reflexes and respiration and does not depend on verbal response."},
   {"text": "Report components with the total, e.g. E2 V3 M5 = 10. The components carry more information than the sum."}],
 "limitations": [
   "Developed for describing consciousness; its severity bands are derived from traumatic brain injury.",
   "Verbal response cannot be assessed in intubated or aphasic patients.",
   "Does not assess brainstem reflexes, pupils or lateralising signs.",
   "Inter-rater variability is higher in the intermediate range and with inexperienced assessors."],
 "confounders": ["Sedative or paralytic drugs", "Intoxication (alcohol, drugs)", "Hypoxia, hypotension, hypoglycaemia", "Post-ictal state", "Hypothermia", "Language barrier, deafness, aphasia", "Spinal cord injury or limb injury limiting motor response", "Facial or orbital swelling"],
 "commonErrors": [
   "Reporting a total when a component is not testable, or assigning 1 instead of NT.",
   "Recording the worst rather than the best motor response.",
   "Testing motor response in the lower limbs (spinal reflexes can mislead).",
   "Applying painful stimulus before checking the response to sound.",
   "Scoring 'localising' when the hand does not cross the clavicle."],
 "doesNotTellYou": ["The cause of impaired consciousness.", "Whether a focal or brainstem lesion is present.", "The need for any specific intervention.", "Prognosis on its own, outside an appropriate model."],
 "related": ["gcsp", "four", "wfns", "ich"],
 "sources": GCS_SOURCES, "licensing": GCS_LICENSE,
 "guide": {
   "what": "A three-component scale (eye, verbal, motor) that describes a patient's responsiveness. Totals range from 3 to 15.",
   "whenUseful": "Initial and serial neurological assessment, handover communication, trauma triage, and as an input to other scores (WFNS, ICH Score, GCS-P).",
   "howToCalculate": "Check for factors that interfere with each response. Observe first, then stimulate: sound before physical pressure. Record the best response for each component. Report components and, only when all are testable, the sum.",
   "clinicalContext": "Trends matter more than a single value. A fall of 2 or more points, or of 1 point in the motor score, is commonly treated as significant deterioration in TBI practice; respond according to local protocol."}
})

# ---------------------------------------------------------------- GCS-P
gcsp_inputs = json.loads(json.dumps(GCS_INPUTS)) + [{
  "id": "prs", "type": "choice", "label": "Pupil reactivity to light", "short": "Pupils",
  "help": "Only reactivity counts; pupil size does not enter the calculation.",
  "options": [opt("0", "Both pupils react", 0, "PRS0"), opt("1", "One pupil unreactive", 1, "PRS1"), opt("2", "Both pupils unreactive", 2, "PRS2"),
              opt("NT", "Not assessable", None, "PRS-NT", "e.g. orbital trauma, prior eye surgery, mydriatics.", nt=True)]}]
scores.append({
 "id": "gcsp", "name": "GCS-Pupils Score", "abbreviation": "GCS-P", "aliases": ["gcs pupils", "pupil reactivity score", "prs"],
 "category": "consciousness", "specialty": ["Neurosurgery", "Neurocritical Care", "Trauma"],
 "version": {"label": "Brennan, Murray & Teasdale 2018", "detail": "GCS-P = GCS total − Pupil Reactivity Score (number of unreactive pupils). Range 1–15."},
 "contentVersion": CV, "lastReviewed": REVIEWED, "reviewStatus": REVIEW_STATUS,
 "purpose": "Single index combining GCS and pupil reactivity to extend the range over which early severity relates to outcome after TBI.",
 "intendedPopulation": "Adults with traumatic brain injury (derived from CRASH and IMPACT data).",
 "inputs": gcsp_inputs,
 "values": [{"id": "gcs", "expr": "e + v + m"}, {"id": "total", "expr": "e + v + m - prs"}],
 "primary": "total", "range": "1–15", "display": "{total}",
 "share": "GCS-P {total} (GCS {gcs}: {e_code} {v_code} {m_code}; PRS {prs})",
 "notTestable": {"label": "GCS-P not calculable",
    "summary": "GCS-P requires a complete GCS total and an assessable pupil reaction.",
    "display": "{e_code} {v_code} {m_code}", "share": "GCS-P not calculable (component not testable)"},
 "states": [
   {"when": "total <= 8", "state": "high", "label": "Severe range", "range": "1–8",
    "summary": "GCS-P in the severe range (1–8).",
    "detail": "Lower GCS-P values were associated with higher mortality and lower probability of favourable outcome in the derivation data. Assess airway, ventilation, oxygenation, neurological status and reversible causes according to local protocol."},
   {"state": "info", "label": "Calculated", "range": "9–15",
    "summary": "GCS-P above the severe range.",
    "detail": "Lower values indicate more severe injury. Interpret alongside the components, pupil findings and imaging."}],
 "insights": [
   {"when": "prs >= 1", "text": "Pupil unreactivity lowers GCS-P below the GCS total, reflecting brainstem information the GCS does not capture."},
   {"text": "Report the GCS components, the pupil findings and the GCS-P together, never GCS-P alone."}],
 "limitations": ["Derived in TBI; not validated as a general coma measure.", "Prognostic associations come from trial and registry cohorts and may not transfer to every setting.", "Adds only reactivity, not pupil size or asymmetry."],
 "confounders": ["All GCS confounders (sedation, intoxication, hypoxia, hypotension)", "Ocular trauma", "Mydriatic or miotic drugs", "Prior eye surgery or disease"],
 "commonErrors": ["Counting pupil size or anisocoria instead of reactivity.", "Calculating from a GCS with a non-testable component.", "Reporting GCS-P without its components."],
 "doesNotTellYou": ["An individual patient's outcome.", "Which treatment is indicated.", "The cause of pupil abnormality."],
 "related": ["gcs", "four"],
 "sources": [{"citation": "Brennan PM, Murray GD, Teasdale GM. Simplifying the use of prognostic information in traumatic brain injury. Part 1: The GCS-Pupils score: an extended index of clinical severity. J Neurosurg. 2018;128(6):1612-1620.", "doi": "10.3171/2017.12.JNS172780"}] + GCS_SOURCES[:1],
 "licensing": GCS_LICENSE,
 "guide": {
   "what": "The GCS total minus the number of unreactive pupils (0, 1 or 2), giving a 1–15 index.",
   "whenUseful": "Early severity description after TBI, particularly at low GCS where pupil findings add prognostic information.",
   "howToCalculate": "Assess GCS with the structured approach. Assess each pupil's reaction to light. PRS = number of unreactive pupils. GCS-P = GCS − PRS.",
   "clinicalContext": "The authors also published probability charts combining GCS-P with age and CT findings; those charts are not reproduced in this app."}
})

# ---------------------------------------------------------------- FOUR
scores.append({
 "id": "four", "name": "Full Outline of UnResponsiveness Score", "abbreviation": "FOUR", "aliases": ["four score", "coma", "unresponsiveness", "wijdicks"],
 "category": "consciousness", "specialty": ["Neurocritical Care", "Neurology", "Neurosurgery"],
 "version": {"label": "Wijdicks et al. 2005 (adult)", "detail": "Four components, each scored 0–4. Total 0–16."},
 "contentVersion": CV, "lastReviewed": REVIEWED, "reviewStatus": REVIEW_STATUS,
 "purpose": "Coma scale that assesses eye, motor, brainstem and respiratory function without needing a verbal response.",
 "intendedPopulation": "Adults with impaired consciousness, including intubated patients in the ICU and emergency department.",
 "inputs": [
   {"id": "e", "type": "choice", "label": "Eye response", "short": "Eye (E)", "options": [
     opt("4", "Eyelids open or opened, tracking or blinking to command", 4, "E4"),
     opt("3", "Eyelids open, not tracking", 3, "E3"),
     opt("2", "Eyelids closed, open to loud voice", 2, "E2"),
     opt("1", "Eyelids closed, open to pain", 1, "E1"),
     opt("0", "Eyelids remain closed with pain", 0, "E0")]},
   {"id": "m", "type": "choice", "label": "Motor response", "short": "Motor (M)", "help": "Preferably tested in the upper limbs.", "options": [
     opt("4", "Thumbs-up, fist or peace sign to command", 4, "M4"),
     opt("3", "Localising to pain", 3, "M3"),
     opt("2", "Flexion response to pain", 2, "M2"),
     opt("1", "Extension response to pain", 1, "M1"),
     opt("0", "No response to pain, or generalised myoclonus status", 0, "M0")]},
   {"id": "b", "type": "choice", "label": "Brainstem reflexes", "short": "Brainstem (B)", "options": [
     opt("4", "Pupil and corneal reflexes present", 4, "B4"),
     opt("3", "One pupil wide and fixed", 3, "B3"),
     opt("2", "Pupil or corneal reflexes absent", 2, "B2"),
     opt("1", "Pupil and corneal reflexes absent", 1, "B1"),
     opt("0", "Absent pupil, corneal and cough reflexes", 0, "B0")]},
   {"id": "r", "type": "choice", "label": "Respiration", "short": "Respiration (R)", "options": [
     opt("4", "Not intubated, regular breathing pattern", 4, "R4"),
     opt("3", "Not intubated, Cheyne–Stokes breathing", 3, "R3"),
     opt("2", "Not intubated, irregular breathing", 2, "R2"),
     opt("1", "Breathes above ventilator rate", 1, "R1"),
     opt("0", "Breathes at ventilator rate, or apnoea", 0, "R0")]}],
 "values": [{"id": "total", "expr": "e + m + b + r"}],
 "primary": "total", "range": "0–16", "display": "{total}",
 "share": "FOUR {total} ({e_code} {m_code} {b_code} {r_code})",
 "states": [
   {"when": "total == 16", "state": "normal", "label": "No impairment measured", "range": "16",
    "summary": "No impairment detected across the four FOUR domains at this assessment."},
   {"when": "total == 0", "state": "critical", "label": "No measured responses", "range": "0",
    "summary": "No eye, motor, brainstem or respiratory response above ventilator rate was recorded.",
    "detail": "A FOUR score of 0 does not by itself establish death by neurologic criteria. That determination requires the full formal protocol, including exclusion of confounders and apnoea testing where applicable."},
   {"state": "info", "label": "Calculated", "range": "1–15",
    "summary": "The FOUR score has no validated severity bands. Interpret the components and the trend.",
    "detail": "Lower totals indicate greater impairment. Each component conveys distinct information."}],
 "insights": [
   {"when": "e == 4 && m <= 1", "text": "Eye tracking or blinking to command with little or no limb motor response: consider locked-in syndrome, or limb or spinal factors limiting motor response."},
   {"when": "e == 3", "text": "Eyes open without tracking can be seen in disorders of consciousness such as the vegetative state / unresponsive wakefulness."},
   {"when": "b <= 2", "text": "Loss of brainstem reflexes is a major finding. Exclude confounders (drugs, hypothermia, metabolic causes) before drawing conclusions."},
   {"when": "r == 0", "text": "R0 includes breathing at ventilator rate; it does not establish apnoea. Formal apnoea testing is a separate procedure."}],
 "limitations": ["No universally accepted severity categories.", "Fewer validation studies in children and outside ICU settings than GCS.", "Respiratory component depends on ventilator settings and sedation."],
 "confounders": ["Sedatives, neuromuscular blockade", "Hypothermia", "Metabolic encephalopathy", "Ocular trauma or prior eye disease", "High cervical cord injury"],
 "commonErrors": ["Scoring respiration without considering ventilator mode and sedation.", "Treating B3 as bilateral pupil loss (it is one pupil wide and fixed).", "Testing motor response in the legs."],
 "doesNotTellYou": ["Whether the criteria for death by neurologic criteria are met.", "The cause of coma.", "The appropriate intervention."],
 "related": ["gcs", "gcsp", "rass"],
 "sources": [{"citation": "Wijdicks EFM, Bamlet WR, Maramattom BV, Manno EM, McClelland RL. Validation of a new coma scale: The FOUR score. Ann Neurol. 2005;58(4):585-593.", "doi": "10.1002/ana.20611"},
             {"citation": "Wolf CA, Wijdicks EFM, Bamlet WR, McClelland RL. Further validation of the FOUR score coma scale by intensive care nurses. Mayo Clin Proc. 2007;82(4):435-438."}],
 "licensing": {"status": "Criteria in original wording; official figure not reproduced",
    "note": "The published FOUR score figure is © Mayo Foundation. Confirm permission with Mayo Clinic before commercial distribution of this score."},
 "guide": {
   "what": "A 0–16 coma scale with four components (eye, motor, brainstem, respiration), each scored 0–4.",
   "whenUseful": "Patients who are intubated, aphasic or deeply comatose, where GCS verbal assessment is not possible or brainstem findings matter.",
   "howToCalculate": "Score each domain 0–4 using the best observed response, then sum. Record the components alongside the total.",
   "clinicalContext": "Detects features the GCS cannot, such as locked-in syndrome (eye blinking to command) and brainstem reflex loss."}
})

# ---------------------------------------------------------------- ICH Score
scores.append({
 "id": "ich", "name": "ICH Score", "abbreviation": "ICH Score", "aliases": ["intracerebral hemorrhage", "intracerebral haemorrhage", "hemphill", "ich"],
 "category": "ich", "specialty": ["Stroke", "Neurocritical Care", "Neurosurgery"],
 "version": {"label": "Hemphill et al. 2001 (original)", "detail": "Five components, total 0–6. Mortality figures are the observed 30-day mortality in the derivation cohort (n = 152)."},
 "contentVersion": CV, "lastReviewed": REVIEWED, "reviewStatus": REVIEW_STATUS,
 "purpose": "Standardised clinical grading of spontaneous intracerebral haemorrhage severity at presentation.",
 "intendedPopulation": "Adults with spontaneous (non-traumatic) intracerebral haemorrhage, assessed at presentation.",
 "inputs": [
   {"id": "gcs", "type": "choice", "label": "GCS at presentation", "short": "GCS", "options": [opt("0", "13–15", 0), opt("1", "5–12", 1), opt("2", "3–4", 2)]},
   {"id": "vol", "type": "choice", "label": "ICH volume", "short": "Volume", "help": "Measured on initial CT, commonly by the ABC/2 method.", "options": [opt("0", "Less than 30 mL", 0), opt("1", "30 mL or more", 1)]},
   yesno("ivh", "Intraventricular haemorrhage", "IVH"),
   {"id": "infra", "type": "choice", "label": "Origin of haemorrhage", "short": "Origin", "options": [opt("0", "Supratentorial", 0), opt("1", "Infratentorial", 1)]},
   {"id": "age", "type": "choice", "label": "Age", "short": "Age", "options": [opt("0", "Under 80 years", 0), opt("1", "80 years or older", 1)]}],
 "values": [{"id": "total", "expr": "gcs + vol + ivh + infra + age"}],
 "primary": "total", "range": "0–6", "display": "{total}", "share": "ICH Score {total}",
 "states": [
   {"when": "total == 0", "state": "low", "label": "Score 0", "range": "0", "summary": "Observed 30-day mortality in the derivation cohort: 0%."},
   {"when": "total == 1", "state": "mild", "label": "Score 1", "range": "1", "summary": "Observed 30-day mortality in the derivation cohort: 13%."},
   {"when": "total == 2", "state": "moderate", "label": "Score 2", "range": "2", "summary": "Observed 30-day mortality in the derivation cohort: 26%."},
   {"when": "total == 3", "state": "high", "label": "Score 3", "range": "3", "summary": "Observed 30-day mortality in the derivation cohort: 72%."},
   {"when": "total == 4", "state": "critical", "label": "Score 4", "range": "4", "summary": "Observed 30-day mortality in the derivation cohort: 97%."},
   {"when": "total == 5", "state": "critical", "label": "Score 5", "range": "5", "summary": "Observed 30-day mortality in the derivation cohort: 100%."},
   {"when": "total == 6", "state": "critical", "label": "Score 6", "range": "6", "summary": "No patient in the derivation cohort had a score of 6; no observed mortality figure exists."}],
 "insights": [
   {"text": "Mortality figures describe a 2001 derivation cohort in which care limitations were common. Early do-not-resuscitate decisions can make prognostic scores self-fulfilling."},
   {"when": "total >= 3", "text": "A high score should not by itself determine goals of care. Guidelines advise against early care limitation based on a single prognostic score."}],
 "limitations": ["Derived in a small single-centre cohort.", "Not designed to guide individual treatment decisions.", "Does not include haematoma expansion, anticoagulation, or location detail beyond supra/infratentorial."],
 "confounders": ["GCS depressed by sedation, intoxication or seizures", "Volume estimation error (irregular haematomas, ABC/2 overestimation)", "Timing of the CT relative to symptom onset"],
 "commonErrors": ["Using a GCS obtained after sedation or intubation.", "Measuring volume on a later scan rather than the initial CT.", "Applying the score to traumatic or tumour-related haemorrhage."],
 "doesNotTellYou": ["Functional outcome in survivors.", "Whether surgery or any intervention is indicated.", "An individual patient's prognosis."],
 "related": ["gcs", "mrs"],
 "sources": [{"citation": "Hemphill JC 3rd, Bonovich DC, Besmertis L, Manley GT, Johnston SC. The ICH score: a simple, reliable grading scale for intracerebral hemorrhage. Stroke. 2001;32(4):891-897.", "doi": "10.1161/01.STR.32.4.891"},
             {"citation": "Zahuranec DB, et al. Early care limitations independently predict mortality after intracerebral hemorrhage. Neurology. 2007;68(20):1651-1657.", "doi": "10.1212/01.wnl.0000261906.93238.72"}],
 "licensing": {"status": "Published scoring criteria, original wording", "note": "No reproduction restrictions identified for the scoring criteria."},
 "guide": {
   "what": "A 0–6 grading scale combining GCS, haematoma volume, intraventricular extension, infratentorial origin and age.",
   "whenUseful": "Standardised communication of ICH severity at presentation, research stratification, and as one input into prognostic discussion.",
   "howToCalculate": "Use the GCS at presentation and the initial CT. Assign points for each component and sum.",
   "clinicalContext": "Use as a severity descriptor, not a prognosis for an individual patient. Prognostic discussions should integrate the full clinical picture and should not rely on early scores alone."}
})

# ---------------------------------------------------------------- Hunt & Hess
scores.append({
 "id": "hunthess", "name": "Hunt and Hess Scale", "abbreviation": "Hunt & Hess", "aliases": ["hunt hess", "h&h", "sah grade", "subarachnoid"],
 "category": "sah", "specialty": ["Neurosurgery", "Neurocritical Care"],
 "version": {"label": "Original 1968 classification", "detail": "Includes the original rule that serious systemic disease or severe vasospasm on arteriography moves the patient to the next less favourable grade. Many units apply the scale without this modifier; record which you use."},
 "contentVersion": CV, "lastReviewed": REVIEWED, "reviewStatus": REVIEW_STATUS,
 "purpose": "Clinical grading of aneurysmal subarachnoid haemorrhage severity.",
 "intendedPopulation": "Patients with aneurysmal subarachnoid haemorrhage.",
 "inputs": [
   {"id": "grade", "type": "choice", "label": "Clinical presentation", "short": "Clinical grade", "options": [
     opt("1", "Asymptomatic, or minimal headache and slight neck stiffness", 1, "I"),
     opt("2", "Moderate to severe headache, neck stiffness, no deficit other than cranial nerve palsy", 2, "II"),
     opt("3", "Drowsiness, confusion, or mild focal deficit", 3, "III"),
     opt("4", "Stupor, moderate to severe hemiparesis, possible early decerebrate rigidity and vegetative disturbance", 4, "IV"),
     opt("5", "Deep coma, decerebrate rigidity, moribund appearance", 5, "V")]},
   yesno("mod", "Serious systemic disease or severe vasospasm on arteriography", "Modifier",
         help="Original examples: hypertension, diabetes, severe arteriosclerosis, chronic pulmonary disease.")],
 "values": [{"id": "final", "expr": "min(5, grade + mod)"}],
 "primary": "final", "range": "I–V", "display": "Grade {roman(final)}",
 "share": "Hunt & Hess Grade {roman(final)} (clinical {roman(grade)}{mod == 1 ? ' + modifier' : ''})",
 "states": [
   {"when": "final == 1", "state": "low", "label": "Grade I", "range": "I", "summary": "Least severe clinical grade."},
   {"when": "final == 2", "state": "mild", "label": "Grade II", "range": "II", "summary": "Headache and meningism without focal deficit (cranial nerve palsy allowed)."},
   {"when": "final == 3", "state": "moderate", "label": "Grade III", "range": "III", "summary": "Drowsiness, confusion or mild focal deficit."},
   {"when": "final == 4", "state": "high", "label": "Grade IV", "range": "IV", "summary": "Stupor with significant deficit. Commonly grouped as poor grade (IV–V)."},
   {"when": "final == 5", "state": "critical", "label": "Grade V", "range": "V", "summary": "Deep coma. Commonly grouped as poor grade (IV–V)."}],
 "insights": [
   {"when": "mod == 1", "text": "The grade has been moved up one level by the original systemic disease/vasospasm modifier. State this when communicating the grade."},
   {"text": "Grade can change rapidly with hydrocephalus, rebleeding or seizures. Reassess after resuscitation and CSF diversion."}],
 "limitations": ["Descriptors are subjective; inter-rater reliability is modest.", "The systemic disease modifier is inconsistently applied across centres.", "Mixes level of consciousness and focal deficit in single categories."],
 "confounders": ["Acute hydrocephalus", "Post-ictal state", "Sedation", "Systemic hypoxia or hypotension"],
 "commonErrors": ["Mixing the original modifier and unmodified use without stating which was applied.", "Grading before resuscitation without recording timing."],
 "doesNotTellYou": ["Aneurysm characteristics or rebleeding risk.", "Delayed cerebral ischaemia risk.", "Which treatment is indicated."],
 "related": ["wfns", "mwfns", "mfisher", "gcs"],
 "sources": [{"citation": "Hunt WE, Hess RM. Surgical risk as related to time of intervention in the repair of intracranial aneurysms. J Neurosurg. 1968;28(1):14-20.", "doi": "10.3171/jns.1968.28.1.0014"},
             {"citation": "Rosen DS, Macdonald RL. Subarachnoid hemorrhage grading scales: a systematic review. Neurocrit Care. 2005;2(2):110-118."}],
 "licensing": {"status": "Published classification, original wording", "note": "No reproduction restrictions identified."},
 "guide": {
   "what": "A five-grade clinical classification of aneurysmal SAH based on headache, meningism, consciousness and focal deficit.",
   "whenUseful": "Admission grading, communication between teams, and research stratification.",
   "howToCalculate": "Choose the description that best fits the presentation. In the original version, move one grade worse if serious systemic disease or severe arteriographic vasospasm is present (maximum Grade V).",
   "clinicalContext": "Poor-grade status (IV–V) is used in many studies. Grades should be documented with timing relative to resuscitation."}
})

# ---------------------------------------------------------------- WFNS (original)
scores.append({
 "id": "wfns", "name": "WFNS Subarachnoid Haemorrhage Grade", "abbreviation": "WFNS", "aliases": ["world federation", "sah grade", "subarachnoid", "o-wfns"],
 "category": "sah", "specialty": ["Neurosurgery", "Neurocritical Care"],
 "version": {"label": "Original WFNS (1988)", "detail": "Uses GCS and presence of a major focal deficit. GCS 15 with a focal deficit is not defined in the original scale. The 2015 modified WFNS is a separate entry."},
 "contentVersion": CV, "lastReviewed": REVIEWED, "reviewStatus": REVIEW_STATUS,
 "purpose": "Grading of aneurysmal subarachnoid haemorrhage based on GCS and focal motor deficit.",
 "intendedPopulation": "Patients with aneurysmal subarachnoid haemorrhage.",
 "inputs": [
   {"id": "gcs", "type": "number", "label": "GCS total", "short": "GCS", "min": 3, "max": 15, "integer": True, "help": "Enter a complete GCS total (3–15).", "link": "gcs"},
   yesno("deficit", "Major focal neurological deficit", "Focal deficit", help="Commonly interpreted as hemiparesis or aphasia.")],
 "values": [{"id": "grade", "expr": "gcs == 15 ? (deficit == 0 ? 1 : 0) : gcs >= 13 ? (deficit == 0 ? 2 : 3) : gcs >= 7 ? 4 : 5"}],
 "primary": "grade", "range": "I–V", "display": "{grade == 0 ? 'Undefined' : 'Grade ' + roman(grade)}",
 "share": "WFNS (original) {grade == 0 ? 'not defined' : 'Grade ' + roman(grade)} (GCS {gcs}, deficit {deficit == 1 ? 'present' : 'absent'})",
 "states": [
   {"when": "grade == 0", "state": "incomplete", "label": "Not defined in original WFNS", "range": "GCS 15 + deficit",
    "summary": "The original WFNS scale does not define a grade for GCS 15 with a focal deficit.",
    "detail": "Document GCS and the deficit explicitly. The modified WFNS (2015) grades by GCS alone and would assign Grade I."},
   {"when": "grade == 1", "state": "low", "label": "Grade I", "range": "GCS 15, no deficit", "summary": "Good-grade SAH (Grades I–III commonly grouped as good grade)."},
   {"when": "grade == 2", "state": "mild", "label": "Grade II", "range": "GCS 13–14, no deficit", "summary": "Good-grade SAH."},
   {"when": "grade == 3", "state": "moderate", "label": "Grade III", "range": "GCS 13–14, deficit", "summary": "Good-grade SAH with focal deficit."},
   {"when": "grade == 4", "state": "high", "label": "Grade IV", "range": "GCS 7–12", "summary": "Poor-grade SAH (Grades IV–V)."},
   {"when": "grade == 5", "state": "critical", "label": "Grade V", "range": "GCS 3–6", "summary": "Poor-grade SAH (Grades IV–V)."}],
 "insights": [
   {"when": "gcs >= 13 && gcs <= 14", "text": "In this GCS range the deficit determines Grade II vs III, the distinction with the most inter-rater variability."},
   {"when": "grade >= 4", "text": "Grade may improve after treatment of hydrocephalus or seizures. Record the timing of grading."}],
 "limitations": ["GCS 15 with deficit is undefined.", "Grade II vs III separation has limited prognostic discrimination.", "Inherits all GCS limitations."],
 "confounders": ["Acute hydrocephalus", "Post-ictal state", "Sedation or intubation (GCS not fully testable)"],
 "commonErrors": ["Mixing original and modified WFNS.", "Using a GCS with a non-testable component.", "Counting cranial nerve palsy as a major focal deficit."],
 "doesNotTellYou": ["Imaging burden or vasospasm risk (see modified Fisher).", "Aneurysm characteristics.", "Treatment choice."],
 "related": ["mwfns", "hunthess", "mfisher", "gcs"],
 "sources": [{"citation": "Drake CG. Report of World Federation of Neurological Surgeons Committee on a Universal Subarachnoid Hemorrhage Grading Scale. J Neurosurg. 1988;68(6):985-986."},
             {"citation": "Sano H, Satoh A, Murayama Y, et al. Modified World Federation of Neurosurgical Societies subarachnoid hemorrhage grading system. World Neurosurg. 2015;83(5):801-807."}],
 "licensing": {"status": "Published classification, original wording", "note": "No reproduction restrictions identified."},
 "guide": {
   "what": "A five-grade SAH scale combining GCS total with the presence of a major focal deficit.",
   "whenUseful": "Admission grading, triage communication and research stratification.",
   "howToCalculate": "Obtain a full GCS. GCS 15 without deficit = I; 13–14 without deficit = II; 13–14 with deficit = III; 7–12 = IV; 3–6 = V.",
   "clinicalContext": "Widely used alongside Hunt & Hess. Grades IV–V are commonly termed poor grade."}
})

# ---------------------------------------------------------------- Modified WFNS
scores.append({
 "id": "mwfns", "name": "Modified WFNS Grade", "abbreviation": "m-WFNS", "aliases": ["modified wfns", "sano", "sah grade", "subarachnoid"],
 "category": "sah", "specialty": ["Neurosurgery", "Neurocritical Care"],
 "version": {"label": "Modified WFNS (Sano et al. 2015)", "detail": "Proposed by the WFNS Cerebrovascular Disease & Treatment Committee with the Japan Neurosurgical Society. Grades by GCS alone; focal deficit is not used."},
 "contentVersion": CV, "lastReviewed": REVIEWED, "reviewStatus": REVIEW_STATUS,
 "purpose": "GCS-only SAH grading intended to improve prognostic separation of grades II and III.",
 "intendedPopulation": "Patients with aneurysmal subarachnoid haemorrhage.",
 "inputs": [{"id": "gcs", "type": "number", "label": "GCS total", "short": "GCS", "min": 3, "max": 15, "integer": True, "help": "Enter a complete GCS total (3–15).", "link": "gcs"}],
 "values": [{"id": "grade", "expr": "gcs == 15 ? 1 : gcs == 14 ? 2 : gcs == 13 ? 3 : gcs >= 7 ? 4 : 5"}],
 "primary": "grade", "range": "I–V", "display": "Grade {roman(grade)}", "share": "m-WFNS Grade {roman(grade)} (GCS {gcs})",
 "states": [
   {"when": "grade == 1", "state": "low", "label": "Grade I", "range": "GCS 15", "summary": "Least severe grade."},
   {"when": "grade == 2", "state": "mild", "label": "Grade II", "range": "GCS 14", "summary": "Mildly reduced consciousness."},
   {"when": "grade == 3", "state": "moderate", "label": "Grade III", "range": "GCS 13", "summary": "Moderately reduced consciousness."},
   {"when": "grade == 4", "state": "high", "label": "Grade IV", "range": "GCS 7–12", "summary": "Poor grade."},
   {"when": "grade == 5", "state": "critical", "label": "Grade V", "range": "GCS 3–6", "summary": "Poor grade."}],
 "insights": [{"text": "Not interchangeable with the original WFNS. Always label which version is reported."}],
 "limitations": ["Fewer external validation studies than the original WFNS.", "Ignores focal deficit entirely.", "Inherits GCS limitations."],
 "confounders": ["Acute hydrocephalus", "Post-ictal state", "Sedation or intubation"],
 "commonErrors": ["Reporting as 'WFNS' without stating the modified version.", "Using a GCS with a non-testable component."],
 "doesNotTellYou": ["Focal deficit status.", "Vasospasm or DCI risk.", "Treatment choice."],
 "related": ["wfns", "hunthess", "mfisher"],
 "sources": [{"citation": "Sano H, Satoh A, Murayama Y, et al. Modified World Federation of Neurosurgical Societies subarachnoid hemorrhage grading system. World Neurosurg. 2015;83(5):801-807."}],
 "licensing": {"status": "Published classification, original wording", "note": "No reproduction restrictions identified."},
 "guide": {
   "what": "A GCS-only version of the WFNS grade: 15 = I, 14 = II, 13 = III, 7–12 = IV, 3–6 = V.",
   "whenUseful": "Where a GCS-only grade is preferred, or the original Grade II/III distinction is unreliable.",
   "howToCalculate": "Obtain a full GCS and map it to the grade.",
   "clinicalContext": "Use the version your unit and the relevant literature use, and label it."}
})

# ---------------------------------------------------------------- Modified Fisher
scores.append({
 "id": "mfisher", "name": "Modified Fisher Scale", "abbreviation": "mFisher", "aliases": ["modified fisher", "fisher", "vasospasm", "sah ct", "frontera"],
 "category": "sah", "specialty": ["Neurosurgery", "Neurocritical Care", "Neuroradiology"],
 "version": {"label": "Frontera et al. 2006", "detail": "CT grade 0–4 from cisternal clot thickness and IVH. Distinct from the original Fisher scale (1980) and from the Claassen 2001 scale."},
 "contentVersion": CV, "lastReviewed": REVIEWED, "reviewStatus": REVIEW_STATUS,
 "purpose": "CT grading of SAH blood burden associated with risk of symptomatic vasospasm.",
 "intendedPopulation": "Patients with aneurysmal subarachnoid haemorrhage, graded on the admission CT.",
 "inputs": [
   {"id": "sah", "type": "choice", "label": "Cisternal subarachnoid blood", "short": "SAH", "options": [
     opt("0", "None", 0), opt("1", "Thin (focal or diffuse)", 1, detail="Not completely filling any cistern or fissure."),
     opt("2", "Thick", 2, detail="Completely filling at least one cistern or fissure.")]},
   yesno("ivh", "Intraventricular haemorrhage", "IVH")],
 "values": [{"id": "grade", "expr": "sah == 0 ? (ivh == 0 ? 0 : -1) : sah == 1 ? (ivh == 1 ? 2 : 1) : (ivh == 1 ? 4 : 3)"}],
 "primary": "grade", "range": "0–4", "display": "{grade < 0 ? 'Undefined' : 'Grade ' + grade}",
 "share": "Modified Fisher {grade < 0 ? 'not defined' : 'Grade ' + grade}",
 "states": [
   {"when": "grade < 0", "state": "incomplete", "label": "Not defined", "range": "IVH without SAH",
    "summary": "The modified Fisher scale does not define a grade for IVH without subarachnoid blood.",
    "detail": "Describe the findings explicitly. Consider whether an alternative scale (e.g. Graeb for IVH) is appropriate."},
   {"when": "grade == 0", "state": "low", "label": "Grade 0", "range": "0", "summary": "No SAH or IVH on CT."},
   {"when": "grade == 1", "state": "low", "label": "Grade 1", "range": "1", "summary": "Thin SAH, no IVH. Reference category (with grade 0) in the derivation study."},
   {"when": "grade == 2", "state": "moderate", "label": "Grade 2", "range": "2", "summary": "Thin SAH with IVH. Crude OR for symptomatic vasospasm 1.6 vs grades 0–1."},
   {"when": "grade == 3", "state": "moderate", "label": "Grade 3", "range": "3", "summary": "Thick SAH, no IVH. Crude OR for symptomatic vasospasm 1.6 vs grades 0–1."},
   {"when": "grade == 4", "state": "high", "label": "Grade 4", "range": "4", "summary": "Thick SAH with IVH. Crude OR for symptomatic vasospasm 2.2 vs grades 0–1."}],
 "insights": [
   {"text": "Odds ratios are from the derivation cohort (placebo arms of tirilazad trials, n = 1355; 33% developed symptomatic vasospasm)."},
   {"when": "grade >= 2", "text": "Risk estimates are group-level. Delayed cerebral ischaemia surveillance should follow local protocol for all aneurysmal SAH."}],
 "limitations": ["Thickness judgement is subjective.", "IVH is binary and ignores its volume.", "CT timing affects the grade as blood clears."],
 "confounders": ["Delayed CT (blood redistribution and clearance)", "Post-procedural blood or contrast", "Motion or beam-hardening artefact"],
 "commonErrors": ["Confusing with the original Fisher scale (grades 1–4) or the Claassen scale.", "Grading from a post-treatment CT.", "Applying to non-aneurysmal or traumatic SAH."],
 "doesNotTellYou": ["Clinical grade (see WFNS / Hunt & Hess).", "Individual vasospasm probability.", "Treatment choice."],
 "related": ["wfns", "mwfns", "hunthess"],
 "sources": [{"citation": "Frontera JA, Claassen J, Schmidt JM, et al. Prediction of symptomatic vasospasm after subarachnoid hemorrhage: the modified Fisher scale. Neurosurgery. 2006;59(1):21-27.", "doi": "10.1227/01.NEU.0000218821.34014.1B"}],
 "licensing": {"status": "Published classification, original wording", "note": "No reproduction restrictions identified."},
 "guide": {
   "what": "A 0–4 CT grade based on whether cisternal SAH is thin or thick, and whether IVH is present.",
   "whenUseful": "Stratifying vasospasm/DCI risk on the admission CT, and in research.",
   "howToCalculate": "On the admission CT, decide whether cisternal blood is absent, thin, or thick (completely filling at least one cistern or fissure). Note IVH. 0: none; 1: thin, no IVH; 2: thin + IVH; 3: thick, no IVH; 4: thick + IVH.",
   "clinicalContext": "Frequently combined with the clinical grade (e.g. in VASOGRADE). Use the admission scan."}
})

# ---------------------------------------------------------------- mRS
scores.append({
 "id": "mrs", "name": "Modified Rankin Scale", "abbreviation": "mRS", "aliases": ["rankin", "disability", "functional outcome", "stroke outcome"],
 "category": "functional", "specialty": ["Stroke", "Neurology", "Neurosurgery", "Rehabilitation"],
 "version": {"label": "Modified Rankin Scale (UK-TIA wording, 0–6)", "detail": "Rankin 1957, modified by van Swieten et al. 1988 with grade 6 (death) commonly added in trials."},
 "contentVersion": CV, "lastReviewed": REVIEWED, "reviewStatus": REVIEW_STATUS,
 "purpose": "Global measure of disability and dependence in daily activities.",
 "intendedPopulation": "Adults after stroke and other neurological disorders.",
 "inputs": [{"id": "grade", "type": "choice", "label": "Functional level", "short": "mRS grade", "options": [
   opt("0", "No symptoms", 0, "0"),
   opt("1", "No significant disability despite symptoms", 1, "1", "Able to carry out all usual duties and activities."),
   opt("2", "Slight disability", 2, "2", "Unable to carry out all previous activities, but looks after own affairs without assistance."),
   opt("3", "Moderate disability", 3, "3", "Requires some help, but walks without assistance."),
   opt("4", "Moderately severe disability", 4, "4", "Unable to walk or attend to bodily needs without assistance."),
   opt("5", "Severe disability", 5, "5", "Bedridden, incontinent, requires constant nursing care."),
   opt("6", "Dead", 6, "6")]}],
 "values": [{"id": "g", "expr": "grade"}],
 "primary": "g", "range": "0–6", "display": "mRS {g}", "share": "mRS {g}",
 "states": [
   {"when": "g == 0", "state": "normal", "label": "No symptoms", "range": "0", "summary": "No symptoms reported or observed."},
   {"when": "g == 1", "state": "low", "label": "No significant disability", "range": "1", "summary": "Symptoms present but all usual activities possible."},
   {"when": "g == 2", "state": "mild", "label": "Slight disability", "range": "2", "summary": "Independent in own affairs, with some activity restriction."},
   {"when": "g == 3", "state": "moderate", "label": "Moderate disability", "range": "3", "summary": "Needs some help; walks without assistance."},
   {"when": "g == 4", "state": "high", "label": "Moderately severe disability", "range": "4", "summary": "Dependent for walking and bodily needs."},
   {"when": "g == 5", "state": "critical", "label": "Severe disability", "range": "5", "summary": "Requires constant care."},
   {"when": "g == 6", "state": "info", "label": "Dead", "range": "6", "summary": "Death."}],
 "insights": [
   {"text": "'Favourable outcome' thresholds differ between trials (mRS 0–1, 0–2, or shift analysis). State the definition when comparing results."},
   {"when": "g >= 1 && g <= 3", "text": "Boundaries between grades 1–3 have the most inter-rater variability. Structured interviews improve reliability."}],
 "limitations": ["Moderate inter-rater reliability without structured assessment.", "Weighted toward mobility; cognitive and mood effects may be under-represented.", "Pre-stroke disability affects interpretation."],
 "confounders": ["Pre-morbid disability", "Non-neurological comorbidity", "Proxy versus patient report"],
 "commonErrors": ["Not recording pre-stroke mRS.", "Grading from mobility alone.", "Assigning 0 when minor symptoms persist (should be 1)."],
 "doesNotTellYou": ["The specific deficit causing disability.", "Quality of life.", "Rehabilitation potential."],
 "related": ["ich", "gcs"],
 "sources": [{"citation": "van Swieten JC, Koudstaal PJ, Visser MC, Schouten HJ, van Gijn J. Interobserver agreement for the assessment of handicap in stroke patients. Stroke. 1988;19(5):604-607.", "doi": "10.1161/01.STR.19.5.604"},
             {"citation": "Rankin J. Cerebral vascular accidents in patients over the age of 60. II. Prognosis. Scott Med J. 1957;2(5):200-215."}],
 "licensing": {"status": "Grade definitions in widely published wording", "note": "Structured interview instruments for mRS (e.g. mRS-9Q, RFA) have their own terms and are not reproduced."},
 "guide": {
   "what": "A 7-level ordinal scale from 0 (no symptoms) to 6 (dead) describing global disability.",
   "whenUseful": "Stroke trial outcomes, documenting pre-morbid function, and follow-up assessment.",
   "howToCalculate": "Select the single level that best describes the patient's current function, considering all activities. Use a structured interview where possible.",
   "clinicalContext": "Pre-stroke mRS influences eligibility decisions in many protocols and should be documented."}
})

# ---------------------------------------------------------------- RASS
scores.append({
 "id": "rass", "name": "Richmond Agitation–Sedation Scale", "abbreviation": "RASS", "aliases": ["sedation", "agitation", "richmond", "icu"],
 "category": "neurocritical", "specialty": ["Neurocritical Care", "Critical Care"],
 "version": {"label": "Sessler et al. 2002", "detail": "10 levels from +4 (combative) to −5 (unarousable)."},
 "contentVersion": CV, "lastReviewed": REVIEWED, "reviewStatus": REVIEW_STATUS,
 "purpose": "Standardised description of agitation and depth of sedation in critically ill patients.",
 "intendedPopulation": "Adult ICU patients, sedated or not.",
 "inputs": [{"id": "level", "type": "choice", "label": "Observed level", "short": "RASS level",
   "help": "Observe first. If not alert, call by name and ask to open eyes and look at you. Use physical stimulation only if there is no response to voice.",
   "options": [
     opt("4", "+4 Combative", 4, "+4", "Overtly combative or violent; immediate danger to staff."),
     opt("3", "+3 Very agitated", 3, "+3", "Pulls on or removes tubes or catheters; aggressive."),
     opt("2", "+2 Agitated", 2, "+2", "Frequent non-purposeful movement; fights the ventilator."),
     opt("1", "+1 Restless", 1, "+1", "Anxious, but movements not aggressive or vigorous."),
     opt("0", "0 Alert and calm", 0, "0"),
     opt("-1", "−1 Drowsy", -1, "-1", "Not fully alert; sustained (over 10 s) awakening with eye contact to voice."),
     opt("-2", "−2 Light sedation", -2, "-2", "Briefly (under 10 s) awakens with eye contact to voice."),
     opt("-3", "−3 Moderate sedation", -3, "-3", "Movement or eye opening to voice, but no eye contact."),
     opt("-4", "−4 Deep sedation", -4, "-4", "No response to voice; movement or eye opening to physical stimulation."),
     opt("-5", "−5 Unarousable", -5, "-5", "No response to voice or physical stimulation.")]}],
 "values": [{"id": "l", "expr": "level"}],
 "primary": "l", "range": "+4 to −5", "display": "RASS {signed(l)}", "share": "RASS {signed(l)}",
 "states": [
   {"when": "l >= 3", "state": "high", "label": "Severe agitation", "range": "+3 to +4", "summary": "Agitation with risk to patient or staff safety.",
    "detail": "Assess for pain, delirium, hypoxia, withdrawal and other causes according to local protocol."},
   {"when": "l >= 1", "state": "mild", "label": "Restless to agitated", "range": "+1 to +2", "summary": "Increased activity or agitation."},
   {"when": "l == 0", "state": "normal", "label": "Alert and calm", "range": "0", "summary": "Alert and calm."},
   {"when": "l >= -2", "state": "info", "label": "Drowsy to light sedation", "range": "−1 to −2", "summary": "Responds to voice with eye contact."},
   {"when": "l == -3", "state": "info", "label": "Moderate sedation", "range": "−3", "summary": "Responds to voice without eye contact."},
   {"state": "moderate", "label": "Deep sedation or unarousable", "range": "−4 to −5", "summary": "No response to voice.",
    "detail": "Whether this level is appropriate depends on the sedation target set for this patient. Delirium screening (e.g. CAM-ICU) cannot be performed at −4 or −5."}],
 "insights": [
   {"text": "Compare the observed level against the prescribed sedation target; RASS itself does not define the target."},
   {"when": "l >= -3", "text": "At RASS −3 or above, delirium screening (e.g. CAM-ICU) is possible."}],
 "limitations": ["Validated in adult ICU populations.", "Depends on response to voice: limited in deafness, language barriers, or neurological deficits affecting eye opening."],
 "confounders": ["Neuromuscular blockade", "Structural brain injury", "Deafness or language barrier", "Ocular injury"],
 "commonErrors": ["Using physical stimulation before voice.", "Confusing brief (−2) with sustained (−1) eye contact.", "Scoring during a procedure or immediately after a sedative bolus without noting it."],
 "doesNotTellYou": ["Presence of delirium.", "Pain level.", "Underlying cause of agitation or depressed arousal."],
 "related": ["four", "gcs"],
 "sources": [{"citation": "Sessler CN, Gosnell MS, Grap MJ, et al. The Richmond Agitation-Sedation Scale: validity and reliability in adult intensive care unit patients. Am J Respir Crit Care Med. 2002;166(10):1338-1344.", "doi": "10.1164/rccm.2107138"},
             {"citation": "Ely EW, Truman B, Shintani A, et al. Monitoring sedation status over time in ICU patients: reliability and validity of the RASS. JAMA. 2003;289(22):2983-2991."}],
 "licensing": {"status": "Published scale, original wording", "note": "No reproduction restrictions identified."},
 "guide": {
   "what": "A 10-point scale describing a patient's level of agitation (+1 to +4), calm alertness (0), or sedation (−1 to −5).",
   "whenUseful": "Titrating sedation to a target, communicating arousal state, and as the first step of CAM-ICU delirium screening.",
   "howToCalculate": "Observe for 30 seconds. If not alert, address by name and ask the patient to open eyes and look at you; note eye contact and its duration. If no response to voice, use physical stimulation (shoulder shake, then sternal rub).",
   "clinicalContext": "Targets are individualised; light sedation is the default target in many ICU guidelines unless a deeper level is specifically indicated."}
})

CATEGORIES = [
 {"id": "consciousness", "name": "Consciousness"},
 {"id": "stroke", "name": "Stroke"},
 {"id": "ich", "name": "Intracerebral haemorrhage"},
 {"id": "sah", "name": "Subarachnoid haemorrhage"},
 {"id": "tbi", "name": "Traumatic brain injury"},
 {"id": "spine", "name": "Spine and spinal cord"},
 {"id": "oncology", "name": "Neuro-oncology"},
 {"id": "functional", "name": "Functional and disability"},
 {"id": "neurocritical", "name": "Neurocritical care"},
 {"id": "general", "name": "General neurology"},
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "app", "assets", "content")
    os.makedirs(os.path.join(out, "scores"), exist_ok=True)
    ids = set(s["id"] for s in scores)
    for s in scores:
        for r in s["related"]:
            assert r in ids, (s["id"], "related", r)
        assert s["category"] in [c["id"] for c in CATEGORIES], s["id"]
        with open(os.path.join(out, "scores", s["id"] + ".json"), "w") as f:
            json.dump(s, f, ensure_ascii=False, indent=1)
    manifest = {"contentVersion": CV, "generated": REVIEWED, "categories": CATEGORIES,
                "scores": [{"id": s["id"], "name": s["name"], "abbreviation": s["abbreviation"], "aliases": s.get("aliases", []),
                            "category": s["category"], "version": s["version"]["label"]} for s in scores]}
    with open(os.path.join(out, "manifest.json"), "w") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    print("wrote", len(scores), "scores")
