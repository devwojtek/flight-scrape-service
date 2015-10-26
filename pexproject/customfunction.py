#!/usr/bin/env python
import os,sys
from subprocess import call
from bs4 import BeautifulSoup
from selenium import webdriver
import selenium
import datetime
from datetime import timedelta
import time
import MySQLdb
from selenium.webdriver.common.proxy import *
from datetime import date
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.db import connection,transaction
from pyvirtualdisplay import Display
import socket
import urllib

def united(origin,destination,searchdate,searchkey):
    cursor = connection.cursor()
    url = "http://www.united.com/web/en-US/default.aspx?root=1"
    display = Display(visible=0, size=(800, 600))
    display.start()
    chromedriver = "/usr/bin/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    dt = datetime.datetime.strptime(searchdate, '%Y/%m/%d')
    date = dt.strftime('%m/%d/%Y')
    #curdate = datetime.date.today() + datetime.timedelta(days=10)
    #date = curdate.strftime('%m/%d/%Y')
    currentdatetime = datetime.datetime.now()
    time = currentdatetime.strftime('%Y-%m-%d %H:%M:%S')
    #print date
    driver.get(url)
    driver.implicitly_wait(20)
    oneway = driver.find_element_by_id("ctl00_ContentInfo_Booking1_rdoSearchType2")
    driver.execute_script("arguments[0].click();", oneway)


    #driver.find_elements_by_css_selector("input[type='radio'][value='rdoSearchType2']")[0].click()

    #test = driver.find_elements_by_css_selector("label[for='ctl00_ContentInfo_Booking1_rdoSearchType2']")[0]
    #test.send_keys(Keys.ENTER)
    inputElement = driver.find_element_by_id("ctl00_ContentInfo_Booking1_Destination_txtDestination")
    inputElement.clear()
    inputElement.send_keys(destination)

    inputElement1 = driver.find_element_by_id("ctl00_ContentInfo_Booking1_Origin_txtOrigin")
    inputElement1.clear()
    inputElement1.send_keys(origin)

    driver.find_element_by_id("ctl00_ContentInfo_Booking1_SearchBy_rdosearchby3").click()
    inputElement2 = driver.find_element_by_id("ctl00_ContentInfo_Booking1_DepDateTime_Depdate_txtDptDate")
    inputElement2.clear()
    inputElement2.send_keys(date)

    inputElement2.send_keys(Keys.ENTER)

    driver.implicitly_wait(20)
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "rewardSegments")))
    except:
        display.stop()
        driver.quit()
        return searchkey
    
    html_page = driver.page_source

    soup = BeautifulSoup(html_page)
    table = soup.findAll("table",{"class":"rewardResults"})
    i= 1
    fltno =''
    searchid = searchkey
    fltno =''
    source=''
    Destination = ''
    arivalformat1 = ''
    departdetails=''
    arivedetails=''
    planedetails=''
    test1 =''
    operatedbytext =''
    stop = 0
    for trs in table:
        trblock = trs.findAll("tr")
        for tds in trblock:
            tdsegblock = tds.findAll("td",{"class":"tdSegmentBlock"})
            for datablock in tdsegblock:
                contenttr = datablock.findAll("tr")
                blocklenght = len(contenttr)
                for m in range(0,blocklenght):
                    stop = 0
                    departdlist = []
                    arivelist= []
                    planelist= []
                    operatedby=[]
                    for content in contenttr:
                        if content.find("td",{"class":"tdDepart"}):
                            stop = stop+1
                            print "==================================================================================="
                            departinfo = content.find("td",{"class":"tdDepart"})
                            info = departinfo.findAll("div")
                            depart = info[1].text
                            departdate= info[2].text
                            #print "Departdate", departdate
                            depart = depart.replace(".","")
                            test = (datetime.datetime.strptime(depart,'%I:%M %p'))
                            source1 = info[3].text
                            flightdetail = content.find("td",{"class":"tdSegmentDtl"})
                            fltno1 = flightdetail.find("div").text
                            operatedby1 = flightdetail.find("div",{"class":"ocMsg"}).text
                            if 'Operated by' in operatedby1:
                                operatedby1 = operatedby1.replace('Operated by','')
                            operatedby.append(operatedby1)
                            if stop == 1:
                                test1 = test.strftime('%H:%M')
                                source2 = source1.split('(')
                                source3 = (source2[1].replace(')','')).split('-')
                                source = source3[0]
                                fltno = fltno1
                            
                            departdetail=departdate.replace('.,',"")+" | "+depart+"  from   "+source1
                            departdlist.append(departdetail)
                            
                            arivinfo = content.find("td",{"class":"tdArrive"})
                            ainfo = arivinfo.findAll("div")
                            arival = ainfo[1].text
                            #print arival
                            arivedate = info[2].text
                            #print "arivedate",arivedate
                            
                            arival1 = arival.replace(".","").strip()
                            if '+' in arival1:
                                arival1 = arival1.split("+")
                                arival1 = arival1[0].strip()
                            arivalformat = (datetime.datetime.strptime(arival1,'%I:%M %p'))
                            arivalformat1 = arivalformat.strftime('%H:%M')
                            destination1 = ainfo[3].text
                            destination2 = destination1.split('(')
                            destination3 = (destination2[1].replace(')','')).split('-')
                            Destination = destination3[0]
                            
                            duration = content.find("td",{"class":"tdTrvlTime"})
                            traveltime = duration.find("span").text
                            #print "traveltime",traveltime
                            if 'Travel Time:' in traveltime:
                                traveltime = traveltime.replace('Travel Time:','')
                                
                            
                            fltno2 = fltno1.replace('Flight:','')
                            
                            
                            
                            
                            if duration.find("span",{"class":"PHead"}):
                                totaltime = duration.find("span",{"class":"PHead"}).text
                            if traveltime == '':
                                traveltime = totaltime
                            planecontent = fltno2+"  |  "+traveltime.replace('Flight Time:','')
                            planelist.append(planecontent)
                            traveltime = duration.findAll("span")
                            for timetext in traveltime:
                                print timetext.text
                            arivedetail = arivedate.replace('.,',"")+" | "+arival+"  at   "+destination1
                            arivelist.append(arivedetail)
                            """
                            flightdetail = content.find("td",{"class":"tdSegmentDtl"})
                            fltno = flightdetail.find("div").text
                            print fltno
                            """
                    #duration = ''
                    #for flno in flightdetail:
                        #print flno.find("div").text
                    #print content.find("td",{"class":"tdSegmentDtl"}).text
                    departdetails='@'.join(departdlist)
                    arivedetails='@'.join(arivelist)
                    planedetails='@'.join(planelist)
                    operatedbytext='@'.join(operatedby)
                j = 0
                k = 0
                cabin = []
                fare1 = 0
                fare2 = 0
                fare3 = 0
                cabintype1 = ''
                cabintype2 = ''
                cabintype3 = ''
                extramile =''
                extratax = []
                maintax = 0
                businesstax =0
                firsttax = 0
                tdblock = tds.findAll("td",{"class":"tdRewardPrice"})
                for mileage in tdblock:
                    j = j+1
                    k = k+1
                    
                    miles = mileage.find("div",{"class":"divMileage"}).text
                    miles = miles.replace(",", "")
                    splitmiles = miles.split(' ') 
                    miles = splitmiles[0].strip() 
                   
                    if mileage.find("div",{"class":"divTaxBreakdownA"}):
                        extramile = mileage.find("div",{"class":"divTaxBreakdownA"}).text
                        extramile = extramile.split("and")
                        extramile = extramile[1].strip()
                        extramile = extramile.replace('$','')
                        extratax.append(extramile)
                    else:
                        extratax.append('')
                        
                    '''
                    else:
                        notavl = mileage.find("div",{"class":"divNA"}).text
                        miles = notavl.strip()
                    '''
                     
                    if miles != "NotAvailable":
                        cabin.append(miles)
                    else:
                        cabin.append('')
                    #print "K val =",k
                    if j == 2:
                        #cabinval = "|".join(cabin)
                        if k == 2:
                            if cabin[0]:
                                fare1 = cabin[0]
                                maintax = extratax[0]
                            else:
                                if(cabin[1]):
                                    fare1 = cabin[1]
                                    maintax = extratax[1]
                            #print fare1
                            if fare1:
                                cabintype1 = "Economy"
                            else:
                                cabintype1 = ""
                            
                            cabin =[]
                            extratax = []
                           
                        if k == 4:
                            if cabin[0]:
                                fare2 = cabin[0]
                                businesstax = extratax[1]
                            else:
                                if(cabin[1]):
                                    fare2 = cabin[1]
                                    businesstax = extratax[1]
                            if fare2:
                                cabintype2 = "Business"
                            else:
                                cabintype2 = ""
                            cabin =[]
                            extratax = []
                            #print cabintype2,fare2
                           
                        if k == 6:
                            if cabin[0]:
                                fare3 = cabin[0]
                                firsttax = extratax[0]
                            else:
                                if(cabin[1]):
                                    fare3 = cabin[1]
                                    firsttax = extratax[1]
                            if fare3:
                                cabintype3 = "First"
                            else:
                                cabintype3 = ""
                                #cabintype3 = "first two row"
                            cabin =[]
                            extratax = []
                        j=0        
                if stop-1 < 1:
                    stopage = "NONSTOP"
                elif stop-1 == 1:
                    stopage = "1 STOP"
                else:
                    if stop-1 == 2:
                        stopage = "2 STOPS"
                #print fare1,fare2
                cursor.execute ("INSERT INTO pexproject_flightdata (flighno,searchkeyid,scrapetime,stoppage,stoppage_station,origin,destination,departure,arival,duration,maincabin,maintax,firstclass,firsttax,business,businesstax,cabintype1,cabintype2,cabintype3,datasource,departdetails,arivedetails,planedetails,operatedby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", (fltno,str(searchid),time,stopage,"test",source,Destination,test1,arivalformat1,totaltime,str(fare1),str(maintax),str(fare2),str(businesstax),str(fare3),str(firsttax),cabintype1,cabintype2,cabintype3,"united",departdetails,arivedetails,planedetails,operatedbytext))
                transaction.commit()
                print "row inserted"
    display.stop
    driver.quit()
    return searchid

	#call(["pgrep chrome | xargs kill"])	
def delta(orgn,dest,searchdate,searchkey):
    cursor = connection.cursor()
    url ="http://www.delta.com/"   
    searchid = str(searchkey)
    currentdatetime = datetime.datetime.now()
    time = currentdatetime.strftime('%Y-%m-%d %H:%M:%S')
    print orgn, dest
    try:
    	display = Display(visible=0, size=(800, 600))
    	display.start()
    	chromedriver = "/usr/bin/chromedriver"
    	os.environ["webdriver.chrome.driver"] = chromedriver
    	chrome_options = Options()
    	#chrome_options = webdriver.ChromeOptions()
    	#chrome_options.add_argument('--enable-alternative-services')
    	print "option"
       	driver = webdriver.Chrome(chromedriver)
        print "oneway"
    	driver.implicitly_wait(20)
    	driver.get(url)
    	oneway = driver.find_element_by_id('oneWayBtn')
    	driver.execute_script("arguments[0].click();", oneway)
    	
    	origin = driver.find_element_by_id("originCity")
    	origin.clear()
    	origin.send_keys(orgn.strip())
    	destination = driver.find_element_by_id("destinationCity")
    	destination.send_keys(dest.strip())
    
    	ddate = driver.find_element_by_id("departureDate")#.click()
    	ddate.send_keys(str(searchdate))
    	'''
    	if returndate:
        	returndate = driver.find_element_by_id("returnDate")#.click()
        	returndate.send_keys(date1)
    	'''
    	#driver.find_element_by_id("departureDate").click()
    	#driver.find_elements_by_css_selector("td[data-date='"+date+"']")[0].click()
    
    	driver.find_element_by_id("milesBtn").send_keys(Keys.ENTER)
    	driver.find_element_by_id("findFlightsSubmit").send_keys(Keys.ENTER)
	    
    except:
        display.stop
    	driver.quit()
    	return searchkey
    try:
        print "test1"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "_fareDisplayContainer_tmplHolder")))
    except:
        print "exception"
        display.stop()
        driver.quit()
        return searchkey
    
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "showAll")))
        driver.find_element_by_link_text('Show All').click()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "fareRowContainer_20")))
    except:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "fareRowContainer_0")))
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "fareRowContainer_0")))
    html_page = driver.page_source
    soup = BeautifulSoup(html_page)
    datatable = soup.findAll("table",{"class":"fareDetails"})
    n=0
    for content in datatable:
        detailid = content.find("div",{"class":"detailLinkHldr"})['id']
        driver.execute_script("document.getElementById('"+detailid+"').click()")
        driver.implicitly_wait(2)
        page = driver.page_source
        soup2 = BeautifulSoup(page)
        datatable1 = soup2.findAll("table",{"class":"fareDetails"})
        k=0
        departdetails=[]
        arrivedetails=[]
        planedetails=[]
        operatedbytext=''
        for cnt in datatable1:
            if cnt.find("div",{"class":"detailsRow" }) and k==n:
                detailblk = cnt.findAll("div",{"class":"detailsRow"})
                for tmp in detailblk:
                    print "----------------------------------"
                    spaninfo =  tmp.findAll("p")
                    departdetails.append((spaninfo[0].text).replace('DEPARTS',''))
                    arrivedetails.append(spaninfo[1].text.replace('ARRIVES',''))
                    planedetails.append(spaninfo[2].text.replace('FLIGHT',''))
            k=k+1
        n=n+1
        tds = content.findAll("td")
        detailsblock = tds[0]
        economy = tds[1]
        if len(tds) > 2:
            business = tds[2]
        else:
            business = ''

        cabintype2 =''
        fare2 = 0
        timeblock = detailsblock.findAll("div",{"class":"flightDateTime"})
        for info in timeblock:
            temp = info.findAll("span")
            depature = temp[0].text
            part = depature[-2:]
            depature1 = depature.replace(part, "")
            depaturetime = depature1+" "+part
            print depaturetime
            test = (datetime.datetime.strptime(depaturetime,'%I:%M %p'))
            test1 = test.strftime('%H:%M')
            print test1
            arival = temp[3].text
            apart =  arival[-2:]
            arival = arival.replace(apart, "")
            arivaltime = arival+" "+apart
            arivalformat = (datetime.datetime.strptime(arivaltime,'%I:%M %p'))
            arivalformat1 = arivalformat.strftime('%H:%M')
            duration = temp[4].text
            
        flite_route = detailsblock.findAll("div",{"class":"flightPathWrapper"})
        fltno = detailsblock.find("a",{"class":"helpIcon"}).text
        print 
        for route in flite_route:
            if route.find("div",{"class":"nonStopBtn"}):
                stp = "NONSTOP"
                lyover = ""
                #print "nonstop"
            else:
                if route.find("div",{"class":"nStopBtn"}):
                    stp = route.find("div",{"class":"nStopBtn"}).text
                    #print route.find("div",{"class":"nStopBtn"}).text
                    if route.find("div",{"class":"layOver"}):
                        lyover = route.find("div",{"class":"layOver"}).text
                    elif route.find("div",{"class":"originCityVia2Stops"}):
                        multistop = route.findAll("div",{"class":"originCityVia2Stops"})
                        stoplist =[]
                        for sp in multistop:
                            stoplist.append(sp.text)
                        lyover="|".join(stoplist)
                    else:
                        lyover=''
                    #print route.find("div",{"class":"layOver"}).find("span").text
                    #print route.find("div",{"class":"layovertoolTip"}).text
                    #layover.append(lyover)
            sourcestn = (route.find("div",{"class":"originCity"}).text)
            destinationstn = (route.find("div",{"class":"destinationCity"}).text)
        print "-------------------- Economy--------------------------------------------------"
        economytax = 0
        businesstax = 0
        fare3 =0
        firsttax = 0
        cabintype3 =''
        if economy.findAll("div",{"class":"priceHolder"}):
            fare1 = economy.find("span",{"class":"tblCntBigTxt mileage"}).text
            fare1 = fare1.replace(",","")
            if economy.find("span",{"class":"tblCntSmallTxt"}):
                economytax = economy.find("span",{"class":"tblCntSmallTxt"}).text
                economytax = economytax.split('$')
                economytax = economytax[1].strip()
            print economytax
            #lenght = len(fareblock)
            #print fareblock[0].text
            if economy.findAll("div",{"class":"frmTxtHldr flightCabinClass"}):
                cabintype1 = economy.find("div",{"class":"frmTxtHldr flightCabinClass"}).text
                if 'Main Cabin' in cabintype1:
                    cabintype1 = cabintype1.replace('Main Cabin','Economy')
                if 'Multiple Cabins' in cabintype1:
                    cabintype1 = cabintype1.replace('Multiple Cabins','Economy')
        else:
            fare1 = 0 #economy.find("span",{"class":"ntAvail"}).text
            cabintype1 =''
            
        print "-------------------- Business --------------------------------------------------"
        if business:

            if business.findAll("div",{"class":"priceHolder"}):
                fare2 = business.find("span",{"class":"tblCntBigTxt mileage"}).text
                fare2 = fare2.replace(",","")
                if business.find("span",{"class":"tblCntSmallTxt"}):
                    businesstax = business.find("span",{"class":"tblCntSmallTxt"}).text
                    businesstax = businesstax.split('$')
                    businesstax = businesstax[1].strip()
                print businesstax
                #lenght = len(fareblock)
                #print fareblock[0].text
                if business.findAll("div",{"class":"frmTxtHldr flightCabinClass"}):
                    cabintype2 = business.find("div",{"class":"frmTxtHldr flightCabinClass"}).text
                    
            else:
                fare2 = 0 #business.find("span",{"class":"ntAvail"}).text
                cabintype2 = ''
            if 'First' in cabintype2:
                fare3 = fare2
                fare2 = 0
                cabintype3 = cabintype2
                firsttax = businesstax
                cabintype2 =''
            else:
                cabintype2 = "Business"

        deptdetail = '@'.join(departdetails)
        arivedetail = '@'.join(arrivedetails)
        planetext = '@'.join(planedetails)
        #print 'arivedetail',arrivedetails
        #print 'plane', planedetails
        cursor.execute ("INSERT INTO pexproject_flightdata (flighno,searchkeyid,scrapetime,stoppage,stoppage_station,origin,destination,departure,arival,duration,maincabin,maintax,firstclass,firsttax,business,businesstax,cabintype1,cabintype2,cabintype3,datasource,departdetails,arivedetails,planedetails,operatedby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", (fltno,searchid,time,stp,lyover,sourcestn,destinationstn,test1,arivalformat1,duration,str(fare1),str(economytax),str(fare2),str(businesstax),str(fare3),str(firsttax),cabintype1.strip(),cabintype2.strip(),cabintype3,"delta",deptdetail,arivedetail,planetext,operatedbytext))
        transaction.commit()
        print "data inserted"


    
    display.stop()
    driver.quit()
    return searchkey

    
