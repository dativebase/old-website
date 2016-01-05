# -*- coding: utf-8 -*-

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

