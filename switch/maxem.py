"""
Support for Maxem chargepoll switch.

Add the following to your configuration.yaml
switch: 
  - platform: maxem
    email: ""
    password: ""
    maxemBoxID: ""
"""
import logging
import voluptuous as vol 
import homeassistant.helpers.config_validation as cv

from homeassistant.components.switch import (PLATFORM_SCHEMA)
from homeassistant.const import STATE_OFF, STATE_ON
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)
_LOGGER.info("Maxem ====> Maxem.py switch")

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required('email'): cv.string, 
    vol.Required('password'): cv.string, 
    vol.Required('maxemBoxID'): cv.string,
})


#***************************************************************
#
# MAXEM_API: this contains all the code to communicate with the 
# the API of Maxem. 
# Todo: move to a seperate file
#
#**************************************************************
#from sys import version_info
import requests
import logging
import json

# Common definitions
_VERSION_HEADER = 'application/api.maxem.user-v1'
_BASE_URL = "https://api.maxem.io/"
_LOGGER = logging.getLogger(__name__)

def authenticate(email, password):
    params = dict(email= email, password= password)
    headers = {'Content-Type' : 'application/json', 'accept' : _VERSION_HEADER}
    url = _BASE_URL + "authenticate?isMobile=true"
    try:
        resp = requests.post(url, data=json.dumps(params), headers=headers)
        _LOGGER.info("Maxem API-Authenticate-call ========>" + str(resp))
        if resp.status_code == 200: 
            # the response is a string. the first part is the HTTP_Cookie. Split the string
            maxem_cookie = resp.headers["set-cookie"].split(';') 
            _LOGGER.info("Maxem API-Authenticate-call ========>" + maxem_cookie)
            return maxem_cookie[0]  #return the cookie.    
    except ValueError:
        _LOGGER.error("maxem_api.py" + ValueError)
        return ValueError

def set_chargePoll(email, password, maxemBoxID, enabled):
    # first call the authenticate to be sure the session is not timed out
    maxem_cookie = authenticate(email, password)

    params = dict(enabled)
    headers = {'Content-Type' : 'application/json', 'accept' : _VERSION_HEADER, 'cookie': maxem_cookie}
    url = _BASE_URL + maxemBoxID + "/chargepoint/control/enabled?isMobile=true"
    try:
        resp = requests.post(url, data=json.dumps(params), headers=headers)
        _LOGGER.info("Maxem API-set_chargePoll call ========>" + str(resp))
        if resp.status_code == 200: 
            # the response is a string. the first part is the HTTP_Cookie. Split the string
            return True    
    except ValueError:
        _LOGGER.error("maxem_api.py" + ValueError)
        return ValueError

#***************************************************************
#
# MAXEM: code for Hass.io 
#
#**************************************************************


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Maxem switch platform."""
    _LOGGER.info("Maxem ====> Setup_platform started")
    add_devices([MaxemSwitch(config.get('email'), config.get('password'), config.get('maxemBoxID'))])


class MaxemSwitch(Entity):
    """Representation of a Maxem chargerpoll switch."""

    def __init__(self, email, password, maxemBoxID):
        """Initialise of the switch."""
        self._email = email
        self._password = password
        self._maxemBoxID = maxemBoxID
        self._state = None

    def turn_on(self, **kwargs):
        """Send the on command."""
        set_chargePoll(self._email, self._password, self._maxemBoxID, True)
        self._state = True
        _LOGGER.debug("Maxem ===> Enable charging for: %s", self._maxemBoxID)   

    def turn_off(self, **kwargs):
        """Send the off command."""
        set_chargePoll(self._email, self._password, self._maxemBoxID, False)
        self._state = False
        _LOGGER.debug("Maxem ===> Disable charging for: %s", self._maxemBoxID)

    @property
    def is_on(self):
        """Get whether the switch is in on state."""
        return self._state == STATE_ON
