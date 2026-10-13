"""Insula Neuro Score — v0.12: neurotrauma decision rules, spine and neuro-oncology grades (licence-free)."""
from library import o, single, yn, st, conf, score
from library4 import mk, C, levels, select_states

RULE = lambda label: {"type": "decision-rule", "typeLabel": label, "meter": False}

def build():
    L = []
    # =====================================================================================  NEUROTRAUMA RULES
    applies_ct = single("applies", "Does the rule apply?", "Applies", [o("yes", "Yes: minor head injury in the rule's population", 1, "yes",
                         "Blunt head injury with witnessed loss of consciousness, definite amnesia or witnessed disorientation; GCS 13–15; age 16 or over."),
                         o("no", "No: outside the rule", 0, "no", "e.g. age under 16, GCS under 13, anticoagulation or bleeding disorder, obvious open skull fracture, no loss of consciousness/amnesia/disorientation.")])
    hi = [("h1", "GCS below 15 at 2 hours after injury", "GCS <15 at 2 h"), ("h2", "Suspected open or depressed skull fracture", "Open/depressed fracture"), ("h3", "Any sign of basal skull fracture", "Basal skull fracture", "Haemotympanum, 'raccoon' eyes, CSF otorrhoea or rhinorrhoea, Battle's sign."),
          ("h4", "Vomiting two or more episodes", "Vomiting ≥2"), ("h5", "Age 65 or older", "Age ≥65")]
    md = [("m1", "Amnesia before impact of 30 minutes or more", "Amnesia ≥30 min"), ("m2", "Dangerous mechanism", "Dangerous mechanism", "Pedestrian struck by a motor vehicle, occupant ejected from a vehicle, or fall from over 3 feet or 5 stairs.")]
    L.append(mk(id="cchr", name="Canadian CT Head Rule", abbreviation="Canadian CT Head", aliases=["canadian ct head", "cchr", "ct head rule", "minor head injury", "head ct"],
        category="tbi", subcategory="Imaging decision rule", specialties=["Emergency Medicine", "Neurosurgery", "Trauma"],
        version={"label": "Canadian CT Head Rule (Stiell et al. 2001)", "detail": "Five high-risk factors (for neurosurgical intervention) and two medium-risk factors (for brain injury on CT) in adults with minor head injury and GCS 13–15."},
        purpose="Identifies adults with minor head injury in whom the rule's criteria for CT are met.", intendedPopulation="Adults (16+) with blunt minor head injury, GCS 13–15, and witnessed LOC, definite amnesia or witnessed disorientation.",
        resultPresentation=RULE("Decision rule result"),
        calculatorNotice={"tone": "warning", "title": "Check that the rule applies", "message": "The rule was not derived for children, GCS below 13, anticoagulated patients or obvious open skull fracture. Local protocols may differ (e.g. for anticoagulation)."},
        inputDefinitions=[applies_ct] + [yn(x[0], x[1], x[2], yes="Yes", no="No", help=(x[3] if len(x) > 3 else None)) for x in hi + md],
        components=[{"id": "c_app", "label": "Applicability", "inputs": ["applies"]}, {"id": "high", "label": "High-risk factors", "inputs": [x[0] for x in hi]}, {"id": "medium", "label": "Medium-risk factors", "inputs": [x[0] for x in md]}],
        calculationMethod={"type": "expression", "expression": "applies == 0 ? 0 : (high > 0 ? 3 : (medium > 0 ? 2 : 1))", "range": {"min": 0, "max": 3},
                           "display": "{total == 0 ? 'Not applicable' : total == 3 ? 'High risk' : total == 2 ? 'Medium risk' : 'No risk factor'}", "formulaEquals": False,
                           "share": "Canadian CT Head Rule: {total == 0 ? 'rule not applicable' : total == 3 ? 'high-risk factor present' : total == 2 ? 'medium-risk factor present' : 'no risk factors'}"},
        interpretationRules=[{"when": "total == 0", "state": "na"}, {"when": "total == 3", "state": "high"}, {"when": "total == 2", "state": "med"}, {"state": "none"}],
        resultStates=[st("na", "informational", "Rule not applicable", "The patient is outside the population in which the rule was derived.", None, "Use clinical judgement and local protocol."),
                      st("high", "high", "High-risk factor present", "At least one high-risk factor (risk of needing neurosurgical intervention). The rule's criteria for CT are met.", None, "Assess according to the clinical situation and local protocol."),
                      st("med", "moderate", "Medium-risk factor present", "A medium-risk factor (risk of brain injury on CT) without a high-risk factor. The rule's criteria for CT are met.", None),
                      st("none", "low", "No rule risk factor", "None of the seven factors is present: the rule's criteria for CT are not met.", None, "Clinical judgement and observation still apply; the rule does not exclude injury.")],
        clinicalContext=[C("Highly sensitive for injuries needing neurosurgical intervention in its derivation and validation cohorts.", True), C("An imaging decision aid, not a substitute for clinical assessment.")],
        clinicalInsights=[{"when": "h5 == 1", "text": "Age 65 or older is a high-risk factor on its own."}, {"text": "Document the GCS at 2 hours after injury, not only on arrival."}],
        limitations=[C("Applies only to its derivation population; not to children, anticoagulated patients or GCS below 13.", True), "Requires reliable history of LOC, amnesia and mechanism.", "Local guidelines (e.g. NICE) use different criteria."],
        confounders=conf(("Intoxication", "Makes GCS and amnesia unreliable."), ("Anticoagulation", "Outside the rule; risk of haemorrhage is higher.")),
        whatItDoesNotTellYou=["Whether CT will show injury.", "Need for admission or observation.", "C-spine status (see Canadian C-spine Rule)."],
        commonErrors=["Applying the rule to anticoagulated patients or children.", "Using the arrival GCS instead of the 2-hour GCS."],
        relatedScores=[], guideSections={"what": "A decision rule with five high-risk and two medium-risk factors for CT after minor head injury.", "whenToUse": "Adults with minor head injury (GCS 13–15) and LOC, amnesia or disorientation.",
            "howToPerform": "Confirm the rule applies. Check each high-risk and medium-risk factor. Any factor present meets the rule's criteria for CT.", "clinicalContext": "Supports, but does not replace, clinical judgement and local protocol."},
        sources=[{"citation": "Stiell IG, Wells GA, Vandemheen K, et al. The Canadian CT Head Rule for patients with minor head injury. Lancet. 2001;357(9266):1391-1396."}],
        licensing={"status": "Published decision rule with attribution", "note": "No reproduction restrictions identified."}))

    # ---------------------------------------------------------------- NEXUS
    nx = [("t", "Posterior midline cervical spine tenderness", "Midline tenderness"), ("f", "Focal neurological deficit", "Focal deficit"), ("a", "Altered level of alertness", "Altered alertness"), ("i", "Evidence of intoxication", "Intoxication"), ("d", "Painful distracting injury", "Distracting injury")]
    L.append(mk(id="nexus", name="NEXUS Low-Risk Criteria (cervical spine)", abbreviation="NEXUS", aliases=["nexus", "c-spine", "cervical spine imaging", "neck injury"],
        category="spine", subcategory="Spine trauma imaging rule", specialties=["Emergency Medicine", "Trauma", "Spine Surgery", "Neurosurgery"],
        version={"label": "NEXUS low-risk criteria (Hoffman et al. 2000)", "detail": "Five criteria; imaging was considered unnecessary only when all five were met. The criteria terms were deliberately left without strict definitions."},
        purpose="Identifies blunt trauma patients at low risk of cervical spine injury.", intendedPopulation="Patients with blunt trauma being considered for cervical spine imaging.",
        resultPresentation=RULE("Decision rule result"),
        inputDefinitions=[yn(i, lab, sh, yes="Present", no="Absent") for i, lab, sh in nx],
        components=[{"id": "crit", "label": "NEXUS criteria (each must be absent)", "inputs": [x[0] for x in nx]}],
        calculationMethod={"type": "expression", "expression": "crit > 0 ? 1 : 0", "range": {"min": 0, "max": 1}, "display": "{total == 0 ? 'Low risk' : 'Not low risk'}", "share": "NEXUS: {total == 0 ? 'all five low-risk criteria met' : (crit == 1 ? '1 criterion present' : crit + ' criteria present')}"},
        interpretationRules=[{"when": "total == 0", "state": "low"}, {"state": "not"}],
        resultStates=[st("low", "low", "All five low-risk criteria met", "No tenderness, deficit, altered alertness, intoxication or distracting injury.", None, "In the derivation study imaging was considered unnecessary; clinical judgement still applies."),
                      st("not", "moderate", "Not all criteria met", "One or more NEXUS criteria present: the rule's criteria for imaging are met.", None)],
        clinicalContext=[C("High sensitivity for clinically significant cervical spine injury in the derivation cohort.", True)],
        clinicalInsights=[{"text": "The Canadian C-spine Rule had higher specificity in a head-to-head comparison; local protocols choose one."}],
        limitations=[C("Criteria terms are subjective (e.g. distracting injury), which reduces reliability.", True), "Lower sensitivity reported in older adults in some studies."],
        confounders=conf(("Intoxication", "Makes examination unreliable."), ("Communication barriers", "Limit tenderness and neurological assessment.")),
        whatItDoesNotTellYou=["Which imaging modality to use.", "Ligamentous injury without bony injury."], commonErrors=["Scoring paraspinal tenderness as midline tenderness."],
        guideSections={"what": "Five clinical criteria; when all are absent the patient is low risk for cervical spine injury.", "whenToUse": "Blunt trauma patients considered for cervical spine imaging.",
            "howToPerform": "Assess each criterion; if any is present the rule's imaging criteria are met.", "clinicalContext": "Supports, but does not replace, clinical judgement."},
        sources=[{"citation": "Hoffman JR, Mower WR, Wolfson AB, Todd KH, Zucker MI. Validity of a set of clinical criteria to rule out injury to the cervical spine in patients with blunt trauma. N Engl J Med. 2000;343(2):94-99."}],
        licensing={"status": "Published decision rule with attribution", "note": "No reproduction restrictions identified."}))

    # ---------------------------------------------------------------- Canadian C-spine Rule
    hr = [("age65", "Age 65 or older", "Age ≥65"), ("mech", "Dangerous mechanism", "Dangerous mechanism", "Fall from 3 feet / 1 m or 5 stairs; axial load to the head; motor vehicle collision at high speed (>100 km/h), rollover or ejection; motorised recreational vehicle; bicycle collision."),
          ("par", "Paraesthesias in the extremities", "Paraesthesias")]
    lr = [("rear", "Simple rear-end motor vehicle collision", "Simple rear-end MVC", "Excludes being pushed into oncoming traffic, hit by a bus or large truck, rollover, or hit by a high-speed vehicle."), ("sit", "Sitting position in the emergency department", "Sitting in ED"),
          ("amb", "Ambulatory at any time since injury", "Ambulatory"), ("delay", "Delayed onset of neck pain", "Delayed neck pain"), ("nomid", "Absence of midline cervical spine tenderness", "No midline tenderness")]
    L.append(mk(id="ccsr", name="Canadian C-spine Rule", abbreviation="Canadian C-spine", aliases=["canadian c-spine", "ccsr", "c-spine rule", "cervical spine imaging", "neck injury"],
        category="spine", subcategory="Spine trauma imaging rule", specialties=["Emergency Medicine", "Trauma", "Spine Surgery", "Neurosurgery"],
        version={"label": "Canadian C-spine Rule (Stiell et al. 2001)", "detail": "Three steps: any high-risk factor → radiography; no low-risk factor → radiography; low-risk factor present → assess active rotation 45° left and right; unable → radiography."},
        purpose="Identifies alert, stable trauma patients in whom the rule's criteria for cervical spine imaging are met.", intendedPopulation="Alert (GCS 15), stable adults (16+) after blunt trauma to the head or neck.",
        resultPresentation=RULE("Decision rule result"),
        calculatorNotice={"tone": "warning", "title": "Check that the rule applies", "message": "Not for children, GCS below 15, unstable vital signs, penetrating trauma, acute paralysis, known vertebral disease or previous cervical spine surgery."},
        inputDefinitions=[single("applies", "Does the rule apply?", "Applies", [o("yes", "Yes: alert, stable adult with blunt head or neck trauma", 1, "yes"), o("no", "No: outside the rule", 0, "no")])] +
                         [yn(x[0], x[1], x[2], yes="Yes", no="No", help=(x[3] if len(x) > 3 else None)) for x in hr + lr] +
                         [dict(single("rot", "Able to actively rotate the neck 45° to the left and right?", "Rotation", [o("no", "Unable", 0, "unable"), o("yes", "Able", 1, "able")]), required=False,
                               help="Only assessed when no high-risk factor and at least one low-risk factor is present.")],
        components=[{"id": "c_app", "label": "Applicability", "inputs": ["applies"]}, {"id": "highrisk", "label": "High-risk factors", "inputs": [x[0] for x in hr]},
                    {"id": "lowrisk", "label": "Low-risk factors", "inputs": [x[0] for x in lr]}, {"id": "c_rot", "label": "Active rotation", "inputs": ["rot"]}],
        calculationMethod={"type": "expression", "expression": "applies == 0 ? 0 : (highrisk > 0 ? 2 : (lowrisk == 0 ? 3 : (isnull(rot) ? 4 : (rot == 0 ? 5 : 1))))", "range": {"min": 0, "max": 5}, "formulaEquals": False,
                           "display": "{total == 0 ? 'Not applicable' : total == 1 ? 'Rule criteria not met' : total == 4 ? 'Assess rotation' : 'Rule criteria met'}",
                           "share": "Canadian C-spine Rule: {total == 0 ? 'not applicable' : total == 1 ? 'low risk, able to rotate 45°' : total == 2 ? 'high-risk factor' : total == 3 ? 'no low-risk factor' : total == 4 ? 'rotation not yet assessed' : 'unable to rotate 45°'}"},
        consistencyRules=[{"when": "highrisk > 0 && !isnull(rot)", "severity": "warning", "inputs": ["rot"], "message": "Rotation is not assessed when a high-risk factor is present."},
                          {"when": "applies == 1 && highrisk == 0 && lowrisk == 0 && !isnull(rot)", "severity": "warning", "inputs": ["rot"], "message": "Rotation is only assessed when at least one low-risk factor allows safe assessment."}],
        interpretationRules=[{"when": "total == 0", "state": "na"}, {"when": "total == 2", "state": "high"}, {"when": "total == 3", "state": "nolow"}, {"when": "total == 4", "state": "rot"}, {"when": "total == 5", "state": "unable"}, {"state": "clear"}],
        resultStates=[st("na", "informational", "Rule not applicable", "The patient is outside the population in which the rule was derived.", None, "Use clinical judgement and local protocol."),
                      st("high", "high", "High-risk factor present", "A high-risk factor is present: the rule's criteria for radiography are met.", None, "Assess according to the clinical situation and local protocol."),
                      st("nolow", "moderate", "No low-risk factor", "No low-risk factor allows safe assessment of range of motion: the rule's criteria for radiography are met.", None),
                      st("rot", "incomplete", "Assess active rotation", "A low-risk factor is present. Assess whether the patient can actively rotate the neck 45° left and right.", None),
                      st("unable", "moderate", "Unable to rotate 45°", "Unable to actively rotate the neck 45° left and right: the rule's criteria for radiography are met.", None),
                      st("clear", "low", "Rule criteria not met", "No high-risk factor, a low-risk factor present and able to rotate 45° left and right: the rule's criteria for radiography are not met.", None, "Clinical judgement still applies.")],
        clinicalContext=[C("High sensitivity and better specificity than NEXUS in the head-to-head validation study.", True)],
        clinicalInsights=[{"text": "Active rotation is assessed only after a low-risk factor makes it safe."}],
        limitations=[C("Only for alert, stable adults; excluded groups need clinical judgement.", True), "Requires an accurate mechanism history."],
        confounders=conf(("Intoxication or reduced alertness", "Outside the rule."), ("Distracting injuries", "Can make examination unreliable.")),
        whatItDoesNotTellYou=["Which imaging modality to use.", "Ligamentous injury without bony injury.", "Head injury risk (see Canadian CT Head Rule)."],
        commonErrors=["Testing rotation before excluding high-risk factors.", "Applying to patients with GCS below 15."],
        guideSections={"what": "A three-step rule for cervical spine radiography in alert, stable trauma patients.", "whenToUse": "Alert (GCS 15), stable adults after blunt head or neck trauma.",
            "howToPerform": "1) Any high-risk factor → criteria met. 2) If no low-risk factor → criteria met. 3) Otherwise ask the patient to rotate 45° each way; unable → criteria met.", "clinicalContext": "Supports, but does not replace, clinical judgement."},
        sources=[{"citation": "Stiell IG, Wells GA, Vandemheen KL, et al. The Canadian C-spine rule for radiography in alert and stable trauma patients. JAMA. 2001;286(15):1841-1848."},
                 {"citation": "Stiell IG, Clement CM, McKnight RD, et al. The Canadian C-spine rule versus the NEXUS low-risk criteria in patients with trauma. N Engl J Med. 2003;349(26):2510-2518."}],
        licensing={"status": "Published decision rule with attribution", "note": "No reproduction restrictions identified."}))

    # =====================================================================================  SPINE TRAUMA
    L.append(mk(id="slic", name="Subaxial Cervical Spine Injury Classification (SLIC)", abbreviation="SLIC", aliases=["slic", "subaxial", "cervical spine injury", "c3-c7 injury"],
        category="spine", subcategory="Spine trauma", specialties=["Spine Surgery", "Neurosurgery", "Trauma"],
        version={"label": "SLIC (Vaccaro et al. 2007)", "detail": "Morphology 0–4 + discoligamentous complex 0–2 + neurological status 0–3, plus 1 for continuous cord compression with a neurological deficit. Total 0–10."},
        purpose="Classifies subaxial (C3–C7) cervical spine injuries and summarises features relevant to management.", intendedPopulation="Adults with subaxial cervical spine trauma, using CT, MRI and neurological examination.",
        resultPresentation={"type": "classification", "typeLabel": "Injury severity", "meter": True},
        calculatorNotice={"tone": "info", "title": "Classification, not a surgical decision", "message": "The authors proposed treatment thresholds; management also depends on the patient, associated injuries and surgeon judgement."},
        inputDefinitions=[single("morph", "Morphology", "Morphology", [o("none", "No abnormality", 0), o("comp", "Compression (including endplate or vertical body fracture)", 1), o("burst", "Burst", 2),
                                                                        o("dist", "Distraction (e.g. facet perch, hyperextension)", 3), o("rot", "Rotation or translation (e.g. facet dislocation, unstable teardrop)", 4)], help="Score the most severe morphology at the level."),
                          single("dlc", "Discoligamentous complex", "DLC", [o("intact", "Intact", 0), o("indet", "Indeterminate (e.g. isolated interspinous widening, MRI signal change only)", 1), o("disr", "Disrupted (e.g. widened disc space, facet perch or dislocation)", 2)]),
                          single("neuro", "Neurological status", "Neuro", [o("intact", "Intact", 0), o("root", "Root injury", 1), o("complete", "Complete cord injury", 2), o("incomplete", "Incomplete cord injury", 3)]),
                          yn("ccc", "Continuous cord compression with a neurological deficit", "Compression +1", yes="Yes", no="No")],
        calculationMethod={"type": "sum", "range": {"min": 0, "max": 10}, "display": "{total}", "share": "SLIC {total} (morphology {morph}, DLC {dlc}, neuro {neuro}{ccc == 1 ? ' +1' : ''})"},
        consistencyRules=[{"when": "ccc == 1 && neuro == 0", "severity": "warning", "inputs": ["ccc"], "message": "The +1 modifier applies to continuous cord compression in the setting of a neurological deficit."}],
        interpretationRules=[{"when": "total <= 3", "state": "low"}, {"when": "total == 4", "state": "mid"}, {"state": "high"}],
        resultStates=[st("low", "low", "SLIC {total}", "Score 0–3: the authors' non-operative range.", "0–3", None, 0, 3),
                      st("mid", "moderate", "SLIC 4", "Score 4: indeterminate in the authors' scheme.", "4", "Management depends on patient and injury factors.", 4, 4),
                      st("high", "high", "SLIC {total}", "Score 5 or more: the authors' operative range.", "5–10", "Management depends on neurological status, associated injuries, patient factors and surgical judgement.", 5, 10)],
        clinicalContext=[C("Combines injury morphology, ligamentous integrity and neurology, the three features that drive management.", True)],
        clinicalInsights=[{"when": "neuro == 3", "text": "Incomplete cord injury scores higher than complete because decompression may improve it."}],
        limitations=[C("Proposed thresholds are not a substitute for surgical judgement.", True), "DLC assessment on MRI is variably interpreted.", "Not for C1–C2 injuries."],
        confounders=conf(("Pre-existing spondylosis or ankylosing spondylitis", "Changes injury behaviour."), ("Incomplete imaging", "Affects DLC assessment.")),
        whatItDoesNotTellYou=["The surgical approach.", "Prognosis for neurological recovery."], commonErrors=["Scoring several morphologies instead of the most severe.", "Applying the +1 modifier without a deficit."],
        guideSections={"what": "A 0–10 score from morphology, discoligamentous complex and neurology for C3–C7 injuries.", "whenToUse": "Subaxial cervical spine trauma.",
            "howToPerform": "Score the most severe morphology, the DLC and the neurological status; add 1 for continuous cord compression with a deficit.", "clinicalContext": "A classification that supports management decisions made with the full clinical picture."},
        sources=[{"citation": "Vaccaro AR, Hulbert RJ, Patel AA, et al. The subaxial cervical spine injury classification system: a novel approach to recognize the importance of morphology, neurology, and integrity of the disco-ligamentous complex. Spine. 2007;32(21):2365-2374."}],
        licensing={"status": "Published classification with attribution", "note": "No reproduction restrictions identified."}))

    L.append(mk(id="tlics", name="Thoracolumbar Injury Classification and Severity Score (TLICS)", abbreviation="TLICS", aliases=["tlics", "thoracolumbar injury", "burst fracture", "spine fracture"],
        category="spine", subcategory="Spine trauma", specialties=["Spine Surgery", "Neurosurgery", "Trauma"],
        version={"label": "TLICS (Vaccaro et al. 2005)", "detail": "Morphology 1–4 + posterior ligamentous complex 0–3 + neurological status 0–3. Total 1–10. The AO Spine thoracolumbar classification is a separate (licensed) system."},
        purpose="Classifies thoracolumbar injuries and summarises features relevant to management.", intendedPopulation="Adults with thoracolumbar spine trauma, using CT, MRI and neurological examination.",
        resultPresentation={"type": "classification", "typeLabel": "Injury severity", "meter": True},
        calculatorNotice={"tone": "info", "title": "Classification, not a surgical decision", "message": "The authors proposed treatment thresholds; management also depends on the patient, associated injuries and surgeon judgement."},
        inputDefinitions=[single("morph", "Morphology", "Morphology", [o("comp", "Compression", 1), o("burst", "Burst", 2), o("trans", "Translation or rotation", 3), o("dist", "Distraction", 4)], help="Score the most severe morphology."),
                          single("plc", "Posterior ligamentous complex", "PLC", [o("intact", "Intact", 0), o("indet", "Suspected or indeterminate", 2), o("inj", "Injured", 3)]),
                          single("neuro", "Neurological status", "Neuro", [o("intact", "Intact", 0), o("root", "Nerve root", 2), o("complete", "Cord or conus medullaris: complete", 2, "2 (complete)"),
                                                                            o("incomplete", "Cord or conus medullaris: incomplete", 3, "3 (incomplete)"), o("ce", "Cauda equina", 3, "3 (CE)")])],
        calculationMethod={"type": "sum", "range": {"min": 1, "max": 10}, "display": "{total}", "share": "TLICS {total} (morphology {morph}, PLC {plc}, neuro {neuro})"},
        interpretationRules=[{"when": "total <= 3", "state": "low"}, {"when": "total == 4", "state": "mid"}, {"state": "high"}],
        resultStates=[st("low", "low", "TLICS {total}", "Score 0–3: the authors' non-operative range.", "1–3", None, 1, 3),
                      st("mid", "moderate", "TLICS 4", "Score 4: either approach in the authors' scheme.", "4", "Management depends on patient and injury factors.", 4, 4),
                      st("high", "high", "TLICS {total}", "Score 5 or more: the authors' operative range.", "5–10", "Management depends on neurological status, associated injuries, patient factors and surgical judgement.", 5, 10)],
        clinicalContext=[C("Combines morphology, PLC integrity and neurology to classify thoracolumbar injuries.", True)],
        clinicalInsights=[{"when": "neuro_value == 'incomplete'", "text": "Incomplete cord/conus injury scores higher (3) than complete (2), reflecting potential benefit from decompression."}],
        limitations=[C("Proposed thresholds are not a substitute for surgical judgement.", True), "PLC assessment varies between readers.", "Does not include patient factors such as bone quality."],
        confounders=conf(("Osteoporosis", "Changes injury pattern and treatment."), ("Incomplete MRI", "Leaves PLC indeterminate.")),
        whatItDoesNotTellYou=["The surgical approach.", "Prognosis for recovery."], commonErrors=["Scoring complete cord injury as 3 (it is 2).", "Adding several morphologies."],
        guideSections={"what": "A score from morphology, PLC integrity and neurology for thoracolumbar injuries.", "whenToUse": "Thoracolumbar spine trauma.",
            "howToPerform": "Score the most severe morphology, the PLC and neurology; sum.", "clinicalContext": "Supports management decisions made with the full clinical picture."},
        sources=[{"citation": "Vaccaro AR, Lehman RA Jr, Hurlbert RJ, et al. A new classification of thoracolumbar injuries: the importance of injury morphology, the integrity of the posterior ligamentous complex, and neurologic status. Spine. 2005;30(20):2325-2333."}],
        licensing={"status": "Published classification with attribution", "note": "No reproduction restrictions identified."}))

    ad = [("I", "Odontoid tip", "Oblique avulsion fracture through the tip of the dens."), ("II", "Base of the dens", "Fracture at the junction of the dens and the body of C2."), ("III", "Body of C2", "Fracture extending into the body of C2.")]
    r, s = select_states([(c, "informational", "Type %s: %s" % (c, lab.lower()), det, None) for c, lab, det in ad])
    L.append(mk(id="andersondalonzo", name="Anderson and D'Alonzo Classification of Odontoid Fractures", abbreviation="Anderson-D'Alonzo", aliases=["odontoid fracture", "dens fracture", "anderson dalonzo", "c2 fracture"],
        category="spine", subcategory="Spine trauma", specialties=["Spine Surgery", "Neurosurgery", "Trauma"],
        version={"label": "Anderson and D'Alonzo (1974), types I–III", "detail": "Grauer's subdivision of type II (IIA–IIC) is a later modification and is not combined."},
        purpose="Classifies odontoid (dens) fractures by level.", intendedPopulation="Patients with odontoid fractures on CT.", resultPresentation={"type": "imaging-classification", "typeLabel": "Fracture type", "meter": False},
        inputDefinitions=[levels("t", "Fracture level", "Type", ad)],
        calculationMethod={"type": "select", "input": "t", "range": {"min": 1, "max": 3}, "display": "Type {t_code}", "share": "Odontoid fracture type {t_code} (Anderson-D'Alonzo)"},
        interpretationRules=r, resultStates=s,
        clinicalContext=[C("Type II fractures have the highest non-union risk, especially with displacement, comminution or older age.", True)],
        clinicalInsights=[{"when": "t == 2", "text": "Displacement, angulation, comminution and age influence healing; describe them with the type."}],
        limitations=[C("Describes level only; displacement and stability are described separately.", True), "Distinguishing low type II from shallow type III fractures varies between readers."], confounders=conf(("Os odontoideum", "Can mimic a type II fracture."),),
        whatItDoesNotTellYou=["Stability or the need for fixation on its own."], commonErrors=["Mistaking os odontoideum for an acute fracture."],
        guideSections={"what": "Three types of odontoid fracture by level.", "whenToUse": "C2 dens fractures on CT.", "howToPerform": "Identify the fracture level on sagittal and coronal CT.", "clinicalContext": "Used with displacement, age and comorbidity in management planning."},
        sources=[{"citation": "Anderson LD, D'Alonzo RT. Fractures of the odontoid process of the axis. J Bone Joint Surg Am. 1974;56(8):1663-1674."}],
        licensing={"status": "Published classification with attribution", "note": "No reproduction restrictions identified."}))

    le = [("I", "Minimal displacement", "Fracture through the pars of C2 with displacement under 3 mm and no angulation; C2–3 disc intact."),
          ("II", "Displaced and angulated", "Displacement over 3 mm with significant angulation; C2–3 disc disrupted."),
          ("IIa", "Angulated without translation", "Significant angulation with minimal translation; more horizontal fracture line (flexion-distraction)."),
          ("III", "With facet dislocation", "Type II with bilateral C2–3 facet dislocation.")]
    r, s = select_states([(c, "informational", "Type %s: %s" % (c, lab.lower()), det, None) for c, lab, det in le])
    L.append(mk(id="levineedwards", name="Levine and Edwards Classification of Hangman's Fractures", abbreviation="Levine-Edwards", aliases=["hangman fracture", "traumatic spondylolisthesis of the axis", "levine edwards", "c2 pars fracture"],
        category="spine", subcategory="Spine trauma", specialties=["Spine Surgery", "Neurosurgery", "Trauma"],
        version={"label": "Levine and Edwards (1985), types I, II, IIa, III", "detail": "Modification of the Effendi classification of traumatic spondylolisthesis of the axis."},
        purpose="Classifies traumatic spondylolisthesis of C2 (hangman's fracture).", intendedPopulation="Patients with C2 pars fractures on CT.", resultPresentation={"type": "imaging-classification", "typeLabel": "Fracture type", "meter": False},
        inputDefinitions=[levels("t", "Fracture pattern", "Type", le)],
        calculationMethod={"type": "select", "input": "t", "range": {"min": 1, "max": 4}, "display": "Type {t_code}", "share": "Hangman's fracture type {t_code} (Levine-Edwards)"},
        interpretationRules=r, resultStates=s,
        clinicalContext=[C("Distinguishes stable (type I) from unstable patterns; type IIa should not be treated with traction.", True)],
        clinicalInsights=[{"when": "t == 4", "text": "Facet dislocation (type III) usually needs open reduction."}, {"when": "t == 3", "text": "Type IIa has a flexion-distraction pattern; traction can widen it."}],
        limitations=[C("Displacement and angulation are judged on lateral imaging; thresholds vary between reports.", True), "Atypical patterns (e.g. fractures through the posterior body) do not fit the types well."], confounders=conf(("Patient positioning", "Changes apparent displacement."),),
        whatItDoesNotTellYou=["Neurological status."], commonErrors=["Missing type IIa, which behaves differently under traction."],
        guideSections={"what": "Four types of hangman's fracture by displacement, angulation and facet dislocation.", "whenToUse": "C2 pars fractures.", "howToPerform": "Assess translation, angulation, fracture orientation and the C2–3 facets.", "clinicalContext": "Guides stability assessment with the full clinical picture."},
        sources=[{"citation": "Levine AM, Edwards CC. The management of traumatic spondylolisthesis of the axis. J Bone Joint Surg Am. 1985;67(2):217-226."}],
        licensing={"status": "Published classification with attribution", "note": "No reproduction restrictions identified."}))

    # =====================================================================================  DEGENERATIVE SPINE
    pf = [("I", "Homogeneous, bright white; clear nucleus–annulus distinction; normal height."), ("II", "Inhomogeneous, with or without horizontal bands; clear distinction; normal height."),
          ("III", "Inhomogeneous, grey; distinction unclear; height normal or slightly decreased."), ("IV", "Inhomogeneous, grey to black; distinction lost; height normal to moderately decreased."),
          ("V", "Inhomogeneous, black; distinction lost; disc space collapsed.")]
    r, s = select_states([(c, "informational", "Grade %s" % c, det, None) for c, det in pf])
    L.append(mk(id="pfirrmann", name="Pfirrmann Grading of Disc Degeneration", abbreviation="Pfirrmann", aliases=["pfirrmann", "disc degeneration", "disc desiccation"],
        category="spine", subcategory="Degenerative spine imaging", specialties=["Spine Surgery", "Neurosurgery", "Radiology"],
        version={"label": "Pfirrmann et al. (2001), grades I–V", "detail": "Lumbar discs on T2-weighted MRI. The 8-level modified grading (Griffith et al. 2007) is a different system."},
        purpose="Grades lumbar intervertebral disc degeneration on T2-weighted MRI.", intendedPopulation="Patients with lumbar spine MRI.", resultPresentation={"type": "imaging-classification", "typeLabel": "Disc grade", "meter": False},
        inputDefinitions=[levels("g", "Disc appearance on T2 MRI", "Grade", [(c, "Grade " + c, det) for c, det in pf])],
        calculationMethod={"type": "select", "input": "g", "range": {"min": 1, "max": 5}, "display": "Grade {g_code}", "share": "Pfirrmann grade {g_code}"},
        interpretationRules=r, resultStates=s,
        clinicalContext=[C("Describes disc degeneration; degeneration is common without symptoms.", True)], clinicalInsights=[{"text": "Grade each level separately."}],
        limitations=[C("Imaging findings correlate poorly with pain.", True), "Reliability lower between grades III and IV."], confounders=conf(("Field strength and sequence", "Change signal appearance."),),
        whatItDoesNotTellYou=["The source of pain.", "Need for intervention."], commonErrors=["Grading on T1-weighted images."],
        guideSections={"what": "Five grades of disc degeneration from signal, structure, nucleus–annulus distinction and height.", "whenToUse": "Lumbar MRI reporting and research.", "howToPerform": "On mid-sagittal T2 images assess each disc and choose the grade.", "clinicalContext": "Correlate with symptoms and examination."},
        sources=[{"citation": "Pfirrmann CWA, Metzdorf A, Zanetti M, Hodler J, Boos N. Magnetic resonance classification of lumbar intervertebral disc degeneration. Spine. 2001;26(17):1873-1878."}],
        licensing={"status": "Published grading with attribution", "note": "No reproduction restrictions identified."}))

    md_ = [("1", "Type 1: oedema / inflammation", "Low T1 and high T2 signal in the vertebral endplate and marrow."), ("2", "Type 2: fatty replacement", "High T1 and iso- to high T2 signal."), ("3", "Type 3: sclerosis", "Low T1 and low T2 signal.")]
    r, s = select_states([(c, "informational", lab, det, None) for c, lab, det in md_])
    L.append(mk(id="modic", name="Modic Endplate Changes", abbreviation="Modic", aliases=["modic", "endplate changes", "vertebral endplate"],
        category="spine", subcategory="Degenerative spine imaging", specialties=["Spine Surgery", "Neurosurgery", "Radiology"],
        version={"label": "Modic et al. (1988), types 1–3", "detail": "Classified by T1 and T2 signal of the endplate and adjacent marrow. Mixed types (e.g. 1/2) are described as such."},
        purpose="Classifies degenerative vertebral endplate and marrow signal changes on MRI.", intendedPopulation="Patients with spine MRI.", resultPresentation={"type": "imaging-classification", "typeLabel": "Endplate change type", "meter": False},
        inputDefinitions=[levels("t", "Signal pattern", "Type", md_)],
        calculationMethod={"type": "select", "input": "t", "range": {"min": 1, "max": 3}, "display": "Modic type {t_code}", "share": "Modic type {t_code}"},
        interpretationRules=r, resultStates=s,
        clinicalContext=[C("Type 1 changes are the most often associated with low back pain.", True)], clinicalInsights=[{"when": "t == 1", "text": "Type 1 changes can resemble infection; correlate clinically and with the disc."}],
        limitations=[C("Signal change is not specific; discitis and tumour must be considered in the right context.", True), "Changes can convert between types over time."], confounders=conf(("Infection", "Can mimic type 1."),),
        whatItDoesNotTellYou=["The cause of pain."], commonErrors=["Calling discitis a Modic type 1 change without considering the clinical picture."],
        guideSections={"what": "Three types of endplate marrow change by T1/T2 signal.", "whenToUse": "Spine MRI reporting.", "howToPerform": "Compare endplate marrow signal on T1 and T2 with normal marrow; choose the type.", "clinicalContext": "Correlate with symptoms; consider infection when appropriate."},
        sources=[{"citation": "Modic MT, Steinberg PM, Ross JS, Masaryk TJ, Carter JR. Degenerative disk disease: assessment of changes in vertebral body marrow with MR imaging. Radiology. 1988;166(1):193-199."}],
        licensing={"status": "Published classification with attribution", "note": "No reproduction restrictions identified."}))

    my = [("I", "Up to 25% slip", None), ("II", "26–50% slip", None), ("III", "51–75% slip", None), ("IV", "76–100% slip", None), ("V", "Over 100% (spondyloptosis)", None)]
    r, s = select_states([(c, "informational", "Grade %s" % c, lab + " of the vertebral body width.", None) for c, lab, _ in my])
    L.append(mk(id="meyerding", name="Meyerding Grading of Spondylolisthesis", abbreviation="Meyerding", aliases=["meyerding", "spondylolisthesis", "listhesis", "spondyloptosis"],
        category="spine", subcategory="Degenerative spine imaging", specialties=["Spine Surgery", "Neurosurgery", "Radiology"],
        version={"label": "Meyerding (1932), grades I–V", "detail": "Slip of the superior vertebra relative to the inferior, as a percentage of the inferior vertebral body's anteroposterior width. Grade V (spondyloptosis) was added later and is widely used."},
        purpose="Grades the degree of vertebral slip in spondylolisthesis.", intendedPopulation="Patients with spondylolisthesis on lateral radiograph, CT or MRI.", resultPresentation={"type": "imaging-classification", "typeLabel": "Slip grade", "meter": False},
        inputDefinitions=[levels("g", "Percentage slip", "Grade", [(c, lab, None) for c, lab, _ in my])],
        calculationMethod={"type": "select", "input": "g", "range": {"min": 1, "max": 5}, "display": "Grade {g_code}", "share": "Meyerding grade {g_code}"},
        interpretationRules=r, resultStates=s,
        clinicalContext=[C("Grades I–II are 'low grade' and III–V 'high grade' in common usage.", True)], clinicalInsights=[{"text": "Flexion-extension films show dynamic instability, which the grade does not."}],
        limitations=[C("Static measure; does not show instability or slip angle.", True), "Measurement varies with positioning (supine MRI may under-show slip)."], confounders=conf(("Supine imaging", "Can reduce the apparent slip."),),
        whatItDoesNotTellYou=["Symptoms or nerve compression.", "Stability."], commonErrors=["Measuring against the slipped vertebra instead of the one below."],
        guideSections={"what": "Five grades of slip by percentage of the inferior vertebral body width.", "whenToUse": "Spondylolisthesis on imaging.", "howToPerform": "Divide the inferior endplate into quarters; note where the posterior corner of the superior vertebra lies.", "clinicalContext": "Used with symptoms, dynamic films and slip angle."},
        sources=[{"citation": "Meyerding HW. Spondylolisthesis. Surg Gynecol Obstet. 1932;54:371-377."}],
        licensing={"status": "Published grading with attribution", "note": "No reproduction restrictions identified."}))

    sc = [("A1", "low", "Rootlets dorsal, occupying less than half of the dural sac", "No or minor stenosis."),
          ("A2", "low", "Rootlets dorsal, contacting the dura in a horseshoe configuration", "No or minor stenosis."),
          ("A3", "low", "Rootlets dorsal, occupying more than half of the dural sac", "No or minor stenosis."),
          ("A4", "low", "Rootlets central, occupying most of the dural sac", "No or minor stenosis."),
          ("B", "moderate", "Rootlets occupy the whole sac but CSF is still visible between them", "Moderate stenosis."),
          ("C", "high", "No rootlets distinguishable; homogeneous grey sac without CSF; epidural fat present posteriorly", "Severe stenosis."),
          ("D", "high", "As C, with no posterior epidural fat visible", "Extreme stenosis.")]
    r, s = select_states([(c, tone, "Grade %s: %s" % (c, sev.lower().rstrip('.')), lab + ".", ("Correlate with symptoms and examination; imaging severity does not determine management on its own." if tone == "high" else None)) for c, tone, lab, sev in sc])
    L.append(mk(id="schizas", name="Schizas Grading of Lumbar Spinal Stenosis", abbreviation="Schizas", aliases=["schizas", "spinal stenosis", "lumbar stenosis", "canal stenosis"],
        category="spine", subcategory="Degenerative spine imaging", specialties=["Spine Surgery", "Neurosurgery", "Radiology"],
        version={"label": "Schizas et al. (2010), grades A1–A4, B, C, D", "detail": "Morphological grading of the dural sac on axial T2-weighted MRI, based on the rootlet/CSF ratio."},
        purpose="Grades the morphological severity of central lumbar spinal stenosis.", intendedPopulation="Patients with lumbar MRI.", resultPresentation={"type": "imaging-classification", "typeLabel": "Stenosis grade", "meter": False},
        inputDefinitions=[levels("g", "Dural sac appearance (axial T2)", "Grade", [(c, "%s: %s" % (c, lab), sev) for c, _, lab, sev in sc])],
        calculationMethod={"type": "select", "input": "g", "range": {"min": 1, "max": 7}, "display": "Grade {g_code}", "share": "Schizas grade {g_code}"},
        interpretationRules=r, resultStates=s,
        clinicalContext=[C("A morphological grading that does not require measuring the canal area.", True)], clinicalInsights=[{"text": "Grade the most stenotic level; report each level if several are affected."}],
        limitations=[C("Morphology correlates imperfectly with symptoms and walking capacity.", True), "Lateral recess and foraminal stenosis are not graded."], confounders=conf(("Patient position", "Supine MRI may under-show dynamic stenosis."),),
        whatItDoesNotTellYou=["Symptom severity.", "Foraminal stenosis."], commonErrors=["Using sagittal images only."],
        guideSections={"what": "Seven grades of central stenosis from the appearance of rootlets and CSF in the dural sac.", "whenToUse": "Lumbar MRI reporting.", "howToPerform": "On axial T2 at the narrowest level, assess rootlet distribution and CSF; choose the grade.", "clinicalContext": "Correlate with neurogenic claudication and examination."},
        sources=[{"citation": "Schizas C, Theumann N, Burn A, et al. Qualitative grading of severity of lumbar spinal stenosis based on the morphology of the dural sac on magnetic resonance images. Spine. 2010;35(21):1919-1924."}],
        licensing={"status": "Published grading with attribution", "note": "No reproduction restrictions identified."}))

    # =====================================================================================  NEURO-ONCOLOGY
    kz = [("1", "Small intracanalicular tumour", None), ("2", "Small tumour protruding into the cerebellopontine angle; no contact with the brainstem", None),
          ("3", "Tumour occupying the cerebellopontine cistern without brainstem displacement", None), ("4", "Large tumour with brainstem and cranial nerve displacement", None)]
    r, s = select_states([(c, "informational", "Grade %s" % c, lab + ".", None) for c, lab, _ in kz])
    L.append(mk(id="koos", name="Koos Grading of Vestibular Schwannoma", abbreviation="Koos", aliases=["koos", "vestibular schwannoma", "acoustic neuroma", "cpa tumour", "cpa tumor"],
        category="oncology", subcategory="Tumour grading: skull base", specialties=["Neurosurgery", "Otolaryngology", "Radiation Oncology"],
        version={"label": "Koos et al. (1998), grades 1–4", "detail": "Extrameatal extension and relation to the brainstem on MRI."},
        purpose="Grades vestibular schwannoma extension.", intendedPopulation="Patients with vestibular schwannoma on MRI.", resultPresentation={"type": "imaging-classification", "typeLabel": "Tumour grade", "meter": False},
        inputDefinitions=[levels("g", "Tumour extension", "Grade", [(c, "Grade %s: %s" % (c, lab), None) for c, lab, _ in kz])],
        calculationMethod={"type": "select", "input": "g", "range": {"min": 1, "max": 4}, "display": "Koos {g_code}", "share": "Koos grade {g_code}"},
        interpretationRules=r, resultStates=s,
        clinicalContext=[C("Widely used in choosing between observation, radiosurgery and microsurgery for vestibular schwannoma.", True)],
        clinicalInsights=[{"when": "g == 4", "text": "Brainstem compression: correlate with hydrocephalus and cranial nerve function."}],
        limitations=[C("Describes extension, not volume or growth rate.", True), "Boundaries between grades 2 and 3 vary between readers."], confounders=conf(("Cystic tumours", "May behave differently from solid tumours of similar grade."),),
        whatItDoesNotTellYou=["Growth rate.", "Hearing status (see Gardner-Robertson)."], commonErrors=["Grading on CT alone."],
        guideSections={"what": "Four grades of vestibular schwannoma extension.", "whenToUse": "MRI of vestibular schwannoma.", "howToPerform": "Assess intracanalicular versus cisternal extension and brainstem contact or displacement.", "clinicalContext": "Used with growth, hearing and patient factors."},
        sources=[{"citation": "Koos WT, Day JD, Matula C, Levy DI. Neurotopographic considerations in the microsurgical treatment of small acoustic neurinomas. J Neurosurg. 1998;88(3):506-512."}],
        licensing={"status": "Published grading with attribution", "note": "No reproduction restrictions identified."}))

    sp = [("I", "Macroscopically complete removal, including the dural attachment and any abnormal bone", "9% symptomatic recurrence at 10 years in Simpson's series."),
          ("II", "Macroscopically complete removal with coagulation of the dural attachment", "19% in the original series."),
          ("III", "Macroscopically complete removal without resection or coagulation of the dural attachment or extradural extensions", "29% in the original series."),
          ("IV", "Subtotal removal", "39–44% in the original series."),
          ("V", "Simple decompression, with or without biopsy", "High recurrence (small group in the original series).")]
    r, s = select_states([(c, "informational", "Grade %s" % c, lab + ".", "Recurrence: " + rec) for c, lab, rec in sp])
    L.append(mk(id="simpson", name="Simpson Grade of Meningioma Resection", abbreviation="Simpson grade", aliases=["simpson", "meningioma resection", "extent of resection"],
        category="oncology", subcategory="Tumour grading: meningioma", specialties=["Neurosurgery", "Neuro-oncology"],
        version={"label": "Simpson (1957), grades I–V", "detail": "Extent of meningioma resection as judged by the surgeon. Grade 0 (resection with a dural margin) is a later proposal and is not combined."},
        purpose="Describes the extent of meningioma resection.", intendedPopulation="Patients after meningioma surgery.", resultPresentation={"type": "classification", "typeLabel": "Extent of resection", "meter": False},
        inputDefinitions=[levels("g", "Extent of resection", "Grade", [(c, "Grade %s: %s" % (c, lab), None) for c, lab, _ in sp])],
        calculationMethod={"type": "select", "input": "g", "range": {"min": 1, "max": 5}, "display": "Simpson {g_code}", "share": "Simpson grade {g_code}"},
        interpretationRules=r, resultStates=s,
        clinicalContext=[C("Extent of resection is a key predictor of meningioma recurrence; the 1957 series showed rising recurrence with grade.", True)],
        clinicalInsights=[{"text": "Modern series find smaller differences between grades I–III; WHO grade and location also matter."}],
        limitations=[C("Surgeon-reported; postoperative MRI may disagree.", True), "Recurrence figures come from a 1957 single-surgeon series."], confounders=conf(("Tumour location", "Limits achievable grade (e.g. skull base)."),),
        whatItDoesNotTellYou=["WHO tumour grade.", "Need for adjuvant treatment on its own."], commonErrors=["Grading from imaging alone without the operative description."],
        guideSections={"what": "Five grades of meningioma resection.", "whenToUse": "Operative notes and follow-up planning after meningioma surgery.", "howToPerform": "From the operative findings, record removal of tumour, dura and bone; choose the grade.", "clinicalContext": "Used with WHO grade, MRI and location."},
        sources=[{"citation": "Simpson D. The recurrence of intracranial meningiomas after surgical treatment. J Neurol Neurosurg Psychiatry. 1957;20(1):22-39."}],
        licensing={"status": "Published grading with attribution", "note": "No reproduction restrictions identified."}))

    kn = [("0", "Tumour medial to the medial tangent of the intracavernous and supraclinoid ICA", "0% surgically confirmed invasion."),
          ("1", "Tumour extends to, but not beyond, the intercarotid line", "1.5%."),
          ("2", "Tumour extends beyond the intercarotid line but not beyond the lateral tangent", "9.9%."),
          ("3A", "Extension beyond the lateral tangent into the superior cavernous sinus compartment", "26.5%."),
          ("3B", "Extension beyond the lateral tangent into the inferior cavernous sinus compartment", "70.6%."),
          ("4", "Complete encasement of the intracavernous ICA", "100%.")]
    r, s = select_states([(c, "informational", "Grade %s" % c, lab + ".", "Surgically confirmed cavernous sinus invasion (Micko 2015): " + inv) for c, lab, inv in kn], prefix="Grade ")
    L.append(mk(id="knosp", name="Knosp Classification (modified) of Cavernous Sinus Invasion", abbreviation="Knosp", aliases=["knosp", "cavernous sinus invasion", "pituitary adenoma", "pitnet"],
        category="oncology", subcategory="Tumour grading: pituitary", specialties=["Neurosurgery", "Endocrinology", "Neuroradiology"],
        version={"label": "Knosp classification as modified by Micko et al. (2015): 0, 1, 2, 3A, 3B, 4", "detail": "Based on coronal MRI lines (medial tangent, intercarotid line, lateral tangent) of the intracavernous and supraclinoid ICA. The original 1993 grade 3 is subdivided into 3A and 3B."},
        purpose="Grades the likelihood of cavernous sinus invasion by pituitary adenoma.", intendedPopulation="Patients with pituitary macroadenoma on coronal MRI.", resultPresentation={"type": "imaging-classification", "typeLabel": "Invasion grade", "meter": False},
        inputDefinitions=[levels("g", "Lateral extension on coronal MRI", "Grade", [(c, "Grade %s: %s" % (c, lab), None) for c, lab, _ in kn])],
        calculationMethod={"type": "select", "input": "g", "range": {"min": 1, "max": 6}, "display": "Knosp {g_code}", "share": "Knosp grade {g_code}"},
        interpretationRules=r, resultStates=s,
        clinicalContext=[C("Predicts true cavernous sinus invasion and the chance of complete resection.", True)], clinicalInsights=[{"when": "g >= 5", "text": "Grades 3B and 4 have high rates of true invasion; gross total resection is less likely."}],
        limitations=[C("MRI-based; true invasion is confirmed only surgically or histologically.", True), "Grades 2 and 3A show the most inter-rater variability."], confounders=conf(("ICA position and tortuosity", "Alter the reference lines."),),
        whatItDoesNotTellYou=["Hormonal status.", "Suprasellar extension (see Hardy)."], commonErrors=["Mixing the original grade 3 with 3A/3B."],
        guideSections={"what": "Grades 0–4 (with 3A/3B) of lateral extension relative to ICA reference lines.", "whenToUse": "Pituitary adenoma MRI before surgery.", "howToPerform": "On coronal T1 post-contrast, draw the medial tangent, intercarotid line and lateral tangent; grade the tumour's lateral extent.", "clinicalContext": "Used in surgical planning."},
        sources=[{"citation": "Knosp E, Steiner E, Kitz K, Matula C. Pituitary adenomas with invasion of the cavernous sinus space: a magnetic resonance imaging classification compared with surgical findings. Neurosurgery. 1993;33(4):610-617."},
                 {"citation": "Micko ASG, Wöhrer A, Wolfsberger S, Knosp E. Invasion of the cavernous sinus space in pituitary adenomas: endoscopic verification and its correlation with an MRI-based classification. J Neurosurg. 2015;122(4):803-811."}],
        licensing={"status": "Published classification with attribution", "note": "No reproduction restrictions identified."}))

    hs = [("0", "Intrapituitary microadenoma; normal sellar floor"), ("I", "Normal-sized sella with focal asymmetry or bulging of the floor"), ("II", "Enlarged sella with an intact floor"),
          ("III", "Localised erosion or destruction of the sellar floor"), ("IV", "Diffuse destruction of the sellar floor")]
    hx = [("0", "None"), ("A", "Bulges into the suprasellar (chiasmatic) cistern"), ("B", "Reaches or obliterates the recesses of the floor of the third ventricle"),
          ("C", "Large extension displacing the third ventricle up to the foramen of Monro"), ("D", "Intracranial intradural extension into anterior, middle or posterior fossa"), ("E", "Extradural extension into or beneath the cavernous sinus")]
    L.append(mk(id="hardy", name="Hardy Classification of Pituitary Adenomas (modified by Wilson)", abbreviation="Hardy", aliases=["hardy", "hardy-wilson", "pituitary adenoma", "sellar"],
        category="oncology", subcategory="Tumour grading: pituitary", specialties=["Neurosurgery", "Endocrinology", "Neuroradiology"],
        version={"label": "Hardy sellar grades 0–IV with Wilson's extrasellar stages A–E", "detail": "Sellar floor changes (Hardy) and suprasellar/parasellar extension (Wilson's modification). Wording of the extrasellar stages varies between reproductions."},
        purpose="Describes sellar destruction and extrasellar extension of pituitary adenomas.", intendedPopulation="Patients with pituitary adenoma on MRI or CT.", resultPresentation={"type": "imaging-classification", "typeLabel": "Sellar grade and extension", "meter": False},
        inputDefinitions=[levels("g", "Sellar grade", "Grade", [(c, "Grade %s: %s" % (c, lab), None) for c, lab in hs]),
                          single("x", "Extrasellar extension", "Stage", [o(i, ("%s: %s" % (c, lab)) if c != "0" else "None", i, c) for i, (c, lab) in enumerate(hx)])],
        components=[{"id": "c_g", "label": "Sellar grade", "inputs": ["g"]}, {"id": "c_x", "label": "Extrasellar extension", "inputs": ["x"], "showSubtotal": False}],
        calculationMethod={"type": "select", "input": "g", "range": {"min": 1, "max": 5}, "display": "Grade {g_code}{x_code == '0' ? '' : '-' + x_code}", "share": "Hardy grade {g_code}{x_code == '0' ? '' : ', stage ' + x_code}"},
        interpretationRules=[{"when": "total <= 2", "state": "micro"}, {"state": "macro"}],
        resultStates=[st("micro", "informational", "Grade {g_code}{x_code == '0' ? '' : ', stage ' + x_code}", "Sellar grades 0–I correspond to microadenomas.", "0–I"),
                      st("macro", "informational", "Grade {g_code}{x_code == '0' ? '' : ', stage ' + x_code}", "Sellar grades II–IV correspond to macroadenomas.", "II–IV")],
        clinicalContext=[C("Combines sellar floor destruction with the direction of extrasellar extension.", True)], clinicalInsights=[{"when": "x >= 4", "text": "Stages D–E indicate intracranial or cavernous sinus extension; see Knosp for cavernous sinus invasion."}],
        limitations=[C("Developed in the radiograph/CT era; MRI-based Knosp grading is preferred for cavernous sinus invasion.", True), "Extrasellar stage wording differs between sources."],
        confounders=conf(("Empty sella or previous surgery", "Alters sellar contour."),), whatItDoesNotTellYou=["Hormonal activity.", "Visual function."], commonErrors=["Using stage letters without the sellar grade."],
        guideSections={"what": "Sellar grades 0–IV with extrasellar stages A–E.", "whenToUse": "Describing pituitary adenomas.", "howToPerform": "Grade the sellar floor; then assign the extrasellar extension.", "clinicalContext": "Used with Knosp grade, hormones and visual fields."},
        sources=[{"citation": "Hardy J. Transsphenoidal microsurgery of the normal and pathological pituitary. Clin Neurosurg. 1969;16:185-217."},
                 {"citation": "Wilson CB. Neurosurgical management of large and invasive pituitary tumors. In: Tindall GT, Collins WF, eds. Clinical Management of Pituitary Disorders. New York: Raven Press; 1979:335-342."}],
        licensing={"status": "Published classification with attribution", "note": "No reproduction restrictions identified."}))

    ly = [(100, "Fully active, normal"), (90, "Minor restrictions in strenuous physical activity"), (80, "Active, but tires more quickly"), (70, "Greater restriction of play and less time spent in play"),
          (60, "Up and around, but active play minimal; keeps busy with quieter activities"), (50, "Lies around much of the day; no active play; takes part in quiet play"),
          (40, "Mainly in bed; participates in quiet activities"), (30, "Bedbound; needs assistance even for quiet play"), (20, "Sleeps often; play limited to very passive activities"),
          (10, "Does not play; does not get out of bed"), (0, "Unresponsive")]
    L.append(mk(id="lansky", name="Lansky Play-Performance Scale", abbreviation="Lansky", aliases=["lansky", "play performance", "paediatric performance status", "pediatric performance status"],
        category="oncology", subcategory="Performance status", specialties=["Neuro-oncology", "Paediatric Oncology", "Neurosurgery"],
        version={"label": "Lansky et al. (1987), 0–100 in steps of 10", "detail": "Parent-rated play-performance for children; KPS is used from about age 16."},
        purpose="Describes functional performance in children with cancer.", intendedPopulation="Children (about 1–16 years), commonly in paediatric neuro-oncology.",
        resultPresentation={"type": "functional-status", "typeLabel": "Performance status", "meter": False},
        inputDefinitions=[single("lv", "Play-performance level", "Lansky", [o(v, "%d: %s" % (v, t), v, str(v)) for v, t in ly])],
        calculationMethod={"type": "select", "input": "lv", "range": {"min": 0, "max": 100}, "display": "Lansky {total}", "share": "Lansky {total}"},
        interpretationRules=[{"when": "total == 100", "state": "full"}, {"when": "total >= 50", "state": "mid"}, {"state": "low"}],
        resultStates=[st("full", "favorable", "Fully active", "Fully active, normal play at this assessment.", "100", "Describes play and activity, not the underlying disease."),
                      st("mid", "informational", "Lansky {total}", "Up and about with reduced play.", "50–90"), st("low", "informational", "Lansky {total}", "Mainly in bed or unresponsive.", "0–40")],
        clinicalContext=[C("The paediatric counterpart of the Karnofsky score, used for trial eligibility and monitoring.", True)], clinicalInsights=[{"text": "Usually rated by a parent; record who rated it."}],
        limitations=[C("Parent-reported; varies with the child's mood and setting.", True), "Validated in childhood cancer; less established in other conditions."], confounders=conf(("Developmental stage", "Affects play independent of illness."),),
        whatItDoesNotTellYou=["Tumour status.", "Cognitive function."], commonErrors=["Using it in adults (use KPS)."],
        guideSections={"what": "An 11-level play-performance scale from 100 (normal) to 0 (unresponsive).", "whenToUse": "Children with cancer, including brain tumours.", "howToPerform": "Ask the parent about play and activity over the past week; choose the level.", "clinicalContext": "Used alongside clinical and imaging assessment."},
        sources=[{"citation": "Lansky SB, List MA, Lansky LL, Ritter-Sterr C, Miller DR. The measurement of performance in childhood cancer patients. Cancer. 1987;60(7):1651-1656."}],
        licensing={"status": "Published scale with attribution", "note": "No reproduction restrictions identified."}))
    return L
