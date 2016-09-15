class HomeModel(object):
    def __init__(self):
        self.builds = []
        self.baseline_build = "default"
        self.active_build = "default"
        self.summary = []
        self.debug_message = ""


class ComposedModel(HomeModel):
    def __init__(self):
        super(HomeModel, self).__init__()
        self.category_name = "default"
        self.tests = list()


class HistoryModel(HomeModel):
    def __init__(self):
        super(HomeModel, self).__init__()
        self.category_name = "default"
        self.test_name = "default"
