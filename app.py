import streamlit as st
import anthropic
import json
import re

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ClinIQ",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
h1, h2, h3, h4 { font-family: 'Playfair Display', serif; }

.main, .stApp { background-color: #0f1923; }
.block-container { background-color: #0f1923; padding-top: 2rem !important; }

section[data-testid="stSidebar"] {
    background-color: #141f2e;
    border-right: 1px solid #1e2d42;
}
section[data-testid="stSidebar"] * { color: #c8d8e8 !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stTextInput label,
section[data-testid="stSidebar"] .stMultiSelect label {
    color: #5a7a9a !important;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
}

.header-banner {
    background: linear-gradient(135deg, #141f2e 0%, #1a3a5c 60%, #1e4d7a 100%);
    color: white;
    padding: 2rem 2.5rem;
    border-radius: 14px;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
    border: 1px solid #1e3a5a;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
}
.header-banner h1 { color: white; margin: 0; font-size: 2rem; letter-spacing: -0.02em; }
.header-banner p { color: #7ab0d4; margin: 0.3rem 0 0; font-size: 0.9rem; font-weight: 300; }

.option-card {
    background: #141f2e;
    border-radius: 12px;
    padding: 1.6rem;
    margin-bottom: 1.2rem;
    border: 1px solid #1e3a5a;
    border-left: 4px solid #3a8f6a;
    box-shadow: 0 2px 12px rgba(0,0,0,0.3);
}
.option-card.amber { border-left-color: #d4892a; border-color: #2e2415; }
.option-card.blue  { border-left-color: #4a7fd4; border-color: #1a2540; }
.option-card h3 { margin-top: 0; font-size: 1.1rem; color: #e8f0f8; }
.option-card p { color: #8ab0cc !important; }
.option-card .tag {
    display: inline-block;
    background: #0d2a1e;
    color: #3a8f6a;
    border-radius: 4px;
    padding: 2px 10px;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.8rem;
    border: 1px solid #1e4a36;
}
.option-card.amber .tag { background: #2a1a08; color: #d4892a; border-color: #4a3010; }
.option-card.blue  .tag { background: #0d1a2e; color: #4a7fd4; border-color: #1a2e4a; }

.pro-con { display: flex; gap: 1rem; margin-top: 0.8rem; }
.pros, .cons {
    flex: 1;
    background: #0f1923;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    font-size: 0.87rem;
    color: #a8c4d8 !important;
    border: 1px solid #1e2d42;
}
.pros strong { color: #3a8f6a; }
.cons strong { color: #d45a5a; }
.pros ul li, .cons ul li { color: #a8c4d8 !important; }

.comp-reasoning {
    font-size: 0.93rem;
    color: #a8c4d8 !important;
    line-height: 1.8;
    background: #141f2e;
    border-radius: 12px;
    padding: 1.4rem 1.8rem;
    border: 1px solid #1e3a5a;
    box-shadow: 0 2px 12px rgba(0,0,0,0.3);
}

.driver-chip {
    display: inline-block;
    background: #0d1e30;
    color: #7ab0d4 !important;
    border-radius: 20px;
    padding: 5px 16px;
    font-size: 0.82rem;
    margin: 4px;
    border: 1px solid #1e3a5a;
    font-weight: 500;
}

.rec-box {
    background: #0d2a1e;
    border: 1px solid #1e4a36;
    border-left: 4px solid #3a8f6a;
    border-radius: 12px;
    padding: 1.4rem 1.8rem;
    margin: 1.2rem 0;
}
.rec-box h4 { color: #3a8f6a; margin-top: 0; font-size: 1rem; }
.rec-box p { color: #7ab89a !important; }

.disclaimer {
    background: #1e1a0a;
    border: 1px solid #3a2e08;
    border-left: 4px solid #d4892a;
    border-radius: 10px;
    padding: 1.1rem 1.5rem;
    font-size: 0.82rem;
    color: #b89a5a;
    margin-top: 1.5rem;
    line-height: 1.7;
}

.section-label {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #3a5a7a;
    margin: 1.8rem 0 0.5rem;
}

h2 { color: #c8d8e8 !important; font-size: 1.3rem !important; margin-top: 2rem !important; }

.stTextArea textarea {
    background-color: #141f2e !important;
    color: #c8d8e8 !important;
    border: 1px solid #1e3a5a !important;
    border-radius: 8px !important;
}
.stTextArea label { color: #5a7a9a !important; }

.ready-state { text-align: center; padding: 5rem 2rem; }
.ready-state h3 { color: #4a7a9a; font-size: 1.6rem; margin-top: 1rem; font-family: 'Playfair Display', serif; }
.ready-state p { color: #3a5a7a; max-width: 500px; margin: 0.5rem auto; line-height: 1.7; }

.module-hint {
    background: #141f2e;
    border: 1px solid #1e3a5a;
    border-radius: 10px;
    padding: 1rem 1.4rem;
    margin-bottom: 1rem;
    font-size: 0.85rem;
    color: #5a8aaa;
    line-height: 1.6;
}
.module-hint strong { color: #7ab0d4; }
</style>
""", unsafe_allow_html=True)

# ── Module definitions ────────────────────────────────────────────────────────
MODULES = {
    "afib": {
        "label": "Atrial Fibrillation",
        "icon": "⚡",
        "subtitle": "Rate vs rhythm · Anticoagulation · Ablation",
        "hint": "Include if available: <strong>AFib type</strong> (paroxysmal/persistent/permanent), <strong>symptom burden</strong>, <strong>CHA₂DS₂-VASc score</strong>, <strong>HAS-BLED score</strong>, <strong>prior cardioversions or ablations</strong>, <strong>echo findings</strong> (LA size, EF), <strong>current medications</strong>.",
        "prompt_context": """You are supporting clinical reasoning for atrial fibrillation (AFib) management. Focus on the key decision axes: rate control vs rhythm control, anticoagulation strategy (stroke vs bleeding risk tradeoff), and procedural options.

CRITICAL — model the real clinical workflow accurately:

1. ANTICOAGULATION IS A SHARED DECISION. Never frame it as something to initiate "despite patient preference" or override patient refusal. If the patient declines anticoagulation, explicitly name this as the central decision bottleneck. The appropriate response is structured counseling, risk communication, and exploration of alternatives (e.g. LAAO) — not bypassing patient autonomy. Use language like "strongly recommended pending patient agreement" or "requires shared decision-making given patient's current reluctance."

2. RHYTHM CONTROL FOLLOWS A LAYERED ESCALATION — always present this progression accurately:
   - Step 1: Cardioversion (electrical or pharmacologic) — this is typically the FIRST active rhythm-control intervention. It is distinct from ablation and must appear as its own pathway or step, not collapsed into ablation.
   - Step 2: Antiarrhythmic drug therapy (e.g. flecainide, sotalol, amiodarone) — often trialed alongside or after cardioversion.
   - Step 3: Catheter ablation — appropriate when antiarrhythmics fail, are not tolerated, or when the patient has strong symptom/lifestyle goals and elects an invasive approach after informed discussion.

3. ABLATION POSITIONING. Ablation is a reasonable and guideline-supported option in appropriate candidates — but it is not automatically superior or "best fit." Frame it conditionally: suitable for patients who prefer a potentially more durable rhythm-control strategy, have failed or declined antiarrhythmics, have paroxysmal or early persistent AFib, and are willing to accept procedural risk after informed consent. Do not present it as the obvious choice.

4. RATE AND RHYTHM CONTROL ARE NOT MUTUALLY EXCLUSIVE. Rate control often continues in parallel while cardioversion or rhythm strategy is being planned, trialed, or awaited. Make this explicit.

5. Consider throughout: AFib type (paroxysmal/persistent/longstanding persistent/permanent), symptom burden and its impact on quality of life, CHA₂DS₂-VASc score, HAS-BLED score, LV function (EF), LA size, patient lifestyle goals, prior cardioversions or ablations, current medications, and any explicit patient preferences or refusals."""
    },
    "valvular": {
        "label": "Valvular Heart Disease",
        "icon": "🔬",
        "subtitle": "Watchful waiting vs intervention timing",
        "hint": "Include if available: <strong>valve affected</strong> (aortic/mitral/tricuspid), <strong>lesion type</strong> (stenosis/regurgitation), <strong>severity</strong>, <strong>echo findings</strong> (gradients, valve area, EF, chamber dimensions), <strong>symptom status</strong>, <strong>exercise tolerance</strong>, <strong>prior cardiac surgery</strong>.",
        "prompt_context": """You are supporting clinical reasoning for valvular heart disease management. Focus on the key decision axes: watchful waiting with surveillance vs timing of intervention, and type of intervention if warranted (surgical repair vs replacement vs transcatheter options like TAVR or MitraClip). Consider valve type and lesion severity, LV function and dimensions, symptom status, patient age and surgical risk, and guideline thresholds for intervention."""
    },
    "preop": {
        "label": "Pre-op Cardiac Risk",
        "icon": "⚕️",
        "subtitle": "Cardiac clearance before non-cardiac surgery",
        "hint": "Include if available: <strong>planned surgery type and urgency</strong>, <strong>functional capacity in METs</strong>, <strong>RCRI score</strong>, <strong>prior stress test or echo</strong>, <strong>active cardiac conditions</strong> (unstable angina, decompensated HF, significant arrhythmia, severe valve disease), <strong>current cardiac medications</strong>.",
        "prompt_context": """You are supporting clinical reasoning for pre-operative cardiac risk stratification before non-cardiac surgery. Focus on the key decision axes: proceed to surgery vs further cardiac workup first, and what workup is appropriate (stress testing, echocardiography, cardiology consultation, coronary angiography). Apply the ACC/AHA stepwise approach: surgery urgency, active cardiac conditions, surgical risk, functional capacity, and whether further testing would change management."""
    }
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🫀 Patient Inputs")
    st.markdown('<p class="section-label">Demographics</p>', unsafe_allow_html=True)

    age = st.number_input("Age", 18, 100, value=st.session_state.get("af_age", 65))

    sex_opts = ["Male", "Female", "Other/Not specified"]
    sex = st.selectbox("Sex", sex_opts,
                       index=sex_opts.index(st.session_state.get("af_sex", "Male")))

    st.markdown('<p class="section-label">Comorbidities</p>', unsafe_allow_html=True)
    all_comorbidities = [
        "Diabetes", "Hypertension", "Heart failure", "Coronary artery disease",
        "Prior stroke/TIA", "Chronic kidney disease", "COPD", "Obesity",
        "Peripheral arterial disease", "Smoking", "Hyperlipidemia", "Sleep apnea"
    ]
    raw_comorbidities = st.session_state.get("af_comorbidities", [])
    safe_comorbidities = [c for c in raw_comorbidities if c in all_comorbidities] if isinstance(raw_comorbidities, list) else []
    comorbidities = st.multiselect("Select all that apply", all_comorbidities, default=safe_comorbidities)

    st.markdown('<p class="section-label">Clinical status</p>', unsafe_allow_html=True)

    func_opts = ["Good", "Limited", "Poor", "Unknown"]
    functional_status = st.selectbox("Functional status", func_opts,
        index=func_opts.index(st.session_state.get("af_functional_status", "Unknown")))

    risk_opts = ["Low", "Moderate", "High", "Unknown"]
    operative_risk = st.selectbox("Procedural/operative risk", risk_opts,
        index=risk_opts.index(st.session_state.get("af_operative_risk", "Unknown")))

    setting_opts = ["Outpatient", "Inpatient", "Pre-operative", "Emergency", "Unknown"]
    clinical_setting = st.selectbox("Clinical setting", setting_opts,
        index=setting_opts.index(st.session_state.get("af_clinical_setting", "Unknown")))

    st.markdown('<p class="section-label">Patient priority</p>', unsafe_allow_html=True)
    goal_opts = ["Symptom control", "Avoid procedures", "Quality of life",
                 "Longevity/survival", "Minimize medications", "Not specified"]
    patient_goal = st.selectbox("Primary goal", goal_opts,
        index=goal_opts.index(st.session_state.get("af_patient_goal", "Not specified")))

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
  <div style="font-size:3rem">🫀</div>
  <div>
    <h1>ClinIQ</h1>
    <p>Clinical decision-support for cardiology management &nbsp;·&nbsp; <em>Prototype — not for clinical use</em></p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Narrative box — shown first so auto-detect can read it ───────────────────
if "selected_module" not in st.session_state:
    st.session_state["selected_module"] = None

# Use a shared narrative box before module is selected
pre_module_narrative = st.session_state.get("pre_module_narrative", "")

st.markdown('<p class="section-label">Case narrative</p>', unsafe_allow_html=True)

col_narr, col_btns = st.columns([3, 1])

with col_narr:
    case_narrative_input = st.text_area(
        "Paste your clinical case here, then select a module below",
        value=pre_module_narrative,
        height=160,
        key="pre_narrative_input",
        placeholder="e.g. 67-year-old with persistent AFib, hypertension, palpitations, on metoprolol but not anticoagulated..."
    )
    st.session_state["pre_module_narrative"] = case_narrative_input

with col_btns:
    st.markdown('<p class="section-label">Actions</p>', unsafe_allow_html=True)
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
    except:
        api_key = st.text_input("Anthropic API key", type="password")
    st.markdown("")
    autofill_btn = st.button("✨ Auto-fill sidebar", use_container_width=True,
                              help="AI parses narrative and populates sidebar fields")
    analyze_btn = st.button("🔍 Analyze Case", use_container_width=True, type="primary")

st.markdown("---")

# ── Module selector ───────────────────────────────────────────────────────────
st.markdown('<p class="section-label" style="margin-top:0">Select module</p>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
for col, (key, mod) in zip([col1, col2, col3], MODULES.items()):
    with col:
        btn_label = f"{mod['icon']}  {mod['label']}"
        if st.button(btn_label, key=f"mod_{key}", use_container_width=True):
            st.session_state["selected_module"] = key
            st.rerun()

st.markdown("---")

module_key = st.session_state.get("selected_module")

if not module_key:
    st.markdown("""
    <div class="ready-state">
      <div style="font-size:4rem">🫀</div>
      <h3>Ready to analyze</h3>
      <p>Paste a case narrative above and select a module to begin.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

module = MODULES[module_key]

# Sync narrative to module-specific key
narrative_key = f"narrative_{module_key}"
if st.session_state.get("pre_module_narrative"):
    st.session_state[narrative_key] = st.session_state["pre_module_narrative"]
case_narrative = st.session_state.get(narrative_key, case_narrative_input)

st.markdown(f"<div class='module-hint'>💡 <strong>{module['label']} — suggested narrative details:</strong> {module['hint']}</div>",
            unsafe_allow_html=True)

# ── Autofill prompt ───────────────────────────────────────────────────────────
def build_autofill_prompt(narrative: str) -> str:
    return f"""You are a clinical data extraction assistant. Read the following cardiology case narrative and extract structured fields.

NARRATIVE:
{narrative}

Return ONLY a valid JSON object with these exact keys and allowed values:

{{
  "af_age": <integer, or 65 if unknown>,
  "af_sex": "<Male|Female|Other/Not specified>",
  "af_comorbidities": [<list from: "Diabetes","Hypertension","Heart failure","Coronary artery disease","Prior stroke/TIA","Chronic kidney disease","COPD","Obesity","Peripheral arterial disease","Smoking","Hyperlipidemia","Sleep apnea">],
  "af_functional_status": "<Good|Limited|Poor|Unknown>",
  "af_operative_risk": "<Low|Moderate|High|Unknown>",
  "af_clinical_setting": "<Outpatient|Inpatient|Pre-operative|Emergency|Unknown>",
  "af_patient_goal": "<Symptom control|Avoid procedures|Quality of life|Longevity/survival|Minimize medications|Not specified>"
}}

Rules:
- Use ONLY the allowed values — no variations
- If clearly stated in narrative, extract accurately
- If ambiguous or not mentioned, use "Unknown" — do NOT guess
- Return ONLY the JSON, no explanation or markdown fences
"""

# ── Analysis prompt ───────────────────────────────────────────────────────────
def build_prompt(inputs: dict, module: dict) -> str:
    return f"""{module['prompt_context']}

You do NOT make clinical decisions. You organize competing management strategies to support discussion and education.

PATIENT SUMMARY:
{inputs['narrative'] or '(No narrative provided)'}

STRUCTURED DATA:
- Age/Sex: {inputs['age']} y/o {inputs['sex']}
- Comorbidities: {', '.join(inputs['comorbidities']) if inputs['comorbidities'] else 'None listed'}
- Functional status: {inputs['functional_status']}
- Procedural/operative risk: {inputs['operative_risk']}
- Clinical setting: {inputs['clinical_setting']}
- Patient primary goal: {inputs['patient_goal']}

TASK:
Generate a structured clinical reasoning summary in valid JSON. Return ONLY the JSON object, no preamble or markdown fences.

Schema:
{{
  "options": [
    {{
      "name": "string — short strategy name",
      "description": "string — 2-3 sentences describing this approach",
      "pros": ["string", "string", "string"],
      "cons": ["string", "string", "string"],
      "best_fit_when": "string — 1-2 sentences on ideal patient profile"
    }}
  ],
  "comparative_reasoning": "string — 3-5 sentences comparing options for THIS patient",
  "decision_drivers": ["string", "string", "string"],
  "suggested_direction": "string — 2-3 sentences of soft non-definitive guidance",
  "uncertainty_note": "string — key uncertainties or missing info that would change this analysis"
}}

Rules:
- Generate 2 to 3 meaningfully distinct management options
- Before listing options, identify if there is a true decision bottleneck — a barrier (patient preference, missing workup, active contraindication) that must be addressed before other decisions can proceed. If one exists, name it explicitly in the comparative_reasoning, and frame all options relative to how they engage with or resolve that bottleneck
- PATIENT PREFERENCE BARRIERS (anticoagulation refusal, surgery avoidance, medication burden) must be treated as hard constraints that shape options — never as obstacles to route around. If a patient refuses a therapy, options must either work within that refusal or present a structured path to revisit it through shared decision-making
- Use conditional language throughout — "may," "could," "in appropriate candidates," "pending patient agreement" — never present any single option as clearly correct
- Where options can run in parallel or in sequence (e.g. rate control while awaiting cardioversion; cardioversion before considering ablation), say so explicitly rather than presenting them as mutually exclusive alternatives
- For AFib cases specifically: always reflect the cardioversion → antiarrhythmic → ablation escalation ladder where rhythm control is relevant. Do not compress these into a single "ablation" option
- Ablation should be framed as one reasonable point on the rhythm-control spectrum, not as a default or superior strategy. Anchor it to patient selection criteria (symptom burden, AFib type, antiarrhythmic failure/intolerance, patient preference after informed consent)
- Avoid stating specific numerical risk estimates (e.g. "2.2% stroke risk") — use qualitative terms like "elevated," "modest," "substantially increased" instead
- Keep all sections concise — pros/cons max 3 bullets each, option descriptions 2-3 sentences max
- Decision drivers = the 3 most influential factors in THIS case, including patient preferences or refusals when present
- For fields marked "Unknown": flag in one sentence and explain how it would change reasoning
- If many unknowns, scale back confidence and name the top 2 most needed pieces of information
- If input is nonsensical or not a real clinical case, set all option names to "Insufficient Clinical Information"
- Do not fabricate labs, scores, or imaging not mentioned
- Briefly clarify medical jargon used
"""

# ── Output renderer ───────────────────────────────────────────────────────────
CARD_COLORS = ["", "amber", "blue"]

def render_output(data: dict):
    options = data.get("options", [])
    st.markdown("<h2>Management Options</h2>", unsafe_allow_html=True)
    for i, opt in enumerate(options):
        color = CARD_COLORS[i] if i < len(CARD_COLORS) else ""
        pros_html = "".join(f"<li>{p}</li>" for p in opt.get("pros", []))
        cons_html = "".join(f"<li>{c}</li>" for c in opt.get("cons", []))
        st.markdown(f"""
        <div class="option-card {color}">
          <div class="tag">Option {i+1}</div>
          <h3>{opt.get('name','')}</h3>
          <p style="font-size:0.92rem;margin-bottom:0.8rem">{opt.get('description','')}</p>
          <div class="pro-con">
            <div class="pros"><strong>✓ Pros</strong><ul style="margin:0.4rem 0 0;padding-left:1.2rem">{pros_html}</ul></div>
            <div class="cons"><strong>✗ Cons</strong><ul style="margin:0.4rem 0 0;padding-left:1.2rem">{cons_html}</ul></div>
          </div>
          <p style="margin-top:0.9rem;font-size:0.85rem;color:#6a8fa8"><strong style="color:#8ab0cc">Best fit when:</strong> {opt.get('best_fit_when','')}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<h2>Comparative Reasoning</h2>", unsafe_allow_html=True)
    st.markdown(f"<div class='comp-reasoning'>{data.get('comparative_reasoning','')}</div>",
                unsafe_allow_html=True)

    st.markdown("<h2>Key Decision Drivers</h2>", unsafe_allow_html=True)
    drivers_html = "".join(f'<span class="driver-chip">{d}</span>' for d in data.get("decision_drivers", []))
    st.markdown(f"<div style='margin:0.5rem 0 1.2rem'>{drivers_html}</div>", unsafe_allow_html=True)

    st.markdown("<h2>Suggested Direction</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="rec-box">
      <h4>⚖️ Soft Directional Guidance</h4>
      <p style="margin:0;font-size:0.93rem;line-height:1.7">{data.get('suggested_direction','')}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="disclaimer">
      <strong>⚠️ Uncertainty note:</strong> {data.get('uncertainty_note','')}<br><br>
      <strong>Disclaimer:</strong> This tool is a prototype for educational and decision-support purposes only. It does not constitute clinical advice, diagnosis, or treatment recommendations. All management decisions must be made by qualified clinicians based on complete patient evaluation. Do not use this output to guide real patient care.
    </div>
    """, unsafe_allow_html=True)

# ── Autofill logic ────────────────────────────────────────────────────────────
if autofill_btn:
    if not api_key:
        st.error("Please enter your Anthropic API key.")
    elif not case_narrative.strip():
        st.warning("Please enter a case narrative first.")
    else:
        with st.spinner("Parsing narrative — auto-filling sidebar..."):
            try:
                client = anthropic.Anthropic(api_key=api_key)
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=1000,
                    messages=[{"role": "user", "content": build_autofill_prompt(case_narrative)}]
                )
                raw = response.content[0].text.strip()
                raw = re.sub(r'^```(?:json)?\s*', '', raw)
                raw = re.sub(r'\s*```$', '', raw)
                parsed = json.loads(raw)
                for key, val in parsed.items():
                    st.session_state[key] = val
                st.success("✅ Sidebar auto-filled! Review fields then click Analyze Case.")
                st.rerun()
            except json.JSONDecodeError as e:
                st.error(f"Could not parse auto-fill response. Try again. ({e})")
            except Exception as e:
                st.error(f"Auto-fill error: {e}")

# ── Analysis logic ────────────────────────────────────────────────────────────
if analyze_btn:
    if not api_key:
        st.error("Please enter your Anthropic API key.")
    elif not case_narrative.strip():
        st.warning("Please enter a case narrative.")
    else:
        inputs = {
            "narrative": case_narrative,
            "age": age, "sex": sex,
            "comorbidities": comorbidities,
            "functional_status": functional_status,
            "operative_risk": operative_risk,
            "clinical_setting": clinical_setting,
            "patient_goal": patient_goal,
        }
        with st.spinner(f"Analyzing {module['label']} case..."):
            try:
                client = anthropic.Anthropic(api_key=api_key)
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=4000,
                    messages=[{"role": "user", "content": build_prompt(inputs, module)}]
                )
                raw = response.content[0].text.strip()
                raw = re.sub(r'^```(?:json)?\s*', '', raw)
                raw = re.sub(r'\s*```$', '', raw)
                data = json.loads(raw)
                render_output(data)
            except json.JSONDecodeError as e:
                st.error(f"Could not parse model response. Try again. ({e})")
                with st.expander("Raw output"):
                    st.code(raw)
            except anthropic.AuthenticationError:
                st.error("Invalid API key.")
            except Exception as e:
                st.error(f"Error: {e}")

elif not analyze_btn and not autofill_btn:
    pass
