
# wholesale.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load your dataframes here if they are static or you can load them inside the function if they change
# For simplicity, I am using placeholder data loading code.
# df_wholesale = pd.read_csv('path_to_your_wholesale_data.csv')

def display_wholesale_dashboard(col2, col3, col4):
    # Dropdowns and input for the Wholesale Analysis

    df_wholesale = pd.read_csv('wholesale_final.csv')

    df_wholesale['Date'] = pd.to_datetime(df_wholesale['created_at'], utc=True).dt.date
    df_wholesale['Month-Year'] = pd.to_datetime(df_wholesale['Date']).dt.strftime('%B-%Y')

    with col2:
        month_year_options = sorted(list(df_wholesale['Month-Year'].unique()), key=lambda x: pd.to_datetime(x, format='%B-%Y'))
        selected_month_year = st.selectbox('Select Month-Year:', month_year_options)
        
    with col3:
        vendor_list = df_wholesale['vendor'].unique().tolist()
        vendor_list = [vendor if pd.notna(vendor) else None for vendor in vendor_list]
        selected_vendor = st.selectbox('Select vendor:', options=vendor_list)
        
    with col4:
        threshold_standard = st.number_input('Enter Threshold Value:', value=500)

    # Based on the selections, filter the data and create necessary visualizations
    # You can use the code we discussed earlier here to filter the data and plot graphs

    # -------

    if selected_vendor:
        df_wholesale_box = df_wholesale[df_wholesale['vendor'] == selected_vendor]
    if selected_month_year:
        df_wholesale_box = df_wholesale[df_wholesale['Month-Year'] == selected_month_year]

    unique_orders = df_wholesale_box.drop_duplicates(subset=['id'], keep='first')

    # Calculate total sales and total orders
    total_sales = unique_orders['total_price'].sum()
    total_orders = unique_orders['id'].nunique()

    # Display total sales and total orders in Streamlit with enhanced styling
    col_sales, col_orders = st.columns(2)
    with col_sales:
        st.markdown(f"<div style='background-color:#E6E6FA;padding-top:30px; padding:20px; border-radius:10px;'><h3 style='text-align:center; color:black;'>Total Sales</h3><h1 style='text-align:center; color:black;'>${total_sales:,.2f}</h1></div>", unsafe_allow_html=True)

    with col_orders:
        st.markdown(f"<div style='background-color:#E6E6FA; padding-top:30px; padding:20px; border-radius:10px;'><h3 style='text-align:center; color:black;'>Total Orders</h3><h1 style='text-align:center; color:black;'>{total_orders}</h1></div>", unsafe_allow_html=True)

    st.markdown(f"""
        <div style=' padding-top:20px;'>
        </div>
    """, unsafe_allow_html=True)
# -------

    # For Graph:
    


    # Ensure unique values for 'total_price' against each 'id'
    whole_unique_prices = df_wholesale.drop_duplicates(subset=['id'], keep='first')

    # Group by Month-Year and id to sum the total purchases for each account in each month
    grouped_by_month_email_complete = whole_unique_prices.groupby(['Month-Year', 'id']).agg(
        Monthly_Total_Price=pd.NamedAgg(column='total_price', aggfunc='sum')
    ).reset_index()

    # Filter accounts that have a monthly total less than or equal to the threshold
    filtered_accounts_complete = grouped_by_month_email_complete[grouped_by_month_email_complete['Monthly_Total_Price'] <= threshold_standard]

    # Count the number of unique accounts that meet the threshold for each month
    monthly_counts_complete = filtered_accounts_complete.groupby('Month-Year').size()

    # Sorting the index (Month-Year) in chronological order and plotting the graph
    monthly_counts_complete_sorted = monthly_counts_complete.sort_index(key=lambda x: pd.to_datetime(x, format='%B-%Y'))
    plt.figure(figsize=(15, 7))
    monthly_counts_complete_sorted.plot(kind='bar', color='skyblue', alpha=0.7)
    plt.title(f'Number of Accounts with Monthly Total Less Than or Equal to ${threshold_standard}')
    plt.xlabel('Month-Year')
    plt.ylabel('Number of Accounts')
    plt.xticks(rotation=45)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, axis='y')
    plt.tight_layout()
    plt.show()

    st.pyplot(plt,  use_container_width=True)


    # Table

    if selected_vendor:
        df_wholesale = df_wholesale[df_wholesale['vendor'] == selected_vendor]
    if selected_month_year:
        df_wholesale = df_wholesale[df_wholesale['Month-Year'] == selected_month_year]


        # Within your display_wholesale_dashboard function in wholesale.py after filtering the data based on vendor and month-year:


    # Ensure unique values for 'Total_Spent' against each 'id'
    filtered_unique_prices_df_wholesale = df_wholesale.drop_duplicates(subset=['id'], keep='first')

    # Group by Month-Year and id to sum the total purchases for each account in each month
    grouped_by_month_email_df_wholesale = filtered_unique_prices_df_wholesale.groupby(['Month-Year', 'id']).agg(
        Monthly_Total_Price=pd.NamedAgg(column='total_price', aggfunc='sum')
    ).reset_index()

    # Filter accounts that have a monthly total less than or equal to the threshold
    filtered_accounts_df_wholesale = grouped_by_month_email_df_wholesale[grouped_by_month_email_df_wholesale['Monthly_Total_Price'] <= threshold_standard]

    # Extracting the table data for the selected Month-Year, vendor, and Threshold
    table_data_df_wholesale = df_wholesale[df_wholesale['id'].isin(filtered_accounts_df_wholesale['id'])]
    table_data_df_wholesale = table_data_df_wholesale.sort_values(by='created_at', ascending=True)

    # Extracting the table data for the selected Month-Year, vendor, and Threshold using correct column names
    table_data_df_wholesale_corrected = table_data_df_wholesale[['created_at', 'customer_email', 'customer_first_name', 'customer_last_name', 'total_price', 'quantity', 'title']]


    # Display the table data
    st.dataframe(table_data_df_wholesale_corrected)


        # Within your display_wholesale_dashboard function in wholesale.py after filtering the data based on vendor and month-year:

# Within your display_wholesale_dashboard function in wholesale.py after filtering the data based on vendor and month-year:

    # Ensure unique values for 'total_price' against each 'id'
    df_wholesale_unique = df_wholesale.drop_duplicates(subset=['id'], keep='first')

    # Group by 'title' to aggregate total revenue ('total_price') and quantity sold ('quantity') for each product
    product_sales = df_wholesale_unique.groupby('title').agg(
        Total_Quantity=pd.NamedAgg(column='quantity', aggfunc='sum'),
        Total_Sales=pd.NamedAgg(column='total_price', aggfunc='sum')
    ).reset_index()

    # Display top products by total quantity sold
    st.write("### Top 15 Products by Quantity Sold")
    top_products_by_qty = product_sales.sort_values(by='Total_Quantity', ascending=False).head(15)

    plt.figure(figsize=(15, 7))
    plt.bar(top_products_by_qty['title'], top_products_by_qty['Total_Quantity'], color='skyblue')
    plt.title('Top 15 Products by Quantity Sold')
    plt.xlabel('Product Name')
    plt.ylabel('Total Quantity Sold')
    plt.xticks(rotation=45, ha='right')  # Rotating the x-axis labels
    plt.tight_layout()
    st.pyplot(plt)

    # Display top products by total sales
    st.write("### Top 15 Products by Revenue")
    top_products_by_sales = product_sales.sort_values(by='Total_Sales', ascending=False).head(15)

    plt.figure(figsize=(15, 7))
    plt.bar(top_products_by_sales['title'], top_products_by_sales['Total_Sales'], color='skyblue')
    plt.title('Top 15 Products by Revenue')
    plt.xlabel('Product Name')
    plt.ylabel('Total Revenue Generated')
    plt.xticks(rotation=45, ha='right')  # Rotating the x-axis labels
    plt.tight_layout()
    st.pyplot(plt)
