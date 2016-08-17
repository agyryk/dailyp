from django.shortcuts import render
from django import forms
import models
import db_fake
from settings import DailypSettings
from bigtree import BigTree
import db_cbs


class FormBuildsSelector(forms.Form):
    def __init__(self, *args, **kwargs):
        builds_choices = self.get_build_choices()
        baseline_build_selected = kwargs.pop('baseline_build_selected', None)
        active_build_selected = kwargs.pop('active_build_selected', None)
        super(FormBuildsSelector, self).__init__(*args, **kwargs)
        self.fields['Baseline Build'] = forms.TypedChoiceField(choices=builds_choices, initial = baseline_build_selected)
        self.fields['Active Build'] = forms.TypedChoiceField(choices=builds_choices, initial = active_build_selected)
    def get_build_choices(self):
        builds = db_fake.FakeDB().get_all_builds()
        build_choices = []
        for value in builds:
            build_tuple = (value,value)
            build_choices.append(build_tuple)
        return build_choices


def homeView(request):
    settings = DailypSettings()
    home_model = models.HomeModel()
    fake_db = db_fake.FakeDB()
    home_model.builds = fake_db.get_all_builds()
    if request.method == 'POST':
        home_model.active_build =  request.POST.get('Active Build','')
        home_model.baseline_build = request.POST.get('Baseline Build','')
    else:
        home_model.active_build = sorted(home_model.builds)[len(home_model.builds)-1]
        home_model.baseline_build = fake_db.default_baseline_build

    buildSelectorForm = FormBuildsSelector(baseline_build_selected=home_model.baseline_build,
                                           active_build_selected=home_model.active_build)
    bigtree = BigTree(home_model.active_build,home_model.baseline_build)
    home_model.debug_message = str(len(home_model.summary))
    for category_node in bigtree.root:
        home_model.summary.append({'name':category_node.name, 'status':category_node.status})

    cbs = db_cbs.CBS()
    if cbs.connect():
        home_model.debug_message = cbs.get_all_builds()
    return render(request, "dashboard.html", {"model": home_model, "form_buildsSelector":buildSelectorForm})


def categoryView(request):
    settings = DailypSettings()
    cat_model = models.CategoryModel()
    fake_db = db_fake.FakeDB()
    cat_model.builds = fake_db.get_all_builds()
    cat_model.category_name = request.GET['category']
    cat_model.active_build = request.GET['a']
    cat_model.baseline_build = request.GET['b']
    buildSelectorForm = FormBuildsSelector(baseline_build_selected=cat_model.baseline_build,
                                           active_build_selected=cat_model.active_build)
    bigtree = BigTree(cat_model.active_build, cat_model.baseline_build)
    for category in bigtree.root:
        if category.name == cat_model.category_name:
            for test in category.child_tests:
                cat_model.summary.append({'name':test.name, 'title': test.title, 'status':test.status})
    return render(request, "category_details.html", {"model": cat_model, "form_buildsSelector": buildSelectorForm})


def testView(request):
    settings = DailypSettings()
    test_model = models.CategoryModel()
    fake_db = db_fake.FakeDB()
    test_model.builds = fake_db.get_all_builds()
    test_model.category_name = request.GET['category']
    test_model.test_name = request.GET['test']
    test_model.active_build = request.GET['a']
    test_model.baseline_build = request.GET['b']
    buildSelectorForm = FormBuildsSelector(baseline_build_selected=test_model.baseline_build,
                                           active_build_selected=test_model.active_build)
    bigtree = BigTree(test_model.active_build, test_model.baseline_build)
    for category in bigtree.root:
        if category.name == test_model.category_name:
            for test in category.child_tests:
                if test.name == test_model.test_name:
                    test_model.test_title = test.title
                    for metric in test.child_metrics:
                        test_model.summary.append({'name':metric.name, 'description': metric.description,
                                                   'status':metric.status, "baseline": metric.b_value,
                                                   "current": metric.a_value})
    return render(request, "test_details.html", {"model": test_model, "form_buildsSelector": buildSelectorForm})