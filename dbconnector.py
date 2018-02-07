#!/usr/bin/env python3

import mysql.connector


class MySql:
    
    def __init__(self, db_config):
        self.cnx = mysql.connector.connect(**db_config)

    def select_data(self, itemid, before, after):
        query = """SELECT clock, value
                   FROM history_uint
                   WHERE itemid='{0}' 
                   AND clock>='{1}'
                   AND clock<='{2}'""".format(itemid, before, after)
        cursor = self.cnx.cursor()
        cursor.execute(query)
        for (clock, value) in cursor:
            yield (clock, value)
        cursor.close()


    def get_itemid(self, node, interface):
        query = """SELECT i.itemid, i.key_
                   FROM hosts h, items i 
                   WHERE i.flags in (4,0) 
                   AND i.hostid=h.hostid 
                   AND h.name like '{0}' 
                   AND i.key_ regexp '.*Octets.*{1}.*'""".format(node, interface)
        cursor = self.cnx.cursor()
        cursor.execute(query)
    
        retid = {}
        for itemid, key in cursor:
            if 'In' in key:
                retid['IN'] = itemid
            if 'Out' in key:
                retid['OUT'] = itemid
        cursor.close()
        return retid

if __name__ == "__main__":
    # test
    import parseconf
    conf = parseconf.ParseConf()
    mysql = MySql(conf.get_db_conn())
    ret = mysql.get_itemid('msk20-rtr1', 'GigabitEthernet0/2')
    for inout, itemid in ret.items():
        print(inout)
        ret2 = mysql.select_data(itemid, '1506574800', '1506578400')
        for clock, value in ret2:
            print(clock, value)
