import os
import json

DATABASE_FOLDER = os.path.dirname(os.path.abspath(__file__))

OUTPUT_FILE = os.path.join(
    DATABASE_FOLDER,
    "disease_database.json"
)

IGNORE_FILES = {
    "merge_database.py",
    "disease_database.json"
}

merged_database = {}

duplicate_keys = []

print("=" * 60)
print("Merging Disease Database")
print("=" * 60)

for filename in sorted(os.listdir(DATABASE_FOLDER)):

    if not filename.endswith(".json"):
        continue

    if filename in IGNORE_FILES:
        continue

    filepath = os.path.join(
        DATABASE_FOLDER,
        filename
    )

    print(f"Loading {filename}")

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

    except json.JSONDecodeError as e:
        print(f"\n❌ JSON Error in: {filename}")
        print(e)
        exit()

    for key, value in data.items():

        if key in merged_database:

            duplicate_keys.append(key)

        merged_database[key] = value

print()

print(f"Total Disease Classes : {len(merged_database)}")

if duplicate_keys:

    print()

    print("Duplicate Keys Found:")

    for key in duplicate_keys:

        print("-", key)

else:

    print("No duplicate keys found.")

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as outfile:

    json.dump(
        merged_database,
        outfile,
        indent=4,
        ensure_ascii=False
    )

print()

print("Database successfully created!")

print(OUTPUT_FILE)