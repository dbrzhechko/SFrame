#! /usr/bin/env python

import os, sys, getopt, multiprocessing
import copy, glob
import math
from array import array
from ROOT import gROOT, TFile, TH1F

import optparse
usage = "usage: %prog [options]"
parser = optparse.OptionParser(usage)
parser.add_option("-f", "--fileName", action="store", type="string", dest="fileName", default="")
parser.add_option("-r", "--remove", action="store", type="string", default="", dest="catList")
parser.add_option("-c", "--cutcount", action="store_true", default=False, dest="isCutAndCount")
parser.add_option("-o", "--override", action="store_true", default=False, dest="override")
parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose")
parser.add_option("-N", "--name", action="store", type="string", dest="name", default="test")
(options, args) = parser.parse_args()

fileName = options.fileName
catList = options.catList
isShape = not options.isCutAndCount
isOverride = options.override
verbose = options.verbose


def combineCards():
    try: os.stat('combinedCards_'+options.name)
    except: os.mkdir('combinedCards_'+options.name)
    os.chdir('datacards_'+options.name)
    cardList = glob.glob('t*txt')

    signalPoints = []
    
    for card in cardList:
        print card
        mChi = card[card.find("MChi")+4:card.find("MPhi")-1]
        if "OP" in card:
            endPhi = card.find("_OP")
        elif "SL" in card:
            endPhi = card.find("_SL")
        elif "AH" in card:
            endPhi = card.find("_AH")

        mPhi = card[card.find("MPhi")+4:endPhi]
        model = card[:card.find("MChi")-1]
        signalPoints.append((model, mChi, mPhi))

    signalPoints = list(set(signalPoints))

    for s in signalPoints:
        print s
        cardsForSignal = glob.glob(s[0]+'_MChi'+s[1]+'_MPhi'+s[2]+'_*.txt')
        cmdSL = "combineCards.py "
        cmdAH = "combineCards.py "
        cmdALL = "combineCards.py "
        for card in cardsForSignal:

            region = card[card.rfind('_')+1:card.find('.txt')]
            print region
            if 'SL' in region:
                cmdSL = cmdSL + region + "=" + card + " "
                cmdALL = cmdALL + region + "=" + card + " "
            if 'AH' in region:
                cmdAH = cmdAH + region + "=" + card + " "
                cmdALL = cmdALL + region + "=" + card + " "
        
        
        cardOut = ' > ' + '../combinedCards_'+options.name+'/'+s[0]+'_MChi'+s[1]+'_MPhi'+s[2]+'_'
        
        cmdSL = cmdSL + cardOut + "SL.txt"
        cmdAH = cmdAH + cardOut + "AH.txt"
        cmdALL = cmdALL + cardOut + "ALL.txt"

        print 'Combining cards for '+s[0]+'_MChi'+s[1]+'_MPhi'+s[2] + ' SL ' 
        print cmdSL
        os.system(cmdSL)
        print 'Combining cards for '+s[0]+'_MChi'+s[1]+'_MPhi'+s[2] + ' AH ' 
        print cmdAH
        os.system(cmdAH)

        print 'Combining cards for '+s[0]+'_MChi'+s[1]+'_MPhi'+s[2] + ' ALL ' 
        print cmdALL
        os.system(cmdALL)

    return


if __name__ == "__main__":
    combineCards()
    if 1==2: #maybe fix later 
        print 'running combine'
        cardList = glob.glob(('combinedCards_'+options.name+'/t*ALL.txt'))
        for card in cardList:
            mPhi = card[card.find("MPhi")+4:card.find("ALL")-1]
            print mPhi
            cmd = 'combine -M AsymptoticLimits --run blind --datacard '+card+' -n '+ card[card.find("/")+1:].replace('.txt','') + ' -m ' + mPhi
            print cmd
            os.system(cmd)



# python datacard.py -f rootfiles/DM.root -o

