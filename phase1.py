import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Charger les données
st.header("1. Charger les Données")
df = pd.read_csv('AmesHousing.csv')
st.write(df.head())

# Afficher les informations sur le DataFrame
st.header("2. Informations sur le DataFrame")
buffer = st.empty()
df_info = df.info(buf=buffer)
st.text(buffer.text)

# Afficher des statistiques descriptives
st.header("3. Statistiques Descriptives")
st.write(df.describe(include='all'))

# Nettoyage des Données
st.header("4. Nettoyage des Données")

# Nettoyer les noms des colonnes en supprimant les espaces et les caractères invisibles
df.columns = df.columns.str.strip()

# Calculer le nombre de valeurs manquantes par colonne
st.subheader("Valeurs Manquantes")
st.write(df.isnull().sum())

# Imputer les valeurs manquantes avec la médiane pour les colonnes numériques
df.fillna(df.median(numeric_only=True), inplace=True)

# Conversion de la colonne 'Year Built' en numérique
df['Year Built'] = pd.to_numeric(df['Year Built'], errors='coerce')

# Détection des Valeurs Aberrantes
st.header("5. Détection des Valeurs Aberrantes")

# Calculer les quartiles et l'IQR pour la colonne 'SalePrice'
Q1 = df['SalePrice'].quantile(0.25)
Q3 = df['SalePrice'].quantile(0.75)
IQR = Q3 - Q1

# Définir les bornes pour les valeurs aberrantes
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Identifier les valeurs aberrantes
outliers = df[(df['SalePrice'] < lower_bound) | (df['SalePrice'] > upper_bound)]
st.subheader("Valeurs Aberrantes")
st.write(outliers)

# Visualisation des valeurs aberrantes pour 'SalePrice' avec un histogramme
st.subheader("Distribution des Prix de Vente")
fig, ax = plt.subplots()
df['SalePrice'].plot(kind='hist', bins=50, edgecolor='k', alpha=0.7, ax=ax)
ax.set_title('Distribution des Prix de Vente')
ax.set_xlabel('Prix de Vente')
ax.set_ylabel('Fréquence')
st.pyplot(fig)

# Ingénierie des Fonctionnalités
st.header("6. Ingénierie des Fonctionnalités")

# Ajouter une fonctionnalité pour la différence d'année de construction
df['Age'] = df['Yr Sold'] - df['Year Built']

# Création de variables indicatrices pour les colonnes catégorielles
df_encoded = pd.get_dummies(df, columns=['Neighborhood', 'House Style'])

st.subheader("DataFrame Encodé")
st.write(df_encoded.head())
