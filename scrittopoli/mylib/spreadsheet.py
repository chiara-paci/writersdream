import httplib2
import os
import os.path

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
        "fontSize": 10,
        "bold": True
    }

    normal_text={
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
    
    def __init__(self):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
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
        values = result.get("valueRanges")[0]["values"]
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

    # def _req_autoresize_cols(self,sheet,col_s,col_e):
    #     return {
    #         "autoResizeDimensions": {
    #             "dimensions": {
    #                 "startIndex": col_s,
    #                 "endIndex": col_e+1,
    #                 "sheetId": self.sheets_id[sheet],
    #                 "dimension": "COLUMNS",
    #             }
    #         }
    #     }


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

    def _req_format(self,sheet,row_s,row_e,col_s,col_e,cell_format):
        c_range=self._c_range(sheet,row_s,row_e,col_s,col_e)
        return self._req_style(c_range,cell_format)

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



class N2017Spreadsheet(Spreadsheet):
    spreadsheetId = '1dWyk3L8xJiT303LqL9fg4gqmIIGr29rCVHwqaIHeXTA'

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

    def _req_body_data(self,sheet,data,first_cell="a1"):
        return {
            "valueInputOption": "RAW", #USER_ENTERED
            "data": [{
                "values": data,
                "majorDimension": "ROWS",
                "range": "%s!%s" % (sheet,first_cell)
            }]
        }

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
