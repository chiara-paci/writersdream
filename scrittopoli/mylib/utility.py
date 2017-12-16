import numpy
import random
import string

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

def random_title(x):
    size=random.randint(10,20)
    chars=string.ascii_lowercase +string.ascii_uppercase + string.digits
    chars+="               "
    S=''.join(random.choice(chars) for _ in range(size))
    S=S.strip()
    S=" ".join(S.split())
    return S

def random_len(x):
    return random.randint(300,8200)

def random_riserva(x):
    if random.choice([True,False]):
        return ""
    return "12-08 23:23"

def random_verifica(x):
    if random.choice([True,False,True,True,True,True,True,True,True,True,True]):
        return "x"
    return ""

def calc_penalita_lungh(x):
    return -int(x>8000)

def calc_penalita(x):
    if x: return 0
    return -1
