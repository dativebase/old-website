# -*- coding: utf-8 -*-

"""This is a python script that serves as a set of code examples for
illustrating how to work with an OLD.

Running ``python example.py`` should result in several successful requests,
i.e., all of the code below should work. You will, however, need to supply a
valid username and password in the login block.

Running ``python example-py2html.py`` will take this code, interleave it in the
correct places in index-src.html and write the result to index.html. The word
after "start-block: " and "end-block: " in the blocks below must match a word
after an HTML comment of the form "code-block: " in index-src.html.

"""

import pprint

# start-block: logging-in
import requests, json
s = requests.Session()
url = 'https://projects.linguistics.ubc.ca/demoold/'
s.headers.update({'Content-Type': 'application/json'})
resp = s.post('%slogin/authenticate' % url,
    data=json.dumps({
        'username': 'myusername',
        'password': 'mypassword'}))
assert resp.json().get('authenticated') == True
# end-block: logging-in


# start-block: getting-forms
forms = s.get('%sforms' % url).json()
for form in forms[:3]:
    print '%s "%s"' % (form['transcription'],
        form['translations'][0]['transcription'])
# Qaⱡa kin in? "Who are you?"
# Hun upxni qaⱡa hin in. "I know who you are."
# Qaⱡa ku in? "Who am I?"
# end-block: getting-forms

# start-block: pagination
paginator = {'items_per_page': 10, 'page': 1}
forms = s.get('%sforms' % url, params=paginator).json()
print forms['paginator']['count']
# 800
print len(forms['items'])
# 10
print forms['items'][0]['transcription']
# maⱡtin haqapsi kanuhus nanas
# end-block: pagination

# start-block: getting-collections
collections = s.get('%scollections' % url).json()
for collection in collections[:3]:
    print '%s. %s' % (collection['title'],
        collection['description'])
# Martina's Fall. Group 4
# Is This A...?. 
# Cup Game. Group 1
# end-block: getting-collections

# start-block: get-collection-with-forms
collection = s.get('%scollections/1' % url).json()
coll_forms = collection['forms']
print 'Collection %s contains %d forms.\n' % (
    collection['title'], len(coll_forms))
# Collection Going for a visit ... contains 9 forms.
import re
for form_id in map(int, re.findall('form\[(\d+)\]',
    collection['contents'])):
    form = [f for f in coll_forms
        if f['id'] == form_id][0]
    print u'%s\n%s\n' % (form['transcription'],
        form['translations'][0]['transcription'])
# ȼan qakiʔni: xman qawakaxi ka akitⱡa kuȼxaⱡ upxnamnaⱡa
# John says: Come to me for a visit! (Come over to my ...
#
# James qakiʔni: Waha! Huȼxaⱡ qataⱡ ȼ̓inaⱡ upxnisni at ...
# James says: No! I can't go to you for a visit. I ...
#
# ...
# end-block: get-collection-with-forms

# start-block: search-1
url = 'https://projects.linguistics.ubc.ca/demoold/'
search_expr = json.dumps({
    "query": {
        "filter": ["Form", "transcription", "regex", "^a"]}})
r = s.post('%sforms/search' % url,
    data=search_expr).json()
print '\n'.join(t['transcription'] for t in r[:3])
# anteferre
# abacus
# abacus
# end-block: search-1

# start-block: search-2
search_expr = json.dumps({
    "query": {
        "filter": ["Form", "transcription", "regex", "^a"],
        "order_by": ["Form", "transcription", "desc"]
    },
    "paginator": {
        "page": 1,
        "items_per_page": 3
    }
})
r = s.post('%sforms/search' % url,
    data=search_expr).json()
print r['paginator']['count']
# 720
print '\n'.join(t['transcription'] for t in r['items'])
# azymum
# axitiosus
# axitiosus
# end-block: search-2

# start-block: search-3
search_expr = json.dumps({
    "query": {
        "filter": ["and",
            [
                ["Form", "transcription", "regex", "^a"],
                ["Form", "grammaticality", "=", ""]
            ]
        ]}})
r = s.post('%sforms/search' % url,
    data=search_expr).json()
print '\n'.join(t['transcription'] for t in r[:3])
# anteferre
# abacus
# abacus
# end-block: search-3

# start-block: search-4
search_expr = json.dumps({
    "query": {
        "filter": ["or",
            [
                ["Form", "morpheme_gloss", "regex", "cat"],
                ["Form", "comments", "regex", "cat"],
                ["Form", "translations", "transcription",
                    "regex", "cat"],
            ]
        ]}})
r = s.post('%sforms/search' % url,
    data=search_expr).json()
print ('transcription:  %s\n'
       'morpheme gloss: %s\n'
       'comments:       %s\n'
       'translation(s): %s' % (
           r[0]['transcription'],
           r[0]['morpheme_gloss'],
           r[0]['comments'],
           '\n                '.join(
               t['transcription'] for t in r[0]['translations'])))
# transcription:  abdico
# morpheme gloss:
# comments:
# translation(s): resign, abdicate
#                 abolish
#                 disinherit
#                 renounce, reject, expel, disapprove of
# end-block: search-4


s = requests.Session()
url = 'https://projects.linguistics.ubc.ca/blaold/'
s.headers.update({'Content-Type': 'application/json'})
resp = s.post('%slogin/authenticate' % url,
    data=json.dumps({
        'username': 'myusername',
        'password': 'mypassword'}))
assert resp.json().get('authenticated') == True


# start-block: search-5
search_expr = json.dumps({
    "query": {
        "filter": ["and",
            [
                ["not", ["Form", "grammaticality", "=", "*"]],
                ["Form", "status", "!=", "requires testing"],
                ["Form", "enterer", "last_name", "=", "Dunham"],
                ["Form", "translations", "transcription",
                    "regex", "( )(is|am|are)( ).+ing( |$)"],
                ["Form", "morpheme_break", "regex", "(^| |-)á-"],
                ["Form", "datetime_entered", "<",
                    "2011-01-01T12:00:00"]
            ]
        ]}})
r = s.post('%sforms/search' % url,
    data=search_expr).json()
print ('transcription:  %s\n'
       'morpheme break: %s\n'
       'morpheme gloss: %s\n'
       'translation(s): %s\n'
       'entered:        %s\n'
       'enterer:        %s' % (
            r[0]['transcription'],
            r[0]['morpheme_break'],
            r[0]['morpheme_gloss'],
            '\n                '.join(
                t['transcription'] for t in r[0]['translations']),
            r[0]['datetime_entered'],
            '%s %s' % (
                r[0]['enterer']['first_name'],
                r[0]['enterer']['last_name'])))

# transcription:  oma sinai'koan nitááwaanika otsin'iihka'siimii
# morpheme break: om-wa sina-ikoan nit-á-waanii-ok-wa ot-inihka'sim-yi
# morpheme gloss: DEM-PROX cree-being 1-DUR-say-INV-3SG 3-name-IN.SG
# translation(s): that Cree man is telling me his name
# entered:        2008-02-25T00:00:00
# enterer:        Joel Dunham
# end-block: search-5


# start-block: form-template
form_template = {
    "grammaticality": "",
    "transcription": "",
    "morpheme_break": "",
    "morpheme_gloss": "",
    "narrow_phonetic_transcription": "",
    "phonetic_transcription": "",
    "translations": [],
    "comments": "",
    "speaker_comments": "",
    "date_elicited": "",
    "speaker": None,
    "source": None,
    "elicitation_method": None,
    "elicitor": None,
    "syntax": "",
    "semantics": "",
    "status": "",
    "syntactic_category": None,
    "verifier": None
}
# end-block: form-template

# start-block: adding-form
import copy
form = copy.deepcopy(form_template)
form['transcription'] = 'Arma virumque cano.'
form['translations'].append({
    'transcription': 'I sing of arms and a man.',
    'grammaticality': ''
})
r = s.post('%sforms' % url, data=json.dumps(form)).json()
assert r['transcription'] == 'Arma virumque cano.'
print '%s %s created a new form with id %d on %s.' % (
    r['enterer']['first_name'],
    r['enterer']['last_name'],
    r['id'],
    r['datetime_entered'])
# Joel Dunham created a new form with id 1014 on 2016-01-25T06:41:06.
# end-block: adding-form

# start-block: updating-form
r['morpheme_break'] = 'arm-a vir-um-que can-o'
r['morpheme_gloss'] = 'arm-ACC.PL man-ACC.PL-and sing-1SG.PRS'
r = s.put('%sforms/%d' % (url, r['id']),
    data=json.dumps(r)).json()
print 'Form %d modified on %s.' % (r['id'],
    r['datetime_modified'])
# Form 1014 modified on 2016-01-25T07:12:51.
# end-block: adding-form


