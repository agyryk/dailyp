from couchbase import Couchbase
from couchbase.bucket import Bucket
from pytz import timezone
import datetime
import json
import time


class CBS():
    def __init__(self):
        #self.bucket = ""
        self.bucket = Bucket('couchbase://cbmonitor.sc.couchbase.com/perf_daily')
        return

    def connect(self):
        try:
            self.bucket = Bucket('couchbase://cbmonitor.sc.couchbase.com/perf_daily')
        except:
            return False
        return True

    def get_all_builds(self):
        ret = []
        for row in self.bucket.n1ql_query("select `build` from perf_daily"):
            ret.append(row['build'].encode('utf8'))
        return ret

    def query_tester(self):
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
        json_doc = json.dumps(doc)
        return json_doc


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
