#!/usr/bin/env python

import os
import time
import doctest

def do_tests():
    tests = [
             "fanimplications", 
             "fanpoints",
             #"xcombinations", 
             "HTMLTags", 
             "mahjongutil", 
             "informat", 
             "mahjonggrouping", 
             "maxpoints",
             "identifan", 
             "mahtml", 
            ]
    for t in tests:
        print "%s: " % t
        start_time = time.time()
        module = __import__(t)
        tests_failed, tests_performed = doctest.testmod(module)
        s_duration = time.time() - start_time
        print ("%d tests, %d failed in %.2fs --\n" % 
              (tests_performed, tests_failed, s_duration))

if __name__ == "__main__":
    """
    import cProfile
    profile_file = 'test_all.prof'
    cProfile.run('do_tests()', 'test_all.prof')
    from pstats import Stats
    s = Stats(profile_file)
    s.strip_dirs()
    s.sort_stats('time')
    s.print_stats(12)
    """
    do_tests()
