#!/usr/bin/env python

# get top-level status

import os, sys, time, json,  urllib2

def test():
    host = "http://localhost:19000/status"
    try:
        req = urllib2.urlopen(host)
        reply = req.read()
        print("Reply data:")
        print(reply)
    except Exception as e:
        print("exception occurred while getting status: "  + str(e))
        return False
    return True

if __name__ == '__main__':
    test()
