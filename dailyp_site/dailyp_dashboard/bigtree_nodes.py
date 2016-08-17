class CategoryNode:
    def __init__(self, name, build_marker,child_tests,status='default'):
        self.name = name
        self.build_marker = build_marker
        self.status = status
        self.child_tests = child_tests


class TestNode:
    def __init__(self, name, title, build_marker, child_metrics, status='default'):
        self.name = name
        self.title = title
        self.build_marker = build_marker
        self.status = status
        self.child_metrics = child_metrics


class MetricNode:
    def __init__(self,name,build_marker,value,description, larger_is_better, status="default"):
        self.name = name
        self.build_marker = build_marker
        self.value = value
        self.description = description
        self.b_value=""
        self.a_value=""
        self.larger_is_better = larger_is_better
        self.status = status
