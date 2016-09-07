from django.shortcuts import render
from django import forms
import models
from settings import DailypSettings
from bigtree import BigTree
from db_cbs_kv import CBS
from operator import itemgetter
import operator

class FormBuildsSelector(forms.Form):
    def __init__(self, *args, **kwargs):
        builds_choices = self.get_build_choices()
        baseline_build_selected = kwargs.pop('baseline_build_selected', None)
        active_build_selected = kwargs.pop('active_build_selected', None)
        super(FormBuildsSelector, self).__init__(*args, **kwargs)
        self.fields['Baseline Build'] = forms.TypedChoiceField(choices=builds_choices, initial = baseline_build_selected)
        self.fields['Active Build'] = forms.TypedChoiceField(choices=builds_choices, initial = active_build_selected)

    def get_build_choices(self):
        cbs = CBS()
        if cbs.connect():
            builds = cbs.get_all_builds()
            build_choices = []
            for value in builds:
                build_tuple = (value,value)
                build_choices.append(build_tuple)
        return build_choices


def homeView(request):
    settings = DailypSettings()
    home_model = models.HomeModel()
    cbs = CBS()
    if cbs.connect():
        home_model.builds = cbs.get_all_builds()
        if request.method == 'POST':
            home_model.active_build =  request.POST.get('Active Build','')
            home_model.baseline_build = request.POST.get('Baseline Build','')
        else:
            home_model.active_build = sorted(home_model.builds)[len(home_model.builds)-1]
            home_model.baseline_build = cbs.default_baseline_build

        buildSelectorForm = FormBuildsSelector(baseline_build_selected=home_model.baseline_build,
                                               active_build_selected=home_model.active_build)
        bigtree = BigTree(cbs, home_model.active_build, home_model.baseline_build)
        for category_node in bigtree.root:
            total, passed, failed, incomplete = 0,0,0,0
            for test_node in category_node.child_tests:
                total +=1
                if test_node.status == BigTree.STATUS_INCOMPLETE:
                    incomplete +=1
                elif test_node.status == BigTree.STATUS_PASSED:
                    passed +=1
                elif test_node.status == BigTree.STATUS_FAILED:
                    failed +=1
            home_model.summary.append({'name': category_node.name, 'status': category_node.status,
                                       'passed': passed, 'failed': failed, 'incomplete': incomplete, 'total': total})

            home_model.summary.sort(key=operator.itemgetter('name'), reverse=True)
        return render(request, "dashboard.html", {"model": home_model, "form_buildsSelector": buildSelectorForm})

    home_model.debug_message = "Error connecting CBS"
    return render(request, "dashboard.html", {"model": home_model})

def composedView(request):
    composed_model = models.ComposedModel()
    cbs = CBS()
    if cbs.connect():
        composed_model.builds = cbs.get_all_builds()
        composed_model.category_name = request.GET['category']
        composed_model.active_build = request.GET['a']
        composed_model.baseline_build = request.GET['b']
        buildSelectorForm = FormBuildsSelector(baseline_build_selected=composed_model.baseline_build,
                                               active_build_selected=composed_model.active_build)
        bigtree = BigTree(cbs,composed_model.active_build, composed_model.baseline_build)
        for category in bigtree.root:
            if category.name == composed_model.category_name:
                tests = list()
                for test in category.child_tests:
                    metrics = list ()
                    for metric in test.child_metrics:
                        metrics.append({'name': metric.name, 'description': metric.description,
                                        'status': metric.status, "baseline": metric.b_value,
                                        "current": metric.a_value, 'threshold': metric.threshold})
                    tests.append({'name': test.name, 'active_datetime': test.active_datetime,
                                  'baseline_datetime': test.baseline_datetime, 'title': test.title,
                                  'status': test.status, 'active_snapshots': test.active_snapshots,
                                  'baseline_snapshots': test.baseline_snapshots, 'metrics': metrics})
                composed_model.summary = tests
                composed_model.summary = sorted(composed_model.summary, key=itemgetter('title'))
        return render(request, "details.html",{"model": composed_model,
                                                        "form_buildsSelector": buildSelectorForm})

    composed_model.debug_message = "Error connecting CBS"
    return render(request, "dashboard.html", {"model": composed_model})


def categoryView(request):
    settings = DailypSettings()
    cat_model = models.CategoryModel()
    cbs = CBS()
    if cbs.connect():
        cat_model.builds = cbs.get_all_builds()
        cat_model.category_name = request.GET['category']
        cat_model.active_build = request.GET['a']
        cat_model.baseline_build = request.GET['b']
        buildSelectorForm = FormBuildsSelector(baseline_build_selected=cat_model.baseline_build,
                                               active_build_selected=cat_model.active_build)
        bigtree = BigTree(cbs,cat_model.active_build, cat_model.baseline_build)
        for category in bigtree.root:
            if category.name == cat_model.category_name:
                for test in category.child_tests:
                    cat_model.summary.append({'name':test.name, 'title': test.title, 'status':test.status})
        return render(request, "category_details.html", {"model": cat_model, "form_buildsSelector": buildSelectorForm})

    cat_model.debug_message = "Error connecting CBS"
    return render(request, "dashboard.html", {"model": cat_model})


def testView(request):
    settings = DailypSettings()
    test_model = models.CategoryModel()
    cbs = CBS()
    if cbs.connect():
        test_model.builds = cbs.get_all_builds()
        test_model.category_name = request.GET['category']
        test_model.test_name = request.GET['test']
        test_model.active_build = request.GET['a']
        test_model.baseline_build = request.GET['b']
        buildSelectorForm = FormBuildsSelector(baseline_build_selected=test_model.baseline_build,
                                               active_build_selected=test_model.active_build)
        bigtree = BigTree(cbs,test_model.active_build, test_model.baseline_build)
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

    test_model.debug_message = "Error connecting CBS"
    return render(request, "dashboard.html", {"model": test_model})


def historyView(request):
    settings = DailypSettings()
    history_model = models.HistoryModel()
    cbs = CBS()
    if cbs.connect():
        history_model.builds = cbs.get_all_builds()
        history_model.category_name = request.GET['category']
        history_model.test_name = request.GET['test']
        history_model.active_build = request.GET['a']
        history_model.baseline_build = request.GET['b']
        history_model.summary = cbs.get_history_by_test(history_model.category_name,history_model.test_name)
        buildSelectorForm = FormBuildsSelector(baseline_build_selected=history_model.baseline_build,
                                               active_build_selected=history_model.active_build)
        return render(request, "history.html", {"model": history_model, "form_buildsSelector": buildSelectorForm})

    history_model.debug_message = "Error connecting CBS"
    return render(request, "dashboard.html", {"model": history_model})