from couchbase import Couchbase
from couchbase.bucket import Bucket
from pytz import timezone
import datetime
import json
import time


class CBS():
    def __init__(self):
        self.bucket = ""
        return

    def connect(self):
        try:
            self.bucket = Bucket('couchbase://cbmonitor.sc.couchbase.com/perf_daily')
        except:
            return False
        return True

    def get_all_builds(self):
        result = []
        for row in self.bucket.n1ql_query("select `build` from perf_daily"):
            result.append(row['build'].encode('utf8'))
        return result

    def get_cats_by_build(self, build_number):
        result = []
        for row in self.bucket.n1ql_query("select category from perf_daily where `build`='" + build_number + "'"):
            result.append(row['category'].encode('utf8'))
        return set(result)

    def get_tests_by_cat(self, build_number, category):
        result = []
        for row in self.bucket.n1ql_query("select test, test_title from perf_daily where `build`='" + build_number
                                            + "' and category='" + category + "'"):
            result.append([row['test'].encode('utf8'), row['test_title'].encode('utf8')])
        return result

    def get_metrics_by_test(self, build_number, category, test):
        result = []
        for row in self.bucket.n1ql_query("select metrics from perf_daily where `build`='" + build_number
                                          + "' and category='" + category + "' and test='" + test + "'"):
            for metric in row['metrics']:
                result.append([metric['name'].encode('utf8'), metric['value'],
                               metric['description'].encode('utf8'), metric['larger_is_better']])
        return result

    # Debug message [{u'metrics': [{u'value': 256002, u'description': u'Throughput, Average, ops/sec', u'name': u'Throughput', u'larger_is_better': True}, {u'value': 123.02, u'description': u'95 percentile latency', u'name': u'Latency', u'larger_is_better': False}]}]

    #                     metrics.append([metric.name, metric.value, metric.description, metric.larger_is_better])

    def load_tmp_data(self):
        date_time_str = datetime.datetime.now(timezone('US/Pacific')).strftime("%Y_%m_%d-%H:%M")
        th_title = 'Throughput, Average, ops/sec'
        lat_title = '95 percentile latency'
        category = "n1ql"

        build = "4.1.1-0000"  #################################################################

        test = "n1ql_fdb_q2_stale_false"
        test_title = "Q2, Singleton Unique Lookup, 20M docs, GSI, stale=false"
        id = category + "__" + test + "__" + build + "__" + date_time_str
        doc = {'build': build, 'category': category, 'test': test, 'test_title': test_title, 'datetime': date_time_str,
               'metrics': [
                            {'name': 'Throughput', 'description':th_title,'larger_is_better': True,'value': 256002},
                            {'name': 'Latency', 'description': lat_title,'larger_is_better': False, 'value': 123.02}
                           ]
               }
        #json_doc = json.dumps(doc)
        self.bucket.upsert(id,doc)


        test = "n1ql_fdb_q2_stale_ok"
        test_title = "Q2, Singleton Unique Lookup, 20M docs, GSI, stale=ok"
        id = category + "__" + test + "__" + build + "__" + date_time_str
        doc = {'build': build, 'category': category, 'test': test, 'test_title': test_title, 'datetime': date_time_str,
               'metrics': [
                            {'name': 'Throughput', 'description':th_title,'larger_is_better': True,'value': 256002},
                            {'name': 'Latency', 'description': lat_title,'larger_is_better': False, 'value': 123.02}
                           ]
               }
        #json_doc = json.dumps(doc)
        self.bucket.upsert(id,doc)

        test = "n1ql_fdb_q3_stale_false"
        test_title = "Q3, Range Scan, 20M docs, GSI, stale=false"
        id = category + "__" + test + "__" + build + "__" + date_time_str
        doc = {'build': build, 'category': category, 'test': test, 'test_title': test_title, 'datetime': date_time_str,
               'metrics': [
                   {'name': 'Throughput', 'description': th_title, 'larger_is_better': True, 'value': 256002},
                   {'name': 'Latency', 'description': lat_title, 'larger_is_better': False, 'value': 123.02}
               ]
               }
        #json_doc = json.dumps(doc)
        self.bucket.upsert(id,doc)

        test = "n1ql_fdb_q3_stale_ok"
        test_title = "Q3, Range Scan, 20M docs, GSI, stale=ok"
        id = category + "__" + test + "__" + build + "__" + date_time_str
        doc = {'build': build, 'category': category, 'test': test, 'test_title': test_title, 'datetime': date_time_str,
               'metrics': [
                   {'name': 'Throughput', 'description': th_title, 'larger_is_better': True, 'value': 256002},
                   {'name': 'Latency', 'description': lat_title, 'larger_is_better': False, 'value': 123.02}
               ]
               }
        #json_doc = json.dumps(doc)
        self.bucket.upsert(id,doc)





        build = "4.2.1-1234"  #################################################################

        test = "n1ql_fdb_q2_stale_false"
        test_title = "Q2, Singleton Unique Lookup, 20M docs, GSI, stale=false"
        id = category + "__" + test + "__" + build + "__" + date_time_str
        doc = {'build': build, 'category': category, 'test': test, 'test_title': test_title, 'datetime': date_time_str,
               'metrics': [
                            {'name': 'Throughput', 'description':th_title,'larger_is_better': True,'value': 256002},
                            {'name': 'Latency', 'description': lat_title,'larger_is_better': False, 'value': 123.02}
                           ]
               }
        #json_doc = json.dumps(doc)
        self.bucket.upsert(id,doc)


        test = "n1ql_fdb_q2_stale_ok"
        test_title = "Q2, Singleton Unique Lookup, 20M docs, GSI, stale=ok"
        id = category + "__" + test + "__" + build + "__" + date_time_str
        doc = {'build': build, 'category': category, 'test': test, 'test_title': test_title, 'datetime': date_time_str,
               'metrics': [
                            {'name': 'Throughput', 'description':th_title,'larger_is_better': True,'value': 256002},
                            {'name': 'Latency', 'description': lat_title,'larger_is_better': False, 'value': 123.02}
                           ]
               }
        #json_doc = json.dumps(doc)
        self.bucket.upsert(id,doc)

        test = "n1ql_fdb_q3_stale_false"
        test_title = "Q3, Range Scan, 20M docs, GSI, stale=false"
        id = category + "__" + test + "__" + build + "__" + date_time_str
        doc = {'build': build, 'category': category, 'test': test, 'test_title': test_title, 'datetime': date_time_str,
               'metrics': [
                   {'name': 'Throughput', 'description': th_title, 'larger_is_better': True, 'value': 256002},
                   {'name': 'Latency', 'description': lat_title, 'larger_is_better': False, 'value': 123.02}
               ]
               }
        #json_doc = json.dumps(doc)
        self.bucket.upsert(id,doc)

        test = "n1ql_fdb_q3_stale_ok"
        test_title = "Q3, Range Scan, 20M docs, GSI, stale=ok"
        id = category + "__" + test + "__" + build + "__" + date_time_str
        doc = {'build': build, 'category': category, 'test': test, 'test_title': test_title, 'datetime': date_time_str,
               'metrics': [
                   {'name': 'Throughput', 'description': th_title, 'larger_is_better': True, 'value': 256002},
                   {'name': 'Latency', 'description': lat_title, 'larger_is_better': False, 'value': 123.02}
               ]
               }
        #json_doc = json.dumps(doc)
        self.bucket.upsert(id,doc)



        build = "4.3.2-9876"  #################################################################

        test = "n1ql_fdb_q2_stale_false"
        test_title = "Q2, Singleton Unique Lookup, 20M docs, GSI, stale=false"
        id = category + "__" + test + "__" + build + "__" + date_time_str
        doc = {'build': build, 'category': category, 'test': test, 'test_title': test_title, 'datetime': date_time_str,
               'metrics': [
                            {'name': 'Throughput', 'description':th_title,'larger_is_better': True,'value': 256002},
                            {'name': 'Latency', 'description': lat_title,'larger_is_better': False, 'value': 123.02}
                           ]
               }
        #json_doc = json.dumps(doc)
        self.bucket.upsert(id,doc)


        test = "n1ql_fdb_q2_stale_ok"
        test_title = "Q2, Singleton Unique Lookup, 20M docs, GSI, stale=ok"
        id = category + "__" + test + "__" + build + "__" + date_time_str
        doc = {'build': build, 'category': category, 'test': test, 'test_title': test_title, 'datetime': date_time_str,
               'metrics': [
                            {'name': 'Throughput', 'description':th_title,'larger_is_better': True,'value': 56002},
                            {'name': 'Latency', 'description': lat_title,'larger_is_better': False, 'value': 5432.02}
                           ]
               }
        #json_doc = json.dumps(doc)
        self.bucket.upsert(id,doc)

        test = "n1ql_fdb_q3_stale_false"
        test_title = "Q3, Range Scan, 20M docs, GSI, stale=false"
        id = category + "__" + test + "__" + build + "__" + date_time_str
        doc = {'build': build, 'category': category, 'test': test, 'test_title': test_title, 'datetime': date_time_str,
               'metrics': [
                   {'name': 'Throughput', 'description': th_title, 'larger_is_better': True, 'value': 256002},
                   {'name': 'Latency', 'description': lat_title, 'larger_is_better': False, 'value': 123.02}
               ]
               }
        #json_doc = json.dumps(doc)
        self.bucket.upsert(id,doc)

        test = "n1ql_fdb_q3_stale_ok"
        test_title = "Q3, Range Scan, 20M docs, GSI, stale=ok"
        id = category + "__" + test + "__" + build + "__" + date_time_str
        doc = {'build': build, 'category': category, 'test': test, 'test_title': test_title, 'datetime': date_time_str,
               'metrics': [
                   {'name': 'Throughput', 'description': th_title, 'larger_is_better': True, 'value': 256002},
                   {'name': 'Latency', 'description': lat_title, 'larger_is_better': False, 'value': 687.02}
               ]
               }
        #json_doc = json.dumps(doc)
        self.bucket.upsert(id,doc)
