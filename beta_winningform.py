import urllib.request #to get url request
from PyQt5 import QtGui, QtWidgets # Import the PyQt5 module we'll need
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget, QInputDialog, QLineEdit, QFileDialog,QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication, QUrl, QDate
import sys # We need sys so that we can pass argv to QApplication
import os
import design 
from bs4 import BeautifulSoup #the scrapper library I am using

import re
import contextlib
import sqlite3
import csv
import time

class WinningForm(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Simple reason why we use it here is that it allows us to
        # access variables, methods etc in the design.py file
        #set of variables
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
                            # It sets up layout and widgets that are defined
        
        primaryURL='http://beta.winningform.co.za' #the url value
        with contextlib.closing(urllib.request.urlopen(primaryURL)) as r: #writing with a 'with' statement ensures the url request object closes after execution
        #r=urllib.request.urlopen('http://beta.winningform.co.za/')#primary url to scrap
            soup=BeautifulSoup(r,'lxml') #initiate the scrapper
        links=soup.findAll('a',class_='btn btn-default') #finding all the meeting buttons
        ctLink=soup.findAll('div',style=re.compile(r'font-size: 1.7em; font-weight: bold; color: #6c1b98'))
        cityNames=[]
        for i in range(len(ctLink)):
            cityNames.append(str(ctLink[i].text))
        self.dictCity={}
        for i in range(len(links)):
            c={cityNames[i]:links[i]}
            self.dictCity.update(c)
        self.citySelect.addItems(cityNames)
        self.dictRace={}
        self.updateRaceLinkList('dummy')        
        #print(dictCity)
        self.analyzeButton.clicked.connect(self.extractRaceInfo)
        self.citySelect.currentTextChanged.connect(self.updateRaceLinkList)
        dateToday=QDate.currentDate()
        self.todayDate.setText(dateToday)
        # msg.done(1)
    def updateRaceLinkList(self,text):
        self.dictRace={}
        self.statusbar.showMessage('Generating Race List')
        for i in range(len(self.raceSelect)):
            self.raceSelect.removeItem(0)
        curLink='http://beta.winningform.co.za'+self.dictCity[self.citySelect.currentText()]['href']
        #print(curLink)
        with contextlib.closing(urllib.request.urlopen(curLink)) as r: 
            soup=BeautifulSoup(r,'lxml')
        links=soup.findAll('a',class_='col-sm-6 raceDiv clickable') #finding the race links
        race_links=[]
        for i in range(len(links)):
            race_links.append('http://beta.winningform.co.za'+links[i]['href'])
            self.raceSelect.addItem('Race '+str(i+1))
            ki='Race '+str(i+1)
            ctor={ki:race_links[i]}
            self.dictRace.update(ctor)
        self.statusbar.showMessage('Race list complete')
    def extractRaceInfo(self):
        self.resetCheckList()
        self.top3Table.clearContents()
        self.statusbar.showMessage(self.citySelect.currentText()+' '+self.raceSelect.currentText()+' Analysis started')
        curRace=self.raceSelect.currentText()
        race_to_scrape=self.dictRace[curRace]
        bDrawList=self.barrierChart(race_to_scrape)
        with contextlib.closing(urllib.request.urlopen(race_to_scrape)) as r: #entering into each eace links
            soup=BeautifulSoup(r,'lxml')            
        markup=str(soup)                
        regex=r'(?<=<div style="float: left; font-size: 1.7em; margin-top: 10px; font-weight: bold; color: #6B389E; margin-left: -10px;">)[0-9]+' #Regular expression. To find the total no of horses of a race

        m=re.search(regex,markup)
        horsenumber=m.group(0) #getting the string of tottal no of horses
        x = self.extractHorseInfo(soup,int(horsenumber),bDrawList) #now we wxtract information for each horse
        self.updateTrigon(x)
        #self.updateDetails(x)
        
        
        
        #return x
    def updateDetails(self,dbNamor):
        conn=sqlite3.connect('analysisData.db')
        c=conn.cursor()
        conn.commit()
        conn.close()
        c.execute('SELECT * FROM '+dbNamor)
        
    def updateTrigon(self,dbNamor):
        conn=sqlite3.connect('analysisData.db')
        c=conn.cursor()
        self.top3Table.setColumnCount(14)
        self.top3Table.setRowCount(3)
        self.top3Table.setWindowTitle('Top 3 horses')
        header=['Rank','Name','Jockey','Trainer','HorseNo','Odds','Last3','Draw','Distance','Total Runs','WeightRate','Rating','Stakes','Total Factor']
        self.top3Table.setVerticalHeaderLabels(header)
        self.top3Table.show()
        c.execute('SELECT * FROM '+dbNamor+' ORDER BY totalFactor DESC')
        valerian=c.fetchall()
        for i in range(3):
            for j in range(14):
                if(j==0):
                    self.top3Table.setItem(i,j,QTableWidgetItem(str(i+1)))
                elif(j==1):
                    self.top3Table.setItem(i,j,QTableWidgetItem(valerian[i][1]))
                elif(j==2):
                    self.top3Table.setItem(i,j,QTableWidgetItem(str(valerian[i][2])))
                elif(j==3):
                    self.top3Table.setItem(i,j,QTableWidgetItem(str(valerian[i][3])))
                elif(j==4):
                    self.top3Table.setItem(i,j,QTableWidgetItem(str(valerian[i][4])))
                elif(j==5):
                    self.top3Table.setItem(i,j,QTableWidgetItem(str(valerian[i][5])))
                elif(j==6):
                    self.top3Table.setItem(i,j,QTableWidgetItem(str(valerian[i][6])))
                elif(j==7):
                    self.top3Table.setItem(i,j,QTableWidgetItem(str(valerian[i][7])))
                elif(j==8):
                    self.top3Table.setItem(i,j,QTableWidgetItem(str(valerian[i][8])))
                elif(j==9):
                    self.top3Table.setItem(i,j,QTableWidgetItem(str(valerian[i][9])))
                elif(j==10):
                    self.top3Table.setItem(i,j,QTableWidgetItem(str(valerian[i][10])))
                elif(j==11):
                    self.top3Table.setItem(i,j,QTableWidgetItem(str(valerian[i][11])))
                elif(j==12):
                    self.top3Table.setItem(i,j,QTableWidgetItem(str(valerian[i][12])))
                elif(j==13):
                    self.top3Table.setItem(i,j,QTableWidgetItem(str(valerian[i][13])))
        conn.commit()
        conn.close()
    def extractHorseInfo(self,soup,horseTot,bDrawList): #extraction of horse's information
        self.statusbar.showMessage('Extracting raw data')
        idval='horse' #a necessary variable for creating a soup
        horseDiv=[]
        #city name
        quesCity=soup.find('div',style=re.compile(r'color: #643A90; font-size: 3.5em; z-index: 1; font-weight: bold'))
        cityName=quesCity.text #extracting the name of the city
        #race name
        quesRace=soup.find('div',style=re.compile(r'color: #6B389E; font-size: 1.7em; z-index: 1; font-weight: bold'))
        raceName=quesRace.text #extracting the name of the race
        self.statusbar.showMessage('Extracting race data')
        raceName=raceName[0:raceName.index('-')] #string operation to extract the particular race id
        #print (raceName)
        filename=cityName+'_'+raceName+'_'+time.strftime("%d-%m-%Y")
        '''with open(filename,'w+',newline='') as csvfile: #initiation of the raw data file
            writer=csv.DictWriter(csvfile,fieldnames=['Sl.no','weightVal','oddVal','nameVal','resVal','prevVal','distanceVal','ratingVal','jockeyVal','trainerVal','drawVal'],delimiter=',')
            writer.writeheader()'''
        for i in range(horseTot):
            questions=soup.find('div',class_='row',id=idval+str(i+1))
            horseDiv.append(questions) #collecting each row of horse
        #print ("len of horseDiv",len(horseDiv))
        #print ("horseDiv" , horseDiv)
        self.statusbar.showMessage('Extracting horse info')
        for i in range(len(horseDiv)):
            weightVal,oddVal,nameVal,allRes,allPrev,distanceVal,ratingVal,jockeyVal,trainerVal,drawVal,stakesVal,totalRunsVal=self.extractValue(horseDiv[i],i) #SECOND MOST IMPORTANT FUNCTION: extract our required values
            self.inputInDatabase(i+1,filename,cityName,raceName,weightVal,oddVal,nameVal,allRes,allPrev,distanceVal,ratingVal,jockeyVal,trainerVal,drawVal,stakesVal,totalRunsVal) #just to input into raw file
        #print(filename + ' data stored in db')
        self.statusbar.showMessage('Horse info extracted')
        dbNamor=self.generateAnalysis(filename,bDrawList) #THIS IS THE MOST IMPORTANT PART: extract values from the generated raw file and perform analysis
        #print('Analysis generated and saved as '+filename)
        return dbNamor
    def inputInDatabase(self,sl,filename,cityName,raceName,weightVal,oddVal,nameVal,allRes,allPrev,distanceVal,ratingVal,jockeyVal,trainerVal,drawVal,stakesVal,totalRunsVal): #function to store the raw data in database (I used csv for convenience)
        self.statusbar.showMessage('Inputing raw data in database')
        resVal=''
        prevVal=''
        if not (allRes==[]):
            for i in range(len(allRes)):
                resVal=resVal+allRes[i]+',' #processing the race history for storing
        else:
            resVal='NEW'

        if not (allPrev==None):
            for i in range(len(allPrev)):
                prevVal=prevVal+allPrev[i]+',' #processing the previous results for storing
        else:
            prevVal='NEW'
        
        #resVal = ",".join(allRes)
        #prevVal = ",".join(allPrev)

        temp=drawVal[0]+','+drawVal[1]

        # format table name
        #fname = filename  
        filename = filename.replace(" ", "_")
        filename = filename.replace("-","_")
        #print (filename)

        sql_1 = """CREATE TABLE IF NOT EXISTS """ + filename +  """ (serial_no INTEGER PRIMARY KEY UNIQUE ON CONFLICT ABORT, weightVal TEXT, oddVal TEXT, nameVal TEXT, resVal TEXT, prevVal TEXT,distanceVal TEXT,ratingVal TEXT,jockeyVal TEXT,trainerVal TEXT, drawVal TEXT,stakesVal TEXT,totalRunsVal TEXT)""" # create table for race

        params = (sl,weightVal,oddVal,nameVal,resVal,prevVal,distanceVal,ratingVal,jockeyVal,trainerVal,temp,stakesVal,totalRunsVal)
        sql_2 = """INSERT OR IGNORE INTO """+ filename + """ VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""" # insert data in table
        
        # db operations
        with sqlite3.connect('rawData.db') as conn:
            curs = conn.cursor()
            curs.execute(sql_1)
            curs.execute(sql_2.format(),params)
            conn.commit()           
        curs.close()
        conn.close()
        
        # csv operations
        '''with open(filename,'a',newline='') as csvfile:
            writer=csv.DictWriter(csvfile,fieldnames=['Sl.no','weightVal','oddVal','nameVal','resVal','prevVal','distanceVal','ratingVal','jockeyVal','trainerVal','drawVal'],delimiter=',') #creating a dict type variable for csv writing
            writer.writerow({'Sl.no':sl,'weightVal':weightVal,'oddVal':oddVal,'nameVal':nameVal,'resVal':resVal,'prevVal':prevVal,'distanceVal':distanceVal,'ratingVal':ratingVal,'jockeyVal':jockeyVal,'trainerVal':trainerVal,'drawVal':temp}) #writing in dict format'''  
        self.statusbar.showMessage('Raw data stored in db')
    def generateAnalysis(self,filename,bDrawList): #welcome to the most important part. to generate our analysis
        self.statusbar.showMessage('Analysis started')
        '''selectedRace = []
        selectedbDrawList = []

        drawVal = []

        #idval='horse'

        for i in range(len(self.par[0])):
            selectedRace.append(self.par[0][i])
            selectedbDrawList.append(self.bD[i][1])
            

        #print ("selectedRace len", len(selectedRace)
        # )
        #print ("selectedbDrawList len", len(selectedbDrawList))


        for i in range(len(selectedRace)):
            if selectedRace[i] == self.rce:
                bDrawList = selectedbDrawList[i]'''
            
        dataRows=[]
        horseOdds=[]
        horseRace=[]
        horseWeight=[]
        horseRating=[]
        stakes = []
        #print (filename)
        # print (self.rce)
        #print (self.par.index(self.rce))
        #self.par[0].index(self.rce)
        #print (self.rce)
        #print (self.par[self.par[0].index(self.rce)][0])
        

        #bDrawList = [self.par[0][1]]
        #print (bDrawList)
        #format table name
        #fname = filename[8:-4]  
        #filename = filename[8:-4] 
        
        filename = filename.replace(" ", "_")
        filename = filename.replace("-","_")
        #print (filename)

        with sqlite3.connect('rawData.db') as conn:
            conn.row_factory = sqlite3.Row
            curs = conn.cursor()
            curs.execute("SELECT * FROM " + filename)
            data = curs.fetchall()
            for row in data:
                #print(row)
                dataRows.append(row)
                horseOdds.append(row['oddVal'])
                horseRace.append(row['resVal'])
                horseWeight.append(row['weightVal'])
                horseRating.append(row['ratingVal'])
                stakes.append(row['stakesVal'])
        curs.close()
        conn.close()

        '''with open(filename) as csvfile: #creating a local dict variable dataRows
            reader = csv.DictReader(csvfile)
            for row in reader:
                dataRows.append(row)
                horseOdds.append(row['oddVal'])
                horseRace.append(row['resVal'])
                horseWeight.append(row['weightVal'])
                horseRating.append(row['ratingVal'])'''
        
        highestRating=0
        for i in range(len(horseRating)): #calculate and store the highest rating
            curVal=int(horseRating[i])
            if not (curVal==-1):
                if(curVal>highestRating):
                    highestRating=curVal 
        #print (highestRating)
        lowestWeight=500000
        for i in range(len(horseWeight)): #calculate and store the lowest horse weight
            temp=horseWeight[i]
            rDot=r','
            temp=re.sub(rDot,'.',temp)
            if (temp.find('-')==-1):
                val=float(temp[0:temp.index('k')])
            else:
                val=float(temp[0:temp.index('k')])
            if(val<lowestWeight):
                lowestWeight=val



        lowestOdds=500000
        for i in range(len(horseOdds)): #calculate and store the lowest odds
            temp=horseOdds[i]
            up=int(temp[temp.index('-')+1:temp.index('/')])
            down=int(temp[temp.index('/')+1:temp.rindex('-')])
            val=up/down
            if(val<lowestOdds):
                lowestOdds=val
            

        lowestRaceVal=450000 #calculate and store the lowest race value
        for i in range(len(horseRace)):
            if not (horseRace[i]=='NEW'):
                arr=horseRace[i].split(',')
                if(len(arr)>3):
                    a0=int(arr[0])*1
                    a1=int(arr[1])*2
                    a2=int(arr[2])*3
                    horseTotal=a0+a1+a2
                else:
                    horseTotal=0
                    for j in range(len(arr)-1):
                        horseTotal=horseTotal+int(arr[j])
                if(horseTotal<lowestRaceVal):
                    lowestRaceVal=horseTotal
            
        
        anaFile='analysisData/Analysis of '+filename
        anaArr=[] #array with the processed analytical result

        for i in range(len(dataRows)):
            jockeyVal=dataRows[i]['jockeyVal'] #jockey values
            trainerVal=dataRows[i]['trainerVal'] #trainer values

            if not (jockeyVal==''):
                totalJockeyRace=int(jockeyVal[jockeyVal.index('*')+1:jockeyVal.index(':')])
                totalJockeyWin=int(jockeyVal[jockeyVal.index(':')+1:jockeyVal.index('-')])
                jockeyDet=totalJockeyWin/totalJockeyRace #analyzed jockey rating
            else:
                jockeyDet=0

            if not (trainerVal==''):
                totalTrainerRace=int(trainerVal[trainerVal.index('*')+1:trainerVal.index(':')])
                totalTrainerWin=int(trainerVal[trainerVal.index(':')+1:trainerVal.index('-')])
                if totalTrainerRace == 0:
                    trainerDet = 0
                else:
                    trainerDet=totalTrainerWin/totalTrainerRace #analyzed trainer rating    
            else:
                trainerDet=0

            resVal=dataRows[i]['resVal']

            if not (resVal=='NEW'): #I stored in the dict array in such a way if the horse is new then this keyword will be stored
                horseNo=0.88 #horseno rating
            else:
                horseNo=0.12 #horseno rating
            
            oddVal=dataRows[i]['oddVal']
            up=int(oddVal[oddVal.index('-')+1:oddVal.index('/')])
            down=int(oddVal[oddVal.index('/')+1:oddVal.rindex('-')])

            val=up/down
            odds=lowestOdds/val #odds rating

            if not (resVal=='NEW'):
                arr=resVal.split(',')
                if(len(arr)>3):
                    a0=int(arr[0])*1
                    a1=int(arr[1])*2
                    a2B=int(arr[2])*3
                    horseTotal=a0+a1+a2
                else:
                    horseTotal=0
                    for j in range(len(arr)-1):
                        horseTotal=horseTotal+int(arr[j])
                if(horseTotal==0):
                    last3=0.00 #last3 rating
                else:
                    last3=lowestRaceVal/horseTotal #last3 rating
            else:
                last3=0.00

            distanceVal=dataRows[i]['distanceVal']
            totalRace=int(distanceVal[0:distanceVal.index(':')])
            totalWin=distanceVal[distanceVal.index(':')+1:]
            totalWin=int(totalWin[0:totalWin.index('-')])

            #total runs calc
            totalRunsVal=dataRows[i]['totalRunsVal']
            totalRuns1=int(totalRunsVal[0:totalRunsVal.index(':')])
            totalRuns2=totalRunsVal[totalRunsVal.index(':')+1:]
            totalRuns2=int(totalRuns2[0:totalRuns2.index('-')])

            #stakes calc
            stakesVal = dataRows[i]['stakesVal']
            if not stakesVal == '':
                stakesVal = stakesVal[stakesVal.index('R')+1:]
                stakesVal = int(stakesVal[0:])
            else:
                stakesVal = None
            #print (stakesVal)
            #draw=totalWin/100 #draw rating
            drawValue=dataRows[i]['drawVal']
            tempDraw=drawValue.split(',')
            jibonDraw=int(tempDraw[1])
            jibonPos=int(tempDraw[0])
            #print(jibonDraw)
            #print(jibonPos)
            draw=0
            for e in range(len(bDrawList)):
                tempIntPos=int(bDrawList[e][0])
                if(tempIntPos==jibonDraw):
                    draw=int(bDrawList[e][1])
                    draw=draw/100
                    break
            #draw=draw
            

            if not (totalWin==0): #special treatment for horses with no win
                distance=totalRace/totalWin #distance rating
            else:
                distance=0

            if not (totalRuns2==0): #special treatment for horses with no win
                totRuns=totalRuns2/totalRuns1 #distance rating
            else:
                totRuns=0
            

            weightVal=dataRows[i]['weightVal']
            rDot=r','
            weightVal=re.sub(rDot,'.',weightVal)
            if (weightVal.find('-')==-1):
                valw=float(weightVal[0:weightVal.index('k')])#only taking the number
            else:
                valw=float(weightVal[0:weightVal.index('k')])#only taking the number

            weightRate=lowestWeight/valw #weight value

            ratingVal=dataRows[i]['ratingVal']
            if not(highestRating==0):
                if not (int(ratingVal)==-1):
                    rating=int(ratingVal)/highestRating #rating value
                else:
                    rating=0
            else:
                rating=0
            odds=odds*0.03306
            totalFactor=rating+weightRate+distance+draw+last3+horseNo+odds+jockeyDet+trainerDet #total factor value 
            anaArr.append({'Sl.no':i,'name':dataRows[i]['nameVal'],'jockey':jockeyDet,'trainer':trainerDet,'horseNo':horseNo,'odds':odds,'last3':last3,'draw':draw,'distance':distance, 'total runs':totRuns,'weightRate':weightRate,'rating':rating,'stakes':stakesVal,'totalFactor':totalFactor})

        
        #print (anaArr)
        stakesArr = []
        stakesArrNo = []
        for i in range(len(anaArr)):
            if not anaArr[i]['stakes'] == None:
                stakesArr.append(anaArr[i]['stakes'])
                stakesArrNo.append(anaArr[i]['stakes'])
            else:
                stakesArr.append(None)

        #print(stakesArr)
        stake_final = []
        for i in range(len(stakesArr)):
            if stakesArr[i] == None:
                stake_final.append(0)
            else:
                stake_final.append(stakesArr[i]/max(stakesArrNo))
        

        #print (stake_final)
        #table name
        
        anaFname = anaFile[13:]
        anaFname = anaFname.replace(" ", "_")
        anaFname = anaFname.replace("-","_")
        #print (anaFile)
        #print (anaFname)

        sql_1 = """CREATE TABLE IF NOT EXISTS """ + anaFname +  """ (serial_no INTEGER PRIMARY KEY UNIQUE ON CONFLICT ABORT, name TEXT, jockey DOUBLE, trainer DOUBLE, horseNo DOUBLE, odds DOUBLE,last3 DOUBLE,draw DOUBLE,distance DOUBLE, totRuns DOUBLE, weightRate DOUBLE, rating DOUBLE, stakes DOUBLE, totalFactor DOUBLE)""" # create table for race

        sql_2 = """INSERT OR IGNORE INTO """+ anaFname + """ VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""" # insert data in table

        #round off the values
       
        for i in range(len(anaArr)):
            params = (anaArr[i]['Sl.no']+1,anaArr[i]['name'],round(anaArr[i]['jockey'],3),round(anaArr[i]['trainer'],3),anaArr[i]['horseNo'],round(anaArr[i]['odds'],3),round(anaArr[i]['last3'],3),anaArr[i]['draw'],anaArr[i]['distance'],round(anaArr[i]['total runs'],3),round(anaArr[i]['weightRate'],3),round(anaArr[i]['rating'],3),round(stake_final[i],3),round(anaArr[i]['totalFactor']+stake_final[i],4))

            #db connection
            with sqlite3.connect('analysisData.db') as conn:
                curs = conn.cursor()
                curs.execute(sql_1)
                curs.execute(sql_2.format(),params)
                conn.commit()
        curs.close()
        conn.close()
           
            

        #sortedArr=self.sort(anaArr) not necessary        
        '''with open(anaFile,'w+',newline='') as opFile: #starting to write the analysis file
            writer=csv.DictWriter(opFile,fieldnames=['Sl. no','name','jockey','trainer','horseNo','odds','last3','draw','distance','weightRate','rating','totalFactor'],delimiter=',')
            writer.writeheader()
            for i in range(len(anaArr)): #writing the dict file
                writer.writerow({'Sl. no':anaArr[i]['Sl.no']+1,'name':anaArr[i]['name'],'jockey':anaArr[i]['jockey'],'trainer':anaArr[i]['trainer'],'horseNo':anaArr[i]['horseNo'],'odds':round(anaArr[i]['odds'],3),'last3':round(anaArr[i]['last3'],3),'draw':anaArr[i]['draw'],'distance':anaArr[i]['distance'],'weightRate':round(anaArr[i]['weightRate'],3),'rating':round(anaArr[i]['rating'],3),'totalFactor':anaArr[i]['totalFactor']})'''
        self.statusbar.showMessage('Analysis complete')
        return anaFname
    def barrierChart(self,link):
        self.statusbar.showMessage('Retrieving the barrier chart info')
        with contextlib.closing(urllib.request.urlopen(link)) as r:
            soup=BeautifulSoup(r,'lxml')
        div=soup.findAll('div',class_='col-sm-6')
        n=len(div)
        #print(n)
        barrierGraph=div[n-2]
        soup=BeautifulSoup(str(barrierGraph.contents),'lxml')
        script=soup.find('script')
        script=str(script)
        var=script[script.index('var s'):]
        var=var[var.index('[')+1:var.index(']')]
        li=var.split(',')
        ##for i in range(len(li)):
        ##    print(li[i])
        regex=r'(?<=a: )[0-9]+'

        scoreList=[]
        index=0;
        for i in range(1,len(li),2):
            m=re.search(regex,li[i])
            index=index+1
            scoreList.append([index,m.group(0)])
##        for i in range(len(scoreList)):
##            print(scoreList[i])
        self.statusbar.showMessage('Barrier chart info retrieved')
        return scoreList
    def extractValue(self,horseDiv,no):
        #print(horseDiv)
        soup=BeautifulSoup(str(horseDiv),'lxml') #entering into a horse's row
        questions=soup.div # get the div elements
        #print(questions.contents)
        #some necessary regular expression based on the website layout. as you can see the variables has been named according to the relevant data to be extracted
        oddRegex=r'(?<=<div style="font-weight: bold; font-size: 1.3em;">)[0-9/]+'
        horseRegex=r'(?<=<div class="horseHeader" id="header'+re.escape(str(no+1))+r'">)[A-Za-z0-9 ]+'
        ratingRegex=r'(?<=<div style="font-weight: bold; font-size: 1.3em; display: block; background: #643A90; color: #fff; margin-top: 4px; padding: 2px; border-radius: 4px;">)[0-9]+'
        #stakesRegex = r'(?<=<div style="color: #643A90; font-size: 1.2em; margin: 4px; margin-left: 0;">)[0-9]+'
        

        #weight extraction
        prevLinOfWeight='<div style="color: #643A90; font-weight: bold; text-align: center; font-size: 1.7em; margin-top: 30px">'
##        text=str(questions.contents)
##        #print(text)
##        text=text[text.index(prevLinOfWeight)+2:text.index('kg')]
##        rBlank=r' '
##        weightVal=re.sub(rBlank,'',text)
        weightDiv=soup.find('div',style=re.compile(r'color: #643A90; font-weight: bold; text-align: center; font-size: 1.7em; margin-top: 30px'))
        weightVal=weightDiv.text
        rBlank=r' '
        rNew=r'\n'
        weightVal=re.sub(rBlank,'',weightVal)
        weightVal=re.sub(rNew,'',weightVal) #extracted raw weight value (will be processed later)

        

        #odd extraction
        text=str(questions.contents)
        m=re.search(oddRegex,text)
        oddVal=m.group(0)
        oddVal='-'+oddVal+'-' #extracted odds value (will be processed later)

        #Name extraction
        text=str(questions.contents)
        m=re.search(horseRegex,text)
        #print (m)
        nameVal=m.group(0)
        #print (nameVal)

        #resultExtraction
        allRes=[]
        rcHist=soup.findAll('div',class_='raceHistory')
        if not (rcHist==None):
            for j in range(len(rcHist)):
                allRes.append(rcHist[j].string) #extracted race history value (will be processed later)

        #previous runs
        allPrev=[]
        rcPrev=soup.findAll('div',class_='prev4Label')
        if not (rcPrev==None):
            for j in range(len(rcPrev)):
                allPrev.append(rcPrev[j].string) # extracted previous number of races


        #previous rating
        text=str(questions.contents)
        m=re.search(ratingRegex,text)
        if not (m==None):
            ratingVal=m.group(0) #extracted ratings value (will be processed later)
        else:
            ratingVal='-1' #some horses didn't have ratings. for them to identify I initiated with -1

        

        #distance extraction
        rcTable=soup.find('div',class_='col-sm-5')
        text=str(rcTable.contents)
        soupInterim=BeautifulSoup(text,'lxml')
        #print (soupInterim)
        rcDist=soupInterim.find('b',text='Distance').findNext('td')
        #print (rcDist)
        rBlank=r'\n'
        distanceVal=re.sub(rBlank,'',rcDist.text) #extracting distance value raw (will be processed later)



        #draw extraction
        soupInterim=BeautifulSoup(str(horseDiv),'lxml')        
        drawQ=soupInterim.findAll('div',class_='col-sm-1')
        drawQ=str(drawQ[len(drawQ)-1].contents)
        #print(drawQ)
        soupInterim2=BeautifulSoup(drawQ,'lxml')
        posQ=soupInterim2.find('b')
        scorePost=posQ.string #score position
        drawTemp=soupInterim2.find('div',style=re.compile(r'width: 90%; color: #643A90; font-size: 1.1em; border-bottom: 1px solid #ccc; margin: auto;'))
        drawPost=drawTemp.string #draw position
        drawVal=[scorePost,drawPost] 
        
        
        #JockeyAndTrainingExtraction
        rcTable=soup.findAll('div',class_='col-sm-2')
        n=len(rcTable)
        
        jockeyText=str(rcTable[n-2])
        trainerText=str(rcTable[n-1])
        #print (trainerText)
        
        soupInterim=BeautifulSoup(jockeyText,'lxml')
        jockxt=soupInterim.find('div',style=re.compile(r'color: #643A90; text-align: center; font-size: 1.2em;'))
        if not (jockxt==None):
            jockeyVal=jockxt.text #extracting raw jockey value (will be processed later)
        else:
            jockeyVal=''

        soupInterim=BeautifulSoup(trainerText,'lxml')
        trainxt=soupInterim.find('div',style=re.compile(r'color: #643A90; text-align: center; font-size: 1.2em;'))
        if not (trainxt==None):
            trainerVal=trainxt.text #extracting raw jockey value (will be processed later)
        else:
            trainerVal=''
        #trainerVal=jockeyText[1].text        #extracting raw trainer value (will be processed later)

        #stakes extraction
        rcTable=soup.find('div',class_='col-sm-7')
        text=str(rcTable.contents)
        soupInterim=BeautifulSoup(text,'lxml')
        #print (soupInterim)
        rcStakes=soupInterim.find('b',text='Stakes: ')
        #print (rcDist)
        if not rcStakes == None:
            rBlank=r'\n'
            stakesVal=re.sub(rBlank,'',rcStakes.next_sibling)
        else:
            stakesVal = ''

        #total runs
        rcTable=soup.find('div',class_='col-sm-7')
        text=str(rcTable.contents)
        soupInterim=BeautifulSoup(text,'lxml')
        #print (soupInterim)
        rcTotalRuns=soupInterim.find('b',text='Total Runs: ')
        #print (rcDist)
        if not rcTotalRuns == None:
            rBlank=r'\n'
            totalRunsVal=re.sub(rBlank,'',rcTotalRuns.next_sibling)
        else:
            totalRunsVal = ''

        # predicted finish: speed index, predicted time
        return weightVal,oddVal,nameVal,allRes,allPrev,distanceVal,ratingVal,jockeyVal,trainerVal,drawVal,stakesVal,totalRunsVal #returning the raw values

def main():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = WinningForm()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app
if __name__=='__main__':
    main()