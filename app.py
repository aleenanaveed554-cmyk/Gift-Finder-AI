import streamlit as st
from groq import Groq
import json
import re

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Gift Finder AI",
    page_icon="🎁",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

    * {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(255, 190, 120, 0.12), transparent 28%),
            radial-gradient(circle at 90% 20%, rgba(180, 120, 255, 0.12), transparent 30%),
            linear-gradient(135deg, #08080d 0%, #11101a 50%, #09090d 100%);
        color: #ffffff;
    }

    header {
        visibility: hidden;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    .brand {
        font-size: 1.25rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.5px;
    }

    .brand span {
        color: #f3b45b;
    }

    .hero {
        text-align: center;
        padding: 55px 20px 35px;
    }

    .badge {
        display: inline-block;
        padding: 8px 16px;
        border: 1px solid rgba(243,180,91,0.35);
        background: rgba(243,180,91,0.08);
        border-radius: 999px;
        color: #f3b45b;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 18px;
    }

    .hero h1 {
        font-family: 'Playfair Display', serif;
        font-size: 3.8rem;
        line-height: 1.05;
        margin: 0;
        color: #ffffff;
    }

    .hero h1 span {
        color: #f3b45b;
    }

    .hero p {
        max-width: 700px;
        margin: 20px auto;
        color: #b9b8c2;
        font-size: 1.08rem;
        line-height: 1.7;
    }

    .section-title {
        font-size: 1.45rem;
        font-weight: 700;
        color: #ffffff;
        margin: 28px 0 14px;
    }

    .section-subtitle {
        color: #96959f;
        margin-bottom: 20px;
    }

    .info-card {
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 22px;
        padding: 24px;
        margin-bottom: 18px;
        box-shadow: 0 15px 45px rgba(0,0,0,0.18);
    }

    .gift-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.065), rgba(255,255,255,0.025));
        border: 1px solid rgba(243,180,91,0.18);
        border-radius: 22px;
        padding: 24px;
        margin: 12px 0;
        min-height: 360px;
        box-shadow: 0 15px 45px rgba(0,0,0,0.25);
    }

    .gift-card:hover {
        border-color: rgba(243,180,91,0.45);
    }

    .gift-name {
        font-size: 1.35rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 8px;
    }

    .price {
        color: #f3b45b;
        font-weight: 700;
        font-size: 1rem;
    }

    .category {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 999px;
        background: rgba(243,180,91,0.10);
        color: #f3b45b;
        font-size: 0.75rem;
        margin: 5px 0;
    }

    .best-match {
        display: inline-block;
        background: linear-gradient(90deg, #f3b45b, #ffd99b);
        color: #16120d;
        font-size: 0.72rem;
        font-weight: 800;
        padding: 6px 11px;
        border-radius: 999px;
        margin-bottom: 12px;
    }

    .gift-label {
        color: #f3b45b;
        font-weight: 700;
        font-size: 0.82rem;
        margin-top: 15px;
        margin-bottom: 4px;
    }

    .gift-text {
        color: #d2d1d7;
        line-height: 1.55;
        font-size: 0.9rem;
    }

    .top-pick {
        background: linear-gradient(135deg, rgba(243,180,91,0.12), rgba(255,255,255,0.035));
        border: 1px solid rgba(243,180,91,0.3);
        border-radius: 20px;
        padding: 20px;
        min-height: 145px;
    }

    .top-pick-title {
        color: #f3b45b;
        font-weight: 700;
        font-size: 0.9rem;
    }

    .top-pick-name {
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 700;
        margin-top: 8px;
    }

    .empty-state {
        text-align: center;
        padding: 70px 20px;
        background: rgba(255,255,255,0.03);
        border: 1px dashed rgba(255,255,255,0.13);
        border-radius: 24px;
        margin-top: 25px;
    }

    .empty-state .emoji {
        font-size: 3rem;
    }

    .empty-state h3 {
        color: white;
        margin-top: 15px;
    }

    .empty-state p {
        color: #9998a2;
    }

    div.stButton > button {
        border-radius: 12px;
        border: 1px solid rgba(243,180,91,0.3);
        background: rgba(255,255,255,0.05);
        color: #ffffff;
        font-weight: 600;
        min-height: 44px;
        transition: 0.2s ease;
    }

    div.stButton > button:hover {
        border-color: #f3b45b;
        color: #f3b45b;
        background: rgba(243,180,91,0.08);
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #f3b45b, #e99c38);
        color: #17120c;
        border: none;
        font-weight: 800;
    }

    div.stButton > button[kind="primary"]:hover {
        color: #17120c;
        box-shadow: 0 8px 25px rgba(243,180,91,0.25);
    }

    label {
        color: #dddce1 !important;
        font-weight: 600 !important;
    }

    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"],
    .stNumberInput input {
        background: rgba(255,255,255,0.055) !important;
        color: #ffffff !important;
        border-color: rgba(255,255,255,0.12) !important;
        border-radius: 12px !important;
    }

    .stMultiSelect div[data-baseweb="select"] {
        background: rgba(255,255,255,0.055) !important;
        border-radius: 12px !important;
    }

    .small-note {
        color: #777680;
        font-size: 0.78rem;
        text-align: center;
        margin-top: 30px;
    }

    .divider {
        height: 1px;
        background: rgba(255,255,255,0.08);
        margin: 30px 0;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if "results" not in st.session_state:
    st.session_state.results = None

if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "form_data" not in st.session_state:
    st.session_state.form_data = {}

# ---------------------------------------------------------
# GROQ CLIENT
# ---------------------------------------------------------
def get_groq_client():
    try:
        api_key = st.secrets["GROQ_API_KEY"]
        return Groq(api_key=api_key)
    except Exception:
        return None


# ---------------------------------------------------------
# AI GENERATION
# ---------------------------------------------------------
def generate_gifts(data):

    client = get_groq_client()

    if client is None:
        st.error(
            "Groq API key not found. Please add GROQ_API_KEY to Streamlit Secrets."
        )
        return None

    prompt = f"""
You are an expert personalized gift recommendation AI.

Analyze the following recipient information and generate highly thoughtful,
realistic and personalized gift recommendations.

RECIPIENT:
Name: {data['name']}
Relationship: {data['relationship']}
Age Group: {data['age_group']}
Gender: {data['gender']}
Personality: {data['personality']}
Hobbies & Interests: {data['interests']}
Favorite Colors: {data['colors']}
Favorite Brands/Categories: {data['brands']}

OCCASION:
{data['occasion']}

BUDGET:
{data['budget']}

GIFT PREFERENCES:
{data['preferences']}

Return ONLY valid JSON.

Use this exact structure:

{{
  "top_picks": {{
    "best_overall": "gift name",
    "most_thoughtful": "gift name",
    "best_budget": "gift name",
    "most_unique": "gift name",
    "premium_choice": "gift name"
  }},
  "gifts": [
    {{
      "name": "Gift Name",
      "description": "Short description",
      "why_perfect": "Explain specifically why it matches the recipient",
      "price_range": "Estimated price range",
      "personalization": "Personalization idea",
      "occasion": "Best occasion",
      "category": "Gift category",
      "surprise_level": "Low/Medium/High",
      "practicality": "Low/Medium/High",
      "emotional_value": "Low/Medium/High",
      "uniqueness": "Low/Medium/High",
      "gift_message": "Short card message"
    }}
  ]
}}

Generate 6 gift recommendations.
Avoid generic suggestions whenever possible.
Make the recommendations practical and realistic.
Consider the user's budget carefully.
"""

    try:
        response = client.chat.completions.create(
          model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional personalized gift recommendation engine."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.8,
            max_tokens=5000
        )

        content = response.choices[0].message.content.strip()

        # Remove markdown JSON fences if model adds them
        content = re.sub(r"```json", "", content)
        content = re.sub(r"```", "", content).strip()

        return json.loads(content)

    except Exception as e:
        st.error(f"AI generation failed: {str(e)}")
        return None


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown(
    '<div class="brand">🎁 Gift Finder <span>AI</span></div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="badge">✨ AI-Powered Personalized Gift Discovery</div>

    <h1>
        Find a Gift They’ll<br>
        <span>Actually Love.</span> 🎁
    </h1>

    <p>
        Tell us who you’re shopping for, what they love, and your budget.
        Gift Finder AI will turn those details into thoughtful,
        personalized gift ideas.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# INPUT FORM
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">👤 Tell Us About the Recipient</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">The more details you provide, the smarter your recommendations will be.</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    name = st.text_input(
        "Recipient Name",
        placeholder="e.g. Sarah"
    )

    relationship = st.selectbox(
        "Relationship",
        [
            "Friend",
            "Best Friend",
            "Mother",
            "Father",
            "Sister",
            "Brother",
            "Spouse",
            "Fiancé / Fiancée",
            "Partner",
            "Teacher",
            "Colleague",
            "Child",
            "Other"
        ]
    )

    age_group = st.selectbox(
        "Age Group",
        [
            "Under 13",
            "13–17",
            "18–24",
            "25–34",
            "35–44",
            "45–54",
            "55+"
        ]
    )

    gender = st.selectbox(
        "Gender (Optional)",
        [
            "Prefer not to say",
            "Female",
            "Male",
            "Other"
        ]
    )

with col2:
    personality = st.selectbox(
        "Personality Type",
        [
            "Creative & Artistic",
            "Adventurous",
            "Calm & Minimalist",
            "Social & Fun",
            "Bookish & Intellectual",
            "Tech Lover",
            "Fashionable",
            "Practical & Organized",
            "Romantic & Emotional",
            "Luxury Lover"
        ]
    )

    interests = st.text_area(
        "Hobbies & Interests",
        placeholder="e.g. photography, books, coffee, traveling, gaming...",
        height=100
    )

    colors = st.text_input(
        "Favorite Colors",
        placeholder="e.g. Black, Pink, Gold"
    )

    brands = st.text_input(
        "Favorite Brands / Categories",
        placeholder="e.g. Apple, Nike, skincare, books"
    )

# ---------------------------------------------------------
# OCCASION
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">🎉 Choose the Occasion</div>',
    unsafe_allow_html=True
)

occasion = st.selectbox(
    "What are you celebrating?",
    [
        "Birthday",
        "Wedding",
        "Anniversary",
        "Graduation",
        "Eid",
        "Christmas",
        "Valentine's Day",
        "Mother's Day",
        "Father's Day",
        "Friendship",
        "Thank You",
        "New Baby",
        "Housewarming",
        "Other"
    ]
)

# ---------------------------------------------------------
# BUDGET + PREFERENCES
# ---------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        '<div class="section-title">💰 Your Budget</div>',
        unsafe_allow_html=True
    )

    budget = st.selectbox(
        "Select Budget",
        [
            "Low Budget",
            "Medium Budget",
            "Premium",
            "Custom Budget"
        ]
    )

    custom_budget = ""

    if budget == "Custom Budget":
        custom_budget = st.text_input(
            "Enter Your Budget",
            placeholder="e.g. PKR 5,000"
        )

with col2:
    st.markdown(
        '<div class="section-title">🎁 Gift Preferences</div>',
        unsafe_allow_html=True
    )

    preferences = st.multiselect(
        "Choose gift categories",
        [
            "Personalized gifts",
            "Fashion",
            "Beauty",
            "Technology",
            "Books",
            "Home & Decor",
            "Accessories",
            "Experiences",
            "Handmade gifts",
            "Luxury gifts",
            "Practical gifts",
            "Funny gifts"
        ],
        default=[]
    )

# ---------------------------------------------------------
# MAIN BUTTONS
# ---------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    find_gift = st.button(
        "🎁 Find My Perfect Gifts →",
        type="primary",
        use_container_width=True
    )

if find_gift:

    if not name.strip():
        st.warning("Please enter the recipient's name.")

    elif not interests.strip():
        st.warning("Please add at least a few hobbies or interests.")

    elif not preferences:
        st.warning("Please select at least one gift preference.")

    else:

        final_budget = custom_budget if budget == "Custom Budget" else budget

        form_data = {
            "name": name,
            "relationship": relationship,
            "age_group": age_group,
            "gender": gender,
            "personality": personality,
            "interests": interests,
            "colors": colors,
            "brands": brands,
            "occasion": occasion,
            "budget": final_budget,
            "preferences": ", ".join(preferences)
        }

        st.session_state.form_data = form_data

        with st.spinner("✨ AI is finding gifts that actually match..."):
            result = generate_gifts(form_data)

        if result:
            st.session_state.results = result
            st.success("Your personalized gift ideas are ready! 🎁")


# ---------------------------------------------------------
# RESULTS
# ---------------------------------------------------------
if st.session_state.results:

    result = st.session_state.results

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">🏆 Your Top Picks</div>',
        unsafe_allow_html=True
    )

    top = result.get("top_picks", {})

    top_cols = st.columns(5)

    top_data = [
        ("🏆", "Best Overall", top.get("best_overall", "")),
        ("💝", "Most Thoughtful", top.get("most_thoughtful", "")),
        ("💰", "Best Budget", top.get("best_budget", "")),
        ("✨", "Most Unique", top.get("most_unique", "")),
        ("🎁", "Premium Choice", top.get("premium_choice", ""))
    ]

    for col, item in zip(top_cols, top_data):
        with col:
            st.markdown(
                f"""
                <div class="top-pick">
                    <div class="top-pick-title">
                        {item[0]} {item[1]}
                    </div>
                    <div class="top-pick-name">
                        {item[2]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # -----------------------------------------------------
    # ACTION BUTTONS
    # -----------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔄 Regenerate Suggestions", use_container_width=True):
            with st.spinner("✨ Finding new ideas..."):
                new_result = generate_gifts(st.session_state.form_data)

            if new_result:
                st.session_state.results = new_result
                st.rerun()

    with col2:
        if st.button("❤️ Save Best Match", use_container_width=True):
            best = top.get("best_overall", "")

            if best and best not in st.session_state.favorites:
                st.session_state.favorites.append(best)
                st.success("Saved to favorites!")

    with col3:
        if st.button("🗑️ Reset", use_container_width=True):
            st.session_state.results = None
            st.session_state.form_data = {}
            st.rerun()

    # -----------------------------------------------------
    # GIFT CARDS
    # -----------------------------------------------------
    st.markdown(
        '<div class="section-title">🎁 Personalized Gift Recommendations</div>',
        unsafe_allow_html=True
    )

    gifts = result.get("gifts", [])

    if gifts:

        for index in range(0, len(gifts), 2):

            cols = st.columns(2)

            for col_index in range(2):

                gift_index = index + col_index

                if gift_index >= len(gifts):
                    continue

                gift = gifts[gift_index]

                is_best = (
                    gift.get("name", "").lower()
                    == top.get("best_overall", "").lower()
                )

                badge = (
                    '<div class="best-match">⭐ BEST MATCH</div>'
                    if is_best
                    else ""
                )

                with cols[col_index]:

                    st.markdown(
                        f"""
                        <div class="gift-card">

                            {badge}

                            <div class="gift-name">
                                {gift.get("name", "Gift")}
                            </div>

                            <div class="price">
                                💰 {gift.get("price_range", "Price unavailable")}
                            </div>

                            <div class="category">
                                {gift.get("category", "Gift")}
                            </div>

                            <div class="gift-label">
                                ✨ Why You'll Love It
                            </div>

                            <div class="gift-text">
                                {gift.get("why_perfect", "")}
                            </div>

                            <div class="gift-label">
                                🎯 Perfect For
                            </div>

                            <div class="gift-text">
                                {gift.get("occasion", "")}
                            </div>

                            <div class="gift-label">
                                🎨 Personalization Idea
                            </div>

                            <div class="gift-text">
                                {gift.get("personalization", "")}
                            </div>

                            <div class="gift-label">
                                💌 Gift Message
                            </div>

                            <div class="gift-text">
                                {gift.get("gift_message", "")}
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    copy_text = f"""
{gift.get('name', '')}

Price: {gift.get('price_range', '')}

Why You'll Love It:
{gift.get('why_perfect', '')}

Personalization:
{gift.get('personalization', '')}

Gift Message:
{gift.get('gift_message', '')}
"""

                    if st.button(
                        f"📋 Copy Recommendation #{gift_index + 1}",
                        key=f"copy_{gift_index}",
                        use_container_width=True
                    ):
                        st.code(copy_text)

                    if st.button(
                        f"❤️ Save Gift #{gift_index + 1}",
                        key=f"save_{gift_index}",
                        use_container_width=True
                    ):

                        gift_name = gift.get("name", "")

                        if gift_name not in st.session_state.favorites:
                            st.session_state.favorites.append(gift_name)
                            st.success("Gift saved to favorites!")

    # -----------------------------------------------------
    # GIFT COMPARISON
    # -----------------------------------------------------
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">⚖️ Gift Comparison</div>',
        unsafe_allow_html=True
    )

    comparison_data = []

    for gift in gifts:
        comparison_data.append({
            "Gift": gift.get("name", ""),
            "Price": gift.get("price_range", ""),
            "Uniqueness": gift.get("uniqueness", ""),
            "Practicality": gift.get("practicality", ""),
            "Emotional Value": gift.get("emotional_value", "")
        })

    if comparison_data:
        st.dataframe(
            comparison_data,
            use_container_width=True,
            hide_index=True
        )

    # -----------------------------------------------------
    # FAVORITES
    # -----------------------------------------------------
    if st.session_state.favorites:

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        st.markdown(
            '<div class="section-title">❤️ Saved Favorites</div>',
            unsafe_allow_html=True
        )

        for favorite in st.session_state.favorites:
            st.markdown(
                f"""
                <div class="info-card">
                    🎁 <strong>{favorite}</strong>
                </div>
                """,
                unsafe_allow_html=True
            )

# ---------------------------------------------------------
# EMPTY STATE
# ---------------------------------------------------------
else:

    st.markdown("""
    <div class="empty-state">

        <div class="emoji">🎁</div>

        <h3>Your perfect gift is waiting</h3>

        <p>
            Tell us about the recipient above and let AI discover
            thoughtful gift ideas tailored just for them.
        </p>

    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown(
    """
    <div class="small-note">
        Gift Finder AI • Personalized gift discovery powered by AI
    </div>
    """,
    unsafe_allow_html=True
)
