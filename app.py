import streamlit as st
import pandas as pd
from datetime import datetime
from db import init_db, add_sub, get_all_sub, delete_sub
from guide_library import get_cancel_guide

st.set_page_config(page_title="Subscription Renewal Tracker", layout="wide")
init_db()

st.title("📅 Subscription Renewal Tracker")
st.subheader("Fintech Mini MVP | Manual Entry, Alert, Cancellation Guide & Export")

# -------- Add Form --------
with st.expander("➕ Add Subscription Record"):
    name = st.text_input("Subscription name (e.g. ChatGPT Plus)")
    platform = st.text_input("Platform")
    renew_date = st.date_input("Next renewal date")
    cycle = st.selectbox("Billing cycle", ["Monthly", "Yearly", "Weekly", "Quarterly"])
    amount = st.number_input("Amount", min_value=0.0, step=1.0)
    currency = st.text_input("Currency", value="HKD")
    link = st.text_input("Official link (optional)")
    note = st.text_input("Note (optional)")

    if st.button("Save"):
        add_sub(name, platform, renew_date, cycle, amount, currency, link, note)
        st.success("Saved!")
        st.rerun()

# -------- Upcoming Renewals --------
st.markdown("---")
st.header("⏰ Upcoming Renewals (within 7 days)")
all_sub = get_all_sub()
today = datetime.now().date()
upcoming = []
for row in all_sub:
    try:
        rd = datetime.strptime(row["renew_date"], "%Y-%m-%d").date()
        diff = (rd - today).days
        if 0 <= diff <=7:
            upcoming.append((row, diff))
    except:
        pass

if upcoming:
    for item, d in upcoming:
        st.info(f"{item['name']} ({item['platform']}) | {item['amount']} {item['currency']} | Renew on {item['renew_date']}")
        with st.expander("⌄ Get cancellation guide"):
            st.warning("⚠️ Reference only, confirm on official website.")
            guide = get_cancel_guide(item["platform"])
            st.write(guide)
else:
    st.info("No subscriptions due in 7 days.")

# -------- All Table --------
st.markdown("---")
st.header("📋 All Active Subscriptions")
if all_sub:
    df = pd.DataFrame(all_sub)
    # compute days to renew
    def calc_days(r):
        try:
            rd = datetime.strptime(r["renew_date"], "%Y-%m-%d").date()
            return (rd - today).days
        except:
            return None
    df["days_to_renew"] = df.apply(calc_days, axis=1)
    st.dataframe(df, hide_index=True)

    # Delete
    del_id = st.number_input("Enter ID to delete", min_value=1, step=1)
    if st.button("Delete this record"):
        delete_sub(del_id)
        st.success("Deleted")
        st.rerun()

    # Export CSV
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button("📩 Export CSV", data=csv_data, file_name="my_subscriptions.csv", mime="text/csv")

    # Cost Summary
    st.markdown("---")
    st.header("💰 Recurring Cost Summary")
    monthly_sum = 0
    yearly_sum = 0
    for _, r in df.iterrows():
        amt = float(r["amount"])
        if r["cycle"] == "Monthly":
            monthly_sum += amt
            yearly_sum += amt *12
        elif r["cycle"] == "Yearly":
            yearly_sum += amt
        elif r["cycle"] == "Quarterly":
            monthly_sum += amt /3
            yearly_sum += amt *4
        elif r["cycle"] == "Weekly":
            monthly_sum += amt * 4.33
            yearly_sum += amt *52
    st.write(f"Monthly total: {monthly_sum:.2f} {currency}")
    st.write(f"Yearly total: {yearly_sum:.2f} {currency}")

else:
    st.info("No records yet. Add your first subscription above.")
