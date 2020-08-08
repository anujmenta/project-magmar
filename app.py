from flask import Flask, render_template, jsonify

import requests, time, json

app = Flask(__name__)

headers = {
'accept': 'application/json, text/plain, */*',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
'cookie': '__cfduid=d3d6fb2841facf9d68decdd87126ee4de1552310622; _pxhd=a6dd9d5efab48e7fc3e962d64164be0592764c032fd56e5fb680cc40a2329b5f:e41ebfe1-4400-11e9-a9c3-739b63cef1b4; cid=rBsP3lyGYV4KMgAhA/3AAg==; _ga=GA1.2.1299721724.1552310627; _gid=GA1.2.2115517028.1552310627; _fbp=fb.1.1552310627060.2024589605; hblid=EHwfALkxGYGfe2Qd3F6pZ0J63APBoEr0; _okdetect=%7B%22token%22%3A%2215523106273180%22%2C%22proto%22%3A%22https%3A%22%2C%22host%22%3A%22www.crunchbase.com%22%7D; __qca=P0-1463243748-1552310626967; _pendo_visitorId.c2d5ec20-6f43-454d-5214-f0bb69852048=_PENDO_T_dPRrqg5DlCC; olfsk=olfsk9225065529076975; _ok=1554-355-10-6773; __zlcmid=rGi4veapc5KTJG; _mkto_trk=id:976-JJA-800&token:_mch-crunchbase.com-1552311355382-27764; wcsid=jgoq02HsKRYwZ9yF3F6pZ0Jo3ra0EPbA; _okbk=cd4%3Dtrue%2Cvi5%3D0%2Cvi4%3D1552315720869%2Cvi3%3Dactive%2Cvi2%3Dfalse%2Cvi1%3Dfalse%2Ccd8%3Dchat%2Ccd6%3D0%2Ccd5%3Daway%2Ccd3%3Dfalse%2Ccd2%3D0%2Ccd1%3D0%2C; _oklv=1552315900867%2Cjgoq02HsKRYwZ9yF3F6pZ0Jo3ra0EPbA; _pendo_meta.c2d5ec20-6f43-454d-5214-f0bb69852048=2655801586; _gaexp=GAX1.2.P1jW6YWJRnCmoIi0wMRIaw.18059.1; _hp2_ses_props.973801186=%7B%22ts%22%3A1552383374311%2C%22d%22%3A%22www.crunchbase.com%22%2C%22h%22%3A%22%2Forganization%2Ftapchief%22%7D; _pxff_tm=1; _px3=b71f1c8b00bce199892f88d7790342596d74306ed2fbb6504b78b17c0d89e535:rmcgLpNBpSo6FxfS9S2Pm4blJdKAOkdLOqd3TLKzV7g0s7ALpvF0ad6sbA3KixaJz2mtqferSd+nH2YavH6QDQ==:1000:0y8VdoTsBaPf8GFwIkewPd4hasZMfgz//IIrVx6kpzW2ytiu/Z2l0maMFRvFAttN5D1bWJsxL6F/sOiR1RDDP7nvpPmb7nD0aYWDZ1Q7WZvZU1/DM8vxphOLQyzGgsKXH/MYuWMRd3NbJJTqoWR36edP34/Eb9Pk+jFl2V1xQtc=; _gat_UA-60854465-1=1; _hp2_props.973801186=%7B%22Logged%20In%22%3Afalse%2C%22Pro%22%3Afalse%2C%22cbPro%22%3Afalse%2C%22apptopia-lite%22%3Afalse%2C%22apptopia-premium%22%3Afalse%2C%22builtwith%22%3Afalse%2C%22ipqwery%22%3Afalse%2C%22siftery%22%3Afalse%2C%22similarweb%22%3Afalse%2C%22bombora%22%3Afalse%2C%22owler%22%3Afalse%7D; _hp2_id.973801186=%7B%22userId%22%3A%221035836532930018%22%2C%22pageviewId%22%3A%221749680495276294%22%2C%22sessionId%22%3A%228506666868252209%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D',
'referer': 'https://www.crunchbase.com/search/organization.companies/field/organizations/rank_org_company/680000',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

slack_url = 'https://hooks.slack.com/services/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'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/comp/<uuid>')

def get_company_data(uuid):
	time.sleep(0.5)
	resp = requests.get('https://www.crunchbase.com/v4/data/entities/organizations/'+uuid+'?field_ids=%5B%22identifier%22,%22layout_id%22,%22facet_ids%22,%22title%22,%22short_description%22,%22is_locked%22%5D&layout_mode=view', headers=headers)
	data = json.loads(resp.text)
	requests.post(slack_url, json={"text":"Test export"})
	return jsonify(data)


if __name__ == '__main__': app.run(debug=True)