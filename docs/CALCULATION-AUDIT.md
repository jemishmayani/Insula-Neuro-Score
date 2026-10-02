# Calculation audit

Derived automatically from the shipped score files through the production engine (`node tools/calc_audit.js`).

| Score | Method | Declared range | Reachable | Combinations evaluated | States reached | Missing → incomplete | NT behaviour | Issues |
|---|---|---|---|---|---|---|---|---|
| ABCD² | sum | 0–7 | 0–7 | 72 (all) | 3/3 | Yes | n/a | None |
| ASPECTS | expression | 0–10 | 0–10 | 1,024 (all) | 2/2 | Yes | n/a | None |
| ECOG | select | 0–5 | 0–5 | 6 (all) | 6/6 | Yes | n/a | None |
| Fisher | select | 1–4 | 1–4 | 4 (all) | 4/4 | Yes | n/a | None |
| Frankel | select | 1–5 | 1–5 | 5 (all) | 5/5 | Yes | n/a | None |
| FUNC | sum | 0–11 | 0–11 | 108 (all) | 3/3 | Yes | n/a | None |
| GCS | sum | 3–15 | 3–15 | 120 (all) | 4/4 | Yes | block | None |
| GCS-P | expression | 1–15 | 1–15 | 360 (all) | 3/3 | Yes | block | None |
| GOS | select | 1–5 | 1–5 | 5 (all) | 5/5 | Yes | n/a | None |
| GOSE | select | 1–8 | 1–8 | 8 (all) | 8/8 | Yes | n/a | None |
| Hunt & Hess | expression | 1–5 | 1–5 | 10 (all) | 5/5 | Yes | n/a | None |
| ICH Score | sum | 0–6 | 0–6 | 48 (all) | 7/7 | Yes | n/a | None |
| ISS | expression | 0–75 | 0–75 | 117,649 (all) | 4/4 | Yes | n/a | None |
| KPS | select | 0–100 | 0–100 | 11 (all) | 5/5 | Yes | n/a | None |
| LAMS | sum | 0–5 | 0–5 | 18 (all) | 2/2 | Yes | n/a | None |
| Marshall | expression | 1–6 | 1–6 | 32 (all) | 6/6 | Yes | n/a | None |
| mFisher | expression | -1–4 | -1–4 | 6 (all) | 6/6 | Yes | n/a | None |
| mRS | select | 0–6 | 0–6 | 7 (all) | 7/7 | Yes | n/a | None |
| NIHSS | sum | 0–42 | 0–42 | 300,059 (sample) | 2/2 | Yes | exclude | None |
| Nurick | select | 0–5 | 0–5 | 6 (all) | 6/6 | Yes | n/a | None |
| pc-ASPECTS | expression | 0–10 | 0–10 | 256 (all) | 2/2 | Yes | n/a | None |
| RACE | sum | 0–9 | 0–9 | 162 (all) | 2/2 | Yes | n/a | None |
| Rotterdam | expression | 1–6 | 1–6 | 24 (all) | 6/6 | Yes | n/a | None |
| Revised Tokuhashi | sum | 0–15 | 0–15 | 1,458 (all) | 3/3 | Yes | n/a | None |
| RTS | expression | 0–7.8408 | 0–7.8408 | 3,328 (all) | 3/3 | Yes | n/a | None |
| SINS | sum | 0–18 | 0–18 | 1,296 (all) | 3/3 | Yes | n/a | None |
| Tomita | sum | 2–10 | 2–10 | 18 (all) | 1/1 | Yes | n/a | None |
| WFNS | expression | 0–5 | 0–5 | 26 (all) | 6/6 | Yes | n/a | None |

## Per-score detail

### ABCD²

Version: ABCD² (Johnston et al. 2007). Method: `sum`.

| Component | Points |
|---|---|
| Age | 0=0, 1=1 |
| Blood pressure at first assessment | 0=0, 1=1 |
| Clinical features | 0=0, 1=1, 2=2 |
| Duration of symptoms | 0=0, 1=1, 2=2 |
| Diabetes | no=0, yes=1 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Lower risk group | low | 0–3 | 0–3 |
| Moderate risk group | moderate | 4–5 | 4–5 |
| Higher risk group | high | 6–7 | 6–7 |

Boundaries: 3→4: low → moderate; 5→6: moderate → high

### ASPECTS

Version: ASPECTS (Barber et al. 2000), non-contrast CT. Method: `expression: 10 - regions`.

| Component | Points |
|---|---|
| Regions with early ischaemic change | c=1, l=1, ic=1, i=1, m1=1, m2=1, m3=1, m4=1, m5=1, m6=1, none=0 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| No early ischaemic change | favorable | 10 | 10 |
| ASPECTS {total} | informational | 0–9 | 0–9 |

Boundaries: 9→10: scored → ten

### ECOG

Version: ECOG Performance Status (Oken et al. 1982). Method: `select`.

| Component | Points |
|---|---|
| Grade | 0=0, 1=1, 2=2, 3=3, 4=4, 5=5 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| ECOG 0 | favorable | 0 | 0 |
| ECOG 1 | informational | 1 | 1 |
| ECOG 2 | informational | 2 | 2 |
| ECOG 3 | informational | 3 | 3 |
| ECOG 4 | informational | 4 | 4 |
| ECOG 5 | informational | 5 | 5 |

Boundaries: 0→1: g0 → g1; 1→2: g1 → g2; 2→3: g2 → g3; 3→4: g3 → g4; 4→5: g4 → g5

### Fisher

Version: Original Fisher scale (1980). Method: `select`.

| Component | Points |
|---|---|
| CT appearance | 1=1, 2=2, 3=3, 4=4 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Grade 1 | favorable | 1 | 1 |
| Grade 2 | mild | 2 | 2 |
| Grade 3 | high | 3 | 3 |
| Grade 4 | moderate | 4 | 4 |

Boundaries: 1→2: g1 → g2; 2→3: g2 → g3; 3→4: g3 → g4

### Frankel

Version: Frankel grade (Frankel et al. 1969). Method: `select`.

| Component | Points |
|---|---|
| Neurological function below the injury | A=1, B=2, C=3, D=4, E=5 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Grade A: complete | high | A | 1 |
| Grade B: sensory only | high | B | 2 |
| Grade C: motor useless | moderate | C | 3 |
| Grade D: motor useful | mild | D | 4 |
| Grade E: recovery | favorable | E | 5 |

Boundaries: 1→2: g1 → g2; 2→3: g2 → g3; 3→4: g3 → g4; 4→5: g4 → g5

### FUNC

Version: FUNC (Rost et al. 2008). Method: `sum`.

| Component | Points |
|---|---|
| ICH volume | 4=4, 2=2, 0=0 |
| Age | 2=2, 1=1, 0=0 |
| ICH location | 2=2, 1=1, 0=0 |
| GCS | 2=2, 0=0 |
| Pre-ICH cognitive impairment | 1=1, 0=0 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| FUNC 0–4 | high | 0–4 | 0–4 |
| FUNC {total} | informational | 5–10 | 5–10 |
| FUNC 11 | favorable | 11 | 11 |

Boundaries: 4→5: low4 → mid; 10→11: mid → top

### GCS

Version: Adult GCS, Glasgow structured approach. Method: `sum`.

| Component | Points |
|---|---|
| Eye opening (E) · NT (Periorbital swelling/Dressing or bandage/Other local factor) | E4=4, E3=3, E2=2, E1=1 |
| Verbal response (V) · NT (Endotracheal tube or tracheostomy/Other factor interfering with communication) | V5=5, V4=4, V3=3, V2=2, V1=1 |
| Best motor response (M) · NT (Paralysed/Other limiting factor) | M6=6, M5=5, M4=4, M3=3, M2=2, M1=1 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Severe impairment | high | 3–8 | 3–8 |
| Moderate impairment | moderate | 9–12 | 9–12 |
| Mild impairment | low | 13–14 | 13–14 |
| No impairment measured | favorable | 15 | 15 |

Boundaries: 8→9: severe → moderate; 12→13: moderate → mild; 14→15: mild → none

Not testable: e → not-interpretable; v → not-interpretable; m → not-interpretable

### GCS-P

Version: GCS-P (Brennan, Murray & Teasdale 2018). Method: `expression: e + v + m - prs`.

| Component | Points |
|---|---|
| Eye opening (E) · NT (Periorbital swelling/Dressing or bandage/Other local factor) | E4=4, E3=3, E2=2, E1=1 |
| Verbal response (V) · NT (Endotracheal tube or tracheostomy/Other factor interfering with communication) | V5=5, V4=4, V3=3, V2=2, V1=1 |
| Best motor response (M) · NT (Paralysed/Other limiting factor) | M6=6, M5=5, M4=4, M3=3, M2=2, M1=1 |
| Pupil reactivity to light · NT (Ocular trauma/Prior eye surgery or disease/Drug effect on pupils) | PRS 0=0, PRS 1=1, PRS 2=2 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Severe range | high | 1–8 | 1–8 |
| Above the severe range | informational | 9–14 | 9–14 |
| No impairment measured | favorable | 15 | 15 |

Boundaries: 8→9: severe → above; 14→15: above → none

Not testable: e → not-interpretable; v → not-interpretable; m → not-interpretable; prs → not-interpretable

### GOS

Version: GOS, five categories (Jennett & Bond 1975). Method: `select`.

| Component | Points |
|---|---|
| Outcome category | 1=1, 2=2, 3=3, 4=4, 5=5 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Death | informational | 1 | 1 |
| Vegetative state | informational | 2 | 2 |
| Severe disability | informational | 3 | 3 |
| Moderate disability | informational | 4 | 4 |
| Good recovery | favorable | 5 | 5 |

Boundaries: 1→2: g1 → g2; 2→3: g2 → g3; 3→4: g3 → g4; 4→5: g4 → g5

### GOSE

Version: GOSE, eight categories (Wilson et al. 1998). Method: `select`.

| Component | Points |
|---|---|
| GOSE category | 1=1, 2=2, 3=3, 4=4, 5=5, 6=6, 7=7, 8=8 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Death | informational | 1 | 1 |
| Vegetative state | informational | 2 | 2 |
| Lower severe disability | informational | 3 | 3 |
| Upper severe disability | informational | 4 | 4 |
| Lower moderate disability | informational | 5 | 5 |
| Upper moderate disability | informational | 6 | 6 |
| Lower good recovery | informational | 7 | 7 |
| Upper good recovery | favorable | 8 | 8 |

Boundaries: 1→2: g1 → g2; 2→3: g2 → g3; 3→4: g3 → g4; 4→5: g4 → g5; 5→6: g5 → g6; 6→7: g6 → g7; 7→8: g7 → g8

### Hunt & Hess

Version: Hunt & Hess 1968 (original, with modifier). Method: `expression: min(5, grade + mod)`.

| Component | Points |
|---|---|
| Clinical presentation | I=1, II=2, III=3, IV=4, V=5 |
| Serious systemic disease or severe arteriographic vasospasm | no=0, yes=1 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Grade I | low | I | 1 |
| Grade II | mild | II | 2 |
| Grade III | moderate | III | 3 |
| Grade IV | high | IV | 4 |
| Grade V | high | V | 5 |

Boundaries: 1→2: g1 → g2; 2→3: g2 → g3; 3→4: g3 → g4; 4→5: g4 → g5

### ICH Score

Version: ICH Score (Hemphill et al. 2001). Method: `sum`.

| Component | Points |
|---|---|
| GCS at presentation | 0=0, 1=1, 2=2 |
| ICH volume (initial CT) | 0=0, 1=1 |
| Intraventricular haemorrhage | no=0, yes=1 |
| Origin | 0=0, 1=1 |
| Age | 0=0, 1=1 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Score 0 | favorable | 0 | 0 |
| Score 1 | low | 1 | 1 |
| Score 2 | moderate | 2 | 2 |
| Score 3 | high | 3 | 3 |
| Score 4 | critical | 4 | 4 |
| Score 5 | critical | 5 | 5 |
| Score 6 | critical | 6 | 6 |

Boundaries: 0→1: s0 → s1; 1→2: s1 → s2; 2→3: s2 → s3; 3→4: s3 → s4; 4→5: s4 → s5; 5→6: s5 → s6

### ISS

Version: ISS (Baker et al. 1974). Method: `expression: l1 == 6 ? 75 : l1 * l1 + l2 * l2 + l3 * l3`.

| Component | Points |
|---|---|
| Head or neck | 0–6 |
| Face | 0–6 |
| Chest | 0–6 |
| Abdomen or pelvic contents | 0–6 |
| Extremities or pelvic girdle | 0–6 |
| External | 0–6 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| No injury recorded | favorable | 0 | 0 |
| ISS {total} | informational | 1–15 | 1–14 |
| ISS {total}: above 15 | high | 16–74 | 16–66 |
| ISS 75 | critical | 75 | 75 |

Boundaries: 0→1: none → below; 14→16: below → major; 66→75: major → max

### KPS

Version: Karnofsky Performance Status (Karnofsky 1949). Method: `select`.

| Component | Points |
|---|---|
| Performance level | 100=100, 90=90, 80=80, 70=70, 60=60, 50=50, 40=40, 30=30, 20=20, 10=10, 0=0 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| KPS 100 | favorable | 100 | 100 |
| KPS {total} | informational | 80–90 | 80–90 |
| KPS {total} | informational | 50–70 | 50–70 |
| KPS {total} | informational | 10–40 | 10–40 |
| KPS 0 | informational | 0 | 0 |

Boundaries: 0→10: dead → dependent; 40→50: dependent → self; 70→80: self → normal_act; 90→100: normal_act → k100

### LAMS

Version: LAMS (Llanes et al. 2004). Method: `sum`.

| Component | Points |
|---|---|
| Facial droop | 0=0, 1=1 |
| Arm drift | 0=0, 1=1, 2=2 |
| Grip strength | 0=0, 1=1, 2=2 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Below the ≥4 cut-off | informational | 0–3 | 0–3 |
| At or above the ≥4 cut-off | high | 4–5 | 4–5 |

Boundaries: 3→4: below → above

### Marshall

Version: Marshall CT classification (1991). Method: `expression: evac == 1 ? 5 : mass == 1 ? 6 : shift == 1 ? 4 : cisterns == 1 ? 3 : path == 1 ? 2 : 1`.

| Component | Points |
|---|---|
| Any lesion surgically evacuated | no=0, yes=1 |
| High- or mixed-density lesion >25 mL (not evacuated) | no=0, yes=1 |
| Midline shift greater than 5 mm | no=0, yes=1 |
| Basal cisterns | 0=0, 1=1 |
| Any visible intracranial pathology | no=0, yes=1 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Diffuse injury I | favorable | I | 1 |
| Diffuse injury II | low | II | 2 |
| Diffuse injury III (swelling) | moderate | III | 3 |
| Diffuse injury IV (shift) | high | IV | 4 |
| Evacuated mass lesion (V) | high | V | 5 |
| Non-evacuated mass lesion (VI) | high | VI | 6 |

Boundaries: 1→2: c1 → c2; 2→3: c2 → c3; 3→4: c3 → c4; 4→5: c4 → c5; 5→6: c5 → c6

### mFisher

Version: Modified Fisher (Frontera et al. 2006). Method: `expression: sah == 0 ? (ivh == 0 ? 0 : -1) : sah == 1 ? (ivh == 1 ? 2 : 1) : (ivh == 1 ? 4 : 3)`.

| Component | Points |
|---|---|
| Cisternal subarachnoid blood | 0=0, 1=1, 2=2 |
| Intraventricular haemorrhage | no=0, yes=1 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Not defined | incomplete | IVH only | -1 |
| Grade 0 | favorable | 0 | 0 |
| Grade 1 | low | 1 | 1 |
| Grade 2 | moderate | 2 | 2 |
| Grade 3 | moderate | 3 | 3 |
| Grade 4 | high | 4 | 4 |

Boundaries: -1→0: undef → g0; 0→1: g0 → g1; 1→2: g1 → g2; 2→3: g2 → g3; 3→4: g3 → g4

### mRS

Version: Modified Rankin Scale 0–6 (van Swieten et al. 1988). Method: `select`.

| Component | Points |
|---|---|
| Functional level | 0=0, 1=1, 2=2, 3=3, 4=4, 5=5, 6=6 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| No symptoms | favorable | 0 | 0 |
| No significant disability | informational | 1 | 1 |
| Slight disability | informational | 2 | 2 |
| Moderate disability | informational | 3 | 3 |
| Moderately severe disability | informational | 4 | 4 |
| Severe disability | informational | 5 | 5 |
| Dead | informational | 6 | 6 |

Boundaries: 0→1: g0 → g1; 1→2: g1 → g2; 2→3: g2 → g3; 3→4: g3 → g4; 4→5: g4 → g5; 5→6: g5 → g6

### NIHSS

Version: NINDS NIH Stroke Scale (2024 update), 15 items. Method: `sum`.

| Component | Points |
|---|---|
| 1a. Level of consciousness | 0=0, 1=1, 2=2, 3=3 |
| 1b. LOC questions | 0=0, 1=1, 2=2 |
| 1c. LOC commands | 0=0, 1=1, 2=2 |
| 2. Best gaze | 0=0, 1=1, 2=2 |
| 3. Visual | 0=0, 1=1, 2=2, 3=3 |
| 4. Facial palsy | 0=0, 1=1, 2=2, 3=3 |
| 5a. Motor arm, left · NT (Amputation/Joint fusion) | 0=0, 1=1, 2=2, 3=3, 4=4 |
| 5b. Motor arm, right · NT (Amputation/Joint fusion) | 0=0, 1=1, 2=2, 3=3, 4=4 |
| 6a. Motor leg, left · NT (Amputation/Joint fusion) | 0=0, 1=1, 2=2, 3=3, 4=4 |
| 6b. Motor leg, right · NT (Amputation/Joint fusion) | 0=0, 1=1, 2=2, 3=3, 4=4 |
| 7. Limb ataxia · NT (Amputation/Joint fusion) | 0=0, 1=1, 2=2 |
| 8. Sensory | 0=0, 1=1, 2=2 |
| 9. Best language | 0=0, 1=1, 2=2, 3=3 |
| 10. Dysarthria · NT (Intubated/Other physical barrier to speech) | 0=0, 1=1, 2=2 |
| 11. Extinction and inattention | 0=0, 1=1, 2=2 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| No measurable deficit | favorable | 0 | 0 |
| NIHSS {total} | informational | 1–42 | 1–42 |

Boundaries: 0→1: zero → scored

Not testable: item_5a → complete (total 0); item_5b → complete (total 0); item_6a → complete (total 0); item_6b → complete (total 0); item_7 → complete (total 0); item_10 → complete (total 0)

### Nurick

Version: Nurick grade (1972). Method: `select`.

| Component | Points |
|---|---|
| Grade | 0=0, 1=1, 2=2, 3=3, 4=4, 5=5 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Grade 0 | informational | 0 | 0 |
| Grade 1 | informational | 1 | 1 |
| Grade 2 | informational | 2 | 2 |
| Grade 3 | informational | 3 | 3 |
| Grade 4 | informational | 4 | 4 |
| Grade 5 | informational | 5 | 5 |

Boundaries: 0→1: g0 → g1; 1→2: g1 → g2; 2→3: g2 → g3; 3→4: g3 → g4; 4→5: g4 → g5

### pc-ASPECTS

Version: pc-ASPECTS (Puetz et al. 2008). Method: `expression: 10 - regions`.

| Component | Points |
|---|---|
| Regions with early ischaemic change | lt=1, rt=1, lc=1, rc=1, lp=1, rp=1, mb=2, po=2, none=0 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| No early ischaemic change | favorable | 10 | 10 |
| pc-ASPECTS {total} | informational | 0–9 | 0–9 |

Boundaries: 9→10: scored → ten

### RACE

Version: RACE (Pérez de la Ossa et al. 2014). Method: `sum`.

| Component | Points |
|---|---|
| Facial palsy | 0=0, 1=1, 2=2 |
| Arm motor function | 0=0, 1=1, 2=2 |
| Leg motor function | 0=0, 1=1, 2=2 |
| Head and gaze deviation | 0=0, 1=1 |
| Aphasia (right hemiparesis) or agnosia (left hemiparesis) | 0=0, 1=1, 2=2 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Below the derivation cut-off | informational | 0–4 | 0–4 |
| At or above the derivation cut-off | high | 5–9 | 5–9 |

Boundaries: 4→5: below → above

### Rotterdam

Version: Rotterdam CT score (Maas et al. 2005). Method: `expression: cisterns + shift + edh + ivh + 1`.

| Component | Points |
|---|---|
| Basal cisterns | 0=0, 1=1, 2=2 |
| Midline shift | 0=0, 1=1 |
| Epidural mass lesion | 0=0, 1=1 |
| Intraventricular blood or traumatic SAH | 0=0, 1=1 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Score 1 | favorable | 1 | 1 |
| Score 2 | low | 2 | 2 |
| Score 3 | mild | 3 | 3 |
| Score 4 | moderate | 4 | 4 |
| Score 5 | high | 5 | 5 |
| Score 6 | critical | 6 | 6 |

Boundaries: 1→2: s1 → s2; 2→3: s2 → s3; 3→4: s3 → s4; 4→5: s4 → s5; 5→6: s5 → s6

### Revised Tokuhashi

Version: Revised Tokuhashi (Tokuhashi et al. 2005). Method: `sum`.

| Component | Points |
|---|---|
| General condition (KPS) | 0=0, 1=1, 2=2 |
| Extraspinal bone metastasis foci | 0=0, 1=1, 2=2 |
| Metastases in the vertebral body | 0=0, 1=1, 2=2 |
| Metastases to major internal organs | 0=0, 1=1, 2=2 |
| Primary site | p0=0, p1=1, p2=2, p3=3, p4=4, p5=5 |
| Spinal cord palsy | 0=0, 1=1, 2=2 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Predicted <6 months | high | 0–8 | 0–8 |
| Predicted ≥6 months | moderate | 9–11 | 9–11 |
| Predicted ≥1 year | low | 12–15 | 12–15 |

Boundaries: 8→9: short → mid; 11→12: mid → long

### RTS

Version: RTS (Champion et al. 1989), weighted. Method: `expression: 0.9368 * gcs + 0.7326 * sbp + 0.2908 * rr`.

| Component | Points |
|---|---|
| GCS total | …–3→0, 4–5→1, 6–8→2, 9–12→3, 13–…→4 |
| Systolic blood pressure | …–0→0, 1–49→1, 50–75→2, 76–89→3, 90–…→4 |
| Respiratory rate | …–0→0, 1–5→1, 6–9→2, 10–29→4, 30–…→3 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| All coded values normal | favorable | 7.8408 | 7.8408 |
| RTS {fixed(total, 4)} | informational | 4–7.84 | 4.007–7.55 |
| RTS below 4 | high | < 4 | 0–3.9736 |

Boundaries: 3.9736→4.007: low4 → mid; 7.55→7.8408: mid → full

### SINS

Version: SOSG SINS (Fisher et al. 2010). Method: `sum`.

| Component | Points |
|---|---|
| Location | 3=3, 2=2, 1=1, 0=0 |
| Pain | 3=3, 1=1, 0=0 |
| Bone lesion | 2=2, 1=1, 0=0 |
| Radiographic spinal alignment | 4=4, 2=2, 0=0 |
| Vertebral body collapse | 3=3, 2=2, 1=1, 0=0 |
| Posterolateral involvement of spinal elements | 3=3, 1=1, 0=0 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Stable | favorable | 0–6 | 0–6 |
| Potentially unstable | moderate | 7–12 | 7–12 |
| Unstable | high | 13–18 | 13–18 |

Boundaries: 6→7: stable → potential; 12→13: potential → unstable

### Tomita

Version: Tomita score (Tomita et al. 2001). Method: `sum`.

| Component | Points |
|---|---|
| Primary tumour growth | 1=1, 2=2, 4=4 |
| Visceral metastases | 0=0, 2=2, 4=4 |
| Bone metastases | 1=1, 2=2 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Tomita {total} | informational | 2–10 | 2–10 |

Boundaries: none (single state)

### WFNS

Version: Original WFNS (1988). Method: `expression: gcs == 15 ? (deficit == 0 ? 1 : 0) : gcs >= 13 ? (deficit == 0 ? 2 : 3) : gcs >= 7 ? 4 : 5`.

| Component | Points |
|---|---|
| GCS total | 3–15 |
| Major focal neurological deficit | no=0, yes=1 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Not defined in original WFNS | incomplete | GCS 15 + deficit | 0 |
| Grade I | low | I | 1 |
| Grade II | mild | II | 2 |
| Grade III | moderate | III | 3 |
| Grade IV | high | IV | 4 |
| Grade V | high | V | 5 |

Boundaries: 0→1: undef → g1; 1→2: g1 → g2; 2→3: g2 → g3; 3→4: g3 → g4; 4→5: g4 → g5

