
def fetchSurveyData(MongoURI="mongodb+srv://jalshaktiAdmin:jsadmin@jalshakti-cluster.gznyv.mongodb.net/dynamicDB?retryWrites=true&w=majority",dbName='dynamicDB',collectionName='approvedSurveys'):
    import pymongo
    client = pymongo.MongoClient(MongoURI)
    db = client[dbName]
    surveys_collection = db[collectionName]
    database = surveys_collection.find()

    Surveryforms = []
    for survey in database:
        print(survey)
        Surveryforms = survey['districts'][0]['data']

    return Surveryforms


def ShapefileToCSV(LatLong,csvFile):
    import csv
    fieldNames=['FID','Shape','Id','longitude','latitude','SurveyId']
    with open(csvFile,'w') as CSVfile:
        writer=csv.writer(CSVfile)
        writer.writerow(fieldNames)
        cursor=[]
        index=0
        for location in LatLong:
            FID = index
            Id = 0
            longitude = location[1]
            latitude = location[0]
            SurveyId = location[2]
            Shape = (longitude, latitude)
            index += 1
            cursor.append((FID,Shape,Id,longitude,latitude,SurveyId))
        for row in cursor:
            writer.writerow(row)
    CSVfile.close()
    return "Survey CSV file created."


def mongo2csv(csvFile="./static/surveyData.csv"):
    LatLong=surveytoLocation()
    return (ShapefileToCSV(LatLong,csvFile))


def surveytoLocation():
    SurveyForms=fetchSurveyData()

    latlong=[]
    for forms in SurveyForms:
        latitude=float(forms['location']['latitude'])
        longitude=float(forms['location']['longitude'])
        surveyId=str(forms['surveyId'])
        Location = (latitude, longitude, surveyId)
        latlong.append(Location)
    print(str(len(latlong))+" : survey fetched from mongoDB.")
    return latlong

