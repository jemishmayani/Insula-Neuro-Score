"""Item types and default Home groups (v0.11).

Every shipped item is one of four types, shown on its card and detail page:
  score           points or a model combine into a total (GCS, NIHSS, ISS, TRISS)
  grade           one ordinal level chosen from defined descriptions (MRC 0–5, House-Brackmann, mRS)
  classification  a category, not an ordinal severity (Fisher, Cognard, Engel, plantar response)
  measurement     a measured quantity (Modified Tardieu angles)
Grades and classifications are examination findings or categories, not prognostic scores.
"""
ITEM_TYPES = {
    "score": ["gcs", "gcsp", "nihss", "aspects", "pcaspects", "abcd2", "race", "lams", "fasted", "ich", "func", "graeb",
              "rotterdam", "rts", "iss", "triss", "sins", "mjoa", "rtokuhashi", "tomita", "gpa", "kps", "sofa", "mrcss"],
    "grade": ["mrc", "dtr", "mas", "hb", "hunthess", "wfns", "spetzler", "lawtonyoung", "markwalder", "frankel", "nurick", "ecog", "mrs"],
    "classification": ["fisher", "mfisher", "marshall", "gos", "gose", "borden", "cognard", "engel", "ilae", "gr", "clonus", "plantar"],
    "measurement": ["mts"],
}
TYPE_LABEL = {"score": "Score", "grade": "Grade", "classification": "Classification", "measurement": "Measurement"}
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
