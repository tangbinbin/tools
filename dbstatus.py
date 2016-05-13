#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import MySQLdb
import time
import datetime
import sys
import getopt

def usage():
    sl = [
            "dbstatus.py usage:",
            "--help: print help message",
            "-h: mysql host",
            "-P: mysql Port",
            "-u: mysql user",
            "-p: mysql password",
         ]
    print "\n    ".join(sl)
    print "\nexample:"
    print "    ./dbstatus.py -h127.0.0.1 -P3306 -utest -ptest"

def get_conn(Host, Port, User, Passwd):
    db =  MySQLdb.connect(
            user    = User,
            passwd  = Passwd,
            host    = Host,
            port    = Port,
            charset = 'utf8')
    return db

def echo_state(db):
    cursor = db.cursor()
    cursor.execute("set autocommit=1")

    sql = "show global status where variable_name in \
            ('Questions', 'Com_select', 'Com_update',\
            'Com_insert', 'Com_delete', 'Threads_connected',\
            'Threads_created', 'Threads_running',\
            'Innodb_rows_inserted', 'Innodb_rows_read',\
            'Innodb_rows_updated', 'Innodb_rows_deleted',\
            'Bytes_received','Bytes_sent')"

    q = {
            'Questions':0,
            'Com_select':0,
            'Com_update':0,
            'Com_insert':0,
            'Com_delete':0,
            'Threads_connected':0,
            'Threads_created':0,
            'Threads_running':0,
            'Innodb_rows_inserted':0,
            'Innodb_rows_read':0,
            'Innodb_rows_updated':0,
            'Innodb_rows_deleted':0,
            'Bytes_received':0,
            'Bytes_sent':0
        }

    sta = dict()

    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        sta[row[0]] = int(row[1])

    i = 0
    while True:
        time.sleep(1)
        if i%20==0:
            head =  ("|","--QPS--","|"," --Innodb Rows Status-- |  --Thread--  | --kbytes-- ")
            print "\033[0;46;1m%9s%18s%10s%s\033[0m" % head
            l =  ("time|", "ins", "upd", "del",
                    "sel", "qps|", "ins", "upd",
                    "del", "read|", "run", "con",
                    "cre|", "recv", "send")
            print "\033[0;32;1m%9s%5s%5s%5s%6s%7s%5s%6s%6s%8s%4s%5s%6s%6s%6s\033[0m" % l
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            k = row[0]
            v = int(row[1])

            if k == 'Threads_running' or k == 'Threads_connected':
                q[k] = v
            else:
                q[k] = v - sta[k]
                sta[k] = v

        il = (
                datetime.datetime.now().strftime("%H:%M:%S"),
                q['Com_insert'],
                q['Com_update'],
                q['Com_delete'],
                q['Com_select'],
                q['Questions'],
                q['Innodb_rows_inserted'],
                q['Innodb_rows_updated'],
                q['Innodb_rows_deleted'],
                q['Innodb_rows_read'],
                q['Threads_running'],
                q['Threads_connected'],
                q['Threads_created'],
                q['Bytes_received']/1000+1,
                q['Bytes_sent']/1000+1,
             )
        print "\033[0;33;1m%s\033[0m|%5d%5d%5d%6d%6d|%5d%6d%6d%7d|%4d%5d%5d|%6d%6d" % il
        i += 1

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h:P:u:p:", ["help"])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)

    Host = "127.0.0.1"
    Port = 3306
    for o, a in opts:
        if o == "--help":
            usage()
            sys.exit(1)
        elif o == "-h":
            Host = a
        elif o == "-P":
            Port = int(a)
        elif o == "-u":
            User = a
        elif o == "-p":
            Passwd = a
        else:
            print "unhandled option"
            sys.exit(3)

    db = get_conn(Host, Port, User, Passwd)
    echo_state(db)

if __name__ == '__main__':
    ''' '''
    main(sys.argv[1:])
