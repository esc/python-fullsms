#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import urllib
import ConfigParser
import options

BASE_URL = "https://www.fullsms.de/gw/"

def parse_config(section='settings', config_filename="~/.fullsms"):
    """ Parse a configuration file with app settings.

    Parameters
    ----------
    section : str
        the name of the config section where to look for settings
        (default: 'settings')
    config_filename : str
        the path to and name of the config file
        (default: '~/.fullsms')

    Returns
    -------
    settings : dict
        any settings found in the config file

    Raises
    ------
    IOError:
        if config_filename does not exist
    NoSectionError
        if no section with name 'section' exists

    """
    config_filename = os.path.expanduser(config_filename)
    cp = ConfigParser.RawConfigParser()
    with open(config_filename) as fp:
        cp.readfp(fp)
    return dict(cp.items('settings'))

def assemble_rest_call(function, parameters):
    """ Create a URL suitable for making a REST call to fullsms.de

    Parameters
    ----------
    function : str
        the api function to execute
    parameters : dict
        the parameters to use in the call

    Returns
    -------
    url : str
        an ready made url

    """
    query = urllib.urlencode(sorted(parameters.items()))
    return "%s%s?%s" % (BASE_URL, function, query)

def call(str_):
    file_like = urllib.urlopen(str_)
    return file_like.read()

def assemble_send_str(params):
    return assemble_rest_call('', params)

def assemble_check_str(params):
    return assemble_rest_call('konto.php', params)

def send(user, password, gateway, receiver, sender, message):
    parameters = {
            'user': user,
            'passwort': password,
            'typ': gateway,
            'handynr': receiver,
            'absender': sender,
            'text': message
            }
    rest_str = assemble_rest_call('', parameters)
    return call(rest_str)

def check(user, password):
    params = {'user': user, 'passwort': password}
    str_ = assemble_check_str(params)
    return call(str_)

if __name__ == '__main__':
    subcommands = ['send', 'check']
    optspec = """
    sms %s [opts] <message>
    --
    u,user= the fullsms.de username
    p,password the fullsms.de password
    g,gateway= the gateway to use
    r,receiver= the person to send the message to
    s,sender= the sender to use
    """ % ('[' + ' | '.join(subcommands) + ']')
    o = options.Options(optspec)
    (opt, flags, extra) = o.parse(sys.argv[1:])
    cfs = parse_config()
    if extra[0] not in ['check']:
        options.fatal('invalid subcommand')
    elif extra[0] == 'check':
        result = check(cfs['user'], cfs['password'])
        if result is not None:
            return "The current balance for the account %s is: %s €" % (result 
        else:
            options.fatal("Error checking balance")

