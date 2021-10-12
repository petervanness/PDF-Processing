def pull_keywords(keywords, text, filename):
    out_df = pd.DataFrame(columns=['Keyword','Reference','File'])
    for keyword in keywords:
        k = keyword.lower()
        t = text.lower()
        res = [i.start() for i in re.finditer(k, t)]
        if len(res)>0:
            print(keyword +' found '+str(len(res))+' time(s) in '+str(filename))
        for i in res:
            tmp = pd.DataFrame({'Keyword':[keyword],'Reference':[text[i-100:i+100].replace("\n"," ")],'File':[filename]})
            out_df = out_df.append(tmp)
    return out_df
