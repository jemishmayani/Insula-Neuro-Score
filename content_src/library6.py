"""Insula Neuro Score — v0.12: neurocritical care measurements, general neurology, Chiari and peripheral nerve (licence-free)."""
from library import o, single, yn, st, conf, score
from library4 import mk, C, levels, select_states

MEAS = lambda label: {"type": "measurement", "typeLabel": label, "meter": False}

def build():
    L = []
    # ---------------------------------------------------------------- STESS
    L.append(mk(id="stess", name="Status Epilepticus Severity Score", abbreviation="STESS", aliases=["stess", "status epilepticus", "se prognosis"],
        category="neurocritical", subcategory="Status epilepticus", specialties=["Neurology", "Neurocritical Care", "Emergency Medicine"],
        version={"label": "STESS (Rossetti et al. 2008)", "detail": "Consciousness 0–1, worst seizure type 0–2, age 0 or 2, history of seizures 0–1; total 0–6. Scores 0–2 were 'favourable'."},
        purpose="Estimates the risk of death in adults with status epilepticus, assessed before treatment.", intendedPopulation="Adults with status epilepticus (excluding post-anoxic status).",
        resultPresentation={"type": "prognostic-category", "typeLabel": "Prognostic score", "meter": True},
        inputDefinitions=[single("loc", "Consciousness before treatment", "Consciousness", [o("alert", "Alert, somnolent or confused", 0), o("stupor", "Stuporous or comatose", 1)]),
                          single("type", "Worst seizure type", "Seizure type", [o("focal", "Simple or complex partial, absence, or myoclonic (myoclonic only in idiopathic generalised epilepsy)", 0),
                                                                              o("gc", "Generalised convulsive", 1), o("ncse", "Non-convulsive status epilepticus in coma", 2)]),
                          single("age", "Age", "Age", [o("lt65", "Under 65 years", 0), o("ge65", "65 years or older", 2)]),
                          single("hx", "Previous seizures", "History", [o("yes", "Yes", 0), o("no", "No or unknown", 1)])],
        calculationMethod={"type": "sum", "range": {"min": 0, "max": 6}, "display": "{total}", "share": "STESS {total}"},
        interpretationRules=[{"when": "total <= 2", "state": "fav"}, {"state": "unfav"}],
        resultStates=[st("fav", "low", "Favourable range (0–2)", "STESS 0–2: the derivation study's favourable group, with a high negative predictive value for death.", "0–2", "Prognosis also depends on aetiology and response to treatment.", 0, 2),
                      st("unfav", "high", "Unfavourable range (≥3)", "STESS 3 or more: higher mortality in the derivation and validation cohorts.", "3–6", "Aetiology and treatment response strongly influence outcome; assess according to the clinical situation and local protocol.", 3, 6)],
        clinicalContext=[C("Its main strength is identifying patients likely to survive (high negative predictive value).", True)], clinicalInsights=[{"text": "Aetiology is not in STESS; scores such as EMSE include it."}],
        limitations=[C("Low positive predictive value for death; not for individual treatment limitation.", True), "Seizure type and consciousness can be hard to judge before EEG."],
        confounders=conf(("Sedative drugs before assessment", "Lower consciousness."), ("Unknown seizure history", "Scores 1.")),
        whatItDoesNotTellYou=["The cause of status epilepticus.", "Which treatment to use."], commonErrors=["Scoring after treatment instead of before.", "Scoring age 65+ as 1 (it scores 2)."],
        guideSections={"what": "A 0–6 score from consciousness, seizure type, age and seizure history.", "whenToUse": "Early in adult status epilepticus.", "howToPerform": "Assess the four items before treatment; sum.", "clinicalContext": "A prognostic aid used with aetiology and EEG."},
        sources=[{"citation": "Rossetti AO, Logroscino G, Milligan TA, Michaelides C, Ruffieux C, Bromfield EB. Status Epilepticus Severity Score (STESS): a tool to orient early treatment strategy. J Neurol. 2008;255(10):1561-1566."}],
        licensing={"status": "Published score with attribution", "note": "No reproduction restrictions identified."}))

    # ---------------------------------------------------------------- CPP
    L.append(mk(id="cpp", name="Cerebral Perfusion Pressure", abbreviation="CPP", aliases=["cpp", "cerebral perfusion pressure", "icp", "intracranial pressure", "map"],
        category="neurocritical", subcategory="Intracranial pressure", specialties=["Neurocritical Care", "Neurosurgery"],
        version={"label": "CPP = MAP − ICP", "detail": "Mean arterial pressure minus intracranial pressure, both in mmHg. If MAP is not displayed, it can be estimated as diastolic + (systolic − diastolic)/3."},
        purpose="Calculates cerebral perfusion pressure from MAP and ICP.", intendedPopulation="Patients with ICP monitoring, e.g. after severe traumatic brain injury.",
        resultPresentation=MEAS("Cerebral perfusion pressure"),
        calculatorNotice={"tone": "info", "title": "Use one reference level", "message": "Arterial transducer levelling (heart or tragus) changes MAP and therefore CPP. Use your unit's convention consistently."},
        inputDefinitions=[{"id": "map", "type": "integer", "label": "Mean arterial pressure", "short": "MAP", "unit": "mmHg", "min": 20, "max": 200},
                          {"id": "icp", "type": "integer", "label": "Intracranial pressure", "short": "ICP", "unit": "mmHg", "min": -10, "max": 100}],
        calculationMethod={"type": "expression", "expression": "map - icp", "range": {"min": -80, "max": 210}, "formula": "MAP {map} − ICP {icp}", "display": "{total} mmHg", "share": "CPP {total} mmHg (MAP {map}, ICP {icp})"},
        interpretationRules=[{"state": "val"}],
        resultStates=[st("val", "informational", "CPP {total} mmHg", "Calculated cerebral perfusion pressure.", None, "Interpret with ICP, MAP trend, autoregulation status and the unit's targets.")],
        clinicalContext=[C("CPP is a surrogate for cerebral blood flow when autoregulation is impaired.", True),
                         C("Severe TBI guideline context (Brain Trauma Foundation, 4th ed. 2016): CPP 60–70 mmHg recommended as a target range; ICP above 22 mmHg associated with higher mortality.")],
        clinicalInsights=[{"when": "icp > 22", "importance": "major", "text": "ICP is above 22 mmHg, the BTF 2016 threshold associated with increased mortality in severe TBI."},
                          {"when": "total < 60", "text": "CPP is below the BTF 2016 target range of 60–70 mmHg for severe TBI."},
                          {"when": "total > 70", "text": "CPP is above 70 mmHg; BTF 2016 notes risk of respiratory complications with aggressive CPP elevation."}],
        limitations=[C("A single value; trends and autoregulation matter more than one reading.", True), "Targets come from severe TBI and may not apply to other conditions."],
        confounders=conf(("Transducer levelling", "Changes MAP and CPP by several mmHg."), ("Zero drift of ICP monitors", "Particularly with parenchymal sensors over time.")),
        whatItDoesNotTellYou=["Cerebral blood flow directly.", "Autoregulation status."], commonErrors=["Using systolic pressure instead of MAP.", "Mixing transducer levels between readings."],
        guideSections={"what": "CPP = MAP − ICP.", "whenToUse": "Patients with ICP monitoring.", "howToPerform": "Enter MAP and ICP measured at the same time.", "clinicalContext": "Interpret with trends, autoregulation and guideline targets."},
        sources=[{"citation": "Carney N, Totten AM, O'Reilly C, et al. Guidelines for the management of severe traumatic brain injury, fourth edition. Neurosurgery. 2017;80(1):6-15."}],
        licensing={"status": "Formula; guideline cited", "note": "No reproduction restrictions identified."}))

    # ---------------------------------------------------------------- Serum osmolality
    L.append(mk(id="osmolality", name="Calculated Serum Osmolality and Osmolar Gap", abbreviation="Osmolality", aliases=["osmolality", "osmolarity", "osmolar gap", "osmolal gap", "mannitol", "hypertonic saline"],
        category="neurocritical", subcategory="Osmotherapy monitoring", specialties=["Neurocritical Care", "Neurosurgery", "Critical Care"],
        version={"label": "Calculated osmolality = 2 × Na + glucose + urea (mmol/L)", "detail": "Equivalent to 2 × Na + glucose (mg/dL)/18 + BUN (mg/dL)/2.8. Osmolar gap = measured − calculated osmolality. Other formulas (e.g. 1.86 × Na) give different values and are not combined."},
        purpose="Calculates serum osmolality and the osmolar gap, e.g. when monitoring mannitol therapy.", intendedPopulation="Adults with serum sodium, glucose and urea results.",
        resultPresentation=MEAS("Calculated osmolality"),
        inputDefinitions=[{"id": "na", "type": "integer", "label": "Sodium", "short": "Na", "unit": "mmol/L", "min": 100, "max": 200},
                          {"id": "glu", "type": "measurement", "label": "Glucose", "short": "Glucose", "min": 0, "max": 150, "units": [{"id": "mmol", "label": "mmol/L", "factor": 1}, {"id": "mgdl", "label": "mg/dL", "factor": 0.0555556}]},
                          {"id": "urea", "type": "measurement", "label": "Urea (or BUN)", "short": "Urea", "min": 0, "max": 100, "units": [{"id": "mmol", "label": "mmol/L urea", "factor": 1}, {"id": "bun", "label": "mg/dL BUN", "factor": 0.357143}]},
                          {"id": "meas", "type": "integer", "label": "Measured osmolality (optional)", "short": "Measured", "unit": "mOsm/kg", "min": 200, "max": 500, "required": False, "help": "Adds the osmolar gap."}],
        components=[{"id": "c_calc", "label": "Calculated osmolality", "inputs": ["na", "glu", "urea"], "showSubtotal": False}, {"id": "c_meas", "label": "Measured", "inputs": ["meas"], "showSubtotal": False}],
        scoringRules=[{"id": "calc", "expr": "2 * na + glu + urea"}, {"id": "gap", "expr": "isnull(meas) ? 0 : meas - (2 * na + glu + urea)"}],
        calculationMethod={"type": "expression", "expression": "calc", "range": {"min": 200, "max": 650}, "formula": "2 × {na} + {fixed(glu, 1)} + {fixed(urea, 1)}",
                           "display": "{round(total)} mOsm/kg{isnull(meas) ? '' : ' · gap ' + round(gap)}", "share": "Calculated osmolality {round(total)} mOsm/kg{isnull(meas) ? '' : '; measured ' + meas + ', gap ' + round(gap)}"},
        interpretationRules=[{"when": "!isnull(meas) && gap > 10", "state": "gap"}, {"state": "val"}],
        resultStates=[st("val", "informational", "{round(total)} mOsm/kg", "Calculated serum osmolality.", None, "Typical reference range about 275–295 mOsm/kg; laboratories differ."),
                      st("gap", "moderate", "Osmolar gap {round(gap)}", "Measured osmolality exceeds the calculated value by more than 10 mOsm/kg.", None, "Unmeasured osmoles (e.g. mannitol, alcohols) raise the gap; interpret with the clinical context and laboratory method.")],
        clinicalContext=[C("Used to monitor osmotherapy: a raised osmolar gap suggests mannitol accumulation.", True), C("Measured osmolality is needed for the gap; calculated osmolality alone does not detect mannitol.")],
        clinicalInsights=[{"when": "!isnull(meas)", "text": "Measured and calculated values should be from the same sample."}],
        limitations=[C("Formula-dependent; reference ranges and gap thresholds vary between laboratories.", True), "Lipaemia and hyperproteinaemia affect sodium measurement."],
        confounders=conf(("Pseudohyponatraemia", "Alters the calculated value."), ("Alcohol", "Raises measured osmolality and the gap.")),
        whatItDoesNotTellYou=["The cause of a raised gap.", "Tonicity (urea crosses cell membranes)."], commonErrors=["Mixing mg/dL and mmol/L units.", "Comparing values from different samples."],
        guideSections={"what": "Calculated osmolality from sodium, glucose and urea, with the gap against measured osmolality.", "whenToUse": "Osmotherapy monitoring and suspected toxic alcohol ingestion.", "howToPerform": "Enter sodium, glucose and urea with their units; add measured osmolality for the gap.", "clinicalContext": "Interpret with the laboratory's reference ranges."},
        sources=[{"citation": "Purssell RA, Lynd LD, Koga Y. The use of the osmole gap as a screening test for the presence of exogenous substances. Toxicol Rev. 2004;23(3):189-202."}],
        licensing={"status": "Formula", "note": "No reproduction restrictions identified."}))

    # ---------------------------------------------------------------- Hoehn & Yahr
    hy = [("1", "Unilateral involvement only, usually with minimal or no functional disability"), ("2", "Bilateral or midline involvement without impairment of balance"),
          ("3", "Bilateral disease: mild to moderate disability with impaired postural reflexes; physically independent"), ("4", "Severely disabling disease; still able to walk or stand unassisted"),
          ("5", "Confinement to bed or wheelchair unless aided")]
    r, s = select_states([(c, "informational", "Stage %s" % c, lab + ".", None) for c, lab in hy])
    L.append(mk(id="hoehnyahr", name="Hoehn and Yahr Staging of Parkinson's Disease", abbreviation="Hoehn & Yahr", aliases=["hoehn", "yahr", "hoehn and yahr", "parkinson", "parkinsons", "pd stage"],
        category="neurology", subcategory="Movement disorders", specialties=["Neurology", "Movement Disorders", "Functional Neurosurgery"],
        version={"label": "Original Hoehn and Yahr (1967), stages 1–5", "detail": "The 'modified' version with stages 1.5 and 2.5 is not combined; the MDS Task Force (2004) recommends the original scale."},
        purpose="Describes the stage of motor disability in Parkinson's disease.", intendedPopulation="Patients with Parkinson's disease.", resultPresentation={"type": "disability", "typeLabel": "Disease stage", "meter": False},
        inputDefinitions=[levels("stg", "Stage", "Stage", [(c, "Stage %s: %s" % (c, lab), None) for c, lab in hy])],
        calculationMethod={"type": "select", "input": "stg", "range": {"min": 1, "max": 5}, "display": "H&Y {stg_code}", "share": "Hoehn & Yahr stage {stg_code}"},
        interpretationRules=r, resultStates=s,
        clinicalContext=[C("A simple global staging used in clinical description and trial eligibility (e.g. for deep brain stimulation selection).", True)], clinicalInsights=[{"text": "Record whether the patient was assessed 'on' or 'off' medication."}],
        limitations=[C("Weighted to motor and postural impairment; non-motor symptoms are not captured.", True), "Coarse; insensitive to change."], confounders=conf(("Medication state", "On/off state changes the stage."),),
        whatItDoesNotTellYou=["Non-motor symptoms.", "Response to levodopa."], commonErrors=["Using half-stages from the modified version."],
        guideSections={"what": "Five stages from unilateral disease to wheelchair or bed bound.", "whenToUse": "Describing Parkinson's disease severity.", "howToPerform": "Assess laterality, balance (pull test) and independence; choose the stage.", "clinicalContext": "Used with MDS-UPDRS and functional assessment."},
        sources=[{"citation": "Hoehn MM, Yahr MD. Parkinsonism: onset, progression and mortality. Neurology. 1967;17(5):427-442."},
                 {"citation": "Goetz CG, Poewe W, Rascol O, et al. Movement Disorder Society Task Force report on the Hoehn and Yahr staging scale: status and recommendations. Mov Disord. 2004;19(9):1020-1028."}],
        licensing={"status": "Published staging with attribution", "note": "No reproduction restrictions identified. MDS-UPDRS (licensed) is not included."}))

    # ---------------------------------------------------------------- GBS disability scale
    gd = [("0", "A healthy state"), ("1", "Minor symptoms and capable of running"), ("2", "Able to walk 10 m or more without assistance but unable to run"),
          ("3", "Able to walk 10 m across an open space with help"), ("4", "Bedridden or chairbound"), ("5", "Requiring assisted ventilation for at least part of the day"), ("6", "Dead")]
    L.append(mk(id="gbsds", name="GBS Disability Scale (Hughes)", abbreviation="GBS disability", aliases=["hughes", "gbs disability", "guillain-barre", "guillain barre", "gbs"],
        category="neurology", subcategory="Neuromuscular", specialties=["Neurology", "Neurocritical Care"],
        version={"label": "GBS disability scale (Hughes 1978) as used in EGOS (van Koningsveld 2007)", "detail": "Grades 0–6. Wording of grades 2–3 differs slightly between versions (5 m vs 10 m); the EGOS wording is used."},
        purpose="Grades functional disability in Guillain-Barré syndrome.", intendedPopulation="Patients with Guillain-Barré syndrome.", resultPresentation={"type": "disability", "typeLabel": "Disability grade", "meter": False},
        inputDefinitions=[single("g", "Functional level", "Grade", [o(i, "%s: %s" % (c, lab), i, c) for i, (c, lab) in enumerate(gd)])],
        calculationMethod={"type": "select", "input": "g", "range": {"min": 0, "max": 6}, "display": "Grade {total}", "share": "GBS disability grade {total}"},
        interpretationRules=[{"when": "total == 0", "state": "g0"}, {"when": "total <= 2", "state": "walk"}, {"when": "total <= 4", "state": "nowalk"}, {"when": "total == 5", "state": "vent"}, {"state": "dead"}],
        resultStates=[st("g0", "favorable", "Healthy state", "No disability measured by the scale at this assessment.", "0", "Fatigue, pain and sensory symptoms are not captured."),
                      st("walk", "informational", "Grade {total}: walks independently", "Able to walk independently.", "1–2"),
                      st("nowalk", "informational", "Grade {total}: unable to walk independently", "Unable to walk 10 m without help.", "3–4"),
                      st("vent", "informational", "Grade 5: ventilated", "Requires assisted ventilation for at least part of the day.", "5"),
                      st("dead", "informational", "Grade 6: dead", "Outcome: dead.", "6")],
        clinicalContext=[C("The standard functional outcome in GBS trials; grade 3 or more defines inability to walk independently.", True)], clinicalInsights=[{"text": "The grade at 2 weeks after admission feeds the EGOS prognostic score."}],
        limitations=[C("Coarse, walking-weighted scale.", True), "Insensitive to upper limb, sensory and autonomic involvement."], confounders=conf(("Pre-existing gait problems", "Raise the grade independent of GBS."),),
        whatItDoesNotTellYou=["Strength (see MRC sum score).", "Autonomic dysfunction."], commonErrors=["Mixing the 5 m and 10 m wording versions."],
        guideSections={"what": "Seven grades from healthy (0) to dead (6).", "whenToUse": "Serial assessment in GBS and trial outcomes.", "howToPerform": "Assess walking, running and ventilation needs; choose the grade.", "clinicalContext": "Used with MRC sum score and EGOS."},
        sources=[{"citation": "Hughes RAC, Newsom-Davis JM, Perkin GD, Pierce JM. Controlled trial of prednisolone in acute polyneuropathy. Lancet. 1978;2(8093):750-753."},
                 {"citation": "van Koningsveld R, Steyerberg EW, Hughes RAC, Swan AV, van Doorn PA, Jacobs BC. A clinical prognostic scoring system for Guillain-Barré syndrome. Lancet Neurol. 2007;6(7):589-594."}],
        licensing={"status": "Published scale with attribution", "note": "No reproduction restrictions identified."}))

    # ---------------------------------------------------------------- EGOS
    L.append(mk(id="egos", name="Erasmus GBS Outcome Score", abbreviation="EGOS", aliases=["egos", "erasmus", "gbs outcome", "guillain-barre prognosis"],
        category="neurology", subcategory="Neuromuscular", specialties=["Neurology", "Neurocritical Care"],
        version={"label": "EGOS (van Koningsveld et al. 2007)", "detail": "Age (>60 = 1, 41–60 = 0.5, ≤40 = 0) + preceding diarrhoea within 4 weeks (1) + GBS disability grade at 2 weeks after admission (0–1 = 1, 2 = 2, 3 = 3, 4 = 4, 5 = 5). Total 1–7. The modified EGOS (mEGOS) uses MRC sum score and is a different score."},
        purpose="Estimates the probability of being unable to walk independently at 6 months in Guillain-Barré syndrome.", intendedPopulation="Patients with GBS, scored 2 weeks after hospital admission.",
        resultPresentation={"type": "prognostic-category", "typeLabel": "Prognostic score", "meter": True},
        inputDefinitions=[single("age", "Age at onset", "Age", [o("le40", "40 years or younger", 0), o("41to60", "41–60 years", 0.5, "0.5"), o("gt60", "Over 60 years", 1)]),
                          yn("diar", "Diarrhoea in the 4 weeks before onset", "Diarrhoea"),
                          single("gbs", "GBS disability grade at 2 weeks after admission", "GBS grade", [o("0", "Grade 0–1", 1, "1"), o("2", "Grade 2", 2), o("3", "Grade 3", 3), o("4", "Grade 4", 4), o("5", "Grade 5", 5)])],
        calculationMethod={"type": "sum", "range": {"min": 1, "max": 7}, "display": "{total}", "share": "EGOS {total}"},
        interpretationRules=[{"when": "total <= 3", "state": "low"}, {"when": "total <= 5", "state": "mid"}, {"state": "high"}],
        resultStates=[st("low", "low", "EGOS {total}", "Lower scores: lower probability of being unable to walk at 6 months.", "1–3", None, 1, 3),
                      st("mid", "moderate", "EGOS {total}", "Intermediate probability of being unable to walk independently at 6 months.", "3.5–5", None, 3.5, 5),
                      st("high", "high", "EGOS {total}", "Higher scores: higher probability of being unable to walk independently at 6 months.", "5.5–7", "A group-level estimate; recovery continues beyond 6 months in many patients. Integrate with the clinical course.", 5.5, 7)],
        clinicalContext=[C("Helps counsel patients and families and stratify patients for trials.", True)], clinicalInsights=[{"text": "Score at 2 weeks after admission, when the disability grade is known."}],
        limitations=[C("Derived in Dutch cohorts; calibration varies between populations.", True), "Group-level prediction; not for individual treatment decisions."], confounders=conf(("Timing", "Scoring before 2 weeks uses the wrong disability grade."),),
        whatItDoesNotTellYou=["Need for ventilation (see EGRIS).", "Outcome beyond 6 months."], commonErrors=["Using the admission disability grade instead of the 2-week grade.", "Confusing EGOS with mEGOS."],
        guideSections={"what": "A 1–7 score from age, preceding diarrhoea and disability at 2 weeks.", "whenToUse": "GBS at 2 weeks after admission.", "howToPerform": "Score age band, diarrhoea history and the GBS disability grade; sum.", "clinicalContext": "A prognostic aid for counselling."},
        sources=[{"citation": "van Koningsveld R, Steyerberg EW, Hughes RAC, Swan AV, van Doorn PA, Jacobs BC. A clinical prognostic scoring system for Guillain-Barré syndrome. Lancet Neurol. 2007;6(7):589-594."}],
        licensing={"status": "Published score with attribution", "note": "No reproduction restrictions identified."}))

    # ---------------------------------------------------------------- MGFA
    mg = [("I", "Ocular weakness only (may include eye closure); all other strength normal"), ("IIa", "Mild non-ocular weakness, predominantly limb and/or axial"), ("IIb", "Mild non-ocular weakness, predominantly oropharyngeal and/or respiratory"),
          ("IIIa", "Moderate non-ocular weakness, predominantly limb and/or axial"), ("IIIb", "Moderate non-ocular weakness, predominantly oropharyngeal and/or respiratory"),
          ("IVa", "Severe non-ocular weakness, predominantly limb and/or axial"), ("IVb", "Severe non-ocular weakness, predominantly oropharyngeal and/or respiratory (includes feeding tube without intubation)"),
          ("V", "Intubation, with or without mechanical ventilation (excluding routine postoperative care)")]
    r, s = select_states([(c, "informational", "Class %s" % c, lab + ".", None) for c, lab in mg])
    L.append(mk(id="mgfa", name="MGFA Clinical Classification of Myasthenia Gravis", abbreviation="MGFA class", aliases=["mgfa", "myasthenia", "myasthenia gravis", "osserman"],
        category="neurology", subcategory="Neuromuscular", specialties=["Neurology", "Neurocritical Care"],
        version={"label": "MGFA clinical classification (Jaretzki et al. 2000)", "detail": "Classes I–V with subclasses a (limb/axial) and b (oropharyngeal/respiratory). Classes II–IV allow ocular weakness of any severity. The older Osserman classification is different."},
        purpose="Classifies the maximum severity and distribution of myasthenic weakness.", intendedPopulation="Patients with myasthenia gravis.", resultPresentation={"type": "classification", "typeLabel": "Clinical class", "meter": False},
        inputDefinitions=[levels("cls", "Clinical class", "Class", [(c, "%s: %s" % (c, lab), None) for c, lab in mg])],
        calculationMethod={"type": "select", "input": "cls", "range": {"min": 1, "max": 8}, "display": "MGFA {cls_code}", "share": "MGFA class {cls_code}"},
        interpretationRules=r, resultStates=s,
        clinicalContext=[C("Standard description of disease severity and pattern, used for trial entry and communication.", True)], clinicalInsights=[{"when": "cls == 3 || cls == 5 || cls == 7", "text": "Bulbar or respiratory predominance: correlate with respiratory function and swallowing."}],
        limitations=[C("Designed to classify maximum severity; not a sensitive measure of change (use quantitative scales).", True), "Mild, moderate and severe are not defined numerically."], confounders=conf(("Treatment", "Classification at maximum severity versus current status differs."),),
        whatItDoesNotTellYou=["Response to treatment.", "Antibody status."], commonErrors=["Using MGFA class as an outcome measure."],
        guideSections={"what": "Five classes of myasthenic weakness, with a/b subclasses by distribution.", "whenToUse": "Describing myasthenia gravis severity.", "howToPerform": "Assess ocular, limb, axial, bulbar and respiratory weakness; choose the class.", "clinicalContext": "Used with quantitative MG scores and respiratory monitoring."},
        sources=[{"citation": "Jaretzki A 3rd, Barohn RJ, Ernstoff RM, et al. Myasthenia gravis: recommendations for clinical research standards. Task Force of the Medical Scientific Advisory Board of the Myasthenia Gravis Foundation of America. Neurology. 2000;55(1):16-23."}],
        licensing={"status": "Published classification with attribution", "note": "No reproduction restrictions identified."}))

    # ---------------------------------------------------------------- Chiari
    ch = [("I", "Caudal displacement of the cerebellar tonsils below the foramen magnum (commonly ≥5 mm on MRI)", "May be associated with syringomyelia."),
          ("II", "Caudal displacement of the vermis, brainstem and fourth ventricle", "Almost always with open spinal dysraphism (myelomeningocele)."),
          ("III", "Herniation of posterior fossa contents into a low occipital or high cervical encephalocele", "Rare and severe."),
          ("IV", "Severe cerebellar hypoplasia without herniation", "Now regarded as a form of cerebellar hypoplasia.")]
    r, s = select_states([(c, "informational", "Type %s" % c, lab + ".", det) for c, lab, det in ch])
    L.append(mk(id="chiari", name="Chiari Malformation Classification", abbreviation="Chiari", aliases=["chiari", "arnold-chiari", "tonsillar ectopia", "hindbrain herniation"],
        category="spine", subcategory="Craniovertebral junction", specialties=["Neurosurgery", "Paediatric Neurosurgery", "Neuroradiology"],
        version={"label": "Classical Chiari types I–IV (Chiari 1891, 1896)", "detail": "Types 0, 1.5 and V are later additions and are not included. The ≥5 mm tonsillar descent threshold is a later radiological convention."},
        purpose="Classifies hindbrain herniation malformations.", intendedPopulation="Patients with posterior fossa or craniovertebral junction anomalies on MRI.", resultPresentation={"type": "classification", "typeLabel": "Malformation type", "meter": False},
        inputDefinitions=[levels("t", "Malformation type", "Type", [(c, "Type %s: %s" % (c, lab), None) for c, lab, _ in ch])],
        calculationMethod={"type": "select", "input": "t", "range": {"min": 1, "max": 4}, "display": "Chiari {t_code}", "share": "Chiari type {t_code}"},
        interpretationRules=r, resultStates=s,
        clinicalContext=[C("Types I and II are common in clinical practice; type II accompanies myelomeningocele.", True)], clinicalInsights=[{"when": "t == 1", "text": "Tonsillar descent alone, without symptoms or syrinx, is often an incidental finding."}],
        limitations=[C("Anatomical classification; symptoms correlate poorly with the degree of tonsillar descent.", True), "Types IV and later additions are inconsistently defined between sources."], confounders=conf(("Intracranial hypotension", "Can cause acquired tonsillar descent."),),
        whatItDoesNotTellYou=["Whether symptoms are due to the malformation.", "Need for surgery."], commonErrors=["Calling acquired tonsillar descent from low CSF pressure a Chiari I malformation."],
        guideSections={"what": "Four classical types of hindbrain malformation.", "whenToUse": "MRI of the posterior fossa and craniovertebral junction.", "howToPerform": "Identify which structures are displaced and any associated dysraphism or encephalocele.", "clinicalContext": "Correlate with symptoms, syrinx and CSF flow."},
        sources=[{"citation": "Chiari H. Über Veränderungen des Kleinhirns infolge von Hydrocephalie des Grosshirns. Dtsch Med Wochenschr. 1891;17:1172-1175."}],
        licensing={"status": "Classical classification", "note": "No reproduction restrictions identified."}))

    # ---------------------------------------------------------------- Seddon / Sunderland
    sd = [("Neurapraxia", "Focal conduction block with intact axons (myelin injury)", "Recovery usually complete within weeks to months."),
          ("Axonotmesis", "Axonal disruption with preserved connective tissue sheaths; Wallerian degeneration", "Recovery by regeneration (about 1 mm/day), often good."),
          ("Neurotmesis", "Complete disruption of the nerve including its connective tissue", "No useful spontaneous recovery expected.")]
    r, s = select_states([(c, "informational", c, lab + ".", det) for c, lab, det in sd])
    L.append(mk(id="seddon", name="Seddon Classification of Nerve Injury", abbreviation="Seddon", aliases=["seddon", "nerve injury", "neurapraxia", "axonotmesis", "neurotmesis", "peripheral nerve"],
        category="exam", subcategory="Peripheral nerve", specialties=["Neurosurgery", "Neurology", "Plastic Surgery", "Orthopaedics"],
        version={"label": "Seddon (1943): neurapraxia, axonotmesis, neurotmesis", "detail": "Three classes by the structures injured. Sunderland's five degrees subdivide these."},
        purpose="Classifies peripheral nerve injury by the structures disrupted.", intendedPopulation="Patients with peripheral nerve injury.", resultPresentation={"type": "classification", "typeLabel": "Injury class", "meter": False},
        inputDefinitions=[levels("c", "Injury class", "Class", [(c, "%s: %s" % (c, lab), None) for c, lab, _ in sd])],
        calculationMethod={"type": "select", "input": "c", "range": {"min": 1, "max": 3}, "display": "{c_code}", "share": "Seddon: {c_code}"},
        interpretationRules=r, resultStates=s,
        clinicalContext=[C("Determines expected recovery and whether surgical repair may be needed.", True)], clinicalInsights=[{"text": "The class is often clear only with time and serial neurophysiology; early injuries can be mixed."}],
        limitations=[C("Often cannot be determined at presentation; mixed injuries are common.", True), "Does not separate the degrees within axonotmesis that differ in recovery (see Sunderland)."], confounders=conf(("Timing of neurophysiology", "Wallerian degeneration takes days to show."),),
        whatItDoesNotTellYou=["The level of injury.", "Timing of repair."], commonErrors=["Classifying before neurophysiology can distinguish conduction block from axonal loss."],
        guideSections={"what": "Three classes of nerve injury.", "whenToUse": "Peripheral nerve trauma.", "howToPerform": "Combine mechanism, examination, serial neurophysiology and operative findings.", "clinicalContext": "Guides expectations and timing of surgery."},
        sources=[{"citation": "Seddon HJ. Three types of nerve injury. Brain. 1943;66(4):237-288."}],
        licensing={"status": "Classical classification", "note": "No reproduction restrictions identified."}))

    su = [("1", "First degree", "Conduction block; axon intact (= neurapraxia)", "Full recovery expected."),
          ("2", "Second degree", "Axon disrupted; endoneurium intact (axonotmesis)", "Full recovery by regeneration expected."),
          ("3", "Third degree", "Axon and endoneurium disrupted; perineurium intact", "Variable recovery; misdirected regeneration possible."),
          ("4", "Fourth degree", "Only epineurium intact (neuroma in continuity)", "Little useful spontaneous recovery; surgical repair usually considered."),
          ("5", "Fifth degree", "Complete transection (= neurotmesis)", "No spontaneous recovery.")]
    r, s = select_states([(c, "informational", lab, det + ".", rec) for c, lab, det, rec in su])
    L.append(mk(id="sunderland", name="Sunderland Classification of Nerve Injury", abbreviation="Sunderland", aliases=["sunderland", "nerve injury degree", "peripheral nerve", "neuroma in continuity"],
        category="exam", subcategory="Peripheral nerve", specialties=["Neurosurgery", "Neurology", "Plastic Surgery", "Orthopaedics"],
        version={"label": "Sunderland (1951), first to fifth degree", "detail": "Mackinnon's sixth degree (mixed injury) is a later addition and is not included."},
        purpose="Grades peripheral nerve injury by the connective tissue layers disrupted.", intendedPopulation="Patients with peripheral nerve injury.", resultPresentation={"type": "classification", "typeLabel": "Injury degree", "meter": False},
        inputDefinitions=[levels("d", "Injury degree", "Degree", [(c, "%s: %s" % (lab, det), None) for c, lab, det, _ in su])],
        calculationMethod={"type": "select", "input": "d", "range": {"min": 1, "max": 5}, "display": "Degree {d_code}", "share": "Sunderland degree {d_code}"},
        interpretationRules=r, resultStates=s,
        clinicalContext=[C("Refines Seddon's axonotmesis into degrees with different recovery potential.", True)], clinicalInsights=[{"when": "d >= 4", "text": "Fourth and fifth degree injuries do not recover usefully without repair."}],
        limitations=[C("The degree is usually inferred over time; not directly visible clinically.", True), "Third and fourth degree injuries are hard to separate without surgical exploration."], confounders=conf(("Mixed injuries", "Different fascicles can have different degrees."),),
        whatItDoesNotTellYou=["Injury level.", "Timing of surgery."], commonErrors=["Assigning a degree on day one without follow-up."],
        guideSections={"what": "Five degrees of nerve injury.", "whenToUse": "Peripheral nerve trauma.", "howToPerform": "Combine clinical recovery, serial neurophysiology and operative findings.", "clinicalContext": "Guides decisions about exploration and repair."},
        sources=[{"citation": "Sunderland S. A classification of peripheral nerve injuries producing loss of function. Brain. 1951;74(4):491-516."}],
        licensing={"status": "Classical classification", "note": "No reproduction restrictions identified."}))
    return L

# Considered for v0.12 but not built. Recorded in catalog.json → withheld (not shown in the app).
WITHHELD_V12 = {
    "pgcs": ("Paediatric Glasgow Coma Scale", "Paediatric GCS", "consciousness", "Version",
             "Several different paediatric modifications are in use (verbal scales for preverbal children differ), and the official Glasgow paediatric aid has its own reproduction terms. Not implemented until one version and its terms are confirmed."),
    "emse": ("Epidemiology-based Mortality Score in Status Epilepticus", "EMSE", "neurocritical", "Verification",
             "Aetiology, comorbidity, age and EEG item weights could not be confirmed from an accessible primary source in this review."),
    "rano": ("Response Assessment in Neuro-Oncology criteria", "RANO", "oncology", "Version",
             "RANO 2010 and RANO 2.0 (2023) differ; response categories need serial measurements and steroid/clinical data, which a single-entry calculator cannot capture reliably."),
    "mcdonald": ("McDonald criteria for multiple sclerosis (2017)", "McDonald 2017", "neurology", "Scope",
             "Diagnostic criteria. The app does not diagnose; to be reconsidered as a reference checklist."),
    "whocns5": ("WHO Classification of CNS Tumours (5th ed., 2021)", "WHO CNS5", "oncology", "Scope",
             "A reference classification of tumour types and grades rather than a calculator; integrated molecular diagnosis is outside the app's scope."),
    "aospine": ("AO Spine injury classifications", "AO Spine", "spine", "Licensing",
             "AO Spine classifications are published by AO Foundation with reproduction terms; not implemented until permission is confirmed. TLICS and SLIC are implemented instead."),
    "edss": ("Expanded Disability Status Scale (Kurtzke)", "EDSS", "neurology", "Licensing",
             "The scoring definitions and Neurostatus training materials have reproduction and use terms; not implemented until permission is confirmed."),
    "alsfrsr": ("Revised ALS Functional Rating Scale", "ALSFRS-R", "neurology", "Licensing",
             "A copyrighted questionnaire; use terms not confirmed."),
    "camicu": ("Confusion Assessment Method for the ICU", "CAM-ICU", "neurocritical", "Licensing",
             "Copyrighted instrument with its own terms of use; not reproduced until confirmed."),
    "braindeath": ("Brain death / death by neurological criteria checklist", "BD/DNC checklist", "neurocritical", "Scope",
             "Criteria and procedures are defined by national and institutional protocols; a single checklist would not be correct everywhere."),
}
