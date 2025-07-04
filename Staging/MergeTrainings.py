import os
import pandas as pd
from io import StringIO

trainings_path = "Raw_Trainings"
output_rows = []

for idx, filename in enumerate(sorted(os.listdir(trainings_path))):
    if filename.endswith(".csv"):
        file_path = os.path.join(trainings_path, filename)
        session_tag = f"Training{idx + 1}"
        
        # Citește conținutul brut pentru a identifica secțiunea "2. Participants"
        with open(file_path, "r", encoding="utf-16") as f:
            lines = f.readlines()

        # Identifică secțiunea între "2. Participants" și prima linie cu celulă goală
        start_index = None
        for i, line in enumerate(lines):
            if line.strip().startswith("2. Participants"):
                start_index = i
                break

        if start_index is None:
            print("⚠️ Nu s-a găsit secțiunea '2. Participants' în fișierul:", filename)
            continue  # Nu s-a găsit secțiunea

        # Caută antetul și apoi datele
        header_index = start_index + 1  # Antetul este imediat după "2. Participants"

        data_lines = []
        for line in lines[header_index:]:
            if line.strip() == "" or line.startswith("\t"):
                break
            data_lines.append(line)

        # Scrie aceste linii într-un buffer temporar CSV
        temp_csv = StringIO("".join(data_lines))

        # Încarcă în pandas folosind tab separator
        df = pd.read_csv(temp_csv, sep="\t")

        # Curățare și selecție coloane
        df = df[["Name", "First Join", "Last Leave", "Email", "Role"]].copy()
        df.columns = ["Name", "First_Join", "Last_Leave", "Email_Participant", "Role"]
        df["Training_Session"] = session_tag

        output_rows.append(df)

if output_rows:
    combined_df = pd.concat(output_rows, ignore_index=True)
    combined_df.to_csv("Combined_Trainings.csv", index=False, encoding="utf-8")
    print("Fisierul final a fost salvat ca 'Combined_Trainings.csv'")
else:
    print("Nu s-a putut realiza mergeuirea fișierelor.")