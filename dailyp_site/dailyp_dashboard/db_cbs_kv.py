from couchbase.bucket import Bucket
from pytz import timezone
import datetime


class CBS:
    def __init__(self):
        self.bucket = object
        self.all_docs = list()
        self.default_baseline_build = '4.5.0-2601'
        return

    def connect(self):
        try:
            self.bucket = Bucket('couchbase://cbmonitor.sc.couchbase.com/perf_daily')
            docs = self.bucket.n1ql_query("select perf_daily from perf_daily")
            runs = list()
            for row in docs:
                self.all_docs.append(row["perf_daily"])
        except:
            return False
        return True

    def get_all_builds(self):
        builds = set()
        for doc in self.all_docs:
            build = doc["build"]
            builds.add(build)
        return sorted(builds)

    def get_cats_by_build(self, build_number):
        cats = set()
        for doc in self.all_docs:
            if doc["build"] == build_number:
                cats.add(doc["category"])
        return cats

    def get_tests_by_cat(self, build_number, category):
        all_tests = list()
        build_date_map = {}
        for doc in self.all_docs:
            if doc["build"] == build_number and doc["category"] == category:
                all_tests.append({"test_name": doc['test'].encode('utf8'),
                                  "test_title": doc['test_title'].encode('utf8'),
                                  "datetime": doc['datetime'].encode('utf8'),
                                  "build":build_number})

        for test in all_tests:
            t_key = "{}_{}".format(test["test_name"], build_number)
            if t_key in build_date_map:
                curr_date = datetime.datetime.strptime(build_date_map[t_key], "%Y_%m_%d-%H:%M")
                new_date = datetime.datetime.strptime(test["datetime"], "%Y_%m_%d-%H:%M")
                if curr_date < new_date:
                    build_date_map[t_key] = test["datetime"]
            else:
                build_date_map[t_key] = test["datetime"]

        recent_tests = list()
        for test in all_tests:
            t_key = "{}_{}".format(test["test_name"], build_number)
            t_val = test["datetime"]
            if t_val == build_date_map[t_key]:
                recent_tests.append(test)

        return recent_tests

    def get_snapshots_by_test(self, build_number, category, test, datetime):
        snapshots = list()
        for doc in self.all_docs:
            if doc["build"] == build_number and \
               doc["category"] == category and \
               doc["test"] == test and \
               doc["datetime"] == datetime:
                for snapshot in doc["snapshots"]:
                    snapshots.append(snapshot)
        return snapshots

    def get_metrics_by_test(self, build_number, category, test, datetime):
        metrics = list()
        for doc in self.all_docs:
            if doc["build"] == build_number and \
               doc["category"] == category and \
               doc["test"] == test and \
               doc["datetime"] == datetime:
                for metric in doc["metrics"]:
                    metrics.append({"metric_name": metric['name'].encode('utf8'), "metric_value": metric['value'],
                                   "metric_description": metric['description'].encode('utf8'),
                                   "metric_lisb": metric['larger_is_better'], "metric_threshold": metric['threshold']})
        return metrics

    def get_history_by_test(self, category, test):
        metrics_dict = list()
        for doc in self.all_docs:
            if doc["category"] == category and doc["test"] == test:
                t_build = doc["build"].encode('utf8')
                t_datetime = doc["datetime"].encode('utf8')
                metrics = doc["metrics"]
                for metric in metrics:
                    metrics_dict.append(
                        {"build": t_build, "datetime": t_datetime, "metric_name": metric["name"].encode('utf8'),
                         "metric_value": metric["value"],
                         "metric_description": metric["description"].encode('utf8')})

        metrics_map = {}
        for metric in metrics_dict:
            m_name = metric["metric_name"]
            if m_name not in metrics_map:
                metrics_map[m_name] = list()
            metrics_map[m_name].append(metric)
        return metrics_map