import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from MatchDetails import MatchDetails
from MapDetails import MapDetails

class VLRDF:
    MatchCols = ['VLR_MATCH_ID','TOURNAMENT_NAME','TOUR_STAGE_NAME','DATE-TIME','PATCH_ID','TEAM_1_NAME','TEAM_2_NAME','TEAM_1_MSCORE','TEAM_2_MSCORE']

    GameCols = ['match_id','game_id','mp_name','t1_scre','t2_scre','T1_agnt_1_nme','T1_plyr_1_nme','T1_ACS_1','T1_k_1','T1_D_1','T1_Ass_1','T1_ADR_1','T1_HS_1','T1_FK_1','T1_FD_1','T1_agnt_2_nme',
    'T1_plyr_2_nme','T1_ACS_2','T1_k_2','T1_D_2','T1_Ass_2','T1_ADR_2','T1_HS_2','T1_FK_2','T1_FD_2','T1_agnt_3_nme','T1_plyr_3_nme','T1_ACS_3','T1_k_3','T1_D_3','T1_Ass_3','T1_ADR_3','T1_HS_3','T1_FK_3','T1_FD_3','T1_agnt_4_nme','T1_plyr_4_nme','T1_ACS_4','T1_k_4','T1_D_4','T1_Ass_4','T1_ADR_4','T1_HS_4','T1_FK_4','T1_FD_4','T1_agnt_5_nme','T1_plyr_5_nme','T1_ACS_5','T1_k_5','T1_D_5','T1_Ass_5','T1_ADR_5','T1_HS_5','T1_FK_5','T1_FD_5','T2_agnt_1_nme','T2_plyr_1_nme','T2_ACS_1','T2_k_1','T2_D_1','T2_Ass_1','T2_ADR_1','T2_HS_1','T2_FK_1','T2_FD_1','T2_agnt_2_nme','T2_plyr_2_nme','T2_ACS_2','T2_k_2','T2_D_2','T2_Ass_2','T2_ADR_2','T2_HS_2','T2_FK_2','T2_FD_2','T2_agnt_3_nme','T2_plyr_3_nme','T2_ACS_3','T2_k_3','T2_D_3','T2_Ass_3','T2_ADR_3','T2_HS_3','T2_FK_3','T2_FD_3','T2_agnt_4_nme','T2_plyr_4_nme','T2_ACS_4','T2_k_4','T2_D_4','T2_Ass_4','T2_ADR_4','T2_HS_4','T2_FK_4','T2_FD_4','T2_agnt_5_nme','T2_plyr_5_nme','T2_ACS_5','T2_k_5','T2_D_5','T2_Ass_5','T2_ADR_5','T2_HS_5','T2_FK_5','T2_FD_5','RND_RSLT_1','RND_RSLT_2','RND_RSLT_3','RND_RSLT_4','RND_RSLT_5','RND_RSLT_6','RND_RSLT_7','RND_RSLT_8','RND_RSLT_9','RND_RSLT_10','RND_RSLT_11','RND_RSLT_12','RND_RSLT_13','RND_RSLT_14','RND_RSLT_15','RND_RSLT_16','RND_RSLT_17','RND_RSLT_18','RND_RSLT_19','RND_RSLT_20','RND_RSLT_21','RND_RSLT_22','RND_RSLT_23','RND_RSLT_24','RND_RSLT_25','RND_RSLT_26','RND_RSLT_27','RND_RSLT_28','RND_RSLT_29','RND_RSLT_30','RND_RSLT_31','RND_RSLT_32','RND_RSLT_33','RND_RSLT_34','RND_RSLT_35','RND_RSLT_36','RND_RSLT_37','RND_RSLT_38','RND_RSLT_39','RND_RSLT_40','RND_RSLT_41','RND_RSLT_42','RND_RSLT_43','RND_RSLT_44','RND_RSLT_45','RND_RSLT_46','RND_RSLT_47','RND_RSLT_48','RND_RSLT_49','RND_RSLT_50','RND_RSLT_51','RND_RSLT_52','RND_RSLT_53','RND_RSLT_54','RND_RSLT_55','RND_RSLT_56','RND_RSLT_57','RND_RSLT_58','RND_RSLT_59','RND_RSLT_60','RND_RSLT_61','RND_RSLT_62','RND_RSLT_63','RND_RSLT_64','RND_RSLT_65','RND_RSLT_66','RND_RSLT_67','RND_RSLT_68','RND_RSLT_69','RND_RSLT_70','RND_RSLT_71','RND_RSLT_72','RND_RSLT_73','RND_RSLT_74','RND_RSLT_75','RND_RSLT_76','RND_RSLT_77','RND_RSLT_78','RND_RSLT_79','RND_RSLT_80']
    #matchDF = pd.DataFrame(columns = MatchCols)
#gameDF = pd.DataFrame(columns = GameCols)
    BASE_URL = 'https://www.vlr.gg'
    MATCH_LIST_URL = 'https://www.vlr.gg/matches/results/?page={0}'

    def __init__(self):
        self.MATCH_URLS = []

    def saveCSV(self,matchArr,gameArr,excptnArr,savedir):
        if len(matchArr) > 0:
            matchDF = pd.DataFrame(matchArr)
            matchDF.columns = VLRDF.MatchCols
            matchDF.to_csv(savedir + 'matches.csv',index=False)

        if len(gameArr) > 0:
            gameDF = pd.DataFrame(gameArr)
            gameDF.columns = VLRDF.GameCols
            gameDF.to_csv(savedir+ 'games.csv',index=False)

        if len(excptnArr) > 0:
            exceptDF = pd.DataFrame(excptnArr)
            exceptDF.columns = ['EXCEPTION_URL']
            exceptDF.to_csv(savedir +'exception.csv',index=False)

    def prepareMTCHURLS(self,fromPage,toPage):
        for i in range(fromPage,toPage):
            html_txt = requests.get(VLRDF.MATCH_LIST_URL.format(i+1)).text
            soup = BeautifulSoup(html_txt, 'html.parser')
            match_divs = soup.find(id="wrapper").find_all("a", class_="match-item")
            for match_div in match_divs:
                self.MATCH_URLS.append(VLRDF.BASE_URL + match_div['href'])

    def dataOfMATCH(self,MATCH_URL):
        html_txt = requests.get(MATCH_URL).text
        match_id = MATCH_URL.split("/")[-2]

        mtchDetails = MatchDetails(html_txt,match_id)
        matchDet = mtchDetails.getDetails()

        mpDetails = MapDetails(html_txt,match_id)
        gameDets = mpDetails.getDetails()
        return matchDet,gameDets

    def getData(self,fromPage = 0,toPage = 10,test=False,savedir=''):
        self.prepareMTCHURLS(fromPage,toPage)
        matchArr = []
        gameArr = []
        exceptionArr = []

        endLength = len(self.MATCH_URLS)
        if test:
            endLength = 10

        for MATCH_URL in tqdm(self.MATCH_URLS[:endLength]):
            try:
                matchDet,gameDets = self.dataOfMATCH(MATCH_URL)
                if len(matchDet) == 9:
                    matchArr.append(matchDet)
                for gameDet in gameDets:
                    if len(gameDet) == 185:
                        gameArr.append(gameDet)

            except Exception:
                exceptionArr.append(MATCH_URL)
            #print("done-"+MATCH_URL.split("/")[-1])
            '''
            try:
                matchDet,gameDets = self.dataOfMATCH(MATCH_URL)
                if len(matchDet) == 9:
                    matchArr.append(matchDet)
                for gameDet in gameDets:
                    if len(gameDet) == 185:
                        gameArr.append(gameDet)
            except Exception:
                exceptionArr.append(MATCH_URL)
            #print("done-"+MATCH_URL.split("/")[-1])
            '''
        self.saveCSV(matchArr,gameArr,exceptionArr,savedir)
