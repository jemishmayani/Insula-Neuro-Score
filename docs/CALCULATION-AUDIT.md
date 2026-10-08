# Calculation audit

Derived automatically from the shipped score files through the production engine (`node tools/calc_audit.js`).

| Score | Method | Declared range | Reachable | Combinations evaluated | States reached | Missing → incomplete | NT behaviour | Issues |
|---|---|---|---|---|---|---|---|---|
| ABCD² | sum | 0–7 | 0–7 | 72 (all) | 3/3 | Yes | n/a | None |
| ASPECTS | expression | 0–10 | 0–10 | 1,024 (all) | 2/2 | Yes | n/a | None |
| Borden | select | 1–3 | 1–3 | 9 (all) | 3/3 | Yes | n/a | None |
| Clonus | select | 0–2 | 0–2 | 135 (all) | 3/3 | Yes | n/a | None |
| Cognard | select | 1–7 | 1–7 | 7 (all) | 7/7 | Yes | n/a | None |
| Reflex grade | select | 0–4 | 0–4 | 105 (all) | 4/4 | Yes | n/a | None |
| ECOG | select | 0–5 | 0–5 | 6 (all) | 6/6 | Yes | n/a | None |
| Engel | select | 1–13 | 1–13 | 39 (all) | 4/4 | Yes | n/a | None |
| FAST-ED | sum | 0–9 | 0–9 | 162 (all) | 2/2 | Yes | n/a | None |
| Fisher | select | 1–4 | 1–4 | 4 (all) | 4/4 | Yes | n/a | None |
| Frankel | select | 1–5 | 1–5 | 5 (all) | 5/5 | Yes | n/a | None |
| FUNC | sum | 0–11 | 0–11 | 108 (all) | 3/3 | Yes | n/a | None |
| GCS | sum | 3–15 | 3–15 | 120 (all) | 4/4 | Yes | block | None |
| GCS-P | expression | 1–15 | 1–15 | 360 (all) | 3/3 | Yes | block | None |
| GOS | select | 1–5 | 1–5 | 5 (all) | 5/5 | Yes | n/a | None |
| GOSE | select | 1–8 | 1–8 | 8 (all) | 8/8 | Yes | n/a | None |
| GPA | sum | 0–4 | 0–4 | 54 (all) | 4/4 | Yes | n/a | None |
| Gardner-Robertson | expression | 0–5 | 0–5 | 25 (all) | 6/6 | Yes | n/a | None |
| Graeb | sum | 0–12 | 0–12 | 225 (all) | 2/2 | Yes | n/a | None |
| House-Brackmann | select | 1–6 | 1–6 | 18 (all) | 6/6 | Yes | n/a | None |
| Hunt & Hess | expression | 1–5 | 1–5 | 10 (all) | 5/5 | Yes | n/a | None |
| ICH Score | sum | 0–6 | 0–6 | 48 (all) | 7/7 | Yes | n/a | None |
| ILAE outcome | select | 1–6 | 1–6 | 54 (all) | 7/7 | Yes | n/a | None |
| ISS | expression | 0–75 | 0–75 | 117,649 (all) | 4/4 | Yes | n/a | None |
| KPS | select | 0–100 | 0–100 | 11 (all) | 5/5 | Yes | n/a | None |
| LAMS | sum | 0–5 | 0–5 | 18 (all) | 2/2 | Yes | n/a | None |
| Lawton-Young | expression | 1–5 | 1–5 | 72 (all) | 2/2 | Yes | n/a | None |
| Markwalder | select | 0–4 | 0–4 | 5 (all) | 5/5 | Yes | n/a | None |
| Marshall | expression | 1–6 | 1–6 | 32 (all) | 6/6 | Yes | n/a | None |
| MAS | select | 0–5 | 0–5 | 126 (all) | 5/5 | Yes | n/a | None |
| mFisher | expression | -1–4 | -1–4 | 6 (all) | 6/6 | Yes | n/a | None |
| mJOA | sum | 0–18 | 0–18 | 768 (all) | 4/4 | Yes | n/a | None |
| MRC power | select | 0–5 | 0–5 | 18 (all) | 6/6 | Yes | n/a | None |
| MRC-SS | sum | 0–60 | 0–60 | 300,074 (sample) | 3/3 | Yes | block | None |
| mRS | select | 0–6 | 0–6 | 7 (all) | 7/7 | Yes | n/a | None |
| MTS | expression | 0–180 | 0–180 | 576 (all) | 2/2 | Yes | n/a | None |
| NIHSS | sum | 0–42 | 0–42 | 300,059 (sample) | 2/2 | Yes | exclude | None |
| Nurick | select | 0–5 | 0–5 | 6 (all) | 6/6 | Yes | n/a | None |
| pc-ASPECTS | expression | 0–10 | 0–10 | 256 (all) | 2/2 | Yes | n/a | None |
| Plantar | select | 1–4 | 1–4 | 12 (all) | 4/4 | Yes | n/a | None |
| RACE | sum | 0–9 | 0–9 | 162 (all) | 2/2 | Yes | n/a | None |
| Rotterdam | expression | 1–6 | 1–6 | 24 (all) | 6/6 | Yes | n/a | None |
| Revised Tokuhashi | sum | 0–15 | 0–15 | 1,458 (all) | 3/3 | Yes | n/a | None |
| RTS | expression | 0–7.8408 | 0–7.8408 | 3,328 (all) | 3/3 | Yes | n/a | None |
| SINS | sum | 0–18 | 0–18 | 1,296 (all) | 3/3 | Yes | n/a | None |
| SOFA | sum | 0–24 | 0–24 | 15,625 (all) | 2/2 | Yes | n/a | None |
| Spetzler-Martin | sum | 1–5 | 1–5 | 12 (all) | 3/3 | Yes | n/a | None |
| Tomita | sum | 2–10 | 2–10 | 18 (all) | 1/1 | Yes | n/a | None |
| TRISS | expression | 0–100 | 0.121427–44.650844 | 300,007 (sample) | 1/1 | Yes | n/a | None |
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

### Borden

Version: Borden classification (Borden, Wu & Shucart 1995), types I–III with subtypes a/b. Method: `select`.

| Component | Points |
|---|---|
| Venous drainage | I=1, II=2, III=3 |
| Subtype (optional) | a=0, b=0 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Type I: no cortical venous drainage | low | I | 1 |
| Type II: cortical venous reflux | high | II | 2 |
| Type III: direct cortical venous drainage | high | III | 3 |

Boundaries: 1→2: t1 → t2; 2→3: t2 → t3

### Clonus

Version: Descriptive examination record: absent, unsustained or sustained. Method: `select`.

| Component | Points |
|---|---|
| Clonus | Absent=0, Unsustained=1, Sustained=2 |
| Joint (optional) | =0, =0, =0, =0 |
| Number of beats (optional) | 1–100 |
| Side (optional) | L=0, R=0 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| No clonus elicited | favorable |  | 0 |
| Unsustained clonus | informational |  | 1 |
| Sustained clonus | moderate |  | 2 |

Boundaries: 0→1: absent → unsustained; 1→2: unsustained → sustained

### Cognard

Version: Cognard revised classification (Cognard et al. 1995): I, IIa, IIb, IIa+b, III, IV, V. Method: `select`.

| Component | Points |
|---|---|
| Venous drainage pattern | I=1, IIa=2, IIb=3, IIa+b=4, III=5, IV=6, V=7 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Type I | low | I | 1 |
| Type IIa | low | IIa | 2 |
| Type IIb | high | IIb | 3 |
| Type IIa+b | high | IIa+b | 4 |
| Type III | high | III | 5 |
| Type IV | high | IV | 6 |
| Type V | high | V | 7 |

Boundaries: 1→2: t1 → t2; 2→3: t2 → t3; 3→4: t3 → t4; 4→5: t4 → t5; 5→6: t5 → t6; 6→7: t6 → t7

### Reflex grade

Version: NINDS Myotatic Reflex Scale, 0–4 (Hallett 1993). Method: `select`.

| Component | Points |
|---|---|
| Reflex amplitude | 0=0, 1+=1, 2+=2, 3+=3, 4+=4 |
| Reflex tested (optional) | =0, =0, =0, =0, =0, =0 |
| Side (optional) | L=0, R=0 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Absent | informational | 0 | 0 |
| Reduced | informational | 1+ | 1 |
| Within the normal range | favorable | 2+–3+ | 2–3 |
| Enhanced | informational | 4+ | 4 |

Boundaries: 0→1: absent → reduced; 1→2: reduced → normal; 3→4: normal → enhanced

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

### Engel

Version: Engel classification (Engel et al. 1993), classes I–IV with subclasses. Method: `select`.

| Component | Points |
|---|---|
| Outcome subclass | IA=1, IB=2, IC=3, ID=4, IIA=5, IIB=6, IIC=7, IID=8, IIIA=9, IIIB=10, IVA=11, IVB=12, IVC=13 |
| Follow-up since surgery (years, optional) | 1–50 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Class I: free of disabling seizures | favorable | IA–ID | 1–4 |
| Class II: rare disabling seizures | low | IIA–IID | 5–8 |
| Class III: worthwhile improvement | moderate | IIIA–IIIB | 9–10 |
| Class IV: no worthwhile improvement | high | IVA–IVC | 11–13 |

Boundaries: 4→5: c1 → c2; 8→9: c2 → c3; 10→11: c3 → c4

### FAST-ED

Version: FAST-ED (Lima et al. 2016). Method: `sum`.

| Component | Points |
|---|---|
| Facial palsy | 0=0, 1=1 |
| Arm weakness | 0=0, 1=1, 2=2 |
| Speech changes | 0=0, 1=1, 2=2 |
| Eye deviation | 0=0, 1=1, 2=2 |
| Denial / neglect | 0=0, 1=1, 2=2 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| No deficit on FAST-ED items | favorable | 0 | 0 |
| FAST-ED {total} | informational | 1–9 | 1–9 |

Boundaries: 0→1: zero → scored

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

### GPA

Version: Original GPA (Sperduto et al. 2008, RTOG database). Method: `sum`.

| Component | Points |
|---|---|
| Age | o60=0, 50to60=0.5, u50=1 |
| Karnofsky Performance Status | lt70=0, 70to80=0.5, 90to100=1 |
| Number of brain metastases | gt3=0, 2to3=0.5, one=1 |
| Extracranial metastases | present=0, none=1 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| GPA 0–1 | high | 0–1 | 0–1 |
| GPA 1.5–2.5 | moderate | 1.5–2.5 | 1.5–2.5 |
| GPA 3 | mild | 3 | 3 |
| GPA 3.5–4 | low | 3.5–4 | 3.5–4 |

Boundaries: 1→1.5: g1 → g2; 2.5→3: g2 → g3; 3→3.5: g3 → g4

### Gardner-Robertson

Version: Gardner-Robertson modified hearing classification (1988). Method: `expression: pta == sds ? pta : 0`.

| Component | Points |
|---|---|
| Pure-tone average (PTA) | I=1, II=2, III=3, IV=4, V=5 |
| Speech discrimination score (SDS) | I=1, II=2, III=3, IV=4, V=5 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Discordant: PTA class {roman(pta)}, SDS class {roman(sds)} | informational |  | 0 |
| Class I: good to excellent | favorable | I | 1 |
| Class II: serviceable | low | II | 2 |
| Class III: non-serviceable | moderate | III | 3 |
| Class IV: poor | high | IV | 4 |
| Class V: none | high | V | 5 |

Boundaries: 0→1: disc → c1; 1→2: c1 → c2; 2→3: c2 → c3; 3→4: c3 → c4; 4→5: c4 → c5

### Graeb

Version: Original Graeb score (Graeb et al. 1982). Method: `sum`.

| Component | Points |
|---|---|
| Right lateral ventricle | 0=0, 1=1, 2=2, 3=3, 4=4 |
| Left lateral ventricle | 0=0, 1=1, 2=2, 3=3, 4=4 |
| Third ventricle | 0=0, 1=1, 2=2 |
| Fourth ventricle | 0=0, 1=1, 2=2 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| No intraventricular blood | favorable | 0 | 0 |
| Graeb {total} | informational | 1–12 | 1–12 |

Boundaries: 0→1: none → scored

### House-Brackmann

Version: House-Brackmann grading system, grades I–VI (House & Brackmann 1985). Method: `select`.

| Component | Points |
|---|---|
| Facial nerve function | I=1, II=2, III=3, IV=4, V=5, VI=6 |
| Side (optional) | L=0, R=0 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Grade I: normal | favorable | I | 1 |
| Grade II: mild dysfunction | low | II | 2 |
| Grade III: moderate dysfunction | mild | III | 3 |
| Grade IV: moderately severe dysfunction | moderate | IV | 4 |
| Grade V: severe dysfunction | high | V | 5 |
| Grade VI: total paralysis | high | VI | 6 |

Boundaries: 1→2: g1 → g2; 2→3: g2 → g3; 3→4: g3 → g4; 4→5: g4 → g5; 5→6: g5 → g6

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

### ILAE outcome

Version: ILAE outcome classification (Wieser et al. 2001), classes 1–6 with 1a. Method: `select`.

| Component | Points |
|---|---|
| Outcome in this follow-up year | 1=1, 2=2, 3=3, 4=4, 5=5, 6=6 |
| Seizure free with no auras since surgery? (class 1a) | =0, =0 |
| Follow-up year (optional) | 1–50 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Class 1a | favorable | 1a | 1 |
| Class 1 | favorable | 1 | 1 |
| Class 2 | favorable | 2 | 2 |
| Class 3 | low | 3 | 3 |
| Class 4 | moderate | 4 | 4 |
| Class 5 | high | 5 | 5 |
| Class 6 | high | 6 | 6 |

Boundaries: 1→1: c1 → c1a; 1→2: c1a → c2; 2→3: c2 → c3; 3→4: c3 → c4; 4→5: c4 → c5; 5→6: c5 → c6

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

### Lawton-Young

Version: Lawton-Young supplementary grading scale (Lawton et al. 2010). Method: `expression: supp`.

| Component | Points |
|---|---|
| Age | lt20=1, 20to40=2, gt40=3 |
| Presentation | ruptured=0, unruptured=1 |
| Nidus | compact=0, diffuse=1 |
| Spetzler-Martin grade (optional) | I=1, II=2, III=3, IV=4, V=5 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Supplementary grade {total} | informational | Supp 1–5 | 1–5 |
| Supp-SM grade {combined} | informational | Supp-SM 2–10 | 1–5 |

Boundaries: 1→1: comb → supp; 1→2: supp → comb; 2→2: comb → supp; 2→3: supp → comb; 3→3: comb → supp; 3→4: supp → comb; 4→4: comb → supp; 4→5: supp → comb; 5→5: comb → supp

### Markwalder

Version: Markwalder grading scale (1981), grades 0–4. Method: `select`.

| Component | Points |
|---|---|
| Clinical grade | 0=0, 1=1, 2=2, 3=3, 4=4 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Grade 0: neurologically normal | favorable | 0 | 0 |
| Grade 1: alert and oriented | low | 1 | 1 |
| Grade 2: drowsy or disoriented | moderate | 2 | 2 |
| Grade 3: stuporous | high | 3 | 3 |
| Grade 4: comatose | high | 4 | 4 |

Boundaries: 0→1: g0 → g1; 1→2: g1 → g2; 2→3: g2 → g3; 3→4: g3 → g4

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

### MAS

Version: Modified Ashworth Scale (Bohannon & Smith 1987). Method: `select`.

| Component | Points |
|---|---|
| Resistance to passive movement | 0=0, 1=1, 1+=2, 2=3, 3=4, 4=5 |
| Muscle group (optional) | =0, =0, =0, =0, =0, =0 |
| Side (optional) | L=0, R=0 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| No increase in tone | favorable | MAS 0 | 0 |
| Slight increase in tone | low | MAS 1–1+ | 1–2 |
| More marked increase | mild | MAS 2 | 3 |
| Considerable increase | moderate | MAS 3 | 4 |
| Rigid | high | MAS 4 | 5 |

Boundaries: 0→1: g0 → slight; 2→3: slight → marked; 3→4: marked → considerable; 4→5: considerable → rigid

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

### mJOA

Version: mJOA, clinician-rated (Benzel et al. 1991), 0–18. Method: `sum`.

| Component | Points |
|---|---|
| Upper-limb motor function | 0=0, 1=1, 2=2, 3=3, 4=4, 5=5 |
| Lower-limb motor function | 0=0, 1=1, 2=2, 3=3, 4=4, 5=5, 6=6, 7=7 |
| Upper-limb sensation | 0=0, 1=1, 2=2, 3=3 |
| Micturition | 0=0, 1=1, 2=2, 3=3 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Severe myelopathy | high | 0–11 | 0–11 |
| Moderate myelopathy | moderate | 12–14 | 12–14 |
| Mild myelopathy | mild | 15–17 | 15–17 |
| No dysfunction measured | favorable | 18 | 18 |

Boundaries: 11→12: severe → moderate; 14→15: moderate → mild; 17→18: mild → none

### MRC power

Version: Medical Research Council scale, grades 0–5. Method: `select`.

| Component | Points |
|---|---|
| Power grade | 5=5, 4=4, 3=3, 2=2, 1=1, 0=0 |
| Side (optional) | L=0, R=0 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Grade 5: normal power | favorable | 5 | 5 |
| Grade 4: against gravity and resistance | mild | 4 | 4 |
| Grade 3: against gravity | moderate | 3 | 3 |
| Grade 2: gravity eliminated | high | 2 | 2 |
| Grade 1: flicker or trace | high | 1 | 1 |
| Grade 0: no contraction | high | 0 | 0 |

Boundaries: 0→1: g0 → g1; 1→2: g1 → g2; 2→3: g2 → g3; 3→4: g3 → g4; 4→5: g4 → g5

### MRC-SS

Version: MRC sum score, 12 muscle groups (Kleyweg et al. 1991). Method: `sum`.

| Component | Points |
|---|---|
| Shoulder abduction, left · NT (Amputation or injury/Pain prevents testing/Not cooperating or sedated/Other) | 5=5, 4=4, 3=3, 2=2, 1=1, 0=0 |
| Elbow flexion, left · NT (Amputation or injury/Pain prevents testing/Not cooperating or sedated/Other) | 5=5, 4=4, 3=3, 2=2, 1=1, 0=0 |
| Wrist extension, left · NT (Amputation or injury/Pain prevents testing/Not cooperating or sedated/Other) | 5=5, 4=4, 3=3, 2=2, 1=1, 0=0 |
| Hip flexion, left · NT (Amputation or injury/Pain prevents testing/Not cooperating or sedated/Other) | 5=5, 4=4, 3=3, 2=2, 1=1, 0=0 |
| Knee extension, left · NT (Amputation or injury/Pain prevents testing/Not cooperating or sedated/Other) | 5=5, 4=4, 3=3, 2=2, 1=1, 0=0 |
| Ankle dorsiflexion, left · NT (Amputation or injury/Pain prevents testing/Not cooperating or sedated/Other) | 5=5, 4=4, 3=3, 2=2, 1=1, 0=0 |
| Shoulder abduction, right · NT (Amputation or injury/Pain prevents testing/Not cooperating or sedated/Other) | 5=5, 4=4, 3=3, 2=2, 1=1, 0=0 |
| Elbow flexion, right · NT (Amputation or injury/Pain prevents testing/Not cooperating or sedated/Other) | 5=5, 4=4, 3=3, 2=2, 1=1, 0=0 |
| Wrist extension, right · NT (Amputation or injury/Pain prevents testing/Not cooperating or sedated/Other) | 5=5, 4=4, 3=3, 2=2, 1=1, 0=0 |
| Hip flexion, right · NT (Amputation or injury/Pain prevents testing/Not cooperating or sedated/Other) | 5=5, 4=4, 3=3, 2=2, 1=1, 0=0 |
| Knee extension, right · NT (Amputation or injury/Pain prevents testing/Not cooperating or sedated/Other) | 5=5, 4=4, 3=3, 2=2, 1=1, 0=0 |
| Ankle dorsiflexion, right · NT (Amputation or injury/Pain prevents testing/Not cooperating or sedated/Other) | 5=5, 4=4, 3=3, 2=2, 1=1, 0=0 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| No weakness measured | favorable | 60 | 60 |
| Weakness above the ICU-AW threshold | mild | 48–59 | 48–59 |
| Below 48: meets the ICU-AW strength criterion | high | 0–47 | 0–47 |

Boundaries: 47→48: below → above; 59→60: above → full

Not testable: sh_l → not-interpretable; el_l → not-interpretable; wr_l → not-interpretable; hi_l → not-interpretable; kn_l → not-interpretable; an_l → not-interpretable; sh_r → not-interpretable; el_r → not-interpretable; wr_r → not-interpretable; hi_r → not-interpretable; kn_r → not-interpretable; an_r → not-interpretable

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

### MTS

Version: Modified Tardieu Scale (Boyd & Graham 1999). Method: `expression: isnull(r1) ? 0 : abs(r2 - r1)`.

| Component | Points |
|---|---|
| Muscle group (optional) | =0, =0, =0, =0, =0, =0, =0 |
| Velocity of the fast stretch | V2=0, V3=0 |
| Quality of muscle reaction (X) | X0=0, X1=1, X2=2, X3=3, X4=4, X5=5 |
| R1: angle of catch (fast stretch) | 0–180 |
| R2: passive range (slow stretch, V1) | 0–180 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| {x_code}, no angle of catch | informational |  | 0 |
| {x_code}, dynamic component {total}° | informational |  | 0–180 |

Boundaries: 0→0: catch → nocatch; 0→180: nocatch → catch

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

### Plantar

Version: Descriptive examination record: flexor, extensor, equivocal or no response. Method: `select`.

| Component | Points |
|---|---|
| Great toe response | Flexor=1, Extensor=2, Equivocal=3, No response=4 |
| Side (optional) | L=0, R=0 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Flexor response | favorable |  | 1 |
| Extensor response (Babinski sign) | moderate |  | 2 |
| Equivocal | informational |  | 3 |
| No response | informational |  | 4 |

Boundaries: 1→2: flexor → extensor; 2→3: extensor → equivocal; 3→4: equivocal → none

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

### SOFA

Version: Original SOFA (Vincent et al. 1996), as tabulated in Sepsis-3 (Singer et al. 2016). Method: `sum`.

| Component | Points |
|---|---|
| Respiration: PaO₂/FiO₂, mmHg (kPa) | 0=0, 1=1, 2=2, 3=3, 4=4 |
| Coagulation: platelets, ×10³/µL | 0=0, 1=1, 2=2, 3=3, 4=4 |
| Liver: bilirubin, mg/dL (µmol/L) | 0=0, 1=1, 2=2, 3=3, 4=4 |
| Cardiovascular | 0=0, 1=1, 2=2, 3=3, 4=4 |
| Central nervous system: GCS | 0=0, 1=1, 2=2, 3=3, 4=4 |
| Renal: creatinine, mg/dL (µmol/L), or urine output | 0=0, 1=1, 2=2, 3=3, 4=4 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| No organ dysfunction measured | favorable | 0 | 0 |
| SOFA {total} | informational | 1–24 | 1–24 |

Boundaries: 0→1: zero → scored

### Spetzler-Martin

Version: Spetzler-Martin grading system (1986), grades I–V. Method: `sum`.

| Component | Points |
|---|---|
| Nidus size (maximum diameter) | small=1, medium=2, large=3 |
| Eloquence of adjacent brain | no=0, yes=1 |
| Venous drainage | sup=0, deep=1 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Grade {roman(total)} | low | I–II | 1–2 |
| Grade III | moderate | III | 3 |
| Grade {roman(total)} | high | IV–V | 4–5 |

Boundaries: 2→3: low → mid; 3→4: mid → high

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

### TRISS

Version: TRISS with 1995 MTOS coefficients (Champion et al.). Method: `expression: 100 / (1 + exp(-b))`.

| Component | Points |
|---|---|
| Mechanism | blunt=0, pen=1 |
| Age | child=0, adult=0, older=1 |
| GCS total | …–3→0, 4–5→1, 6–8→2, 9–12→3, 13–…→4 |
| Systolic blood pressure | …–0→0, 1–49→1, 50–75→2, 76–89→3, 90–…→4 |
| Respiratory rate | …–0→0, 1–5→1, 6–9→2, 10–29→4, 30–…→3 |
| Head or neck | 0–6 |
| Face | 0–6 |
| Chest | 0–6 |
| Abdomen or pelvic contents | 0–6 |
| Extremities or pelvic girdle | 0–6 |
| External | 0–6 |

| State | Tone | Declared range | Totals that reach it |
|---|---|---|---|
| Ps {fixed(total, 1)}% | informational | 0–100% | 0.121427–44.650844 |

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

