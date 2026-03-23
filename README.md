# VascRecon Advisor 🩺

**A clinical decision-support prototype for lower extremity wounds at the intersection of vascular surgery and reconstructive plastic surgery.**

> ⚠️ **This is a prototype for educational and reasoning-support purposes only. It does not provide clinical advice and must not be used to guide real patient care.**

---

## What it does

VascRecon Advisor takes structured patient data (comorbidities, vascular status, wound characteristics) and a free-text clinical narrative, then uses an LLM to generate:

- **2–3 meaningfully different management strategies** (e.g., conservative care, revascularization-first, reconstruction, amputation)
- **Pros and cons** for each option, specific to the patient
- **Comparative reasoning** that weighs options against each other
- **Key decision drivers** — the 3 most influential factors in this case
- **Soft directional guidance** framed explicitly as non-definitive
- **Uncertainty notes** about what's missing or would change the analysis

### Target users
- Medical trainees learning to reason through complex vascular/reconstructive cases
- Interdisciplinary teams preparing for multidisciplinary meetings
- Educators building case-based learning exercises

---

## Clinical scope

Lower extremity wounds where vascular disease affects reconstructive decisions, including:
- Diabetic foot ulcers with PAD
- Ischemic wounds (rest pain, tissue loss)
- Post-traumatic wounds with vascular compromise
- Heel pressure injuries in vascular patients
- Mixed venous/arterial ulcers

**Out of scope:** Diagnosis, image analysis, real patient data, EHR integration, other surgical fields.

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/vasc-recon-advisor.git
cd vasc-recon-advisor
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get an Anthropic API key
Sign up at [console.anthropic.com](https://console.anthropic.com). The app uses **Claude Haiku** — extremely cost-efficient (~$0.001 per analysis).

### 4. Run the app
```bash
streamlit run app.py
```

Enter your API key in the app interface (not stored anywhere).

---

## Cost estimate

Using Claude Haiku (`claude-haiku-4-5`):
- ~$0.001–0.002 per case analysis
- $10 in API credits ≈ **5,000–10,000 analyses**

---

## Sample cases

5 built-in cases covering the clinical spectrum:
1. Diabetic forefoot ulcer with moderate PAD
2. Heel wound with severe ischemia in a high-risk patient
3. Post-traumatic ankle wound in a young low-risk patient
4. Ischemic midfoot gangrene with no revascularization options
5. Mixed venous/arterial lower leg ulcer

Load any sample from the sidebar dropdown to explore the tool immediately.

---

## Project structure

```
vasc-recon-advisor/
├── app.py              # Main Streamlit application
├── sample_cases.py     # Built-in sample cases
├── requirements.txt    # Python dependencies
└── README.md
```

---

## Roadmap / future work

- [ ] "What-if" scenario testing (toggle one variable, see how options shift)
- [ ] Export case + output as PDF for MDT preparation
- [ ] Scoring or uncertainty quantification
- [ ] Expanded case library (20+ cases)
- [ ] Validated against expert clinician reasoning

---

## Disclaimer

This tool is a prototype. It does not constitute medical advice, clinical diagnosis, or treatment recommendations. All decisions must be made by qualified clinicians based on complete patient evaluation. The authors are not responsible for any clinical outcomes related to use of this tool.

---

*Built as a prototype for physician review and feedback. Developed with interest in scaling through academic medical center partnership.*
