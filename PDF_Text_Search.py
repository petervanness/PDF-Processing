def pull_keywords(keywords, text, filename):
    out_df = pd.DataFrame(columns=['Keyword','Reference','File'])
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
