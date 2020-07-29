import os
import datetime
from app import serverApplication
from app.views import mongo
from flask import request, redirect, render_template
from werkzeug.utils import secure_filename 


#-------------------------------------------API routes for flutter 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
FILE_PATH=''

def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@serverApplication.route('/api/admin/login',methods=['POST'])
def loginUser():
   flag = False
   response={}
   if(request.method == 'POST'):
      print(request.get_json())
      requestBody = request.get_json()
      name = requestBody['username']
      password=requestBody['password']
      print("Name: "+name)
      print("Password: "+password)
      prefix = name[0:2] #prefix code of state
      name = name[2:] #actual username to search
      print(prefix)      
      print(name)
      state_users = mongo.db[prefix]
      for admin in state_users.find():
         print(admin)
         if(admin['username'] == name and admin['password'] == password):
            flag = True
            response['full-name'] = admin['full-name']
            response['state'] = admin['state']
            response['district'] = admin['district']
            break
      if flag:
         response['status'] = 1         
         response['message'] = "User Authenticated"
      else:
         response['status'] = 0
         response['message'] = "Invalid username or password"
   return response   

@serverApplication.route('/api/getSurveyQuestions',methods=['POST','GET'])
def prepareSurveyQuestions():
   response = {}
   if(request.method=='POST'):
      print(request.get_json())
      jsonData = request.get_json()
      lang = jsonData['language']
      if (lang =='en'):
         filter = {"_id":0,"hindiQuestions":0}
      else:
         filter = {"_id":0,"englishQuestions":0}
      data  = mongo.db.surveyQuestions.find({},filter)
      print(type(data))
      print(data)
      for item in data:
         if(lang=='en'):
            response['questions'] = item['englishQuestions']
         else:
            response['questions'] = item['hindiQuestions'] 
      response['message'] = "OK"
   return response   

@serverApplication.route('/api/emergency',methods=['POST'])
def save_ee():
   response={}
   print('...EE data received')
   if(request.method=='POST'):
      print(request.get_json())
      jsonData = request.get_json()
      print(type(jsonData))
      reportType = jsonData['report-type']
      state = jsonData['state']
      district = jsonData['district']
      region = jsonData['region']
      dataToStore = {"reporter":jsonData['reporter'],"data":jsonData['data']}
      f = mongo.db.embankmentEmergencies.update_one({"state":state},{"$push":{reportType:{'time-stamp':datetime.datetime.now(),'district':district,'region':region,'report-data':dataToStore}}})
      print(f)
      if f:
         response['status'] = 1         
         response['message'] = "Data submitted successfully"
      else:
         response['status'] = 0
         response['message'] = "Error submitting"
   print(response)
   return response   


@serverApplication.route('/api/getSurveys',methods=['POST'])
def getSurveyData():
   surveysList = []
   response = {}

   if(request.method=='POST'):
      print(request.get_json())
      jsonRequest = request.get_json()
      state = jsonRequest['state']
      district = jsonRequest['district']
      data = mongo.db.pendingSurveys.find({'state':state},{'_id':0})
      surveys=""
      
      for doc in data:
         #print("\nDOC\n")
         #print(doc)
         surveys=doc['surveys']
      print(surveys)

      for item in surveys:
         if(item['district']==district):
            #print(item)
            #print("\n")
            surveyId = item['surveyId']
            user = item['surveyer']
            timestamp = item['date-time']
            loc = item['location']
            surveyStatus = item['survey-status']
            imageURL = item['image-url']
            surveyDataToSend = {"surveyId":surveyId,"surveyer":user,"time-stamp":timestamp,"location":loc,"survey-status":surveyStatus,"image-url":imageURL}
            #print(surveyDataToSend)
            surveysList.append(surveyDataToSend)
            
      # for survey in data:
      #    surveysList.append(survey) 
   if(len(surveysList)<1):
      response['status'] = 0
      response['message'] = "No surveys found" 
   else:
      response['status'] = 1
      response['message'] = surveysList  
   print("Response to send")
   print(response)
   return response  


@serverApplication.route('/api/survey/uploadImage',methods=['POST'])
def save_image():
   print('...Request received')
   if(request.method=='POST'):
      if request.files:
         file = request.files['image-file']
         print(file.filename)
         if(allowed_file(file.filename)):
            filename = secure_filename(file.filename)
            FILE_PATH = os.path.join(serverApplication.config['UPLOAD_FOLDER'],filename)
            file.save(FILE_PATH)
            data = mongo.db.images.insert_one({'image_name':filename,'url':'<server-url>/'+FILE_PATH})
            if(data):
               res=FILE_PATH
         else:
            res="Unsupported image format"
      else:
         res = "No file received"
   print('........')
   
   return res

@serverApplication.route('/api/surveys/storeUserSurvey',methods=['POST'])
def saveSurvey():
   response ={}
   if(request.method=='POST'):
      print("Request data:\n")
      print(request.get_json())
      data = request.get_json()
      print(type(data))
      state = data['state']
      #state= "Maharashtra"
      print(state)
      flag = mongo.db.pendingSurveys.update({"state":state},{'$push':{"surveys":data}})
      if(flag):
         print('Survey data stored in mongodb................')
         response['status'] = 'OK'
         response['message'] = 'Data Stored...'
      else:
         print("Some problem storing data................")
         response['status'] = 'Error'
         response['message'] = "Couldn't store data..."
   
   return response


#--------------------------------------------Routes for web application
@serverApplication.route('/')
@serverApplication.route('/index')
def index():
    user = {'nickname': 'JAID'}  # fake user
    return render_template('index.html',
                           title='Home',
                           user=user)

@serverApplication.route('/webmap')
def Webmap():
    user={'nickname':'Jaid'}
    return render_template('WebMap.html',title='WorkSpace',user=user)

@serverApplication.route('/fetchSurvey')
def dynamicSurvey():
    from app.surveyData import mongo2csv
    mongo2csv(csvFile="./app/static/surveyData.csv")
    user = {'nickname': 'JAID'}  # fake user
    return redirect('/scene')

@serverApplication.route('/scene')
def scene():
    user = {'nickname': 'JAID'}  # fake user
    return render_template('arcscene.html',
                           title='Datas',
                           user=user)

@serverApplication.route('/heatmap')
def heatmap():
    user={'nickname':'Jaid'}
    return render_template('heatmap.html',title='HeatMap',user=user)

@serverApplication.route('/healthcard')
def healthcard():
    from app.finalHealthCard import getHealthValues
    healthcard=getHealthValues()
    user={'nickname':'Jaid'}
    return render_template('healthcard.html',title='HealthCard',user=user,healthcard=healthcard)