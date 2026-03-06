import os

# Set your paths
images_dir = r"C:/Users/.../Capstone/OIDv4_ToolKit/OID/Dataset/images"  # folder with all images
labels_dir = r"C:/Users/.../Capstone/OIDv4_ToolKit/OID/Dataset/labels"  # folder with all label txt files

def normalize_labels(images_dir, labels_dir):
    from PIL import Image

    for label_file in os.listdir(labels_dir):
        if not label_file.endswith(".txt"):
            continue

        label_path = os.path.join(labels_dir, label_file)
        image_name = label_file.replace(".txt", ".jpg")  # adjust if some images are png
        image_path = os.path.join(images_dir, image_name)

        if not os.path.exists(image_path):
            print(f"Warning: image not found for {label_file}, skipping.")
            continue

        # Open image to get size
        img = Image.open(image_path)
        w, h = img.size

        new_lines = []
        with open(label_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            parts = line.strip().split()
            if len(parts) < 5:
                print(f"Skipping malformed line in {label_file}: {line}")
                continue

            cls = parts[0]
            # assuming your labels are in absolute pixel format x1 y1 x2 y2
            x1, y1, x2, y2 = map(float, parts[1:5])

            # clip coordinates to image size
            x1 = max(0, min(x1, w))
            x2 = max(0, min(x2, w))
            y1 = max(0, min(y1, h))
            y2 = max(0, min(y2, h))

            # compute YOLO format
            x_center = (x1 + x2) / 2 / w
            y_center = (y1 + y2) / 2 / h
            width = (x2 - x1) / w
            height = (y2 - y1) / h

            # make sure everything is between 0 and 1
            x_center = min(max(x_center, 0), 1)
            y_center = min(max(y_center, 0), 1)
            width = min(max(width, 0), 1)
            height = min(max(height, 0), 1)

            new_lines.append(f"{cls} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

        # overwrite label file with normalized coordinates
        with open(label_path, "w") as f:
            f.writelines(new_lines)

    print("Labels fixed!")

if __name__ == "__main__":
    normalize_labels(images_dir, labels_dir)
