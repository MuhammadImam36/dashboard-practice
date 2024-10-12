import streamlit as st
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
ecommerce = pd.read_csv('./ecommerce.csv')
ecommerce["order_purchase_timestamp"] = pd.to_datetime(ecommerce["order_purchase_timestamp"])

# Membuat tabel category_counts
category_counts = ecommerce.groupby(['product_category_name', 'product_category_name_english']).size().reset_index(name='count')
category_counts = category_counts.sort_values(by='count', ascending=False).reset_index()

# Membuat tabel monthly_orders
monthly_orders = ecommerce.groupby(ecommerce['order_purchase_timestamp'].dt.strftime('%B')).agg({
    "order_id": "count",
}).reset_index()

monthly_orders.rename(columns={
    "order_id": "order_count",
    "order_purchase_timestamp": "month",
}, inplace=True)

month_order = ["January", "February", "March", "April", "May", "June", 
               "July", "August", "September", "October", "November", "December"]
monthly_orders['month'] = pd.Categorical(monthly_orders['month'], categories=month_order, ordered=True)
monthly_orders = monthly_orders.sort_values('month')
monthly_orders = monthly_orders.reset_index(drop = True)
    
# Membuat header
st.header('Dashboard Analisis Dataset Ecommerce')

tab1, tab2  = st.tabs(["Tabel 1", "Tabel 2"])

# Visualisasi tabel
with tab1:
    st.subheader('Penjualan produk ecommerce setiap bulan')

    tabel_penjualan_produk = plt.figure(figsize=(20, 10)) 
    plt.plot(monthly_orders["month"], monthly_orders["order_count"], marker='o', markersize=15, linewidth=5, color="#72BCD4")  
    plt.xticks(fontsize=17) 
    plt.yticks(fontsize=15) 

    st.pyplot(tabel_penjualan_produk)

    # Insight
    with st.expander("Insight"):
        st.write(
            "Pada bulan agustus, kustomer paling banyak melakukan transaksi, namun di bulan berikutnya terjadi penurunan yang signifikan"
        )
        
with tab2:
    st.subheader('Top 5 produk yang paling banyak dibeli oleh kustomer')

    tabel_produk = plt.figure(figsize=(20, 10))
    sns.barplot(x='product_category_name', y='count', data=category_counts[:5])
    plt.xticks(fontsize=20) 
    plt.yticks(fontsize=20)
    plt.xlabel('')
    plt.ylabel('') 

    st.pyplot(tabel_produk)

    # Insight
    with st.expander("Insight"):
        st.write(
            "Cama_mesa_banho menjadi produk paling banyak dibeli oleh kustomer"
        )

st.caption('Muhammad Imam Wahid ML-80')