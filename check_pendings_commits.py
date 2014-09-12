#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

POOTLE_DIR = '/var/lib/pootle/checkouts'
OUTPUT = '/home/godiard/pending_commits.html'

out = open(OUTPUT, 'w')

langs =  ['af', 'am', 'ar', 'ar_SY', 'ay', 'bg', 'bi', 'bn', 'bn_IN', 'bs',
        'ca', 'cpp', 'cs', 'de','dz', 'el', 'es', 'fa', 'fa_AF', 'ff', 'fi', 'fil',
        'gu', 'ha', 'he', 'hi', 'ht', 'hu', 'hus', 'ig', 'is', 'it', 'ja',
        'km', 'kn', 'ko', 'kos', 'lv', 'mg', 'mk', 'ml', 'mn', 'mr', 'ms',
        'mvo', 'na', 'nb', 'ne', 'nl', 'nn', 'pa', 'pap', 'pis', 'pl', 'ps',
        'pt', 'pt_BR', 'quy', 'quz', 'ro', 'ru', 'rw', 'sd', 'si', 'sk', 'sl', 'sm',
        'st', 'sv', 'sw', 'ta', 'te', 'th', 'ton', 'tpi', 'tr', 'tvl', 'tzo',
        'ug', 'uk', 'ur', 'vi', 'wa', 'yo', 'zh_CN', 'zh_TW']


projects = ['fructose', 'glucose', 'honey', 'glucose92',
        'fructose84', 'glucose84',  'dextrose3', 'olpc_software']
cant_langs = len(langs)

out.write('<html><body>')
out.write('<table>')
out.write('<tr><th>Module</th><th>Git</th>')

out.write('<head>' +
        '<style type=text/css>' +
        'body {' + 
        '    background-color:#d0e4fe;' +
        '    font-family:Arial;' +
        '    font-size:10px;}' +
        'p {' +
        '    font-size:14px;' +
        '    color:orange;}' +
        'th {' +
        '    background-color:grey;' +
        '    color:orange;' +
        '    text-align:center;}' +
        'td {' +
        '    background-color:white;}' +
        '</style></head>')

for lang in langs:
    out.write('<th>%s</th>' % lang)
out.write('</tr>\n')

for project in projects:
    out.write('<tr><th> %s </th><th></th><th colspan="%d"></th></tr>' % 
            (project, cant_langs))
    for module in os.listdir(os.path.join(POOTLE_DIR, project)):
        if not module.endswith('.old') and \
                not module.endswith('.bak'):
            module_dir = os.path.join(POOTLE_DIR, project, module)
            if os.path.isdir(module_dir) and \
                    os.path.isdir(os.path.join(module_dir, 'po')):
                out.write('<tr><th> %s </th>' % module)
                # check push status
                push_status = subprocess.Popen(['sudo', '-u', 'pootle',
                        'git', 'push', '-n'], stderr=subprocess.PIPE,
                        stdout=subprocess.PIPE).communicate()[1]
                in_signature = True
                push_msj = ''
                #print push_status
                for line in push_status.split('\n'):
                    if not in_signature:
                        push_msj += line
                    if line == '+-----------------+':
                        in_signature = False
                if push_msj.endswith('Everything up-to-date') or push_msj == '':
                    out.write('<th>OK</th>')
                else:
                    out.write('<th><a href="javascript:alert(\'%s\')" ' % 
                            push_msj.replace("'","*") + 'style="color:red">ERROR</a></th>')

                # check git status
                module_state = {}
                os.chdir(os.path.join(module_dir, 'po'))
                status = subprocess.Popen(['sudo', '-u', 'pootle',
                        'git', 'status', '-s'],
                        stdout=subprocess.PIPE).communicate()[0]


                for line in status.split('\n'):
                    words = line.split()
                    if words == []:
                        break
                    state = words[0]
                    if words[1].endswith('.po'):
                        lang = words[1][:-3]
                        if lang in langs:
                            module_state[lang] = state
                for lang in langs:
                    if lang in module_state:
                        out.write('<td>%s</td>' % module_state[lang])
                    else:
                        out.write('<td></td>')
                out.write('</tr>\n')


out.write('</table>')
out.write('</body></html>')

