import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd

st.title("Bet Scraper")

uploaded_file = st.file_uploader("Choose an HTML file", type="html")

if uploaded_file is not None:
    html_content = uploaded_file.read().decode("utf-8")
    st.success("File uploaded successfully!")
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all rows with the correct class
    bet_rows = soup.select(".bet-history__table__body__rows__columns")
    
    data = []

    for row in bet_rows:
        ticket = row.select_one(".bet-history__table__body__rows__columns--id")
        date = row.select_one(".bet-history__table__body__rows__columns--date")
        description = row.select_one(".bet-history__table__body__rows__columns--description")
        bet_type = row.select_one(".bet-history__table__body__rows__columns--type")
        status = row.select_one(".bet-history__table__body__rows__columns--status")
        amount = row.select_one(".bet-history__table__body__rows__columns--amount--mobile")
        to_win = row.select_one(".bet-history__table__body__rows__columns--towin")

        # Only add rows that contain valid data
        if ticket and date:
            data.append({
                "Ticket #": ticket.text.strip() if ticket else "",
                "Date": date.text.strip() if date else "",
                "Description": description.text.strip() if description else "",
                "Type": bet_type.text.strip() if bet_type else "",
                "Status": status.text.strip() if status else "",
                "Amount": amount.text.strip() if amount else "",
                "To Win": to_win.text.strip() if to_win else "",
            })

    if data:
        df = pd.DataFrame(data)
        st.subheader("Parsed Bet History")
        st.dataframe(df)
    else:
        st.warning("No betting data found in the uploaded file.")
