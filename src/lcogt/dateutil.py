"""
Module:
    dateutil.py

Description:
    Module containing useful datetime utility functions.

Author:
    Martin Norbury (mnorbury@lcogt.net)

December 2012
"""

from __future__ import division
import math
import calendar, re
import datetime as dt
import logging
import warnings

logger = logging.getLogger(__name__)

DAYS2SECONDS         = 24*60*60
MICROSECONDS2SECONDS = 1/1000000.0
YEARCHARS            = 4
DATETIMECHARS        = 2
SECONDS2MICROSECONDS = 10**6

class ParseException(Exception):
    ''' Exception for all internal parsing errors. '''
    pass

def datetime2unixtime( timestamp ):
    ''' Convert a datetime instance to unixtime. '''
    microsecond = timestamp.microsecond / 1000000.0
    return calendar.timegm( timestamp.timetuple() ) + microsecond

def unixtime2datetime( timestamp ):
    ''' Convert unixtime to datetime instance. '''
    return dt.datetime.utcfromtimestamp( timestamp )

def timedelta2seconds( td ):
    ''' Return the length of the timedelta, in seconds. '''
    return (td.microseconds + (td.seconds + td.days * DAYS2SECONDS)
            * SECONDS2MICROSECONDS) / SECONDS2MICROSECONDS

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

    results    = re.split('-|T|:| ', datetime_string.rstrip('Z') )

    # Deal with the 'filename' format, which has no delimiters
    if len(results) == 1:
        results = __parse_datestring( datetime_string )

    try:
        components = [ _convert_component(component) for component in results ]
    except ValueError as e:
        msg = "Unable to create datetime from '%s'" % datetime_string
        raise ParseException(msg)

    logger.debug("Processing components {0}".format(components))

    if __datestring( datetime_string ):
        logging.debug("Converting to date instance")
        return __create_dt_type('date', components)

    if __timestring( datetime_string ):
        logging.debug("Converting to time instance")
        if __fractional_second( datetime_string ) :
            logging.debug("Scaling fractional second to microseconds")
            remainder, seconds = math.modf(components[-1])
            components = components[:-1] + [int(seconds), int(remainder*1000000)]
        return __create_dt_type('time', components)

    if __fractional_second( datetime_string ) :
        logging.debug("Scaling fractional second to microseconds")
        remainder, seconds = math.modf(components[-1])
        components = components[:-1] + [int(seconds), int(remainder*1000000)]
    logging.debug("Returning datetime instance")
    return __create_dt_type('datetime', components)

def __create_dt_type(function_name, components):
    ''' Convert tokenised input into date, time or datetime objects as appropriate,
        repackaging any exceptions.

        DeprecationWarnings are raised as ParseException to force early versions of
        Python (e.g 2.6.x) to comply with later versions (2.7.x).
    '''
    try:
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered
            warnings.simplefilter("always")

            # Actually create the date instance
            date = getattr(dt, function_name)( *components )

            # Raise an exception if we have any warnings
            if len(w):
                warning = w[0]
                msg     = str(warning.message)
                raise ParseException(msg)

            return date
    except (TypeError, ValueError) as e:
        msg = str(e)
        raise ParseException(msg)

def _convert_component(component):
    ''' Cast an incoming string to an appropriate number. '''
    if '.' in component:
        return float(component)
    return int(component)

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
    ''' Tokenise the input string into year, dt_component chunks. '''
    year, remainder = input_string[:YEARCHARS], input_string[YEARCHARS:]
    yield year
    while remainder:
        value, remainder = remainder[:DATETIMECHARS], remainder[DATETIMECHARS:]
        yield value
