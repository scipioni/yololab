import os
from PIL import Image
import xml.etree.ElementTree as ET

path = "C:/Users/CJ/Desktop/GOPR1716/clean_xml"
path2 = "C:/Users/CJ/Desktop/croppedImage"
path3 = "C:/Users/CJ/Desktop/filestxt"
xml_file_path = path+"/"+"GOPR1716_00000.xml"
txt_file_path = path3

folder = os.listdir(path)
isDif = True
i = 0

def reBounds():

    dim = [612,440,698,747]
    dimFin = [0,0,0,0]


    for i in range (0, len(dim)):

        if(i == 0 or i == 1):
            dimFin[i] = int(dim[i]*640/1920)

        if(i == 2 or i == 3):
            dimFin[i] = int(dim[i]*640/1080)
    

    print(dimFin)

def conv_xml_txt(fold):

    for entry in folder:

        
        try:
            # Carica il file XML
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            print(txt_file_path+"/"+entry[:-4]+".txt")
            # Apri il file di output in modalità scrittura
            with open(txt_file_path+"/"+entry[:-4]+".txt", 'w') as txt_file:
                # Itera su tutti gli elementi del file XML
                for element in root.iter():
                    # Ottieni il testo dell'elemento e scrivilo nel file di testo
                    text = element.text
                    if text:
                        txt_file.write(text + '\n')
            
            print(f"Il file XML è stato convertito correttamente in {txt_file_path}")
        except Exception as e:
            print("Si è verificato un errore durante la conversione:", str(e))


def crop(fold):

    for entry in folder:
    
        try:
            print(path2+"/"+entry)

            img = Image.open(path+"/"+entry)
            width, height = img.size
            
            if(width>640 and height>640):
                box = (640,220,1280,860)
                img2 = img.crop(box)       
                img2.save(path2+"/"+entry)
            
                
        except:

            print()
    

    
    #workbook = Workbook(path+"/"+"GOPR1716_00000.xml")
    #workbook.save(path2+"/GOPR1716_00000.xml")
