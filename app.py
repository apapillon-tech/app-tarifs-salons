import streamlit as st
import pandas as pd

# Configuration de la page pour les mobiles
st.set_page_config(page_title="Tarifs Salons", page_icon="📱", layout="centered")

def load_data():
    # Lecture de votre fichier Excel nettoyé
    df = pd.read_excel("fixed.xlsx")
    # Suppression des lignes vides sans désignation
    df = df.dropna(subset=['Désignation 2025 FDL'])
    return df

# Chargement des données
try:
    df = load_data()
except Exception as e:
    st.error("Erreur lors de la lecture du fichier Excel. Assurez-vous que le fichier se nomme bien 'fixed.xlsx'.")
    st.stop()

st.title("📱 Tarifs Foires & Salons")

# 1. Champ de recherche par mots-clés
st.write("### 1. Recherche")
search_term = st.text_input("🔍 Entrez un ou plusieurs mots-clés (ex: Plateau 30) :")

if search_term:
    # Découpage de la recherche en plusieurs mots-clés pour une recherche plus souple
    keywords = search_term.lower().split()
    
    # Filtrage : la ligne doit contenir TOUS les mots-clés saisis
    mask = pd.Series([True] * len(df), index=df.index)
    for kw in keywords:
        mask = mask & df['Désignation 2025 FDL'].str.lower().str.contains(kw, na=False)
        
    df_filtered = df[mask]
    
    if df_filtered.empty:
        st.warning("Aucune désignation trouvée pour ces mots-clés. Essayez d'autres termes.")
    else:
        # 2. Sélection de la désignation exacte
        st.write("### 2. Sélection")
        options = df_filtered['Désignation 2025 FDL'].tolist()
        selected_designation = st.selectbox(
            f"🎯 Choisissez parmi les {len(options)} résultats correspondants :", 
            options
        )
        
        # 3. Affichage des détails pour la désignation sélectionnée
        if selected_designation:
            # Récupération de la ligne exacte
            row = df_filtered[df_filtered['Désignation 2025 FDL'] == selected_designation].iloc[0]
            
            st.divider()
            
            # Affichage de la désignation et du freinage
            st.markdown(f"#### {row['Désignation 2025 FDL']}")
            st.caption(f"Freinage : {row['Freinage'] if pd.notna(row['Freinage']) else 'Non spécifié'}")
            
            # Affichage des prix en gros et bien visibles
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"**Vente Agriculteur**\n\n### {row['Prix de vente agriculteur']} €")
            with col2:
                st.info(f"**Port Indicatif**\n\n### {row['Port indicatif']} €")
                
            # Affichage du prix net foire en très petit, discret, tout en bas
            st.markdown(
                f"<div style='text-align: center; font-size: 10px; color: #d3d3d3; margin-top: 30px;'>"
                f"Prix net foire (confid.) : {row['Prix net distributeur foire']} €"
                f"</div>", 
                unsafe_allow_html=True
            )
else:
    st.info("Saisissez des mots-clés ci-dessus pour commencer la recherche.")