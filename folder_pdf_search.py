#------------------------------------------------------------------------------------------------------------------------------------
in_folder = input("Enter folder containing PDFs to be searched:")
delimiter = "|" #@param ["|", ",", ";"]
Keywords = input("Enter words of interest separated by {}: ".format(delimiter))
out_folder = input("Optional: Enter folder in which to place file with keyword references: ")
#------------------------------------------------------------------------------------------------------------------------------------

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


def pull_keywords(keywords, text, filename):
    out_df = pd.DataFrame(columns=['Keyword','Reference','File','Full Path'])
    for keyword in keywords:
        k = keyword.lower()
        t = text.lower()
        res = [i.start() for i in re.finditer(k, t)]
        if len(res)==1:
            print('--'+keyword +' found '+str(len(res))+' time in '+str(filename.split('/')[-1]))
        elif len(res)>1:
            print('--'+keyword +' found '+str(len(res))+' times in '+str(filename.split('/')[-1]))
        for i in res:
            tmp = pd.DataFrame({'Keyword':[keyword],'Reference':[text[i-50:i+50].replace("\n"," ")],'File':[str(filename.split('/')[-1])],'Full Path':[filename]})
            out_df = out_df.append(tmp)
    return out_df


def pdf_to_text(in_file):
    output_string = io.StringIO()
    parser = PDFParser(in_file)
    doc = PDFDocument(parser)
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)
    text = output_string.getvalue()
    return text


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

#set output file name and use user-designated path if applicable
out_folder = folder_structuring(out_folder)
outname = out_folder+Keywords[:30].replace(delimiter,'_').replace(' ','')+'.csv'

if len(in_folder) == 0:
    print('-----------No input folder detected; enter one to run search---------')
    exit()

in_folder = folder_structuring(in_folder)

if len(Keywords) == 0:
    Keywords = ['marginal cost', 'endogenous growth']
    print('No keywords detected; setting to test keywords: ',Keywords)
elif isinstance(Keywords,list) == False:
    Keywords = Keywords.split(delimiter)

if ' ' in Keywords:
    Keywords.remove(' ')

pull_pdfs_folder(in_folder, keywords = Keywords, out_path=outname)
