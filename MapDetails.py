import requests
import re
from bs4 import BeautifulSoup

class MapDetails:
    def __init__(self,html_text,mtch_id):
        self.html_txt = html_text
        self.match_id = mtch_id

    def cleanStr(self,st):
        return st.strip().replace('\t','').replace('\n','')

    def getMapName(self,mapstat):
        MapNames = ['Breeze','Ascent','Bind','Icebox','Haven','Split']
        mapDivs = mapstat.find_all("div",class_="map")
        map_str = None
        if(len(mapDivs) > 0):
            map_str = self.cleanStr(mapDivs[0].text)

        for mapName in MapNames:
            if map_str.find(mapName) > -1:
                 return mapName

    def getAgentFromPlayerRow(self,playrRow):
        agentName = playrRow.find("td",class_="mod-agents").find("img")["title"]
        plyrName = self.cleanStr(playrRow.find("td",class_="mod-player").find("div",class_="text-of").text)
        statDivs = playrRow.find_all("td",class_="mod-stat")
        acs = self.cleanStr(statDivs[0].span.text)
        K = self.cleanStr(statDivs[1].span.text)
        D = self.cleanStr(statDivs[2].span.find_all("span")[1].text)
        AS = self.cleanStr(statDivs[3].span.text)
        ADR = self.cleanStr(statDivs[5].span.text)
        HS = self.cleanStr(statDivs[6].span.text)
        FK = self.cleanStr(statDivs[7].span.text)
        FD = self.cleanStr(statDivs[8].span.text)
        return [agentName,plyrName,acs,K,D,AS,ADR,HS,FK,FD]

    def getTPlyrStats(self,tStat):
        agentArray = []
        playrRows = tStat.find("tbody").find_all("tr")
        for playrRow in playrRows:
            agentArray = agentArray + self.getAgentFromPlayerRow(playrRow)
        return agentArray

    def getSideAndWinWay(self,rndSq):
        rndResult = ""
        if "mod-ct" in rndSq["class"]:
            rndResult += "CT_"
        else:
            rndResult += "T_"

        imgSrc = rndSq.find("img")["src"]
        return rndResult + imgSrc.split("/")[-1].split(".")[0]

    def getRndRslt(self,roundCol):
        rndSqs = roundCol.find_all("div",class_="rnd-sq")
        rndRslt = "T"
        #which team won the round and which side
        for i in range(len(rndSqs)):
            rndSq = rndSqs[i]
            if "mod-win" in rndSq["class"]:
                rndRslt += str(i+1) +"_"
                rndRslt += self.getSideAndWinWay(rndSq)
                return rndRslt

    def getRoundArray(self,roundRows):
        rndArray = []
        for roundRow in roundRows:
            roundCols = roundRow.find_all("div",class_="vlr-rounds-row-col")[1:]
            for roundCol in roundCols:
                if not 'mod-spacing' in roundCol["class"]:
                    if roundCol.find("img") is not None:
                        rndArray.append(self.getRndRslt(roundCol))
        return rndArray

    def getMapArray(self,mapstat):
        game_id = mapstat['data-game-id']
        #get Map Name
        mapName = self.getMapName(mapstat)
        #get Map Score
        mp_hdr_prts = mapstat.find_all("div",class_="vm-stats-game-header")[0]
        mpScr1 = '0'
        mpScr2 = '0'
        tmDivs = mp_hdr_prts.find_all("div",class_="team")
        for tmDiv in tmDivs:
            if 'mod-right' in tmDiv['class']:
                mpScr2 = self.cleanStr(tmDiv.find("div",class_="score").text)
            else:
                mpScr1 = self.cleanStr(tmDiv.find("div",class_="score").text)

        #GET ROUND INFO
        roundRows = mapstat.find_all("div",class_="vlr-rounds-row")
        #for roundRow in roundRows:
        #    roundCols = roundRow.find_all("div",class_="vlr-rounds-row-col")[1:]
        roundArr = self.getRoundArray(roundRows)
        #get player stats
        tStats = mapstat.find_all("table",class_="wf-table-inset")
        tarr = []
        for tStat in tStats:
            tarr = tarr + self.getTPlyrStats(tStat)
        return [[game_id,mapName,mpScr1,mpScr2] + tarr] + [roundArr]

    def getMapDF(self,match_id,allStats):
        mapstats = allStats.find_all("div",class_="vm-stats-game")
        mapArrs = []
        for mapstat in mapstats:
            game_id = mapstat['data-game-id']
            if not game_id == 'all':
                mapArrs.append(self.getFullArray(match_id,self.getMapArray(mapstat)))
        return mapArrs

    def getFullArray(self,match_id,shrtArr):


        #fill full round array
        rndArr = [None for i in range(80)]
        for i in range(len(shrtArr[-1])):
            rndArr[i] = shrtArr[-1][i]
        return [match_id] + shrtArr[0] + rndArr

    def getDetails(self):
        #MATCH_URL = 'https://www.vlr.gg/35140/yfp-gaming-vs-soar-community-gaming-premier-series-finale-main-event-ubqf'

        #html_txt = requests.get(MATCH_URL).text
        allStats = BeautifulSoup(self.html_txt, 'html.parser').find_all("div",class_="col-container")[0].find("div",class_="mod-3",recursive=False)


        #match_id = MATCH_URL.split("/")[-2]
        return self.getMapDF(self.match_id,allStats)
