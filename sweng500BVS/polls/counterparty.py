#import json
#import requests
from __future__ import print_function
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse
import time, requests, json


url = "http://localhost:14000/api/"
header = {'content-type': 'application/json'}
auth = HTTPBasicAuth('rpc', 'sweng')

## default port for bitcoin testnet
## (change to 8332 for 'main net'),
rpcPort = 18332
rpcUser = 'bitcoinrpc'
## not a real password
## but if you use the random password generated by bitcoind
## your password should look something like this
rpcPassword = 'rpc'
serverURL = 'http://' + rpcUser + ':' + rpcPassword + '@localhost:' + str(rpcPort)

headers = {'content-type': 'application/json'}

def getBalance(address,asset):
  result = "None"
  payload = {
     "method": "get_balances",
     "params": {
                "filters": [{"field": "address", "op": "==", "value": address}],
                "filterop": "or"
               },
     "jsonrpc": "2.0",
     "id": 0
    }
  node=json.dumps(payload)
  response = requests.post(url, data=node, headers=headers, auth=auth)
  #print("Response for balance check: ", response.text)
  jsonObj = json.loads(response.text)
  for results in jsonObj['result']:
    if results['asset'] == asset:
      result = results['asset'], ":" , results['quantity']
  return result

def getBallotCandidateBalance(candidateAddress, asset):
# Fetch all balances for all assets for both of two addresses, using keyword-based arguments
  payload = {
     "method": "get_balances",
     "params": {
                "filters": [{"field": "address", "op": "==", "value": candidateAddress}],
                "filterop": "or"
               },
     "jsonrpc": "2.0",
     "id": 0
    }
  node=json.dumps(payload)
  response = requests.post(url, data=node, headers=headers, auth=auth)
  jsonObj = json.loads(response.text)
  for results in jsonObj['result']:
    if results['asset'] == asset:
      return results['quantity']
  return 0


def getAssetList(address):
  result = []

  payload = {
     "method": "get_balances",
     "params": {
                "filters": [{"field": "address", "op": "==", "value": address}],
                "filterop": "or"
               },
     "jsonrpc": "2.0",
     "id": 0
    }
  node=json.dumps(payload)
  response = requests.post(url, data=node, headers=headers, auth=auth)
  
  jsonObj = json.loads(response.text)
  for results in jsonObj['result']:
      result.append(results['asset'])
  return result

def createIssuance(address, assetName):
  # Issuance (indivisible)
  payload = {
     "method": "create_issuance",
     "params": {
                "source": address,
                "asset": assetName,
                "quantity": 100,
                "divisible": False,
                "description": "This is issuance of assets for ballot",
                "transfer_destination": "",
                "allow_unconfirmed_inputs": True
               },
     "jsonrpc": "2.0",
     "id": 0
    }
  #response = requests.post(serverURL, headers=headers, data=json.dumps(payload))
  return requests.post(url, data=json.dumps(payload), headers=header, auth=auth)

def createSend(srcAddress, destAddress, assetName):
  # Send 1 XCP (specified in satoshis) from one address to another.
  payload = {
             "method": "create_send",
             "params": {
                        'source': srcAddress, 
                        'destination': destAddress,
                        'asset': assetName,
                        'quantity': 25,
                        "allow_unconfirmed_inputs": True
                       },
             "jsonrpc": "2.0",
             "id": 0
            }

  return requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)

def signRawTransaction(result):
  payload = {
    "method": 'signrawtransaction',
    "params": [result],
    "jsonrpc": "2.0"
    }
  return requests.post(serverURL, headers=headers, data=json.dumps(payload))

def sendRawTransaction(result):
  payload = {
    "method": 'sendrawtransaction',
    "params": [result],
    "jsonrpc": "2.0"
    }
  return requests.post(serverURL, headers=headers, data=json.dumps(payload))

###### NEW CLASS CODE by MXL5588 #########################################



# ## default port for bitcoin testnet
# ## (change to 8332 for 'main net'),
# rpcPort = 18332
# rpcUser = 'bitcoinrpc'
# ## not a real password
# ## but if you use the random password generated by bitcoind
# ## your password should look something like this
# rpcPassword = 'rpc'
btcserverURL = 'http://' + rpcUser + ':' + rpcPassword + '@localhost:' + str(rpcPort)

xcpserverURL = "http://localhost:14000/api/"
#auth = HTTPBasicAuth('rpc', 'sweng')

# counterparty api class
class xcpRPCHost(object):
    def __init__(self, url):
        self._session = requests.Session()
        self._url = url
        self._headers = {'content-type': 'application/json'}
    def call(self, rpcMethod, params):
        #print(self)
        #print(rpcMethod)
        #print(params)
        payload = json.dumps({"method": rpcMethod, "params": params, "jsonrpc": "2.0", "id": 0})
        #print (payload)
        tries = 10
        hadConnectionFailures = False
        while True:
            try:
                response = self._session.post(self._url, headers=self._headers, data=payload, auth=auth)
            except requests.exceptions.ConnectionError:
                tries -= 1
                if tries == 0:
                    raise Exception('Failed to connect for remote procedure call.')
                hadFailedConnections = True
                print("Couldn't connect for remote procedure call, will sleep for ten seconds and then try again ({} more tries)".format(tries))
                time.sleep(10)
            else:
                if hadConnectionFailures:
                    print('Connected for remote procedure call after retry.')
                break
        if not response.status_code in (200, 500):
            raise Exception('RPC connection failure: ' + str(response.status_code) + ' ' + response.reason)
        responseJSON = response.json()
        if 'error' in responseJSON and responseJSON['error'] != None:
            raise Exception('Error in RPC call: ' + str(responseJSON['error']))
        return responseJSON['result']

# bitcoind api class
class btcRPCHost(object):
    def __init__(self, url):
        self._session = requests.Session()
        self._url = url
        self._headers = {'content-type': 'application/json'}
    def call(self, rpcMethod, *params):
        payload = json.dumps({"method": rpcMethod, "params": list(params), "jsonrpc": "2.0"})
        tries = 10
        hadConnectionFailures = False
        while True:
            try:
                response = self._session.post(self._url, headers=self._headers, data=payload)
            except requests.exceptions.ConnectionError:
                tries -= 1
                if tries == 0:
                    raise Exception('Failed to connect for remote procedure call.')
                hadFailedConnections = True
                print("Couldn't connect for remote procedure call, will sleep for ten seconds and then try again ({} more tries)".format(tries))
                time.sleep(10)
            else:
                if hadConnectionFailures:
                    print('Connected for remote procedure call after retry.')
                break
        if not response.status_code in (200, 500):
            raise Exception('RPC connection failure: ' + str(response.status_code) + ' ' + response.reason)
        responseJSON = response.json()
        if 'error' in responseJSON and responseJSON['error'] != None:
            raise Exception('Error in RPC call: ' + str(responseJSON['error']))
        return responseJSON['result']


xcpHost = xcpRPCHost(xcpserverURL)
btcHost = btcRPCHost(btcserverURL)


#create a counterparty asset
def createAsset(sourceAddress, assetName, assetQuantity, assetDescription, isDivisible):
  #try:
    objParams = {"source": sourceAddress,
                          "asset": assetName,
                          "quantity": assetQuantity,
                          "description": assetDescription,
                          "divisible": isDivisible,
                          "allow_unconfirmed_inputs": True}

    unsignedTransaction = xcpHost.call('create_issuance', objParams)
    print("Unsigned Transaction:", unsignedTransaction)
    return unsignedTransaction
  #except:
  # print ("Failed. createAsset()")

# #sign a raw counterparty transaction output
# def signRawTransaction(unsignedTransaction):
#   #try:
#     hash = btcHost.call('signrawtransaction', unsigned )
#     strHex = hash.get('hex')
#     print ("Signed Raw Transaction Hex", strHex)
#     return strHex
#   #except:
#   # print ("Failed. signRawTransaction()")

# #broadcast raw bitcoin transaction
# def sendRawTransaction(signedTransactionHex):
#   #try:
#     broadcast = btcHost.call('sendrawtransaction', signedTransactionHex)
#     print ("Sent Transaction Hash", broadcast)
#     return broadcast
#   #except:
#   # print ("Failed. sendRawTransaction()")

#get rawtransaction data
def getRawTransaction(sentTransaction):
  #try:
    rawhash = btcHost.call('getrawtransaction', sentTransaction)
    print("Raw Transaction:", rawhash)
    return rawhash
  #except:
  # print ("Failed. getRawTransaction()")

# Send 1 XCP (specified in satoshis) from one address to another.
def castVote(userSourceAddress, candidateAddress, assetName, voteQuantity):

  objParams = {"source": userSourceAddress,
  "destination": candidateAddress,
  "asset": assetName,
  "quantity": voteQuantity,
  "allow_unconfirmed_inputs": True}
  unsignedTransaction = xcpHost.call('create_send', objParams)
  print("Unsigned Transaction:", unsignedTransaction)
  return unsignedTransaction

# sign and broadcast transaction
def broadcastSignedTransaction(unsignedTransaction):
  signed = signRawTransaction(unsigned)

  sent = sendRawTransaction(signed)

  raw = getRawTransaction(sent)

  return raw

# unfinished getCandidateBalance
def getCandidateBalance(candidateAddress):
  objParams = {"filters": [{"field": "address", "op": "==", "value": candidateAddress}],
                      "filterop": "or"}
  candidateBalance = xcpHost.call('get_balances', objParams)
  #balance = candidateBalance.get('balance')
  print("Candidate Balance:", candidateBalance)
  return candidateBalance


# lock the ballot
def lockBallot(sourceAddress, assetName):
  objParams = {
                      "source": sourceAddress,
                      "asset": assetName,
                      "quantity": 0,
                      "description": "LOCK"
                     }
  unsignedTransaction = xcpHost.call('create_issuance', objParams)
  print("Unsigned Lock Transaction:", unsignedTransaction)
  return unsignedTransaction

#send btc to fund voter address
def sendBTCToAddress(address, amount):
    sent = btcHost.call('sendtoaddress', address, amount)
    print("Transaction Sent to: ", address)
    print("Amount Sent: ", amount)
    return sent

#burn bitcoin for xcp tokens - quantity is in satoshis of bitcoin to burn
def burnBTC(sourceAddress, burnQuantity):
    objParams = {
            "source": sourceAddress,
            "quantity": burnQuantity
        }
    unsignedTransaction = xcpHost.call('create_burn', objParams)
    print("Unsigned Burn Transaction:", unsignedTransaction)
    return unsignedTransaction

#validate bitcoin address is a valid address
def validateAddress(address):
    validation = btcHost.call('validateaddress', address)
    print("Address Validation: ", validation['isvalid'])
    return validation['isvalid']

def getAssetBalance(address, assetName):
  objParams = {
                "filters": [{"field": "address", "op": "==", "value": address}],
                "filterop": "or"
               }

  payload = xcpHost.call('get_balances', objParams)
  for results in payload:
    if results['asset'] == assetName:
      quantity = results['quantity']
  return quantity


def getXCPTxInfo(rawTransactionHex):
    objParams = {
        "tx_hex": rawTransactionHex
        }
    txInfo = xcpHost.call('get_tx_info', objParams)
    print("Tx Info:", txInfo)
    for results in txInfo:
        dataHex = results
    return dataHex

def getUnconfirmedQuantity(dataHex):
    print("Data Hex: ", dataHex)
    objParams = {
        "data_hex": dataHex
        }
    unpacked = xcpHost.call('unpack', objParams)
    for results in unpacked:
        if results != 0: 
            quantity = results['quantity']
            asset = results['asset']
            #print("UNCONFIRMED QUANTITY: ", quantity)
    return quantity