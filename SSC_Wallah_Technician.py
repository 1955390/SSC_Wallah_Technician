import streamlit as st
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import uuid

# ---------------------------- PAGE CONFIG ----------------------------
st.set_page_config(
    page_title="SSC Wallah Technician",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------- FIXED GMAIL CREDENTIALS ---------------
GMAIL_SENDER = "sscwallahtec966@gmail.com"
GMAIL_APP_PASSWORD = "byqasipohrtqjlvf"  # Password without spaces

# ---------------------------- CUSTOM STYLING ------------------------
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0033a0, #00a3e0);
        padding: 1.8rem 1rem;
        border-radius: 30px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 12px 25px rgba(0,51,160,0.25);
    }
    .main-header h1 {
        font-size: 3.2rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 3px 3px 0 #002080;
    }
    .total-box {
        background: linear-gradient(145deg, #ffffff, #f2f6fc);
        padding: 1.5rem;
        border-radius: 28px;
        border: 2px solid #0033a0;
        font-size: 1.6rem;
        font-weight: 800;
        text-align: center;
    }
    .stButton > button {
        background: #0033a0;
        color: white;
        font-weight: 600;
        padding: 0.75rem 2.5rem;
        border-radius: 60px;
        border: none;
        box-shadow: 0 8px 16px rgba(0,51,160,0.25);
        font-size: 1.2rem;
        width: 100%;
        transition: 0.2s;
    }
    .stButton > button:hover {
        background: #002080;
        transform: scale(1.02);
    }
    .footer {
        text-align: center;
        color: #6c757d;
        padding: 2rem 0 0 0;
        font-size: 0.95rem;
    }
    .price-box {
        background-color: #f0f7ff;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        border-left: 4px solid #0033a0;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------- SESSION STATE -------------------------
if 'booking_id' not in st.session_state:
    st.session_state.booking_id = str(uuid.uuid4())[:8].upper()
if 'technician_name' not in st.session_state:
    st.session_state.technician_name = "Prem (Senior Tech)"

# ---------------------------- HEADER ---------------------------------
st.markdown("""
<div class="main-header">
    <h1>❄️ SSC WALLAH TECHNICIAN</h1>
    <p>⚡ Lucknow • Full Area Coverage • 24x7 Emergency Service ⚡</p>
    <p style="font-size:1rem; margin-top:12px;">📞 8174083966  |  9532006520  |  📧 sscwallahtec966@gmail.com</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------- SIDEBAR -------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3145/3145762.png", width=80)
    st.markdown("## 👨‍🔧 Technician Panel")
    tech_name = st.text_input("Your name", value=st.session_state.technician_name)
    st.session_state.technician_name = tech_name

    now = datetime.now()
    current_date = now.strftime("%d %B %Y")
    current_day = now.strftime("%A")
    current_time = now.strftime("%I:%M %p")

    st.markdown(f"""
    <div style="background:#eef2f6; padding:1.2rem; border-radius:22px; margin:1rem 0;">
        <p style="margin:0; font-weight:600;">📅 {current_date}</p>
        <p style="margin:0; font-weight:500;">🗓️ {current_day}</p>
        <p style="margin:0; font-weight:500;">⏰ {current_time}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📋 Booking ID")
    st.code(st.session_state.booking_id)
    st.markdown("---")
    st.success("✅ Gmail: sscwallahtec966@gmail.com")

# ---------------------------- MAIN FORM -----------------------------
st.markdown("## 📋 New Service Booking")

col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.markdown("### 👤 Customer Details")
    c1, c2 = st.columns(2)
    with c1:
        cust_name = st.text_input("Full name *", placeholder="Abhay Kumar Ji", value="Abhay Kumar Ji")
        cust_phone = st.text_input("Phone *", placeholder="9101112233", value="9101112233")
    with c2:
        cust_email = st.text_input("Email *", placeholder="customer@example.com", value="customer@example.com")
        cust_location = st.text_input("Location *", placeholder="Chinhat Lucknow", value="Chinhat Lucknow")

    st.markdown("### 🛠️ Services with Editable Pricing")
    
    # AC Section
    st.markdown("#### ❄️ AC Service")
    col_a1, col_a2, col_a3 = st.columns([1, 1, 1])
    with col_a1:
        ac_type = st.radio("Type", ["Split AC", "Window AC"], horizontal=True, key="ac_type")
    with col_a2:
        ac_qty = st.number_input("Quantity", min_value=0, max_value=50, value=3, step=1, key="ac_qty")
    with col_a3:
        st.markdown("<br>", unsafe_allow_html=True)
        ac_price_edit = st.checkbox("Edit Price", key="ac_edit")
    
    if ac_price_edit:
        col_a_price1, col_a_price2 = st.columns(2)
        with col_a_price1:
            ac_base_price = st.number_input("Base Price (₹)", min_value=0, value=499 if ac_type == "Split AC" else 399, step=50, key="ac_base")
        with col_a_price2:
            ac_offer_price = st.number_input("Offer Price (2+ units) ₹", min_value=0, value=399 if ac_type == "Split AC" else 349, step=50, key="ac_offer")
    else:
        ac_base_price = 499 if ac_type == "Split AC" else 399
        ac_offer_price = 399 if ac_type == "Split AC" else 349
    
    # Calculate AC totals
    if ac_qty >= 2:
        ac_total = ac_qty * ac_offer_price
        ac_offer_applied = True
        ac_savings = (ac_qty * ac_base_price) - ac_total
        ac_price_display = ac_offer_price
        ac_price_text = f"Offer Price: ₹{ac_offer_price}"
    else:
        ac_total = ac_qty * ac_base_price
        ac_offer_applied = False
        ac_savings = 0
        ac_price_display = ac_base_price
        ac_price_text = f"Unit Price: ₹{ac_base_price}"
    
    st.caption(f"📌 {ac_price_text}")
    
    st.markdown("---")
    
    # Fridge Section
    st.markdown("#### 🧊 Fridge Service")
    col_f1, col_f2, col_f3 = st.columns([1, 1, 1])
    with col_f1:
        fridge_type = st.selectbox("Type", ["Direct Cool", "Frost Free", "Double Door"], key="fridge_type")
    with col_f2:
        fridge_qty = st.number_input("Quantity", min_value=0, max_value=50, value=0, step=1, key="fridge_qty")
    with col_f3:
        st.markdown("<br>", unsafe_allow_html=True)
        fridge_price_edit = st.checkbox("Edit Price", key="fridge_edit")
    
    default_fridge_prices = {"Direct Cool": 399, "Frost Free": 499, "Double Door": 599}
    
    if fridge_price_edit:
        fridge_price = st.number_input("Unit Price (₹)", min_value=0, value=default_fridge_prices[fridge_type], step=50, key="fridge_price")
    else:
        fridge_price = default_fridge_prices[fridge_type]
    
    fridge_total = fridge_qty * fridge_price
    st.caption(f"📌 Unit Price: ₹{fridge_price}")
    
    st.markdown("---")
    
    # Washing Machine Section
    st.markdown("#### 🧺 Washing Machine")
    col_w1, col_w2, col_w3 = st.columns([1, 1, 1])
    with col_w1:
        wm_type = st.selectbox("Type", ["Semi Auto", "Top Load", "Fully Auto"], key="wm_type")
    with col_w2:
        wm_qty = st.number_input("Quantity", min_value=0, max_value=50, value=0, step=1, key="wm_qty")
    with col_w3:
        st.markdown("<br>", unsafe_allow_html=True)
        wm_price_edit = st.checkbox("Edit Price", key="wm_edit")
    
    default_wm_prices = {"Semi Auto": 449, "Top Load": 549, "Fully Auto": 599}
    
    if wm_price_edit:
        wm_price = st.number_input("Unit Price (₹)", min_value=0, value=default_wm_prices[wm_type], step=50, key="wm_price")
    else:
        wm_price = default_wm_prices[wm_type]
    
    wm_total = wm_qty * wm_price
    st.caption(f"📌 Unit Price: ₹{wm_price}")
    
    st.markdown("---")
    
    # Additional Items
    st.markdown("#### ➕ Additional Items")
    
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.markdown("**Item 1**")
        extra_service_1 = st.text_input("Service name", key="extra_name1", placeholder="Gas Filling", value="Gas Filling")
        extra_qty_1 = st.number_input("Qty", min_value=0, value=0, step=1, key="extra_qty1")
        extra_price_1 = st.number_input("Unit Price (₹)", min_value=0, value=0, step=50, key="extra_price1")
        extra_total_1 = extra_qty_1 * extra_price_1
    
    with col_e2:
        st.markdown("**Item 2**")
        extra_service_2 = st.text_input("Service name", key="extra_name2", placeholder="Installation", value="Installation")
        extra_qty_2 = st.number_input("Qty", min_value=0, value=0, step=1, key="extra_qty2")
        extra_price_2 = st.number_input("Unit Price (₹)", min_value=0, value=0, step=50, key="extra_price2")
        extra_total_2 = extra_qty_2 * extra_price_2
    
    st.markdown("---")
    
    # Additional Services Description
    extra_services = st.text_area("📝 Additional Work Description", 
        value="📢 AC service ke saath complete system checking ki gayi, jisme Gas, Capacitor, Electrical Wiring, Coil aur Cooling Performance ko check kiya gaya. 💯",
        placeholder="Describe additional work done")
    
    # Quick Extra Charges
    extra_charges = st.number_input("Extra Charges (₹) - Quick Add", min_value=0, value=200, step=100)
    
    # Technician Remarks
    remarks = st.text_area("📝 Technician Remarks", 
        value="Customer ka behaviour bahut hi polite aur supportive tha 👍 Service dene me bahut achha experience raha. Thank you 🙏",
        placeholder="Call before visit, gate code, etc.")

# ---------------------------- RIGHT PANEL ---------------------------
with col_right:
    st.markdown("### 🧾 Bill Summary")
    with st.container():
        st.markdown(f"**ID:** `{st.session_state.booking_id}`")
        st.markdown(f"**Tech:** {st.session_state.technician_name}")
        st.markdown(f"**Date:** {current_date} {current_time}")
        st.markdown(f"**Customer:** {cust_name}")
        
        # Calculate grand total
        grand_total = ac_total + fridge_total + wm_total + extra_total_1 + extra_total_2 + extra_charges
        
        st.markdown("---")
        st.markdown("##### Services Breakdown:")
        
        has_services = False
        
        # AC Section
        if ac_qty > 0:
            has_services = True
            offer_text = " 🔥 OFFER APPLIED" if ac_offer_applied else ""
            st.markdown(f"❄️ **AC ({ac_type})**")
            st.markdown(f"   ×{ac_qty} @ ₹{ac_price_display} = ₹{ac_total:,}{offer_text}")
        
        # Fridge Section
        if fridge_qty > 0:
            has_services = True
            st.markdown(f"🧊 **Fridge ({fridge_type})**")
            st.markdown(f"   ×{fridge_qty} @ ₹{fridge_price} = ₹{fridge_total:,}")
        
        # WM Section
        if wm_qty > 0:
            has_services = True
            st.markdown(f"🧺 **WM ({wm_type})**")
            st.markdown(f"   ×{wm_qty} @ ₹{wm_price} = ₹{wm_total:,}")
        
        # Extra Items
        if extra_qty_1 > 0 and extra_service_1:
            has_services = True
            st.markdown(f"➕ **{extra_service_1}**")
            st.markdown(f"   ×{extra_qty_1} @ ₹{extra_price_1} = ₹{extra_total_1:,}")
        
        if extra_qty_2 > 0 and extra_service_2:
            has_services = True
            st.markdown(f"➕ **{extra_service_2}**")
            st.markdown(f"   ×{extra_qty_2} @ ₹{extra_price_2} = ₹{extra_total_2:,}")
        
        if extra_charges > 0:
            has_services = True
            st.markdown(f"➕ **Extra Charges:** ₹{extra_charges:,}")
        
        st.markdown("---")
        
        # Show savings if any
        if ac_offer_applied and ac_savings > 0:
            st.success(f"🎉 You saved ₹{ac_savings:,} on AC service!")
        
        # Grand Total
        if not has_services and extra_charges == 0:
            st.warning("⚠️ No services added. Bill amount is zero.")
            grand_total = 0
        
        st.markdown(f"<div class='total-box'>💰 GRAND TOTAL: ₹{grand_total:,}</div>", unsafe_allow_html=True)

    # ------------------------ SMS PREVIEW ---------------------------
    st.markdown("### 📱 SMS Preview")
    
    if cust_name and grand_total > 0:
        # Build SMS with all details
        sms_content = f"""Dear {cust_name},
Thank you for choosing SSC Wallah Technician.
Here is your service estimate:


═══════════════════════════════════════════
📋 BOOKING DETAILS
═══════════════════════════════════════════
Booking ID:     {st.session_state.booking_id}
Date & Time:    {current_date} at {current_time}
Location:       {cust_location}
Technician:     {st.session_state.technician_name}
Contact:        {cust_phone}


═══════════════════════════════════════════
🛠️ SERVICES
═══════════════════════════════════════════
"""
        if ac_qty > 0:
            if ac_offer_applied:
                sms_content += f"❄️ AC ({ac_type}) x{ac_qty} @ ₹{ac_offer_price} = ₹{ac_total:,} (Offer)\n"
            else:
                sms_content += f"❄️ AC ({ac_type}) x{ac_qty} @ ₹{ac_base_price} = ₹{ac_total:,}\n"
        
        if fridge_qty > 0:
            sms_content += f"🧊 Fridge ({fridge_type}) x{fridge_qty} @ ₹{fridge_price} = ₹{fridge_total:,}\n"
        
        if wm_qty > 0:
            sms_content += f"🧺 WM ({wm_type}) x{wm_qty} @ ₹{wm_price} = ₹{wm_total:,}\n"
        
        if extra_qty_1 > 0 and extra_service_1:
            sms_content += f"➕ {extra_service_1} x{extra_qty_1} @ ₹{extra_price_1} = ₹{extra_total_1:,}\n"
        
        if extra_qty_2 > 0 and extra_service_2:
            sms_content += f"➕ {extra_service_2} x{extra_qty_2} @ ₹{extra_price_2} = ₹{extra_total_2:,}\n"
        
        if extra_charges > 0:
            sms_content += f"➕ Extra Charges: ₹{extra_charges:,}\n"
        
        if extra_services:
            sms_content += f"\n📌 Note: {extra_services}\n"
            
        if ac_offer_applied:
            sms_content += f"""
═══════════════════════════════════════════
🎉 SPECIAL OFFER APPLIED!
You saved ₹{ac_savings:,} on AC service!
═══════════════════════════════════════════
"""
            
        sms_content += f"""
═══════════════════════════════════════════
💰 TOTAL: ₹{grand_total:,}
═══════════════════════════════════════════


{remarks}


📞 8174083966 / 9532006520
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SSC Wallah Technician
Lucknow • 24x7 Service
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
        
        st.code(sms_content, language="text")
    else:
        if grand_total == 0:
            st.info("Add services to see SMS preview")
        else:
            st.info("Enter customer details to see SMS preview")

# ---------------------------- SEND EMAIL & SMS ----------------------
st.markdown("---")
st.markdown("## 📤 Send to Customer")

col_s1, col_s2, col_s3 = st.columns(3)

def send_customer_email():
    """Send email to customer"""
    try:
        # Build email content
        email_content = f"""Dear {cust_name},
Thank you for choosing SSC Wallah Technician.
Here is your service estimate:


═══════════════════════════════════════════
📋 BOOKING DETAILS
═══════════════════════════════════════════
Booking ID:     {st.session_state.booking_id}
Date & Time:    {current_date} at {current_time}
Location:       {cust_location}
Technician:     {st.session_state.technician_name}
Contact:        {cust_phone}


═══════════════════════════════════════════
🛠️ SERVICES
═══════════════════════════════════════════
"""
        if ac_qty > 0:
            if ac_offer_applied:
                email_content += f"❄️ AC ({ac_type}) x{ac_qty} @ ₹{ac_offer_price} = ₹{ac_total:,} (Offer Applied)\n"
            else:
                email_content += f"❄️ AC ({ac_type}) x{ac_qty} @ ₹{ac_base_price} = ₹{ac_total:,}\n"
        
        if fridge_qty > 0:
            email_content += f"🧊 Fridge ({fridge_type}) x{fridge_qty} @ ₹{fridge_price} = ₹{fridge_total:,}\n"
        
        if wm_qty > 0:
            email_content += f"🧺 WM ({wm_type}) x{wm_qty} @ ₹{wm_price} = ₹{wm_total:,}\n"
        
        if extra_qty_1 > 0 and extra_service_1:
            email_content += f"➕ {extra_service_1} x{extra_qty_1} @ ₹{extra_price_1} = ₹{extra_total_1:,}\n"
        
        if extra_qty_2 > 0 and extra_service_2:
            email_content += f"➕ {extra_service_2} x{extra_qty_2} @ ₹{extra_price_2} = ₹{extra_total_2:,}\n"
        
        if extra_charges > 0:
            email_content += f"➕ Extra Charges: ₹{extra_charges:,}\n"
        
        if extra_services:
            email_content += f"\n📌 Additional Work: {extra_services}\n"
            
        if ac_offer_applied:
            email_content += f"""
═══════════════════════════════════════════
🎉 SPECIAL OFFER APPLIED!
You saved ₹{ac_savings:,} on AC service!
═══════════════════════════════════════════
"""
            
        email_content += f"""
═══════════════════════════════════════════
💰 TOTAL AMOUNT: ₹{grand_total:,}
═══════════════════════════════════════════


Technician Notes:
{remarks}


Our team will contact you shortly.
For immediate assistance:
📞 8174083966 or 9532006520
📧 sscwallahtec966@gmail.com


Thank you for trusting SSC Wallah Technician!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SSC Wallah Team
Lucknow • Full Area Service • 24x7 Support
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

        # Create email
        msg = MIMEText(email_content, 'plain', 'utf-8')
        msg['From'] = GMAIL_SENDER
        msg['To'] = cust_email
        msg['Reply-To'] = GMAIL_SENDER
        msg['Subject'] = f"Service Estimate | {cust_name} | {st.session_state.booking_id}"
        
        # Send
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login(GMAIL_SENDER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
            
            # Send self copy
            self_msg = MIMEText(f"TECHNICIAN COPY - Sent to {cust_email}\n\n{email_content}", 'plain', 'utf-8')
            self_msg['From'] = GMAIL_SENDER
            self_msg['To'] = GMAIL_SENDER
            self_msg['Subject'] = f"[COPY] {cust_name} - {st.session_state.booking_id}"
            server.send_message(self_msg)
            
        return True, "Email sent"
    except Exception as e:
        return False, str(e)

def send_customer_sms():
    """Send SMS to customer (demo)"""
    try:
        # Build SMS
        sms_content = f"""Dear {cust_name},
Thank you for choosing SSC Wallah Technician.
Here is your service estimate:


═══════════════════════════════════════════
📋 BOOKING DETAILS
═══════════════════════════════════════════
Booking ID:     {st.session_state.booking_id}
Date & Time:    {current_date} at {current_time}
Location:       {cust_location}
Technician:     {st.session_state.technician_name}
Contact:        {cust_phone}


═══════════════════════════════════════════
🛠️ SERVICES
═══════════════════════════════════════════
"""
        if ac_qty > 0:
            if ac_offer_applied:
                sms_content += f"❄️ AC ({ac_type}) x{ac_qty} @ ₹{ac_offer_price} = ₹{ac_total:,}\n"
            else:
                sms_content += f"❄️ AC ({ac_type}) x{ac_qty} @ ₹{ac_base_price} = ₹{ac_total:,}\n"
        
        if fridge_qty > 0:
            sms_content += f"🧊 Fridge ({fridge_type}) x{fridge_qty} @ ₹{fridge_price} = ₹{fridge_total:,}\n"
        
        if wm_qty > 0:
            sms_content += f"🧺 WM ({wm_type}) x{wm_qty} @ ₹{wm_price} = ₹{wm_total:,}\n"
        
        if extra_qty_1 > 0 and extra_service_1:
            sms_content += f"➕ {extra_service_1} x{extra_qty_1} @ ₹{extra_price_1} = ₹{extra_total_1:,}\n"
        
        if extra_qty_2 > 0 and extra_service_2:
            sms_content += f"➕ {extra_service_2} x{extra_qty_2} @ ₹{extra_price_2} = ₹{extra_total_2:,}\n"
        
        if extra_charges > 0:
            sms_content += f"➕ Extra: ₹{extra_charges:,}\n"
            
        if ac_offer_applied:
            sms_content += f"""
═══════════════════════════════════════════
🎉 OFFER APPLIED! Saved ₹{ac_savings:,}
═══════════════════════════════════════════
"""
            
        sms_content += f"""
═══════════════════════════════════════════
💰 TOTAL: ₹{grand_total:,}
═══════════════════════════════════════════


📞 8174083966 / 9532006520
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SSC Wallah Technician"""
        
        # Demo mode - just show success
        st.info(f"📱 SMS ready for {cust_phone}")
        return True, "SMS demo mode"
    except Exception as e:
        return False, str(e)

with col_s1:
    if st.button("📧 Send Email Only", key="email_only"):
        if not all([cust_name, cust_email, cust_location]):
            st.error("❌ Please fill all customer details")
        elif grand_total == 0:
            st.warning("⚠️ Bill amount is zero. Add some services.")
        else:
            with st.spinner("Sending email..."):
                success, msg = send_customer_email()
                if success:
                    st.success(f"✅ Email sent to {cust_email}")
                    st.success("✅ Copy saved to technician inbox")
                else:
                    st.error(f"❌ Failed: {msg}")

with col_s2:
    if st.button("📱 Send SMS Only", key="sms_only"):
        if not cust_phone:
            st.error("❌ Customer phone number required")
        elif grand_total == 0:
            st.warning("⚠️ Bill amount is zero. Add some services.")
        else:
            with st.spinner("Preparing SMS..."):
                success, msg = send_customer_sms()
                if success:
                    st.success(f"✅ SMS ready for {cust_phone}")

with col_s3:
    if st.button("📧📱 Send Both", key="both"):
        if not all([cust_name, cust_email, cust_location, cust_phone]):
            st.error("❌ Please fill all customer details")
        elif grand_total == 0:
            st.warning("⚠️ Bill amount is zero. Add some services.")
        else:
            with st.spinner("Sending..."):
                e_success, e_msg = send_customer_email()
                s_success, s_msg = send_customer_sms()
                
                if e_success:
                    st.success(f"✅ Email to {cust_email}")
                if s_success:
                    st.success(f"✅ SMS to {cust_phone}")
                if e_success and s_success:
                    st.balloons()

# ---------------------------- FOOTER --------------------------------
st.markdown("---")
st.markdown("""
<div class="footer">
    ⚡ All prices editable • Real-time calculation • Zero bill handling ⚡<br>
    ⚡ 2+ AC Jet Service @ Special Offer automatically applied ⚡<br>
    © SSC Wallah Technician — 8174083966 / 9532006520 — sscwallahtec966@gmail.com
</div>
""", unsafe_allow_html=True)
