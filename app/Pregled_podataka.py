import streamlit as st
import yaml
import os
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
from filter_results import filter_results
from helpers import landing_page, engine_sqlalchemy, img, report_form

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

footer="""<style>
.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: right;
left: -40px;
}
</style>
<div class="footer">
<p>By <i>Marko Kajkut</i>, <i>markokajkut1@gmail.com</i> <a style='display: block; text-align: center;'</p>
</div>
"""


st.set_page_config(
    page_title="Pregled podataka",
    page_icon="📈",
    layout="wide",
)

if not os.path.exists(".streamlit/config.toml"):
    os.makedirs(".streamlit")
    with open(".streamlit/config.toml", "w") as file:
        file.write(
'''[theme]
secondaryBackgroundColor = "#E9F4FD"
'''
        )
    
st.markdown(footer,unsafe_allow_html=True)

if "authentication_status" not in st.session_state:
    st.session_state.authentication_status = None

if "logout" not in st.session_state:
    st.session_state.logout = True
    
if "report_generated_status" not in st.session_state:
    st.session_state.report_generated_status = False

# Konfiguracija login forme i autentifikacije
with open(f'{parent_dir}/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    credentials=config.get('credentials'),
    cookie_name=config.get('cookie').get('name'),
    key=config.get('cookie').get('key'),
    cookie_expiry_days=float(config.get('cookie').get('expiry_days'))
)
name, authentication_status, username = authenticator.login('Prijavite se', 'sidebar')


administracija_engine = engine_sqlalchemy("DB_ADMINISTRACIJA")

def main():
    
    # Logo
    img()
    
    st.title('Administracija finansija')
    st.subheader("Pregled podataka")
    st.write("---")

    with st.sidebar:
        st.subheader("Odabir tabele")
        odabir_tabele = st.selectbox("Odaberite tabelu iz baze podataka", ("Promet", "Gorivo", "Servis-Gume-Registracija", "Kazne", "Trošak"))
        st.info(f"Odabrali ste tabelu {odabir_tabele}.")
    
    with administracija_engine.connect() as administracija_connection:
        st.subheader(f"{odabir_tabele}")
        filter_results(odabir_tabele, administracija_connection)
        
    # Reporting form
    report_form()
    
# Ulogovan                   
if st.session_state["authentication_status"]:
    authenticator.logout('Odjavite se', 'sidebar')
    main()
# Izlogovan - netacni kredencijali
elif st.session_state["authentication_status"] is False:
    landing_page()
    with st.sidebar:
        st.error('Korisničko ime ili lozinka netačni.')
# Izlogovan
elif st.session_state["authentication_status"] is None:
    landing_page()
    with st.sidebar:
        st.warning('Unesite kredencijale za prijavu.')

