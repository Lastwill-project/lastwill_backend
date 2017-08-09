import requests
import json
import re
from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.middleware import csrf
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from lastwill.settings import ETHERSCAN_API_URL, API_KEY
from lastwill import check, settings

def index(request):
    csrf_token = csrf.get_token(request)
    return render_to_response('index.html', {'csrf_token': csrf_token, 'request': request})


@api_view(http_method_names=['GET'])
def get_balance(request):
    params = {
        'module': 'account',
        'action': 'balance',
        'address': request.GET['address'],
        'tag': 'latest',
        'apikey': API_KEY
    }
    result = requests.get(ETHERSCAN_API_URL, params=params)
    return JsonResponse(json.loads(result.content.decode()))


@api_view(http_method_names=['POST'])
def create_contract(request):
    print (request.data)
    if not check.is_address(request.data['address']):
        raise APIException(code=400, detail='address is not valid')
    for heir in request.data['heirs']:
        if not check.is_address(heir['address']):
            raise APIException(code=400, detail='heir address %s is not valid' % heir['address'])
        if heir['email'] and not check.is_email(heir['email']):
            raise APIException(code=400, detail='heir email %s is not valid' % heir['email'])
        if not check.is_percent(heir['percent']):
            raise APIException(code=400, detail='percent %s is not valid' % heir['percent'])
    if sum([x['percent'] for x in request.data['heirs']]) != 100:
        raise APIException(code=400, detail='percents sum is not equal to 100')
    with open('../lastwill/contracts/LastWillContractTemplate.sol', 'r') as contract_file:
        contract = contract_file.read()
        contract = re.sub('{{targetUser}}', request.data['address'], contract)
        contract = re.sub('{{lastWillAccount}}', settings.LASTWILL_ACCOUNT, contract)
        contract = re.sub('{{recipientPercents}}', 'zzz', contract)

    print(contract) 
    # deploy
    return JsonResponse({'contract': contract})
