import glob, os
import requests
import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px
import numpy as np
import pydeck as pdk
import time


def Traitement_df_Lieu_Naissance_egale_Lieu_Deces(df_base):
    df_traitee = df_base
    df_traitee = df_base[df_base["LIEU DECES"] == df_base["LIEU NAISSANCE"]]
    return df_traitee


def Traitement_df_mort_ne(df_base):
    df_traitee = df_base
    df_traitee = df_base[df_base["DATE DECES"] == df_base["DATE NAISSANCE"]]
    return df_traitee


def Traitement_df_nom(df_base, nom):
    df_traitee = df_base
    df_traitee = df_base[df_base["NOM"] == nom]
    return df_traitee


def Sexe(value):
    value = int(value)
    if value == 1:
        return "H"
    elif value == 2:
        return "F"


def Date(value):
    annee = value[0:4]
    mois = value[4:6]
    jour = value[6:8]
    if jour == "00": jour = "XX"
    return jour + "-" + mois + "-" + annee


def Recup_annee(date):  # format date DD-MM-AAAA
    annee = date[6:10]
    return annee


def Recup_mois(date):  # format date DD-MM-AAAA
    mois = date[3:5]
    return mois


def Recup_jour(date):  # format date DD-MM-AAAA
    jour = date[0:2]
    return jour


def Path_ID_lieu():
    path = r"C:\Users\yoann\PycharmProjects\myfirstproject\Projet_d'essai"
    s = glob.glob(os.path.join(path, '*.csv'))
    for files in s:
        if 'ID_lieu' in files:
            df_ID = pd.read_csv(files, ",")
        else:
            pass
    return df_ID


def Recherche_ID_lieu(value, df_lieu):
    for index in range(len(df_lieu)):
        if df_lieu['ID'][index] == value:
            return df_lieu['ville'][index]


def Recherche_path(value):
    path = r"C:\Users\yoann\PycharmProjects\myfirstproject\Projet_d'essai"
    s = glob.glob(os.path.join(path, '*.csv'))
    for files in s:
        if 'path_url' in files:
            df_ID = pd.read_csv(files, ",")
        else:
            pass
    for index in range(len(df_ID)):
        if df_ID['annee'][index] == value:
            return df_ID['path_URL'][index]


def Prog_df(date):
    pre_link = "https://static.data.gouv.fr/resources/fichier-des-personnes-decedees/"
    link = pre_link + Recherche_path(date)

    file = requests.get(link)
    filetext = file.text.split("\n")
    filetext1 = file.text

    longueur = len(filetext)

    nom_prenom_list = []
    inter_list = []
    nom_list = []
    prenom_inter_list = []
    prenom_list = []
    # naissance_list = []
    naissance_sexe_list = []
    naissance_date_list = []
    naissance_lieu_list = []
    # deces_list = []
    deces_date_list = []
    deces_lieu_list = []
    # deces_acte_list = []
    age_list = []

    try:
        for index in range(longueur - 1):
            nom_prenom_list.append(filetext[index][0:79])
            if '*' in nom_prenom_list[index]:
                inter_list.append(nom_prenom_list[index].split("*"))
            else:
                inter_list.append(["NAN", nom_prenom_list[index]])
            nom_list.append(inter_list[index][0])
            prenom_inter_list.append(inter_list[index][1].split("/"))
            prenom_list.append(prenom_inter_list[index][0])
            # naissance_list.append(filetext[index][80:153])
            naissance_sexe_list.append(Sexe(filetext[index][80:81]))
            naissance_date_list.append(Date(filetext[index][81:89]))
            naissance_lieu_list.append(filetext[index][89:94])
            # deces_list.append(filetext[index][154:175])
            deces_date_list.append(Date(filetext[index][154:162]))
            deces_lieu_list.append(filetext[index][162:167])
            # deces_acte_list.append(filetext[index][167:175])
            age_list.append((int(deces_date_list[index][6:10])) - (int(naissance_date_list[index][6:10])))

        # pd.set_option('display.max_rows', None, 'display.max_columns', None)
        df = pd.DataFrame()

        df['NOM'] = nom_list
        df['PRENOM'] = prenom_list
        # df['NAISSANCE'] = naissance_list
        df['SEXE'] = naissance_sexe_list
        df['DATE NAISSANCE'] = naissance_date_list
        df['LIEU NAISSANCE'] = naissance_lieu_list
        # df['DECES'] = deces_list
        df['DATE DECES'] = deces_date_list
        df['LIEU DECES'] = deces_lieu_list
        # df['ACTE DECES'] = deces_acte_list
        df['AGE'] = age_list

    except:
        print("Bug........")
        print("Defaut index :" + str(index) + " " + str(date))
        file2 = open(r"E:\Exemple.txt", "w")
        file2.write(filetext1)
        file2.close()
    return df


def Main_test(data_start, data_end, nom):
    df_result = pd.DataFrame()
    nb_year = data_end - data_start
    my_bar = st.progress(0)
    i_bar = 0
    for index in range(data_start, data_end):
        df_out = Prog_df(index)
        df_result = df_result.append(df_out)
        i_bar += 100/(data_end-data_start)
        my_bar.progress(int(i_bar))
        print("fini", index)

    pd.set_option('display.max_rows', None, 'display.max_columns', None)
    if nom != "":
        dft_name = Traitement_df_nom(df_result, nom)
    else:
        dft_name = df_result
    file1 = open(r"E:\Name1970.txt", "w")
    file1.write(str(dft_name))
    file1.close()
    return dft_name


def Recherche_mean_death(df, startsearch, nb_year):
    df_mean = pd.DataFrame()
    longueur_df = len(df.index)
    nb_death_list = []
    year_list = []
    age_mean_list = []
    for x in range(nb_year):
        year_actual = str(int(startsearch) + int(x))
        print(year_actual)
        nb_death = 0
        somme = 0
        mean = 0
        for data_index in range(longueur_df):
            if df["DATE DECES"][data_index][6:10] == str(year_actual):
                nb_death = nb_death + 1
                somme = somme + df["AGE"][data_index]
        if nb_death != 0:
            mean = round(somme / nb_death, 2)
        else:
            mean = "0"
        year_list.append(year_actual)
        nb_death_list.append(nb_death)
        age_mean_list.append(mean)
    df_mean['ANNEE'] = year_list
    df_mean['NOMBRE DE MORT'] = nb_death_list
    df_mean['AGE MOYEN'] = age_mean_list
    st.write(df_mean)
    c = alt.Chart(df_mean).mark_bar().encode(x = 'ANNEE', y = 'NOMBRE DE MORT', tooltip = ['ANNEE', 'NOMBRE DE MORT', 'AGE MOYEN'])
    f = alt.Chart(df_mean).mark_line().encode(x='ANNEE', y='AGE MOYEN', tooltip=['ANNEE', 'NOMBRE DE MORT', 'AGE MOYEN'])
    st.write(c)
    st.write(f)
    return df_mean


st.title("Programme of the dead")
st.write("Ici nous allons pour pouvoir voir les déplacements d'une famille :")
search_item = st.selectbox("Votre recherche",["Nom", "Prénom", "Age", "Lieu"])
var_search = st.text_input("")
var_search = var_search.upper()

# if st.checkbox('Plus de précision'):
#     if st.checkbox('Recherche sur le nom'):
#         nom = st.text_input(key=10, label="Inserer le nom de la personne :")
#         nom = nom.upper()
#     if st.checkbox('Recherche sur le prenom'):
#         prenom = st.text_input(key=11, label="Inserer le prenom de la personne :")
#         prenom = prenom.upper()
#     if st.checkbox('Recherche sur le lieu'):
#         lieu = st.text_input(key=12, label="Inserer le lieu de la personne :")
#         lieu.upper()

year_search = st.slider('Année de recherche', 1970, 2018, (1970, 1973))

if st.button("LANCER RECHERCHE"):
    if search_item == "Nom":
        df = Main_test(year_search[0], int(year_search[1]) + 1, str(var_search))
        df.reset_index(drop=True, inplace=True)
        cols = ["name", "host_name", "neighbourhood", "room_type", "price"]
        st.write(df)
        total_year_search = (int(year_search[1]) + 1) - year_search[0]
        df_mean = Recherche_mean_death(df, year_search[0], total_year_search)
        st.balloons()
    elif search_item == "Prénom":
        st.write("Cette partie du code n'est pas encore prête. Veuillez patienter...")
    elif search_item == "Age":
        st.write("Cette partie du code n'est pas encore prête. Veuillez patienter...")
    elif search_item == "Lieu":
        st.write("Cette partie du code n'est pas encore prête. Veuillez patienter...")
    else:
        st.write("Erreur...")