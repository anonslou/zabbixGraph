#!/usr/bin/env python3

import dbconnector
import parseconf
import painter
import mailsender
from datetime import datetime
from time import mktime

WORK_DIR = '/home/zabbix/python/'

conf = parseconf.ParseConf('{}config.yaml'.format(WORK_DIR))
mysql = dbconnector.MySql(conf.get_db_conn())

today = datetime.now()
today_8am = today.replace(hour=7, minute=45, second=0, microsecond=0)
today_8am = str(int(mktime(today_8am.timetuple())))
today_9am = today.replace(hour=9, minute=15, second=0, microsecond=0)
today_9am = str(int(mktime(today_9am.timetuple())))

files=[]
for node, (name, interfaces) in conf.get_all_nodes().items():
    graph = painter.Plot('{} {}'.format(node,name))
    for descr, port in interfaces.items():
        itemids = mysql.get_itemid(node, port)
        indata = mysql.select_data(itemids['IN'], today_8am, today_9am)
        outdata = mysql.select_data(itemids['OUT'], today_8am, today_9am)
        graph.add_line(indata, 'IN {0} {1}'.format(descr, port))
        graph.add_line(outdata, 'OUT {0} {1}'.format(descr, port))
    graph.paint_graph()
    filename = '{}.png'.format(node)
    graph.save(WORK_DIR+filename)
    files.append(WORK_DIR+filename)

mail = mailsender.MailMe(conf.get_from(), conf.get_to())
mail.set_subjmes('Loading Domain Filials: 10, 20, 30', 'Graphs in attachment')
for f in files:
    mail.add_attach(f)
mail.send_mail(conf.get_mail_server())

