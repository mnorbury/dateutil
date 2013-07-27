"""
Module:
    dateutil.py

Description:
    Module containing useful datetime utility functions.

Author:
    Martin Norbury (mnorbury@lcogt.net)

December 2012
"""

import time, re
import datetime as dt
import logging

logger = logging.getLogger(__name__)

DAYS2SECONDS         = 24*60*60
MICROSECONDS2SECONDS = 1/1000000.0
YEARCHARS            = 4
DATETIMECHARS        = 2


def datetime2unixtime( timestamp ):
    ''' Convert a datetime instance to unixtime. '''
    microsecond = timestamp.microsecond / 1000000.0
    return time.mktime( timestamp.timetuple() ) + microsecond

def unixtime2datetime( timestamp ):
    ''' Convert unixtime to datetime instance. '''
    return dt.datetime.utcfromtimestamp( timestamp )

def timedelta2seconds( timedelta ):
    days         = timedelta.days * DAYS2SECONDS
    seconds      = timedelta.seconds
    microseconds = timedelta.microseconds * MICROSECONDS2SECONDS
    return days + seconds + microseconds

def parse( datetime_string ):
    '''
    Convert a string into a datetime, date or time object.

    The input string accepts any of the following:-

    - YYYYMMDD[[[HH]MM]SS]
    - YYYY-MM-DDTHH-MM-SS.sss
    - YYYY-MM-DD
    - HH-MM-DD
    '''
    logger.debug("Parsing {0}".format( datetime_string ))

    results    = re.split('-|T|:|\.| ', datetime_string.rstrip('Z') )
    if len(results) == 1:
        results = __parse_datestring( datetime_string )

    components = [ int( component ) for component in results ]

    logger.debug("Processing components {0}".format(components))

    if __datestring( datetime_string ):
        logging.debug("Converting to date instance")
        return dt.date( *components )

    if __timestring( datetime_string ):
        logging.debug("Converting to time instance")
        if __fractional_second( datetime_string ) :
            logging.debug("Scaling fractional second to microseconds")
            components[-1] *= 1000
        return dt.time( *components )

    if __fractional_second( datetime_string ) :
        logging.debug("Scaling fractional second to microseconds")
        components[-1] *= 1000
    logging.debug("Returning datetime instance")
    return dt.datetime( *components )

def __datestring( inputstring ):
    ''' Return true if this is a date string. '''
    return '-' in inputstring and not ':' in inputstring

def __fractional_second( inputstring ):
    ''' Return true if we contain fractional seconds. '''
    return '.' in inputstring

def __timestring( inputstring ):
    ''' Return true if this is a time string. '''
    return ':' in inputstring and not '-' in inputstring

def __parse_datestring( input_string ):
    year, remainder = input_string[:YEARCHARS], input_string[YEARCHARS:]
    yield year
    while remainder:
        value, remainder = remainder[:DATETIMECHARS], remainder[DATETIMECHARS:]
        yield value
