# =====================================================
# StayEase - Hotel Booking Cost Calculator (styled version)
# College project: Python Programming for Business Students
# NOTE: All prices and policies are SAMPLE assumptions.
# This is a cost estimator, not a real booking system.
# Colour scheme: blue, gold and white
# =====================================================

# Section 1: Import Streamlit (we call it "st" to keep the code short)
import streamlit as st

# Section 2: Page setup. layout="wide" lets the page use the full screen width
st.set_page_config(page_title="StayEase", page_icon="🏨", layout="wide")

# Section 2B: Styling (CSS). This block only changes how the page LOOKS.
# It does not change any calculation. Colours: blue #0B2A5B, gold #D4AF37, white
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&display=swap');

/* Blue background for the whole page */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #061A3F 0%, #0B3C8C 60%, #14509F 100%);
}
[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 4rem; max-width: 1150px; }

/* Left side: hero text */
.hero-label { color: #D4AF37; letter-spacing: 4px; font-weight: 600; font-size: 0.85rem; }
.hero-title { font-family: 'Playfair Display', Georgia, serif; color: #FFFFFF;
              font-size: 3.4rem; line-height: 1.15; margin: 0.6rem 0 1rem 0; }
.hero-text { color: #EAF0FA; font-size: 1.1rem; line-height: 1.6; }
.hero-link { display: inline-block; color: #FFFFFF; letter-spacing: 3px; font-weight: 600;
             border-bottom: 2px solid #D4AF37; padding-bottom: 4px; margin: 0.8rem 0 1.5rem 0; }
.hero-note { color: #C9D6EE; font-size: 0.85rem; font-style: italic; margin-bottom: 1.2rem; }

/* Right side: white booking card */
.st-key-booking_card { background: #FFFFFF; padding: 2.2rem; border-radius: 6px;
                       box-shadow: 0 10px 40px rgba(0, 0, 0, 0.35); }
.card-title { font-family: 'Playfair Display', Georgia, serif; color: #0B2A5B;
              font-size: 2rem; margin-bottom: 0.5rem; }
.st-key-booking_card label p { color: #0B2A5B !important; font-weight: 500; }
/* Make the input boxes light blue-white, even if the computer is in dark mode */
.st-key-booking_card [data-testid="stSelectbox"] div,
.st-key-booking_card [data-testid="stNumberInputContainer"],
.st-key-booking_card [data-testid="stNumberInputContainer"] div {
    background-color: #F4F6FB !important; color: #0B2A5B !important; }
.st-key-booking_card [data-testid="stWidgetLabel"],
.st-key-booking_card [data-testid="stWidgetLabel"] div { background-color: transparent !important; }
.st-key-booking_card input, .st-key-booking_card [data-testid="stSelectbox"] * { color: #0B2A5B !important; }
.st-key-booking_card [data-testid="stNumberInputContainer"] button { color: #0B2A5B !important; }
/* Checkboxes: white box with blue border, gold when ticked */
.st-key-booking_card [data-testid="stCheckbox"] label > div:first-of-type {
    background-color: #FFFFFF !important; border: 1.5px solid #0B2A5B !important; }
.st-key-booking_card [data-testid="stCheckbox"] label:has(input:checked) > div:first-of-type {
    background-color: #D4AF37 !important; border-color: #D4AF37 !important; }
/* Dropdown list that opens when the room type is clicked */
[data-testid="stSelectboxVirtualDropdown"], [data-testid="stSelectboxVirtualDropdown"] * ,
ul[role="listbox"], ul[role="listbox"] li { background-color: #FFFFFF !important; color: #0B2A5B !important; }
/* Top-right menu text in white so it is visible on the blue background */
[data-testid="stToolbar"] * { color: #FFFFFF !important; }

/* Price breakdown card (gold border) */
.st-key-result_card { background: rgba(255, 255, 255, 0.08); border: 1px solid #D4AF37;
                      border-radius: 6px; padding: 1.6rem; }
.result-title { font-family: 'Playfair Display', Georgia, serif; color: #D4AF37;
                font-size: 1.6rem; margin-bottom: 0.6rem; }
.bill-row { display: flex; justify-content: space-between; color: #FFFFFF;
            padding: 0.55rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.18); }
.bill-gold { color: #D4AF37; font-weight: 600; }
.st-key-result_card [data-testid="stAlert"] { background-color: #D4AF37 !important;
            border-radius: 4px; margin-top: 1rem; }
.st-key-result_card [data-testid="stAlert"] * { color: #061A3F !important; font-weight: 700;
            background-color: transparent !important; }
</style>
""", unsafe_allow_html=True)

# Section 4: Dictionary of room types and their price per night (in rupees)
# A dictionary stores pairs: room name (key) -> price (value)
room_prices = {
    "Standard Room": 2500,
    "Deluxe Room": 4000,
    "Suite": 6500
}

# Prices of the extra services (stored in variables so they are easy to change)
breakfast_price = 500      # per guest, per night
extra_bed_price = 1000     # per night
late_checkout_price = 500  # once per booking

# Layout: split the page into a wide left column (info + results) and a right column (form)
left_column, right_column = st.columns([1.3, 1], gap="large")

# Sections 5 to 10: All input widgets go inside the white booking card (right column)
with right_column:
    with st.container(key="booking_card"):
        st.markdown('<div class="card-title">Estimate Your Stay</div>', unsafe_allow_html=True)

        # Section 5: Dropdown for room type (list of room names comes from the dictionary)
        room_type = st.selectbox("Room type", list(room_prices.keys()))

        # Section 6: Number of nights (whole number, 1 to 30)
        nights = st.number_input("Number of nights (1 to 30)", min_value=1, max_value=30, value=1, step=1)

        # Section 7: Number of guests (whole number, 1 to 10)
        guests = st.number_input("Number of guests (1 to 10)", min_value=1, max_value=10, value=1, step=1)

        # Sections 8, 9 and 10: Checkboxes. Each one gives True (ticked) or False (not ticked)
        want_breakfast = st.checkbox("Breakfast (₹500 per guest per night)")
        want_extra_bed = st.checkbox("Extra bed (₹1,000 per night)")
        want_late_checkout = st.checkbox("Late checkout (₹500 once per booking)")

# Left column: heading, introduction and the price breakdown
with left_column:
    # Section 3: Heading and introduction
    st.markdown("""
<div class="hero-label">HOTEL COST CALCULATOR</div>
<div class="hero-title">StayEase<br>Plan Your Stay, Know Your Price</div>
<div class="hero-text">Choose your room and extras to estimate the cost of your stay. Longer stays unlock bigger discounts.</div>
<div class="hero-link">ESTIMATE YOUR STAY</div>
<div class="hero-note">Note: All prices and discounts shown here are sample assumptions for a college project.</div>
""", unsafe_allow_html=True)

    with st.container(key="result_card"):
        # Section 17: Check the input first, so the app never crashes on bad values
        if nights < 1 or nights > 30:
            st.error("Number of nights must be between 1 and 30.")
        elif guests < 1 or guests > 10:
            st.error("Number of guests must be between 1 and 10.")
        else:
            # Section 11: Room cost = price per night x number of nights
            room_price_per_night = room_prices[room_type]
            room_cost = room_price_per_night * nights

            # Section 12: Cost of optional services (start at 0, add only if ticked)
            breakfast_cost = 0
            extra_bed_cost = 0
            late_checkout_cost = 0

            if want_breakfast:
                breakfast_cost = breakfast_price * guests * nights  # depends on guests AND nights
            if want_extra_bed:
                extra_bed_cost = extra_bed_price * nights           # depends on nights only
            if want_late_checkout:
                late_checkout_cost = late_checkout_price            # charged only once

            services_cost = breakfast_cost + extra_bed_cost + late_checkout_cost

            # Section 13: Subtotal = room cost + services (the discount is applied to this)
            subtotal = room_cost + services_cost

            # Section 14: Choose the discount percentage using the number of nights
            if nights <= 2:
                discount_percent = 0    # 1-2 nights: no discount
            elif nights <= 4:
                discount_percent = 5    # 3-4 nights: 5% discount
            else:
                discount_percent = 10   # 5-30 nights: 10% discount

            # Section 15: Discount amount and final total
            discount_amount = subtotal * discount_percent / 100
            final_total = subtotal - discount_amount

            # Section 16: Show the itemised price breakdown and the final total
            st.markdown(f"""
<div class="result-title">Your Price Breakdown</div>
<div class="bill-row"><span>Room: {room_type} - ₹{room_price_per_night:,.2f} x {nights} night(s)</span><span>₹{room_cost:,.2f}</span></div>
<div class="bill-row"><span>Breakfast</span><span>₹{breakfast_cost:,.2f}</span></div>
<div class="bill-row"><span>Extra bed</span><span>₹{extra_bed_cost:,.2f}</span></div>
<div class="bill-row"><span>Late checkout</span><span>₹{late_checkout_cost:,.2f}</span></div>
<div class="bill-row"><span>Subtotal</span><span>₹{subtotal:,.2f}</span></div>
<div class="bill-row bill-gold"><span>Discount ({discount_percent}%)</span><span>- ₹{discount_amount:,.2f}</span></div>
""", unsafe_allow_html=True)
            st.success(f"Final Total: ₹{final_total:,.2f}")
