# -*- coding: utf-8 -*-

import httplib2shim
import httplib2
import os
import os.path
import collections
import pandas

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import sys
import urllib,string

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
#SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = '/home/chiara/ticonzero/etc/client_secret.apps.googleusercontent.com.json'
GAPPLICATION_NAME = 'Ti con zero'

class Spreadsheet(object):
    spreadsheetId = ''

    black={
        "blue": 0.0,
        "red": 0.0,
        "green": 0.0,
        "alpha": 1.0,
    }

    white={
        "blue": 1.0,
        "red": 1.0,
        "green": 1.0,
        "alpha": 1.0,
    }

    grey={
        "blue": 1,
        "red": 1,
        "green": 1,
        "alpha": .10,
    }

    yellow_light={
        "red":   1.0,
        "green": 1.0,
        "blue":  .9,
        "alpha": 1.0,
    }

    yellow={
        "red":   1.0,
        "green": 1.0,
        "blue":  .75,
        "alpha": 1.0,
    }

    yellow_dark={
        "red":   1.0,
        "green": 1.0,
        "blue":  .4,
        "alpha": 1.0,
    }

    green_light={
        "red": 0.9,
        "green": 1.0,
        "blue": 0.85,
        "alpha": 1.0,
    }

    green={
        "red": 0.7,
        "green": 1.0,
        "blue": 0.65,
        "alpha": 1.0,
    }

    green_dark={
        "red": 0.35,
        "green": 1.0,
        "blue": 0.3,
        "alpha": 1.0,
    }

    blue_light={
        "red": 0.9,
        "green": .9,
        "blue": 1,
        "alpha": 1.0,
    }

    blue={
        "red": 0.7,
        "green": .7,
        "blue": 1,
        "alpha": 1.0,
    }

    blue_dark={
        "red": 0.35,
        "green": .35,
        "blue": 1.0,
        "alpha": 1.0,
    }

    red={
        "red":   1.0,
        "green": .75,
        "blue":  .75,
        "alpha": 1.0,
    }

    red_light={
        "red":   1.0,
        "green": .9,
        "blue":  .9,
        "alpha": 1.0,
    }

    red_dark={
        "red":   1.0,
        "green": .35,
        "blue":  .35,
        "alpha": 1.0,
    }

    none_color={
        "red": 0,
        "green": 0,
        "blue": 0,
        "alpha": 0,
    }

    black_line={
        "style": "SOLID",
        "width": 1,
        "color": black,
    }

    white_line={
        "style": "SOLID",
        "width": 1,
        "color": white,
    }

    none_line={
        "style": "NONE",
        "width": 0,
        "color": none_color,
    }

    grey_line={
        "style": "SOLID",
        "width": 1,
        "color": grey,
    }
    
    bold_text={
        "foregroundColor": black,
        "fontFamily": "Courier New",
        "fontSize": 10,
        "bold": True
    }

    normal_text={
        "fontFamily": "Courier New",
        "foregroundColor": black,
        "fontSize": 10,
        "bold": False
    }

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'sheets.googleapis.com-python-ticonzero.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = GAPPLICATION_NAME
            credentials = tools.run_flow(flow, store, None)
            print('Storing credentials to ' + credential_path)
        return credentials
    
    def __init__(self,proxy=""):
        credentials = self.get_credentials()
        if proxy:
            pi = httplib2.proxy_info_from_url(proxy)
            http=httplib2shim.Http(proxy_info=pi)
        else:
            http = credentials.authorize(httplib2shim.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        self.service = discovery.build('sheets', 'v4', http=http,
                                       discoveryServiceUrl=discoveryUrl)

        self.spreadsheets=self.service.spreadsheets()
        self.values=self.spreadsheets.values()

        result = self.spreadsheets.get(spreadsheetId=self.spreadsheetId).execute()

        self.sheets_id={}
        for obj in result.get("sheets"):
            key=obj["properties"]["title"]
            self.sheets_id[key]=obj["properties"]["sheetId"]

    def _cell(self,row,column):
        C=chr(ord("a")+column)
        return C+str(row+1)

    def _c_range(self,sheet,row_s,row_e,col_s,col_e):
        c_range= {
            "sheetId": self.sheets_id[sheet],
            "startRowIndex": row_s,
            "endRowIndex": row_e+1,
            "startColumnIndex": col_s,
            "endColumnIndex": col_e+1
        }
        return c_range


    def _get_data(self,rangedef):
        result = self.values.batchGet(spreadsheetId=self.spreadsheetId, 
                                      majorDimension="ROWS",
                                      ranges=rangedef).execute()
        values=result.get("valueRanges")[0]["values"]
        return values

    def _clear_sheet(self,rangedef):
        body={
            "ranges": [ rangedef ]
        }
        result = self.values.batchClear(spreadsheetId=self.spreadsheetId,body=body).execute()
        return result

    def _req_merge(self,sheet,row_s,row_e,col_s,col_e):
        r=self._c_range(sheet,row_s,row_e,col_s,col_e)
        ret={ "mergeCells": {
            "range": r,
            "mergeType": "MERGE_ALL"
        }}
        return ret

    def _req_unmerge(self,sheet,row_s,row_e,col_s,col_e):
        r=self._c_range(sheet,row_s,row_e,col_s,col_e)
        ret={ "unmergeCells": {
            "range": r,
        }}
        return ret

    def _req_clear_borders(self,sheet,row_s,row_e,col_s,col_e):
        c_range=self._c_range(sheet,row_s,row_e,col_s,col_e)
        update={ "range": c_range }
        for key in ["top","left","right","bottom",
                    "innerVertical","innerHorizontal"]:
            update[key]=self.none_line
        return { "updateBorders": update }        


    def _req_autoresize_columns(self,sheet,col_s,col_e):
        req={
            "dimensions": {
                "sheetId": self.sheets_id[sheet],
                "dimension": "COLUMNS",
                "startIndex": col_s,
                "endIndex": col_e+1,
            }
        }
        return { "autoResizeDimensions": req }

    def _req_resize_columns(self,sheet,col_s,col_e,pixels):
        req={
            "range": {
                "sheetId": self.sheets_id[sheet],
                "dimension": "COLUMNS",
                "startIndex": col_s,
                "endIndex": col_e+1,
            },
            "properties": {
                "pixelSize": pixels
            },
            "fields": "pixelSize"
        }
        return { "updateDimensionProperties": req }

    def _req_resize_rows(self,sheet,row_s,row_e,pixels):
        req={
            "range": {
                "sheetId": self.sheets_id[sheet],
                "dimension": "ROWS",
                "startIndex": row_s,
                "endIndex": row_e+1,
            },
            "properties": {
                "pixelSize": pixels
            },
            "fields": "pixelSize"
        }
        return { "updateDimensionProperties": req }


    def _req_border(self,sheet,row_s,row_e,col_s,col_e,**kwargs):
        # all=None,
        # inner=None,top_bottom=None,left_right=None,
        # outer=None,top=None,bottom=None,left=None,right=None,
        # inner_vert=None,inner_hor=None

        c_range=self._c_range(sheet,row_s,row_e,col_s,col_e)
        update={ "range": c_range }
        for key in ["top","left","right","bottom",
                    "innerVertical","innerHorizontal"]:
            if key in kwargs:
                update[key]=kwargs[key]

        for label,sel in [ ( "all", ["top","left","right","bottom",
                                     "innerVertical","innerHorizontal"]),
                           ( "outer", ["top","left","right","bottom"]),
                           ( "inner", ["innerVertical","innerHorizontal"]),
                           ( "top_bottom", ["top","bottom"]),
                           ( "left_right", ["left","right"]) ]:
            if label in kwargs:
                for key in sel:
                    update[key]=kwargs[label]
        return { "updateBorders": update }

    def _req_style(self,c_range,cell_format):
        fields=",".join(list(cell_format.keys()))
        ret={
            "repeatCell": {
                "range": c_range,
                "cell": {
                    "userEnteredFormat": cell_format
                },
                "fields": "userEnteredFormat("+fields+")"
            }
        }
        return ret

    def _req_format(self,sheet,row_s,row_e,col_s,col_e,cell_format):
        c_range=self._c_range(sheet,row_s,row_e,col_s,col_e)
        return self._req_style(c_range,cell_format)

    def _req_alignment(self,sheet,row_s,row_e,col_s,col_e,
                       vertical="TOP",horizontal="LEFT"):
        c_range=self._c_range(sheet,row_s,row_e,col_s,col_e)
        cell_format={
            "verticalAlignment": vertical.upper(),
            "horizontalAlignment": horizontal.upper()
        }

        return self._req_style(c_range,cell_format)

    def _req_delete_conditional_format(self,sheet,rule_id):
        req={
            'deleteConditionalFormatRule': {
                'index': rule_id,
                "sheetId": self.sheets_id[sheet],

            }
        }   
        return req

    def _req_conditional_format(self,sheet,row_s,row_e,col_s,col_e,condition,cell_format):
        c_range=self._c_range(sheet,row_s,row_e,col_s,col_e)

        rule= {
            'ranges': c_range,
            'booleanRule': {
                'format': {'textFormat': cell_format },
                'condition': {
                    'type': 'CUSTOM_FORMULA',
                    'values': [{'userEnteredValue': condition}]
                },
            },
        }

        req={
            'addConditionalFormatRule': {
                'index': 0,
                'rule': rule,
            }
        }   
        return req

    def _req_colors(self,sheet,row_s,row_e,col_s,col_e,
                    background,text_format=normal_text):
        c_range=self._c_range(sheet,row_s,row_e,col_s,col_e)
        cell_format={
            "backgroundColor": background,
            "textFormat": text_format,
        }

        return self._req_style(c_range,cell_format)

    def _req_clear_colors(self,sheet,row_s,row_e,col_s,col_e):
        return self._req_colors(sheet,row_s,row_e,col_s,col_e,background=self.white)

    def _req_body_data(self,sheet,data,first_cell="a1"):
        return {
            #"valueInputOption": "RAW",
            "valueInputOption": "USER_ENTERED",
            "data": [{
                "values": data,
                "majorDimension": "ROWS",
                "range": "%s!%s" % (sheet,first_cell)
            }]
        }

#############

class SetGiornataSheet(object):
    def __init__(self,spreadsheet,sheet_names):
        self._ss=spreadsheet
        self._names=sheet_names

        self.black_line={
            "style": "SOLID",
            "width": 3,
            "color": self._ss.black,
        }

        self.gray_line={
            "style": "SOLID",
            "width": 1,
            "color": self._ss.gray,
        }


    def _h_gironi(self,gironi):
        H=[]
        len_H=0
        for girone in gironi.columns:
            s_list=list(gironi[gironi[girone]!="(riposo)"][girone])
            H.append( (girone,s_list) )
            len_H+=len(s_list)
        return H,len_H

    def _headers(self,sheet,giornata,accoppiamenti,gironi,old_data):
        H,len_H=self._h_gironi(gironi)

        dati_base=["girone","partita","squadra","goal partita","capitano",
                   "riserva","ingresso riserva","titolari","titolo","goal match"]
        verifiche=["lunghezza","tag","link","link commento","commento valido","penalità"]
        
        len_D=len(dati_base)
        len_V=len(verifiche)

        num_cols=len_D+len_V+len_H
        num_rows=3

        headers=[ ["" for c in range(num_cols) ] for r in range(num_rows) ] 
        req_list=[]

        for c in range(len_D):
            headers[0][c]=dati_base[c]
            req_list.append(self._ss._req_merge(sheet,0,2,c,c))

        headers[0][len_D]="verifiche e penalità" 
        req_list.append(self._ss._req_merge(sheet,0,1,len_D,len_D+len_V-1))

        for c in range(len_V):
            headers[2][len_D+c]=verifiche[c]

        headers[0][len_D+len_V]="voti"
        req_list+=[
            self._ss._req_merge(sheet,0,0,len_D+len_V,num_cols-1),
            self._ss._req_border(sheet,0,0,len_D+len_V,num_cols-1,
                                 inner=self.black_line,outer=self.black_line),
        ]

        c=len_D+len_V
        for girone,s_list in H:
            headers[1][c]="Girone "+girone
            req_list+=[
                self._ss._req_merge(sheet,1,1,c,c+len(s_list)-1),
                self._ss._req_border(sheet,1,2,c,c+len(s_list)-1,
                                     inner=self.gray_line,outer=self.black_line),
            ]
            for squadra in s_list:
                headers[2][c]=squadra
                c=c+1


        h_format={
            "backgroundColor": self._ss.red,
            "verticalAlignment": "BOTTOM",
            "horizontalAlignment": "CENTER",
            "textFormat": self._ss.bold_text,
        }

        r_format=h_format.copy()
        r_format["textRotation"]= {
            "angle": 90,
        }


        req_list+=[
            self._ss._req_format(sheet,0,2,          0,            1,r_format),
            self._ss._req_format(sheet,0,2,          2,            2,h_format),
            self._ss._req_format(sheet,0,2,          3,            3,r_format),
            self._ss._req_format(sheet,0,2,          4,      len_D-1,h_format),
            self._ss._req_format(sheet,0,1,len_D,   num_cols-1,h_format),
            self._ss._req_format(sheet,2,2,len_D,   num_cols-1,r_format),

            self._ss._req_border(sheet,0,2,0,9,
                                 inner=self.gray_line,outer=self.black_line),
            self._ss._req_border(sheet,0,2,10,15,
                                 inner=self.gray_line,outer=self.black_line),

        ]

        return headers,req_list

    def _set_titolare(self,R,r,r_big,H,old_data,titolare):
        formula_penalita='=-5'
        formula_penalita+='+if(K%d<=8000,1,0)'
        formula_penalita+='+countif(L%d:O%d,"?*")'
        R[r][7]=titolare
        R[r][9]="=sum(P%d:AA%d)" % (r_big+r+1,r_big+r+1)
        R[r][15]=formula_penalita % (r_big+r+1,r_big+r+1,r_big+r+1)

        if old_data is None: return
        R[r][6]=old_data.loc[titolare]["base","ingresso riserva"]
        R[r][8]=old_data.loc[titolare]["base","titolo"]

        verifiche=["lunghezza","tag","link","link commento","commento valido"]
        for n in range(len(verifiche)):
            R[r][10+n]=old_data.loc[titolare]["verifiche",verifiche[n]]

        n=16
        for girone,s_list in H:
            for squadra in s_list:
                R[r][n]=old_data.loc[titolare][girone,squadra]
                n+=1

    def _data(self,sheet,num_cols,giornata,accoppiamenti,gironi,old_data):
        h_rows=3
        H,len_H=self._h_gironi(gironi)
        start_H=num_cols-len_H

        partite=collections.OrderedDict()
        for girone,partita in accoppiamenti.index.unique():
            if girone not in partite: partite[girone]=[]
            partite[girone].append(partita)
        partite=list(partite.items())

        t_format={
            #"backgroundColor": self._ss.red,
            "verticalAlignment": "MIDDLE",
            "horizontalAlignment": "LEFT",
            "textFormat": self._ss.normal_text,
        }

        c_format=t_format.copy()
        c_format["horizontalAlignment"]= "CENTER"

        d_format=t_format.copy()
        d_format["numberFormat"]={
            "type": "DATE",
            "pattern": "dd/mm hh:mm"
        }

        data=[]
        req_list=[]
        r_big=h_rows

        for girone,p_list in partite:
            nr=4*len(p_list)
            R=[ ["" for c in range(0,16) ]+[ "" for c in range(16,num_cols) ] for r in range(nr) ]
            R[0][0]=girone

            r=0
            for partita in p_list:
                R[r][1]=partita
                req_list.append(self._ss._req_merge(sheet,r_big+r,r_big+r+3,1,1))
                for n in [0,1]:
                    sq=accoppiamenti.loc[girone,partita].iloc[n]
                    R[r][2]=sq["squadra"]
                    R[r][4]=sq["capitano"]
                    R[r][5]=sq["riserva"]

                    self._set_titolare(R,r,r_big,H,old_data,sq["match 1"])
                    self._set_titolare(R,r+1,r_big,H,old_data,sq["match 2"])

                    R[r][3]="=J%d+J%d" % (r_big+r+1,r_big+r+2)

                    req_list+=[
                        self._ss._req_merge(sheet,r_big+r,r_big+r+1,2,2),
                        self._ss._req_merge(sheet,r_big+r,r_big+r+1,3,3),
                        self._ss._req_merge(sheet,r_big+r,r_big+r+1,4,4),
                        self._ss._req_merge(sheet,r_big+r,r_big+r+1,5,5),
                    ]

                    r+=2
            req_list+=[
                self._ss._req_merge(sheet,r_big,r_big+nr-1,0,0),
                self._ss._req_border(sheet,r_big,r_big+nr-1,0,9,
                                     inner=self.gray_line,outer=self.black_line),
                self._ss._req_border(sheet,r_big,r_big+nr-1,10,15,
                                     inner=self.gray_line,outer=self.black_line),
            ]

            c=start_H
            for g_col,s_list in H:
                nc=len(s_list)
                if g_col!=girone:
                    req_list.append(self._ss._req_border(sheet,r_big,r_big+nr-1,c,c+nc-1,
                                                         inner=self.gray_line,outer=self.black_line))
                    c+=nc
                    continue
                req_list+=[
                    self._ss._req_border(sheet,r_big,r_big+nr-1,c,c+nc-1,
                                         inner=self.gray_line,outer=self.black_line),
                    self._ss._req_colors(sheet,r_big,r_big+nr-1,c,c+nc-1,
                                         background=self._ss.gray), #,text_format=c_format),
                ]
                c+=nc
                continue

            data+=R
            r_big+=nr


        num_rows=h_rows+len(data)

        req_list+=[
            self._ss._req_format(sheet,h_rows,num_rows-1,0,1,c_format),
            self._ss._req_format(sheet,h_rows,num_rows-1,2,2,t_format),
            self._ss._req_format(sheet,h_rows,num_rows-1,3,3,c_format),
            self._ss._req_format(sheet,h_rows,num_rows-1,4,5,c_format),
            self._ss._req_format(sheet,h_rows,num_rows-1,6,6,d_format),
            self._ss._req_format(sheet,h_rows,num_rows-1,7,8,t_format),
            self._ss._req_format(sheet,h_rows,num_rows-1,9,num_cols-1,c_format),
        ]

        return data,req_list

    def _general_requests(self,sheet,num_rows,num_cols):
        req_list=[
            self._ss._req_autoresize_columns(sheet,0,num_cols-1),
            self._ss._req_resize_rows(sheet,3,num_rows-1,30),
            self._ss._req_resize_columns(sheet,0,1,30),
            self._ss._req_resize_columns(sheet,11,num_cols-1,30),
            self._ss._req_resize_columns(sheet,8,8,500),
            self._ss._req_resize_columns(sheet,3,3,60),
            self._ss._req_resize_columns(sheet,9,9,60),
            self._ss._req_resize_columns(sheet,10,10,60),
        ]
        return req_list

    def __call__(self,giornata,accoppiamenti,gironi,old_data): 
        sheet=self._names[giornata-1]

        headers,req_headers=self._headers(sheet,giornata,accoppiamenti,gironi,old_data)
        num_cols=len(headers[0])
        data,req_data=self._data(sheet,num_cols,giornata,accoppiamenti,gironi,old_data)
        D=headers+data
        num_rows=len(D)

        body=self._ss._req_body_data(sheet,D)
        result = self._ss._batch_update_values(body)

        req_list=[
            self._ss._req_unmerge(sheet,0,2*num_rows,0,2*num_cols),
        ]
        req_list+=req_headers
        req_list+=req_data
        req_list+=self._general_requests(sheet,num_rows,num_cols)

        body={
            "requests": req_list,
        }

        result = self._ss._batch_update_spreadsheets(body)


class SetGiornataFinaliSheet(object):
    def __init__(self,spreadsheet,sheet_names):
        self._ss=spreadsheet
        self._names=sheet_names

        self.black_line={
            "style": "SOLID",
            "width": 3,
            "color": self._ss.black,
        }

        self.gray_line={
            "style": "SOLID",
            "width": 1,
            "color": self._ss.gray,
        }


    # ok
    def _h_gironi(self,squadre_in_gioco,altre_squadre):
        H=[]
        len_H=0
        for partita in squadre_in_gioco.index.unique():
            s_list=list(squadre_in_gioco.loc[partita]["squadra"])
            H.append( (partita,s_list) )
            len_H+=len(s_list)
        H.append( ("non qualificate",altre_squadre) )
        len_H+=len(altre_squadre)
        return H,len_H

    # ok
    def _headers(self,sheet,giornata,accoppiamenti,squadre_in_gioco,altre_squadre,old_data):
        H,len_H=self._h_gironi(squadre_in_gioco,altre_squadre)

        dati_base=["partita","squadra","goal partita","capitano",
                   "riserva","ingresso riserva","titolari","titolo","goal match"]
        verifiche=["lunghezza","tag","link","link commento","commento valido","penalità"]
        
        len_D=len(dati_base)
        len_V=len(verifiche)

        num_cols=len_D+len_V+len_H
        num_rows=3

        headers=[ ["" for c in range(num_cols) ] for r in range(num_rows) ] 
        req_list=[]

        for c in range(len_D):
            headers[0][c]=dati_base[c]
            req_list.append(self._ss._req_merge(sheet,0,2,c,c))

        headers[0][len_D]="verifiche e penalità" 
        req_list.append(self._ss._req_merge(sheet,0,1,len_D,len_D+len_V-1))

        for c in range(len_V):
            headers[2][len_D+c]=verifiche[c]

        headers[0][len_D+len_V]="voti"
        req_list+=[
            self._ss._req_merge(sheet,0,0,len_D+len_V,num_cols-1),
            self._ss._req_border(sheet,0,0,len_D+len_V,num_cols-1,
                                 inner=self.black_line,outer=self.black_line),
        ]

        c=len_D+len_V
        for partita,s_list in H:
            headers[1][c]=partita
            req_list+=[
                self._ss._req_merge(sheet,1,1,c,c+len(s_list)-1),
                self._ss._req_border(sheet,1,2,c,c+len(s_list)-1,
                                     inner=self.gray_line,outer=self.black_line),
            ]
            for squadra in s_list:
                headers[2][c]=squadra
                c=c+1


        h_format={
            "backgroundColor": self._ss.red,
            "verticalAlignment": "BOTTOM",
            "horizontalAlignment": "CENTER",
            "textFormat": self._ss.bold_text,
        }

        r_format=h_format.copy()
        r_format["textRotation"]= {
            "angle": 90,
        }


        req_list+=[
            self._ss._req_format(sheet,0,2,          0,            0,r_format),
            self._ss._req_format(sheet,0,2,          1,            1,h_format),
            self._ss._req_format(sheet,0,2,          2,            2,r_format),
            self._ss._req_format(sheet,0,2,          3,      len_D-2,h_format),
            self._ss._req_format(sheet,0,2,    len_D-1,      len_D-1,r_format),
            self._ss._req_format(sheet,0,1,      len_D,   num_cols-1,h_format),
            self._ss._req_format(sheet,2,2,      len_D,   num_cols-1,r_format),

            self._ss._req_border(sheet,0,2,0,8,
                                 inner=self.gray_line,outer=self.black_line),
            self._ss._req_border(sheet,0,2,9,14,
                                 inner=self.gray_line,outer=self.black_line),

        ]

        return headers,req_list

    # ok
    def _set_titolare(self,R,r,r_big,H,old_data,titolare):
        formula_penalita='=-5'
        formula_penalita+='+if(J%d<=8000,1,0)'
        formula_penalita+='+countif(K%d:N%d,"?*")'
        R[r][6]=titolare
        R[r][8]="=sum(O%d:Z%d)" % (r_big+r+1,r_big+r+1)
        R[r][14]=formula_penalita % (r_big+r+1,r_big+r+1,r_big+r+1)

        if old_data is None: return
        R[r][5]=old_data.loc[titolare]["base","ingresso riserva"]
        R[r][7]=old_data.loc[titolare]["base","titolo"]

        verifiche=["lunghezza","tag","link","link commento","commento valido"]
        for n in range(len(verifiche)):
            R[r][9+n]=old_data.loc[titolare]["verifiche",verifiche[n]]

        n=15
        for girone,s_list in H:
            for squadra in s_list:
                R[r][n]=old_data.loc[titolare][girone,squadra]
                n+=1

    def _data(self,sheet,num_cols,giornata,accoppiamenti,squadre_in_gioco,altre_squadre,old_data):
        h_rows=3
        H,len_H=self._h_gironi(squadre_in_gioco,altre_squadre)
        start_H=num_cols-len_H

        # partite=collections.OrderedDict()
        # for girone,partita in accoppiamenti.index.unique():
        #     if girone not in partite: partite[girone]=[]
        #     partite[girone].append(partita)
        # partite=list(partite.items())

        partite=list(accoppiamenti.index.unique())

        t_format={
            #"backgroundColor": self._ss.red,
            "verticalAlignment": "MIDDLE",
            "horizontalAlignment": "LEFT",
            "textFormat": self._ss.normal_text,
        }

        c_format=t_format.copy()
        c_format["horizontalAlignment"]= "CENTER"

        d_format=t_format.copy()
        d_format["numberFormat"]={
            "type": "DATE",
            "pattern": "dd/mm hh:mm"
        }

        data=[]
        req_list=[]
        r_big=h_rows

        nr=4*len(partite)
        R=[ ["" for c in range(0,15) ]+[ "" for c in range(15,num_cols) ] for r in range(nr) ]

        r=0
        for partita in partite:
            R[r][0]=partita
            req_list+=[
                self._ss._req_merge(sheet,r_big+r,r_big+r+3,0,0),
                self._ss._req_border(sheet,r_big+r,r_big+r+3,0,8,
                                     inner=self.gray_line,outer=self.black_line),
                self._ss._req_border(sheet,r_big+r,r_big+r+3,9,14,
                                     inner=self.gray_line,outer=self.black_line),
            ]
            c=start_H
            for p_col,s_list in H:
                nc=len(s_list)
                if p_col!=partita:
                    req_list.append(self._ss._req_border(sheet,r_big+r,r_big+r+3,c,c+nc-1,
                                                         inner=self.gray_line,outer=self.black_line))
                    c+=nc
                    continue
                req_list+=[
                    self._ss._req_border(sheet,r_big+r,r_big+r+3,c,c+nc-1,
                                         inner=self.gray_line,outer=self.black_line),
                    self._ss._req_colors(sheet,r_big+r,r_big+r+3,c,c+nc-1,
                                         background=self._ss.gray), #,text_format=c_format),
                ]
                c+=nc
                continue
            for n in [0,1]:
                sq=accoppiamenti.loc[partita].iloc[n]
                R[r][1]=sq["squadra"]
                R[r][3]=sq["capitano"]
                R[r][4]=sq["riserva"]

                self._set_titolare(R,r,r_big,H,old_data,sq["match 1"])
                self._set_titolare(R,r+1,r_big,H,old_data,sq["match 2"])

                R[r][2]="=I%d+I%d" % (r_big+r+1,r_big+r+2)

                req_list+=[
                    self._ss._req_merge(sheet,r_big+r,r_big+r+1,1,1),
                    self._ss._req_merge(sheet,r_big+r,r_big+r+1,2,2),
                    self._ss._req_merge(sheet,r_big+r,r_big+r+1,3,3),
                    self._ss._req_merge(sheet,r_big+r,r_big+r+1,4,4),
                ]
                r+=2



        data+=R
        r_big+=nr


        num_rows=h_rows+len(data)

        req_list+=[
            self._ss._req_format(sheet,h_rows,num_rows-1,0,0,c_format),
            self._ss._req_format(sheet,h_rows,num_rows-1,1,1,t_format),
            self._ss._req_format(sheet,h_rows,num_rows-1,2,2,c_format),
            self._ss._req_format(sheet,h_rows,num_rows-1,3,4,c_format),
            self._ss._req_format(sheet,h_rows,num_rows-1,5,5,d_format),
            self._ss._req_format(sheet,h_rows,num_rows-1,6,7,t_format),
            self._ss._req_format(sheet,h_rows,num_rows-1,8,num_cols-1,c_format),
        ]

        return data,req_list

    # ok
    def _general_requests(self,sheet,num_rows,num_cols):
        req_list=[
            self._ss._req_autoresize_columns(sheet,0,num_cols-1),
            self._ss._req_resize_rows(sheet,3,num_rows-1,30),
            self._ss._req_resize_columns(sheet,0,0,30),
            self._ss._req_resize_columns(sheet,10,num_cols-1,30),
            self._ss._req_resize_columns(sheet,7,7,500),
            self._ss._req_resize_columns(sheet,2,2,60),
            self._ss._req_resize_columns(sheet,8,8,60),
            self._ss._req_resize_columns(sheet,9,9,60),
        ]
        return req_list

    def __call__(self,giornata,accoppiamenti,squadre_in_gioco,altre_squadre,old_data): 
        sheet=self._names[giornata-1]

        headers,req_headers=self._headers(sheet,giornata,accoppiamenti,squadre_in_gioco,altre_squadre,old_data)
        num_cols=len(headers[0])
        data,req_data=self._data(sheet,num_cols,giornata,accoppiamenti,squadre_in_gioco,altre_squadre,old_data)

        D=headers+data
        num_rows=len(D)

        body=self._ss._req_body_data(sheet,D)
        result = self._ss._batch_update_values(body)

        req_list=[
            self._ss._req_unmerge(sheet,0,2*num_rows,0,2*num_cols),
        ]
        req_list+=req_headers
        req_list+=req_data
        req_list+=self._general_requests(sheet,num_rows,num_cols)

        body={
            "requests": req_list,
        }

        result = self._ss._batch_update_spreadsheets(body)


class SetFormazioniSheet(object):
    def __init__(self,spreadsheet,sheet_names):
        self._ss=spreadsheet
        self._names=sheet_names

        self.black_line={
            "style": "SOLID",
            "width": 1,
            "color": self._ss.black,
        }

    def _headers(self,sheet,giornata,riposano,squadre,old_data):
        headers=["squadra","riposa","capitano","riserva","titolare 1","titolare 2"]
        num_cols=len(headers)

        h_format={
            "backgroundColor": self._ss.green,
            "verticalAlignment": "BOTTOM",
            "horizontalAlignment": "CENTER",
            "textFormat": self._ss.bold_text,
        }

        req_list=[
            self._ss._req_border(sheet,0,0,0,num_cols-1,
                                 inner=self.black_line,outer=self.black_line),
            self._ss._req_format(sheet,0,0,0,num_cols-1,h_format),
        ]

        return [headers],req_list

    def _data(self,sheet,num_cols,giornata,riposano,squadre,old_data):
        data=[]
        req_list=[]
        ind_riposano=[]

        for sq in squadre:
            R=[ sq ] + [ "" for c in range(1,num_cols) ]
            if sq in riposano:
                ind_riposano.append(len(data))
                R[1]="(riposa)"
            if old_data is None:
                data.append(R)
                continue
            R[2]=old_data.loc[sq]["capitano"]
            R[3]=old_data.loc[sq]["riserva"]
            R[4]=old_data.loc[sq]["titolare 1"]
            R[5]=old_data.loc[sq]["titolare 2"]
            data.append(R)

        num_rows=len(data)

        t_format={
            #"backgroundColor": self._ss.red,
            "verticalAlignment": "MIDDLE",
            "horizontalAlignment": "LEFT",
            "textFormat": self._ss.normal_text,
        }

        r_format=t_format.copy()
        r_format["backgroundColor"]= self._ss.gray

        req_list+=[
            self._ss._req_border(sheet,1,num_rows,0,num_cols-1,
                                 inner=self.black_line,outer=self.black_line),
            self._ss._req_format(sheet,1,num_rows,0,num_cols-1,t_format),
        ]

        for r in ind_riposano:
            req_list.append(self._ss._req_format(sheet,r+1,r+1,0,num_cols-1,r_format))

        return data,req_list

    def _general_requests(self,sheet,num_rows,num_cols):
        req_list=[
            self._ss._req_autoresize_columns(sheet,0,num_cols-1),
        ]
        return req_list

    def __call__(self,giornata,riposano,squadre,old_data): 
        sheet=self._names[giornata-1]

        headers,req_headers=self._headers(sheet,giornata,riposano,squadre,old_data)
        num_cols=len(headers[0])
        data,req_data=self._data(sheet,num_cols,giornata,riposano,squadre,old_data)
        D=headers+data
        num_rows=len(D)

        body=self._ss._req_body_data(sheet,D)
        result = self._ss._batch_update_values(body)

        req_list=[
            self._ss._req_unmerge(sheet,0,2*num_rows,0,2*num_cols),
        ]
        req_list+=req_headers
        req_list+=req_data
        req_list+=self._general_requests(sheet,num_rows,num_cols)

        body={
            "requests": req_list,
        }

        result = self._ss._batch_update_spreadsheets(body)

class N2017Spreadsheet(Spreadsheet):
    spreadsheetId = '1dWyk3L8xJiT303LqL9fg4gqmIIGr29rCVHwqaIHeXTA'

    def _batch_update_values(self,body):
        return self.values.batchUpdate(spreadsheetId=self.spreadsheetId,body=body).execute()

    def _batch_update_spreadsheets(self,body):
        return self.spreadsheets.batchUpdate(spreadsheetId=self.spreadsheetId,body=body).execute()
        

    gray={
        "blue": 0.75,
        "red": 0.75,
        "green": 0.75,
        "alpha": 1.0,
    }

    green={
        "blue": 0.75,
        "red": 0.75,
        "green": 1.0,
        "alpha": 1.0,
    }

    disabled_text = {
        "foregroundColor": gray,
        "fontSize": 10,
        "bold": False
    }

    gironi="Gironi"
    calendario="Calendario"
    voti="Voti"
    ranking_generale="Ranking generale"
    ranking_giocatori="Ranking giocatori"
    ranking_squadre="Ranking squadre"
    elo_squadre="Elo squadre"
    elo_giocatori="Elo giocatori"

    giornate=[
        "Prima giornata",
        "Seconda giornata",
        "Terza giornata",
        "Quarti di finale",
        "Semifinali",
        "Finali",
    ]

    formazioni=[
        "Formazioni prima giornata",
        "Formazioni seconda giornata",
        "Formazioni terza giornata",
        "Formazioni quarti di finale",
        "Formazioni semifinali",
        "Formazioni finali",
    ]

    def __init__(self):
        Spreadsheet.__init__(self)
        self.set_giornata=SetGiornataSheet(self,self.giornate)
        self.set_giornata_finali=SetGiornataFinaliSheet(self,self.giornate)
        self.set_formazioni=SetFormazioniSheet(self,self.formazioni)

    def set_calendario(self,labels,data):
        header=["giornata","girone","partita","squadra 1","squadra 2"]
        D=[header]+data
        body=self._req_body_data(self.calendario,D)
        result = self.values.batchUpdate(spreadsheetId=self.spreadsheetId,body=body).execute()

        h_format={
            "backgroundColor": self.red,
            "verticalAlignment": "MIDDLE",
            "horizontalAlignment": "CENTER",
            "textFormat": self.bold_text
        }

        h1_format=h_format.copy()
        h2_format=h_format.copy()
        h3_format=h_format.copy()

        h1_format["backgroundColor"]=self.green
        h2_format["backgroundColor"]=self.yellow
        h3_format["backgroundColor"]=self.blue

        d1_format={
            "verticalAlignment": "MIDDLE",
            "horizontalAlignment": "LEFT",
            "textFormat": self.normal_text
        }
        d2_format=d1_format.copy()
        d3_format=d1_format.copy()
        
        d1_format["backgroundColor"]=self.green_light
        d2_format["backgroundColor"]=self.yellow_light
        d3_format["backgroundColor"]=self.blue_light

        num_rows=6*len(labels)+1
        num_cols=5

        num_gironi=len(labels)

        req_list=[
            self._req_border(self.calendario,0,num_rows-1,0,num_cols-1,
                             inner=self.black_line,outer=self.black_line),
            self._req_format(self.calendario,0,0,0,num_cols-1,h_format),

            self._req_format(self.calendario,1,             2*num_gironi,0,2,h1_format),
            self._req_format(self.calendario,1+2*num_gironi,4*num_gironi,0,2,h2_format),
            self._req_format(self.calendario,1+4*num_gironi,6*num_gironi,0,2,h3_format),
            self._req_format(self.calendario,1,             2*num_gironi,3,4,d1_format),
            self._req_format(self.calendario,1+2*num_gironi,4*num_gironi,3,4,d2_format),
            self._req_format(self.calendario,1+4*num_gironi,6*num_gironi,3,4,d3_format),
            self._req_autoresize_columns(self.calendario,0,num_cols-1),

            self._req_unmerge(self.calendario,0,2*num_rows,0,2*num_cols),
            self._req_merge(self.calendario,1,             2*num_gironi,0,0),
            self._req_merge(self.calendario,1+2*num_gironi,4*num_gironi,0,0),
            self._req_merge(self.calendario,1+4*num_gironi,6*num_gironi,0,0),

        ]

        for n in range(num_gironi):
            req_list+=[
                self._req_merge(self.calendario,2*n+1,             2*n+2,1,1),
                self._req_merge(self.calendario,2*n+1+2*num_gironi,2*n+2+2*num_gironi,1,1),
                self._req_merge(self.calendario,2*n+1+4*num_gironi,2*n+2+4*num_gironi,1,1),
            ]

        body={
            "requests": req_list,
        }

        result = self.spreadsheets.batchUpdate(spreadsheetId=self.spreadsheetId,body=body).execute()
        

    def set_gironi(self,labels,data):
        D=[labels]
        for r in data:
            R=[]
            for c in r:
                if c=="(riposo)":
                    R.append("")
                    continue
                R.append(c)
            D.append(R)

        body=self._req_body_data(self.gironi,D)
        result = self.values.batchUpdate(spreadsheetId=self.spreadsheetId,body=body).execute()
        
        h_format={
            "backgroundColor": self.green,
            "verticalAlignment": "MIDDLE",
            "horizontalAlignment": "CENTER",
            "textFormat": self.bold_text
        }

        d_format={
            "verticalAlignment": "MIDDLE",
            "horizontalAlignment": "LEFT",
            "textFormat": self.normal_text
        }

        req_list=[
            self._req_border(self.gironi,0,4,0,len(labels)-1,
                             inner=self.black_line,outer=self.black_line),
            self._req_format(self.gironi,0,0,0,len(labels)-1,h_format),
            self._req_format(self.gironi,1,4,0,len(labels)-1,d_format),
            self._req_autoresize_columns(self.gironi,0,len(labels)-1),

        ]

        body={
            "requests": req_list,
        }

        result = self.spreadsheets.batchUpdate(spreadsheetId=self.spreadsheetId,body=body).execute()

    def set_ranking_generale(self,labels,data):
        D=[["utente"]+labels]+data
        body=self._req_body_data(self.ranking_generale,D)
        result = self.values.batchUpdate(spreadsheetId=self.spreadsheetId,body=body).execute()
        
        h_format={
            "backgroundColor": self.green,
            "verticalAlignment": "MIDDLE",
            "horizontalAlignment": "CENTER",
            "textFormat": self.bold_text
        }

        hv_format={
            "backgroundColor": self.green,
            "verticalAlignment": "MIDDLE",
            "horizontalAlignment": "RIGHT",
            "textFormat": self.bold_text
        }
        

        d_format={
            "verticalAlignment": "MIDDLE",
            "horizontalAlignment": "CENTER",
            "textFormat": self.normal_text
        }

        dt_format={
            "backgroundColor": self.green_light,
            "verticalAlignment": "MIDDLE",
            "horizontalAlignment": "CENTER",
            "textFormat": self.normal_text
        }

        dis_format={
            'foregroundColor': self.gray
        }

        num_rows=1+len(data)
        num_cols=1+len(labels)

        req_list=[
            self._req_border(self.ranking_generale,0,num_rows-1,0,num_cols-1,
                             inner=self.black_line,outer=self.black_line),
            self._req_format(self.ranking_generale,0,0,0,num_cols-1,h_format),
            self._req_format(self.ranking_generale,0,num_rows-1,0,0,hv_format),
            self._req_format(self.ranking_generale,1,num_rows-1,2,num_cols-1,d_format),
            self._req_format(self.ranking_generale,1,num_rows-1,1,1,dt_format),
            self._req_autoresize_columns(self.ranking_generale,0,num_cols-1),
            self._req_conditional_format(self.ranking_generale,1,num_rows-1,2,num_cols-1,"=c2=0",dis_format),
        ]

        body={
            "requests": req_list,
        }

        result = self.spreadsheets.batchUpdate(spreadsheetId=self.spreadsheetId,body=body).execute()


    def set_ranking_squadre(self,labels,data,num_gironi):
        D=[labels]
        for r in data:
            if r[0]=="(riposo)":
                D.append(["","","F4"])
                continue
            D.append(r)
        body=self._req_body_data(self.ranking_squadre,D)
        result = self.values.batchUpdate(spreadsheetId=self.spreadsheetId,body=body).execute()
        
        h_format={
            "backgroundColor": self.gray,
            "verticalAlignment": "MIDDLE",
            "horizontalAlignment": "CENTER",
            "textFormat": self.bold_text
        }

        hv_format=[]
        d_format=[]

        h_colors=[ self.green,self.yellow,self.blue,self.red ]
        d_colors=[ self.green_light,self.yellow_light,self.blue_light,self.red_light ]

        for n in range(4):
            h={
                "backgroundColor": h_colors[n],
                "verticalAlignment": "MIDDLE",
                "horizontalAlignment": "RIGHT",
                "textFormat": self.bold_text
            }
            hv_format.append(h)
            d={
                "backgroundColor": d_colors[n],
                "verticalAlignment": "MIDDLE",
                "horizontalAlignment": "CENTER",
                "textFormat": self.normal_text
            }
            d_format.append(d)


        num_rows=1+len(data)
        num_cols=len(labels)

        req_list=[
            self._req_unmerge(self.ranking_squadre,0,2*num_rows,0,2*num_cols),
            self._req_border(self.ranking_squadre,0,num_rows-1,0,num_cols-1,
                             inner=self.black_line,outer=self.black_line),
            self._req_format(self.ranking_squadre,0,0,0,num_cols-1,h_format),
            self._req_autoresize_columns(self.ranking_squadre,0,num_cols-1),
        ]

        for n in range(4):
            c=num_gironi*n+1
            req_list+=[
                self._req_merge(self.ranking_squadre,c,c+num_gironi-1,0,0),
                self._req_format(self.ranking_squadre,c,c+num_gironi-1,0,0,hv_format[n]),
                self._req_format(self.ranking_squadre,c,c+num_gironi-1,1,num_cols-1,d_format[n]),
            ]

    def set_ranking_giocatori(self,labels,data):
        D=[["squadra","utente"]+labels]+data
        body=self._req_body_data(self.ranking_giocatori,D)
        result = self.values.batchUpdate(spreadsheetId=self.spreadsheetId,body=body).execute()
        
        h_format={
            "backgroundColor": self.red,
            "verticalAlignment": "MIDDLE",
            "horizontalAlignment": "CENTER",
            "textFormat": self.bold_text
        }

        hv_format=[
            {
                "backgroundColor": self.green,
                "verticalAlignment": "MIDDLE",
                "horizontalAlignment": "RIGHT",
                "textFormat": self.bold_text
            },
            {
                "backgroundColor": self.yellow,
                "verticalAlignment": "MIDDLE",
                "horizontalAlignment": "RIGHT",
                "textFormat": self.bold_text
            }
        ]
        

        d_format=[
            {
                "backgroundColor": self.green_light,
                "verticalAlignment": "MIDDLE",
                "horizontalAlignment": "CENTER",
                "textFormat": self.normal_text
            },
            {
                "backgroundColor": self.yellow_light,
                "verticalAlignment": "MIDDLE",
                "horizontalAlignment": "CENTER",
                "textFormat": self.normal_text
            },
        ]

        dis_format={
            'foregroundColor': self.gray
        }

        num_rows=1+len(data)
        num_cols=2+len(labels)

        req_list=[
            self._req_border(self.ranking_giocatori,0,num_rows-1,0,num_cols-1,
                             inner=self.black_line,outer=self.black_line),
            self._req_format(self.ranking_giocatori,0,0,0,num_cols-1,h_format),


            self._req_autoresize_columns(self.ranking_giocatori,0,num_cols-1),
            self._req_conditional_format(self.ranking_giocatori,1,num_rows-1,3,num_cols-1,"=d2=0",dis_format),
            self._req_unmerge(self.ranking_giocatori,0,2*num_rows,0,2*num_cols),
        ]


        for n in range(len(data)//3):
            req_list+=[
                self._req_merge(self.ranking_giocatori,3*n+1,3*n+3,0,0),
                self._req_format(self.ranking_giocatori,3*n+1,3*n+3,0,2,hv_format[n%2]),
                self._req_format(self.ranking_giocatori,3*n+1,3*n+3,3,num_cols-1,d_format[n%2]),
            ]
        

        body={
            "requests": req_list,
        }

        result = self.spreadsheets.batchUpdate(spreadsheetId=self.spreadsheetId,body=body).execute()

    def set_elo_giocatori(self,labels,data):
        D=[["utente"]+labels]+data
        body=self._req_body_data(self.elo_giocatori,D)
        result = self.values.batchUpdate(spreadsheetId=self.spreadsheetId,body=body).execute()
        
        h_format={
            "backgroundColor": self.green,
            "verticalAlignment": "MIDDLE",
            "horizontalAlignment": "CENTER",
            "textFormat": self.bold_text
        }

        hv_format={
            "backgroundColor": self.green,
            "verticalAlignment": "MIDDLE",
            "horizontalAlignment": "RIGHT",
            "textFormat": self.bold_text
        }
        

        d_format={
            "verticalAlignment": "MIDDLE",
            "horizontalAlignment": "CENTER",
            "textFormat": self.normal_text
        }

        dt_format={
            "backgroundColor": self.green_light,
            "verticalAlignment": "MIDDLE",
            "horizontalAlignment": "CENTER",
            "textFormat": self.normal_text
        }

        dis_format={
            'foregroundColor': self.gray
        }

        num_rows=1+len(data)
        num_cols=1+len(labels)

        req_list=[
            self._req_border(self.elo_giocatori,0,num_rows-1,0,num_cols-1,
                             inner=self.black_line,outer=self.black_line),
            self._req_format(self.elo_giocatori,0,0,0,num_cols-1,h_format),
            self._req_format(self.elo_giocatori,0,num_rows-1,0,0,hv_format),
            self._req_format(self.elo_giocatori,1,num_rows-1,2,num_cols-1,d_format),
            self._req_format(self.elo_giocatori,1,num_rows-1,1,1,dt_format),
            self._req_autoresize_columns(self.elo_giocatori,0,num_cols-1),
            self._req_conditional_format(self.elo_giocatori,1,num_rows-1,2,num_cols-1,"=c2=0",dis_format),
        ]

        body={
            "requests": req_list,
        }

        result = self.spreadsheets.batchUpdate(spreadsheetId=self.spreadsheetId,body=body).execute()

    def set_elo_squadre(self,labels,data):
        D=[["squadra","utente"]+labels]+data
        body=self._req_body_data(self.elo_squadre,D)
        result = self.values.batchUpdate(spreadsheetId=self.spreadsheetId,body=body).execute()
        
        h_format={
            "backgroundColor": self.red,
            "verticalAlignment": "MIDDLE",
            "horizontalAlignment": "CENTER",
            "textFormat": self.bold_text
        }

        hv_format=[
            {
                "backgroundColor": self.green,
                "verticalAlignment": "MIDDLE",
                "horizontalAlignment": "RIGHT",
                "textFormat": self.bold_text
            },
            {
                "backgroundColor": self.yellow,
                "verticalAlignment": "MIDDLE",
                "horizontalAlignment": "RIGHT",
                "textFormat": self.bold_text
            }
        ]
        

        d_format=[
            {
                "backgroundColor": self.green_light,
                "verticalAlignment": "MIDDLE",
                "horizontalAlignment": "CENTER",
                "textFormat": self.normal_text
            },
            {
                "backgroundColor": self.yellow_light,
                "verticalAlignment": "MIDDLE",
                "horizontalAlignment": "CENTER",
                "textFormat": self.normal_text
            },
        ]

        dis_format={
            'foregroundColor': self.gray
        }

        num_rows=1+len(data)
        num_cols=2+len(labels)


        req_list=[
            self._req_border(self.elo_squadre,0,num_rows-1,0,num_cols-1,
                             inner=self.black_line,outer=self.black_line),
            self._req_format(self.elo_squadre,0,0,0,num_cols-1,h_format),
            self._req_autoresize_columns(self.elo_squadre,0,num_cols-1),
            self._req_conditional_format(self.elo_squadre,1,num_rows-1,3,num_cols-1,"=d2=0",dis_format),
            self._req_unmerge(self.elo_squadre,0,2*num_rows,0,2*num_cols),
        ]


        for n in range(len(data)//3):
            req_list+=[
                self._req_merge(self.elo_squadre,3*n+1,3*n+3,0,0),
                self._req_format(self.elo_squadre,3*n+1,3*n+3,0,2,hv_format[n%2]),
                self._req_format(self.elo_squadre,3*n+1,3*n+3,3,num_cols-1,d_format[n%2]),
            ]
        

        body={
            "requests": req_list,
        }

        result = self.spreadsheets.batchUpdate(spreadsheetId=self.spreadsheetId,body=body).execute()

    def get_giornata(self,giornata):
        sheet=self.giornate[giornata-1]
        
        try:
            g=self._get_data(sheet+'!G:ZZ')
        except KeyError as e:
            return None

        T=[]
        for n in range(4):
            T.append(("base",g[0][n]))
        for n in range(4,10):
            T.append(("verifiche",g[2][n]))
        girone=""    
        for n in range(10,len(g[2])):
            if len(g[1])>n and g[1][n]:
                girone=g[1][n].replace("Girone","").strip()
            T.append((girone,g[2][n]))
        tindex=pandas.MultiIndex.from_tuples(T)

        D=[]
        for r in g[3:]:
            if len(r)==len(g[2]):
                D.append(r)
                continue
            for n in range(len(r),len(g[2])):
                r.append("")
            D.append(r)

        d=pandas.DataFrame(D,columns=tindex)
        d=d.set_index([("base","titolari")])
        d.index.names=["titolare"]
        d=d.drop([("base","goal match")],axis=1)
        return d

    def get_formazioni(self,giornata):
        sheet=self.formazioni[giornata-1]
        
        try:
            g=self._get_data(sheet+'!A:ZZ')
        except KeyError as e:
            return None

        T=g[0]
        D=[]
        for r in g[1:]:
            if len(r)==len(g[0]):
                D.append(r)
                continue
            for n in range(len(r),len(g[0])):
                r.append("")
            D.append(r)

        d=pandas.DataFrame(D,columns=T)
        d=d.set_index(["squadra"])
        return d

    def get_giornata_finali(self,giornata):
        sheet=self.giornate[giornata-1]
        
        try:
            g=self._get_data(sheet+'!F:ZZ')
        except KeyError as e:
            return None

        T=[]
        for n in range(4):
            T.append(("base",g[0][n]))
        for n in range(4,10):
            T.append(("verifiche",g[2][n]))
        girone=""    
        for n in range(10,len(g[2])):
            if len(g[1])>n and g[1][n]:
                girone=g[1][n].replace("Girone","").strip()
            T.append((girone,g[2][n]))
        tindex=pandas.MultiIndex.from_tuples(T)

        D=[]
        for r in g[3:]:
            if len(r)==len(g[2]):
                D.append(r)
                continue
            for n in range(len(r),len(g[2])):
                r.append("")
            D.append(r)

        d=pandas.DataFrame(D,columns=tindex)
        d=d.set_index([("base","titolari")])
        d.index.names=["titolare"]
        d=d.drop([("base","goal match")],axis=1)
        return d
