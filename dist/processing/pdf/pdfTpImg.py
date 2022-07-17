##pip install pdf2image
# pdf to image
from  pdf2image import convert_from_path
from pathlib import Path
from os import walk
import os
from PIL import Image

class pdfProcessor:

  BASE_PATH=os.path.abspath(".")
  pdfs_dir=BASE_PATH+"\\pdfs\\"
  poppler_path=BASE_PATH+"\\processing\\pdf\\lib\\poppler-22.01.0\\Library\\bin"
  save_dir = BASE_PATH+'\\processing\\pdf\\imgs\\' # save extracted images

  def start_process(self):
    self.delete_old_Images()
    list,length=self.list_Of_Pdfs()
    self.process_all_pdfs(list,length)
    self.merge_images_onto_one_pdf()

    # print(f"res:{list}")
    # print(f"len:{length}")

  def delete_old_Images(self):
    # cleanup before starting
    for i in self.list_Of_Images():
      os.remove(pdfProcessor.save_dir+i)


  def list_Of_Pdfs(self):
    # return list of pdf files only, located in {pdfs} dir
    f=[]
    for i in os.listdir(pdfProcessor.pdfs_dir):
      if (i[-3:-1]+i[-1])=="pdf":
        f.append(i)
    return f ,len(f)
  
  def process_all_pdfs(self,pdfs_list,pdfs_count):
    # saved page count number stoped at..
    self.p_counter_stoped_at=0
    for i in pdfs_list:
      # pdf file location
      pdf_file=(pdfProcessor.pdfs_dir+i)
      # get pdf file to process
      images = convert_from_path(pdf_file,poppler_path=r''+pdfProcessor.poppler_path)
      # extract images from pdf file
      self.extract_imges(images,self.p_counter_stoped_at)
  
  def extract_imges(self, images, p_counter_start_at):
    for i in range(len(images)):
      # Save pages as images from the pdf to location (pdfProcessor.save_dir)
      images[i].save(Path(pdfProcessor.save_dir) / f'{str(p_counter_start_at+i+1)}.jpg', 'JPEG')
      self.p_counter_stoped_at+=1
  
  def merge_images_onto_one_pdf(self):
    images = [
    Image.open(pdfProcessor.save_dir + f)
    for f in (self.list_Of_Images())
    ]
    pdf_path = pdfProcessor.BASE_PATH+"/Search_File.pdf"
    images[0].save(
    pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
    )
  
  def list_Of_Images(self):
    # return list of jpg Images only, located in {processing\pdf\imgs} dir
    f=[]
    f2=[]
    for i in os.listdir(pdfProcessor.save_dir):
      if (i[-3:-1]+i[-1])=="jpg":
        f.append(i.replace('.jpg',''))
    f.sort(key = int)
    for i in f:
      f2.append(i+'.jpg')
    return f2

  
       

# x=pdfProcessor()
# x.start_process()


# p=os.path.abspath(".")
# # pp=next(os.walk(p))

# xp=os.listdir(p+'\\pdfs')

# print(xp)




# # image output dir
# save_dir = Path('pdf\\imgs')

# # saved page number stoped at..
# p_counter=0


# # images = convert_from_path('pdf\\SO1.pdf',poppler_path=r'C:\\Program Files\\poppler-22.01.0\\Library\\bin', output_folder=out_Path)

# # (pdf file read path, poppler_path - the path for a required library )

# images = convert_from_path('pdf\\SO1.pdf',poppler_path=r'pdf\\lib\\poppler-22.01.0\\Library\\bin')
# for i in range(len(images)):
#     # Save pages as images from the pdf
#     images[i].save(save_dir / f'{str(i+1)}.jpg', 'JPEG')