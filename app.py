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
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3 { font-family: 'DM Serif Display', serif; }

.main { background-color: #f7f6f2; }

.stApp { background-color: #f7f6f2; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #1a2332;
    color: #e8e4dc;
}
section[data-testid="stSidebar"] * { color: #e8e4dc !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stTextInput label,
section[data-testid="stSidebar"] .stMultiSelect label { color: #a8b5c8 !important; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em; }

/* Header banner */
.header-banner {
    background: linear-gradient(135deg, #1a2332 0%, #2d4a6b 100%);
    color: white;
    padding: 2rem 2.5rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
}
.header-banner h1 { color: white; margin: 0; font-size: 2rem; }
.header-banner p { color: #a8c4e0; margin: 0.3rem 0 0; font-size: 0.95rem; font-weight: 300; }

/* Cards */
.option-card {
    background: white;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    border-left: 5px solid #2d6a4f;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}
.option-card.amber { border-left-color: #d4892a; }
.option-card.blue  { border-left-color: #2d4a9b; }
.option-card h3 { margin-top: 0; font-size: 1.15rem; color: #1a2332; }
.option-card .tag {
    display: inline-block;
    background: #e8f5ee;
    color: #2d6a4f;
    border-radius: 4px;
    padding: 2px 10px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 0.7rem;
}
.option-card.amber .tag { background: #fdf0dc; color: #d4892a; }
.option-card.blue  .tag { background: #e8edf8; color: #2d4a9b; }

.pro-con { display: flex; gap: 1rem; margin-top: 0.8rem; }
.pros, .cons {
    flex: 1;
    background: #f9f9f7;
    border-radius: 6px;
    padding: 0.75rem 1rem;
    font-size: 0.88rem;
    color: #2a2a2a !important;
}
.pros strong { color: #2d6a4f; }
.cons strong { color: #c0392b; }
.pros ul li, .cons ul li { color: #2a2a2a !important; }

/* Comparative reasoning */
.comp-reasoning {
    font-size: 0.95rem;
    color: #2a2a2a !important;
    line-height: 1.7;
    background: white;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}

/* Driver chips */
.driver-chip {
    display: inline-block;
    background: #1a2332;
    color: #a8c4e0 !important;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.82rem;
    margin: 4px;
}

/* Recommendation box */
.rec-box {
    background: linear-gradient(135deg, #e8f5ee, #f0f8f0);
    border: 1.5px solid #2d6a4f;
    border-radius: 10px;
    padding: 1.4rem 1.8rem;
    margin: 1.2rem 0;
}
.rec-box h4 { color: #1a5c38; margin-top: 0; }

/* Disclaimer */
.disclaimer {
    background: #fff8e7;
    border: 1px solid #f0c040;
    border-radius: 8px;
    padding: 1rem 1.4rem;
    font-size: 0.82rem;
    color: #7a5c00;
    margin-top: 1.5rem;
}

/* Divider */
.section-label {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #8a9ab0;
    margin: 1.8rem 0 0.5rem;
}
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

    # Populate defaults from sample or autofill
    def get_default(field, fallback):
        # Autofill from narrative takes priority
        if f"autofill_{field}" in st.session_state:
            return st.session_state[f"autofill_{field}"]
        if chosen_sample and chosen_sample != "— select —":
            case = next((c for c in SAMPLE_CASES if c["name"] == chosen_sample), None)
            if case:
                return case.get(field, fallback)
        return fallback

    st.markdown("---")
    st.markdown('<p class="section-label">Demographics</p>', unsafe_allow_html=True)
    age = st.number_input("Age", 18, 100, value=get_default("age", 65))
    sex = st.selectbox("Sex", ["Male", "Female", "Other/Not specified"],
                       index=["Male","Female","Other/Not specified"].index(get_default("sex","Male")))

    st.markdown('<p class="section-label">Comorbidities</p>', unsafe_allow_html=True)
    all_comorbidities = ["Diabetes", "Smoking", "Coronary artery disease", "Heart failure",
                         "Peripheral arterial disease", "Chronic kidney disease",
                         "Prior stroke", "Hypertension", "Obesity", "COPD"]
    comorbidities = st.multiselect("Select all that apply", all_comorbidities,
                                   default=get_default("comorbidities", []))

    st.markdown('<p class="section-label">Functional & operative status</p>', unsafe_allow_html=True)
    functional_status = st.selectbox("Functional status",
        ["Good", "Limited", "Poor"],
        index=["Good","Limited","Poor"].index(get_default("functional_status","Good")))
    operative_risk = st.selectbox("Operative risk",
        ["Low", "Moderate", "High"],
        index=["Low","Moderate","High"].index(get_default("operative_risk","Low")))
    ambulatory = st.selectbox("Ambulatory status",
        ["Fully ambulatory", "Limited ambulation", "Non-ambulatory"],
        index=["Fully ambulatory","Limited ambulation","Non-ambulatory"].index(
            get_default("ambulatory","Fully ambulatory")))

    st.markdown('<p class="section-label">Vascular status</p>', unsafe_allow_html=True)
    vasc_status_opts = ["Normal/adequate perfusion","Mild disease","Moderate disease","Severe ischemia","Unknown"]
    vascular_status = st.selectbox("Vascular perfusion",
        vasc_status_opts,
        index=vasc_status_opts.index(get_default("vascular_status","Normal/adequate perfusion")))
    prior_vasc_opts = ["None","Prior revascularization","Prior bypass","Prior angioplasty/stent"]
    prior_vasc = st.selectbox("Prior vascular intervention",
        prior_vasc_opts,
        index=prior_vasc_opts.index(get_default("prior_vasc","None")))

    st.markdown('<p class="section-label">Wound characteristics</p>', unsafe_allow_html=True)
    wound_location = st.selectbox("Location",
        ["Forefoot","Midfoot","Heel","Ankle","Lower leg","Other"],
        index=["Forefoot","Midfoot","Heel","Ankle","Lower leg","Other"].index(
            get_default("wound_location","Forefoot")))
    wound_size = st.selectbox("Size",
        ["Small (<2 cm)","Medium (2–5 cm)","Large (>5 cm)"],
        index=["Small (<2 cm)","Medium (2–5 cm)","Large (>5 cm)"].index(
            get_default("wound_size","Small (<2 cm)")))
    wound_depth = st.selectbox("Depth",
        ["Superficial","Into subcutaneous tissue","Exposed tendon/bone","Deep/complex"],
        index=["Superficial","Into subcutaneous tissue","Exposed tendon/bone","Deep/complex"].index(
            get_default("wound_depth","Superficial")))
    infection = st.selectbox("Infection status",
        ["None","Suspected","Confirmed localized","Confirmed deep/osteomyelitis"],
        index=["None","Suspected","Confirmed localized","Confirmed deep/osteomyelitis"].index(
            get_default("infection","None")))
    tissue = st.selectbox("Tissue status",
        ["Healthy appearing","Necrotic tissue present","Mixed/unclear"],
        index=["Healthy appearing","Necrotic tissue present","Mixed/unclear"].index(
            get_default("tissue","Healthy appearing")))
    chronicity = st.selectbox("Chronicity",
        ["Acute (<4 wks)","Subacute (4–12 wks)","Chronic (>12 wks)"],
        index=["Acute (<4 wks)","Subacute (4–12 wks)","Chronic (>12 wks)"].index(
            get_default("chronicity","Acute (<4 wks)")))
    pain = st.selectbox("Pain level",
        ["None","Mild","Moderate","Severe"],
        index=["None","Mild","Moderate","Severe"].index(get_default("pain","None")))

    st.markdown('<p class="section-label">Patient priority</p>', unsafe_allow_html=True)
    goal_opts = ["Limb salvage","Fastest healing","Avoid major surgery",
                 "Preserve function","Pain control","Not specified"]
    patient_goal = st.selectbox("Primary goal",
        goal_opts,
        index=goal_opts.index(get_default("patient_goal","Not specified")))

# ── Auto-parse prompt ─────────────────────────────────────────────────────────
def build_autofill_prompt(narrative: str) -> str:
    return f"""You are a clinical data extraction assistant. Read the following clinical case narrative and extract structured fields.

NARRATIVE:
{narrative}

Return ONLY a valid JSON object with these exact keys and allowed values:

{{
  "age": <integer or 65 if unknown>,
  "sex": "<Male|Female|Other/Not specified>",
  "comorbidities": [<list from: "Diabetes","Smoking","Coronary artery disease","Heart failure","Peripheral arterial disease","Chronic kidney disease","Prior stroke","Hypertension","Obesity","COPD">],
  "functional_status": "<Good|Limited|Poor>",
  "operative_risk": "<Low|Moderate|High>",
  "ambulatory": "<Fully ambulatory|Limited ambulation|Non-ambulatory>",
  "vascular_status": "<Normal/adequate perfusion|Mild disease|Moderate disease|Severe ischemia|Unknown>",
  "prior_vasc": "<None|Prior revascularization|Prior bypass|Prior angioplasty/stent>",
  "wound_location": "<Forefoot|Midfoot|Heel|Ankle|Lower leg|Other>",
  "wound_size": "<Small (<2 cm)|Medium (2–5 cm)|Large (>5 cm)>",
  "wound_depth": "<Superficial|Into subcutaneous tissue|Exposed tendon/bone|Deep/complex>",
  "infection": "<None|Suspected|Confirmed localized|Confirmed deep/osteomyelitis>",
  "tissue": "<Healthy appearing|Necrotic tissue present|Mixed/unclear>",
  "chronicity": "<Acute (<4 wks)|Subacute (4–12 wks)|Chronic (>12 wks)>",
  "pain": "<None|Mild|Moderate|Severe>",
  "patient_goal": "<Limb salvage|Fastest healing|Avoid major surgery|Preserve function|Pain control|Not specified>"
}}

Rules:
- Use ONLY the allowed values listed above — no variations
- If a field is not mentioned, make a reasonable clinical inference or use the most neutral option
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
        st.success("🔑 API key loaded", icon="✅")
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
    <div style="text-align:center;padding:4rem 2rem;color:#8a9ab0">
      <div style="font-size:4rem">🫀</div>
      <h3 style="font-family:'DM Serif Display',serif;color:#2a3a4a;margin-top:1rem">Ready to analyze</h3>
      <p style="max-width:480px;margin:0.5rem auto;line-height:1.6">
        Fill in patient details in the sidebar, enter a case narrative above,
        add your Anthropic API key, and click <strong>Analyze Case</strong>.
        Or load one of the built-in sample cases to explore the tool.
      </p>
    </div>
    """, unsafe_allow_html=True)
