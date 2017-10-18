from flask import render_template, url_for, redirect, Response, send_from_directory, Flask
import os
import xml.etree.ElementTree as ET
import glob
import webbrowser

from . import home
from .forms import TestSelectForm, DashboardForm, CatalogForm, ReportForm, LSQLForm, UIForm
from env import BVT_PATH, APP_XML, SAVE_PATH


@home.route('/', methods=['GET', 'POST'])
def homepage():
    """
    Render the homepage template on the / route
    """

    return render_template('home/index.html', title="Welcome")


@home.route('/view_tests', methods=['GET', 'POST'])
def view_tests():
    """
    Render the test view template
    """

    tests = [file for file in os.listdir(BVT_PATH + '\\' + 'Comparisons')]

    return render_template('home/view_tests.html', tests=tests, title="View Test Results")


@home.route('/view_test/<testname>', methods=['GET', 'POST'])
def view_test(testname):
    """
    Route user to test results view from BVT
    """
    test_path = BVT_PATH + 'Comparisons' + '\\' + testname

    # Iterate through the different test folders in the testname directory and display html results
    for folder in os.listdir(test_path):
        for file in glob.glob(os.path.join(test_path, folder, '*.html')):
            webbrowser.open('file://' + os.path.realpath(file))


@home.route('/test_select', methods=['GET', 'POST'])
def test_select():
    """
    Route to test select form
    """

    form = TestSelectForm()

    if form.validate_on_submit():
        # Check to see which option is selected
        value = form.test_type.data
        if value == 'dashboard':
            return redirect(url_for('home.dashboardtest'))
        elif value == 'catalog':
            return redirect(url_for('home.catalogtest'))
        elif value == 'ui':
            return redirect(url_for('home.uitest'))
        elif value == 'report':
            return redirect(url_for('home.reporttest'))
        else:
            return redirect(url_for('home.lsqltest'))

    return render_template('home/choose_test.html', form=form, title="Select Test Type")


@home.route('/dashboard_test', methods=['GET', 'POST'])
def dashboardtest():
    """
    Route user to dashboard config form
    """

    # Instantiate form object
    form = DashboardForm()

    # variable for jinja template to render dashboard form
    dashboard_test = True

    # path to dashboard test template
    xml_file = APP_XML + '\\' + 'dashboard.xml'

    # form POST request to save new XML file to path and perform update logic
    if form.validate_on_submit():
        # Save copy of dashboard config xml file to test_files directory with name of file from config form
        xml_copy = SAVE_PATH + "\\" + form.test_name.data + '.xml'
        with open(xml_copy, 'w') as xml_test:
            with open(xml_file, 'r') as xml_temp:
                for line in xml_temp:
                    xml_test.write(line)

        # Append dashboard config file with field entries from form object
        tree = ET.parse(xml_copy)
        root = tree.getroot()

        # Get deployment objects and append with form data
        deployments = root.findall('Deployment')
        deployments[0].set('name', form.deployment_a.data)  # Deployment name for baseline environment
        deployments[1].set('name', form.deployment_b.data)  # Deployment name for target environment

        # Get catalog path element and append with form data
        test_plugin = root.findall('TestPlugin')
        test = test_plugin[0].findall('Test')
        parameter = test[0].findall('Parameter')
        parameter[0].set('value', form.dashboard_path.data)  # Catalog path to tested dashboard(s)

        # Get Server child elements and append with form data
        server_a_elem = deployments[0].findall('Server')
        user_a = server_a_elem[0].findall('UserName')  # Username for baseline environment
        user_a[0].text = form.username_a.data
        pass_a = server_a_elem[0].findall('Password')  # Password for baseline environment
        pass_a[0].text = form.password_a.data
        url_a = server_a_elem[0].findall('AnalyticsURL')  # URL for baseline environment
        url_a[0].text = form.baseline_env.data
        server_b_elem = deployments[1].findall('Server')
        user_b = server_b_elem[0].findall('UserName')  # Username for target environment
        user_b[0].text = form.username_b.data
        pass_b = server_b_elem[0].findall('Password')  # Password for target environment
        pass_b[0].text = form.password_b.data
        url_b = server_b_elem[0].findall('AnalyticsURL')  # URL for target environment
        url_b[0].text = form.secondary_env.data

        # Write copy of new xml to previously saved copy
        tree.write(xml_copy)

        # Run shell commands in background to execute test
        os.chdir(os.path.join(BVT_PATH))  # Change path to BVT home
        os.system('.\\bin\\obibvt -config {} -deployment {}'.format(xml_copy, form.deployment_a.data))  # Run first deployment
        os.system('.\\bin\\obibvt -config {} -deployment {}'.format(xml_copy, form.deployment_b.data))  # Run second deployment
        os.system('.\\bin\\obibvt -config {} -compareresults {} {}'.format(xml_copy, '.\\' + 'Results' + '\\' + form.deployment_a.data,
                                                                           '.\\' + 'Results' + '\\' + form.deployment_b.data))

        ### Comparison report run section###
        # Comparison test name variable and dashboard test variable
        comparison_test_name = form.deployment_a.data + '_' + form.deployment_b.data
        dash_test = 'com.oracle.biee.bvt.plugin.dashboard'

        # Check to see if test results page exists and if so, render it in app.
        # fReturn no results page if not, and link to home.
        if os.path.isfile(os.path.join(BVT_PATH, 'Comparisons', comparison_test_name, dash_test, 'DashboardPlugin.html')):
            return send_from_directory(os.path.join(BVT_PATH, 'Comparisons',
                                                    comparison_test_name, dash_test, 'DashboardPlugin.html'))
        else:
            return render_template('#')

    return render_template('home/test_config.html', dashboard_form=form, dashboard_test=dashboard_test, title="Dashboard")


@home.route('/catalog_test', methods=['GET', 'POST'])
def catalogtest():
    """
    Route user to catalog test page
    """

    form = CatalogForm()

    catalog_test = True

    xml_file = os.path.join(APP_XML, 'catalog.xml')

    if form.validate_on_submit():
        # Save copy of dashboard config xml file to test_files directory
        xml_copy = SAVE_PATH + "\\" + form.test_name.data + '.xml'
        with open(SAVE_PATH + '\\' + form.test_name.data + '.xml', 'w') as xml_test:
            with open(xml_file, 'r') as xml_temp:
                for line in xml_temp:
                    xml_test.write(line)

        # Append dashboard config file with field entries from form object
        tree = ET.parse(xml_copy)
        root = tree.getroot()

        # Get deployment objects and append with form data
        deployments = root.findall('Deployment')
        deployments[0].set('name', form.deployment_a.data)  # Deployment name for baseline environment
        deployments[1].set('name', form.deployment_b.data)  # Deployment name for target environment

        # Get catalog path element and append with form data
        tests = root.findall('Tests')
        test_plugin = tests[0].findall('TestPlugin')  # Get Testplugin child element
        test = test_plugin[0].findall('Test')
        parameter = test[0].findall('Parameter')
        parameter[0].set('value', form.catalog_path.data)  # Catalog path to tested report(s)

        # Get Server child elements and append with form data
        server_a_elem = deployments[0].findall('Server')
        user_a = server_a_elem[0].findall('UserName')  # Username for baseline environment
        user_a[0].text = form.username_a.data
        pass_a = server_a_elem[0].findall('Password')  # Password for baseline environment
        pass_a[0].text = form.password_a.data
        url_a = server_a_elem[0].findall('AnalyticsURL')  # URL for baseline environment
        url_a[0].text = form.baseline_env.data
        server_b_elem = deployments[1].findall('Server')
        user_b = server_b_elem[0].findall('UserName')  # Username for target environment
        user_b[0].text = form.username_b.data
        pass_b = server_b_elem[0].findall('Password')  # Password for target environment
        pass_b[0].text = form.password_b.data
        url_b = server_b_elem[0].findall('AnalyticsURL')  # URL for target environment
        url_b[0].text = form.secondary_env.data

        # Write copy of new xml to previously saved copy
        tree.write(xml_copy)

        # Run shell commands in background to execute test
        os.chdir(BVT_PATH)  # Change path to BVT home
        os.system('.\\bin\\obibvt -config {} -deployment {}'.format(xml_copy,
                                                                    form.deployment_a.data))  # Run first deployment
        os.system('.\\bin\\obibvt -config {} -deployment {}'.format(xml_copy,
                                                                    form.deployment_b.data))  # Run second deployment
        os.system('.\\bin\\obibvt -config {} -compareresults {} {}'.format(xml_copy,
                                                                                   '.\\' + 'Results' + '\\' + form.deployment_a.data,
                                                                                   '.\\' + 'Results' + '\\' + form.deployment_b.data))

    return render_template('home/test_config.html', catalog_form=form, catalog_test=catalog_test, title="Catalog")


@home.route('/ui_test', methods=['GET', 'POST'])
def uitest():
    """
    Route user to user interface test page
    """

    form = UIForm()

    ui_test = True

    xml_file = os.path.join(APP_XML, 'ui.xml')

    if form.validate_on_submit():
        # Save copy of dashboard config xml file to test_files directory
        xml_copy = SAVE_PATH + "\\" + form.test_name.data + '.xml'
        with open(SAVE_PATH + '\\' + form.test_name.data + '.xml', 'w') as xml_test:
            with open(xml_file, 'r') as xml_temp:
                for line in xml_temp:
                    xml_test.write(line)

        tree = ET.parse(xml_copy)
        root = tree.getroot()

        # Get deployment objects and append with form data
        deployments = root.findall('Deployment')
        deployments[0].set('name', form.deployment_a.data)  # Deployment name for baseline environment
        deployments[1].set('name', form.deployment_b.data)  # Deployment name for target environment

        # Get catalog path element and append with form data
        test_plugin = root.findall('TestPlugin')  # Get TestPlugin root child element
        test = test_plugin[0].findall('Test')  # Get Test child element
        test[0].set('enabled', form.not_rendered_flag.data)  # Set Not Rendered Components flag
        test[1].set('enabled', form.report_snapshot_diff_flag.data)  # Set Report Snapshot Differences flag
        test[2].set('enabled', form.dashboard_snapshot_diff_flag.data)  # Set Dashboard Snapshot Differences flag
        # Set TestPlugin parameter values
        parameter = test_plugin[0].findall('Parameter')  # Get Parameter child element
        parameter[0].set('value', form.catalog_path.data)  # Catalog path to tested report(s)
        parameter[1].set('value', form.thread_queue.data)  # Thread queue entry
        parameter[2].set('value', form.thread_timeout.data)  # Thread timeout entry
        parameter[3].set('value', form.browser.data)  # Browser type value

        # Get Server child elements and append with form data
        server_a_elem = deployments[0].findall('Server')
        user_a = server_a_elem[0].findall('UserName')  # Username for baseline environment
        user_a[0].text = form.username_a.data
        pass_a = server_a_elem[0].findall('Password')  # Password for baseline environment
        pass_a[0].text = form.password_a.data
        url_a = server_a_elem[0].findall('AnalyticsURL')  # URL for baseline environment
        url_a[0].text = form.baseline_env.data
        server_b_elem = deployments[1].findall('Server')
        user_b = server_b_elem[0].findall('UserName')  # Username for target environment
        user_b[0].text = form.username_b.data
        pass_b = server_b_elem[0].findall('Password')  # Password for target environment
        pass_b[0].text = form.password_b.data
        url_b = server_b_elem[0].findall('AnalyticsURL')  # URL for target environment
        url_b[0].text = form.secondary_env.data

        # Write copy of new xml to previously saved copy
        tree.write(xml_copy)

        # Run shell commands in background to execute test
        os.chdir(BVT_PATH)  # Change path to BVT home
        os.system('.\\bin\\obibvt -config {} -deployment {}'.format(xml_copy,
                                                                    form.deployment_a.data))  # Run first deployment
        os.system('.\\bin\\obibvt -config {} -deployment {}'.format(xml_copy,
                                                                    form.deployment_b.data))  # Run second deployment
        os.system('.\\bin\\obibvt -config {} -compareresults {} {}'.format(xml_copy,
                                                                           '.\\' + 'Results' + '\\' + form.deployment_a.data,
                                                                           '.\\' + 'Results' + '\\' + form.deployment_b.data))

    return render_template('home/test_config.html', ui_form=form, ui_test=ui_test, title="User Interface")


@home.route('/report_test', methods=['GET', 'POST'])
def reporttest():
    """
    Route user to report test page
    """

    form = ReportForm()

    report_test = True

    xml_file = os.path.join(APP_XML, 'report.xml')

    # form POST request to save new XML file to path and perform update logic
    if form.validate_on_submit():
        # Save copy of dashboard config xml file to test_files directory with name of file from config form
        xml_copy = SAVE_PATH + "\\" + form.test_name.data + '.xml'
        with open(xml_copy, 'w') as xml_test:
            with open(xml_file, 'r') as xml_temp:
                for line in xml_temp:
                    xml_test.write(line)

        # Append dashboard config file with field entries from form object
        tree = ET.parse(xml_copy)
        root = tree.getroot()

        # Get deployment objects and append with form data
        deployments = root.findall('Deployment')
        deployments[0].set('name', form.deployment_a.data)  # Deployment name for baseline environment
        deployments[1].set('name', form.deployment_b.data)  # Deployment name for target environment

        # Get catalog path element and append with form data
        test_plugin = root.findall('TestPlugin')
        test = test_plugin[0].findall('Test')
        parameter = test[0].findall('Parameter')
        parameter[0].set('value', form.catalog_path.data)  # Catalog path to tested report(s)

        # Get timeout element and append with form data
        parameter_parent = test_plugin[0].findall('Parameter')
        parameter_parent[0].set('value', form.read_timeout.data)

        # Get Server child elements and append with form data
        server_a_elem = deployments[0].findall('Server')
        user_a = server_a_elem[0].findall('UserName')  # Username for baseline environment
        user_a[0].text = form.username_a.data
        pass_a = server_a_elem[0].findall('Password')  # Password for baseline environment
        pass_a[0].text = form.password_a.data
        url_a = server_a_elem[0].findall('AnalyticsURL')  # URL for baseline environment
        url_a[0].text = form.baseline_env.data
        server_b_elem = deployments[1].findall('Server')
        user_b = server_b_elem[0].findall('UserName')  # Username for target environment
        user_b[0].text = form.username_b.data
        pass_b = server_b_elem[0].findall('Password')  # Password for target environment
        pass_b[0].text = form.password_b.data
        url_b = server_b_elem[0].findall('AnalyticsURL')  # URL for target environment
        url_b[0].text = form.secondary_env.data

        # Write copy of new xml to previously saved copy
        tree.write(xml_copy)

        # Run shell commands in background to execute test
        os.chdir(BVT_PATH)  # Change path to BVT home
        os.system('.\\bin\\obibvt -config {} -deployment {}'.format(xml_copy,
                                                                    form.deployment_a.data))  # Run first deployment
        os.system('.\\bin\\obibvt -config {} -deployment {}'.format(xml_copy,
                                                                    form.deployment_b.data))  # Run second deployment
        os.system('.\\bin\\obibvt -config {} -compareresults {} {}'.format(xml_copy,
                                                                           '.\\' + 'Results' + '\\' + form.deployment_a.data,
                                                                           '.\\' + 'Results' + '\\' + form.deployment_b.data))

    return render_template('home/test_config.html', report_form=form, report_test=report_test, title="Report")


@home.route('/lsql_test', methods=['GET', 'POST'])
def lsqltest():
    """
    Route user to logical sql test page
    """

    form = LSQLForm()

    lsql_test = True

    xml_file = os.path.join(APP_XML, 'lsql.xml')

    if form.validate_on_submit():
        # Save copy of dashboard config xml file to test_files directory
        xml_copy = SAVE_PATH + "\\" + form.test_name.data + '.xml'
        with open(SAVE_PATH + '\\' + form.test_name.data + '.xml', 'w') as xml_test:
            with open(xml_file, 'r') as xml_temp:
                for line in xml_temp:
                    xml_test.write(line)

                    # Append dashboard config file with field entries from form object
        tree = ET.parse(xml_copy)
        root = tree.getroot()

        # Get deployment objects and append with form data
        deployments = root.findall('Deployment')
        deployments[0].set('name', form.deployment_a.data)  # Deployment name for baseline environment
        deployments[1].set('name', form.deployment_b.data)  # Deployment name for target environment

        # Get catalog path element and append with form data
        tests = root.findall('Tests')
        test_plugin = tests[0].findall('TestPlugin')  # Get Testplugin child element
        test = test_plugin[0].findall('Test')
        parameter = test[0].findall('Parameter')
        parameter[0].set('value', form.catalog_path.data)  # Catalog path to tested report(s)

        # Get Server child elements and append with form data
        server_a_elem = deployments[0].findall('Server')
        user_a = server_a_elem[0].findall('UserName')  # Username for baseline environment
        user_a[0].text = form.username_a.data
        pass_a = server_a_elem[0].findall('Password')  # Password for baseline environment
        pass_a[0].text = form.password_a.data
        url_a = server_a_elem[0].findall('AnalyticsURL')  # URL for baseline environment
        url_a[0].text = form.baseline_env.data
        server_b_elem = deployments[1].findall('Server')
        user_b = server_b_elem[0].findall('UserName')  # Username for target environment
        user_b[0].text = form.username_b.data
        pass_b = server_b_elem[0].findall('Password')  # Password for target environment
        pass_b[0].text = form.password_b.data
        url_b = server_b_elem[0].findall('AnalyticsURL')  # URL for target environment
        url_b[0].text = form.secondary_env.data

        # Write copy of new xml to previously saved copy
        tree.write(xml_copy)

        # Run shell commands in background to execute test
        os.chdir(BVT_PATH)  # Change path to BVT home
        os.system('.\\bin\\obibvt -config {} -deployment {}'.format(xml_copy,
                                                                    form.deployment_a.data))  # Run first deployment
        os.system('.\\bin\\obibvt -config {} -deployment {}'.format(xml_copy,
                                                                    form.deployment_b.data))  # Run second deployment
        os.system('.\\bin\\obibvt -config {} -compareresults {} {}'.format(xml_copy,
                                                                           '.\\' + 'Results' + '\\' + form.deployment_a.data,
                                                                           '.\\' + 'Results' + '\\' + form.deployment_b.data))

    return render_template('home/test_config.html', lsql_form=form, lsql_test=lsql_test, title="Logical SQL")



