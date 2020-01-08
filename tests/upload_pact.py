# -*- coding: utf-8 -*-
# @Time    : 2020/1/7 下午4:19
# @Author  : yu_hsuan_chen@trendmicro.com
# @File    : upload_pact
# @Version : 3.6
import json
import optparse
import os

import requests
from requests.auth import HTTPBasicAuth


def main():
    parser = optparse.OptionParser()
    parser.add_option(
        '-b', '--broker-path', type='string', dest='input_broker',
        help="Pact Broker Path, http://127.0.0.1", default="http://127.0.0.1")

    parser.add_option(
        '-i', '--input', type='string', dest='input_file',
        help="Pact File Path", default=None)

    parser.add_option(
        '-v', '--version', type="string", dest='input_version',
        help="Pact File Version", default="0.0.1")

    (options, args) = parser.parse_args()
    broker = options.input_broker
    pact_file = options.input_file
    pact_version = options.input_version

    pact_upload_url, pact_file_json = generate_pact_path_url(broker, pact_file, pact_version)
    basic_auth = HTTPBasicAuth("pactbroker", "pactbroker")
    if pact_file is not None and pact_file_json is not None:
        try:
            res = requests.put(pact_upload_url, auth=basic_auth, json=pact_file_json)
            if res.status_code == 200:
                print("Update Success!!! Message: %s" % res.json())
            elif res.status_code == 201:
                print("Upload Success!!! Message: %s" % res.json())
            else:
                print("Upload pact file fail!!! Status Code: %s, Message: %s" % (res.status_code, res.json()))
        except Exception as e:
            print("Please check the pact-broker server")
            print(e)
    else:
        print("Please check pact-broker path or pact file")


def generate_pact_path_url(broker, pact_file, pact_version):
    if os.path.isfile(pact_file):
        with open(pact_file, 'rb') as pact_file:
            pact_file_json = json.load(pact_file)

        consumer = pact_file_json['consumer']['name']
        provider = pact_file_json['provider']['name']
        pact_upload_url = "{base_url}/pacts/provider/{provider}/consumer/{consumer}/version/{version}".format(
            base_url=broker.strip("/"), provider=provider, consumer=consumer, version=pact_version)
        return pact_upload_url, pact_file_json
    else:
        return None, None


if __name__ == '__main__':
    main()
