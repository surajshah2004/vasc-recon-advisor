ClinAdvisor (Baseline)
ClinAdvisor is a Streamlit app that takes a free-text atrial fibrillation clinical case and generates 2–3 structured management strategies. Each strategy includes pros and cons, tradeoff reasoning, key decision drivers, bottleneck identification, and soft directional guidance. The goal is to simulate real clinical reasoning — not provide a single correct answer.
Purpose
This is the baseline version (LLM only, no retrieval). It serves as the control condition in a research study comparing standard LLM outputs against retrieval-augmented generation (RAG) using real patient cases from MIMIC-IV.
Research Study
We are testing whether giving the model access to similar real patient cases improves clinical reasoning quality. Outputs from both versions are scored manually using a rubric covering clinical appropriateness, tradeoff reasoning, bottleneck identification, uncertainty handling, harmfulness, and trainee usefulness.

### Target users
- Medical trainees learning to reason through complex vascular/reconstructive cases
- Interdisciplinary teams preparing for multidisciplinary meetings
- Educators building case-based learning exercises

---

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

## Disclaimer

This tool is a prototype. It does not constitute medical advice, clinical diagnosis, or treatment recommendations. All decisions must be made by qualified clinicians based on complete patient evaluation. The authors are not responsible for any clinical outcomes related to use of this tool.

---

*Built as a prototype for physician review and feedback. Developed with interest in scaling through academic medical center partnership.*
