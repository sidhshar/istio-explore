#!/usr/bin/python
#
# Copyright 2017 Istio Authors
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


from flask import Flask, request, render_template, redirect, url_for
import simplejson as json
import requests
import sys
from json2html import *
import logging

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

app = Flask(__name__)
logging.basicConfig(filename='microservice.log',filemode='w',level=logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

from flask_bootstrap import Bootstrap
Bootstrap(app)

VULNERABILITY_ASSESSMENT_SERVER_IP = "35.237.198.143"
VULNERABILITY_ASSESSMENT_URL = "http://%s/performvulassessment" % (VULNERABILITY_ASSESSMENT_SERVER_IP,)


details = {
    "name" : "http://details:9080",
    "endpoint" : "details",
    "children" : []
}

financedetails = {
    "name" : "http://financedetails:9080",
    "endpoint" : "financedetails",
    "children" : []
}

findetails = {
    "name" : "http://findetails:9080",
    "endpoint" : "findetails",
    "children" : []
}

workexpdetails = {
    "name" : "http://workexpdetails:9080",
    "endpoint" : "workexpdetails",
    "children" : []
}

hrdetails = {
    "name" : "http://hrdetails:9080",
    "endpoint" : "hrdetails",
    "children" : []
}

ratings = {
    "name" : "http://ratings:9080",
    "endpoint" : "ratings",
    "children" : []
}

hratings = {
    "name" : "http://hratings:9080",
    "endpoint" : "hratings",
    "children" : []
}

reviews = {
    "name" : "http://reviews:9080",
    "endpoint" : "reviews",
    "children" : [ratings]
}

productpage = {
    "name" : "http://productpage:9080",
    "endpoint" : "details",
    "children" : [details, reviews]
}

service_dict = {
    "productpage" : productpage,
    "details" : details,
    "reviews" : reviews,
}

def getForwardHeadersOnlyHeader(request):
    headers = {}

    user_cookie = request.cookies.get("user")
    if user_cookie:
        headers['Cookie'] = 'user=' + user_cookie

    incoming_headers = [ 'x-request-id',
                         'x-b3-traceid',
                         'x-b3-spanid',
                         'x-b3-parentspanid',
                         'x-b3-sampled',
                         'x-b3-flags',
                         'x-ot-span-context',
                         'x-is-allowed'
    ]

    for ihdr in incoming_headers:
        val = request.headers.get(ihdr)
        if val is not None:
            headers[ihdr] = val

    return headers

def get_remote_address(request):
    # TODO: Need to change based on the request parameters from Istio Gateway
    if request.headers.getlist("X-Forwarded-For"):
        remote_addr = request.headers.getlist("X-Forwarded-For")[0]
    else:
        remote_addr = request.remote_addr
    return remote_addr

def getForwardHeaders(request):
    headers = {}

    user_cookie = request.cookies.get("user")
    is_allowed_cookie = request.cookies.get("x-is-allowed-c")
    if is_allowed_cookie and user_cookie:
        headers['Cookie'] = 'user=' + user_cookie + '; x-is-allowed-c=' + is_allowed_cookie
    elif user_cookie:
        headers['Cookie'] = 'user=' + user_cookie
    elif is_allowed_cookie:
        headers['Cookie'] = 'x-is-allowed-c=' + is_allowed_cookie

    incoming_headers = [ 'x-request-id',
                         'x-b3-traceid',
                         'x-b3-spanid',
                         'x-b3-parentspanid',
                         'x-b3-sampled',
                         'x-b3-flags',
                         'x-ot-span-context',
                         #'x-is-allowed'
    ]

    # incoming_headers = [ 'x-request-id',
    #                      'x-b3-traceid',
    #                      'x-b3-spanid',
    #                      'x-b3-parentspanid',
    #                      'x-b3-sampled',
    #                      'x-b3-flags',
    #                      'x-ot-span-context',
    #                      'x-is-allowed'
    # ]

    print 'In getForwardHeaders -->>>>> Printing all incoming headers...'
    for k, v in request.headers.items():
        print 'k: %s, v: %s' % (k, v,)

    for ihdr in incoming_headers:
        val = request.headers.get(ihdr)
        if val is not None:
            headers[ihdr] = val
            #print "incoming: "+ihdr+":"+val

    # Preserve the request initiator Host and User Agent fields for external service call
    headers['x-initiator-host'] = request.headers.get('Host')
    headers['x-initiator-ua'] = request.headers.get('User-Agent')
    remote_addr = get_remote_address(request)
    headers['x-initiator-remote-addr-1'] = remote_addr
    headers['x-initiator-remote-addr-2'] = request.remote_addr
    # if not headers.has_key('x-is-allowed'):
    #     headers['x-is-allowed'] = '0'

    print 'Exiting getForwardHeaders.........'
    return headers


# The UI:
@app.route('/')
@app.route('/index.html')
def index():
    """ Display productpage with normal user and test user buttons"""
    global productpage

    table = json2html.convert(json=json.dumps(productpage),
                              table_attributes="class=\"table table-condensed table-bordered table-hover\"")

    return render_template('index.html', serviceTable=table)


@app.route('/health')
def health():
    return 'E page is healthy'


@app.route('/login', methods=['POST'])
def login():
    user = request.values.get('username')
    response = app.make_response(redirect(request.referrer))
    response.set_cookie('user', user)
    return response


@app.route('/logout', methods=['GET'])
def logout():
    response = app.make_response(redirect(request.referrer))
    response.set_cookie('user', '', expires=0)
    return response


@app.route('/productpage')
def front():
    product_id = 0 # TODO: replace default value
    headers = getForwardHeaders(request)
    user = request.cookies.get("user", "")
    product = getProduct(product_id)
    detailsStatus, details = getProductDetails(product_id, headers)
    reviewsStatus, reviews = getProductReviews(product_id, headers)
    return render_template(
        'productpage.html',
        detailsStatus=detailsStatus,
        reviewsStatus=reviewsStatus,
        product=product,
        details=details,
        reviews=reviews,
        user=user)

@app.route('/employeepage')
def employeeFront():
    product_id = 0 # TODO: replace default value
    headers = getForwardHeaders(request)
    user = request.cookies.get("user", "")
    product = getProduct(product_id)

    # Making an external call to get the vulnerability assessment
    #external_call_response = requests.get(VULNERABILITY_ASSESSMENT_URL, headers=headers)
    #external_call_response_content = external_call_response.content
    #extresponsedict = external_call_response.content
    #return extresponsedict

    try:
        external_call_response = requests.get(VULNERABILITY_ASSESSMENT_URL, headers=headers)
        app.logger.info("In employeepage external_call_response: %s" % (external_call_response,))
        extresponsedict = json.loads(external_call_response.content)
        app.logger.info("In employeepage extresponsedict: %s" % (extresponsedict,))
        if extresponsedict.has_key('result') and extresponsedict['result']['x_is_enabled'] is True:
            headers.update({ 'x-is-allowed': '1' })
        else:
            headers.update({ 'x-is-allowed': '0' })
    except Exception, e:
        app.logger.info("Exception while invoking external service: %s" % (e,))
        headers.update({ 'x-is-allowed': '0' })

    # if type(extresponsedict) == type({}) and extresponsedict.has_key('x_is_enabled'):
    #     if extresponsedict['x_is_enabled'] is True:
    #         headers.update({ 'x-is-allowed': '1' })
    #         app.logger.info("Marking x-is-allowed 1")
    #     else:
    #         headers.update({ 'x-is-allowed': '0' })
    #         app.logger.info("Marking x-is-allowed 0")
    # else:
    #     app.logger.info("Could not find x-is-allowed in response")

    app.logger.info("Proceeding with these headers: %s" % (headers,))

    #app.logger.info("In employeepage external_call_response: %s external_call_response_content: %s" % (external_call_response, extresponsedict,))

    detailsStatus, details = getProductDetails(product_id, headers)
    reviewsStatus, reviews = getProductReviews(product_id, headers)

    #financeStatus, financeData = 200, {'type':'financeData'}
    financeStatus, financeData = getFinanceDetails(product_id, headers)
    workexpStatus, workexpData = getWorkExpDetails(product_id, headers)
    hrStatus, hrData = getHRDetails(product_id, headers)

    # NodeJs based endpoint
    ratingStatus, ratings = getProductRatings(product_id, headers)
    hratingStatus, hratings = getProductHratings(product_id, headers)
    finStatus, finData = getFinDetails(product_id, headers)

    return render_template(
        'employeepage.html',
        detailsStatus=detailsStatus,
        reviewsStatus=reviewsStatus,
        financeStatus=financeStatus,
        finStatus=finStatus,
        workexpStatus=workexpStatus,
        hrStatus=hrStatus,
        product=product,
        details=details,
        reviews=reviews,
        financeData=financeData,
        ratings=ratings,
        hratings=hratings,
        finData=finData,
        workexpData=workexpData,
        hrData=hrData,
        user=user)


# The API:
@app.route('/api/v1/products')
def productsRoute():
    return json.dumps(getProducts()), 200, {'Content-Type': 'application/json'}


@app.route('/api/v1/products/<product_id>')
def productRoute(product_id):
    headers = getForwardHeaders(request)
    status, details = getProductDetails(product_id, headers)
    return json.dumps(details), status, {'Content-Type': 'application/json'}


@app.route('/api/v1/products/<product_id>/reviews')
def reviewsRoute(product_id):
    headers = getForwardHeaders(request)
    status, reviews = getProductReviews(product_id, headers)
    return json.dumps(reviews), status, {'Content-Type': 'application/json'}


@app.route('/api/v1/products/<product_id>/ratings')
def ratingsRoute(product_id):
    headers = getForwardHeaders(request)
    status, ratings = getProductRatings(product_id, headers)
    return json.dumps(ratings), status, {'Content-Type': 'application/json'}



# Data providers:
def getProducts():
    return [
        {
            'id': 0,
            'title': 'Employee Name: T. Baker',
            'descriptionHtml': 'TME',
            'departmentHtml': 'CSG'
        }
    ]


def getProduct(product_id):
    products = getProducts()
    if product_id + 1 > len(products):
        return None
    else:
        return products[product_id]


def getProductDetails(product_id, headers):
    try:
        url = details['name'] + "/" + details['endpoint'] + "/" + str(product_id)
        res = requests.get(url, headers=headers, timeout=3.0)
    except:
        res = None
    if res and res.status_code == 200:
        return 200, res.json()
    else:
        status = res.status_code if res is not None and res.status_code else 500
        return status, {'error': 'Sorry, E details are currently unavailable for this book.'}

def getFinanceDetails(product_id, headers):
    try:
        url = financedetails['name'] + "/" + financedetails['endpoint'] + "/" + str(product_id)
        res = requests.get(url, headers=headers, timeout=3.0)
    except:
        res = None
    if res and res.status_code == 200:
        return 200, res.json()
    else:
        status = res.status_code if res is not None and res.status_code else 500
        return status, {'error': 'Sorry, Finance details are currently unavailable for this employee.'}

def getFinDetails(product_id, headers):
    try:
        url = findetails['name'] + "/" + findetails['endpoint'] + "/" + str(product_id)
        res = requests.get(url, headers=headers, timeout=3.0)
    except:
        res = None
    if res and res.status_code == 200:
        return 200, res.json()
    else:
        status = res.status_code if res is not None and res.status_code else 500
        return status, {'error': 'Sorry, Fin details are currently unavailable for this employee.'}


def getWorkExpDetails(product_id, headers):
    try:
        url = workexpdetails['name'] + "/" + workexpdetails['endpoint'] + "/" + str(product_id)
        res = requests.get(url, headers=headers, timeout=3.0)
    except:
        res = None
    if res and res.status_code == 200:
        return 200, res.json()
    else:
        status = res.status_code if res is not None and res.status_code else 500
        return status, {'error': 'Sorry, Work Exp details are currently unavailable for this employee.'}

def getHRDetails(product_id, headers):
    try:
        url = hrdetails['name'] + "/" + hrdetails['endpoint'] + "/" + str(product_id)
        res = requests.get(url, headers=headers, timeout=3.0)
    except:
        res = None
    if res and res.status_code == 200:
        return 200, res.json()
    else:
        status = res.status_code if res is not None and res.status_code else 500
        return status, {'error': 'Sorry, HR details are currently unavailable for this employee.'}


def getProductReviews(product_id, headers):
    ## Do not remove. Bug introduced explicitly for illustration in fault injection task
    ## TODO: Figure out how to achieve the same effect using Envoy retries/timeouts
    for _ in range(2):
        try:
            url = reviews['name'] + "/" + reviews['endpoint'] + "/" + str(product_id)
            res = requests.get(url, headers=headers, timeout=3.0)
        except:
            res = None
        if res and res.status_code == 200:
            return 200, res.json()
    status = res.status_code if res is not None and res.status_code else 500
    return status, {'error': 'Sorry, E reviews are currently unavailable for this book.'}


def getProductRatings(product_id, headers):
    try:
        url = ratings['name'] + "/" + ratings['endpoint'] + "/" + str(product_id)
        res = requests.get(url, headers=headers, timeout=3.0)
    except:
        res = None
    if res and res.status_code == 200:
        return 200, res.json()
    else:
        status = res.status_code if res is not None and res.status_code else 500
        return status, {'error': 'Sorry, E ratings are currently unavailable for this book.'}

def getProductHratings(product_id, headers):
    try:
        url = hratings['name'] + "/" + hratings['endpoint'] + "/" + str(product_id)
        res = requests.get(url, headers=headers, timeout=3.0)
    except:
        res = None
    if res and res.status_code == 200:
        return 200, res.json()
    else:
        status = res.status_code if res is not None and res.status_code else 500
        return status, {'error': 'Sorry, E hratings are currently unavailable for this book.'}



class Writer(object):
    def __init__(self, filename):
        self.file = open(filename,'w')

    def write(self, data):
        self.file.write(data)
        self.file.flush()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "usage: %s port" % (sys.argv[0])
        sys.exit(-1)

    p = int(sys.argv[1])
    sys.stderr = Writer('stderr.log')
    sys.stdout = Writer('stdout.log')
    print "start at port %s" % (p)
    app.run(host='0.0.0.0', port=p, debug=True, threaded=True)
