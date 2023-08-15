import numpy as np
from PIL import ImageDraw
from PIL import Image
from matplotlib import gridspec, pyplot as plt

def main2():
    add_patient_history = {
          "patient_id": 1,
          "comment": "test-comment",
          "date": "test_date",
          "history_neutral_network": {
             "photo_original": "dddd",
             "photo_predict": "sdfsdfsdf",
             "annotations": [
                {
                   "area": 264.0,
                   "bbox": "213,123,123,33",
                   "segmentation": "[1,2,3,4,5,6,11,22,fff]",
                   "category_id": 2
                }
             ]
          }
    }

    polygon = [76.0, 196.0, 143.0, 68.0, 208.0, 202.0, 76.0, 196.0]
    train_mask = np.zeros((512, 512, 3), dtype=np.uint8)
    img = Image.fromarray(train_mask)
    ImageDraw.Draw(img).polygon(polygon, fill="#ffffff", outline='white')
    plt.imshow(img)
    plt.show()

def compare_versions(version1, version2):
    v1 = version1.split('.')
    v2 = version2.split('.')

    for i in range(len(v1)):
        if int(v1[i]) < int(v2[i]):
            return True
        elif int(v1[i]) > int(v2[i]):
            return False

    return False

if __name__ == '__main__':
    expressions = [
        {"v1": "1.2.2", "v2": "1.2.0002"},
        {"v1": "1.2.2", "v2": "1.2.003"},
        {"v1": "1.2.2", "v2": "2.0.0"},
        {"v1": "1.0.0", "v2": "2.0.0000"},
        {"v1": "1.2.2", "v2": "1.99.99"},
        {"v1": "1.99.99", "v2": "2.0.0"},
        {"v1": "2.0.99", "v2": "2.1.1"},
        {"v1": "99.26.27", "v2": "25.26.28"},
        {"v1": "111.33.2224", "v2": "786.26.28"},
        {"v1": "2312.44.27", "v2": "44.26.444"},
        {"v1": "22.26.533", "v2": "004.26.28"},
        {"v1": "55.21.123", "v2": "1.11.11"},
        {"v1": "22.66.123", "v2": "1.22.33"},
        {"v1": "99.12.345", "v2": "12.34.56"},
        {"v1": "45.22.1111", "v2": "123.34.56"},
        {"v1": "20.20.2020", "v2": "1.2.3"},
        {"v1": "1.1.1", "v2": "1.2.3"},
        {"v1": "10.20.30", "v2": "1.2.3"},
        {"v1": "5.5.5", "v2": "5.10.15"},
        {"v1": "7.6.5", "v2": "7.9.12"},
        {"v1": "9.8.7", "v2": "9.8.8"},
        {"v1": "15.15.15", "v2": "16.16.16"},
        {"v1": "5.4.3", "v2": "5.4.4"},
        {"v1": "6.5.4", "v2": "6.5.3"},
        {"v1": "7.6.8", "v2": "7.6.8"},
        {"v1": "6.5.6", "v2": "6.5.5"},
        {"v1": "4.3.2", "v2": "4.3.2"},
        {"v1": "2.2.2", "v2": "2.2.2"},
        {"v1": "3.3.3", "v2": "3.3.3"},
        {"v1": "9.9.9", "v2": "10.10.10"},
        {"v1": "8.7.6", "v2": "8.7.6"}
    ]

    for expression in expressions:
        version1 = expression['v1']
        version2 = expression['v2']
        result = compare_versions(version1, version2)

        print(f'{version1} < {version2}: {result}')
