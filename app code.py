import streamlit as st
import pandas as pd
import plotly.express as px

# Title and Dataset Description
st.title("Tourism Insights in Lebanon 2023: Hotels, Restaurants, and Development Potential by Region")
st.markdown("""
    Explore Lebanon's tourism sector in 2023 with interactive visualizations. 
    Filter data by the number of guest houses and other tourism-related metrics to uncover insights into the tourism potential 
    and growth opportunities across different regions.
""")

# Load dataset
path = "https://linked.aub.edu.lb/pkgcube/data/f74a59420e9ef432f644575983b672b8_20240907_185056.csv"
df = pd.read_csv(path)

# Drop unnecessary columns
df.drop(columns=["publisher", "dataset", "references"], inplace=True)

# Modify 'refArea' by extracting the last part after the last slash
df['refArea'] = df['refArea'].apply(lambda x: x.split('/')[-1])

# Dropdown menu for the first plot
district_option = st.selectbox('Select District or View All Districts for First Plot',
                               options=['All Districts'] + df['refArea'].unique().tolist(),
                               key='district_filter')

# Filter data for the first plot based on the selected district
if district_option == 'All Districts':
    plot_df = df.copy()
else:
    plot_df = df[df['refArea'] == district_option]

# Plot 1: Scatter Plot of Total Number of Restaurants vs. Total Number of Guest Houses
st.subheader('1. Total Number of Restaurants vs. Total Number of Guest Houses')
st.write("Select whether to view data for all districts or a specific district above.")
fig_scatter = px.scatter(plot_df,
                         x='Total number of guest houses',
                         y='Total number of restaurants',
                         color='refArea',
                         hover_data={'refArea': True},
                         title='Total Number of Restaurants vs. Guest Houses by Region',
                         template='plotly_white')
fig_scatter.update_layout(xaxis_title='Total Number of Guest Houses',
                          yaxis_title='Total Number of Restaurants',
)
st.plotly_chart(fig_scatter, use_container_width=True)
# Summary for Akkar and Matn
summary = "Akkar: Low restaurants & high number of guest houses, rural, growth potential in eco-tourism; Matn: High restaurants, few guest houses, urban, potential in expanding accommodations."

# Display the summary in Streamlit
st.write(summary)

# Plot 2: Horizontal Bar Chart of Total Number of Guest Houses by Region (Flipped)
st.subheader('2. Bar Chart of Total Number of Guest Houses by Region')
fig_bar = px.bar(df,
                 y='refArea',  # Swap x and y to flip the graph
                 x='Total number of guest houses',
                 color_discrete_sequence=['blue'],  # Set all bars to the same color
                 hover_data={'Total number of guest houses': True, 'Total number of restaurants': True},
                 title='Total Number of Guest Houses by Region',
                 template='plotly_white')
fig_bar.update_layout(showlegend=False, 
                      uniformtext_minsize=8, 
                      uniformtext_mode='hide',
                      yaxis_title='Region',
                      xaxis_title='Total Number of Guest Houses')
st.plotly_chart(fig_bar, use_container_width=True)

# Interactive Pie Chart of Restaurant Distribution by Region
st.subheader('3. Pie Chart of Restaurant Distribution by Region')
fig_pie = px.pie(df,
                 names='refArea',
                 values='Total number of restaurants',
                 title='Distribution of Restaurants by Region',
                 template='plotly_white')
fig_pie.update_layout(showlegend=True, 
                      autosize=True)
st.plotly_chart(fig_pie, use_container_width=True)
# Summary for Akkar and Matn
summary1 = "Baabda district has the highest number of Restaurant with 11%, followed by matn district with 8.67% from the total of restaurants"

# Display the summary in Streamlit
st.write(summary1)

# Dropdown menu for the fourth plot
selected_refArea = st.selectbox('Select a District/Region for Histogram',
                                df['refArea'].unique(),
                                key='histogram_filter')

filtered_df_hist = df[df['refArea'] == selected_refArea]

# Histogram of Total Number of Cafes, Restaurants, and Hotels in Selected District
st.subheader('4. Histogram of Total Number of Cafes, Restaurants, and Hotels in Selected District')
st.write("Select a district/region from the dropdown menu above to view the histogram.")
aggregated_df = filtered_df_hist[['Total number of cafes', 'Total number of restaurants', 'Total number of guest houses']].melt()
fig_hist_aggregated = px.histogram(aggregated_df,
                                   x='variable',
                                   y='value',
                                   color='variable',
                                   title=f'Distribution of Cafes, Restaurants, and Hotels in {selected_refArea}',
                                   labels={'variable': 'Type', 'value': 'Count'},
                                   template='plotly_white')
fig_hist_aggregated.update_layout(bargap=0.2, 
                                  xaxis_title='Type',
                                  yaxis_title='Count',
                                  xaxis_tickangle=-45)  # Rotating x-axis labels by -90 degrees
st.plotly_chart(fig_hist_aggregated, use_container_width=True)

# Conclusion message
st.markdown("""
    These interactive visualizations help explore the tourism landscape in Lebanon for 2023, 
    enabling deeper insights into which regions offer higher concentrations of guest houses, restaurants, and cafes.
""")
