from couchbase.bucket import Bucket
from pytz import timezone
import datetime


class CBS:
    def __init__(self):
        self.bucket = object
        self.default_baseline_build = '4.5.0-2601'
        return

    def connect(self):
        try:
            self.bucket = Bucket('couchbase://cbmonitor.sc.couchbase.com/perf_daily')
        except:
            return False
        return True

    def get_all_builds(self):
        result = []
        builds = self.bucket.n1ql_query("select distinct `build` from perf_daily where meta().id is not missing")
        for row in builds:
            result.append(row['build'].encode('utf8'))
        return result

    def get_cats_by_build(self, build_number):
        result = []
        for row in self.bucket.n1ql_query("select distinct category from perf_daily where `build`='" + build_number
                                          + "'"):
            result.append(row['category'].encode('utf8'))
        return result

    def get_tests_by_cat(self, build_number, category):
        result = []
        for row in self.bucket.n1ql_query("select test, test_title, max(datetime) from perf_daily where `build`='"
                                          + build_number + "' and category='" + category
                                          + "' group by test, test_title"):
            result.append({"test_name": row['test'].encode('utf8'), "test_title": row['test_title'].encode('utf8'),
                           "datetime": row['$1'].encode('utf8')})
        return result

    def get_snapshots_by_test(self, build_number, category, test, datetime):
        result = []
        for row in self.bucket.n1ql_query("select snapshots from perf_daily where `build`='" + build_number
                                          + "' and category='" + category + "' and test='" + test
                                          + "' and datetime='" + datetime + "'"):
            for snapshot in row['snapshots']:
                result.append(snapshot.encode('utf8'))
        return result

    def get_metrics_by_test(self, build_number, category, test, datetime):
        result = []
        for row in self.bucket.n1ql_query("select metrics from perf_daily where `build`='" + build_number
                                          + "' and category='" + category + "' and test='" + test
                                          + "' and datetime='" + datetime + "'"):
            for metric in row['metrics']:
                result.append({"metric_name": metric['name'].encode('utf8'),"metric_value": metric['value'],
                               "metric_description": metric['description'].encode('utf8'),
                               "metric_lisb": metric['larger_is_better'], "metric_threshold": metric['threshold']})
        return result

    def post_run(self,test_run_dict):
        id = test_run_dict['category'] + "__" + test_run_dict['test'] + "__" + test_run_dict['build'] + "__" \
                + test_run_dict['datetime']
        self.bucket.upsert(id,test_run_dict)

    def get_history_by_test(self, category, test):
        metrics_dict = list()
        for row in self.bucket.n1ql_query("select `build`, datetime, metrics from perf_daily where category='" +
                                          category + "' and test='" + test + "' order by `build`" ):
            t_build = row["build"].encode('utf8')
            t_datetime = row["datetime"].encode('utf8')
            metrics = row["metrics"]
            for metric in metrics:
                metrics_dict.append({"build": t_build, "datetime": t_datetime, "metric_name": metric["name"].encode('utf8'),
                                     "metric_value": metric["value"],
                                     "metric_description": metric["description"].encode('utf8')})
        metrics_map = {}
        for metric in metrics_dict:
            m_name = metric["metric_name"]
            if m_name not in metrics_map:
                metrics_map[m_name] = list()
            metrics_map[m_name].append(metric)
        return metrics_map
