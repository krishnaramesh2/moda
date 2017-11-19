import json
import facebook_moda

def create_table():
    """
        creates table in the database
    """
    pass

def extract_data():
    """
        main method to extract data
    """
    terms_file = '../templates/terms.json'
    terms_file_f = open(terms_file, 'r')
    terms = json.load(terms_file_f)
    phone_models = terms.keys()
    print phone_models
    # extract data from fb
    fb_extractor = facebook_moda.PageFeedReader('conf.json')
    for model in phone_models:
        model_data = []
        model_terms = terms[model]
        for model_term in model_terms:
            model_data.extend(fb_extractor.fetch_everything(model_term))
        write_data(model, model_data)

def write_data(model, data):
    """
        creates a new file based on the 'model' name and dumps 'data' to it
    """
    json.dump(data, open(model+'_facebook.json', 'w'))

if __name__ == '__main__':
    extract_data()
