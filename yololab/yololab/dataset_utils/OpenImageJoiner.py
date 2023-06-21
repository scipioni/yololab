import glob
import os
import argparse

class OpenImageJoiner():
    def __init__(self) -> None:
        pass

    def browseDir(self, pDir, bDir, sDir):
        for file in glob.glob(os.path.join(pDir, '*.txt')):
            if os.path.exists(os.path.join(sDir, os.path.basename(file))) and os.path.exists(os.path.join(bDir, os.path.basename(file))):
                print('ciao')
                self.joinLabel2(file, sDir, bDir)
            else:    
                if os.path.exists(os.path.join(sDir, os.path.basename(file))):
                    self.joinLabel1(file, sDir)
                if os.path.exists(os.path.join(bDir, os.path.basename(file))):
                    self.joinLabel1(file, bDir)
                    
                        
    def joinLabel1(self, file, dir):
        newLabel = []

        with open(file) as f:
            for line in f.readlines():
                newLabel.append(line.strip())
                print(newLabel)
        f.close()

        with open(os.path.join(dir, os.path.basename(file))) as d:
            for line in d.readlines():
                newLabel.append(line.strip())
                print(newLabel)
        d.close()

        with open(os.path.join('newLabels', os.path.basename(file)), 'w') as l:
            newLabel = '\n'.join(newLabel)
            l.write(newLabel)


    def joinLabel2(self, file, dir1, dir2):
        newLabel = []

        with open(file) as f:
            for line in f.readlines():
                newLabel.append(line.strip())
                print(newLabel)
        f.close()

        with open(os.path.join(dir1, os.path.basename(file))) as d1:
            for line in d1.readlines():
                newLabel.append(line.strip())
                print(newLabel)
        d1.close()

        with open(os.path.join(dir2, os.path.basename(file))) as d2:
            for line in d2.readlines():
                newLabel.append(line.strip())
                print(newLabel)
        d2.close()

        with open(os.path.join('newLabels', os.path.basename(file)), 'w') as l:
            newLabel = '\n'.join(newLabel)
            l.write(newLabel)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--pdir', default='person')
    parser.add_argument('--bdir', default='bed')
    parser.add_argument('--sdir', default='sofa')
    parser.add_argument('--ldir', default='newLabels')
    args = parser.parse_args()
    join = OpenImageJoiner().browseDir(args.pdir, args.bdir, args.sdir)
