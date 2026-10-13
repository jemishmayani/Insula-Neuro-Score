"""Insula Neuro Score — v0.12 viva-yield expansion (licence-free items only).
Each item was checked against the sources in its `sources` field (verification notes: tools/evidence.py).
Descriptors are paraphrased in original wording. Excluded items and reasons: WITHHELD_V12 / OUT_OF_SCOPE below."""
from library import o, single, yn, st, conf, score

REVIEWED = "2026-10-13"

def mk(**k):
    d = score(**k); d["lastReviewed"] = REVIEWED; return d

def C(text, major=False):
    return {"text": text, "importance": "major"} if major else {"text": text}

def levels(id, label, short, rows, help=None):
    """rows: (code, label, detail) — points are the 1-based ordinal; the code is what is shown."""
    return single(id, label, short, [o(i + 1, lab, i + 1, code, det) for i, (code, lab, det) in enumerate(rows)], help)

def select_states(rows, prefix=""):
    """rows: (code, tone, label, summary, detail) → interpretation rules + states keyed by ordinal."""
    rules = [{"when": "total == %d" % (i + 1), "state": "s%d" % (i + 1)} for i in range(len(rows))]
    states = [st("s%d" % (i + 1), tone, lab, summ, prefix + code, det) for i, (code, tone, lab, summ, det) in enumerate(rows)]
    return rules, states

def build():
    L = []

    # =====================================================================================  STROKE
    # ---------------------------------------------------------------- TOAST
    toast = [("LAA", "Large-artery atherosclerosis", "Significant (>50%) stenosis or occlusion of a major brain artery or branch cortical artery, presumed atherosclerotic; cortical, cerebellar, brainstem or large (>1.5 cm) subcortical infarct; cardioembolic source excluded."),
             ("CE", "Cardioembolism", "Arterial occlusion presumed due to an embolus from the heart; at least one cardiac source of embolism identified."),
             ("SVO", "Small-vessel occlusion (lacune)", "Classical lacunar syndrome; normal imaging or a relevant brainstem or subcortical lesion under 1.5 cm; no cardiac source or ipsilateral large-artery stenosis over 50%."),
             ("OC", "Stroke of other determined aetiology", "Rare causes, e.g. non-atherosclerotic vasculopathy, hypercoagulable state or haematological disorder, with investigations supporting it."),
             ("UND", "Stroke of undetermined aetiology", "Two or more possible causes, a negative evaluation, or an incomplete evaluation.")]
    r, s = select_states([(c, "informational", lab, lab + ".", None) for c, lab, _ in toast])
    L.append(mk(id="toast", name="TOAST Classification of Ischaemic Stroke Subtype", abbreviation="TOAST", aliases=["toast", "stroke subtype", "stroke aetiology", "stroke etiology", "stroke mechanism"],
        category="stroke", subcategory="Stroke mechanism", specialties=["Stroke", "Neurology"],
        version={"label": "TOAST (Adams et al. 1993), five subtypes", "detail": "Each subtype may be graded 'probable' or 'possible' depending on how complete and consistent the investigations are. Later systems (e.g. SSS-TOAST, ASCOD) are different versions and are not combined."},
        purpose="Classifies ischaemic stroke by presumed mechanism, using clinical features and investigations.",
        intendedPopulation="Adults with ischaemic stroke after vascular, cardiac and laboratory investigation.",
        resultPresentation={"type": "classification", "typeLabel": "Stroke subtype", "meter": False},
        calculatorNotice={"tone": "info", "title": "Assign after investigation", "message": "TOAST depends on vascular imaging, cardiac evaluation and other tests. Assigned early, it is often provisional."},
        inputDefinitions=[levels("sub", "Presumed mechanism", "Subtype", toast), dict(single("cert", "Certainty (subtypes LAA, CE, SVO, OC)", "Certainty", [o("probable", "Probable", 0, "probable", "Clinical findings, imaging and investigations consistent; other causes excluded."), o("possible", "Possible", 0, "possible", "Clinical and imaging findings suggest the subtype but investigations are incomplete.")]), required=False, help="Optional. Not used for 'undetermined'.")],
        components=[{"id": "c_sub", "label": "Subtype", "inputs": ["sub"]}, {"id": "c_cert", "label": "Certainty", "inputs": ["cert"], "showSubtotal": False}],
        calculationMethod={"type": "select", "input": "sub", "range": {"min": 1, "max": 5}, "display": "{isnull(cert_code) ? sub_code : sub_code + ' (' + cert_code + ')'}", "share": "TOAST {sub_code}{isnull(cert_code) ? '' : ' (' + cert_code + ')'}"},
        consistencyRules=[{"when": "sub == 5 && !isnull(cert_value)", "severity": "warning", "inputs": ["cert"], "message": "'Undetermined' already covers incomplete or conflicting evaluation; probable/possible applies to the other subtypes."}],
        interpretationRules=r, resultStates=s,
        clinicalContext=[C("Classifies ischaemic stroke by presumed mechanism, which guides secondary prevention and research grouping.", True), C("The most widely used stroke subtype classification in trials.")],
        clinicalInsights=[{"when": "sub == 5", "text": "Undetermined includes cryptogenic stroke after full evaluation and strokes with two competing causes; say which."},
                          {"text": "Record which investigations were complete; the subtype can change as results arrive."}],
        limitations=[C("Assignment depends on how complete the investigations are; 'undetermined' rises when evaluation is limited.", True), "Inter-rater agreement is moderate.", "Does not separate embolic stroke of undetermined source as its own group."],
        confounders=conf(("Incomplete investigation", "Pushes cases into 'undetermined'."), ("Coexisting causes", "e.g. atrial fibrillation with carotid stenosis.")),
        whatItDoesNotTellYou=["Stroke severity.", "Prognosis on its own.", "Which treatment to choose."],
        commonErrors=["Assigning small-vessel occlusion to a subcortical infarct over 1.5 cm.", "Assigning a subtype before vascular and cardiac evaluation is complete without marking it 'possible'."],
        relatedScores=[], guideSections={"what": "Five ischaemic stroke subtypes by presumed mechanism: large-artery atherosclerosis, cardioembolism, small-vessel occlusion, other determined and undetermined.",
            "whenToUse": "After investigation of ischaemic stroke; communication, secondary prevention planning and research.",
            "howToPerform": "Combine the clinical syndrome, brain imaging, vascular imaging, cardiac evaluation and laboratory tests. Choose the subtype, then mark probable or possible.",
            "clinicalContext": "A mechanism classification, used with the full investigation results."},
        sources=[{"citation": "Adams HP Jr, Bendixen BH, Kappelle LJ, et al. Classification of subtype of acute ischemic stroke. Definitions for use in a multicenter clinical trial. TOAST. Trial of Org 10172 in Acute Stroke Treatment. Stroke. 1993;24(1):35-41."}],
        licensing={"status": "Published classification with attribution", "note": "No reproduction restrictions identified."}))

    # ---------------------------------------------------------------- Oxfordshire (Bamford)
    ocsp = [("TACI", "Total anterior circulation infarct", "All three: new higher cerebral dysfunction (e.g. dysphasia, neglect); homonymous visual field defect; ipsilateral motor and/or sensory deficit of at least two of face, arm and leg."),
            ("PACI", "Partial anterior circulation infarct", "Two of the three TACI components, or isolated higher cerebral dysfunction, or a motor/sensory deficit more restricted than a lacunar syndrome (e.g. one limb, or face and hand)."),
            ("LACI", "Lacunar infarct", "Pure motor stroke, pure sensory stroke, sensorimotor stroke or ataxic hemiparesis, without higher cerebral dysfunction or visual field defect."),
            ("POCI", "Posterior circulation infarct", "Ipsilateral cranial nerve palsy with contralateral motor/sensory deficit, bilateral motor/sensory deficit, conjugate eye movement disorder, cerebellar dysfunction without ipsilateral long-tract signs, or isolated homonymous visual field defect.")]
    r, s = select_states([(c, "informational", lab, lab + " (clinical syndrome).", None) for c, lab, _ in ocsp])
    L.append(mk(id="ocsp", name="Oxfordshire Community Stroke Project Classification (Bamford)", abbreviation="Oxfordshire (OCSP)", aliases=["bamford", "oxfordshire", "ocsp", "taci", "paci", "laci", "poci", "tacs", "pacs", "lacs", "pocs"],
        category="stroke", subcategory="Stroke syndrome", specialties=["Stroke", "Neurology"],
        version={"label": "OCSP / Bamford classification (Bamford et al. 1991)", "detail": "Four clinical syndromes. '-I' (infarct) is used when imaging confirms infarction; '-S' (syndrome) before imaging."},
        purpose="Classifies acute stroke by bedside clinical syndrome, which relates to lesion size, site and prognosis.",
        intendedPopulation="Patients with acute stroke, classified from the clinical examination.",
        resultPresentation={"type": "classification", "typeLabel": "Clinical stroke syndrome", "meter": False},
        inputDefinitions=[levels("syn", "Clinical syndrome", "Syndrome", ocsp, help="If the patient is drowsy or cannot be tested, higher cerebral dysfunction and field defect are often presumed present for TACI.")],
        calculationMethod={"type": "select", "input": "syn", "range": {"min": 1, "max": 4}, "display": "{syn_code}", "share": "OCSP {syn_code}"},
        interpretationRules=r, resultStates=s,
        clinicalContext=[C("A purely clinical classification that predicts lesion site, size and outcome.", True), C("Quick to apply at the bedside; frequently asked in examinations.")],
        clinicalInsights=[{"when": "syn == 1", "text": "TACI carries the poorest prognosis of the four syndromes in the original cohort."},
                          {"when": "syn == 3", "text": "Lacunar syndromes do not always correspond to lacunar infarcts on imaging."}],
        limitations=[C("Clinical syndrome only; imaging may show a different lesion.", True), "Assessment is harder in drowsy or aphasic patients.", "Does not give stroke mechanism (see TOAST)."],
        confounders=conf(("Reduced consciousness", "Limits testing of cortical function and fields."), ("Pre-existing deficits", "Can be mistaken for new features.")),
        whatItDoesNotTellYou=["The cause of the stroke.", "Haemorrhage versus infarction without imaging.", "Treatment eligibility."],
        commonErrors=["Calling a syndrome TACI without all three components.", "Using '-I' terminology before imaging."],
        relatedScores=[], guideSections={"what": "Four clinical stroke syndromes: TACI, PACI, LACI and POCI.",
            "whenToUse": "Bedside description of acute stroke; communication and prognosis.",
            "howToPerform": "Examine for higher cerebral dysfunction, homonymous field defect, the distribution of motor and sensory deficit, and brainstem or cerebellar signs. Choose the syndrome that fits.",
            "clinicalContext": "A clinical classification, used alongside imaging and TOAST."},
        sources=[{"citation": "Bamford J, Sandercock P, Dennis M, Burn J, Warlow C. Classification and natural history of clinically identifiable subtypes of cerebral infarction. Lancet. 1991;337(8756):1521-1526."}],
        licensing={"status": "Published classification with attribution", "note": "No reproduction restrictions identified."}))

    # ---------------------------------------------------------------- CHA2DS2-VASc
    L.append(mk(id="chadsvasc", name="CHA₂DS₂-VASc Score", abbreviation="CHA₂DS₂-VASc", aliases=["chads", "cha2ds2-vasc", "chadsvasc", "atrial fibrillation stroke risk", "af", "anticoagulation"],
        category="stroke", subcategory="Stroke risk in atrial fibrillation", specialties=["Stroke", "Neurology", "Cardiology"],
        version={"label": "CHA₂DS₂-VASc (Lip et al. 2010)", "detail": "Total 0–9. The 2024 ESC guideline's CHA₂DS₂-VA (sex category removed) is a different version and is not combined."},
        purpose="Estimates thromboembolic stroke risk in non-valvular atrial fibrillation.",
        intendedPopulation="Adults with atrial fibrillation without moderate-severe mitral stenosis or mechanical valves.",
        resultPresentation={"type": "prognostic-category", "typeLabel": "Stroke risk score", "meter": False},
        inputDefinitions=[yn("chf", "Congestive heart failure or LV dysfunction", "C"), yn("htn", "Hypertension", "H"),
                          single("age", "Age", "Age", [o("lt65", "Under 65", 0), o("65to74", "65–74", 1), o("ge75", "75 or older", 2)]),
                          yn("dm", "Diabetes mellitus", "D"), yn("stroke", "Previous stroke, TIA or thromboembolism", "S₂", points=2),
                          yn("vasc", "Vascular disease (previous MI, peripheral arterial disease or aortic plaque)", "V"),
                          single("sex", "Sex category", "Sc", [o("m", "Male", 0), o("f", "Female", 1)])],
        calculationMethod={"type": "sum", "range": {"min": 0, "max": 9}, "display": "{total}", "share": "CHA₂DS₂-VASc {total}"},
        interpretationRules=[{"when": "total == 0", "state": "low"}, {"when": "total == 1 && sex == 1", "state": "sexonly"}, {"when": "total == 1", "state": "one"}, {"state": "two"}],
        resultStates=[st("low", "low", "Low risk", "CHA₂DS₂-VASc 0: the lowest risk group.", "0"),
                      st("sexonly", "low", "Female sex only", "CHA₂DS₂-VASc 1 from female sex alone, which is not regarded as a risk factor on its own.", "1"),
                      st("one", "informational", "CHA₂DS₂-VASc 1", "One non-sex risk factor.", "1", "Decisions depend on the guideline in use and patient factors, including bleeding risk."),
                      st("two", "informational", "CHA₂DS₂-VASc {total}", "Two or more points: higher annual stroke risk with each point.", "2–9", "Guideline thresholds for anticoagulation differ by version and sex; integrate with bleeding risk and patient preference.")],
        clinicalContext=[C("Estimates thromboembolic risk in atrial fibrillation; used with a bleeding risk score.", True), C("Relevant in stroke clinic for secondary prevention after AF-related stroke (previous stroke scores 2).")],
        clinicalInsights=[{"when": "stroke == 2", "text": "After stroke or TIA the score is at least 2; risk factors and bleeding risk still guide shared decisions."},
                          {"text": "Assess bleeding risk alongside (e.g. HAS-BLED) and address modifiable risk factors."}],
        limitations=[C("Derived for non-valvular atrial fibrillation; not for mechanical valves or moderate-severe mitral stenosis.", True), "Event rates per point vary between cohorts.", "Does not include renal function, AF burden or imaging markers."],
        confounders=conf(("Undocumented history", "Under-scores vascular disease or prior TIA."), ("Definition differences", "e.g. what counts as vascular disease.")),
        whatItDoesNotTellYou=["Bleeding risk.", "Whether a stroke was cardioembolic.", "The choice of anticoagulant."],
        commonErrors=["Scoring 1 for age 75+ (it scores 2).", "Treating female sex alone as a risk factor.", "Mixing with the CHA₂DS₂-VA version."],
        guideSections={"what": "A 0–9 point score of stroke risk factors in atrial fibrillation.", "whenToUse": "Atrial fibrillation, including after stroke or TIA.",
            "howToPerform": "Score each factor present: CHF 1, hypertension 1, age 75+ 2, diabetes 1, prior stroke/TIA/thromboembolism 2, vascular disease 1, age 65–74 1, female sex 1.",
            "clinicalContext": "One input to anticoagulation decisions with bleeding risk and patient preference."},
        sources=[{"citation": "Lip GYH, Nieuwlaat R, Pisters R, Lane DA, Crijns HJGM. Refining clinical risk stratification for predicting stroke and thromboembolism in atrial fibrillation using a novel risk factor-based approach: the Euro Heart Survey on Atrial Fibrillation. Chest. 2010;137(2):263-272."}],
        licensing={"status": "Published score with attribution", "note": "No reproduction restrictions identified."}))

    # ---------------------------------------------------------------- HAS-BLED
    L.append(mk(id="hasbled", name="HAS-BLED Bleeding Risk Score", abbreviation="HAS-BLED", aliases=["has bled", "hasbled", "bleeding risk", "anticoagulation bleeding"],
        category="stroke", subcategory="Bleeding risk on anticoagulation", specialties=["Stroke", "Neurology", "Cardiology"],
        version={"label": "HAS-BLED (Pisters et al. 2010)", "detail": "Nine items, one point each, total 0–9. Abnormal renal and liver function, and drugs and alcohol, are scored separately."},
        purpose="Estimates 1-year major bleeding risk in patients with atrial fibrillation on anticoagulation.", intendedPopulation="Adults with atrial fibrillation considered for or taking anticoagulation.",
        resultPresentation={"type": "prognostic-category", "typeLabel": "Bleeding risk score", "meter": False},
        inputDefinitions=[yn("h", "Hypertension (uncontrolled, systolic >160 mmHg)", "H"), yn("ren", "Abnormal renal function (dialysis, transplant or creatinine ≥200 µmol/L)", "A renal"),
                          yn("liv", "Abnormal liver function (cirrhosis, or bilirubin >2× and AST/ALT/ALP >3× normal)", "A liver"), yn("s", "Previous stroke", "S"),
                          yn("b", "Bleeding history or predisposition", "B"), yn("l", "Labile INR (time in range <60%)", "L"), yn("e", "Elderly (age >65)", "E"),
                          yn("drug", "Drugs predisposing to bleeding (antiplatelet agents, NSAIDs)", "D drugs"), yn("alc", "Alcohol (≥8 drinks per week)", "D alcohol")],
        calculationMethod={"type": "sum", "range": {"min": 0, "max": 9}, "display": "{total}", "share": "HAS-BLED {total}"},
        interpretationRules=[{"when": "total >= 3", "state": "high"}, {"state": "lower"}],
        resultStates=[st("lower", "informational", "HAS-BLED {total}", "Score below 3.", "0–2", "Bleeding risk still depends on factors not in the score."),
                      st("high", "high", "High bleeding risk (≥3)", "HAS-BLED 3 or more: high-risk group in the derivation study.", "3–9",
                         "In guidelines this flags the need to correct modifiable factors and review more often; on its own it is not a reason to withhold anticoagulation. Integrate with stroke risk.")],
        clinicalContext=[C("Identifies patients with higher bleeding risk on anticoagulation, and modifiable factors.", True)],
        clinicalInsights=[{"when": "h == 1 || l == 1 || drug == 1 || alc == 1", "text": "Some contributing factors are modifiable (blood pressure, INR control, concomitant drugs, alcohol)."}],
        limitations=[C("Moderate predictive accuracy; not a decision rule for withholding anticoagulation.", True), "Labile INR applies only to vitamin K antagonists."],
        confounders=conf(("Incomplete history", "Under-scores bleeding history or alcohol."), ("Changing medication", "Antiplatelet use changes the score.")),
        whatItDoesNotTellYou=["Stroke risk.", "Intracranial versus extracranial bleeding risk.", "The choice of anticoagulant."],
        commonErrors=["Counting renal and liver as one point.", "Using the score to withhold anticoagulation without weighing stroke risk."],
        guideSections={"what": "Nine bleeding risk factors, one point each.", "whenToUse": "Atrial fibrillation patients on or considered for anticoagulation.",
            "howToPerform": "Score each item present; sum.", "clinicalContext": "Used with CHA₂DS₂-VASc and to target modifiable risk."},
        sources=[{"citation": "Pisters R, Lane DA, Nieuwlaat R, de Vos CB, Crijns HJGM, Lip GYH. A novel user-friendly score (HAS-BLED) to assess 1-year risk of major bleeding in patients with atrial fibrillation: the Euro Heart Survey. Chest. 2010;138(5):1093-1100."}],
        licensing={"status": "Published score with attribution", "note": "No reproduction restrictions identified."}))

    # ---------------------------------------------------------------- mTICI
    mt = [("0", "high", "No perfusion", "No antegrade flow beyond the occlusion.", "Assess further management according to the clinical situation and local protocol."),
          ("1", "high", "Minimal perfusion", "Contrast passes the occlusion with limited, slow distal branch filling and little perfusion.", "Assess further management according to the clinical situation and local protocol."),
          ("2a", "moderate", "Partial reperfusion (<50%)", "Antegrade reperfusion of less than half of the previously ischaemic territory.", None),
          ("2b", "low", "Substantial reperfusion (≥50%)", "Antegrade reperfusion of more than half of the previously ischaemic territory.", "mTICI 2b–3 is the usual definition of successful reperfusion in trials."),
          ("3", "favorable", "Complete reperfusion", "Complete antegrade reperfusion with no visible occlusion in distal branches, at this assessment.", "Final angiographic result; clinical outcome also depends on infarct core, time and collaterals.")]
    r, s = select_states(mt, prefix="mTICI ")
    L.append(mk(id="mtici", name="Modified Treatment in Cerebral Ischaemia (mTICI) Grade", abbreviation="mTICI", aliases=["tici", "mtici", "reperfusion", "thrombectomy result", "recanalization"],
        category="stroke", subcategory="Thrombectomy", specialties=["Stroke", "Interventional Neuroradiology", "Neurology"],
        version={"label": "mTICI (consensus recommendations, Zaidat et al. 2013)", "detail": "Grades 0, 1, 2a, 2b, 3. Grade 2c and the eTICI scale are later versions and are not combined."},
        purpose="Grades angiographic reperfusion after thrombectomy.", intendedPopulation="Patients after endovascular treatment for large vessel occlusion, graded on final angiography.",
        resultPresentation={"type": "imaging-classification", "typeLabel": "Reperfusion grade", "meter": False},
        inputDefinitions=[levels("g", "Final angiographic reperfusion", "mTICI", [(c, lab, summ) for c, _, lab, summ, _ in mt])],
        calculationMethod={"type": "select", "input": "g", "range": {"min": 1, "max": 5}, "display": "mTICI {g_code}", "share": "mTICI {g_code}"},
        interpretationRules=r, resultStates=s,
        clinicalContext=[C("Standard endpoint for reperfusion after thrombectomy; mTICI 2b–3 defines successful reperfusion.", True)],
        clinicalInsights=[{"when": "g == 4", "text": "2b spans 50–99%: later versions add 2c (near-complete) to separate these."}],
        limitations=[C("Visual estimate on angiography with moderate inter-rater agreement, especially between 2a and 2b.", True), "Graded in the territory of the target occlusion only."],
        confounders=conf(("Projection and run timing", "Can hide or exaggerate perfusion defects."), ("Distal emboli to new territories", "Not captured by the grade.")),
        whatItDoesNotTellYou=["Clinical outcome.", "Infarct size.", "Reperfusion in other territories."],
        commonErrors=["Mixing mTICI with eTICI or 2c grades.", "Grading on a single projection."],
        guideSections={"what": "A five-level grade of reperfusion after thrombectomy.", "whenToUse": "Reporting final angiographic results after endovascular stroke treatment.",
            "howToPerform": "Assess antegrade reperfusion of the previously ischaemic territory on final angiography in two projections; choose the grade.",
            "clinicalContext": "A technical endpoint; correlate with imaging and clinical course."},
        sources=[{"citation": "Zaidat OO, Yoo AJ, Khatri P, et al. Recommendations on angiographic revascularization grading standards for acute ischemic stroke: a consensus statement. Stroke. 2013;44(9):2650-2663."}],
        licensing={"status": "Published grading with attribution", "note": "No reproduction restrictions identified."}))

    # ---------------------------------------------------------------- ASITN/SIR collaterals
    col = [("0", "high", "No collaterals", "No collaterals visible to the ischaemic site.", "Assess with the full imaging picture; poor collaterals are associated with larger infarcts."),
           ("1", "moderate", "Slow, peripheral", "Slow collaterals to the periphery of the ischaemic site, with part of the defect persisting.", None),
           ("2", "moderate", "Rapid, peripheral", "Rapid collaterals to the periphery of the ischaemic site, with part of the defect persisting.", None),
           ("3", "low", "Slow but complete", "Collaterals give slow but complete filling of the ischaemic bed by the late venous phase.", None),
           ("4", "favorable", "Complete and rapid", "Complete and rapid retrograde collateral flow to the entire ischaemic territory, at this assessment.", "Good collaterals are associated with smaller infarcts but do not guarantee outcome.")]
    r, s = select_states(col, prefix="Grade ")
    L.append(mk(id="collaterals", name="ASITN/SIR Collateral Flow Grade", abbreviation="ASITN/SIR collaterals", aliases=["collaterals", "collateral grade", "asitn", "sir", "higashida"],
        category="stroke", subcategory="Thrombectomy", specialties=["Stroke", "Interventional Neuroradiology"],
        version={"label": "ASITN/SIR collateral flow grading (Higashida et al. 2003)", "detail": "Grades 0–4 on catheter angiography. CT-angiography collateral scores (e.g. Tan, Maas, Menon) are different systems."},
        purpose="Grades angiographic collateral flow to the ischaemic territory.", intendedPopulation="Patients with acute arterial occlusion undergoing catheter angiography.",
        resultPresentation={"type": "imaging-classification", "typeLabel": "Collateral grade", "meter": False},
        inputDefinitions=[levels("g", "Collateral flow", "Grade", [(c, lab, summ) for c, _, lab, summ, _ in col])],
        calculationMethod={"type": "select", "input": "g", "range": {"min": 1, "max": 5}, "display": "Grade {g_code}", "share": "ASITN/SIR collateral grade {g_code}"},
        interpretationRules=r, resultStates=s,
        clinicalContext=[C("Collateral status modifies how quickly the ischaemic core grows.", True)],
        clinicalInsights=[{"text": "Grade on late arterial and venous phases; collaterals fill late."}],
        limitations=[C("Requires catheter angiography of the collateral supply; often incompletely assessed during thrombectomy.", True), "Inter-rater variability."],
        confounders=conf(("Incomplete injections", "Collateral sources may not be opacified."),),
        whatItDoesNotTellYou=["Infarct core size.", "Clinical outcome on its own."], commonErrors=["Mixing with CT-angiography collateral scores."],
        guideSections={"what": "A five-level angiographic grade of collateral flow (0–4).", "whenToUse": "Angiographic assessment in acute ischaemic stroke.",
            "howToPerform": "Assess the rate and extent of collateral filling of the ischaemic territory through the venous phase; choose the grade.", "clinicalContext": "One imaging marker among core, perfusion and timing."},
        sources=[{"citation": "Higashida RT, Furlan AJ, Roberts H, et al. Trial design and reporting standards for intra-arterial cerebral thrombolysis for acute ischemic stroke. Stroke. 2003;34(8):e109-e137."}],
        licensing={"status": "Published grading with attribution", "note": "No reproduction restrictions identified."}))

    # ---------------------------------------------------------------- Fazekas
    pv = [("0", "Absent", None), ("1", "Caps or pencil-thin lining", None), ("2", "Smooth halo", None), ("3", "Irregular periventricular signal extending into deep white matter", None)]
    dw = [("0", "Absent", None), ("1", "Punctate foci", None), ("2", "Beginning confluence", None), ("3", "Large confluent areas", None)]
    L.append(mk(id="fazekas", name="Fazekas Scale for White Matter Hyperintensities", abbreviation="Fazekas", aliases=["fazekas", "white matter hyperintensities", "leukoaraiosis", "small vessel disease", "wmh"],
        category="stroke", subcategory="Small vessel disease imaging", specialties=["Neurology", "Neuroradiology", "Stroke"],
        version={"label": "Fazekas scale (Fazekas et al. 1987)", "detail": "Periventricular (0–3) and deep white matter (0–3) graded separately on T2/FLAIR MRI. The deep white matter grade is the one most often reported alone."},
        purpose="Grades the extent of white matter T2 hyperintensities.", intendedPopulation="Adults with brain MRI (T2/FLAIR), e.g. in cerebrovascular disease or cognitive assessment.",
        resultPresentation={"type": "imaging-classification", "typeLabel": "White matter grade", "meter": False},
        inputDefinitions=[single("pv", "Periventricular white matter", "PV", [o(i, lab, i, c) for i, (c, lab, _) in enumerate(pv)]),
                          single("dw", "Deep white matter", "Deep", [o(i, lab, i, c) for i, (c, lab, _) in enumerate(dw)])],
        scoringRules=[{"id": "tot", "expr": "pv + dw"}],
        calculationMethod={"type": "expression", "expression": "dw", "range": {"min": 0, "max": 3}, "display": "Deep {dw} · PV {pv}", "formulaEquals": False, "share": "Fazekas: deep {dw}, periventricular {pv}"},
        interpretationRules=[{"when": "total == 0 && pv == 0", "state": "none"}, {"when": "total <= 1", "state": "mild"}, {"when": "total == 2", "state": "mod"}, {"state": "sev"}],
        resultStates=[st("none", "favorable", "No white matter hyperintensities", "No periventricular or deep white matter hyperintensities graded at this assessment.", None, "Grades the T2/FLAIR appearance only; it does not exclude other pathology."),
                      st("mild", "low", "Deep grade 0–1", "Absent or punctate deep white matter hyperintensities (periventricular graded separately).", None),
                      st("mod", "moderate", "Deep grade 2", "Beginning confluence of deep white matter hyperintensities.", None),
                      st("sev", "high", "Deep grade 3", "Large confluent deep white matter hyperintensities.", None, "Interpret with age, vascular risk factors and the clinical question; assess for other causes of white matter change.")],
        clinicalContext=[C("A widely used visual rating of white matter hyperintensities, often presumed of vascular origin in older adults.", True)],
        clinicalInsights=[{"text": "Report both grades; the deep grade is often quoted alone (e.g. 'Fazekas 2')."}],
        limitations=[C("Visual, ordinal rating with ceiling effects; insensitive to small change.", True), "Not specific for vascular aetiology.", "Depends on sequence and field strength."],
        confounders=conf(("Demyelinating or inflammatory disease", "Produces hyperintensities of a different cause."), ("Age", "Some hyperintensity is common with ageing.")),
        whatItDoesNotTellYou=["The cause of the white matter change.", "Cognitive status.", "Stroke risk on its own."],
        commonErrors=["Reporting one number without saying which region.", "Applying it to non-vascular white matter disease without comment."],
        guideSections={"what": "Separate 0–3 grades for periventricular and deep white matter hyperintensities.", "whenToUse": "MRI reporting in cerebrovascular disease and cognitive impairment.",
            "howToPerform": "On FLAIR/T2, grade the periventricular pattern (caps, halo, extension) and the deep white matter pattern (punctate, beginning confluence, confluent).", "clinicalContext": "An imaging descriptor, interpreted with age and clinical context."},
        sources=[{"citation": "Fazekas F, Chawluk JB, Alavi A, Hurtig HI, Zimmerman RA. MR signal abnormalities at 1.5 T in Alzheimer's dementia and normal aging. AJR Am J Roentgenol. 1987;149(2):351-356."}],
        licensing={"status": "Published scale with attribution", "note": "No reproduction restrictions identified."}))

    # ---------------------------------------------------------------- ICH volume ABC/2
    dec = lambda id, label, short, help: {"id": id, "type": "decimal", "label": label, "short": short, "unit": "cm", "min": 0.1, "max": 20, "decimals": 1, "help": help}
    L.append(mk(id="ichvolume", name="Intracerebral Haemorrhage Volume (ABC/2)", abbreviation="ICH volume (ABC/2)", aliases=["abc/2", "abc2", "ich volume", "hematoma volume", "haematoma volume", "kothari"],
        category="ich", subcategory="Haematoma volume", specialties=["Neurosurgery", "Stroke", "Neurocritical Care"],
        version={"label": "ABC/2 ellipsoid estimate (Kothari et al. 1996)", "detail": "Volume (mL) = A × B × C / 2, with A, B and C in cm. C = number of slices showing haematoma × slice thickness, counting a slice as 1 if its haematoma area is ≥75% of the largest slice, 0.5 if 25–75%, and 0 if <25%."},
        purpose="Estimates intracerebral haematoma volume on CT at the bedside.", intendedPopulation="Patients with spontaneous intracerebral haemorrhage on non-contrast CT.",
        resultPresentation={"type": "measurement", "typeLabel": "Haematoma volume", "meter": False},
        calculatorNotice={"tone": "info", "title": "Measure on the largest slice", "message": "A is the largest diameter on the slice with the largest haematoma area; B is the largest diameter perpendicular to A on the same slice; C is the vertical extent."},
        inputDefinitions=[dec("a", "A: largest diameter", "A", "On the axial slice with the largest haematoma area."), dec("b", "B: largest diameter perpendicular to A", "B", "On the same slice as A."),
                          dec("c", "C: vertical extent", "C", "Weighted number of slices × slice thickness in cm (see version note).")],
        calculationMethod={"type": "expression", "expression": "a * b * c / 2", "range": {"min": 0, "max": 4000}, "formula": "{a} × {b} × {c} / 2", "display": "{fixed(total, 1)} mL", "share": "ICH volume (ABC/2) {fixed(total, 1)} mL"},
        interpretationRules=[{"when": "total >= 30", "state": "ge30"}, {"state": "lt30"}],
        resultStates=[st("lt30", "informational", "{fixed(total, 1)} mL", "Estimated haematoma volume below 30 mL.", "<30 mL", "Volume is one predictor of outcome; correlate with location, GCS, IVH and age."),
                      st("ge30", "informational", "{fixed(total, 1)} mL", "Estimated haematoma volume of 30 mL or more (the ICH Score volume threshold).", "≥30 mL", "Volume is one predictor of outcome; correlate with location, GCS, IVH and age.")],
        clinicalContext=[C("A quick bedside estimate of haematoma volume, an important predictor of outcome and expansion.", True), C("ICH volume ≥30 mL scores a point in the ICH Score.")],
        clinicalInsights=[{"when": "total >= 30", "text": "Volume ≥30 mL contributes 1 point to the ICH Score."}, {"text": "Repeat on follow-up CT to quantify expansion."}],
        limitations=[C("Overestimates irregular or lobulated haematomas (e.g. on anticoagulation) compared with planimetry.", True), "Measurement variability between readers.", "Slice weighting for C is often omitted, which overestimates volume."],
        confounders=conf(("Irregular shape", "ABC/2 assumes an ellipsoid."), ("Intraventricular extension", "Not included in the parenchymal estimate."), ("Slice thickness", "Must be known for C.")),
        whatItDoesNotTellYou=["Haematoma location or IVH.", "Whether the haematoma will expand.", "Treatment choice."],
        commonErrors=["Counting C as all slices without weighting.", "Measuring A and B on different slices.", "Mixing mm and cm (result 1000 times off)."],
        guideSections={"what": "An ellipsoid approximation of haematoma volume: A × B × C / 2.", "whenToUse": "Initial and follow-up CT in intracerebral haemorrhage.",
            "howToPerform": "On the slice with the largest haematoma, measure A and the perpendicular B. Count slices with haematoma using the 1 / 0.5 / 0 weighting and multiply by slice thickness for C. Enter in cm.", "clinicalContext": "One input to severity scores such as the ICH Score."},
        sources=[{"citation": "Kothari RU, Brott T, Broderick JP, et al. The ABCs of measuring intracerebral hemorrhage volumes. Stroke. 1996;27(8):1304-1305."}],
        licensing={"status": "Published method with attribution", "note": "No reproduction restrictions identified."}))

    # ---------------------------------------------------------------- BAT score
    L.append(mk(id="bat", name="BAT Score for Haematoma Expansion", abbreviation="BAT score", aliases=["bat", "blend sign", "hematoma expansion", "haematoma expansion", "hypodensity"],
        category="ich", subcategory="Haematoma expansion", specialties=["Stroke", "Neurosurgery", "Neurocritical Care"],
        version={"label": "BAT score (Morotti et al. 2018)", "detail": "Blend sign 1, any intrahaematoma hypodensity 2, time from onset to CT under 2.5 hours 2; total 0–5. A score of 3 or more identified higher risk of expansion."},
        purpose="Estimates the risk of haematoma expansion from non-contrast CT and timing.", intendedPopulation="Adults with spontaneous ICH imaged early with non-contrast CT; patients with coagulopathy were excluded from derivation.",
        resultPresentation={"type": "prognostic-category", "typeLabel": "Expansion risk score", "meter": False},
        inputDefinitions=[yn("blend", "Blend sign", "B", help="Hypodense and hyperdense regions with a well-defined margin, visible density difference of at least 18 HU."),
                          yn("hypo", "Any intrahaematoma hypodensity", "A", points=2), yn("time", "Time from onset to CT under 2.5 hours", "T", yes="Yes", no="No or unknown", points=2)],
        calculationMethod={"type": "sum", "range": {"min": 0, "max": 5}, "display": "{total}", "share": "BAT score {total}"},
        interpretationRules=[{"when": "total >= 3", "state": "high"}, {"state": "low"}],
        resultStates=[st("low", "informational", "BAT {total}", "Below the derivation threshold of 3.", "0–2", "Expansion can still occur; repeat imaging depends on the clinical course."),
                      st("high", "high", "Higher expansion risk (≥3)", "BAT 3 or more: higher risk of haematoma expansion in the derivation and validation cohorts.", "3–5", "Assess and monitor according to the clinical situation and local protocol.")],
        clinicalContext=[C("Combines two non-contrast CT signs with early presentation to identify likely haematoma expansion.", True)],
        clinicalInsights=[{"text": "Expansion is a modifiable determinant of outcome; time from onset matters."}],
        limitations=[C("Moderate discrimination (AUC about 0.65–0.77 across cohorts).", True), "Not derived in coagulopathic patients.", "CT sign interpretation varies between readers."],
        confounders=conf(("Anticoagulation", "Outside the derivation population."), ("Uncertain onset time", "Use last known well.")),
        whatItDoesNotTellYou=["Outcome directly.", "Whether a specific treatment will reduce expansion."], commonErrors=["Scoring the spot sign (CTA) here; BAT uses non-contrast CT only."],
        guideSections={"what": "Blend sign (1) + any hypodensity (2) + CT within 2.5 h of onset (2), total 0–5.", "whenToUse": "Early non-contrast CT in spontaneous ICH.",
            "howToPerform": "Look for a blend sign and intrahaematoma hypodensities; note time from onset to CT; sum.", "clinicalContext": "An expansion risk marker alongside volume and clinical status."},
        sources=[{"citation": "Morotti A, Dowlatshahi D, Boulouis G, et al. Predicting intracerebral hemorrhage expansion with noncontrast computed tomography: the BAT score. Stroke. 2018;49(5):1163-1169."}],
        licensing={"status": "Published score with attribution", "note": "No reproduction restrictions identified."}))

    # ---------------------------------------------------------------- Suzuki
    sz = [("I", "Narrowing of the carotid fork", "Stenosis of the terminal internal carotid arteries."),
          ("II", "Initiation of the moyamoya", "Dilated main cerebral arteries; moyamoya vessels begin to appear at the base."),
          ("III", "Intensification of the moyamoya", "Prominent basal moyamoya vessels; anterior and middle cerebral arteries narrowed or poorly filled."),
          ("IV", "Minimisation of the moyamoya", "Moyamoya vessels decrease; posterior cerebral involvement; extracranial collaterals increase."),
          ("V", "Reduction of the moyamoya", "Further reduction of moyamoya vessels; main intracranial arteries absent; collateral supply mainly external carotid."),
          ("VI", "Disappearance of the moyamoya", "Moyamoya vessels disappear; supply only from the external carotid (and vertebral) systems.")]
    r, s = select_states([(c, "informational", "Stage %s: %s" % (c, lab.lower()), det, None) for c, lab, det in sz])
    L.append(mk(id="suzuki", name="Suzuki Angiographic Staging of Moyamoya Disease", abbreviation="Suzuki stage", aliases=["suzuki", "moyamoya", "moya moya"],
        category="exam", subcategory="Vascular neurosurgery", specialties=["Neurosurgery", "Neurology", "Interventional Neuroradiology"],
        version={"label": "Suzuki and Takaku (1969), stages I–VI", "detail": "Angiographic stages of progressive steno-occlusion of the terminal internal carotid arteries and the development and regression of moyamoya collaterals."},
        purpose="Describes the angiographic stage of moyamoya disease.", intendedPopulation="Patients with moyamoya disease or syndrome studied with catheter angiography.",
        resultPresentation={"type": "imaging-classification", "typeLabel": "Angiographic stage", "meter": False},
        inputDefinitions=[levels("stg", "Angiographic stage", "Stage", sz)],
        calculationMethod={"type": "select", "input": "stg", "range": {"min": 1, "max": 6}, "display": "Stage {stg_code}", "share": "Suzuki stage {stg_code}"},
        interpretationRules=r, resultStates=s,
        clinicalContext=[C("Describes the natural angiographic progression of moyamoya disease.", True)],
        clinicalInsights=[{"text": "Stage each hemisphere separately; disease is often asymmetric."}],
        limitations=[C("Angiographic description; correlates imperfectly with symptoms or haemodynamic impairment.", True), "Progression does not always follow the stages in order."],
        confounders=conf(("Unilateral or asymmetric disease", "A single stage may not describe both sides."),),
        whatItDoesNotTellYou=["Cerebral perfusion reserve.", "Stroke risk.", "Whether revascularisation is indicated."], commonErrors=["Staging both hemispheres as one."],
        guideSections={"what": "Six angiographic stages of moyamoya disease.", "whenToUse": "Describing moyamoya on catheter angiography.",
            "howToPerform": "Review internal and external carotid and vertebral injections; assign the stage that fits each side.", "clinicalContext": "Used with perfusion studies and symptoms."},
        sources=[{"citation": "Suzuki J, Takaku A. Cerebrovascular 'moyamoya' disease. Disease showing abnormal net-like vessels in base of brain. Arch Neurol. 1969;20(3):288-299."}],
        licensing={"status": "Published staging with attribution", "note": "No reproduction restrictions identified."}))

    # ---------------------------------------------------------------- Raymond-Roy
    rr = [("I", "favorable", "Complete obliteration", "No contrast filling of the aneurysm sac or neck at this assessment.", "Follow-up imaging still determines durability."),
          ("II", "low", "Residual neck", "Contrast filling of the neck only.", None),
          ("III", "moderate", "Residual aneurysm", "Contrast filling of the aneurysm sac.", None)]
    r, s = select_states(rr)
    L.append(mk(id="raymondroy", name="Raymond-Roy Occlusion Classification", abbreviation="Raymond-Roy", aliases=["raymond", "raymond roy", "aneurysm occlusion", "coiling result"],
        category="exam", subcategory="Vascular neurosurgery", specialties=["Interventional Neuroradiology", "Neurosurgery"],
        version={"label": "Raymond-Roy occlusion classification (Raymond et al. 2003)", "detail": "Classes I–III. The modified classification (Mascitelli et al. 2015) splits class III into IIIa and IIIb and is a different version."},
        purpose="Classifies the angiographic occlusion of an aneurysm after coil embolisation.", intendedPopulation="Patients with intracranial aneurysms treated with coils, at treatment and follow-up.",
        resultPresentation={"type": "imaging-classification", "typeLabel": "Occlusion class", "meter": False},
        inputDefinitions=[levels("cls", "Angiographic occlusion", "Class", [(c, lab, summ) for c, _, lab, summ, _ in rr])],
        calculationMethod={"type": "select", "input": "cls", "range": {"min": 1, "max": 3}, "display": "Class {cls_code}", "share": "Raymond-Roy class {cls_code}"},
        interpretationRules=r, resultStates=s,
        clinicalContext=[C("Standard description of coil occlusion, used to judge recurrence risk and follow-up.", True)],
        clinicalInsights=[{"when": "cls == 3", "text": "Residual aneurysm is associated with higher recurrence; the modified classification distinguishes contrast within the coil mass (IIIa) from along the wall (IIIb)."}],
        limitations=[C("Two-dimensional angiographic assessment; small remnants may be missed.", True), "Not designed for flow diverters or intrasaccular devices."],
        confounders=conf(("Coil compaction over time", "Changes the class at follow-up."), ("Projection", "Can hide a neck remnant.")),
        whatItDoesNotTellYou=["Rupture risk directly.", "Whether retreatment is needed."], commonErrors=["Mixing classes from the modified version."],
        guideSections={"what": "Three classes of aneurysm occlusion after coiling.", "whenToUse": "Immediately after coiling and at angiographic follow-up.",
            "howToPerform": "On working projections, assess contrast in the neck and sac; choose the class.", "clinicalContext": "Guides surveillance in combination with aneurysm features."},
        sources=[{"citation": "Raymond J, Guilbert F, Weill A, et al. Long-term angiographic recurrences after selective endovascular treatment of aneurysms with detachable coils. Stroke. 2003;34(6):1398-1403."},
                 {"citation": "Roy D, Milot G, Raymond J. Endovascular treatment of unruptured aneurysms. Stroke. 2001;32(9):1998-2004."}],
        licensing={"status": "Published classification with attribution", "note": "No reproduction restrictions identified."}))
    return L
