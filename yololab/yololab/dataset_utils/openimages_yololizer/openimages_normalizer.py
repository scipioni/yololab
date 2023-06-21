import argparse
import os
import glob

class Converter:
    def __init__(self, filename1: str, folder_path: str) -> None:
        self.classes = {"/m/01g317":0, "/m/03ssj5":1, "/m/03m3pdh":2}
        self.filename1 = filename1
        self.folder_path = folder_path
        os.makedirs(self.folder_path, exist_ok=True)

    def convert(self) -> None:
        data = self.read_data()
        self.process_data(data)

    def read_data(self) -> list:
        with open(self.filename1, "r") as file:
            lines = file.readlines()[1:]
        return lines

    def process_data(self, data: list) -> None:
        for line in data:
            line = line.strip().split(",")
            current_id = line[0]
            w = float(line[5]) - float(line[4])
            h = float(line[7]) - float(line[6])
            xc = float(line[5]) -  w / 2
            yc = float(line[7]) - h / 2

            try:
                _class = self.classes[line[2]]
                #print(_class, "kaka")
            except:
                print("skipped label, class not included")
                continue
            label = f"{_class} {xc} {yc} {w} {h}\n"
            self.write_data(current_id, label)

    def write_data(self, current_id: str, label: str) -> None:
        filename = os.path.join(self.folder_path, f"{current_id}.txt")
        with open(filename, "a") as file:
            file.write(label)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OpenImages to YOLO converter")
    parser.add_argument("--src", type=str, help="path to the input CSV file")
    parser.add_argument("--dst", type=str, help="path to the output directory")
    args = parser.parse_args()

    converter = Converter(args.src, args.dst)
    converter.convert()
