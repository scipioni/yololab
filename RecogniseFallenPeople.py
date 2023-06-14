import argparse
import shutil
import os

def check_folders(dpath):
    
    standing_exists = False
    fallen_exists = False

    for entry in os.listdir(dpath):
        
        if(entry=="standing" and os.path.isdir(dpath+"/"+entry)):
            
            standing_exists = True

        if(entry=="fallen" and os.path.isdir(dpath+"/"+entry)):
            
            fallen_exists = True

    if(not standing_exists):
        
        os.mkdir(dpath + "/standing")
    
    if(not fallen_exists):

        os.mkdir(dpath + "/fallen")

def discern_files(spath, dpath):

    is_standing=True

    for entry in os.listdir(spath):

        if os.path.isdir(spath+"/"+entry):
            discern_files(spath+"/"+entry, dpath)

        if(entry.endswith('txt')):
            
            pngfile = spath+"/"+entry[:-4]+".png"

            file = open(spath+"/"+entry, 'r')
            lines = file.readlines()

            for i in range (0, len(lines)):
                words = lines[i].split()

                if(words[0]=='1'):
                    
                    is_standing = False
            
            if(os.path.exists(pngfile)):
                if(not is_standing):
                    shutil.copyfile(pngfile, dpath+"/fallen/"+entry[:-4]+".png")
                    is_standing = True
                else:
                    shutil.copyfile(pngfile, dpath+"/standing/"+entry[:-4]+".png")
                        
    return

def main(spath, dpath):
    
    SPATH = spath
    DPATH = dpath

    check_folders(dpath)
    discern_files(spath, dpath)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Programma di esempio con argparse')
    parser.add_argument('-sp', '--spath', type=str, help='Indirizzo sorgente')
    parser.add_argument('-dp', '--dpath', type=str, help='Indirizzo di destinazione')

    args = parser.parse_args()
    spath = args.spath
    dpath = args.dpath

    if spath and dpath:
        main(spath, dpath)
    else:
        parser.print_help()