import os

LABEL_DIR = "OIDv4_ToolKit/OID/Dataset/labels"

CLASS_MAP = {
    "Box": 0,
    "Person": 1
}

for file in os.listdir(LABEL_DIR):

    if file.endswith(".txt"):

        path = os.path.join(LABEL_DIR, file)

        with open(path, "r") as f:
            lines = f.readlines()

        new_lines = []

        for line in lines:

            parts = line.strip().split()

            if len(parts) < 5:
                continue

            class_name = parts[0]

            if class_name not in CLASS_MAP:
                continue

            class_id = CLASS_MAP[class_name]

            coords = parts[1:]

            new_lines.append(f"{class_id} {' '.join(coords)}")

        with open(path, "w") as f:
            f.write("\n".join(new_lines))

print("DONE")