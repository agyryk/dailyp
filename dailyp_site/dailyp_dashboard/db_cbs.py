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

