import streamlit as st
import retail
import wholesale

def main():
    st.title('Elyxrtore Shopify Wholesale & Retail')

    # Displaying all dropdowns and input in one line
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        page_option = ['Retail Analysis', 'Wholesale Analysis']
        page = st.selectbox('Choose Data Type:', page_option)
        
    if page == 'Retail Analysis':
        retail.display_retail_dashboard(col2, col3, col4)
    elif page == 'Wholesale Analysis':
        wholesale.display_wholesale_dashboard(col2, col3, col4)

if __name__ == '__main__':
    main()
