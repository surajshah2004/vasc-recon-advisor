"""
Sample cases for VascRecon Advisor prototype.
Covers a range of scenarios: mild disease, severe ischemia,
deep infection, high operative risk, and ambiguous presentations.
"""

SAMPLE_CASES = [
    {
        "name": "Case 1 — Diabetic forefoot ulcer, moderate PAD",
        "age": 62,
        "sex": "Male",
        "comorbidities": ["Diabetes", "Peripheral arterial disease", "Hypertension", "Smoking"],
        "functional_status": "Limited",
        "operative_risk": "Moderate",
        "ambulatory": "Limited ambulation",
        "vascular_status": "Moderate disease",
        "prior_vasc": "None",
        "wound_location": "Forefoot",
        "wound_size": "Medium (2–5 cm)",
        "wound_depth": "Into subcutaneous tissue",
        "infection": "Suspected",
        "tissue": "Mixed/unclear",
        "chronicity": "Subacute (4–12 wks)",
        "pain": "Mild",
        "patient_goal": "Limb salvage",
        "narrative": (
            "62-year-old man with T2DM (HbA1c 9.8%) and known PAD presenting with a 6-week-old "
            "plantar ulcer beneath the 2nd metatarsal head. ABI 0.58 right foot. Mild surrounding "
            "erythema but no fluctuance. No fever, WBC 11.2. Plain films negative for osteomyelitis. "
            "Patient uses a walker and is very motivated to keep his foot. Has not had prior vascular workup."
        ),
    },
    {
        "name": "Case 2 — Heel wound, severe ischemia, high surgical risk",
        "age": 74,
        "sex": "Female",
        "comorbidities": ["Diabetes", "Coronary artery disease", "Heart failure", "Chronic kidney disease", "Hypertension"],
        "functional_status": "Poor",
        "operative_risk": "High",
        "ambulatory": "Non-ambulatory",
        "vascular_status": "Severe ischemia",
        "prior_vasc": "Prior angioplasty/stent",
        "wound_location": "Heel",
        "wound_size": "Large (>5 cm)",
        "wound_depth": "Exposed tendon/bone",
        "infection": "Confirmed deep/osteomyelitis",
        "tissue": "Necrotic tissue present",
        "chronicity": "Chronic (>12 wks)",
        "pain": "Severe",
        "patient_goal": "Pain control",
        "narrative": (
            "74-year-old woman, bedbound in a nursing facility, with severe multi-vessel PAD (prior "
            "angioplasty 3 years ago with re-stenosis on recent duplex), EF 25%, CKD stage 4. "
            "Large heel pressure ulcer with exposed calcaneus and surrounding cellulitis. "
            "MRI confirms osteomyelitis. Patient reports severe constant pain. Family goals focus on "
            "comfort. Vascular surgery has reviewed and considers repeat revascularization extremely "
            "high-risk given cardiac status."
        ),
    },
    {
        "name": "Case 3 — Post-traumatic ankle wound, low-risk patient",
        "age": 38,
        "sex": "Male",
        "comorbidities": ["Smoking"],
        "functional_status": "Good",
        "operative_risk": "Low",
        "ambulatory": "Fully ambulatory",
        "vascular_status": "Mild disease",
        "prior_vasc": "None",
        "wound_location": "Ankle",
        "wound_size": "Medium (2–5 cm)",
        "wound_depth": "Exposed tendon/bone",
        "infection": "None",
        "tissue": "Healthy appearing",
        "chronicity": "Acute (<4 wks)",
        "pain": "Moderate",
        "patient_goal": "Preserve function",
        "narrative": (
            "38-year-old male construction worker, active smoker (1 ppd x 15 years), sustained a "
            "degloving injury to the lateral ankle 2 weeks ago. Exposed peroneal tendons visible. "
            "Wound edges are clean, no signs of infection. ABI 0.88 bilaterally. Otherwise healthy. "
            "Patient is eager to return to work and very concerned about long-term ankle function."
        ),
    },
    {
        "name": "Case 4 — Ischemic rest pain, midfoot gangrene",
        "age": 67,
        "sex": "Male",
        "comorbidities": ["Diabetes", "Smoking", "Peripheral arterial disease", "Hypertension", "COPD"],
        "functional_status": "Limited",
        "operative_risk": "Moderate",
        "ambulatory": "Limited ambulation",
        "vascular_status": "Severe ischemia",
        "prior_vasc": "Prior bypass",
        "wound_location": "Midfoot",
        "wound_size": "Large (>5 cm)",
        "wound_depth": "Deep/complex",
        "infection": "Confirmed localized",
        "tissue": "Necrotic tissue present",
        "chronicity": "Subacute (4–12 wks)",
        "pain": "Severe",
        "patient_goal": "Limb salvage",
        "narrative": (
            "67-year-old man with severe PAD, prior fem-pop bypass 5 years ago (now occluded on imaging). "
            "Presents with necrotic midfoot wound and rest pain. ABI non-compressible; toe pressure 18 mmHg. "
            "CTA shows no suitable bypass target. Wound has localized infection with mild systemic response "
            "(WBC 14, low-grade fever). Patient strongly requests limb salvage but vascular surgery has "
            "deemed him a poor candidate for re-do bypass."
        ),
    },
    {
        "name": "Case 5 — Venous/mixed lower leg ulcer, outpatient management",
        "age": 55,
        "sex": "Female",
        "comorbidities": ["Obesity", "Hypertension", "Diabetes"],
        "functional_status": "Good",
        "operative_risk": "Low",
        "ambulatory": "Fully ambulatory",
        "vascular_status": "Mild disease",
        "prior_vasc": "None",
        "wound_location": "Lower leg",
        "wound_size": "Medium (2–5 cm)",
        "wound_depth": "Superficial",
        "infection": "None",
        "tissue": "Mixed/unclear",
        "chronicity": "Chronic (>12 wks)",
        "pain": "Mild",
        "patient_goal": "Fastest healing",
        "narrative": (
            "55-year-old obese woman with longstanding bilateral lower extremity edema and a "
            "3-month-old medial lower leg ulcer. ABI 0.82 — borderline for compression therapy. "
            "Wound bed has fibrinous slough. No signs of active infection. Venous duplex shows "
            "superficial venous reflux. Patient works full-time and wants the fastest outpatient "
            "solution with minimal time off work."
        ),
    },
]
