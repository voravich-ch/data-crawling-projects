# Adjustment on the middlewares provided by https://github.com/TeamHG-Memex/scrapy-rotating-proxies

1) Create a custom ban policy: `banPolicy.py`; the script is as follows:

```python
from rotating_proxies.policy import BanDetectionPolicy

class MyPolicy(BanDetectionPolicy):
    def response_is_ban(self, request, response):
        # use default rules, but also consider HTTP 200 responses
        # a ban if there is 'captcha' word in response body.
        ban = super(MyPolicy, self).response_is_ban(request, response)
        if response.status == 404:
            ban = False
        ban = ban or b'captcha' in response.body
        return ban

    def exception_is_ban(self, request, exception):
        # override method completely: don't take exceptions in account
        return None
```

2) Download python scripts in this [folder](https://github.com/TeamHG-Memex/scrapy-rotating-proxies/tree/master/rotating_proxies) including: `expire.py`, `middleware.py`, and `utils.py`; `middleware.py` was renamed to `rotatingProxies.py` to avoid confusion.

3) Adjust code in `rotatingProxies.py` by adding the following code to `_retry` module before assigning new request (`retryreq`):

```python
# Parse request for musixmatch
if 'verify-user' in request.url:
    new_url = request.url.replace(r'verify-user?redirect=%2F', '').replace(r'%2F', '/')
    request = request.replace(url=new_url)
# Done parsing
```
