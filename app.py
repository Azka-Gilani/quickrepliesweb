#!/usr/bin/env python
import urllib
import urllib2
import json
import os
import re


from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)
QR=['0','1','2','3','4','5','6']

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "yahooWeatherForecast":
        return {}
    global QR
    global intent_name
    intent_name=processIntentName(req)
    city_names=processlocation(req)
    sector_names=processSector(req)
    property_type=processPropertyType(req)
    unit_property=processUnit(req)
    area_property=processArea(req)
    NoOfDays=processDate(req)
    DateUnit=processDateUnit(req)
    school=processSchool(req)
    malls=processMalls(req)
    transport=processTransport(req)
    security=processSecurity(req)
    airport=processAirport(req)
    fuel=processFuel(req)
    #minimum_value=processMinimum(req)
    maximum_value=processMaximum(req)
    latest=processLatestProperties(req)    
    #if minimum_value > maximum_value:
    #    minimum_value,maximum_value=maximum_value,minimum_value
    #else:
    # minimum_value,maximum_value=minimum_value,maximum_value
    if "GettingStarted" in intent_name or "BuyPlot" in intent_name:
        baseurl = "https://aarz.pk/bot/index.php?city_name=islamabad"
        result = urllib.urlopen(baseurl).read()
        data = json.loads(result)
        res = makeWebhookResult(data)
        
    else:
        baseurl = "https://aarz.pk/bot/index.php?city_name="+city_names+"&sector_name="+sector_names+"&minPrice="+maximum_value+"&type="+property_type+"&LatestProperties="+latest+"&UnitArea="+area_property+"&Unit="+unit_property+"&school="+school+"&airport="+airport+"&transport="+transport+"&security="+security+"&shopping_mall="+malls+"&fuel="+fuel
        result = urllib.urlopen(baseurl).read()
        data = json.loads(result)
        res = makeWebhookResult(data)
    return res

def processIntentName(req):
    result = req.get("result")
    parameters = result.get("metadata")
    intent = parameters.get("intentName")
    return intent

def processlocation(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("city")
    return city

def processSector(req):
    result = req.get("result")
    parameters = result.get("parameters")
    sector = parameters.get("Location")
    return sector

def processMinimum(req):
    result = req.get("result")
    parameters = result.get("parameters")
    minimum = parameters.get("number")
    return minimum

def processMaximum(req):
    result = req.get("result")
    parameters = result.get("parameters")
    maximum = parameters.get("number1")
    return maximum


def processPropertyType(req):
    result = req.get("result")
    parameters = result.get("parameters")
    propertyType = parameters.get("PropertyType")
    return propertyType

def processLatestProperties(req):
    result = req.get("result")
    parameters = result.get("parameters")
    latest = parameters.get("LatestProperties")
    return latest

def processUnit(req):
    result = req.get("result")
    parameters = result.get("parameters")
    unit = parameters.get("Unit")
    return unit

def processArea(req):
    result = req.get("result")
    parameters = result.get("parameters")
    area = parameters.get("AreaNumber")
    return area

def processDate(req):
    result = req.get("result")
    parameters = result.get("parameters")
    days = parameters.get("NoOfDays")
    return days

def processDateUnit(req):
    result = req.get("result")
    parameters = result.get("parameters")
    dayUnit = parameters.get("DayUnit")
    return dayUnit

def processSchool(req):
    result = req.get("result")
    parameters = result.get("parameters")
    school = parameters.get("school")
    return school

def processMalls(req):
    result = req.get("result")
    parameters = result.get("parameters")
    malls = parameters.get("malls")
    return malls

def processTransport(req):
    result = req.get("result")
    parameters = result.get("parameters")
    transport = parameters.get("transport")
    return transport

def processSecurity(req):
    result = req.get("result")
    parameters = result.get("parameters")
    security = parameters.get("security")
    return security

def processAirport(req):
    result = req.get("result")
    parameters = result.get("parameters")
    airport = parameters.get("airport")
    return airport

def processFuel(req):
    result = req.get("result")
    parameters = result.get("parameters")
    fuel = parameters.get("fuelstation")
    return fuel
   
def makeWebhookResult(data):
    i=0
    urlquick = "https://aarz.pk/bot/index.php?city_name="
    length=len(data)
    varibale1='34894'
    variable2='32289'
    variable3='433289'
    variable4='432190'
    row_id=['test','test1','test2','test3','test4','test5']
    row_city=['test','test1','test2','test3','test4','test5']
    row_title=['test','test1','test2','test3','test4','test5']
    row_location=['test','test1','test2','test3','test4','test5']
    row_price=['test','test1','test2','test3','test4','test5']
    row_slug=['test','test1','test2','test3','test4','test5']
    row_number=['test','test1','test2','test3','test4','test5']
    while (i <length):
        row_id[i]=data[i]['p_id']
        row_city[i]=data[i]['city']
        row_title[i]=data[i]['title']
        row_location[i]=data[i]['address']
        row_price[i]=data[i]['price']
        row_slug[i]=data[i]['slug']
        row_number[i]=data[i]['mobile_number']
        i+=1
    variable1=str(row_number[0])
    variable2=str(row_number[1])
    variable3=str(row_number[2])
    variable4=str(row_number[3]) 
    
    speech = "Here are some properties with your choice: "+"\n" + " with price "+ row_price[0] +"\n"+ row_title[1] +" in "+ row_location[1] + " with price "+ row_price[1]
    
    if "GettingStarted" in intent_name:     
        message= {
    "type": "quick_reply",
    "content": {
        "type": "text",
        "text": "I am your digital assistant today, How can I help you with your property needs?"
    },
    "msgid": "qr_212",
    "options": [
        "Buy Property"
    ]
  }
    elif "BuyPlot" in intent_name:
        message= {
   "type": "quick_reply",
    "content": {
        "type": "text",
        "text": "Great! Kindly select the city in which you want to buy property?"
    },
    "msgid": "qr_213",
    "options": [
        "Rawalpindi",
        "Karachi",
        "Islamabad",
        "Lahore",
        "Other city?"
    ]
  }
    elif "Menu" in intent_name:
        message= {
   "type": "quick_reply",
    "content": {
        "type": "text",
        "text": "Kindly select one of the options"
    },
    "msgid": "qr_231",
    "options": [
        "Choose Sector",
        "Other City?Specify",
        "Hot Property",
        "Price Range",
        "Land Area",
        "Property Type",
        "Buy Property"
    ]
  }
    elif "ChooseArea" in intent_name:
        message= {
   "type": "quick_reply",
    "content": {
        "type": "text",
        "text": "Kindly select one of the options"
    },
    "msgid": "qr_231",
    "options": [
        "10 Marla",
        "5 Marla",
        "1 Kanal"
    ]
  }
    elif "ChooseCity" in intent_name:
          message= {
    "type": "catalogue",
  "msgid": "cat_254",
  "items": [{
    "title": row_title[0],
    "subtitle": row_location[0],
    "imgurl": "http://www.aarz.pk/assets/images/properties/"+row_id[0]+"/"+row_id[0]+".actual.0.jpg",
    "options": [
        {
        "type": "element_share"
      }, 
            {
        "type": "phone_number",
        "title": "Call us",
        "phone_number":"+92"+variable1[1:]
      },
        {
      "type": "text",
      "title": "Show Menu"
    }

    ]
  }, 
     {
    "title": row_title[1],
    "subtitle": row_location[1],
    "imgurl": "http://www.aarz.pk/assets/images/properties/"+row_id[1]+"/"+row_id[1]+".actual.0.jpg",
    "options": [
        {
        "type": "element_share"
      }, 
            {
        "type": "phone_number",
        "title": "Call us",
        "phone_number":"+92"+variable2[1:]
      },
        {
      "type": "text",
      "title": "Show Menu"
    }

    ]
  },
      {
    "title": row_title[2],
    "subtitle": row_location[2],
    "imgurl": "http://www.aarz.pk/assets/images/properties/"+row_id[2]+"/"+row_id[2]+".actual.0.jpg",
    "options": [
        {
        "type": "element_share"
      }, 
            {
        "type": "phone_number",
        "title": "Call us",
        "phone_number":"+92"+variable3[1:]
      },
        {
      "type": "text",
      "title": "Show Menu"
    }

    ]
  },
      {
    "title": row_title[3],
    "subtitle": row_location[3],
    "imgurl": "http://www.aarz.pk/assets/images/properties/"+row_id[3]+"/"+row_id[3]+".actual.0.jpg",
    "options": [
        {
        "type": "element_share"
      }, 
            {
        "type": "phone_number",
        "title": "Call us",
        "phone_number":"+92"+variable4[1:]
      },
        {
      "type": "text",
      "title": "Show Menu"
    }

    ]
  }
  ]
  }
    elif "ChoosePlotArea" in intent_name:
          message= {
   "type": "quick_reply",
    "content": {
        "type": "text",
        "text": urlquick
    },
    "msgid": "qr_231",
    "options": [
    "Sector in "+row_city[0],
        "Other City?Specify",
        "Hot Property",
        "Price Range",
        "Land Area",
        "Property Type",
        "Buy Property"
    ]
  }
            
    elif "ChooseHotProperties" in intent_name:
          message= {
    "type": "quick_reply",
    "content": {
        "type": "text",
        "text": urlquick
    },
    "msgid": "qr_231",
    "options": [
    "Sector in "+row_city[0],
        "Other City?Specify",
        "Hot Property",
        "Price Range",
        "Land Area",
        "Property Type",
        "Buy Property"
    ]
  }
    elif "ChooseLocationISB" in intent_name:
          message= {
    "type": "quick_reply",
    "content": {
        "type": "text",
        "text": urlquick
    },
    "msgid": "qr_231",
    "options": [
    "Sector in "+row_city[0],
        "Other City?Specify",
        "Hot Property",
        "Price Range",
        "Land Area",
        "Property Type",
        "Buy Property"
    ]
  }
    elif "ChooseLocationRWP" in intent_name:
          message= {
    "type": "quick_reply",
    "content": {
        "type": "text",
        "text": urlquick
    },
    "msgid": "qr_231",
    "options": [
    "Sector in "+row_city[0],
        "Other City?Specify",
        "Hot Property",
        "Price Range",
        "Land Area",
        "Property Type",
        "Buy Property"
    ]
  }
    elif "ChooseLocationKHI" in intent_name:
          message= {
    "type": "quick_reply",
    "content": {
        "type": "text",
        "text": urlquick
    },
    "msgid": "qr_231",
    "options": [
    "Sector in "+row_city[0],
        "Other City?Specify",
        "Hot Property",
        "Price Range",
        "Land Area",
        "Property Type",
        "Buy Property"
    ]
  }
    elif "ChooseLocationLHR" in intent_name:
          message= {
    "type": "quick_reply",
    "content": {
        "type": "text",
        "text": urlquick
    },
    "msgid": "qr_231",
    "options": [
    "Sector in "+row_city[0],
        "Other City?Specify",
        "Hot Property",
        "Price Range",
        "Land Area",
        "Property Type",
        "Buy Property"
    ]
  }
            
    return {
        "speech": speech,
        "displayText": speech,
        "data": message
        # "contextOut": [],
        #"source": "apiai-weather-webhook-sample"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
