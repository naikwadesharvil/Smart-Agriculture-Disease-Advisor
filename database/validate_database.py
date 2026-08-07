import json

DATABASE_FILE = "disease_database.json"

EXPECTED_CLASSES = 38

try:
    with open(DATABASE_FILE, "r", encoding="utf-8") as file:
        database = json.load(file)

    print("=" * 60)
    print("DATABASE VALIDATION")
    print("=" * 60)

    print(f"\nTotal Database Entries : {len(database)}")

    if len(database) == EXPECTED_CLASSES:
        print(f"\n✅ All {EXPECTED_CLASSES} classes found.")
    else:
        print(f"\n❌ Expected {EXPECTED_CLASSES} classes.")
        print(f"Found {len(database)} classes.")

    print("\nChecking required fields...\n")

    required_fields = [
        "Crop",
        "Disease",
        "Scientific_Name",
        "Pathogen",
        "Pathogen_Type",
        "Category",
        "Affected_Part",
        "Environment",
        "Spread",
        "Description",
        "Cause",
        "Age_Cycle",
        "Symptoms",
        "Treatment",
        "Organic_Treatment",
        "Recommended_Chemicals",
        "Prevention",
        "Risk_Level",
        "Severity",
        "Recommended_Actions"
    ]

    missing = False

    for disease, info in database.items():

        for field in required_fields:

            if field not in info:
                missing = True
                print(f"{disease} --> Missing {field}")

    if not missing:
        print("✅ All required fields are present.")

except Exception as e:
    print(e)