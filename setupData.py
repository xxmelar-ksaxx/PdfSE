from PIL import Image
from pytesseract import image_to_string
import csv
import os
from processing.pdf.pdfTpImg import pdfProcessor
import sys

class setup:

    BASE_PATH=os.path.abspath(".")
    ImagesPath = BASE_PATH+'\\processing\\pdf\\imgs\\' # save extracted images
    csvPath = BASE_PATH+'\\csv\\' # save extracted images

    Language='ara' # ara, eng

    # ImagesPath="pdf\\imgs\\"
    # csvPath="csv\\"
    
    def get_Imges_Count():
        f=[]
        for i in os.listdir(setup.ImagesPath):
            if (i[-3:-1]+i[-1])=="jpg":
                f.append(i)
        return len(f)
    
    NumOfFiles=0
    def __init__(self):

        # prepare pdf images
        prep_Pdf=pdfProcessor()
        prep_Pdf.start_process()
        print("")
        setup.NumOfFiles=setup.get_Imges_Count()

        # con=True
        # while(con):
        # setup.NumOfFiles=int(input("Enter Number of Questions to process. (Do not add number of Answers !!, Only Number of Questions):"))
        self.createCSVFile()
        self.ProcessAllRowQAPhotos()
        

    def createCSVFile(self):
        self.csvfile=open(f'{setup.csvPath}qadata.csv', 'w',encoding='UTF8')   # create the file
        self.writer = csv.writer(self.csvfile)   # csv writer 
        header = ['question','Answer']
        self.writer.writerow(header)

    def insertQA(self, q,a, counter):
        data=[q, a]
        # if not a:
        #     x=input(f"Answer not recognized for Question {counter}.\n Please enter the answer manually:")
        #     data=[q, x]
        self.writer.writerow(data)
    
    def ProcessAllRowQAPhotos(self):
        counter=1
        try:
            for i in range(setup.NumOfFiles):
                q=image_to_string(self.getQ(i+1),lang=setup.Language)
                a=i+1
                # print(f'res:{a}')
                self.update_CLI_Progress(i+1)
                self.insertQA(q,a,counter)
                counter+=1
            print("""######################################################\n
    #                                                     #\n
    #       Finished Processing Images successfully !!    #\n
    #                                                     #\n
    #######################################################""")
            input("Press any key to continue . . .")
            # return False
        except Exception as e:
            # print("Encounterded error in files count. Enter the correct number of Questions, try agin please...")
            print(e)
            input("Press any key to continue . . .")
            # return True
        
    
    def getQ(self, Pnumber):
        image=Image.open(f'{setup.ImagesPath}{(Pnumber)}.jpg')
        return image
    
    # def getA(self, Pnumber):
    #     image=Image.open(f'{setup.ImagesPath}a{(Pnumber)}.png')
    #     return image

    def update_CLI_Progress(self, progress):
        calc=round(((progress/setup.NumOfFiles)*100),1)
        print(f"Database building.. {calc}%", end="\r")
        sys.stdout.write("\033[F") # Cursor up one line


def main():
    print("Prepeare pdf...")
    if __name__== "__main__" :
        setup()
        

main()