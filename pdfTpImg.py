##pip install pdf2image
# pdf to image
from  pdf2image import convert_from_path
import os
import sys
class pdfProcessor:

  BASE_PATH=os.path.abspath(".")
  pdfs_dir=BASE_PATH+"\\pdfs\\"
  poppler_path=BASE_PATH+"\\lib\\poppler-22.01.0\\Library\\bin"

  def get_pdf_images(self) -> list:
    '''
      Extracts pdf file pages as images.
      Extraxtion from multiple files can happen
      
      return a list of images
    '''
    self.allImagesList=[]

    pdfNames=self.pdf_names()
    self.extract_images_from_all_pdfs(pdfNames)
    self.merge_images_onto_one_pdf()

    return self.allImagesList

  def pdf_names(self) -> list:
    # return list of pdf files only, located in {pdfs} dir
    f=[]
    for i in os.listdir(pdfProcessor.pdfs_dir):
      if (i[-3:-1]+i[-1])=="pdf":
        f.append(i)
    return f
  
  def extract_images_from_all_pdfs(self,pdfNames):
    self.files_Counter=1
    # saved page count number stoped at..
    self.p_counter_stoped_at=0
    for i in pdfNames:
      # pdf file location
      pdf_file=(pdfProcessor.pdfs_dir+i)
      # get pdf file to process
      images = convert_from_path(pdf_file,poppler_path=r''+pdfProcessor.poppler_path)
      self.allImagesList+=images

      # progress clalculation
      self.update_CLI_Progress(len(pdfNames))
  
  def merge_images_onto_one_pdf(self):
    pdf_path = pdfProcessor.BASE_PATH+"/Search_File.pdf"
    self.allImagesList[0].save(
    pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=self.allImagesList[1:]
    )
  
  def update_CLI_Progress(self, overallCount):
        calc=round(((self.files_Counter/overallCount)*100),1)
        print(f"Pdf Preparing... {calc}%", end="\r")
        sys.stdout.write("\033[F") # Cursor up one line
        self.files_Counter+=1