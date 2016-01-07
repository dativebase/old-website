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
url = 'https://kut.old.jrwdunham.com/'
s.headers.update({'Content-Type': 'application/json'})
login_response = s.post('%slogin/authenticate' % url,
    data=json.dumps({
        'username': 'myusername',
        'password': 'mypassword'}))
assert login_response.json().get('authenticated') == True
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
collection = s.get('%scollections/34' % url).json()
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

