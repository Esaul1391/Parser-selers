import json

with open("data_sellersddd.json", "r", encoding="utf-8") as file:
    data = json.load(file)

result = []
for name, info in data.items():
    reviews = info.get("reviews", [])
    formatted_reviews = ", ".join([f'("{title}", {count})' for title, count in reviews])
    if formatted_reviews:
        result.append(f'{name}: {formatted_reviews}')

for num, line in enumerate(result, 1):
    print(num, line)
