"""Curated clinical relationships between scores (contextual links shown in every Guide).
Kept in one place so relationships can be reviewed together. Links to scores not shown in the app are dropped at build time."""
RELATED = {
    # v0.12
    "toast": [("ocsp", "Clinical syndrome"), ("nihss", "Deficit severity"), ("chadsvasc", "AF stroke risk")],
    "ocsp": [("toast", "Mechanism"), ("nihss", "Deficit severity")],
    "chadsvasc": [("hasbled", "Bleeding risk"), ("toast", "Stroke mechanism"), ("abcd2", "Risk after TIA")],
    "hasbled": [("chadsvasc", "Stroke risk")],
    "mtici": [("collaterals", "Collateral grade"), ("aspects", "Early ischaemic change"), ("nihss", "Deficit severity")],
    "collaterals": [("mtici", "Reperfusion grade"), ("aspects", "Early ischaemic change")],
    "fazekas": [("toast", "Small-vessel occlusion subtype")],
    "ichvolume": [("ich", "Uses volume ≥30 mL"), ("bat", "Expansion risk"), ("func", "Uses volume")],
    "bat": [("ichvolume", "Haematoma volume"), ("ich", "Severity grade")],
    "suzuki": [("spetzler", "AVM grade")],
    "raymondroy": [("hunthess", "SAH grade"), ("wfns", "SAH grade")],
    "cchr": [("gcs", "Consciousness"), ("ccsr", "C-spine rule"), ("marshall", "CT classification")],
    "nexus": [("ccsr", "Alternative C-spine rule"), ("slic", "Subaxial injury classification")],
    "ccsr": [("nexus", "Alternative C-spine rule"), ("cchr", "Head CT rule"), ("slic", "Subaxial injury classification")],
    "slic": [("tlics", "Thoracolumbar equivalent"), ("frankel", "Cord injury grade"), ("andersondalonzo", "Odontoid fractures")],
    "tlics": [("slic", "Cervical equivalent"), ("frankel", "Cord injury grade")],
    "andersondalonzo": [("levineedwards", "C2 pars fractures"), ("slic", "Subaxial injuries")],
    "levineedwards": [("andersondalonzo", "Odontoid fractures"), ("slic", "Subaxial injuries")],
    "pfirrmann": [("modic", "Endplate changes"), ("schizas", "Stenosis grade")],
    "modic": [("pfirrmann", "Disc degeneration")],
    "meyerding": [("schizas", "Stenosis grade"), ("pfirrmann", "Disc degeneration")],
    "schizas": [("meyerding", "Spondylolisthesis"), ("pfirrmann", "Disc degeneration")],
    "koos": [("gr", "Hearing class"), ("hb", "Facial nerve grade")],
    "simpson": [("kps", "Performance status")],
    "knosp": [("hardy", "Sellar grade and extension")],
    "hardy": [("knosp", "Cavernous sinus invasion")],
    "lansky": [("kps", "Adult equivalent")],
    "stess": [("gcs", "Consciousness")],
    "cpp": [("gcs", "Consciousness"), ("marshall", "CT classification")],
    "osmolality": [("cpp", "Perfusion pressure")],
    "hoehnyahr": [("mrs", "Global disability")],
    "gbsds": [("egos", "Prognosis"), ("mrcss", "Global strength")],
    "egos": [("gbsds", "Disability grade used"), ("mrcss", "Global strength")],
    "mgfa": [("mrcss", "Global strength")],
    "chiari": [],
    "seddon": [("sunderland", "Five-degree refinement"), ("mrc", "Muscle power")],
    "sunderland": [("seddon", "Three-class version"), ("mrc", "Muscle power")],
    # Neurosurgical examination & grades (v0.10)
    "mrc": [("mrcss", "Sum of 12 movements"), ("dtr", "Reflex grade"), ("mas", "Tone"), ("plantar", "Upper motor neuron sign")],
    "mrcss": [("mrc", "Grade for each movement"), ("sofa", "Organ dysfunction in ICU"), ("dtr", "Reflex grade")],
    "dtr": [("clonus", "Record clonus"), ("plantar", "Plantar response"), ("mrc", "Muscle power"), ("mas", "Tone")],
    "clonus": [("dtr", "Reflex grade"), ("plantar", "Plantar response"), ("mas", "Tone"), ("mts", "Velocity-dependent spasticity")],
    "plantar": [("dtr", "Reflex grade"), ("clonus", "Clonus"), ("mrc", "Muscle power")],
    "mas": [("mts", "Separates spasticity from contracture"), ("clonus", "Clonus"), ("dtr", "Reflex grade")],
    "mts": [("mas", "Resistance to passive movement"), ("clonus", "Clonus")],
    "hb": [("gr", "Hearing in CPA lesions")],
    "gr": [("hb", "Facial nerve function in CPA lesions")],
    "spetzler": [("lawtonyoung", "Supplementary grade"), ("borden", "Dural fistula classification"), ("mrs", "Functional outcome")],
    "lawtonyoung": [("spetzler", "Grade combined with it"), ("mrs", "Functional outcome")],
    "borden": [("cognard", "More detailed dAVF classification"), ("spetzler", "AVM grade")],
    "cognard": [("borden", "Simpler dAVF classification"), ("spetzler", "AVM grade")],
    "markwalder": [("gcs", "Level of consciousness"), ("mrs", "Functional outcome")],
    "engel": [("ilae", "Alternative outcome classification"), ("mrs", "Functional status")],
    "ilae": [("engel", "Alternative outcome classification")],
    # Consciousness / outcome
    "gcs": [("gcsp", "Adds pupil reactivity"), ("gose", "Outcome after brain injury"), ("wfns", "SAH grade built on GCS")],
    "gcsp": [("gcs", "Underlying scale"), ("gose", "Outcome after brain injury"), ("rotterdam", "CT prognostic score in TBI")],
    "gos": [("gose", "Extended 8-category version"), ("gcs", "Acute level of consciousness"), ("mrs", "Global disability scale")],
    "gose": [("gos", "Original 5-category scale"), ("gcs", "Acute level of consciousness"), ("gcsp", "Acute severity with pupils"), ("mrs", "Global disability scale")],
    # Stroke
    "nihss": [("aspects", "Early ischaemic change on CT"), ("mrs", "Functional outcome"), ("pcaspects", "Posterior circulation CT"), ("race", "Prehospital LVO screen"), ("lams", "Prehospital motor scale"), ("abcd2", "Risk after TIA")],
    "mrs": [("nihss", "Acute neurological deficit"), ("aspects", "Early ischaemic change on CT"), ("gose", "Outcome after brain injury"), ("func", "Functional outcome after ICH")],
    "aspects": [("nihss", "Clinical deficit"), ("pcaspects", "Posterior circulation equivalent"), ("mrs", "Functional outcome")],
    "pcaspects": [("aspects", "Anterior circulation equivalent"), ("nihss", "Clinical deficit"), ("mrs", "Functional outcome")],
    "abcd2": [("nihss", "Neurological deficit"), ("mrs", "Functional status")],
    "race": [("lams", "Prehospital motor scale"), ("fasted", "Prehospital LVO scale"), ("nihss", "Full stroke scale"), ("aspects", "CT extent")],
    "lams": [("race", "Prehospital LVO scale"), ("fasted", "Prehospital LVO scale"), ("nihss", "Full stroke scale")],
    # ICH
    "ich": [("func", "Functional outcome"), ("gcs", "Input"), ("mrs", "Functional outcome scale"), ("graeb", "IVH burden")],
    "func": [("ich", "Severity and mortality grade"), ("mrs", "Functional outcome scale"), ("gcs", "Input")],
    # SAH
    "hunthess": [("wfns", "GCS-based clinical grade"), ("mfisher", "CT grade"), ("fisher", "Original CT grade"), ("gcs", "Level of consciousness")],
    "wfns": [("hunthess", "Alternative clinical grade"), ("mfisher", "CT grade"), ("fisher", "Original CT grade"), ("gcs", "Input")],
    "fisher": [("mfisher", "Modified version"), ("wfns", "Clinical grade"), ("hunthess", "Clinical grade")],
    "mfisher": [("fisher", "Original version"), ("wfns", "Clinical grade"), ("hunthess", "Clinical grade")],
    # Trauma
    "marshall": [("rotterdam", "Alternative CT score"), ("gcs", "Clinical severity"), ("gcsp", "Severity with pupils"), ("iss", "Anatomical injury severity")],
    "rotterdam": [("marshall", "CT classification"), ("gcs", "Clinical severity"), ("gcsp", "Severity with pupils"), ("gose", "Outcome after TBI")],
    "rts": [("iss", "Anatomical severity"), ("triss", "Combined survival model"), ("gcs", "Input")],
    "iss": [("rts", "Physiological severity"), ("triss", "Combined survival model"), ("marshall", "Head CT classification")],
    # Spine and spinal metastases
    "sins": [("rtokuhashi", "Prognosis in spinal metastases"), ("tomita", "Prognosis in spinal metastases"), ("kps", "Performance status"), ("ecog", "Performance status"), ("frankel", "Neurological status")],
    "rtokuhashi": [("sins", "Mechanical stability"), ("tomita", "Alternative prognostic score"), ("kps", "Input: general condition"), ("frankel", "Input: palsy")],
    "tomita": [("sins", "Mechanical stability"), ("rtokuhashi", "Alternative prognostic score"), ("kps", "Performance status")],
    "kps": [("ecog", "Alternative performance scale"), ("rtokuhashi", "Uses KPS"), ("sins", "Spinal metastasis stability")],
    "ecog": [("kps", "Alternative performance scale"), ("rtokuhashi", "Spinal metastasis prognosis"), ("tomita", "Spinal metastasis prognosis")],
    "frankel": [("nurick", "Myelopathy grade"), ("rtokuhashi", "Uses Frankel grade")],
    "nurick": [("mjoa", "Myelopathy score"), ("frankel", "Spinal cord injury grade")],
    # Neurocritical care
    "triss": [("rts", "Physiological component"), ("iss", "Anatomical component"), ("gcs", "Input to RTS")],
    "sofa": [("gcs", "CNS component")],
    "graeb": [("ich", "ICH severity grade"), ("mfisher", "SAH CT grade including IVH")],
    "fasted": [("race", "Prehospital LVO scale"), ("lams", "Prehospital motor scale"), ("nihss", "Full stroke scale")],
    "mjoa": [("nurick", "Myelopathy grade"), ("frankel", "Spinal cord injury grade")],
    "gpa": [("kps", "Input: performance status"), ("ecog", "Performance status")],
}
# Clinical clusters: restored verbatim from the earlier Phase 7 build output (content/related.json).
CLUSTERS = [
 {
  "id": "consciousness",
  "title": "Level of consciousness",
  "keywords": [
   "coma",
   "consciousness",
   "loc"
  ],
  "members": [
   "gcs",
   "gcsp",
   "gose",
   "gos"
  ],
  "description": "Bedside measures of responsiveness and their outcome counterparts."
 },
 {
  "id": "sah",
  "title": "SAH grading",
  "keywords": [
   "sah",
   "subarachnoid",
   "aneurysm",
   "vasospasm"
  ],
  "members": [
   "hunthess",
   "wfns",
   "fisher",
   "mfisher"
  ],
  "description": "Clinical grades (Hunt & Hess, WFNS) and CT grades (Fisher, Modified Fisher) are usually reported together."
 },
 {
  "id": "spinal-mets",
  "title": "Spinal metastases",
  "keywords": [
   "spinal metastasis",
   "metastases",
   "spine tumour",
   "spine tumor",
   "cancer"
  ],
  "members": [
   "sins",
   "rtokuhashi",
   "tomita",
   "kps",
   "ecog"
  ],
  "description": "Stability (SINS), prognosis (Tokuhashi, Tomita) and performance status (KPS, ECOG) inform multidisciplinary decisions together."
 },
 {
  "id": "acute-stroke",
  "title": "Acute stroke assessment",
  "keywords": [
   "stroke",
   "cva",
   "ischaemic",
   "ischemic"
  ],
  "members": [
   "nihss",
   "aspects",
   "pcaspects",
   "mrs"
  ],
  "description": "Clinical deficit (NIHSS), early CT change (ASPECTS) and pre-morbid / outcome function (mRS)."
 },
 {
  "id": "lvo",
  "title": "Prehospital LVO screens",
  "keywords": [
   "lvo",
   "large vessel occlusion",
   "prehospital",
   "ems"
  ],
  "members": [
   "race",
   "lams",
   "fasted",
   "nihss"
  ],
  "description": "Brief scales to estimate large vessel occlusion likelihood before imaging."
 },
 {
  "id": "tia",
  "title": "Transient ischaemic attack",
  "keywords": [
   "tia",
   "transient ischemic attack"
  ],
  "members": [
   "abcd2",
   "nihss"
  ],
  "description": "Early risk after TIA and assessment of any persisting deficit."
 },
 {
  "id": "ich",
  "title": "Intracerebral haemorrhage",
  "keywords": [
   "ich",
   "intracerebral hemorrhage",
   "haemorrhage",
   "hemorrhage",
   "bleed"
  ],
  "members": [
   "ich",
   "func",
   "graeb",
   "gcs"
  ],
  "description": "Severity (ICH Score), expected function (FUNC) and ventricular blood (Graeb)."
 },
 {
  "id": "tbi",
  "title": "Traumatic brain injury",
  "keywords": [
   "tbi",
   "head injury",
   "trauma"
  ],
  "members": [
   "gcs",
   "gcsp",
   "marshall",
   "rotterdam"
  ],
  "description": "Clinical severity with CT classification."
 },
 {
  "id": "trauma-severity",
  "title": "Trauma severity",
  "keywords": [
   "trauma",
   "polytrauma",
   "injury"
  ],
  "members": [
   "rts",
   "iss",
   "triss"
  ],
  "description": "Physiological (RTS) and anatomical (ISS) severity, combined in TRISS."
 },
 {
  "id": "outcome",
  "title": "Functional outcome",
  "keywords": [
   "outcome",
   "disability",
   "function"
  ],
  "members": [
   "mrs",
   "gos",
   "gose"
  ],
  "description": "Global outcome scales used at follow-up."
 },
 {
  "id": "myelopathy",
  "title": "Cervical myelopathy",
  "keywords": [
   "myelopathy",
   "dcm",
   "cervical spondylosis"
  ],
  "members": [
   "nurick",
   "mjoa",
  ],
  "description": "Walking-based (Nurick) and broader functional (mJOA) myelopathy scores."
 },
 {
  "id": "icu",
  "title": "Neurocritical care",
  "keywords": [
   "icu",
   "critical care"
  ],
  "members": [
   "sofa",
   "gcs"
  ],
  "description": "Arousal, coma and organ-dysfunction measures used in the ICU."
 }
]

CLUSTERS += [
 {"id": "motor-reflex", "title": "Motor and reflex examination", "keywords": ["power", "reflexes", "umn", "upper motor neuron"],
  "members": ["mrc", "mrcss", "dtr", "clonus", "plantar"], "description": "Bedside grades for strength, reflexes and upper motor neuron signs."},
 {"id": "spasticity", "title": "Spasticity", "keywords": ["spasticity", "tone", "contracture"],
  "members": ["mas", "mts", "clonus"], "description": "Resistance to passive movement, its velocity-dependent component, and clonus."},
 {"id": "cpa", "title": "Cerebellopontine angle", "keywords": ["vestibular schwannoma", "acoustic neuroma", "cpa", "facial nerve", "hearing"],
  "members": ["hb", "gr"], "description": "Facial nerve and hearing grades used before and after CPA surgery or radiosurgery."},
 {"id": "vascular-malformation", "title": "Vascular malformations", "keywords": ["avm", "davf", "fistula", "arteriovenous"],
  "members": ["spetzler", "lawtonyoung", "borden", "cognard"], "description": "Brain AVM grades and dural arteriovenous fistula classifications."},
 {"id": "epilepsy-surgery", "title": "Epilepsy surgery outcome", "keywords": ["epilepsy", "seizure", "epilepsy surgery"],
  "members": ["engel", "ilae"], "description": "Seizure outcome classifications after epilepsy surgery."},
]

CLUSTERS += [
 {"id": "stroke-mechanism", "title": "Stroke mechanism and prevention", "keywords": ["stroke subtype", "secondary prevention", "atrial fibrillation"],
  "members": ["toast", "ocsp", "chadsvasc", "hasbled"], "description": "Mechanism, syndrome and atrial fibrillation risk scores used after ischaemic stroke."},
 {"id": "thrombectomy", "title": "Thrombectomy", "keywords": ["thrombectomy", "reperfusion", "lvo"],
  "members": ["aspects", "collaterals", "mtici"], "description": "Imaging selection and angiographic grades around endovascular treatment."},
 {"id": "ich-expansion", "title": "ICH volume and expansion", "keywords": ["haematoma", "hematoma", "expansion"],
  "members": ["ichvolume", "bat", "ich"], "description": "Haematoma volume, expansion risk and severity."},
 {"id": "imaging-rules", "title": "Imaging decision rules", "keywords": ["head injury", "c-spine", "imaging"],
  "members": ["cchr", "nexus", "ccsr"], "description": "Validated rules for CT head and cervical spine imaging after trauma."},
 {"id": "spine-trauma", "title": "Spine trauma", "keywords": ["spine fracture", "spinal injury"],
  "members": ["slic", "tlics", "andersondalonzo", "levineedwards", "frankel"], "description": "Injury classifications for the cervical and thoracolumbar spine."},
 {"id": "degenerative-spine", "title": "Degenerative spine imaging", "keywords": ["degenerative", "mri spine"],
  "members": ["pfirrmann", "modic", "meyerding", "schizas"], "description": "MRI and radiograph grades of degenerative spine disease."},
 {"id": "pituitary", "title": "Pituitary adenoma", "keywords": ["pituitary", "sella"],
  "members": ["knosp", "hardy"], "description": "Cavernous sinus invasion and sellar/extrasellar extension."},
 {"id": "gbs", "title": "Guillain-Barré syndrome", "keywords": ["gbs", "guillain-barre"],
  "members": ["gbsds", "egos", "mrcss"], "description": "Disability, strength and prognosis in GBS."},
 {"id": "nerve-injury", "title": "Peripheral nerve injury", "keywords": ["nerve injury"],
  "members": ["seddon", "sunderland", "mrc"], "description": "Classifications of nerve injury with muscle power grading."},
]

CATEGORY_KEYWORDS = {
    "neurology": ["neurology", "parkinson", "neuromuscular", "myasthenia", "guillain-barre", "gbs"],
    "exam": ["examination", "neurological examination", "grade", "grades", "neurosurgery", "neurosurgical"],
    "consciousness": ["coma", "consciousness", "loc", "outcome", "brain injury"],
    "stroke": ["stroke", "tia", "lvo", "ischaemic", "ischemic", "thrombectomy", "cerebrovascular"],
    "ich": ["ich", "intracerebral", "haemorrhage", "hemorrhage", "bleed"],
    "sah": ["sah", "subarachnoid", "aneurysm", "aneurysmal", "vasospasm"],
    "tbi": ["tbi", "trauma", "head injury", "traumatic brain injury", "polytrauma"],
    "spine": ["spine", "spinal", "sci", "spinal cord", "myelopathy", "cervical"],
    "oncology": ["oncology", "tumour", "tumor", "cancer", "metastasis", "metastases", "spinal metastases"],
    "functional": ["outcome", "disability", "function", "functional"],
    "neurocritical": ["icu", "critical care", "intensive care"],
}
EXTRA_KEYWORDS = {"toast": ["ischaemic stroke", "ischemic stroke"], "ocsp": ["stroke syndrome"], "chadsvasc": ["atrial fibrillation", "af"], "hasbled": ["bleeding", "atrial fibrillation"],
                  "mtici": ["thrombectomy", "reperfusion"], "collaterals": ["thrombectomy"], "fazekas": ["white matter", "mri"], "ichvolume": ["haematoma", "hematoma"], "bat": ["haematoma expansion"],
                  "suzuki": ["moyamoya"], "raymondroy": ["aneurysm", "coiling"], "cchr": ["head injury", "ct head"], "nexus": ["c-spine", "neck"], "ccsr": ["c-spine", "neck"],
                  "slic": ["cervical spine"], "tlics": ["thoracolumbar"], "andersondalonzo": ["odontoid", "dens"], "levineedwards": ["hangman"], "pfirrmann": ["disc"], "modic": ["endplate"],
                  "meyerding": ["spondylolisthesis"], "schizas": ["stenosis"], "koos": ["vestibular schwannoma"], "simpson": ["meningioma"], "knosp": ["pituitary"], "hardy": ["pituitary"],
                  "lansky": ["paediatric", "pediatric"], "stess": ["status epilepticus"], "cpp": ["icp"], "osmolality": ["mannitol"], "hoehnyahr": ["parkinson"], "gbsds": ["guillain-barre"],
                  "egos": ["guillain-barre"], "mgfa": ["myasthenia"], "chiari": ["tonsillar"], "seddon": ["nerve injury"], "sunderland": ["nerve injury"],
                  "mrc": ["power", "weakness", "strength"], "mrcss": ["weakness", "icu"], "dtr": ["reflex", "reflexes"], "clonus": ["reflex", "umn"], "plantar": ["reflex", "umn"],
                  "mas": ["spasticity", "tone"], "mts": ["spasticity", "tone", "contracture"], "hb": ["facial nerve", "facial palsy", "cn vii"], "gr": ["hearing", "vestibular schwannoma", "cpa"],
                  "spetzler": ["avm"], "lawtonyoung": ["avm"], "borden": ["davf", "fistula"], "cognard": ["davf", "fistula"], "markwalder": ["csdh", "subdural"],
                  "engel": ["epilepsy", "seizure"], "ilae": ["epilepsy", "seizure"],
                  "sins": ["spinal metastases", "spine metastases"], "rtokuhashi": ["spinal metastases"], "tomita": ["spinal metastases"], "fasted": ["lvo", "prehospital"], "sofa": ["organ failure", "sepsis"], "triss": ["survival", "trauma"], "mjoa": ["myelopathy", "dcm"],
                  "graeb": ["ivh", "intraventricular"], "gpa": ["brain metastases"]}
