from VLRDF import VLRDF
import os


fromPage = 60
toPage = 70
while toPage <= 100:
    outdir = './results/'+str(fromPage)+"-"+str(toPage)+'/'
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    vldf = VLRDF()
    vldf.getData(test=False,fromPage = fromPage,toPage = toPage,savedir=outdir)
    fromPage = toPage
    toPage = toPage + 10
