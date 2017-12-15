import numpy

def cell_val(val):
    if type(val) is int:
        return "<td style='text-align:center;'>%d</td>" % val
    if type(val) in [float,numpy.float64]:
        return "<td style='text-align:center;'>%.2f</td>" % val
    return "<td style='text-align:center;'>%s</td>" % val
        
def to_table_html(df,with_index=False):
    print("<table style='margin:auto;' border='1' width='90%'>")
    if with_index:
        print("<tr><th>&nbsp;</th>")
    c_list=[]
    for col in df.columns:
        print("<th>%s</th>" % col)
        c_list.append(col)
    print("</tr>")
    for r in range(len(df)):
        print("<tr>")
        if with_index:
            print("<th>%s</th>" % df.index[r])
        for c in c_list:
            print(cell_val(df.get_value(df.index[r],c)))                
        print("</tr>")
    print("</table>")

def calc_index_th(index,l,r):
    ind=index.labels[l][r]
    if (r>0) and (index.labels[l][r-1]==ind): return ""
    rowspan=0
    for q in range(r,len(index)):
        if ind != index.labels[l][q]: break
        rowspan+=1
    return "<th rowspan='%d'>%s</th>" % (rowspan,index.levels[l][ind])

def to_table_html_multi(df):
    print("<table style='margin:auto;' border='1' width='90%'>")
    for col in df.index.names:
        print("<th>%s</th>" % col)
    idx_L=len(df.index.levels)
    #print("<tr><th>&nbsp;</th>")
    c_list=[]
    for col in df.columns:
        print("<th>%s</th>" % col)
        c_list.append(col)
    print("</tr>")

    for r in range(len(df)):
        print("<tr>")
        for l in range(idx_L):
            th=calc_index_th(df.index,l,r)
            if th:
                print(th)
        for c in c_list:
            print(cell_val(df.get_value(df.index[r],c)))                
        print("</tr>")

    print("</table>")
