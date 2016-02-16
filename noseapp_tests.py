import noseapp
import requests
from noseapp import TestCase
from time import strftime

hostport = 'http://127.0.0.1:5000'
suite = noseapp.Suite('first_suite')


@suite.register
class BaseFuncTestsForFirstBeginServer(noseapp.ScreenPlayCase):

    def begin(self):
        pass

    @noseapp.step(1, 'first step - start server')
    def step_one(self):
        req = requests.request('GET',  hostport + '/')
        self.assertEquals(req.content, '{"hello": "Hello World!", "name": "My name is Flask Server"}')

    @noseapp.step(2, 'new key: value')
    def step_two(self):
        requests.post(hostport + '/dictionary', data='{"key": "mail.ru", "value": "target"}')
        req = requests.request('GET', hostport + '/')
        self.assertEquals(req.content, '{"mail.ru": "target", "hello": "Hello World!", "name": "My name is Flask Server"}')

    @noseapp.step(3, 'put')
    def step_three(self):
        requests.put(hostport + '/dictionary/mail.ru', data='{"key": "mail.ru", "value": "new_target"}')
        req = requests.request('GET', hostport +  '/')
        self.assertEquals(req.content, '{"mail.ru": "new_target", "hello": "Hello World!", "name": "My name is Flask Server"}')

    @noseapp.step(4, 'Delete')
    def step_four(self):
        requests.delete(hostport + '/dictionary/mail.ru')
        req = requests.request('GET', hostport + '/')
        self.assertEquals(req.content, '{"hello": "Hello World!", "name": "My name is Flask Server"}')

    def finalize(self):
        pass



@suite.register
class TestCaseForWrongPost(TestCase):

    def test_old_key(self):
        res = requests.post(hostport + '/dictionary', data='{"key": "name", "value": "target"}')
        status = res.status_code
        self.assertEquals(status, 409)

    def test_wrong_json(self):
        res = requests.post(hostport + '/dictionary', data='{"wrongkey": "name", "value": "target"}')
        status = res.status_code
        self.assertEquals(status, 400)



@suite.register
class TestCaseForWrongPut(TestCase):

    def test_wrong_json(self):
        res = requests.put(hostport + '/dictionary/name', data='{"key": "name", "wrongvalue": "target"}')
        status = res.status_code
        self.assertEquals(status, 400)

    def test_new_key(self):
        res = requests.put(hostport + '/dictionary/new_new_name', data='{"key": "new_new_name", "value": "target"}')
        status = res.status_code
        self.assertEquals(status, 404)



@suite.register
def test_get_empty_key(case):
    req = requests.get(hostport + '/dictionary/empty_key')
    status = req.status_code
    case.assertEquals(status, 404)


@suite.register
def test_wrong_delete(case):
    res = requests.delete(hostport + '/dictionary/empty_key')
    status = res.status_code
    case.assertEquals(status, 200)


@suite.register
def test_correct_time_server(case):
    result = False
    res = requests.get(hostport + '/dictionary/name')
    body = res.content
    current_time = strftime("%Y-%m-%d %H:%M")
    bigger_curent_time  = current_time[0:-2] + str(int(current_time[-1]) + 1)
    if body.endswith(current_time + '"}') or body.endswith(bigger_curent_time + '"}'):
        result = True
    case.assertTrue(result)



app = noseapp.NoseApp('http_testing')
app.register_suite(suite)

app.run()