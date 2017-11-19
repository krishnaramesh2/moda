import json
import facebook

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
    terms_file_f = open(terms_file,'r')
    terms = json.load(terms_file_f)
    
    phone_models = terms.keys()

    # extract data from fb
    fb_extractor = facebook.PageFeedReader('../data_preprocessing/conf.json')
    for model in phone_models:
        model_terms = phone_models[model]
        for model_term in model_terms:
            pass

def write_data():
    pass

if __name__ == '__main__':
    extract_data()