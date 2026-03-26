import pandas as pd

# Încarcă fișierul combinat
df = pd.read_csv("Combined_Trainings.csv")

# Selectează coloanele necesare și elimină duplicatele
unique_participants = df[["Name", "Email_Participant"]].drop_duplicates()

# (Opțional) Sortează alfabetic după nume
unique_participants = unique_participants.sort_values("Name").reset_index(drop=True)

# Salvează într-un nou fișier CSV
unique_participants.to_csv("Unique_Participants.csv", index=False, encoding="utf-8")

print("Fisierul 'Unique_Participants.csv' a fost generat cu succes.")