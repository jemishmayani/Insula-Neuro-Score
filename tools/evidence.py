"""Phase 9 — verification evidence per score.
Status values:
  "Verified"            matched a primary or authoritative source seen during this project
  "Verified (secondary)" matched several independent secondary sources (tables/protocols citing the original); primary full text not seen
  "Editorial"           written guidance (limitations, cautions) supported by sources but not a scoring rule; needs clinician review
  "FLAG"                uncertainty: manual verification required (see flags)
"""
V, VS, ED, F = "Verified", "Verified (secondary)", "Editorial", "FLAG"
EVIDENCE = {
 "gcs": dict(calc=V, interp=V, pop=V, lim=ED, src=V, basis="Glasgow structured approach (glasgowcomascale.org); Teasdale 2014; severity bands confirmed in CENTER-TBI/TRACK-TBI paper (Leiden)."),
 "gcsp": dict(calc=V, interp=F, pop=V, lim=ED, src=V, basis="Brennan, Murray & Teasdale 2018 abstract (University of Glasgow repository): GCS − non-reacting pupils, range 1–15.",
              flags=["The 1–8 'severe range' is not defined in the original publication (secondary sources only). Content now states this; clinician to confirm whether any band should be shown."]),
 "gos": dict(calc=V, interp=V, pop=V, lim=ED, src=V, basis="Jennett & Bond 1975 categories; Wilson et al. 1998 structured interview guidance."),
 "gose": dict(calc=V, interp=V, pop=V, lim=ED, src=V, basis="Wilson et al. 1998 (eight categories). Category recorder only; the copyrighted structured interview is required for reliable assignment."),
 "nihss": dict(calc=V, interp=V, pop=V, lim=ED, src=V, basis="NINDS NIH Stroke Scale PDF (Feb 2024), fetched directly: items, UN rules, coma rules; Martin-Schild 2011 (NIHSS 0).",
               flags=["UN (untestable) items contribute 0 and are flagged; NINDS does not define how UN enters the total. Convention to be confirmed by a stroke clinician.",
                      "Only two coma auto-scoring rules (items 8, 9) are encoded, as warnings; NINDS instructions for other items in coma not encoded."]),
 "mrs": dict(calc=V, interp=V, pop=V, lim=ED, src=V, basis="van Swieten 1988 standard wording, consistent across multiple trial protocols."),
 "aspects": dict(calc=VS, interp=V, pop=V, lim=ED, src=VS, basis="Barber 2000 region scheme via multiple independent descriptions (Radiopaedia, trial protocol, patent text)."),
 "pcaspects": dict(calc=VS, interp=V, pop=V, lim=ED, src=VS, basis="Puetz 2008 weights (thalami, cerebellar hemispheres, PCA territories 1; midbrain, pons 2) via multiple descriptions."),
 "abcd2": dict(calc=V, interp=V, pop=V, lim=ED, src=V, basis="Johnston 2007 Lancet abstract (PubMed): points, risk groups, 2-day risks."),
 "race": dict(calc=VS, interp=VS, pop=V, lim=ED, src=VS, basis="Pérez de la Ossa 2014 via official EMS cards citing the authors (items 0–9, aphasia/agnosia rule, ≥5 cut-off, sensitivity 0.85)."),
 "lams": dict(calc=VS, interp=VS, pop=V, lim=ED, src=VS, basis="Llanes 2004 items via AHA material; Nazliel 2008 (≥4) by title and summary.",
              flags=["Exact item wording ('drifts down', 'falls rapidly', 'weak grip', 'no grip') confirmed in secondary material only; check against Llanes 2004."]),
 "ich": dict(calc=V, interp=V, pop=V, lim=ED, src=V, basis="Hemphill 2001 abstract (Stroke 32:891): all points; mortality 0/13/26/72/97/100% from tables citing the paper.",
             flags=["Score 6: the app states no derivation patient scored 6 (abstract reports scores up to 5); some summaries list 6 as 100%. Confirm against the paper.",
                    "Removed unverified cohort size from content (sources give 152 and 161)."]),
 "func": dict(calc=V, interp=V, pop=V, lim=ED, src=V, basis="Rost 2008: component table (PMC) and outcome statements from the paper."),
 "hunthess": dict(calc=V, interp=V, pop=V, lim=ED, src=VS, basis="Grades and original modifier confirmed (BMJ Best Practice; independent descriptions). Grade IV wording corrected to include 'vegetative disturbances'."),
 "wfns": dict(calc=V, interp=V, pop=V, lim=ED, src=V, basis="Original 1988 table (GCS + motor deficit) confirmed in BMJ Best Practice; GCS 15 + deficit undefined."),
 "fisher": dict(calc=VS, interp=VS, pop=V, lim=ED, src=VS, basis="Fisher 1980 grade definitions and non-monotonic vasospasm relationship via multiple sources."),
 "mfisher": dict(calc=V, interp=V, pop=V, lim=ED, src=V, basis="Frontera 2006 abstract: grades and crude odds ratios (Phase 1 verification)."),
 "marshall": dict(calc=VS, interp=VS, pop=V, lim=ED, src=VS, basis="Marshall 1991 categories via Radiopaedia and published tables; order of precedence for derived category.",
                  flags=["Category is derived from findings using the standard order of precedence; confirm with a neuroradiologist for mixed-lesion edge cases."]),
 "rotterdam": dict(calc=VS, interp=VS, pop=V, lim=ED, src=VS, basis="Maas 2005 items (+1) and 6-month mortality by score via published tables."),
 "rts": dict(calc=V, interp=VS, pop=V, lim=ED, src=V, basis="Champion 1989 coded values and weights (Wikipedia/LITFL citing the paper; DOI confirmed).",
             flags=["The '<4' threshold is described in secondary sources as proposed for identifying severe injury; confirm wording."]),
 "iss": dict(calc=VS, interp=VS, pop=V, lim=ED, src=VS, basis="Baker 1974 sum-of-squares and AIS 6 = 75 rule; ISS >15 major-trauma convention (trial protocols, LITFL)."),
 "sins": dict(calc=V, interp=V, pop=V, lim=ED, src=V, basis="Fisher 2010 (SOSG) abstract; Fourney 2011; AJR 2014 worked examples (Phase 3)."),
 "frankel": dict(calc=VS, interp=VS, pop=V, lim=ED, src=VS, basis="Frankel 1969 grades A–E via multiple descriptions."),
 "nurick": dict(calc=VS, interp=VS, pop=V, lim=ED, src=VS, basis="Nurick 1972 (Brain) grades 0–5 via multiple descriptions."),
 "kps": dict(calc=V, interp=V, pop=V, lim=ED, src=VS, basis="KPS definitions confirmed in ECOG-ACRIN comparison table and trial protocols."),
 "ecog": dict(calc=V, interp=V, pop=V, lim=ED, src=V, basis="ECOG-ACRIN official page; Oken 1982 (Am J Clin Oncol 5:649-55); public domain (openEHR)."),
 "rtokuhashi": dict(calc=F, interp=V, pop=V, lim=ED, src=VS, basis="Tokuhashi 2005 parameters via WJO reviews and PMC tables.",
                    flags=["CONFLICT: 'Metastases in the vertebral body' is ≥3/2/1 in one reproduction and ≥3/1–2/0 in two others (WJO 2016, PMC review). Implementation uses ≥3/2/1. Verify against the original 2005 paper before clinical use. A notice in the calculator states this."]),
 "tomita": dict(calc=V, interp=V, pop=V, lim=ED, src=VS, basis="Tomita 2001 factors and points (1/2/4; 0/2/4; 1/2) via several independent tables.",
                flags=["One review table (Global Spine J 2018) gives 3 points for rapid growth; the original 2–10 range requires 4. Implementation uses 4; noted for review."]),
}
# Verified but held back from the app pending licensing review (content and tests retained).
HELD = {"rass": dict(calc=V, interp=V, pop=V, lim=ED, src=V, basis="All ten levels confirmed in multiple trial protocols citing Sessler 2002.",
                     flags=["Licensing: VCU lists RASS as a licensable technology; confirm terms before reinstating.",
                            "Terminology: 'Drowsy' sustained awakening is '>10 s' in most sources and '≥10 s' in VCU's description."])}
