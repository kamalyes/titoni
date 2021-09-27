```pycon
import pytest
from iutils.OkHttps import Httpx
from iutils.Processor import JsonPath

class TestLogin():

    def test_requests_001(self):
        headers = {"content-type": "application/json;charset=UTF-8"}
        url = "http://localhost:8005/api/login"
        _json = {"account": "Admin","password": "1235678"}
        reponse = Httpx.sendApi(method="post",url=url,headers=headers,json=_json)
        res_code = Httpx.getStatusCode(reponse)
        res_content = Httpx.getContent(reponse)
        assert res_code == 200
        assert JsonPath.find(res_content, "$.data.account")[0] == "Admin
        pytest.assume(JsonPath.find(res_content, "$.data.account")[0] == "Admin")

if __name__ == '__main__':
    pytest.main(["-s","TestLogin::test_request_001"])
```