import requests
# from a51job.get_item import getProxy
from .tool.bloomfulter import BloomFilter
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



class A51jobDownloaderMiddleware(object):

    def process_request(self,request,spider):
        bf = BloomFilter()
        print(request.url)
        if "search.51job.com" in request.url:
            if bf.isContains(request.url):
                print("此链接%s已爬取，不在爬取！" % request.url)
            else:
                bf.insert(request.url)
                return None
        else:
            return None