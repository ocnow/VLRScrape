import requests
import re
from bs4 import BeautifulSoup

class MatchDetails:
    def __init__(self,html_text):
        self.html_txt = html_text

    def getTourDF(self,match_id,matchHeader):
        tourAndTime = self.getTourAndTime(matchHeader)
        tourTDets = self.getTourTDets(matchHeader)
        return [match_id] + tourAndTime + tourTDets

    def getTourAndTime(self,matchHeader):
        headerSuper = matchHeader.find("div",class_="match-header-super")
        tourDetails = headerSuper.find("a",class_="match-header-event").find("div",recursive=False).find_all("div")

        tournamentName = self.cleanStr(tourDetails[0].text)
        tournamentStgName = self.cleanStr(tourDetails[1].text)
        dateTime = headerSuper.find("div",class_="match-header-date").find("div",class_="moment-tz-convert")["data-utc-ts"]

        patchText = self.cleanStr(headerSuper.find("div",class_="match-header-date").text)
        patchar = re.findall(r'Patch \d+\.\d+', patchText)
        patch = None
        if(len(patchar) > 0):
            patch = patchar[0]

        return [tournamentName,tournamentStgName,dateTime,patch]

    def getTourTDets(self,matchHeader):
        t_divs = matchHeader.find_all("a",class_="match-header-link")
        t1_div = None
        t2_div = None
        for t_div in t_divs:
            if t_div.has_attr('class'):
                if 'mod-1' in t_div['class']:
                    t1_div = t_div
                elif 'mod-2' in t_div['class']:
                    t2_div = t_div

        t1_name = self.cleanStr(t1_div.find("div",class_="wf-title-med").text)
        t2_name = self.cleanStr(t2_div.find("div",class_="wf-title-med").text)
        t1_mscore = self.cleanStr(matchHeader.find("div",class_="match-header-vs-score").find_all('span',class_="match-header-vs-score-winner")[0].text)
        t2_mscore = self.cleanStr(matchHeader.find("div",class_="match-header-vs-score").find_all('span',class_="match-header-vs-score-loser")[0].text)

        return [t1_name,t2_name,t1_mscore,t2_mscore]

    def cleanStr(self,st):
        return st.strip().replace('\t','').replace('\n','')

    def getDetails(self):
        #MATCH_URL = 'https://www.vlr.gg/190/2g4l-vs-inst-cooler-cup-playoffs-qf'

        #html_txt = requests.get(MATCH_URL).text
        mapstats = BeautifulSoup(self.html_txt, 'html.parser').find_all("div",class_="col-container")[0].find("div",class_="mod-3",recursive=False)

        match_id = MATCH_URL.split("/")[-2]

        matchHeader = mapstats.find("div",class_='match-header')
        return self.getTourDF(match_id,matchHeader)
