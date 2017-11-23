from mongo_connector import *
import json
import facebook_moda

mc = None
db = None

def extract_data(model_dict):
    """
        main method to extract data
    """

    pages = [page.strip() for page in (open('pages.txt','r')).readlines()]
   
    # extract data from fb
    fb_extractor = facebook_moda.PageFeedReader('conf.json')
    global mc
    global db
    mc = MongoConnector('localhost' , 27017)
    db = mc.createDatabase("cloud_db")

    model = (model_dict.keys())[0]
    terms = model_dict[model]

    for term in terms:
        for page in pages:
            data = fb_extractor.fetch(model, term, page)
            write_data(model, data)

def write_data(model, data):
    """
        creates a new file based on the 'model' name and dumps 'data' to it
    """
    collection_name = "facebook_" + model
    collection = mc.createCollection(collection_name)

    print "Inserting " + str(len(data)) + " reviews under the collection : " +  collection_name

    if(len(data) > 0):
        mc.insert_many(data, collection)


    """json.dump(data, open(model+'_facebook.json', 'w'))"""

if __name__ == '__main__':
    #extract_data()
    pass
