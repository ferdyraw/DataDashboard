import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

st.set_page_config(page_title="E-Commerce Public Dataset Analysis",
page_icon=":snow_capped_mountain", layout='wide')

def create_rfm_df(all_df):
  rfm_df = all_df.groupby(by="customer_id", as_index=False).agg({
      "order_purchase_timestamp": "max", 
      "order_id": "nunique", 
      "total_price": "sum" 
  })
  rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]

  rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
  recent_date = all_df["order_purchase_timestamp"].dt.date.max()
  rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
  rfm_df.drop("max_order_timestamp", axis=1, inplace=True)

  customer_name = []
  for i in range(1, 98667):
    customer_name.append("Customer " + str(i))

  rfm_df['customer_name'] = customer_name 

  return rfm_df

customer_order_df = pd.read_csv('./dashboard/customer_order_data.csv')

datetime_columns = ["shipping_limit_date",
                    "order_purchase_timestamp",
                    "order_estimated_delivery_date"]

for column in datetime_columns:
  customer_order_df[column] = pd.to_datetime(customer_order_df[column])

state_df = pd.read_csv('./dashboard/state_data.csv')
rfm_df = create_rfm_df(customer_order_df)

with st.sidebar:
  st.subheader("My Dashboard")
  st.text("Nama         : Ferdy Rizkiawan")
  st.text("Email        : ferdyrizkiawan@student.uns.ac.id")
  st.text("Id Dicoding  : ferdyrizz")

with st.container():
  st.subheader('E-Commerce Pubilc Dataset Analysis')
  st.title("Hi, I am Ferdy :wave:")
  st.markdown(
    """I'm a Computer Science student at Sebelas Maret University.""")

  with st.expander("Learn more"):
    st.write("[LinkedIn](https://linkedin.com/in/ferdyrizkiawan)")
    st.write("[Instagram](https://instagram.com/ferdyrizkiawan)")
    st.write("[GitHub](https://github.com/ferdyraw)")
    
with st.container():
  st.write("---")
  st.subheader("Apakah lokasi para seller tersebar merata di setiap state?")

  fig, ax = plt.subplots(figsize=(16, 8))
  sns.barplot(y=state_df['State'], x=state_df['Count'], orient='h', color='#1F9ED1')
  ax.set_ylabel("State", fontsize=14)
  ax.set_xlabel(None)
  ax.set_title("Population of Seller in Each State", loc="center", fontsize=17)
  
  st.pyplot(fig)

  with st.expander("See answer"):
    st.write("""Tidak, para seller belum tersebar secara merata. Bahkan, hampir setengah dari total seller
    berasal dari state "SP". Dan setengah dari state yang ada memiliki total seller yang sangat jauh dibandingkan
    dengan 10 state terbanyak. Sehingga, perusahaan perlu mencari suatu mencari solusi atas permasalahan ini.""")


with st.container():
  st.write("---")

  st.subheader("Best Customer Based on RFM Parameters")
  
  fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(45, 10))
  colors = ["#1F9ED1"]
  
  sns.barplot(x="recency", y="customer_name", data=rfm_df.sort_values(by="recency", ascending=True).head(10), palette=colors, ax=ax[0], orient='h')
  ax[0].set_ylabel(None)
  ax[0].set_xlabel(None)
  ax[0].set_title("By Recency (days)", loc="center", fontsize=40)
  ax[0].tick_params(axis='y', labelsize=15)
  ax[0].tick_params(axis='x', labelsize=20)
  
  sns.barplot(x="frequency", y="customer_name", data=rfm_df.sort_values(by="frequency", ascending=False).head(10), palette=colors, ax=ax[1])
  ax[1].set_ylabel(None)
  ax[1].set_xlabel(None)
  ax[1].set_title("By Frequency", loc="center", fontsize=40)
  ax[1].tick_params(axis='y', labelsize=15)
  ax[1].tick_params(axis='x', labelsize=20)
  
  sns.barplot(x="monetary", y="customer_name", data=rfm_df.sort_values(by="monetary", ascending=False).head(10), palette=colors, ax=ax[2])
  ax[2].set_ylabel(None)
  ax[2].set_xlabel(None)
  ax[2].set_title("By Monetary", loc="center", fontsize=40)
  ax[2].tick_params(axis='y', labelsize=15)
  ax[2].tick_params(axis='x', labelsize=20)
  
  st.pyplot(fig)

  with st.expander("Kapan terakhir customer melakukan transaksi?"):
    st.write("Customer ke-29064 merupakan customer yang paling terakhir melakukan transaksi.")
  
  with st.expander("Seberapa sering seorang customer melakukan pembelian?"):
    st.write("Setelah dilakukan analisis dan visualisasi, rupaya setiap customer hanya melakukan satu kali pembelian. Oleh karena itu, perusahaan harus menganalisis lebih lanjut mengapa hal tersebut dapat terjadi.")

  with st.expander("Berapa banyak uang yang dihabiskan customer?"):
    st.write("Customer ke-8476 merupakan customer yang paling banyak mengeluarkan uang yaitu hampir sebesar 14000.")

st.caption('Copyright (c) 2023')