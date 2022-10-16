import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from import_data import load_data
import numpy as np

# Import data
st.cache()
df = load_data()

dictionary = {'Home': ['RAND Home','Login'], 'RAND Route Optimizer': ['RAND Dashboard','Tabular Data'] }
Navigation = st.sidebar.selectbox("Navigation Menu:", sorted(dictionary.keys()))
selectbox = st.sidebar.radio("Choose any page:", sorted(dictionary[Navigation]))


if selectbox == 'Login':
    st.header('RAND Login Form')
    placeholder = st.empty()
    with placeholder.form("login"):
        st.markdown("#### Enter your credentials")
        name = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
    if submit:
        st.success('You have successfully loged in')
        st.info('Please navigate through our features')

if selectbox == 'RAND Home':
    st.title('RAND Delivery Route Optimizer')
    st.subheader('Route Analytics and Navigation in Delivery')
    st.image("assets/route.png")
    source = st.text_input("Enter the source address")
    destination = st.text_input("Enter the destination address")
    time = st.slider("Enter the expected time to reach the destination (in hours)",1,24)
    if st.button('submit'):
         newtime = time - 1
         st.write("The expected time you need to reach from",source,"to",destination,"is",time,"in hours")
         st.write("The time taken to reach destination using RAND is ",newtime,"in hours")
         st.warning("Got on to dashboard to get optimizer route")
         st.success("Have a nice journey")


    


if selectbox == 'RAND Dashboard':
    from pluggers import load_dashobard
    load_dashobard()

# display data
if selectbox == 'Tabular Data':
    st.title('🗃 RAND Delivery Request Database')
    gd = GridOptionsBuilder.from_dataframe(df)
    gd.configure_default_column(groupable=False, editable=True)
    gd.configure_selection(selection_mode='multiple',use_checkbox=True)
    gd.configure_side_bar()
    
    st.download_button(
     label="Download data as CSV",
     data=df.to_csv().encode('utf-8'),
     file_name='large_df.csv',
     mime='text/csv'
     )

    df_grid = AgGrid(df, height=400, gridOptions=gd.build(),update_mode=GridUpdateMode.SELECTION_CHANGED, theme='light')
    if df_grid['selected_rows']:
        st.dataframe(pd.DataFrame(df_grid['selected_rows'][0], index=np.arange(len(df_grid['selected_rows'][0]))))
    

    # st.write('### Data Summary')
    # AgGrid(df.describe(), fit_columns_on_grid_load=False)
