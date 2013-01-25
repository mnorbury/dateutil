'''
Module:
    test_dateutil.py

Description:
    Test cases for the lcogt.dateutil modules.

Author:
    Martin Norbury (mnorbury@lcogt.net)

December 2012
'''

from nose.tools import eq_, assert_almost_equal

from datetime import datetime, date, time, timedelta

from lcogt import dateutil

def test_parse_full_datetime_string():
    datetime_string = "2012-12-06T12:53:56.123"
    result          = dateutil.parse( datetime_string )
    eq_( result, datetime( 2012, 12, 6, 12, 53, 56, 123000 ) )

def test_parse_partial_datetime_string():
    datetime_string = "2012-12-06T12:53:56"
    result          = dateutil.parse( datetime_string )
    eq_( result, datetime( 2012, 12, 6, 12, 53, 56 ) )

def test_parse_datetime_string_with_no_delimiters():
    datetime_string = "20121206125356"
    result          = dateutil.parse( datetime_string )
    eq_( result, datetime( 2012, 12, 6, 12, 53, 56 ) )

def test_parse_partial_datetime_string_with_no_delimiters():
    datetime_string = "20121206"
    result          = dateutil.parse( datetime_string )
    eq_( result, datetime( 2012, 12, 6 ) )

def test_parse_date_string():
    date_string     = "2012-12-06"
    result          = dateutil.parse( date_string )
    eq_( result, date( 2012, 12, 6 ) )

def test_parse_time_string():
    time_string     = "12:53:56.123"
    result          = dateutil.parse( time_string )
    eq_( result, time( 12, 53, 56, 123000 ) )

def test_parse_time_string_without_fractional_seconds():
    time_string     = "12:53:56"
    result          = dateutil.parse( time_string )
    eq_( result, time( 12, 53, 56 ) )

def test_datetime2unixtime():
    timestamp        = datetime(2012,12,6,12,0,0,123000)
    result           = dateutil.datetime2unixtime( timestamp )
    assert_almost_equal( result, 1354824000.123, places=3 )

def test_unixtime2datetime():
    timestamp        = 1354824000.123
    result           = dateutil.unixtime2datetime( timestamp )
    eq_( result, datetime (2012, 12, 6, 20, 0, 0, 123000) )

def test_timedelta2seconds():
    timeinterval     = timedelta( days = 1, minutes = 1, microseconds=100000 )
    result           = dateutil.timedelta2seconds( timeinterval )
    eq_( result, 86460.1 )
