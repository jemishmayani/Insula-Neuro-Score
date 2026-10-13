"""Item types and default Home groups (v0.11).

Every shipped item is one of four types, shown on its card and detail page:
  score           points or a model combine into a total (GCS, NIHSS, ISS, TRISS)
  grade           one ordinal level chosen from defined descriptions (MRC 0–5, House-Brackmann, mRS)
  classification  a category, not an ordinal severity (Fisher, Cognard, Engel, plantar response)
  measurement     a quantity calculated from measurements (Modified Tardieu angles, ICH volume, CPP)
  rule            a clinical decision rule (Canadian CT Head, NEXUS, Canadian C-spine)
Grades and classifications are examination findings or categories, not prognostic scores.
"""
ITEM_TYPES = {
    "score": ["gcs", "gcsp", "nihss", "aspects", "pcaspects", "abcd2", "race", "lams", "fasted", "ich", "func", "graeb",
              "rotterdam", "rts", "iss", "triss", "sins", "mjoa", "rtokuhashi", "tomita", "gpa", "kps", "sofa", "mrcss", "chadsvasc", "hasbled", "slic", "tlics", "bat", "stess", "egos", "lansky"],
    "grade": ["mrc", "dtr", "mas", "hb", "hunthess", "wfns", "spetzler", "lawtonyoung", "markwalder", "frankel", "nurick", "ecog", "mrs", "mtici", "collaterals", "fazekas", "suzuki", "pfirrmann", "meyerding", "schizas", "koos", "simpson", "knosp", "hardy", "hoehnyahr", "gbsds", "sunderland"],
    "classification": ["fisher", "mfisher", "marshall", "gos", "gose", "borden", "cognard", "engel", "ilae", "gr", "clonus", "plantar", "toast", "ocsp", "raymondroy", "andersondalonzo", "levineedwards", "modic", "mgfa", "chiari", "seddon"],
    "rule": ["cchr", "nexus", "ccsr"],
    "measurement": ["mts", "ichvolume", "cpp", "osmolality"],
}
TYPE_LABEL = {"score": "Score", "grade": "Grade", "classification": "Classification", "measurement": "Measurement", "rule": "Decision rule"}
TYPE_OF = {i: t for t, ids in ITEM_TYPES.items() for i in ids}

# Curated quick groups ("collections"): shown above the Scores & Grades groups and on Home by default.
COLLECTIONS = [
    {"id": "quick-exam", "name": "Quick Clinical Examination", "glyph": "exam", "collection": True,
     "description": "Bedside consciousness, power, facial nerve, reflex and tone grades",
     "include": ["gcs", "mrc", "hb", "dtr", "mas"]},
    {"id": "neurotrauma", "name": "Neurotrauma", "glyph": "tbi", "collection": True,
     "description": "Consciousness, CT classification and injury severity",
     "include": ["gcs", "gcsp", "marshall", "rotterdam", "iss"]},
    {"id": "vascular", "name": "Vascular", "glyph": "sah", "collection": True,
     "description": "SAH grades, AVM grade and dural fistula classifications",
     "include": ["hunthess", "wfns", "mfisher", "spetzler", "borden", "cognard"]},
]
DEFAULT_PRIORITY_GROUPS = [c["id"] for c in COLLECTIONS]

# v0.12 grouping: category sub-sections and cross-listing (a score keeps its own category; "include" lists it in another group too)
NEW_CATEGORIES = [{"id": "neurology", "name": "General neurology", "glyph": "neurology", "description": "Movement disorders and neuromuscular disease"}]
CATEGORY_GROUPS = {
    "stroke": [{"title": "Severity and prehospital triage", "members": ["nihss", "race", "lams", "fasted"]},
               {"title": "Mechanism and syndrome", "members": ["toast", "ocsp"]},
               {"title": "Imaging", "members": ["aspects", "pcaspects", "fazekas"]},
               {"title": "Thrombectomy", "members": ["mtici", "collaterals"]},
               {"title": "Risk", "members": ["abcd2", "chadsvasc", "hasbled"]}],
    "spine": [{"title": "Spine trauma", "members": ["nexus", "ccsr", "slic", "tlics", "andersondalonzo", "levineedwards"]},
              {"title": "Spinal cord injury and myelopathy", "members": ["frankel", "nurick", "mjoa"]},
              {"title": "Degenerative spine", "members": ["pfirrmann", "modic", "meyerding", "schizas"]},
              {"title": "Spinal tumour", "members": ["sins"]},
              {"title": "Craniovertebral junction", "members": ["chiari"]}],
    "oncology": [{"title": "Tumour grades", "members": ["koos", "simpson", "knosp", "hardy"]},
                 {"title": "Performance status", "members": ["kps", "ecog", "lansky"]},
                 {"title": "Spinal metastases", "members": ["sins", "rtokuhashi", "tomita"]},
                 {"title": "Brain metastases", "members": ["gpa"]}],
}
EXTRA_INCLUDES = {"oncology": ["sins"]}
EXAM_GROUP_ADDITIONS = {"Vascular neurosurgery": ["suzuki", "raymondroy"], "Hearing and CPA": ["koos"]}
EXAM_NEW_GROUPS = [{"title": "Peripheral nerve", "members": ["seddon", "sunderland"]}]
EXAM_EXTRA_INCLUDES = ["koos"]
