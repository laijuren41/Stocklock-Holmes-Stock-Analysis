import MySQLdb
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from w3lib.html import remove_tags
import timeit
import mysql.connector
from mysql.connector import (connect)
import dateutil.parser
import time
import sys
from datetime import datetime
import csv
import numpy as np
import pandas as pd
from sklearn import linear_model,metrics
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


dbcon = mysql.connector.connect(user='root', password='root', host='localhost', database='stockfyp')

#datas used for predicting
now = datetime.now()
companyid = []
dateCollect = []

#checking if the companyid that the value passed in exist or not.-----------------------------------------
def checkValue(companyid):
    dbconnection = mysql.connector.connect(user='root', password='root', host='localhost', database='stockfyp')
    checkCursor = dbconnection.cursor(buffered = True)
    checking = 0
    sqlstmt = "select * from stock_info where company_ID = %(companyid)s"
    try:
        stmtVal = {'companyid':companyid}
        checkCursor.execute(sqlstmt,stmtVal)
        if checkCursor.fetchone():
            checkCursor.close()
            dbconnection.close()
            return 1
        else:
            checkCursor.close()
            dbconnection.close()
            return 0
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
#end--checkValue--------------------------------------------------------------------------------------

#calculating the coefficient to determine uptrend or downtrend-----------------------------
def calculateCoef(dates,prices,x):
    linear_mod = linear_model.LinearRegression() #defining the linear regression model
    dates = np.reshape(dates,(len(dates),1)) # converting to matrix of n X 1
    prices = np.reshape(prices,(len(prices),1))
    linear_mod.fit(dates,prices) #fitting the data points in the model
    predicted_price =linear_mod.predict(x)
    return predicted_price[0][0],linear_mod.coef_[0][0] ,linear_mod.intercept_[0]
#end--calculate coefficient------------------------------------------------------------------

#calculating the trends and insert into db----------------------------------
def calCoefandInsertIntoDB():
    #----declare variables-------
    stockpriceID=[]
    coefficient=[]
    days = [1,2,3,4,5,6,7,8,9,10]
    #end--declare variables------
    dbconnection = mysql.connector.connect(user='root', password='root', host='localhost', database='stockfyp')
    cursor = dbconnection.cursor(buffered = True)
    stmt = ("select company_ID,stockpriceID,priceDay1,priceDay2,priceDay3 from predicted_stock")
    try:
        cursor.execute(stmt)
        results = cursor.fetchall()
        for col in results:
            prices=[]
            compID = col[0]
            secondStmt = "select companyPrice from stock_info where company_ID = %(company_ID)s"
            stmtVal = {"company_ID":compID}
            cursor.execute(secondStmt,stmtVal)
            r = cursor.fetchall()
            count = 0
            for results in r:
                count+=1
            recentPriceCount = count - 7
            count = 0
            for results in r:
                if recentPriceCount <= count:
                    prices.append(results[0])
                count+=1
            prices.append(col[2])
            prices.append(col[3])
            prices.append(col[4])
            checkValue = results[0]
            same = True
            for li in prices:
                if li != checkValue:
                    same = False
                    break
            if same:
                coef = 0
            else:
                p,coef,intercept = calculateCoef(days,prices,11)
            try:
                cursor.execute("""update predicted_stock set coefficient=%s where stockpriceID=%s""",(float(coef),col[0]))
                if coef < 0:
                    string = "downtrend"
                    cursor.execute("""update predicted_stock set stock_trend=%s where stockpriceID=%s""",(string,col[0]))
                    #dbconnection.commit()
                elif coef > 0:
                    string = "uptrend"
                    cursor.execute("""update predicted_stock set stock_trend=%s where stockpriceID=%s""",(string,col[0]))
                    #dbconnection.commit()
                else:
                    string = "neutral"
                    cursor.execute("""update predicted_stock set stock_trend=%s where stockpriceID=%s""",(string,col[0]))
                    #adbconnection.commit()
            except (MySQLdb.Error, MySQLdb.Warning) as e:
                print(e)
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)

    cursor.close()
    dbconnection.close()
#end--calculating the coef n trend------------------------------------------------------------------------

def accuracy(dates,prices,companyid):
    linear_mod = linear_model.LinearRegression()
    date = dates
    price = prices
    dates = np.reshape(dates,(len(dates),1)) # converting to matrix of n X 1
    prices = np.reshape(prices,(len(prices),1))
    xtrain, xtest, ytrain, ytest = train_test_split(dates, prices,test_size = 0.33,random_state = 0)
    linear_mod.fit(xtrain,ytrain)
    p = linear_mod.predict(xtest)
    linscore = linear_mod.score(xtest,ytest)*100
    mse = np.mean((linear_mod.predict(xtest)-ytest)**2)
    rmse = np.sqrt(mse)
    print("company ID ---> " ,companyid," has a R-Squared value of  ---> ", linscore)
#this is the linear regression prediction-----------------------------------------------------------------
def predict_price(dates,prices,x):
    linear_mod = linear_model.LinearRegression() #defining the linear regression model
    dates = np.reshape(dates,(len(dates),1)) # converting to matrix of n X 1
    prices = np.reshape(prices,(len(prices),1))
    xtrain, xtest, ytrain, ytest = train_test_split(dates, prices, test_size=0.33, random_state=42)
    linear_mod.fit(xtrain,ytrain) #fitting the data points in the model
    predicted_price =linear_mod.predict(x)
    return predicted_price[0][0],linear_mod.coef_[0][0] ,linear_mod.intercept_[0]
#end--predict_price(dates,prices,x)-----------------------------------------------------------------------

#checking if the companyid that is passed in has any value on predictedstock table-------------------------
def checkDB(companyid):
    dbconnection = mysql.connector.connect(user='root', password='root', host='localhost', database='stockfyp')
    checkCursor = dbconnection.cursor(buffered = True)
    checking = 0
    sqlstmt = "select * from predicted_stock where company_ID = %(companyid)s"
    try:
        stmtVal = {'companyid':companyid}
        checkCursor.execute(sqlstmt,stmtVal)
        if checkCursor.fetchone():
            checkCursor.close()
            dbconnection.close()
            return 1
        else:
            checkCursor.close()
            dbconnection.close()
            return 0
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)

#end--checkDB(companyid)-----------------------------------------------------------------------------

#--calculating predicted price 3 days ahead-------------------------------------------------
def calculatePrice(firstDayPrice,companyID,nextDay):
    #dec variables-------------------------
    compID = []
    prices = []
    predictedPrices = []
    datecollect = []
    dbc = mysql.connector.connect(user='root', password='root', host='localhost', database='stockfyp')
    cursor = dbc.cursor()
    count = 1
    #--end--dec variables------------------

    #getting all the price and date from teststockinfo with companyID
    stmt = "select companyPrice,datetimecollect from stock_info where company_ID = %(companyID)s "
    stmtVal = {'companyID':companyID}
    cursor.execute(stmt,stmtVal)
    results = cursor.fetchall()
    for x in results:
        prices.append(float(x[0]))
        ori = str(x[1])
        splitOri = ori.split(" ")
        wholeDate = splitOri[0].split("-")
        day = wholeDate[2]
        datecollect.append(int(day))
    datecollect.append(nextDay)
    prices.append(firstDayPrice)
    predictedPrices.append(firstDayPrice)
    while count < 3:
        predicted_price, coefficient, constant = predict_price(datecollect,prices,nextDay)
        nextDay = nextDay + count
        newPrice = float(predicted_price)
        datecollect.append(nextDay)
        prices.append(newPrice)
        predictedPrices.append(newPrice)
        count += 1
    return predictedPrices
        
#end-----------------------------------------------------------------------------------------
    
    
#gets the price from stock_info then uses it to do predictions-----------------
def gettingPredictedPriceStocks():
    dbcnx = mysql.connector.connect(user='root', password='root', host='localhost', database='stockfyp')
    cursor = dbcnx.cursor()
    cursor.execute("select company_ID from stock_company")
    data = cursor.fetchall()

    for result in data:
        companyid.append(result[0])

    cursor.close()
    dbcnx.close()

    dbcnx = mysql.connector.connect(user='root', password='root', host='localhost', database='stockfyp')
    cursor = dbcnx.cursor()

    for companyids in companyid:
        predicted_priceFirstDay = 0
        companyPrices = []
        dateCollect = []
        predictPrice = []
        sqlstmtPrice = "select companyPrice,datetimecollect from stock_info where company_ID = %(companyID)s"
        try:
            if checkValue(companyids) == 1:
                stmtValue = {'companyID': companyids}
                cursor.execute(sqlstmtPrice,stmtValue)
                results = cursor.fetchall()
                for result in results:
                    companyPrices.append(float(result[0]))
                    originalTime = str(result[1])
                    splitOriginal = originalTime.split(" ")
                    splitTime = splitOriginal[0].split("-")
                    day = splitTime[2]
                    nextDay = now.day + 1
                    if nextDay > 31:
                        nextDay = 1
                    dateCollect.append(int(day))
                predicted_price, coefficient, constant = predict_price(dateCollect,companyPrices,nextDay)
                predicted_priceFirstDay = float(predicted_price)
                accuracy(dateCollect,companyPrices,companyids)
                predictPrice = calculatePrice(predicted_priceFirstDay,companyids,nextDay)
                
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print(e)
        if checkDB(companyids) == 1:
            try:
                valueToUpdate = {'companyids':companyids}
                cursor.execute("""update predicted_stock set priceDay1=%s, priceDay2=%s, priceDay3=%s where company_ID=%s""",(predictPrice[0],predictPrice[1],predictPrice[2],companyids))
                #dbcnx.commit()
            except (MySQLdb.Error, MySQLdb.Warning) as e:
                print(e)
        else:
            try:
                cursor.execute("""insert into predicted_stock (company_ID,priceDay1,priceDay2,priceDay3) VALUES (%s,%s,%s,%s)""",(companyids,predictPrice[0],predictPrice[1],predictPrice[2]))
               # dbcnx.commit()
            except(MySQLdb.Error,MySQLdb.Warning) as e:
                print(e)

    cursor.close()
    dbcnx.close()
#end--gettingPredictedPriceStocks-------------------------------------------------------

#getting the company id and code to be used in collecting data--- 
#variables and array used to store company_ID
companyIDArray=[]
keys = ['c_ID','c_CODE']

def gettingCompanyID():
    dbcnx = mysql.connector.connect(user='root', password='root', host='localhost', database='stockfyp')
    cursor = dbcnx.cursor()
    query = ("select company_ID,company_CODE from stock_company")
    cursor.execute(query)
    for(c_ID,c_CODE) in cursor:
        collected = [str(c_ID),str(c_CODE)]
        companyIDArray.append(dict(zip(keys,collected)))
    cursor.close()
    dbcnx.close()
    
#end--gettingCompanyID()------------------------------------------------------------

#checking if the the categories for that company has been collected or not-----------
def checkingExist(compID):
    dbc = mysql.connector.connect(user='root', password='root', host='localhost', database='stockfyp')
    checkCursor = dbc.cursor(buffered = True)
    checking = 0
    sqlstmt = "select company_Categories from stock_company where company_ID = %(companyID)s"
    try:
        stmtVal = {'companyID':compID}
        checkCursor.execute(sqlstmt,stmtVal)
        value = checkCursor.fetchall()
        for test in value:
            if not test[0]:
                checkCursor.close()
                dbc.close()
                return 0
            else:
                checkCursor.close()
                dbc.close()
                return 1
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
#end--checkingExist(compID)---------------------------------------------------------


#used to collect the categories in stockcompany table--------------
#if it is null it will collect and insert it into the table
def collectCategories():
    #arrays/ variables used/declared----------------------
    categoriesArr = []
    codeArr = []
    dbc = mysql.connector.connect(user='root',password='root',host='localhost',database='stockfyp')
    count = 0
    #--------------------------------------------
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    driver = webdriver.PhantomJS(desired_capabilities=dcap)
    driver.set_window_size(1920,1080)
    driver.get('https://www.klsescreener.com/v2/')
    #clicking the search button
    clickbtn = driver.find_element_by_xpath('//*[@id="submit"]')
    clickbtn.click()
    timeout = 10
    try:
        element_present = EC.presence_of_element_located((By.XPATH, "//td[@title='Code']"))
        WebDriverWait(driver, timeout).until(element_present)
        clickSort = driver.find_element_by_xpath("//th[@data-column='1']")
        clickSort.click()
        sleep(3)
        #collecting the categories
        for cat in driver.find_elements_by_xpath("//td[@title='Category'][text()]"):
            splitString = cat.text.split(",")
            categoriesArr.append(splitString[0])
        for code in driver.find_elements_by_xpath("//td[@title='Code'][text()]"):
            codeArr.append(code.text)
        for companycode in companyIDArray:
            if checkingExist(companycode['c_ID']) == 0:
                cursor = dbc.cursor(buffered=True)
                cursor.execute("""update stock_company set company_Categories = %s WHERE company_CODE = %s""",(categoriesArr[count-1],codeArr[count-1]))
                #dbc.commit()
            count+=1
    except TimeoutException:
        print("Timeout")
#end--------------------------------------------------------------            

#scraping all the necessary datas-----------------------------
def collectData():
    print(" Starting to collect the data from KLSEScreener ")
    start = timeit.default_timer()
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

    driver = webdriver.PhantomJS(desired_capabilities=dcap)

    driver.set_window_size(1920,1080)
    driver.get('https://www.klsescreener.com/v2/')
    #arrays used to store the data values that are scraped
    dArr = []
    dArrCleaned=[]
    codeArray = []
    categoryArray1=[]
    priceArray=[]
    volumeArray=[]
    epsArray=[]
    dpsArray=[]
    ntaArray=[]
    peArray=[]
    dyArray=[]
    roeArray=[]
    ptbvArray=[]
    MCapArray=[]


    #clicking the search button
    clickbtn = driver.find_element_by_xpath('//*[@id="submit"]')
    clickbtn.click()
    timeout = 10
    try:
        element_present = EC.presence_of_element_located((By.XPATH, "//td[@title='Code']"))
        WebDriverWait(driver, timeout).until(element_present)
        clickSort = driver.find_element_by_xpath("//th[@data-column='1']")
        clickSort.click()
        sleep(3)
       
    
        #collecting the values
        print("Collecting all the other values...")
        print("Collecting the prices...")
        for price in driver.find_elements_by_xpath("//td[contains(@title,'Price')][text()]"):
            priceArray.append(price.text)

        print("Collecting the volumes...")
        for volume in driver.find_elements_by_xpath("//td[@title = 'Volume'][text()]"):
            volumeArray.append(volume.text)

        print("Collecting the EPS values...")
        for eps in driver.find_elements_by_xpath("//td[@title = 'EPS']"):
            epsArray.append(eps.get_attribute('innerHTML'))

        print("Collecting the DPS values...")
        for dps in driver.find_elements_by_xpath("//td[@title = 'DPS']"):
            dpsArray.append(dps.get_attribute('innerHTML'))

        print("Collecting the NTA values...")
        for nta in driver.find_elements_by_xpath("//td[@title = 'NTA']"):
            ntaArray.append(nta.get_attribute('innerHTML'))

        print("Collecting the PE values...")
        for pe in driver.find_elements_by_xpath("//td[@title = 'PE']"):
            if "," in pe.text:
                petesting = ""
                arraySplit = pe.text.split(",")
                for words in arraySplit:
                    petesting += words
                peArray.append(petesting)
            else:
                peArray.append(pe.get_attribute('innerHTML'))

        print("Collecting the DY values...")
        for dy in driver.find_elements_by_xpath("//td[@title = 'DY']"):
            dyArray.append(dy.get_attribute('innerHTML'))


        for roe in driver.find_elements_by_xpath("//td[@title = 'ROE']"):
            if "," in roe.text:
                roetesting = ""
                arraySplit = roe.text.split(",")
                for words in arraySplit:
                    roetesting += words
                roeArray.append(roetesting)
            else:
                roeArray.append(roe.get_attribute('innerHTML'))
            
            

        print("Collecting the PTBV values...")
        for ptbv in driver.find_elements_by_xpath("//td[@title = 'PTBV']"):
            if "," in ptbv.text:
                ptbvtesting = ""
                arraySplit = ptbv.text.split(",")
                for words in arraySplit:
                    ptbvtesting += words
                ptbvArray.append(ptbvtesting)
            else:
                ptbvArray.append(ptbv.get_attribute('innerHTML'))

        print("Collecting the Market Capital values...")
        for mcap in driver.find_elements_by_xpath("//td[@title = 'Market Capital'][text()]"):
            MCapArray.append(mcap.text)
        print("Done...")
        
        #collecting the company codes
        print("Collecting the company codes...")
        for code in driver.find_elements_by_xpath("//td[@title='Code'][text()]"):
            codeArray.append(code.text)
        print("Done...")
        #collecting the categories
        print("Collecting the categories of each of the companies")
        for category in driver.find_elements_by_xpath("//td[@title='Category'][text()]"):
            categoryArray1.append(category.text)
            

        #checking if the value is null or have a ',' in the values
        #if they have a null value it is converted to 0
        #if they have a ',' it is stripped off
        testCount =0
        test1Count = 0

        for pe1 in peArray:
            if pe1 == "":
                peArray[test1Count] = 0.00
            if "," in pe1:
                peArray[test1Count].strip(',')
            test1Count += 1

        test1Count = 0
        
        for eps1 in epsArray:
                if eps1 == "":
                    epsArray[test1Count] = 0.00
                test1Count += 1

        test1Count = 0
        
        for dps1 in dpsArray:
                if dps1 == "":
                    dpsArray[test1Count] = 0.00
                test1Count += 1

        test1Count = 0
        
        for nta1 in ntaArray:
                if nta1 == "":
                    ntaArray[test1Count] = 0.00
                test1Count += 1

        test1Count = 0

        for dy1 in dyArray:
                if dy1 == "":
                    dyArray[test1Count] = 0.00
                test1Count += 1

        test1Count = 0
        
        for roe1 in roeArray:
                if roe1 == "":
                    roeArray[test1Count] = 0.00
                test1Count += 1

        test1Count = 0
        
        for ptbv1 in ptbvArray:
                if ptbv1 == "":
                    ptbvArray[test1Count] = 0.00
                if "," in ptbv1:
                    ptbvArray[test1Count].strip(',')
                test1Count += 1


        
        print("Done...")
        company_CODE = codeArray
        stop = timeit.default_timer()
        tTime = stop - start
        mins, secs = divmod(tTime,60)
        hours, mins = divmod(mins,60)
        datecollect = time.strftime("%Y-%m-%d %H:%M:%S")
        print(datecollect)
    except TimeoutException:
        print("Timed out waiting for page to load")
    #cursor for db operations
    cursor = dbcon.cursor()

    insert_into_stockcompanytable = ("INSERT INTO stock_info"
                                     "(companyPrice,companyVolume,companyEPS,companyDPS,companyNTA,companyPE,companyDY,companyROE,companyPTBV,companyMCAP,company_ID,datetimeCollect)"
                                     "VALUES (%(companyPrice)s, %(companyVolume)s, %(companyEPS)s, %(companyDPS)s, %(companyNTA)s, %(companyPE)s, %(companyDY)s, %(companyROE)s, %(companyPTBV)s, %(companyMCAP)s, %(company_ID)s,%(datetimeCollect)s)")

    count =0
    print("Inserting into the table...")
    #looping to insert the code and company name into the database
    while(count < len(codeArray)):
        if count >= len(codeArray):
            break
        cCode = codeArray[count]
        for companycode in companyIDArray:
            if cCode == companycode['c_CODE']:
                compid = companycode['c_ID']
                cPrice = priceArray[count]
                cVolume = volumeArray[count]
                cEPS = epsArray[count]
                cDPS = dpsArray[count]
                cNTA = ntaArray[count]
                cPE = peArray[count]
                cDY = dyArray[count]
                cROE = roeArray[count]
                cPTBV = ptbvArray[count]
                cMCAP = MCapArray[count]
                try:
                    stockinfo = {
                        'companyPrice': cPrice,
                        'companyVolume': cVolume,
                        'companyEPS': cEPS,
                        'companyDPS': cDPS,
                        'companyNTA': cNTA,
                        'companyPE': cPE,
                        'companyDY': cDY,
                        'companyROE': cROE,
                        'companyPTBV': cPTBV,
                        'companyMCAP': cMCAP,
                        'company_ID': compid,
                        'datetimeCollect': datecollect
                        }
                    cursor.execute(insert_into_stockcompanytable,stockinfo)
                except (MySQLdb.Error, MySQLdb.Warning) as e:
                    print(e)
                    return None
        count=count+1
        #dbcon.commit()

    driver.quit()
    print("Done...")
    return;

#end--collectData()--------------------------------------------------------



def main():

    
    gettingCompanyID()
    #collectCategories()
    collectData()
    gettingPredictedPriceStocks()
    calCoefandInsertIntoDB()
    return;


main()
