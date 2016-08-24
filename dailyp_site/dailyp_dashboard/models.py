class HomeModel(object):
    def __init__(self):
        self.builds = []
        self.baseline_build = "default"
        self.active_build = "default"
        self.summary = []
        self.debug_message = ""



class CategoryModel(HomeModel):
    def __init__(self):
        super(CategoryModel, self).__init__()
        self.category_name = "default"


class TestModel(CategoryModel):
    def __init__(self):
        super(TestModel, self).__init__()
        self.test_name = "default"
        self.test_title = "default"
        self.test_datetime = ""


class ComposedModel(HomeModel):
    def __init__(self):
        super(HomeModel, self).__init__()
        self.category_name = "default"
        self.tests = list()
