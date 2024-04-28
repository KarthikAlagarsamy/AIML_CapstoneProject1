import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

# Function to execute SQL query and return DataFrame
def execute_query(conn, query):
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    df_result = pd.DataFrame(result, columns=[desc[0] for desc in cur.description])
    return df_result

# Connect to the databases
conn1 = sqlite3.connect('/content/Agg_tra.db')
conn2 = sqlite3.connect('/content/Agg_user.db')
conn3 = sqlite3.connect('/content/map_tra.db')
conn4 = sqlite3.connect('/content/map_user.db')
conn5 = sqlite3.connect('/content/top_tra.db')
conn6 = sqlite3.connect('/content/top_user.db')

# Define the options for the selectbox
options = ['Top 5 States with Highest Transaction Amount', 'User Count by Year and Quarter','Total Transaction Count by State',
           'Total Transaction Amount by State','Total User Count by State','Total Registered User Count by State',
           'Transaction Count by Transaction Type and Quarter','Average User Percentage by Brand','Top 5 Districts with Highest Registered Users',
           'Transaction Count by Year and Quarter']
selected_option = st.selectbox('Select query on Phonepe Pulse Data to display:', options)

if selected_option == 'Top 5 States with Highest Transaction Amount':
    # Execute the first query
    query1 = """
            SELECT State, SUM(Transaction_amount) AS Total_Transaction_Amount
            FROM top_tra_SQL
            GROUP BY State
            ORDER BY Total_Transaction_Amount DESC
            LIMIT 5"""
    df1_result = execute_query(conn5, query1)
    df1_result = pd.DataFrame(df1_result, columns=['State', 'Total_Transaction_Amount'])
    df1_result.index = df1_result.index + 1
    st.write(df1_result)

elif selected_option == 'User Count by Year and Quarter':
    # Execute the second query
    query2 = """
            SELECT Year, Quarter, SUM(User_Count) AS Total_User_Count
            FROM Agg_user_SQL
            GROUP BY Year, Quarter"""
    df2_result = execute_query(conn2, query2)
    fig = px.bar(df2_result, x='Year', y='Total_User_Count', color='Quarter',
             title='User Count by Year and Quarter',
             labels={'Year': 'Year', 'Total_User_Count': 'Total User Count'})
    fig.update_layout(xaxis_title='Year', yaxis_title='Total User Count')
    st.plotly_chart(fig)

elif selected_option == 'Total Transaction Count by State':
    # Execute the third query
    query3 = """
            SELECT State, SUM(Transaction_count) AS Total_Transaction_Count
            FROM Agg_tra_SQL
            GROUP BY State"""
    df3_result = execute_query(conn1, query3)
    fig = px.bar(df3_result, x='State', y='Total_Transaction_Count', 
             title='Total Transaction Count by State',
             labels={'State': 'State', 'Total_Transaction_Count': 'Transaction Count'})
    fig.update_layout(xaxis_title='State', yaxis_title='Transaction Count') 
    st.plotly_chart(fig)

elif selected_option == 'Total Transaction Amount by State':
    # Execute the fourth query
    query4 = """
            SELECT State, SUM(Transaction_amount) AS Total_Transaction_Amount
            FROM Agg_tra_SQL
            GROUP BY State"""
    df4_result = execute_query(conn1, query4)
    fig = px.bar(df4_result, x='State', y='Total_Transaction_Amount', 
             title='Total Transaction Amount by State',
             labels={'State': 'State', 'Total_Transaction_Amount': 'Transaction amount'})
    fig.update_layout(xaxis_title='State', yaxis_title='Transaction amount') 
    st.plotly_chart(fig)

elif selected_option == 'Total User Count by State':
    # Execute the fifth query
    query5 = """
            SELECT State, SUM(User_Count) AS Total_User_Count
            FROM Agg_user_SQL
            GROUP BY State"""
    df5_result = execute_query(conn2, query5)
    fig = px.bar(df5_result, x='State', y='Total_User_Count', 
             title='Total User Count by State',
             labels={'State': 'State', 'Total_User_Count': 'Total User Count'})
    fig.update_layout(xaxis_title='State', yaxis_title='Total User Count') 
    st.plotly_chart(fig)

elif selected_option == 'Total Registered User Count by State':
    # Execute the sixth query
    query6 = """
            SELECT State, SUM(Registered_User) AS Total_Registered_User_Count
            FROM top_user_SQL
            GROUP BY State"""
    df6_result = execute_query(conn6, query6)
    fig = px.bar(df6_result, x='State', y='Total_Registered_User_Count', 
             title='Total Registered User Count by State',
             labels={'State': 'State', 'Total_Registered_User_Count': 'Total Registered User Count'})
    fig.update_layout(xaxis_title='State', yaxis_title='Total Registered User Count') 
    st.plotly_chart(fig)

elif selected_option == 'Transaction Count by Transaction Type and Quarter':
    # Execute the seventh query
    query7 = """
            SELECT Year, Quarter, Transaction_type, SUM(Transaction_count) AS Total_Transaction_Count
            FROM Agg_tra_SQL
            GROUP BY Year, Quarter, Transaction_type"""
    df7_result = execute_query(conn1, query7)
    
    fig = px.bar(df7_result, x='Quarter', y='Total_Transaction_Count', color='Transaction_type', 
                 barmode='group', facet_col='Year', 
                 labels={'Total_Transaction_Count': 'Total Transaction Count'})
    
    fig.update_layout(title='Transaction Count by Transaction Type and Quarter',
                      xaxis_title='Quarter', yaxis_title='Total Transaction Count',
                      legend_title='Transaction Type', showlegend=True)
    
    st.plotly_chart(fig)

elif selected_option == 'Average User Percentage by Brand':
    # Execute the eighth query
    query8 = """
            SELECT Brands, AVG(User_Percentage) AS Average_User_Percentage
            FROM Agg_user_SQL
            GROUP BY Brands"""
    df8_result = execute_query(conn2, query8)
    
    fig = px.pie(df8_result, values='Average_User_Percentage', names='Brands', hole=0.2,
                 title='Average User Percentage by Brand')
    
    fig.update_traces(textposition='outside', textinfo='percent+label') 
    st.plotly_chart(fig)

elif selected_option == 'Top 5 Districts with Highest Registered Users':
    # Execute the ninth query
    query9 = """
            SELECT State, District, SUM(Registered_User) AS Total_Registered_User_Count
            FROM map_user_SQL
            GROUP BY State, District
            ORDER BY Total_Registered_User_Count DESC
            LIMIT 5"""
    df9_result = execute_query(conn4, query9)
    df9_result = pd.DataFrame(df9_result, columns=['District','State','Total_Registered_User_Count'])
    df9_result.index = df9_result.index + 1
    st.write(df9_result)

elif selected_option == 'Transaction Count by Year and Quarter':
    # Execute the tenth query
    query10 = """
            SELECT Year, Quarter, SUM(Transaction_count) AS Total_Transaction_Count
            FROM Agg_tra_SQL
            GROUP BY Year, Quarter"""
    df10_result = execute_query(conn1, query10)
    
    fig = px.bar(df10_result, x='Year', y='Total_Transaction_Count', color='Quarter', 
                 barmode='group', 
                 labels={'Total_Transaction_Count': 'Total Transaction Count'})
    
    fig.update_layout(title='Transaction Count by Year and Quarter',
                      xaxis_title='Year', yaxis_title='Total Transaction Count',
                      legend_title='Quarter', showlegend=True)
    
    st.plotly_chart(fig)

