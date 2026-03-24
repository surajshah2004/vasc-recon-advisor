import streamlit as st
import anthropic
import json
import re
from sample_cases import SAMPLE_CASES

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VascRecon Advisor",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3, h4 { font-family: 'Playfair Display', serif; }

/* Main background — warm deep slate */
.main { background-color: #0f1923; }
.stApp { background-color: #0f1923; }

/* Main content area subtle texture */
.block-container {
    background-color: #0f1923;
    padding-top: 2rem !important;
}

/* Sidebar — slightly lighter slate */
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

/* Header banner */
.header-banner {
    background: linear-gradient(135deg, #141f2e 0%, #1a3a5c 60%, #1e4d7a 100%);
    color: white;
    padding: 2rem 2.5rem;
    border-radius: 14px;
    margin-bottom: 2rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
    border: 1px solid #1e3a5a;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
}
.header-banner h1 { color: white; margin: 0; font-size: 2rem; letter-spacing: -0.02em; }
.header-banner p { color: #7ab0d4; margin: 0.3rem 0 0; font-size: 0.9rem; font-weight: 300; }

/* Cards */
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
.option-card .best-fit { color: #6a8fa8 !important; font-size: 0.85rem; margin-top: 0.9rem; }
.option-card .best-fit strong { color: #8ab0cc; }

/* Comparative reasoning */
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

/* Driver chips */
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

/* Recommendation box */
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

/* Disclaimer */
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

/* Section labels */
.section-label {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #3a5a7a;
    margin: 1.8rem 0 0.5rem;
}

/* Section headers */
h2 { color: #c8d8e8 !important; font-size: 1.3rem !important; margin-top: 2rem !important; }

/* Text area and inputs in main area */
.stTextArea textarea {
    background-color: #141f2e !important;
    color: #c8d8e8 !important;
    border: 1px solid #1e3a5a !important;
    border-radius: 8px !important;
}
.stTextArea label { color: #5a7a9a !important; }

/* Ready state placeholder */
.ready-state {
    text-align: center;
    padding: 5rem 2rem;
    color: #3a5a7a;
}
.ready-state h3 { color: #4a7a9a; font-size: 1.6rem; margin-top: 1rem; }
.ready-state p { color: #3a5a7a; max-width: 480px; margin: 0.5rem auto; line-height: 1.7; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
  <div style="font-size:3rem">🩺</div>
  <div>
    <h1>VascRecon Advisor</h1>
    <p>Decision-support for lower extremity wounds at the intersection of vascular and reconstructive surgery &nbsp;·&nbsp; <em>Prototype — not for clinical use</em></p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar — structured inputs ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📋 Patient Inputs")

    # Sample case loader
    st.markdown('<p class="section-label">Load a sample case</p>', unsafe_allow_html=True)
    sample_names = ["— select —"] + [c["name"] for c in SAMPLE_CASES]
    chosen_sample = st.selectbox("Sample cases", sample_names, label_visibility="collapsed")

    # Populate defaults from sample or autofill — safe version
    def get_default(field, fallback, options=None):
        val = None
        if f"autofill_{field}" in st.session_state:
            val = st.session_state[f"autofill_{field}"]
        elif chosen_sample and chosen_sample != "— select —":
            case = next((c for c in SAMPLE_CASES if c["name"] == chosen_sample), None)
            if case:
                val = case.get(field, fallback)
        if val is None:
            return fallback
        # If options provided, verify value is valid — fall back if not
        if options is not None and val not in options:
            return fallback
        return val

    def safe_index(options, field, fallback):
        val = get_default(field, fallback, options)
        return options.index(val) if val in options else options.index(fallback)

    st.markdown("---")
    st.markdown('<p class="section-label">Demographics</p>', unsafe_allow_html=True)
    age_default = get_default("age", 65)
    age = st.number_input("Age", 18, 100, value=int(age_default) if str(age_default).isdigit() or isinstance(age_default, int) else 65)
    sex_opts = ["Male", "Female", "Other/Not specified"]
    sex = st.selectbox("Sex", sex_opts, index=safe_index(sex_opts, "sex", "Male"))

    st.markdown('<p class="section-label">Comorbidities</p>', unsafe_allow_html=True)
    all_comorbidities = ["Diabetes", "Smoking", "Coronary artery disease", "Heart failure",
                         "Peripheral arterial disease", "Chronic kidney disease",
                         "Prior stroke", "Hypertension", "Obesity", "COPD"]
    raw_comorbidities = get_default("comorbidities", [])
    safe_comorbidities = [c for c in raw_comorbidities if c in all_comorbidities] if isinstance(raw_comorbidities, list) else []
    comorbidities = st.multiselect("Select all that apply", all_comorbidities, default=safe_comorbidities)

    st.markdown('<p class="section-label">Functional & operative status</p>', unsafe_allow_html=True)
    func_opts = ["Good", "Limited", "Poor", "Unknown"]
    functional_status = st.selectbox("Functional status", func_opts, index=safe_index(func_opts, "functional_status", "Unknown"))
    risk_opts = ["Low", "Moderate", "High", "Unknown"]
    operative_risk = st.selectbox("Operative risk", risk_opts, index=safe_index(risk_opts, "operative_risk", "Unknown"))
    amb_opts = ["Fully ambulatory", "Limited ambulation", "Non-ambulatory", "Unknown"]
    ambulatory = st.selectbox("Ambulatory status", amb_opts, index=safe_index(amb_opts, "ambulatory", "Unknown"))

    st.markdown('<p class="section-label">Vascular status</p>', unsafe_allow_html=True)
    vasc_status_opts = ["Normal/adequate perfusion","Mild disease","Moderate disease","Severe ischemia","Unknown"]
    vascular_status = st.selectbox("Vascular perfusion", vasc_status_opts, index=safe_index(vasc_status_opts, "vascular_status", "Unknown"))
    prior_vasc_opts = ["None","Prior revascularization","Prior bypass","Prior angioplasty/stent","Unknown"]
    prior_vasc = st.selectbox("Prior vascular intervention", prior_vasc_opts, index=safe_index(prior_vasc_opts, "prior_vasc", "Unknown"))

    st.markdown('<p class="section-label">Wound characteristics</p>', unsafe_allow_html=True)
    loc_opts = ["Forefoot","Midfoot","Heel","Ankle","Lower leg","Other","Unknown"]
    wound_location = st.selectbox("Location", loc_opts, index=safe_index(loc_opts, "wound_location", "Unknown"))
    size_opts = ["Small (<2 cm)","Medium (2–5 cm)","Large (>5 cm)","Unknown"]
    wound_size = st.selectbox("Size", size_opts, index=safe_index(size_opts, "wound_size", "Unknown"))
    depth_opts = ["Superficial","Into subcutaneous tissue","Exposed tendon/bone","Deep/complex","Unknown"]
    wound_depth = st.selectbox("Depth", depth_opts, index=safe_index(depth_opts, "wound_depth", "Unknown"))
    infect_opts = ["None","Suspected","Confirmed localized","Confirmed deep/osteomyelitis","Unknown"]
    infection = st.selectbox("Infection status", infect_opts, index=safe_index(infect_opts, "infection", "Unknown"))
    tissue_opts = ["Healthy appearing","Necrotic tissue present","Mixed/unclear","Unknown"]
    tissue = st.selectbox("Tissue status", tissue_opts, index=safe_index(tissue_opts, "tissue", "Unknown"))
    chron_opts = ["Acute (<4 wks)","Subacute (4–12 wks)","Chronic (>12 wks)","Unknown"]
    chronicity = st.selectbox("Chronicity", chron_opts, index=safe_index(chron_opts, "chronicity", "Unknown"))
    pain_opts = ["None","Mild","Moderate","Severe","Unknown"]
    pain = st.selectbox("Pain level", pain_opts, index=safe_index(pain_opts, "pain", "Unknown"))

    st.markdown('<p class="section-label">Patient priority</p>', unsafe_allow_html=True)
    goal_opts = ["Limb salvage","Fastest healing","Avoid major surgery","Preserve function","Pain control","Not specified"]
    patient_goal = st.selectbox("Primary goal", goal_opts, index=safe_index(goal_opts, "patient_goal", "Not specified"))

# ── Auto-parse prompt ─────────────────────────────────────────────────────────
def build_autofill_prompt(narrative: str) -> str:
    return f"""You are a clinical data extraction assistant. Read the following clinical case narrative and extract structured fields.

NARRATIVE:
{narrative}

Return ONLY a valid JSON object with these exact keys and allowed values:

{{
  "age": <integer, or 65 if unknown>,
  "sex": "<Male|Female|Other/Not specified>",
  "comorbidities": [<list from: "Diabetes","Smoking","Coronary artery disease","Heart failure","Peripheral arterial disease","Chronic kidney disease","Prior stroke","Hypertension","Obesity","COPD">],
  "functional_status": "<Good|Limited|Poor|Unknown>",
  "operative_risk": "<Low|Moderate|High|Unknown>",
  "ambulatory": "<Fully ambulatory|Limited ambulation|Non-ambulatory|Unknown>",
  "vascular_status": "<Normal/adequate perfusion|Mild disease|Moderate disease|Severe ischemia|Unknown>",
  "prior_vasc": "<None|Prior revascularization|Prior bypass|Prior angioplasty/stent|Unknown>",
  "wound_location": "<Forefoot|Midfoot|Heel|Ankle|Lower leg|Other|Unknown>",
  "wound_size": "<Small (<2 cm)|Medium (2–5 cm)|Large (>5 cm)|Unknown>",
  "wound_depth": "<Superficial|Into subcutaneous tissue|Exposed tendon/bone|Deep/complex|Unknown>",
  "infection": "<None|Suspected|Confirmed localized|Confirmed deep/osteomyelitis|Unknown>",
  "tissue": "<Healthy appearing|Necrotic tissue present|Mixed/unclear|Unknown>",
  "chronicity": "<Acute (<4 wks)|Subacute (4–12 wks)|Chronic (>12 wks)|Unknown>",
  "pain": "<None|Mild|Moderate|Severe|Unknown>",
  "patient_goal": "<Limb salvage|Fastest healing|Avoid major surgery|Preserve function|Pain control|Not specified>"
}}

Rules:
- Use ONLY the allowed values listed above — no variations
- If a field is clearly stated, extract it accurately
- If a field is ambiguous or not mentioned, use "Unknown" — do NOT guess
- Return ONLY the JSON, no explanation or markdown fences
"""

# ── Main area — case narrative + submit ───────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<p class="section-label">Case narrative</p>', unsafe_allow_html=True)
    default_narrative = get_default("narrative", "")
    case_narrative = st.text_area(
        "Provide a brief free-text summary of the case (chief complaint, relevant history, exam findings, imaging, labs)",
        value=default_narrative,
        height=160,
        placeholder="e.g. 68-year-old man with poorly controlled T2DM and PAD presenting with a 3-week-old plantar forefoot ulcer with mild surrounding erythema. ABI 0.62 on the right. No systemic signs of infection. Has not had prior vascular workup..."
    )
    autofill_btn = st.button("✨ Auto-fill fields from narrative", help="Uses AI to parse your narrative and populate the sidebar fields automatically")

with col2:
    st.markdown('<p class="section-label">API key</p>', unsafe_allow_html=True)
    # Try to load from Streamlit secrets, fall back to manual entry
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
    except:
        api_key = st.text_input("Anthropic API key", type="password",
                                help="Your key stays in-session only, never stored.")
    st.markdown("")
    analyze_btn = st.button("🔍 Analyze Case", use_container_width=True, type="primary")

# ── Auto-fill logic ───────────────────────────────────────────────────────────
if autofill_btn:
    if not api_key:
        st.error("Please enter your Anthropic API key first.")
    elif not case_narrative.strip():
        st.warning("Please enter a case narrative to auto-fill from.")
    else:
        with st.spinner("Parsing narrative — auto-filling fields..."):
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

                # Store parsed fields in session state
                for key, val in parsed.items():
                    st.session_state[f"autofill_{key}"] = val

                st.success("✅ Fields auto-filled from narrative! Review the sidebar and click Analyze Case.")
                st.rerun()

            except json.JSONDecodeError as e:
                st.error(f"Could not parse auto-fill response. Try again. ({e})")
            except Exception as e:
                st.error(f"Auto-fill error: {e}")

st.markdown("---")

# ── Prompt builder ────────────────────────────────────────────────────────────
def build_prompt(inputs: dict) -> str:
    return f"""You are a clinical reasoning assistant supporting multidisciplinary teams managing complex lower extremity wounds where vascular disease intersects with reconstructive needs. You do NOT make clinical decisions. You organize and explain competing management strategies to support discussion.

PATIENT SUMMARY:
{inputs['narrative'] or '(No narrative provided)'}

STRUCTURED DATA:
- Age/Sex: {inputs['age']} y/o {inputs['sex']}
- Comorbidities: {', '.join(inputs['comorbidities']) if inputs['comorbidities'] else 'None listed'}
- Functional status: {inputs['functional_status']}
- Ambulatory status: {inputs['ambulatory']}
- Operative risk: {inputs['operative_risk']}
- Vascular status: {inputs['vascular_status']}
- Prior vascular intervention: {inputs['prior_vasc']}
- Wound location: {inputs['wound_location']}
- Wound size: {inputs['wound_size']}
- Wound depth: {inputs['wound_depth']}
- Infection: {inputs['infection']}
- Tissue status: {inputs['tissue']}
- Chronicity: {inputs['chronicity']}
- Pain: {inputs['pain']}
- Patient's primary goal: {inputs['patient_goal']}

TASK:
Generate a structured clinical reasoning summary in valid JSON. Return ONLY the JSON object, no preamble or markdown fences.

The JSON must follow this exact schema:
{{
  "options": [
    {{
      "name": "string — short strategy name",
      "description": "string — 2-3 sentence description of this approach",
      "pros": ["string", "string", "string"],
      "cons": ["string", "string", "string"],
      "best_fit_when": "string — 1-2 sentences describing ideal patient profile for this strategy"
    }}
  ],
  "comparative_reasoning": "string — 3-5 sentences comparing the options against each other given THIS patient's specific profile",
  "decision_drivers": ["string", "string", "string"],
  "suggested_direction": "string — 2-3 sentences of soft directional guidance, explicitly framed as non-definitive",
  "uncertainty_note": "string — 1-2 sentences about key uncertainties or missing information that would change this analysis"
}}

Rules:
- Generate 2 to 3 options (not more, not fewer)
- Options must be meaningfully different strategies (e.g. conservative care vs revascularization-first vs amputation vs reconstruction)
- Do NOT recommend one option with high confidence; acknowledge genuine tradeoffs
- Be specific to this patient — avoid generic statements that would apply to any wound
- Decision drivers must be the 3 most influential factors specific to this case
- For any field marked "Unknown": do not assume or fabricate a value — instead explicitly flag it as a gap and explain how knowing it would change the reasoning
- If many fields are Unknown, scale back the confidence of all options significantly and use the uncertainty_note to list the most important missing information needed before any management decision
- If the input appears to be nonsensical, a joke, or clearly not a real clinical case, return options with name "Insufficient Clinical Information" and use the uncertainty_note to explain that a real case narrative is needed
- Do not use medical jargon without brief clarification
- Do not fabricate specific imaging findings or lab values not mentioned
"""

# ── Output renderer ───────────────────────────────────────────────────────────
CARD_COLORS = ["", "amber", "blue"]

def render_output(data: dict):
    options = data.get("options", [])

    st.markdown("<h2 style='color:#1a2332'>Management Options</h2>", unsafe_allow_html=True)
    for i, opt in enumerate(options):
        color = CARD_COLORS[i] if i < len(CARD_COLORS) else ""
        pros_html = "".join(f"<li>{p}</li>" for p in opt.get("pros", []))
        cons_html = "".join(f"<li>{c}</li>" for c in opt.get("cons", []))
        st.markdown(f"""
        <div class="option-card {color}">
          <div class="tag">Option {i+1}</div>
          <h3>{opt.get('name','')}</h3>
          <p style="color:#444;font-size:0.92rem;margin-bottom:0.8rem">{opt.get('description','')}</p>
          <div class="pro-con">
            <div class="pros"><strong>✓ Pros</strong><ul style="margin:0.4rem 0 0;padding-left:1.2rem">{pros_html}</ul></div>
            <div class="cons"><strong>✗ Cons</strong><ul style="margin:0.4rem 0 0;padding-left:1.2rem">{cons_html}</ul></div>
          </div>
          <p style="margin-top:0.9rem;font-size:0.85rem;color:#555"><strong>Best fit when:</strong> {opt.get('best_fit_when','')}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<h2 style='color:#1a2332'>Comparative Reasoning</h2>", unsafe_allow_html=True)
    st.markdown(f"<div class='comp-reasoning'>{data.get('comparative_reasoning','')}</div>",
                unsafe_allow_html=True)

    st.markdown("<h2 style='color:#1a2332'>Key Decision Drivers</h2>", unsafe_allow_html=True)
    drivers_html = "".join(f'<span class="driver-chip">{d}</span>' for d in data.get("decision_drivers", []))
    st.markdown(f"<div style='margin:0.5rem 0 1rem'>{drivers_html}</div>", unsafe_allow_html=True)

    st.markdown("<h2 style='color:#1a2332'>Suggested Direction</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="rec-box">
      <h4>⚖️ Soft Directional Guidance</h4>
      <p style="margin:0;font-size:0.93rem;line-height:1.7;color:#1a2332">{data.get('suggested_direction','')}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="disclaimer">
      <strong>⚠️ Uncertainty note:</strong> {data.get('uncertainty_note','')}<br><br>
      <strong>Fixed disclaimer:</strong> This tool is a prototype designed for educational and decision-support purposes only. It does not constitute clinical advice, diagnosis, or treatment recommendations. All management decisions must be made by qualified clinicians in the context of a complete patient evaluation. Do not use this output to guide real patient care.
    </div>
    """, unsafe_allow_html=True)

# ── Main logic ────────────────────────────────────────────────────────────────
if analyze_btn:
    if not api_key:
        st.error("Please enter your Anthropic API key in the sidebar.")
    elif not case_narrative.strip() and chosen_sample == "— select —":
        st.warning("Please enter a case narrative or load a sample case.")
    else:
        inputs = {
            "narrative": case_narrative,
            "age": age, "sex": sex,
            "comorbidities": comorbidities,
            "functional_status": functional_status,
            "operative_risk": operative_risk,
            "ambulatory": ambulatory,
            "vascular_status": vascular_status,
            "prior_vasc": prior_vasc,
            "wound_location": wound_location,
            "wound_size": wound_size,
            "wound_depth": wound_depth,
            "infection": infection,
            "tissue": tissue,
            "chronicity": chronicity,
            "pain": pain,
            "patient_goal": patient_goal,
        }

        with st.spinner("Analyzing case — generating management options..."):
            try:
                client = anthropic.Anthropic(api_key=api_key)
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=4000,
                    messages=[{"role": "user", "content": build_prompt(inputs)}]
                )
                raw = response.content[0].text.strip()

                # Strip markdown fences if model adds them
                raw = re.sub(r'^```(?:json)?\s*', '', raw)
                raw = re.sub(r'\s*```$', '', raw)

                data = json.loads(raw)
                render_output(data)

            except json.JSONDecodeError as e:
                st.error(f"Could not parse model response as JSON. Try again. ({e})")
                with st.expander("Raw model output"):
                    st.code(raw)
            except anthropic.AuthenticationError:
                st.error("Invalid API key. Check your Anthropic API key and try again.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

else:
    # Placeholder state
    st.markdown("""
    <div class="ready-state">
      <div style="font-size:4rem">🫀</div>
      <h3>Ready to analyze</h3>
      <p>Fill in patient details in the sidebar, enter a case narrative above,
        and click <strong style="color:#7ab0d4">Analyze Case</strong>.
        Or load one of the built-in sample cases to explore the tool.</p>
    </div>
    """, unsafe_allow_html=True)
