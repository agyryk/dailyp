import bigtree_nodes
import logger



class BigTree():
    STATUS_INCOMPLETE = "incomplete"
    STATUS_DEFAULT = 'default'
    STATUS_PASSED = "PASSED"
    STATUS_FAILED = "FAILED"

    def __init__(self, cbs, a_build, b_build):
        self.a_tree = self.load_from_build(cbs, a_build, "active")
        self.b_tree = self.load_from_build(cbs, b_build, "baseline")
        self.root = []
        self.merge_tree()

    def load_from_build(self,cbs, build,marker):
        tree = []
        categories = cbs.get_cats_by_build(build)
        for category in categories:
            category_node = bigtree_nodes.CategoryNode(category, marker, [])
            tests = cbs.get_tests_by_cat(build,category)
            for test in tests:
                test_node = bigtree_nodes.TestNode(name=test["test_name"],
                                                   title=test["test_title"],
                                                   build_marker=marker,
                                                   child_metrics=[])
                test_node.set_datetime(test["datetime"])
                test_node.set_stapshots(cbs.get_snapshots_by_test(build,category,test_node.name, test["datetime"]))
                metrics = cbs.get_metrics_by_test(build,category,test_node.name, test["datetime"])
                for metric in metrics:
                    metric_node = bigtree_nodes.MetricNode(name=metric["metric_name"],
                                                           build_marker=marker,
                                                           value=metric["metric_value"],
                                                           description=metric["metric_description"],
                                                           larger_is_better=metric["metric_lisb"],
                                                           threshold=metric["metric_threshold"])
                    test_node.child_metrics.append(metric_node)
                category_node.child_tests.append(test_node)
            tree.append(category_node)
        return tree

    def merge_tree(self):
        # merge by layer
        metrics_map = {}
        tests_map = {}
        cat_map = {}
        for category in self.b_tree:
            category.status = BigTree.STATUS_INCOMPLETE
            cat_map[category.name] = category
            for test in category.child_tests:
                t_keypath = category.name + test.name
                test.status = BigTree.STATUS_INCOMPLETE
                tests_map[t_keypath] = test
                for metric in test.child_metrics:
                    m_keypath=category.name + test.name + metric.name
                    metric.status = BigTree.STATUS_INCOMPLETE
                    metric.b_value = metric.value
                    metrics_map[m_keypath] = metric
        for category in self.a_tree:
            if category.name in cat_map:
                merged_category = cat_map[category.name]
                merged_category.status = BigTree.STATUS_DEFAULT
            cat_map[category.name] = category
            for test in category.child_tests:
                t_keypath = category.name + test.name
                test.status = BigTree.STATUS_INCOMPLETE
                if t_keypath in tests_map:
                    merged_test = tests_map[t_keypath]
                    merged_test.status = BigTree.STATUS_DEFAULT
                    merged_test.active_snapshots = test.active_snapshots
                    merged_test.active_datetime = test.active_datetime
                    tests_map[t_keypath] = merged_test
                else:
                    tests_map[t_keypath] = test
                for metric in test.child_metrics:
                    m_keypath = category.name + test.name + metric.name
                    metric.status = BigTree.STATUS_INCOMPLETE
                    metric.a_value = metric.value
                    if m_keypath not in metrics_map:
                        metrics_map[m_keypath] = metric
                    else:
                        merged_metric = metrics_map[m_keypath]
                        merged_metric.a_value = metric.a_value
                        if self._check_metric_condition(merged_metric.larger_is_better, merged_metric.a_value,
                                                        merged_metric.b_value, merged_metric.threshold):
                            merged_metric.status = BigTree.STATUS_PASSED
                        else:
                            merged_metric.status = BigTree.STATUS_FAILED
                        metrics_map[m_keypath] = merged_metric

        # relink layer maps back to tree
        self.root = []
        for t_keypath in tests_map:
            test = tests_map[t_keypath]
            test.child_metrics = []
            for m_keypath in metrics_map:
                if m_keypath == (t_keypath + metrics_map[m_keypath].name):
                    test.child_metrics.append(metrics_map[m_keypath])
            if test.status != BigTree.STATUS_INCOMPLETE:
                test.status = BigTree.STATUS_PASSED
                for metric in test.child_metrics:
                    if metric.status == BigTree.STATUS_FAILED:
                        test.status = BigTree.STATUS_FAILED
                        break
            tests_map[t_keypath] = test
        for c_keypath in cat_map:
            category = cat_map[c_keypath]
            category.child_tests = []
            for t_keypath in tests_map:
                if t_keypath == (c_keypath + tests_map[t_keypath].name):
                    category.child_tests.append(tests_map[t_keypath])
            category.status = BigTree.STATUS_PASSED
            for test in category.child_tests:
                if test.status == BigTree.STATUS_INCOMPLETE:
                    category.status = BigTree.STATUS_INCOMPLETE
                    break
            if category.status != BigTree.STATUS_INCOMPLETE:
                for test in category.child_tests:
                    if test.status == BigTree.STATUS_FAILED:
                        category.status = BigTree.STATUS_FAILED
                        break
            self.root.append(category)

    def _check_metric_condition(self, lisb, a_value, b_value, threshold):
        b_value = float(b_value)
        a_value = float(a_value)
        if a_value == b_value:
            return True
        if lisb:
            if a_value < b_value:
                if abs(((b_value-a_value)/b_value)*100) > threshold:
                    return False
        if not lisb:
            if b_value < a_value:
                if abs(((a_value-b_value)/a_value)*100) > threshold:
                    return False
        return True













