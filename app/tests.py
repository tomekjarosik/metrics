import os
import app
import unittest
import filesystem_helper
import metrics_sender
from flask import json
import utils


class AppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.app.test_client()

    def setUp(self):
        self.app_context = app.app.app_context()
        self.app_context.push()
        self.metricsender = metrics_sender.MetricSender()

    def tearDown(self):
        self.app_context.pop()

    def _post(self, a_dict):
        response = self.client.post('/buildmetrics/api/v1.0/add',
            data=json.dumps(a_dict), content_type = 'application/json')
        return response

    def test_send_request_buildmetrics(self):
        request_data = self.metricsender.prepare_request_data("testuser", {"t1" : 0, "t2" : 180}, True, None, None)
        response = self._post(request_data)
        self.assertEquals(201, response.status_code)

    def test_get_list_of_all_metrics(self):
        response = self.client.get('/metrics')
        self.assertEquals(200, response.status_code)

    @unittest.skip("testing skipping")
    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'No entries here so far' in rv.data


class MetricSenderTests(unittest.TestCase):
    def setUp(self):
        self.metricsender = metrics_sender.MetricSender()

    def test_parse_build_times(self):
        results = self.metricsender.parse_build_times("tests/build.times.in")
        self.assertEquals(2, results[':app:buildInfoDebugLoader'])
        self.assertEquals(187, results[':app:preBuild'])
        self.assertEquals(0, results[':app:preDebugBuild'])
        self.assertEquals(625, results['total time'])

    def test_prepare_request_data(self):
        res = self.metricsender.prepare_request_data("testuser", {"t1" : 0, "t2" : 180}, True, None, None)
        res["username"] = "an user"
        res["scores"]["t2"] = 180
        res["is_success"] = True

    def test_send_request(self):
        r = self.metricsender.send_request("testuser", {"t1": 13, "t10": 14}, True, "some diff", "some env")
        self.assertEquals(200, r.status_code)


class FilesystemHelperTests(unittest.TestCase):
    def setUp(self):
        self.helper = filesystem_helper.FilesystemHelper()
        pass

    def tearDown(self):
        pass

    def test_files_modified_since(self):
        import datetime as dt, time
        names = ["_t1.txt", "_t2.txt"]
        root = "."
        f1 = open(names[0], "w")
        result = self.helper.files_modified_since(root, dt.datetime.now() - dt.timedelta(seconds=0.51))
        self.assertEquals(os.path.join(root, names[0]), result[0])
        self.assertEquals(1, result.__len__())
        time.sleep(0.25)
        f2 = open(names[1], "w")
        result = self.helper.files_modified_since(root, dt.datetime.now() - dt.timedelta(seconds=0.5))
        self.assertEquals(os.path.join(root, names[1]), result[1])
        self.assertEquals(2, result.__len__())

        time.sleep(0.35)
        result = self.helper.files_modified_since(root, dt.datetime.now() - dt.timedelta(seconds=0.5))
        self.assertEquals(os.path.join(root, names[1]), result[0])
        self.assertEquals(1, result.__len__())

        f1.close()
        f2.close()
        for name in names:
            os.remove(os.path.join(root, name))

    def test_git_status(self):
        res = self.helper.git_status()
        self.assertTrue(res.startswith("# On branch master"))


class PlatformInfoTest(unittest.TestCase):
    def setUp(self):
        from utils import PlatformInfo
        self.info = PlatformInfo().info()

    def test_platform_info(self):
        self.assertIsNotNone(self.info["machine"])
        self.assertIsNotNone(self.info["user"])

class CustomSorterTest(unittest.TestCase):
    def setUp(self):
        self.customsorter = utils.CustomSorter()
        pass

    def test_sort_scores(self):
        dict = {}
        for i in range(0, 10):
            dict["t"+str(i)] = i * (i % 3)
        actual = self.customsorter.sort_scores(dict, True)
        expected = [('t8', 16), ('t5', 10), ('t7',7), ('t4', 4), ('t2', 4), ('t1', 1), ('t9', 0), ('t6', 0), ('t3', 0), ('t0', 0)]
        self.assertEquals(expected, actual)

if __name__ == '__main__':
    unittest.main()
