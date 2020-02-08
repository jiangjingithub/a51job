import requests
# from a51job.get_item import getProxy

# class RandomProxy():
#
#     def process_request(self, request, spider):
#         mayi_proxy = getProxy()[1]
#         authHeader = getProxy()[0]
#         proxies = {"http": mayi_proxy, "https": mayi_proxy, }
#         request.meta["proxy"] = proxies
#
#     def process_response(self, request, response, spider):
#         '''对返回的response处理'''
#         # 如果返回的response状态不是200，重新生成当前request对象
#         print('状态码: %s' % response.status)
#         if response.status != 200:
#             mayi_proxy = getProxy()[1]
#             authHeader = getProxy()[0]
#             proxies = {"http": mayi_proxy, "https": mayi_proxy, }
#             request.meta["proxy"] = proxies
#             return request
#         return response

from .tool.bloomfulter import BloomFilter

class A51jobDownloaderMiddleware(object):
    def __init__(self):
        self.bf = BloomFilter()

    def process_request(self,request,spider):
        if "search.51job.com" in request.url:
            if self.bf.isContains(request.url):
                print("此链接%s已爬取，不在爬取！" % request.url)
        else:
            return None

    def process_response(self, request, response, spider):
        if response.status == 200 and "search.51job.com" in response.url:
            self.bf.insert(response.url)
        return response
