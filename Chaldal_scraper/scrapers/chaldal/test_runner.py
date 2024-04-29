from test_oop import *

handler = PageHandler()
get_url = UrlManager()
get_data = DataRetriever(handler=handler,get_url=get_url)
main = Main(handler=handler, get_url=get_url, get_data=get_data)
main.executor()