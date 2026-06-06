import json
import random
import string
import streamlit as st
from pathlib import Path

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NovaPay Bank",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Root Variables ── */
:root {
    --bg:        #0b0f1a;
    --surface:   #111827;
    --card:      #16202e;
    --border:    #1f2f42;
    --accent:    #00e5a0;
    --accent2:   #0ab8ff;
    --danger:    #ff4d6d;
    --warning:   #ffb703;
    --text:      #e8edf5;
    --muted:     #6b7a90;
    --radius:    14px;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Streamlit chrome ── */
.stApp { background: var(--bg) !important; }
header[data-testid="stHeader"] { background: transparent !important; }
.stSidebar { background: var(--surface) !important; }
[data-testid="stToolbar"] { display: none; }

/* ── Bank Header ── */
.bank-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
}
.bank-header .logo {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.6rem;
    letter-spacing: -1px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    display: inline-block;
}
.bank-header .tagline {
    font-size: 0.85rem;
    color: var(--muted);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ── Section title ── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.35rem;
    color: var(--text);
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-title span.pill {
    background: linear-gradient(135deg, #00e5a020, #0ab8ff20);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 2px 12px;
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--accent2);
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ── Cards ── */
.stat-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}
.stat-card .label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--muted);
    margin-bottom: 6px;
}
.stat-card .value {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--accent);
}
.stat-card .value.neutral { color: var(--text); }

/* ── User detail card ── */
.user-card {
    background: linear-gradient(135deg, #00e5a012, #0ab8ff0a);
    border: 1px solid #00e5a030;
    border-radius: var(--radius);
    padding: 1.5rem 1.8rem;
    margin-bottom: 1rem;
}
.user-card .user-name {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
}
.user-card .user-acc {
    font-size: 0.78rem;
    color: var(--muted);
    font-family: monospace;
    letter-spacing: 1.5px;
}
.user-card .balance-row {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #ffffff10;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.user-card .balance-amount {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--accent);
}

/* ── Info grid ── */
.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.7rem;
    margin-top: 0.8rem;
}
.info-item { display: flex; flex-direction: column; gap: 2px; }
.info-item .i-label { font-size: 0.72rem; color: var(--muted); text-transform: uppercase; letter-spacing: 1.5px; }
.info-item .i-value { font-size: 0.95rem; font-weight: 500; }

/* ── Divider ── */
.gradient-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 1.8rem 0;
}

/* ── Alerts ── */
.alert { border-radius: 10px; padding: 0.9rem 1.2rem; margin: 0.8rem 0; font-size: 0.9rem; display: flex; align-items: center; gap: 10px; }
.alert-success { background: #00e5a015; border: 1px solid #00e5a040; color: #00e5a0; }
.alert-error   { background: #ff4d6d15; border: 1px solid #ff4d6d40; color: #ff4d6d; }
.alert-info    { background: #0ab8ff15; border: 1px solid #0ab8ff40; color: #0ab8ff; }

/* ── Inputs override ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background: #0d1421 !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px #00e5a020 !important;
}
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label {
    color: var(--muted) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #0b0f1a !important;
    border: none !important;
    border-radius: 9px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.5px !important;
    padding: 0.55rem 1.4rem !important;
    transition: opacity 0.2s, transform 0.15s !important;
    width: 100% !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
button[kind="secondary"] {
    background: var(--card) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
}

/* ── Radio / Select ── */
[data-testid="stRadio"] label { color: var(--text) !important; }
[data-testid="stSelectbox"] { background: var(--card) !important; }
div[data-baseweb="select"] > div {
    background: #0d1421 !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}

/* ── Danger button ── */
.danger-btn > button {
    background: linear-gradient(135deg, var(--danger), #c9184a) !important;
    color: white !important;
}

/* ── Nav tabs ── */
[data-testid="stHorizontalBlock"] { gap: 0.5rem; }

/* ── Footer ── */
.bank-footer {
    text-align: center;
    padding: 2rem 0 1rem;
    color: var(--muted);
    font-size: 0.75rem;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)


# ─── Backend Logic ───────────────────────────────────────────────────────────────
DATABASE = "novapay_database.json"


def load_data():
    if Path(DATABASE).exists():
        with open(DATABASE) as f:
            return json.loads(f.read())
    return []


def save_data(data):
    with open(DATABASE, "w") as f:
        f.write(json.dumps(data, indent=2))


def generate_account_no():
    alpha = random.choices(string.ascii_uppercase, k=6)
    num = random.choices(string.digits, k=4)
    acc = alpha + num
    random.shuffle(acc)
    return "NP-" + "".join(acc)


def find_user(data, accno, pin):
    matches = [u for u in data if u["AccountNo"] == accno and u["pin"] == pin]
    return matches[0] if matches else None


# ─── Session state init ──────────────────────────────────────────────────────────
if "message" not in st.session_state:
    st.session_state.message = None  # {"type": "success"|"error"|"info", "text": "..."}
if "tab" not in st.session_state:
    st.session_state.tab = "Create Account"


# ─── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="bank-header">
    <div class="logo">🏦 NovaPay</div>
    <div class="tagline">Digital Banking · Secure · Simple</div>
</div>
""", unsafe_allow_html=True)

# ─── Navigation ─────────────────────────────────────────────────────────────────
TABS = ["Create Account", "Deposit", "Withdraw", "Account Details", "Update Details", "Delete Account"]
ICONS = ["✦", "＋", "−", "◎", "✎", "✕"]

selected = st.selectbox(
    "Navigate",
    options=TABS,
    format_func=lambda x: f"{ICONS[TABS.index(x)]}  {x}",
    label_visibility="collapsed",
)

st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)


# ─── Message Banner ──────────────────────────────────────────────────────────────
def show_message():
    msg = st.session_state.message
    if msg:
        cls = f"alert-{msg['type']}"
        icons = {"success": "✓", "error": "✕", "info": "ℹ"}
        icon = icons.get(msg["type"], "")
        st.markdown(
            f'<div class="alert {cls}"><span>{icon}</span><span>{msg["text"]}</span></div>',
            unsafe_allow_html=True,
        )
        st.session_state.message = None


show_message()
data = load_data()


# ════════════════════════════════════════════════════════════════════════════════
# 1. CREATE ACCOUNT
# ════════════════════════════════════════════════════════════════════════════════
if selected == "Create Account":
    st.markdown('<div class="section-title">New Account <span class="pill">Registration</span></div>', unsafe_allow_html=True)

    with st.form("create_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", placeholder="e.g. Riya Sharma")
            email = st.text_input("Email Address", placeholder="riya@email.com")
        with col2:
            age = st.number_input("Age", min_value=1, max_value=120, value=18, step=1)
            pin = st.text_input("4-Digit PIN", placeholder="••••", max_chars=4, type="password")

        submitted = st.form_submit_button("Open Account →")

    if submitted:
        if not name or not email or not pin:
            st.session_state.message = {"type": "error", "text": "Please fill in all fields."}
        elif age < 12:
            st.session_state.message = {"type": "error", "text": "Minimum age to open an account is 12 years."}
        elif not pin.isdigit() or len(pin) != 4:
            st.session_state.message = {"type": "error", "text": "PIN must be exactly 4 digits."}
        else:
            acc_no = generate_account_no()
            new_user = {
                "name": name.strip(),
                "age": int(age),
                "email": email.strip().lower(),
                "AccountNo": acc_no,
                "pin": int(pin),
                "balance": 0,
            }
            data.append(new_user)
            save_data(data)

            st.markdown(f"""
            <div class="user-card">
                <div class="user-name">Welcome, {name}! 🎉</div>
                <div class="user-acc">{acc_no}</div>
                <div class="balance-row">
                    <span style="color:var(--muted); font-size:0.82rem;">OPENING BALANCE</span>
                    <span class="balance-amount">₹ 0.00</span>
                </div>
            </div>
            <div class="alert alert-success">✓ &nbsp; Account created successfully. Save your Account Number!</div>
            """, unsafe_allow_html=True)

        st.rerun() if st.session_state.message else None


# ════════════════════════════════════════════════════════════════════════════════
# 2. DEPOSIT
# ════════════════════════════════════════════════════════════════════════════════
elif selected == "Deposit":
    st.markdown('<div class="section-title">Deposit Money <span class="pill">Add Funds</span></div>', unsafe_allow_html=True)

    with st.form("deposit_form", clear_on_submit=False):
        accno = st.text_input("Account Number", placeholder="NP-XXXXXXXX")
        pin   = st.text_input("PIN", placeholder="••••", max_chars=4, type="password")
        amount = st.number_input("Amount (₹)", min_value=1, step=100, value=500)
        submitted = st.form_submit_button("Deposit →")

    if submitted:
        if not accno or not pin:
            st.session_state.message = {"type": "error", "text": "Account number and PIN are required."}
            st.rerun()
        else:
            user = find_user(data, accno.strip().upper(), int(pin))
            if not user:
                st.session_state.message = {"type": "error", "text": "Invalid account number or PIN."}
                st.rerun()
            else:
                user["balance"] += int(amount)
                save_data(data)
                st.markdown(f"""
                <div class="user-card">
                    <div class="user-name">{user['name']}</div>
                    <div class="user-acc">{user['AccountNo']}</div>
                    <div class="balance-row">
                        <span style="color:var(--muted); font-size:0.82rem;">UPDATED BALANCE</span>
                        <span class="balance-amount">₹ {user['balance']:,.2f}</span>
                    </div>
                </div>
                <div class="alert alert-success">✓ &nbsp; ₹{amount:,} deposited successfully.</div>
                """, unsafe_allow_html=True)
        show_message()


# ════════════════════════════════════════════════════════════════════════════════
# 3. WITHDRAW
# ════════════════════════════════════════════════════════════════════════════════
elif selected == "Withdraw":
    st.markdown('<div class="section-title">Withdraw Money <span class="pill">Cash Out</span></div>', unsafe_allow_html=True)

    with st.form("withdraw_form", clear_on_submit=False):
        accno  = st.text_input("Account Number", placeholder="NP-XXXXXXXX")
        pin    = st.text_input("PIN", placeholder="••••", max_chars=4, type="password")
        amount = st.number_input("Amount (₹)", min_value=1, step=100, value=500)
        submitted = st.form_submit_button("Withdraw →")

    if submitted:
        if not accno or not pin:
            st.session_state.message = {"type": "error", "text": "Account number and PIN are required."}
            st.rerun()
        else:
            user = find_user(data, accno.strip().upper(), int(pin))
            if not user:
                st.session_state.message = {"type": "error", "text": "Invalid account number or PIN."}
                st.rerun()
            elif int(amount) > user["balance"]:
                st.session_state.message = {
                    "type": "error",
                    "text": f"Insufficient balance. Available: ₹{user['balance']:,.2f}"
                }
                st.rerun()
            else:
                user["balance"] -= int(amount)
                save_data(data)
                st.markdown(f"""
                <div class="user-card">
                    <div class="user-name">{user['name']}</div>
                    <div class="user-acc">{user['AccountNo']}</div>
                    <div class="balance-row">
                        <span style="color:var(--muted); font-size:0.82rem;">REMAINING BALANCE</span>
                        <span class="balance-amount">₹ {user['balance']:,.2f}</span>
                    </div>
                </div>
                <div class="alert alert-success">✓ &nbsp; ₹{amount:,} withdrawn successfully.</div>
                """, unsafe_allow_html=True)
        show_message()


# ════════════════════════════════════════════════════════════════════════════════
# 4. ACCOUNT DETAILS
# ════════════════════════════════════════════════════════════════════════════════
elif selected == "Account Details":
    st.markdown('<div class="section-title">Account Details <span class="pill">Overview</span></div>', unsafe_allow_html=True)

    with st.form("details_form", clear_on_submit=False):
        accno = st.text_input("Account Number", placeholder="NP-XXXXXXXX")
        pin   = st.text_input("PIN", placeholder="••••", max_chars=4, type="password")
        submitted = st.form_submit_button("View Details →")

    if submitted:
        if not accno or not pin:
            st.session_state.message = {"type": "error", "text": "Both fields are required."}
            st.rerun()
        else:
            user = find_user(data, accno.strip().upper(), int(pin))
            if not user:
                st.session_state.message = {"type": "error", "text": "Invalid account number or PIN."}
                st.rerun()
            else:
                st.markdown(f"""
                <div class="user-card">
                    <div class="user-name">{user['name']}</div>
                    <div class="user-acc">{user['AccountNo']}</div>
                    <div class="info-grid">
                        <div class="info-item">
                            <span class="i-label">Email</span>
                            <span class="i-value">{user['email']}</span>
                        </div>
                        <div class="info-item">
                            <span class="i-label">Age</span>
                            <span class="i-value">{user['age']} years</span>
                        </div>
                    </div>
                    <div class="balance-row">
                        <span style="color:var(--muted); font-size:0.82rem;">AVAILABLE BALANCE</span>
                        <span class="balance-amount">₹ {user['balance']:,.2f}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        show_message()


# ════════════════════════════════════════════════════════════════════════════════
# 5. UPDATE DETAILS
# ════════════════════════════════════════════════════════════════════════════════
elif selected == "Update Details":
    st.markdown('<div class="section-title">Update Details <span class="pill">Edit Info</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="alert alert-info">ℹ &nbsp; Account number, age, and balance cannot be changed.</div>', unsafe_allow_html=True)

    with st.form("update_form", clear_on_submit=False):
        accno = st.text_input("Account Number", placeholder="NP-XXXXXXXX")
        pin   = st.text_input("Current PIN", placeholder="••••", max_chars=4, type="password")
        st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
        new_name  = st.text_input("New Name (leave blank to keep)", placeholder="e.g. Riya Sharma")
        new_email = st.text_input("New Email (leave blank to keep)", placeholder="riya@email.com")
        new_pin   = st.text_input("New PIN (leave blank to keep)", placeholder="••••", max_chars=4, type="password")
        submitted = st.form_submit_button("Save Changes →")

    if submitted:
        if not accno or not pin:
            st.session_state.message = {"type": "error", "text": "Account number and current PIN are required."}
            st.rerun()
        else:
            user = find_user(data, accno.strip().upper(), int(pin))
            if not user:
                st.session_state.message = {"type": "error", "text": "Invalid account number or PIN."}
                st.rerun()
            else:
                if new_name.strip():
                    user["name"] = new_name.strip()
                if new_email.strip():
                    user["email"] = new_email.strip().lower()
                if new_pin.strip():
                    if not new_pin.isdigit() or len(new_pin) != 4:
                        st.session_state.message = {"type": "error", "text": "New PIN must be exactly 4 digits."}
                        st.rerun()
                    else:
                        user["pin"] = int(new_pin)
                save_data(data)
                st.session_state.message = {"type": "success", "text": "Account details updated successfully."}
                st.rerun()
        show_message()


# ════════════════════════════════════════════════════════════════════════════════
# 6. DELETE ACCOUNT
# ════════════════════════════════════════════════════════════════════════════════
elif selected == "Delete Account":
    st.markdown('<div class="section-title">Delete Account <span class="pill">Danger Zone</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="alert alert-error">✕ &nbsp; This action is permanent and cannot be undone.</div>', unsafe_allow_html=True)

    with st.form("delete_form", clear_on_submit=True):
        accno = st.text_input("Account Number", placeholder="NP-XXXXXXXX")
        pin   = st.text_input("PIN", placeholder="••••", max_chars=4, type="password")
        confirm = st.checkbox("I understand this will permanently delete my account and all data.")
        st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
        submitted = st.form_submit_button("Delete Account")
        st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        if not accno or not pin:
            st.session_state.message = {"type": "error", "text": "Account number and PIN are required."}
            st.rerun()
        elif not confirm:
            st.session_state.message = {"type": "error", "text": "Please confirm you understand the consequences."}
            st.rerun()
        else:
            user = find_user(data, accno.strip().upper(), int(pin))
            if not user:
                st.session_state.message = {"type": "error", "text": "Invalid account number or PIN."}
                st.rerun()
            else:
                name_backup = user["name"]
                data.remove(user)
                save_data(data)
                st.session_state.message = {
                    "type": "info",
                    "text": f"Account for {name_backup} has been permanently deleted."
                }
                st.rerun()
        show_message()


# ─── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="gradient-divider"></div>
<div class="bank-footer">
    dimond Digital Banking &nbsp;·&nbsp; Secured &amp; Encrypted &nbsp;·&nbsp; © 2025
</div>
""", unsafe_allow_html=True)