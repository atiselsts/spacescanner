#!/usr/bin/env python

# get status of a run

import os, sys, time, json,  urllib2

def test():
    host = "http://localhost:19000/runs/2"
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
