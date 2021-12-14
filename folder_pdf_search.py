#------------------------------------------------------------------------------------------------------------------------------------
in_folder = input("Enter folder containing PDFs to be searched:")
delimiter = "|" #@param ["|", ",", ";"]
Keywords = input("Enter words of interest separated by {}: ".format(delimiter))
out_folder = input("Optional: Enter folder in which to place file with keyword references: ")
#------------------------------------------------------------------------------------------------------------------------------------
from PDF_to_Text import pdf_to_text
from PDF_Text_Search import pull_keywords

import glob
import io
import os
import pandas as pd
import re
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


def pull_pdfs_folder(in_folder, keywords, out_path):
    out_df = pd.DataFrame(columns=['Keyword','Reference','File','Full Path'])
    not_read = []
    folder = os.listdir(in_folder)
    denom = len(glob.glob1(in_folder,"*.pdf"))
    count = 1
    for file in folder:
        if file[-4:] == '.pdf':
            pdf_in_folder = in_folder+file
            in_file = open(pdf_in_folder, 'rb')
            try:
                txt = pdf_to_text(in_file)
                results = pull_keywords(keywords=keywords, text = txt, filename = pdf_in_folder)
                out_df = out_df.append(results)
            except:
                print("This file was not read: ", pdf_in_folder)
                not_read.append(pdf_in_folder)
                pass
        count += 1
        if count%5 == 0:
            print(str(round((count/denom)*100,1))+ '% of PDFs have been processed.')
    if len(out_df)>0:
        out_df = out_df.sort_values(by=['Keyword'])
        out_df.to_csv(out_path, index=False)
    else:
        print('No keywords found in any of the documents.')
    if len(not_read)>0:
        print('The program failed to read these PDFs:')
        for i in not_read:
            print(i)


# # Structuring input parameters a bit
def folder_structuring(folder):
    # This should be done with os.path; will fix eventually
    folder = folder.replace('\\',"/")
    if len(folder)>0 and folder[-1] != '/':
        folder = folder + '/'
    return folder

if len(in_folder) == 0:
    print('-----------No input folder detected; enter one to run search---------')
    exit()

in_folder = folder_structuring(in_folder)

#set output file name and use user-designated path if applicable
user_out_path = folder_structuring(user_out_path)

if len(user_outfile)>0 and user_outfile[:-4] != '.csv':
    final_outfile = user_outfile+'.csv'

if len(user_outfile) == 0:
    final_outfile = Keywords[:30].replace(delimiter,'_').replace(' ','')+'.csv'

if len(user_out_path) == 0:
    final_out_path = in_folder
elif len(user_out_path) > 0:
    final_out_path = user_out_path

final_out_full = final_out_path+final_outfile

if len(Keywords) == 0:
    Keywords = ['marginal cost', 'endogenous growth']
    print('No keywords detected; setting to test keywords: ',Keywords)
elif isinstance(Keywords,list) == False:
    Keywords = Keywords.split(delimiter)

if ' ' in Keywords:
    Keywords.remove(' ')

pull_pdfs_folder(in_folder, keywords = Keywords, out_path=outname)
