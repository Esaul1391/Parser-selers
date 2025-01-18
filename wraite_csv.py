import json
import csv

# Загрузка данных из JSON
with open("data_sellers.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Формирование данных для CSV
csv_rows = []
for name, info in data.items():
    reviews = info.get("reviews", [])
    # Форматируем каждую пару "объявление и количество"
    formatted_reviews = [f'"{title}, {count}"' for title, count in reviews]
    # Вставляем пустые ячейки между парами
    row = [name] + [item for pair in zip(formatted_reviews, [""] * len(formatted_reviews)) for item in pair]
    csv_rows.append(row)

# Запись данных в CSV
csv_file = "data_sellers.csv"
with open(csv_file, "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    for row in csv_rows:
        writer.writerow(row)

print(f"Данные успешно записаны в {csv_file}")
