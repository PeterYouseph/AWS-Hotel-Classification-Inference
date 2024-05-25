import csv
import json

def json_to_csv(json_data, csv_file):
    # Extrair as chaves do primeiro objeto para usar como cabeçalhos do CSV
    headers = json_data[0].keys() if json_data else []

    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(json_data)

# Exemplo de uso
json_data = [
    {"Name": "John", "Age": 30, "City": "New York"},
    {"Name": "Alice", "Age": 25, "City": "Los Angeles"},
    {"Name": "Bob", "Age": 35, "City": "Chicago"}
]

csv_file = "output.csv"
json_to_csv(json_data, csv_file)
print("Conversão de JSON para CSV concluída.")
