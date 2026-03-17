import streamlit as st
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import re
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
        cust_name = st.text_input("Full name *", placeholder="Abhay Kumar Ji")
        cust_phone = st.text_input("Phone *", placeholder="9101112233")
    with c2:
        cust_email = st.text_input("Email *", placeholder="customer@example.com")
        cust_location = st.text_input("Location *", placeholder="Chinhat Lucknow Kanpur")

    st.markdown("### 🛠️ Services with Pricing")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.markdown("#### ❄️ AC")
        ac_type = st.radio("Type", ["Split AC", "Window AC"], horizontal=True, key="ac_type")
        ac_price = 499 if ac_type == "Split AC" else 399
        ac_offer_price = 399 if ac_type == "Split AC" else 349
        ac_qty = st.number_input("Qty", 0, 10, 3, key="ac_qty")
        
        # Calculate AC total with offer logic
        if ac_qty >= 2:
            ac_total = ac_qty * ac_offer_price
            ac_offer_applied = True
            ac_savings = (ac_qty * ac_price) - ac_total
        else:
            ac_total = ac_qty * ac_price
            ac_offer_applied = False
            ac_savings = 0
            
        st.caption(f"₹{ac_price}/unit | Offer: ₹{ac_offer_price}/unit (2+)")

    with col_b:
        st.markdown("#### 🧊 Fridge")
        fridge_type = st.selectbox("Type", ["Direct Cool", "Frost Free", "Double Door"], key="fridge_type")
        fridge_price = {"Direct Cool": 399, "Frost Free": 499, "Double Door": 599}[fridge_type]
        fridge_qty = st.number_input("Qty", 0, 10, 0, key="fridge_qty")
        fridge_total = fridge_qty * fridge_price
        st.caption(f"₹{fridge_price}/unit")

    with col_c:
        st.markdown("#### 🧺 WM")
        wm_type = st.selectbox("Type", ["Semi Auto", "Top Load", "Fully Auto"], key="wm_type")
        wm_price = {"Semi Auto": 449, "Top Load": 549, "Fully Auto": 599}[wm_type]
        wm_qty = st.number_input("Qty", 0, 10, 0, key="wm_qty")
        wm_total = wm_qty * wm_price
        st.caption(f"₹{wm_price}/unit")

    extra_services = st.text_area("➕ Additional Services", 
        value="📢 AC service ke saath complete system checking ki gayi, jisme Gas, Capacitor, Electrical Wiring, Coil aur Cooling Performance ko thoroughly check kiya gaya. 💯",
        placeholder="Gas filling - ₹500, Installation - ₹300, AMC - ₹1999 etc.")
    extra_charges = st.number_input("Extra charges (₹)", min_value=0, value=200, step=100)
    remarks = st.text_area("📝 Remarks/Instructions", 
        value="Customer ka behaviour bahut hi polite aur supportive tha 👍 Service dene me bahut achha experience raha. Thank you 🙏",
        placeholder="Call before visit, gate code, etc.")

# ---------------------------- RIGHT PANEL ---------------------------
with col_right:
    st.markdown("### 🧾 Summary")
    with st.container():
        st.markdown(f"**ID:** `{st.session_state.booking_id}`")
        st.markdown(f"**Tech:** {st.session_state.technician_name}")
        st.markdown(f"**Date:** {current_date} {current_time}")
        
        total_qty = ac_qty + fridge_qty + wm_qty
        if total_qty == 0:
            st.warning("No services selected")
        else:
            st.markdown("---")
            if ac_qty > 0:
                offer_text = " (Offer Applied)" if ac_offer_applied else ""
                st.markdown(f"❄️ AC ({ac_type}) x{ac_qty} = ₹{ac_total}{offer_text}")
            if fridge_qty > 0:
                st.markdown(f"🧊 Fridge ({fridge_type}) x{fridge_qty} = ₹{fridge_total}")
            if wm_qty > 0:
                st.markdown(f"🧺 WM ({wm_type}) x{wm_qty} = ₹{wm_total}")
            if extra_charges > 0:
                st.markdown(f"➕ Extra charges = ₹{extra_charges}")
            
            grand_total = ac_total + fridge_total + wm_total + extra_charges
            st.markdown(f"<div class='total-box'>💰 ₹{grand_total}</div>", unsafe_allow_html=True)

    # ------------------------ EXACT SMS PREVIEW (As Requested) -----
    st.markdown("### 📱 SMS Preview (Exact Format)")
    
    if cust_name:
        # Build SMS exactly as shown in example
        sms_content = f"""Dear {cust_name},
Thank you for choosing SSC Wallah Technician for your appliance service needs.
Here is your confirmed service estimate:


═══════════════════════════════════════════
📋 BOOKING DETAILS
═══════════════════════════════════════════
Booking ID:     {st.session_state.booking_id}
Date & Time:    {current_date} at {current_time}
Location:       {cust_location}
Technician:     {st.session_state.technician_name}
Contact:        {cust_phone}


═══════════════════════════════════════════
🛠️ SERVICES REQUESTED
═══════════════════════════════════════════
"""
        if ac_qty > 0:
            if ac_offer_applied:
                sms_content += f"❄️ AC Service ({ac_type}) x{ac_qty} (Special Offer Applied congrats - ₹{ac_offer_price}/AC) = ₹{ac_total}\n"
            else:
                sms_content += f"❄️ AC Service ({ac_type}) x{ac_qty} (₹{ac_price}/AC) = ₹{ac_total}\n"
        
        if fridge_qty > 0:
            sms_content += f"🧊 Fridge Service ({fridge_type}) x{fridge_qty} (₹{fridge_price}/unit) = ₹{fridge_total}\n"
        
        if wm_qty > 0:
            sms_content += f"🧺 Washing Machine ({wm_type}) x{wm_qty} (₹{wm_price}/unit) = ₹{wm_total}\n"
        
        if extra_services:
            sms_content += f"\n📌 Additional Services: {extra_services}\n"
        if extra_charges > 0:
            sms_content += f"➕ Extra Charges: ₹{extra_charges}\n"
            
        if ac_offer_applied:
            sms_content += f"""
═══════════════════════════════════════════
🎉 SPECIAL OFFER APPLIED CONGRATULATIONS!
You saved ₹{ac_savings} on AC service!
═══════════════════════════════════════════
"""
            
        sms_content += f"""
═══════════════════════════════════════════
💰 TOTAL AMOUNT: ₹{grand_total}
═══════════════════════════════════════════


TECHNICIAN REMARKS:
{remarks}


Our service team will contact you within 30 minutes to schedule the visit.
We provide 100% guarantee on all repairs with genuine spare parts.


For immediate assistance:
📞 Call/WhatsApp: 8174083966 or 9532006520
📧 Email: sscwallahtec966@gmail.com


Thank you for trusting SSC Wallah Technician!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SSC Wallah Technician Team
Lucknow • Full Area Service • 24x7 Support
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
        
        # Show the exact SMS that will be sent
        st.code(sms_content, language="text")
    else:
        st.info("Enter customer details to see SMS preview")

# ---------------------------- SEND EMAIL & SMS ----------------------
st.markdown("---")
st.markdown("## 📤 Send to Customer")

col_s1, col_s2, col_s3 = st.columns(3)

def send_customer_email():
    """Send email to customer"""
    try:
        # Plain text email - exactly like SMS format
        email_content = f"""Dear {cust_name},
Thank you for choosing SSC Wallah Technician for your appliance service needs.
Here is your confirmed service estimate:


═══════════════════════════════════════════
📋 BOOKING DETAILS
═══════════════════════════════════════════
Booking ID:     {st.session_state.booking_id}

Date & Time:    {current_date} at {current_time}

Location:       {cust_location}

Technician:     {st.session_state.technician_name}

Contact:        {cust_phone}


═══════════════════════════════════════════
🛠️ SERVICES REQUESTED
═══════════════════════════════════════════
"""
        if ac_qty > 0:
            if ac_offer_applied:
                email_content += f"❄️ AC Service ({ac_type}) x{ac_qty} (Special Offer ₹{ac_offer_price}/AC) = ₹{ac_total}\n"
            else:
                email_content += f"❄️ AC Service ({ac_type}) x{ac_qty} (₹{ac_price}/AC) = ₹{ac_total}\n"
        
        if fridge_qty > 0:
            email_content += f"🧊 Fridge Service ({fridge_type}) x{fridge_qty} (₹{fridge_price}/unit) = ₹{fridge_total}\n"
        
        if wm_qty > 0:
            email_content += f"🧺 Washing Machine ({wm_type}) x{wm_qty} (₹{wm_price}/unit) = ₹{wm_total}\n"
        
        if extra_services:
            email_content += f"\n📌 Additional Services: {extra_services}\n"
        if extra_charges > 0:
            email_content += f"➕ Extra Charges: ₹{extra_charges}\n"
            
        if ac_offer_applied:
            email_content += f"""
═══════════════════════════════════════════
🎉 SPECIAL OFFER APPLIED!
You saved ₹{ac_savings} on AC service!
═══════════════════════════════════════════
"""
            
        email_content += f"""
═══════════════════════════════════════════
💰 TOTAL AMOUNT: ₹{grand_total}
═══════════════════════════════════════════
Technician Remarks:

{remarks}


Our service team will contact you within 30 minutes to schedule the visit.
We provide 100% guarantee on all repairs with genuine spare parts.


For immediate assistance:
📞 Call/WhatsApp: 8174083966 or 9532006520
📧 Email: sscwallahtec966@gmail.com


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
        msg['Subject'] = f"Service Confirmation | {cust_name} | {st.session_state.booking_id}"
        
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
    """Send SMS to customer - EXACT format as preview"""
    try:
        # Build SMS exactly as shown in preview
        sms_content = f"""Dear {cust_name},
Thank you for choosing SSC Wallah Technician for your appliance service needs.
Here is your confirmed service estimate:


═══════════════════════════════════════════
📋 BOOKING DETAILS
═══════════════════════════════════════════
Booking ID:     {st.session_state.booking_id}
Date & Time:    {current_date} at {current_time}
Location:       {cust_location}
Technician:     {st.session_state.technician_name}
Contact:        {cust_phone}


═══════════════════════════════════════════
🛠️ SERVICES REQUESTED
═══════════════════════════════════════════
"""
        if ac_qty > 0:
            if ac_offer_applied:
                sms_content += f"❄️ AC Service ({ac_type}) x{ac_qty} (Special Offer ₹{ac_offer_price}/AC) = ₹{ac_total}\n"
            else:
                sms_content += f"❄️ AC Service ({ac_type}) x{ac_qty} (₹{ac_price}/AC) = ₹{ac_total}\n"
        
        if fridge_qty > 0:
            sms_content += f"🧊 Fridge Service ({fridge_type}) x{fridge_qty} (₹{fridge_price}/unit) = ₹{fridge_total}\n"
        
        if wm_qty > 0:
            sms_content += f"🧺 Washing Machine ({wm_type}) x{wm_qty} (₹{wm_price}/unit) = ₹{wm_total}\n"
        
        if extra_services:
            sms_content += f"\n📌 Additional Services: {extra_services}\n"
        if extra_charges > 0:
            sms_content += f"➕ Extra Charges: ₹{extra_charges}\n"
            
        if ac_offer_applied:
            sms_content += f"""
═══════════════════════════════════════════
🎉 SPECIAL OFFER APPLIED!
You saved ₹{ac_savings} on AC service!
═══════════════════════════════════════════
"""
            
        sms_content += f"""
═══════════════════════════════════════════
💰 TOTAL AMOUNT: ₹{grand_total}
═══════════════════════════════════════════


{remarks}


Our service team will contact you within 30 minutes to schedule the visit.
We provide 100% guarantee on all repairs with genuine spare parts.


For immediate assistance:
📞 Call/WhatsApp: 8174083966 or 9532006520
📧 Email: sscwallahtec966@gmail.com


Thank you for trusting SSC Wallah Technician!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SSC Wallah Team
Lucknow • Full Area Service • 24x7 Support
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
        
        # For demo purposes, we'll just show success
        # In production, integrate with SMS API here
        st.info(f"📱 SMS would be sent to {cust_phone} with EXACT format shown above")
        return True, "SMS demo mode"
    except Exception as e:
        return False, str(e)

with col_s1:
    if st.button("📧 Send Email Only", key="email_only"):
        if not all([cust_name, cust_email, cust_location]):
            st.error("Please fill all customer details")
        elif total_qty == 0:
            st.warning("No services selected")
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
            st.error("Customer phone number required")
        else:
            with st.spinner("Preparing SMS..."):
                success, msg = send_customer_sms()
                if success:
                    st.success(f"✅ SMS ready for {cust_phone} (check preview above)")

with col_s3:
    if st.button("📧📱 Send Both", key="both"):
        if not all([cust_name, cust_email, cust_location, cust_phone]):
            st.error("Please fill all customer details")
        else:
            with st.spinner("Sending email and SMS..."):
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
    ⚡ AC: Split ₹499/Window ₹399 | Fridge: ₹399-599 | WM: ₹449-599 ⚡<br>
    ⚡ 2+ AC Jet Service @ ₹399/AC Special Offer ⚡<br>
    © SSC Wallah Technician — 8174083966 / 9532006520 — sscwallahtec966@gmail.com
</div>
""", unsafe_allow_html=True)