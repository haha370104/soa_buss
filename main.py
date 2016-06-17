# coding=utf8
import soaplib
from soaplib.core.model.clazz import Array
from soaplib.core.model.primitive import String, Integer, Float, AnyAsDict, Any
from soaplib.core.server import wsgi
from soaplib.core.service import DefinitionBase, soap
import requests
import json
import backpack

server_url = 'http://115.28.206.58:8080'


class buss_api(DefinitionBase):
    @soap(String, Integer, _returns=Array(String))
    def say_hello(self, name, times):
        results = []
        for i in range(0, times):
            results.append('Hello, %s' % name)
        return results

    @soap(Float, Integer, String, String, _returns=String)
    def get_best_plan(self, money, days, bank, curr):
        # bank = json.dumps(bank)
        curr = curr.encode('utf-8')
        req = requests.get(
            '{0}/bank/get_list_by_duration/{1}/{2}/{3}/{4}/'.format(server_url, bank, str(days), curr, str(money)))
        products = json.loads(req.text)
        bank_name = {1: '中国工商银行', 2: '中国农业银行', 3: '中国建设银行', 4: '交通银行'}
        f = open('config.json')
        dic = json.load(f)
        n = []
        c = []
        w = []
        for product in products:
            if product['duration_flag']:
                n.append(1)
            else:
                n.append(days / (product['duration'] + dic['billing_time'][product['bank_name']]))
            c.append(product['duration'] + dic['billing_time'][product['bank_name']])
            w.append(round(product['rate'] * money * c[-1] / 36500, 2))
        # 这里直接进一个背包问题解答案
        save = backpack.solve(n, c, w, len(n), days)
        ns = backpack.parse(save, c, w)
        result = []
        # 接下来部分变量被修改了---------主要是我不知道怎么取名字了……
        for i in xrange(len(ns)):
            if ns[i] != 0:
                product = {'bank_name': products[i]['bank_name'], 'ID': products[i]['ID'], 'url': products[i]['url'],
                           'day': (ns[i] * c[i]),'product_name':products[i]['product_name']}
                result.append(product)
        result = {'plan_details': result, 'income': save[-1][-1]}
        return json.dumps(result)


if __name__ == '__main__':
    try:
        from wsgiref.simple_server import make_server

        soap_application = soaplib.core.Application([buss_api], 'tns')
        wsgi_application = wsgi.Application(soap_application)
        server = make_server('0.0.0.0', 7789, wsgi_application)
        server.serve_forever()
    except ImportError:
        print("Error: example server code requires Python >= 2.5")
