__author__ = 'Philipp Konrad'


import urllib
import requests
import json
import pycurl
import os

TEST_JSON = '''
{
  "column_1":"You say goodbye",
  "column_2":"And I say hello",
  "column_3":"Hello, hello"
}
{
  "column_1":"I don't know why you say goodbye",
  "column_3":"I say hello"
}
'''

class CrowdFlowerError(Exception): pass

'''
{u'alias': None,
 u'auto_order': False,
 u'auto_order_threshold': None,
 u'auto_order_timeout': None,
 u'cml': None,
 u'completed': False,
 u'completed_at': None,
 u'confidence_fields': None,
 u'created_at': u'2014-02-27T10:25:02+00:00',
 u'css': None,
 u'custom_key': None,
 u'design_verified': False,
 u'desired_requirements': None,
 u'excluded_countries': [],
 u'execution_mode': u'worker_ui_remix',
 u'expected_judgments_per_unit': None,
 u'fields': None,
 u'gold': {},
 u'gold_per_assignment': 0,
 u'golds_count': 0,
 u'id': 393918,
 u'included_countries': [],
 u'instructions': u'Good night and good fight',
 u'js': None,
 u'judgments_count': 0,
 u'judgments_per_unit': 3,
 u'language': u'en',
 u'max_judgments_per_ip': None,
 u'max_judgments_per_unit': None,
 u'max_judgments_per_worker': None,
 u'min_unit_confidence': None,
 u'minimum_account_age_seconds': None,
 u'minimum_requirements': {u'min_score': 1,
                           u'priority': 1,
                           u'skill_scores': {u'level_1_contributors': 1}},
 u'options': {u'after_gold': 4,
              u'front_load': False,
              u'ramuh2_url': u'http://ramuh2-003.cloud.doloreslabs.com:8080/ramuh/api/v2',
              u'track_clones': True},
 u'order_approved': False,
 u'pages_per_assignment': 1,
 u'problem': None,
 u'project_number': None,
 u'public_data': False,
 u'require_worker_login': None,
 u'send_judgments_webhook': None,
 u'state': u'unordered',
 u'support_email': u'selfservice_notifications@crowdflower.com',
 u'title': u'Another upload',
 u'units_count': 0,
 u'units_per_assignment': 5,
 u'units_remain_finalized': None,
 u'updated_at': u'2014-02-27T10:25:02+00:00',
 u'variable_judgments_mode': u'none',
 u'webhook_uri': None,
 u'worker_ui_remix': True}
 '''


class CrowdFlowerClient(object):
    '''
    Crowdflower Client for Crowdflower API Version 1

        >>> api_key = 'your_api_key'
        >>> client = CrowdflowerClient(api_key)
    '''
    CROWDFLOWER_BASIC_URL = 'https://api.crowdflower.com/v1/'
    JOB_URL_PTN = 'jobs/upload.json?key=%(api_key)s'


    def __init__(self, api_key):
        '''
        :param str api_key: An API key taken from https://crowdflower.com/account
        '''
        self.query_params = {'api_key':api_key}
        self.api_key = api_key

    def post_job(self, job):
        '''
        :param job:
        '''

        assert 'title' in job, 'Job title is missing %s' % job
        assert 'instructions' in job, 'Job instructions are missing %s' % job

        headers = {'content-type': 'application/json'}

        args = {'job[%s]' % k if k != 'key' else k:v for k, v in job.iteritems()}
        qry_args = urllib.urlencode(args)

        url = "https://api.crowdflower.com/v1/jobs/%s.json?" % job['id']
        url = url + qry_args

        response = requests.put(url, data=json.dumps(job), headers=headers)
        return response.json()


    def create_job(self):
        '''
        :param str title:
        :param str instructions:
        :param int num_judgements:
        :param int cost_in_cent:
        '''
        job_url = self.JOB_URL_PTN % self.query_params
        headers = {'content-type': 'application/json'}
        url = self.CROWDFLOWER_BASIC_URL + job_url

        response = requests.post(url, headers=headers)
        id = response.json().get('id')

        if not id: raise CrowdFlowerError("Could not create job!")

        return CrowdFlowerJob(self, self.api_key, id)



class CrowdFlowerJob(dict):
    '''
    A job helps you to define all properties of a wished job
    and synchronize it with Crowdflower.

        >>> api_key = 'your_api_key'
        >>> client = CrowdflowerClient(api_key)
        >>> job = client.create_job(job_id=1234)

        >>> job.sync()

    '''

    def __init__(self, client, api_key, id):
        super(CrowdFlowerJob, self).__init__()
        self.client = client
        self['id'] = id
        self['key'] = api_key

    def sync(self):
        '''
        Synchronize job with Crowdflower.
        :returns:
        '''
        return self.client.post_job(self)

class CrowdFlowerClient2(object):

    def __init__(self, key):

        self.key = key
        self.upload_url_pattern = 'http://api.crowdflower.com/v1/jobs/%s/upload.json?key=' + key


    def create_job(self, title, instructions, cml=None, callback=None):

        url = "http://api.crowdflower.com/v1/jobs.json"

        post_dict = {'key':self.key,
                     'job[title]':title,
                     'job[instructions]':instructions}

        if cml: post_dict['job[problem]'] = cml

        post_fields = urllib.urlencode(post_dict)

        c = pycurl.Curl()
        c.setopt(pycurl.POST, True)
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.POSTFIELDS, post_fields)

        if callback: c.setopt(pycurl.WRITEFUNCTION, callback)

        c.setopt(pycurl.HTTPHEADER, ['Content-Type : application/json', ])
        c.perform()
        c.close()


    def upload_csv(self, fname, job_id):

        upload_url = self.upload_url_pattern % job_id

        c = pycurl.Curl()
        c.setopt(pycurl.URL, upload_url)
        c.setopt(pycurl.UPLOAD, True)

        c.setopt(pycurl.READFUNCTION, open(fname, 'r').read)

        filesize = os.path.getsize(fname)

        c.setopt(pycurl.INFILESIZE, filesize)
        c.setopt(pycurl.HTTPHEADER, ['Content-type: text/csv'])

        c.perform()
        c.close()


    def create_and_upload(self, title, instructions, fname, cml):

        def job_created_callback(response):

            response_dict = json.loads(response)
            job_id = response_dict['id']
            self.upload_csv(fname=fname, job_id=job_id)

        self.create_job(title, instructions, cml, job_created_callback)


if __name__ == '__main__':
    cml= open('/tmp/test.cml').read()
    
    
    client_a = CrowdFlowerClient('pZMDXJHB9J6cCzVV7ctu')
    client_b = CrowdFlowerClient2('pZMDXJHB9J6cCzVV7ctu')
    #client.create_and_upload('Finally a CSV','this is created as a test', '/tmp/test.csv', cml)
    
    #
    #client.create_job('Matyas a CSV doit3','this is created as a test', cml)
    client_b.upload_csv('/tmp/test.csv', 393963)
