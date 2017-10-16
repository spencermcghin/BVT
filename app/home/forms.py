# Imports
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, SelectField, PasswordField, IntegerField
from wtforms.validators import DataRequired


class TestSelectForm(FlaskForm):
    """
    Form to select test type and route user to form for test type
    """
    test_type = SelectField(u'Select Test Type',
                            choices=[('dashboard', 'Dashboard'), ('catalog', 'Catalog Objects'), ('ui', 'User Interface'),
                                     ('report', 'Report'), ('logsql', 'Logical SQL')],
                            validators=[DataRequired("Please Choose a Test Type.")])
    submit = SubmitField('Next')


class DashboardForm(FlaskForm):
    """
    Form to configure dashboard test
    """
    test_name = StringField('Test File Name (no spaces)', validators=[DataRequired("Please enter a name for the test.")])
    deployment_a = StringField('Baseline Deployment Name',
                               validators=[DataRequired("Please designate a name for the baseline test.")])
    baseline_env = StringField('Baseline Analytics URL (http://servername:9704/analytics)',
                               validators=[DataRequired("Please designate a baseline analytics URL.")])
    username_a = StringField('Baseline OBIEE User Name', validators=[DataRequired("Please enter your OBIEE user name.")])
    password_a = PasswordField('Baseline OBIEE Password', validators=[(DataRequired("Please enter your OBIEE password."))])
    deployment_b = StringField('Target Deployment Name',
                               validators=[DataRequired("Please designate a name for the target test.")])
    secondary_env = StringField('Target Analytics URL (http://servername:9704/analytics)',
                                validators=[DataRequired("Please designate a secondary analytics URL.")])
    username_b = StringField('Target OBIEE User Name', validators=[DataRequired("Please enter your OBIEE user name.")])
    password_b = PasswordField('Target OBIEE Password', validators=[(DataRequired("Please enter your OBIEE password."))])
    dashboard_path = StringField('Dashboard Path (as in /shared/...)',
                                 validators=[DataRequired("Please designate a path to the target dashboard(s).")])
    submit = SubmitField('Run Test')


class CatalogForm(FlaskForm):
    """
    Form to configure catalog test
    """
    test_name = StringField('Test Name (no_spaces)', validators=[DataRequired("Please enter a name for the test.")])
    baseline_env = StringField('Baseline Analytics URL (http://servername:9704/analytics)',
                               validators=[DataRequired("Please designate a baseline analytics URL.")])
    deployment_a = StringField('Baseline Deployment Name',
                               validators=[DataRequired("Please designate a name for the baseline test.")])
    user_a = StringField('Baseline OBIEE User Name', validators=[DataRequired("Please enter your OBIEE user name.")])
    pass_a = PasswordField('Baseline OBIEE Password', validators=[(DataRequired("Please enter your OBIEE password."))])
    deployment_b = StringField('Target Deployment Name',
                               validators=[DataRequired("Please designate a name for the target test.")])
    secondary_env = StringField('Target Analytics URL (http://servername:9704/analytics)',
                                validators=[DataRequired("Please designate a secondary analytics URL.")])
    user_b = StringField('Target OBIEE User Name', validators=[DataRequired("Please enter your OBIEE user name.")])
    pass_b = PasswordField('Target OBIEE Password', validators=[(DataRequired("Please enter your OBIEE password."))])
    catalog_path = StringField('Catalog Path (as in /shared/...)',
                               validators=[DataRequired("Please designate a path to the target catalog content.")])
    submit = SubmitField('Run Test')


class UIForm(FlaskForm):
    """
    Form to configure catalog test
    """
    test_name = StringField('Test Name (no_spaces)', validators=[DataRequired("Please enter a name for the test.")])
    deployment_a = StringField('Baseline Deployment Name',
                               validators=[DataRequired("Please designate a name for the baseline test.")])
    baseline_env = StringField('Baseline Analytics URL (http://servername:9704/analytics)',
                               validators=[DataRequired("Please designate a baseline analytics URL.")])
    username_a = StringField('Baseline OBIEE User Name', validators=[DataRequired("Please enter your OBIEE user name.")])
    password_a = PasswordField('Baseline OBIEE Password', validators=[(DataRequired("Please enter your OBIEE password."))])
    deployment_b = StringField('Target Deployment Name',
                               validators=[DataRequired("Please designate a name for the target test.")])
    secondary_env = StringField('Target Analytics URL (http://servername:9704/analytics)',
                                validators=[DataRequired("Please designate a secondary analytics URL.")])
    username_b = StringField('Target OBIEE User Name', validators=[DataRequired("Please enter your OBIEE user name.")])
    password_b = PasswordField('Target OBIEE Password', validators=[(DataRequired("Please enter your OBIEE password."))])
    thread_queue = StringField('Thread Queue Size (how many threads to spawn to load reports')
    thread_timeout = StringField('Thread Timeout (in MSecs, between 5 s and 10 min)')
    browser = SelectField(u'Browser',
                          choices=[('Firefox', 'Firefox'), ('Chrome', 'Chrome'), ('InternetExplorer', 'Internet Explorer')],
                          validators=[DataRequired("Please choose a browser type.")])
    not_rendered_flag = SelectField(u'Find Not Rendered Components',
                                    choices=[('True', 'Yes'), ('False', 'No')])
    report_snapshot_diff_flag = SelectField(u'Find Report Snapshot Differences',
                                            choices=[('True', 'Yes'), ('False', 'No')])
    dashboard_snapshot_diff_flag = SelectField(u'Find Dashboard Snapshot Differences',
                                               choices=[('True', 'Yes'), ('False', 'No')])
    catalog_path = StringField('Catalog Path (as in /shared/...)',
                               validators=[DataRequired("Please designate a path to the target catalog content.")])
    submit = SubmitField('Run Test')


class ReportForm(FlaskForm):
    """
    Form to configure report test
    """
    test_name = StringField('Test File Name (no spaces)', validators=[DataRequired("Please enter a name for the test.")])
    deployment_a = StringField('Baseline Deployment Name',
                               validators=[DataRequired("Please designate a name for the baseline test.")])
    baseline_env = StringField('Baseline Analytics URL (http://servername:9704/analytics)',
                               validators=[DataRequired("Please designate a baseline analytics URL.")])
    username_a = StringField('Baseline OBIEE User Name',
                             validators=[DataRequired("Please enter your OBIEE user name.")])
    password_a = PasswordField('Baseline OBIEE Password',
                               validators=[(DataRequired("Please enter your OBIEE password."))])
    deployment_b = StringField('Target Deployment Name',
                               validators=[DataRequired("Please designate a name for the target test.")])
    secondary_env = StringField('Target Analytics URL (http://servername:9704/analytics)',
                                validators=[DataRequired("Please designate a secondary analytics URL.")])
    username_b = StringField('Target OBIEE User Name', validators=[DataRequired("Please enter your OBIEE user name.")])
    password_b = PasswordField('Target OBIEE Password', validators=[(DataRequired("Please enter your OBIEE password."))])
    catalog_path = StringField('Catalog Path (as in /shared/...)',
                               validators=[DataRequired("Please designate a path to the target dashboard(s).")])
    read_timeout = StringField('Read Timeout (in Ms)', validators=[(DataRequired("Please enter a timeout value in Ms."))])
    submit = SubmitField('Run Test')


class LSQLForm(FlaskForm):
    """
    Form to configure logical SQL test
    """
    test_name = StringField('Test Name (no_spaces)', validators=[DataRequired("Please enter a name for the test.")])
    deployment_a = StringField('Baseline Deployment Name',
                               validators=[DataRequired("Please designate a name for the baseline test.")])
    baseline_env = StringField('Baseline Analytics URL (http://servername:9704/analytics)',
                               validators=[DataRequired("Please designate a baseline analytics URL.")])
    user_a = StringField('Baseline OBIEE User Name', validators=[DataRequired("Please enter your OBIEE user name.")])
    pass_a = PasswordField('Baseline OBIEE Password', validators=[(DataRequired("Please enter your OBIEE password."))])
    deployment_b = StringField('Target Deployment Name',
                               validators=[DataRequired("Please designate a name for the target test.")])
    secondary_env = StringField('Target Analytics URL (http://servername:9704/analytics)',
                                validators=[DataRequired("Please designate a secondary analytics URL.")])
    user_b = StringField('Target OBIEE User Name', validators=[DataRequired("Please enter your OBIEE user name.")])
    pass_b = PasswordField('Target OBIEE Password', validators=[(DataRequired("Please enter your OBIEE password."))])
    catalog_path = StringField('Catalog Path (as in /shared/...)',
                               validators=[DataRequired("Please designate a path to the target catalog content.")])
    submit = SubmitField('Run Test')
