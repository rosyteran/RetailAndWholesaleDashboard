
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load your retail data (adjust the path accordingly)

# Function to display the retail dashboard
def display_retail_dashboard(col2, col3, col4):

    retail_complete = pd.read_csv('retailnew.csv')

    retail_complete['Date'] = pd.to_datetime(retail_complete['Created at'], utc=True).dt.date
    retail_complete['Month-Year'] = pd.to_datetime(retail_complete['Date']).dt.strftime('%B-%Y')

    with col2:
        threshold_standard = st.number_input('Threshold Amount:', min_value=0, value=500, step=1)
    with col3:
        month_year_list = retail_complete['Month-Year'].unique().tolist()
        selected_month_year = st.selectbox('Select Month-Year:', options=month_year_list)
    with col4:
        vendor_list = retail_complete['Vendor'].unique().tolist()
        vendor_list = [vendor if pd.notna(vendor) else None for vendor in vendor_list]
        selected_vendor = st.selectbox('Select Vendor:', options=vendor_list)

    # Sales ------

    if selected_vendor:
        df_retail_box = retail_complete[retail_complete['Vendor'] == selected_vendor]
    if selected_month_year:
        df_retail_box = retail_complete[retail_complete['Month-Year'] == selected_month_year]


    # Calculate total sales and total orders for retail
    total_sales_retail = df_retail_box['Total'].sum()  # Assuming 'Total' is the column for total price in retail
    total_orders_retail = df_retail_box['Name'].nunique()

    # Display total sales and total orders in Streamlit with enhanced styling for retail
    col_sales_retail, col_orders_retail = st.columns(2)
    with col_sales_retail:
        st.markdown(f"<div style='background-color:#E6E6FA;padding-top:30px; padding:20px; border-radius:10px;'><h3 style='text-align:center; color:black;'>Retail Total Sales</h3><h1 style='text-align:center; color:black;'>${total_sales_retail:,.2f}</h1></div>", unsafe_allow_html=True)

    with col_orders_retail:
        st.markdown(f"<div style='background-color:#E6E6FA; padding-top:30px; padding:20px; border-radius:10px;'><h3 style='text-align:center; color:black;'>Retail Total Orders</h3><h1 style='text-align:center; color:black;'>{total_orders_retail}</h1></div>", unsafe_allow_html=True)


    st.markdown(f"""
        <div style=' padding-top:20px;'>
        </div>
    """, unsafe_allow_html=True)

    # -- graph

    if selected_vendor:
        retail_complete = retail_complete[retail_complete['Vendor'] == selected_vendor]

    # Group by Month-Year and Email to sum the total purchases for each account in each month
    grouped_by_month_email_complete = retail_complete.groupby(['Month-Year', 'Email']).agg(
        Monthly_Total_Price=pd.NamedAgg(column='Total', aggfunc='sum')
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

    # table ---

    # Filtering the accounts based on the Month-Year filter
    filtered_orders_month = retail_complete[
        (retail_complete['Email'].isin(filtered_accounts_complete[filtered_accounts_complete['Month-Year'] == selected_month_year]['Email'])) & 
        (retail_complete['Month-Year'] == selected_month_year)
    ]

    # Ensuring all values in the Vendor column are strings before aggregating
    filtered_orders_month['Vendor'] = filtered_orders_month['Vendor'].astype(str)

    # Extracting and aggregating the required metrics with the new columns
    table_data_month = filtered_orders_month.groupby(['Email']).agg(
        Order_Date=pd.NamedAgg(column='Created at', aggfunc='first'),  # Taking the first order date in the month for demonstration
        Total_Spent=pd.NamedAgg(column='Total', aggfunc='sum'),
        Product_Names=pd.NamedAgg(column='Lineitem name', aggfunc=lambda x: ', '.join(set(x))),
        Total_Quantity=pd.NamedAgg(column='Lineitem quantity', aggfunc='sum'),
        Vendors=pd.NamedAgg(column='Vendor', aggfunc=lambda x: ', '.join(set(x)))
    ).reset_index()

    # Sorting by order date and displaying the resulting table
    table_data_month = table_data_month.sort_values(by='Order_Date', ascending=True)
    st.write(table_data_month,  use_container_width=True)


    # Porducts Sales Graphs --

    
    # Filter data
    filtered_data = retail_complete[retail_complete['Month-Year'] == selected_month_year]

    # Filtering accounts based on the threshold
    grouped_by_month_email_complete = retail_complete.groupby(['Month-Year', 'Email']).agg(
        Monthly_Total_Price=pd.NamedAgg(column='Total', aggfunc='sum')
    ).reset_index()

    filtered_emails = grouped_by_month_email_complete[grouped_by_month_email_complete['Monthly_Total_Price'] <= threshold_standard]['Email']
    filtered_data = filtered_data[filtered_data['Email'].isin(filtered_emails)]

    # Aggregate product sales
    product_sales = filtered_data.groupby('Lineitem name').agg(
        Total_Quantity=pd.NamedAgg(column='Lineitem quantity', aggfunc='sum'),
        Total_Sales=pd.NamedAgg(column='Total', aggfunc='sum')
    ).reset_index()

    st.write("### Top 15 Products by Quantity Sold")
    top_products_by_qty = product_sales.sort_values(by='Total_Quantity', ascending=False).head(15)

    plt.figure(figsize=(15, 7))
    plt.bar(top_products_by_qty['Lineitem name'], top_products_by_qty['Total_Quantity'], color='skyblue')
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
    plt.bar(top_products_by_sales['Lineitem name'], top_products_by_sales['Total_Sales'], color='skyblue')
    plt.title('Top 15 Products by Revenue')
    plt.xlabel('Product Name')
    plt.ylabel('Total Revenue Generated')
    plt.xticks(rotation=45, ha='right')  # Rotating the x-axis labels
    plt.tight_layout()
    st.pyplot(plt)


    # Display the graph and table

# If you want to test this file independently, uncomment the below line
# display_retail_dashboard()
