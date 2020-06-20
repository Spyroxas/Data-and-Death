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
