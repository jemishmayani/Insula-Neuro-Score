"""Curated clinical relationships between scores (contextual links shown in every Guide).
Kept in one place so relationships can be reviewed together. Ids may point to scores under review."""
RELATED = {
    # Consciousness / outcome
    "gcs": [("gcsp", "Adds pupil reactivity"), ("four", "Coma scale without a verbal component"), ("gose", "Outcome after brain injury"), ("wfns", "SAH grade built on GCS"), ("rass", "Arousal and sedation in ICU")],
    "gcsp": [("gcs", "Underlying scale"), ("four", "Includes brainstem reflexes"), ("gose", "Outcome after brain injury"), ("rotterdam", "CT prognostic score in TBI")],
    "gos": [("gose", "Extended 8-category version"), ("gcs", "Acute level of consciousness"), ("mrs", "Global disability scale")],
    "gose": [("gos", "Original 5-category scale"), ("gcs", "Acute level of consciousness"), ("gcsp", "Acute severity with pupils"), ("mrs", "Global disability scale")],
    # Stroke
    "nihss": [("aspects", "Early ischaemic change on CT"), ("mrs", "Functional outcome"), ("pcaspects", "Posterior circulation CT"), ("race", "Prehospital LVO screen"), ("lams", "Prehospital motor scale"), ("abcd2", "Risk after TIA")],
    "mrs": [("nihss", "Acute neurological deficit"), ("aspects", "Early ischaemic change on CT"), ("gose", "Outcome after brain injury"), ("func", "Functional outcome after ICH")],
    "aspects": [("nihss", "Clinical deficit"), ("pcaspects", "Posterior circulation equivalent"), ("mrs", "Functional outcome")],
    "pcaspects": [("aspects", "Anterior circulation equivalent"), ("nihss", "Clinical deficit"), ("mrs", "Functional outcome")],
    "abcd2": [("nihss", "Neurological deficit"), ("mrs", "Functional status")],
    "race": [("lams", "Prehospital motor scale"), ("fasted", "Prehospital LVO scale (under review)"), ("nihss", "Full stroke scale"), ("aspects", "CT extent")],
    "lams": [("race", "Prehospital LVO scale"), ("fasted", "Prehospital LVO scale (under review)"), ("nihss", "Full stroke scale")],
    # ICH
    "ich": [("func", "Functional outcome"), ("gcs", "Input"), ("mrs", "Functional outcome scale"), ("graeb", "IVH burden (under review)")],
    "func": [("ich", "Severity and mortality grade"), ("mrs", "Functional outcome scale"), ("gcs", "Input")],
    # SAH
    "hunthess": [("wfns", "GCS-based clinical grade"), ("mfisher", "CT grade"), ("fisher", "Original CT grade"), ("gcs", "Level of consciousness")],
    "wfns": [("hunthess", "Alternative clinical grade"), ("mfisher", "CT grade"), ("fisher", "Original CT grade"), ("gcs", "Input")],
    "fisher": [("mfisher", "Modified version"), ("wfns", "Clinical grade"), ("hunthess", "Clinical grade")],
    "mfisher": [("fisher", "Original version"), ("wfns", "Clinical grade"), ("hunthess", "Clinical grade")],
    # Trauma
    "marshall": [("rotterdam", "Alternative CT score"), ("gcs", "Clinical severity"), ("gcsp", "Severity with pupils"), ("iss", "Anatomical injury severity")],
    "rotterdam": [("marshall", "CT classification"), ("gcs", "Clinical severity"), ("gcsp", "Severity with pupils"), ("gose", "Outcome after TBI")],
    "rts": [("iss", "Anatomical severity"), ("triss", "Combined survival model (under review)"), ("gcs", "Input")],
    "iss": [("rts", "Physiological severity"), ("triss", "Combined survival model (under review)"), ("marshall", "Head CT classification")],
    # Spine and spinal metastases
    "sins": [("rtokuhashi", "Prognosis in spinal metastases"), ("tomita", "Prognosis in spinal metastases"), ("kps", "Performance status"), ("ecog", "Performance status"), ("frankel", "Neurological status")],
    "rtokuhashi": [("sins", "Mechanical stability"), ("tomita", "Alternative prognostic score"), ("kps", "Input: general condition"), ("frankel", "Input: palsy")],
    "tomita": [("sins", "Mechanical stability"), ("rtokuhashi", "Alternative prognostic score"), ("kps", "Performance status")],
    "kps": [("ecog", "Alternative performance scale"), ("rtokuhashi", "Uses KPS"), ("sins", "Spinal metastasis stability")],
    "ecog": [("kps", "Alternative performance scale"), ("rtokuhashi", "Spinal metastasis prognosis"), ("tomita", "Spinal metastasis prognosis")],
    "frankel": [("ais", "Current standard (under review)"), ("nurick", "Myelopathy grade"), ("rtokuhashi", "Uses Frankel grade")],
    "nurick": [("mjoa", "Myelopathy score (under review)"), ("frankel", "Spinal cord injury grade")],
    # Neurocritical care
    "triss": [("rts", "Physiological component"), ("iss", "Anatomical component"), ("gcs", "Input to RTS")],
    "sofa": [("sofa2", "Updated version (under review)"), ("gcs", "CNS component"), ("rass", "Sedation level (under review)")],
    "graeb": [("ich", "ICH severity grade"), ("mgraeb", "Modified version (under review)"), ("mfisher", "SAH CT grade including IVH")],
    "fasted": [("race", "Prehospital LVO scale"), ("lams", "Prehospital motor scale"), ("nihss", "Full stroke scale")],
    "mjoa": [("nurick", "Myelopathy grade"), ("joa", "Original JOA (under review)"), ("frankel", "Spinal cord injury grade")],
    "gpa": [("dsgpa", "Disease-specific versions (under review)"), ("kps", "Input: performance status"), ("ecog", "Performance status")],
    "rass": [("gcs", "Level of consciousness"), ("four", "Coma scale (under review)"), ("sofa", "Organ dysfunction")],
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
   "four",
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
   "mgraeb",
   "gcs"
  ],
  "description": "Severity (ICH Score), expected function (FUNC) and ventricular blood (Graeb, under review)."
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
  "description": "Physiological (RTS) and anatomical (ISS) severity, combined in TRISS (under review)."
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
  "id": "sci",
  "title": "Spinal cord injury",
  "keywords": [
   "sci",
   "spinal cord injury",
   "paraplegia",
   "tetraplegia"
  ],
  "members": [
   "frankel",
   "ais"
  ],
  "description": "Frankel grade and the current ASIA/ISNCSCI standard (under review)."
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
   "joa"
  ],
  "description": "Walking-based (Nurick) and broader functional scores (mJOA, JOA; under review)."
 },
 {
  "id": "icu",
  "title": "Neurocritical care",
  "keywords": [
   "icu",
   "sedation",
   "critical care"
  ],
  "members": [
   "rass",
   "four",
   "sofa",
   "gcs"
  ],
  "description": "Arousal, coma and organ-dysfunction measures used in the ICU."
 }
]

CATEGORY_KEYWORDS = {
    "consciousness": ["coma", "consciousness", "loc", "outcome", "brain injury"],
    "stroke": ["stroke", "tia", "lvo", "ischaemic", "ischemic", "thrombectomy", "cerebrovascular"],
    "ich": ["ich", "intracerebral", "haemorrhage", "hemorrhage", "bleed"],
    "sah": ["sah", "subarachnoid", "aneurysm", "aneurysmal", "vasospasm"],
    "tbi": ["tbi", "trauma", "head injury", "traumatic brain injury", "polytrauma"],
    "spine": ["spine", "spinal", "sci", "spinal cord", "myelopathy", "cervical"],
    "oncology": ["oncology", "tumour", "tumor", "cancer", "metastasis", "metastases", "spinal metastases"],
    "functional": ["outcome", "disability", "function", "functional"],
    "neurocritical": ["icu", "critical care", "intensive care", "sedation"],
}
EXTRA_KEYWORDS = {"sins": ["spinal metastases", "spine metastases"], "rtokuhashi": ["spinal metastases"], "tomita": ["spinal metastases"],
                  "four": ["coma", "brainstem"], "fasted": ["lvo", "prehospital"], "sofa": ["organ failure", "sepsis"], "sofa2": ["organ failure", "sepsis"], "dsgpa": ["brain metastases"], "triss": ["survival", "trauma"],
                  "ais": ["asia", "isncsci", "spinal cord injury"], "mjoa": ["myelopathy", "dcm"], "joa": ["myelopathy"], "odi": ["back pain", "disability"],
                  "graeb": ["ivh", "intraventricular"], "mgraeb": ["ivh", "intraventricular"], "gpa": ["brain metastases"], "tokuhashi": ["spinal metastases"]}
