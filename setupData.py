from PIL import Image
from pytesseract import image_to_string
import csv
import os
from pdfTpImg import pdfProcessor
import sys

class setup:

    BASE_PATH=os.path.abspath(".")
    csvPath = BASE_PATH+'\\csv\\' # save extracted images

    def __init__(self):

        self.language_selection()

        # prepare pdf images
        prep_Pdf=pdfProcessor()
        self.pdf_images=prep_Pdf.get_pdf_images()

        print("")

        self.createCSVFile()
        self.ProcessAllRowQAPhotos()
    
    def language_selection(self):
        # select processing language
        Languages={
            '1':'eng',
            '2':'ara'
        }
        self.Language='eng'
        while True:
            userSelection=Languages.get(input('Select prosessing language: 1-English, 2-Arabic\nEnter: '))
            if userSelection:
                self.Language=userSelection
                print(f"Language Selected: {self.Language}")
                break
            print("Wrong selection! Try again.")


    def createCSVFile(self):
        self.csvfile=open(f'{setup.csvPath}qadata.csv', 'w',encoding='UTF8')   # create the file
        self.writer = csv.writer(self.csvfile)   # csv writer 
        header = ['Q','A']
        self.writer.writerow(header)

    def insertQA(self, q,a):
        data=[q, a]
        self.writer.writerow(data)
    
    def ProcessAllRowQAPhotos(self):
        try:
            for k, v in enumerate(self.pdf_images):
                q=image_to_string(v,lang=self.Language)
                a=k+1
                self.update_CLI_Progress(k+1)
                self.insertQA(q,a)
            print("""######################################################\n
#      Finished Processing PDFs successfully !!    #\n
#######################################################""")
            input("Successful: Press any key to continue . . .")
        except Exception as e:
            print(e)
            input("err: Press any key to continue . . .")
        
    def update_CLI_Progress(self, progress):
        calc=round(((progress/len(self.pdf_images))*100),1)
        print(f"Database building.. {calc}%", end="\r")
        sys.stdout.write("\033[F") # Cursor up one line

def main():
    print("Prepeare pdf...")
    setup()

if __name__== "__main__" :
    main()