class TestRun():
    def __init__(self, build='default',category='default',test='default', test_title="default", metrics=[]):
        self.build = build
        self.category = category
        self.test = test
        self.metrics = metrics
        self.test_title = test_title


class Metric():
    def __init__(self, name, value, description, larger_is_better):
        self.name=name
        self.value=value
        self.description=description
        self.larger_is_better = larger_is_better



class FakeDB():
    def __init__(self):
        self.test_runs = []
        self.default_baseline_build = '4.1.1-0000'

        #build
        self.test_runs.append(TestRun(build="4.1.1-0000",category='n1ql',test='n1ql_fdb_q2_stale_false',
                                      test_title='FDB,Q2, stale_false',
                                      metrics=[Metric('Throughput',256002,'Throughput, Average, ops/sec',True),
                                               Metric('Latency',123.02,'95 percentile latency',False)]))

        self.test_runs.append(TestRun(build="4.1.1-0000", category='n1ql', test='n1ql_fdb_q2_stale_ok',
                                      test_title='FDB,Q2, stale_ok',
                                      metrics=[Metric('Throughput', 256002, 'Throughput, Average, ops/sec',True),
                                               Metric('Latency', 123.02, '95 percentile latency',False)]))

        self.test_runs.append(TestRun(build="4.1.1-0000", category='n1ql', test='n1ql_fdb_q3_stale_false',
                                      test_title='FDB,Q3, stale_false',
                                      metrics=[Metric('Throughput', 256003, 'Throughput, Average, ops/sec',True),
                                               Metric('Latency', 123.03, '95 percentile latency',False)]))

        self.test_runs.append(TestRun(build="4.1.1-0000", category='n1ql', test='n1ql_fdb_q3_stale_ok',
                                      test_title='FDB,Q3, stale_ok',
                                      metrics=[Metric('Throughput', 256003, 'Throughput, Average, ops/sec',True),
                                               Metric('Latency', 123.03, '95 percentile latency',False)]))

        #build
        self.test_runs.append(TestRun(build="4.2.0-2601", category='n1ql', test='n1ql_fdb_q2_stale_false',
                                      test_title='FDB,Q2, stale_false',
                                      metrics=[Metric('Throughput', 120002, 'Throughput, Average, ops/sec',True),
                                               Metric('Latency', 123.02, '95 percentile latency',False)]))

        self.test_runs.append(TestRun(build="4.2.0-2601", category='n1ql', test='n1ql_fdb_q2_stale_ok',
                                      test_title='FDB,Q2, stale_ok',
                                      metrics=[Metric('Throughput', 256002, 'Throughput, Average, ops/sec',True),
                                               Metric('Latency', 123.02, '95 percentile latency',False)]))

        self.test_runs.append(TestRun(build="4.2.0-2601", category='n1ql', test='n1ql_fdb_q3_stale_false',
                                      test_title='FDB,Q3, stale_false',
                                      metrics=[Metric('Throughput', 256003, 'Throughput, Average, ops/sec',True),
                                               Metric('Latency', 5238.03, '95 percentile latency',False)]))

        self.test_runs.append(TestRun(build="4.2.0-2601", category='n1ql', test='n1ql_fdb_q3_stale_ok',
                                      test_title='FDB,Q3, stale_ok',
                                      metrics=[Metric('Throughput', 300, 'Throughput, Average, ops/sec',True),
                                               Metric('Latency', 523.03, '95 percentile latency',False)]))


        #build
        self.test_runs.append(TestRun(build="4.4.0-3050", category='n1ql', test='n1ql_fdb_q2_stale_false',
                                      test_title='FDB,Q2, stale_false',
                                      metrics=[Metric('Throughput', 256002, 'Throughput, Average, ops/sec',True),
                                               Metric('Latency', 123.02, '95 percentile latency',False)]))

        self.test_runs.append(TestRun(build="4.4.0-3050", category='n1ql', test='n1ql_fdb_q2_stale_ok',
                                      test_title='FDB,Q2, stale_ok',
                                      metrics=[Metric('Throughput', 256002, 'Throughput, Average, ops/sec',True),
                                               Metric('Latency', 123.02, '95 percentile latency',False)]))

        self.test_runs.append(TestRun(build="4.4.0-3050", category='n1ql', test='n1ql_fdb_q3_stale_false',
                                      test_title='FDB,Q3, stale_false',
                                      metrics=[Metric('Throughput', 256003, 'Throughput, Average, ops/sec',True),
                                               Metric('Latency', 123.03, '95 percentile latency',False)]))
        self.test_runs.append(TestRun(build="4.4.0-3050", category='n1ql', test='n1ql_fdb_q3_stale_ok',
                                      test_title='FDB,Q3, stale_ok',
                                      metrics=[Metric('Throughput', 256003, 'Throughput, Average, ops/sec',True),
                                               Metric('Latency', 123.03, '95 percentile latency',False)]))

    def get_all_builds(self):
        builds = []
        for test_run in self.test_runs:
            builds.append(test_run.build)
        return set(builds)

    def get_cats(self,build):
        cats = []
        for run in self.test_runs:
            if run.build == build:
                cats.append(run.category)
        return set(cats)

    def get_tests_by_cat(self,build,cat):
        tests = []
        for run in self.test_runs:
            if run.build == build and run.category == cat:
                tests.append([run.test, run.test_title])
        return tests

    def get_metrics_by_test(self,build, cat, test):
        metrics = []
        for run in self.test_runs:
            if run.build == build and run.category == cat and run.test == test:
                for metric in run.metrics:
                    metrics.append([metric.name, metric.value, metric.description, metric.larger_is_better])
        return metrics
















