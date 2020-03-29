import logging, time
from datetime import datetime, timedelta

from common.utils import now
from common.utils import str2json
from common.consts import *

from django.http import JsonResponse

############################################################################
## from common.http import JsonResponseBadRequest, JsonResponseRequest
## from common.http import require_http_params
############################################################################

class JsonResponseBadRequest(JsonResponse):
    def __init__(self, data, message, messageid, **kwargs):
        resp = {}
        resp['data'] = data
        resp['message'] = message
        resp['msgid'] = messageid
        resp['code'] = 400

        logger = logging.getLogger('debug')
        ##logger.debug(resp)
        super(JsonResponseBadRequest, self).__init__(resp, status=200, **kwargs)

class JsonResponseRequest(JsonResponse):
    def __init__(self, data, message="successfully", **kwargs):
        resp = {}
        resp['data'] = data
        resp['message'] = message
        resp['code'] = 200
        resp['server_timestamp'] = time.mktime(now().timetuple())
        super(JsonResponseRequest, self).__init__(resp, status=200, **kwargs)


def require_http_params(request_param_list):
    def decorator(func):

        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            logger = logging.getLogger('debug')
            params = None
            if request.method == 'POST':
                params = request.POST
            elif request.method == 'GET':
                params = request.GET
            elif request.method == 'PUT':
                params = str2json(request.body, request.encoding)
                
            logger.debug('params: %s', params)
            if not all(param in params for param in request_param_list):
                message = 'Param(s) missing'
                data    = {}
                data    = {'params': list(set(request_param_list) - set(params))}
                return JsonResponseBadRequest(data=data, message=message, messageid = MSGID_PARAM_MISSING)

            return func(request, *args, **kwargs)
        return inner
    return decorator

def require_session():
    def decroator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, * args, **kwargs):
            logger = logging.getLogger('debug')
            #if not request.session.get('Username', None):
            #  return HttpResponseRedirect('/#/login')
            #el
            if not request.session.has_key('expiry'):
                return HttpResponseRedirect('/#/login')
            else:
                expiry = datetime.fromtimestamp(request.session['expiry'])
            return func(request, *args, **kwargs)

        return inner
    return decorator

