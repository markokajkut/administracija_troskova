import streamlit as st
import mariadb
import datetime
import os
import pandas as pd


cell_hover = {  # for row hover use <tr> instead of <td>
    'selector': 'td:hover',
    'props': [('background-color', '#ffffb3')]
}
index_names = {
    'selector': '.index_name',
    'props': 'font-style: italic; color: darkgrey; font-weight:normal;'
}
headers = {
    'selector': 'th:not(.index_name)',
    'props': 'background-color: #000066; color: white;'
}

secrets_path = "./.streamlit"
if not os.path.exists(secrets_path):
    # Create the directory
    os.makedirs(secrets_path)
    with open(f"{secrets_path}/secrets.toml", "w") as file:
        file.write("[connections.mariadb]\n")
        file.write('dialect = "mariadb"\n')
        file.write('host = "192.168.90.95"\n')
        file.write('port = 3306\n')
        file.write('database="mydatabase"\n')
        file.write('username="root"\n')
        file.write('password="password"')
        file.close()



# connection parameters
conn_params = {
    "user" : "user",
    "password" : "password",
    "host" : "192.168.90.95",
    "port" : 3306,
    "database" : "mydatabase"
}

# Establish a connection
connection_1 = mariadb.connect(**conn_params)
connection = st.experimental_connection('mariadb', type='sql')
cursor = connection_1.cursor()

#danas = datetime.date.today()
#danas = danas.strftime("%d.%m.%Y")

st.title('Administracija finansija')
sidebar = st.sidebar
with sidebar:

    datum = st.date_input("Unesite datum", format="DD.MM.YYYY")
    odabir_tabele = st.selectbox("Odaberite tabelu iz baze podataka", ("Promet", "Gorivo", "Servis", "Kazne", "Trošak"))

df = connection.query(f'SELECT * from {odabir_tabele};', ttl=600)
df = pd.DataFrame(df)
df.style.format('{:.0f}').set_table_styles([cell_hover, index_names, headers])

tabela = st.dataframe(data=df, use_container_width=True)

imena_kolona_query = f"""
SELECT COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'mydatabase'
    AND TABLE_NAME = '{odabir_tabele}';
"""
imena_kolona = connection.query(imena_kolona_query).values
lista_kolona = [imena_kolona[i][0] for i in range(len(imena_kolona))]
print(lista_kolona)

all_queries=[]
with sidebar:

    with st.container():
        st.header(f"Unesite podatke u tabelu {odabir_tabele}")
        with st.form("unos_podataka", clear_on_submit=True):
            for kol in lista_kolona:
                if kol == 'Datum':
                    unos = st.date_input("Unesite datum", format="DD.MM.YYYY")
                    unos_dict = {f"`{kol}`" : f"STR_TO_DATE{unos.strftime('%d.%m.%Y'), '%d.%m.%Y'}"}
                    all_queries.append(unos_dict)
                
                elif kol == 'Lokacija':
                    unos = st.selectbox(label="Lokacija", options=("BiH", "Inostranstvo"))
                    unos_dict = {f"`{kol}`" : f"'{unos}'"}
                    all_queries.append(unos_dict)
                
                elif kol == 'Plaćeno':
                    unos = st.selectbox(label="Plaćeno", options=("DA", "NE"))
                    unos_dict = {f"`{kol}`" : f"'{unos}'"}
                    all_queries.append(unos_dict)
                
                elif kol in ['Kilometraža', 'Iznos gotovina', 'Iznos žiralno', 'Utrošak goriva (L)', 'Cijena', 'Iznos']:
                    unos = st.number_input(kol)
                    unos_dict = {f"`{kol}`" : str(unos)}
                    all_queries.append(unos_dict)
                
                elif kol == 'Opis':
                    unos = st.selectbox(label="Lokacija", options=("Svakodnevni trošak", "Terminal", "Autoput", "Mostarina"))
                    unos_dict = {f"`{kol}`" : f"'{unos}'"}
                    all_queries.append(unos_dict)
                
                else:
                    unos = st.text_input(kol, "")
                    unos_dict = {f"`{kol}`" : f"'{unos}'"}
                    all_queries.append(unos_dict)
            
            key_strings = []
            value_strings = []
            for query in all_queries:
                key_strings.append(f"{', '.join(query.keys())}")
                value_strings.append(f"{', '.join(query.values())}")
            insert_query = f"INSERT INTO {odabir_tabele} ({', '.join(key_strings)}) VALUES ({', '.join(value_strings)});"
            
            submitted = st.form_submit_button("Potvrda")
            if submitted:
                cursor.execute(insert_query)
                connection_1.commit()
                cursor.close()
                connection_1.close()
            
