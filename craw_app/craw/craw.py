import sys
sys.path.append('.')
from craw_app.extract_html.extract import extract_text

def crawler(url, number_pages):
    extract  = extract_text()
    extractor_result = extract.get_data(url, number_pages)
    crawler_dict = {}
    att_dict = {}
    for i in range(len(extractor_result)):
        keys_list = list(extractor_result[i])
        att_dict = {}
        att_dict['Page'+str(i)] = {}
        for j in range(len(keys_list)):
            att_dict['Page'+str(i)][keys_list[j]] = extractor_result[i][keys_list[j]]
        crawler_dict.update(att_dict)
    return crawler_dict
