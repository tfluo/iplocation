import os, sys, json, logging

from common.http import JsonResponseBadRequest, JsonResponseRequest
from common.http import require_http_params
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from common.iplocation import get_location as location
from common.ipfunc import is_ip, ip_int
from common.utils import is_json
from common.consts import *

#####################################################
_METHOD_PREFIX = '/location/'
#####################################################

## 1. get iplist detail
@require_http_methods(['GET'])
# GET /location/
def iplist_show(request):
  #try:
    logger = logging.getLogger('debug')

    body = request.body
    if request.encoding:
        body = body.decode(request.encoding)
    else:
        body = body.decode('utf8')
    if not is_json(body):
        message = 'Invalid request format. (invalid json)'
        data = { 'body': body }
        return JsonResponseBadRequest(data, message, MSGID_INVALID_BODY)

    j = json.loads(body)
    if not 'iplist' in j:
        message = 'Invalid request format. (no key: iplist)'
        data = { }
        return JsonResponseBadRequest(data, message, MSGID_INVALID_BODY)

    iplist = j['iplist']
    result = {}
    for ip in iplist:
        if not is_ip(ip):
            message = 'Invalid IP. \'%s\' does not appear to be an IPv4 or IPv6.' % ip
            data = { 'ip': ip }
            return JsonResponseBadRequest(data, message, MSGID_INVALID_IP)
        result[ip] = location(ip)

    return JsonResponseRequest(result)
  #except:
  #  s = sys.exc_info()
  #  message = "ERROR: %d: %s" % (s[2].tb_lineno, s[1])
  #  data = { 'message': message }
  #  return JsonResponseBadRequest(data, message, MSGID_INVALID_FUNC)

#####################################################
## 3. get a ip detail
@require_http_methods(['GET'])
# GET /location/xxxxxxxx
def ip_show(request):
    logger = logging.getLogger('debug')

    path = request.get_full_path()
    req_ip = path[len(_METHOD_PREFIX):]

    if not is_ip(req_ip):
        message = 'Invalid IP. "%s" does not appear to be an IPv4 or IPv6.' % req_ip
        data = { 'ip': req_ip }
        return JsonResponseBadRequest(data, message, MSGID_INVALID_IP)

    result = { req_ip: location(req_ip) }

    return JsonResponseRequest(result)

#####################################################
# GET|POST /location/
@csrf_exempt
def get_location(request):
    path = request.get_full_path()

    logger = logging.getLogger('debug')
    logger.debug('path is [%s], method is [%s]', path, request.method)

    if request.method == 'GET':
        return iplist_show(request)
        '''
    elif request.method == 'PUT':
        pass
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass
        '''
    else:
        message = 'Invalid method.'
        data = {'method': request.method }
        return JsonResponseBadRequest(data, message, MSGID_INVALID_METHOD)

#####################################################
# GET|PUT|DEL /location/xxxx
@csrf_exempt
def get_location_entity(request):
    path = request.get_full_path()
    
    logger = logging.getLogger('debug')
    logger.debug('path is [%s], method is [%s]', path, request.method)

    if request.method == 'GET':
        return ip_show(request)
        '''
    elif request.method == 'PUT':
        pass
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass
        '''
    else:
        message = 'Invalid method.'
        data = {'method': request.method }
        return JsonResponseBadRequest(data, message, MSGID_INVALID_METHOD)

#####################################################

