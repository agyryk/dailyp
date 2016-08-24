class BigTreeNode(object):
    def __init__(self,name,build_marker,status):
        self.name = name
        self.build_marker = build_marker
        self.status = status


class CategoryNode(BigTreeNode):
    def __init__(self, name, build_marker,child_tests,status='default'):
        super(CategoryNode, self).__init__(name,build_marker,status)
        self.child_tests = child_tests


class TestNode(BigTreeNode):
    def __init__(self, name, title, build_marker, child_metrics, datetime, status='default'):
        super(TestNode, self).__init__(name,build_marker,status)
        self.title = title
        self.child_metrics = child_metrics
        self.baseline_snapshots = list()
        self.active_snapshots = list()
        self.datetime = datetime

    def set_stapshots(self, snapshots):
        if self.build_marker == "active":
            self.active_snapshots = snapshots
        elif self.build_marker == "baseline":
            self.baseline_snapshots = snapshots

class MetricNode(BigTreeNode):
    def __init__(self,name,build_marker,value,description, larger_is_better, threshold, status="default"):
        super(MetricNode, self).__init__(name,build_marker,status)
        self.value = value
        self.description = description
        self.b_value = ""
        self.a_value = ""
        self.larger_is_better = larger_is_better
        self.threshold = threshold

