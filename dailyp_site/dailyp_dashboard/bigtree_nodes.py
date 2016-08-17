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
    def __init__(self, name, title, build_marker, child_metrics, status='default'):
        super(TestNode, self).__init__(name,build_marker,status)
        self.title = title
        self.child_metrics = child_metrics


class MetricNode(BigTreeNode):
    def __init__(self,name,build_marker,value,description, larger_is_better, status="default"):
        super(MetricNode, self).__init__(name,build_marker,status)
        self.value = value
        self.description = description
        self.b_value = ""
        self.a_value = ""
        self.larger_is_better = larger_is_better


