from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re

# access to complete annotated files
# eng_annots = "https://raw.github.ubc.ca/shuning3/COLX523_SH_VT_AL/master/data/final_annotations_english.csv?token=AAAAO6GRFQRYKOZN6FFS5I26PUXY4"
# fre_annots = "https://raw.github.ubc.ca/shuning3/COLX523_SH_VT_AL/master/milestone3/final_anotations_french.csv?token=AAAAO6H33SQ6VBAHDRMJGFK6PUXR4"
# chi_annots = "https://raw.github.ubc.ca/shuning3/COLX523_SH_VT_AL/master/milestone3/Weibo_407annotations_final.csv?token=AAAAO6DIXDWYJZ4TMBTBC2K6PUXUQ"

# final combined annotations
all_annots = "https://raw.github.ubc.ca/amlk8913/SH_VT_AL_public/master/Combined_annotations.csv?token=AAAAPAOK2AZ2KDD5DN2PKQK6P3BTY"

class CorpusWebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        query = parse.urlsplit(self.path).query
        query_dict = parse.parse_qs(query)
        print("This is the query dict:", query_dict)
        if self.path == "/":
            self.send_header('Content-type','text/html; charset=utf-8')
            self.end_headers()
            f = open("frontend.html", encoding="utf-8")
            html = f.read()
            f.close()
            self.wfile.write(html.encode("utf-8"))
        elif "frontend.css" in self.path:
            self.send_header('Content-type','text/css; charset=utf-8')
            self.end_headers()
            f = open("frontend.css", encoding="utf-8")
            css = f.read()
            f.close()
            self.wfile.write(css.encode("utf-8"))
        elif "frontend.js" in self.path:
            self.send_header('Content-type','text/javascript; charset=utf-8')
            self.end_headers()
            f = open("frontend.js", encoding="utf-8")
            js = f.read()
            f.close()
            self.wfile.write(js.encode("utf-8"))
        elif query_dict['output'][0] == 'table':
            self.send_header('Content-type','text/html; charset=utf-8')
            self.end_headers()  
            print("LOOK HERE", query_dict)
            # make dataframe from link above
            query = pd.read_csv(all_annots)
            pd.options.display.max_colwidth = 105
            # different filtering options: keyword search, language, company, sentiment
            if 'search' in query_dict:
                query = search_tweets(query, query_dict["search"][0])
            if 'lang' in query_dict and query is not None:
                query = filter_by(query, 'lang', query_dict['lang'])
            if 'comp' in query_dict and query is not None:
                query = filter_by(query, 'comp', query_dict['comp'])
            if 'senti' in query_dict and query is not None:
                query = filter_by(query, 'senti', query_dict['senti'])
            if query is not None:
                df = pd.DataFrame.to_html(query, classes = 'table', index = False, max_rows = 50, justify = 'center')
                if 'search' in query_dict:
                    html_df = insert_table(df, no_results = False, search_term = query_dict['search'][0])
                else:
                    html_df = insert_table(df, no_results = False)
                self.wfile.write(html_df.encode("utf-8"))
            else:
                df = pd.DataFrame({'placeholder': [1, 2, 3]})
                if 'search' in query_dict:
                    html_df = insert_table(df, no_results = True, search_term = query_dict['search'][0])
                else:
                    html_df = insert_table(df, no_results = True)
                self.wfile.write(html_df.encode("utf-8"))
        # barchart will open up a separate page
        elif query_dict['output'][0] == 'barchart':
            print("test2", query_dict)
            self.send_header('Content-type','text/html; charset=utf-8')
            self.end_headers()
            f = open("frontend_barcharts.html", encoding="utf-8")
            html = f.read()
            f.close()
            self.wfile.write(html.encode("utf-8"))
        # piechart will open up a separate page
        elif query_dict['output'][0] == 'piechart':
            print("test2", query_dict)
            self.send_header('Content-type','text/html; charset=utf-8')
            self.end_headers()
            f = open("frontend_piecharts.html", encoding="utf-8")
            html = f.read()
            f.close()
            self.wfile.write(html.encode("utf-8"))
        return

########################################################

def filter_by(querydf, type_of, query_options):
    """takes in a query/dataframe, filters by the given query options and their type, returns a dataframe"""
    print("these are the query options", query_options)
    if type_of == 'lang':
        category = 'lang'
    elif type_of == 'comp':
        category = 'company'
    elif type_of == 'senti':
        category = 'rating'
        rate_dict = {'vps': 'Very Positive', 'pos': 'Positive', 'neu': 'Neutral', 'neg': 'Negative', 'vng': 'Very Negative'}
        query_options = [rate_dict[qo] for qo in query_options]
    if len(query_options) == 1:
        qstring = category + " == '" + str(query_options[0]) + "'"
        df = querydf.query(qstring)
        return df
    elif len(query_options) > 1:
        qstring2 = ""
        for qo in query_options:
            queryst = category + " == '" + qo + "'"
            qstring2 = qstring2 + queryst + "| "
        df = querydf.query(qstring2[:-2])
        return df

def insert_table(html_df, no_results = False, search_term = None):
    """takes given html_df and inserts it into webpage, says sorry if not found"""
    f = open("frontend.html", encoding="utf-8")
    html = f.read()
    f.close()
    to_replace = re.findall("Your search results will appear here.* between them.",html, flags=re.DOTALL)[0]
    



    if no_results and search_term is not None:
        html = html.replace(to_replace, 'Sorry, no results were found for your search: ' + search_term)
    if no_results == False and search_term is not None:
        html = html.replace(to_replace, 'You searched for: ' + search_term + '<br><br>' + html_df)
    if no_results == False and search_term is None:
        html = html.replace(to_replace, 'Here are your results! <br><br>' + html_df)
    return html

def search_tweets(query, search):
    '''Based on a query, the function returns the total number of tweets that contains the query and a dataframe
    of the text of the tweet and the company'''
    search_list = []
    print(query.shape)
    for i in range(len(query)):
        if search.lower() in query['text'][i].lower():
            search_list.append(query.iloc[i])
    if len(search_list) > 0:
        df = pd.DataFrame(search_list, columns = ['text', 'lang', 'company', 'rating'])
        return df
    else:
        return None


########################################################

if __name__ == "__main__":
    http_port = 9996
    server = HTTPServer(('localhost', http_port),  CorpusWebServer)
    server.serve_forever()