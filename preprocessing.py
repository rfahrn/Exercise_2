#!/usr/local/bin/python3
# *-* coding: UTF-8 *-*
# Author: Jessica Roady & Rebecka Fahrni

import requests
import csv
import json
import spacy
# Uncomment the following lines if spacy is making problems for you:
# from spacy.cli.download import download
# download(model='en_core_web_sm')

# variables for URL-API information retrieval
key = 'f18a3a58-5499-4e50-ad27-a9512055f56b'
lang = 'EN'
headers = {'Accept-Encoding': 'gzip'}
text = ''
lemma = ''

# parameters of API-urls
params1 = {
    'text':text,  # list of strings from read_file()
    'lang':lang,
    'key': key,
}

# parameters of API-urls
params2 = {
    'lemma':lemma,
    'lang':lang,
    'key':key
}

#  URLs for information retrieval of API
service_url_disambiguate = 'https://babelfy.io/v1/disambiguate'
service_url_retrievesynset = 'https://babelnet.io/v6/getSynsetIds'
url_retrievesynsets = f'https://babelnet.io/v6/getSynsetIds?lemma{lemma}&searchLang={lang}&key={key}'.format(lemma=params2['lemma'], searchLang=params2['lang'], key=params2['key'])
url_babelfyversion = f'https://babelnet.io/v6/getVersion?key={key}'.format(key=params1['key'])
url_disambiguate = f'https://babelfy.io/v1/disambiguate?text={text}&lang={lang}&key={key}'.format(text=params1['text'],lang=params1['lang'],key=params1['key'])


def get_response(url,params):
    """ Returns the API-response (json format)"""
    response = requests.get(url, params=params, headers=headers)
    return response.json()


def read_file():
    with open('bbc_article.txt', 'r') as f:
        lines = [line.rstrip() for line in f if not line == '\n']
        params1['text'] = lines
    return lines


def get_link(babelsynsetID):
    """ Returns the link of the NE according to its babelsynsetID """
    url = f'https://babelnet.org/synset?word={babelsynsetID}&lang=EN&langTrans=DE'
    return url


def get_entity(text, cfStart, cfEnd):
    """ Returns the entity according to the character span """
    return text[cfStart:cfEnd+1]


# TODO: break into more functions
def generate_data(lines):
    nlp = spacy.load("en_core_web_sm")
    json_content = read_json('json_response.json')

    entities = []
    ent_on_off = []
    tok_index = []
    tokens = []
    lemmas = []
    pos = []
    links = []
    synsetIds = []

    for i,texts in enumerate(json_content, start=0):
        doc = nlp(lines[i])
        for o, token in enumerate(doc):
            tokens.append(token.text)
            tok_index.append((token.i, token.i))
            lemmas.append(token.lemma_)
            pos.append(token.pos_)

        results_per_text = json_content[texts]
        for result in results_per_text:
            # token from fragment retrieval
            tokenFragment = result.get('tokenFragment')
            tfStart = tokenFragment.get('start')
            tfEnd = tokenFragment.get('end')
            ent_on_off.append((tfStart, tfEnd))

            # Babelsynset ID retrieval
            synsetId = result.get('babelSynsetID')
            synsetIds.append(synsetId)
            links.append(get_link(synsetId))

            # char from fragment retrieval, needed for entity linking
            charFragment = result.get('charFragment')
            cfStart = charFragment.get('start')
            cfEnd = charFragment.get('end')

            entity = get_entity(lines[i], cfStart, cfEnd)
            entities.append(entity)

    ent_info = list(zip(entities, ent_on_off, synsetIds, links))
    for i, item in enumerate(ent_info):
        if i > 0:
            e1_on = ent_info[i - 1][1][0]
            e1_off = ent_info[i - 1][1][1]
            e2_on = item[1][0]
            e2_off = item[1][1]

            # Using the type as a flag for later removal, because if I just remove it the indices will get messed up
            if e1_on >= e2_on and e1_off <= e2_off:
                ent_info[i - 1] = list(ent_info[i - 1])
            if e1_on <= e2_on and e1_off >= e2_off:
                ent_info[i] = list(ent_info[i])

    for i in ent_info:
        if isinstance(i, list):
            ent_info.remove(i)

    rows = []
    token_info = list(zip(tokens, lemmas, pos, tok_index))
    for t in token_info:
        row = list(t)

        for e in ent_info:
            # Single-token entities:
            if t[0] == e[0] and t[3] == e[1]:  # OK because no two identical tokens also have the same indices
                row.extend([e[0], 'B-' + e[2], e[3]])

            # Multi-token entities:
            #   if the onset is the same:
            elif t[0] + ' ' in e[0] and t[3][0] == e[1][0]:
                if not len(row) == 7:  # needed to avoid appending the entity multiple times
                    row.extend([e[0], 'B-' + e[2], e[3]])
            #   if the offset is the same:
            elif ' ' + t[0] in e[0] and t[3][1] == e[1][1]:
                if not len(row) == 7:
                    row.extend([e[0], 'I-' + e[2], e[3]])
            #   if the onsets are within 1 of each other (this is enough because there are no entities longer than 3):
            elif ' ' + t[0] + ' ' in e[0] and t[3][0] - 1 == e[1][0]:
                if not len(row) == 7:
                    row.extend([e[0], 'I-' + e[2], e[3]])

        rows.append(row)

    return rows


def write_csv(data):
    """ Creates a .tsv file of data """
    with open('data.tsv', 'w', encoding='UTF8', newline='\n') as f:
        header = ['token', 'lemma', 'pos', '(onset, offset)', 'entity', 'babelfy_id(iob)', 'link', 'TP', 'FP', 'FN']
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(header)
        writer.writerows(data)


def read_json(file):
    """ Reads a json file and returns its content """
    with open(file, 'r') as j:
        json_content = json.loads(j.read())
        return json_content


def create_json_file(data_disambiguate):
    """ Creates a json file """
    with open('json_response.json', 'w') as f:
        json.dump(data_disambiguate, f, indent=4)


def main():
    lines = read_file()
    data = generate_data(lines)
    write_csv(data)

    # Getting API-response from request and creating a .json file out of it
    datadis = {}
    for i, text in enumerate(params1['text'], start=1):
        params1['text'] = text
        response_dis = requests.get(service_url_disambiguate, params=params1, headers=headers)
        json_data_dis = response_dis.json()
        datadis['text ' + str(i)] = json_data_dis

    create_json_file(datadis)


if __name__ == "__main__":
    main()
