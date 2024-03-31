from behave import given, when, then, step

from django_license_wall.license import LicenseKey, DayLicenseGenerator


@given('license wall is installed')
def step_impl(context):
    pass


@step('user tries to access {url}')
def step_impl(context, url):
    context.page = context.test.client.get(url, follow=True)


@then('he should be redirected to {url}')
def step_impl(context, url):
    if url == '/admin/login':
        page = context.page
        has_license_template = 'django_license_wall/login.html' in page.template_name
        has_license_form = 'input type="text" name="license"' in page.content.decode()
        assert has_license_template and has_license_form
    else:
        assert 'django_license_wall' not in context.page.template_name


@given('user entered license')
def step_impl(context):
    context.license = next(DayLicenseGenerator())


@when('license is valid')
def step_impl(context):
    assert LicenseKey.verify(context.license)
    context.page = context.test.client.post(context.page.wsgi_request.path,
                                            {'license': str(context.license),
                                             'next': context.page.wsgi_request.GET['next']},
                                            follow=True)


@when('license is not valid')
def step_impl(context):
    context.page = context.test.client.post(context.page.wsgi_request.path,
                                            {'license': '123',
                                             'next': context.page.wsgi_request.GET['next']},
                                            follow=True)
