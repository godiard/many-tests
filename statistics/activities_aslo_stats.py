from urllib2 import urlopen
 
from BeautifulSoup import BeautifulSoup as bs
import json
import os

data = []

if not os.path.exists('activities_aslo_stats.json'):

    html_act_index = urlopen('http://download.sugarlabs.org/activities/')
    sopa_index = bs(html_act_index)
    pre = sopa_index.find('pre')


    for link in pre.findAll('a'):
        activity_code = link.text.replace('/', '')

        if activity_code != link.text:

            date = link.nextSibling.strip()
            date = date[:date.find(' ')]
            # search the activity uploader
            act_url = 'http://activities.sugarlabs.org/es-ES/sugar/addons/versions/%s' % activity_code

            uploader = ''
            activity_name = ''
            compat_from = ''
            compat_to = ''
            try:
                sopa_act = bs(urlopen(act_url))
                try:
                    uploader_div = sopa_act.find('div', {'class': 'uploader'})
                    uploader = uploader_div.find('a').text
                except:
                    pass
                if uploader in ('nickname', ''):
                    # try reading from http://activities.sugarlabs.org/es-ES/sugar/addon/%s
                    try:
                        act_main_url = 'http://activities.sugarlabs.org/es-ES/sugar/addon/%s' % activity_code
                        sopa_act_main = bs(urlopen(act_main_url))
                        uploader = sopa_act_main.find('a', {'class': 'profileLink'}).text
                    except:
                        pass

                try:
                    main_div = sopa_act.find('div', role='main')
                    activity_name = main_div.find('a', href='/es-ES/sugar/addon/%s' % activity_code).text
                except:
                    pass
                try:
                    compat_div = sopa_act.find('div', {'class': 'app_compat'})
                    compat = compat_div.find('li').text.replace('&ndash;', '-')
                    compat = compat.replace('Sugar:', '')
                    compat_from = compat[:compat.find('-')].strip().replace('.',',')
                    compat_to = compat[compat.find('-') + 1:].strip().replace('.',',')

                except:
                    pass
            except:
                pass

            if activity_name != '' and uploader != '':
                print "%s;%s;%s;%s;%s;%s" % (activity_code, date, activity_name, uploader, compat_from, compat_to)

                activity_data = {'code': activity_code, 'date': date,
                        'name': activity_name, 'uploader': uploader,
                        'compat_from': compat_from, 'compat_to': compat_to}
                data.append(activity_data)

    f = open('activities_aslo_stats.json', 'w')
    f.write(json.dumps(data))
    f.close()

else:

    f = open('activities_aslo_stats.json')
    data = json.loads(f.read())
    f.close()

    # count activities by uploader
    uploaders = {}
    for activity_data in data:
        uploader = activity_data['uploader']
        if uploader in uploaders.keys():
            uploaders[uploader] = uploaders[uploader] + 1
        else:
            uploaders[uploader] = 1

    for uploader in uploaders:
        print '%s;%s' % (uploader, uploaders[uploader])
