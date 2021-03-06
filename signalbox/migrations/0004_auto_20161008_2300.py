# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-08 23:00
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_fsm.db.fields.fsmfield
import jsonfield.fields
import phonenumber_field.modelfields
import re
import signalbox.models.validators
import signalbox.s3
import yamlfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('signalbox', '0003_auto_20151114_0202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='page',
            field=models.ForeignKey(blank=True, help_text='The page this question was displayed on', null=True, on_delete=django.db.models.deletion.SET_NULL, to='ask.AskPage'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='active',
            field=models.BooleanField(db_index=True, default=True, help_text='If deselected, Observations no longer be sent for Membership.'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='condition',
            field=models.ForeignKey(blank=True, help_text='Choose a Study/Condition for this user. To use Randomisation you must\n        save the Membership first, then randomise to a condition using the tools menu (or\n        if set, the study may auto-randomise the participant).', null=True, on_delete=django.db.models.deletion.CASCADE, to='signalbox.StudyCondition'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='relates_to',
            field=models.ForeignKey(blank=True, help_text='Sometimes a researcher may themselves become a subject in a study (for\n        example to provide ratings of different patients progress). In this instance they may\n        be added to the study multiple times, with the relates_to field set to another User,\n        for which they are providing data.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='membership_relates_to', to='signalbox.Membership', verbose_name='Linked patient'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(help_text='The person providing data, normally the participant.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='observation',
            name='due',
            field=models.DateTimeField(db_index=True, help_text='Time the Obs. will actually be made.\n        This can be affected by many things including user requests for a later call', null=True, verbose_name='time due'),
        ),
        migrations.AlterField(
            model_name='observation',
            name='due_original',
            field=models.DateTimeField(db_index=True, help_text='Original scheduled time to make this Observation.', verbose_name='time scheduled'),
        ),
        migrations.AlterField(
            model_name='observation',
            name='label',
            field=models.CharField(blank=True, help_text='The\n        text label displayed to participants in listings.', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='observation',
            name='n_in_sequence',
            field=models.IntegerField(blank=True, help_text='Indicates what position in the\n        sequence of Observations created by the Script this observation is.', null=True),
        ),
        migrations.AlterField(
            model_name='observation',
            name='offset',
            field=models.IntegerField(blank=True, help_text="Offset added to deterministic time by using the random\n        `jitter' parameter of the parent rule.", null=True, verbose_name='random offset'),
        ),
        migrations.AlterField(
            model_name='observation',
            name='status',
            field=models.IntegerField(choices=[(1, 'complete'), (0, 'pending'), (-1, 'in progress'), (-2, 'email sent, response pending'), (-3, 'due, awaiting completion'), (-4, 'redirected to external service'), (-99, 'failed'), (-999, 'missing')], db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='observationdata',
            name='key',
            field=models.CharField(choices=[('external_id', 'External reference number, e.g. a Twilio SID'), ('attempt', 'Attempt'), ('reminder', 'Reminder'), ('success', 'Success'), ('failure', 'Failure'), ('created', 'Created'), ('timeshift', 'Timeshift')], db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='reminder',
            name='kind',
            field=models.CharField(choices=[('sms', 'sms'), ('email', 'email')], default='email', max_length=100),
        ),
        migrations.AlterField(
            model_name='reminder',
            name='message',
            field=models.TextField(blank=True, help_text='The body of the message.\n        See the documentation for message_body fields on the Script model for\n        more details. You can include some variable with {{}} syntax, for\n        example {{url}} will include a link back to the observation.', verbose_name='Reminder message'),
        ),
        migrations.AlterField(
            model_name='reminder',
            name='subject',
            field=models.CharField(blank=True, help_text='For reminder emails only', max_length=1024, verbose_name='Reminder email subject'),
        ),
        migrations.AlterField(
            model_name='reply',
            name='entry_method',
            field=models.CharField(blank=True, choices=[('ad_hoc', 'Ad-hoc use of questionnaire'), ('answerphone', 'Answerphone message'), ('participant', 'Participant via the web interface'), ('anonymous', 'Anonymous survey response'), ('preview', 'Preview'), ('double_entry', 'Double entry by an administrator'), ('twilio', 'Twilio'), ('ad_hoc_script', 'Data entered after ad-hoc script use')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='reply',
            name='external_id',
            field=models.CharField(blank=True, help_text='Reference for external API, e.g. Twilio', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='reply',
            name='originally_collected_on',
            field=models.DateField(blank=True, help_text='Set this if the date that data were entered into the system is not the date\n        that the participant originally provided the responses (e.g. when retyping paper data)', null=True),
        ),
        migrations.AlterField(
            model_name='reply',
            name='user',
            field=models.ForeignKey(blank=True, help_text="IMPORTANT: this is not necessarily the user providing the data (i.e. a\n        patient) but could be an assessor or admin person doing double entry from paper. It\n        could also be null, where data is added by an AnonymousUser (e.g. Twilio or external\n        API which doesn't authenticate.)", null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='replydata',
            name='key',
            field=models.CharField(choices=[('incorrect_response', 'incorrect_response'), ('question_error', 'an error occured answering question with variablename')], db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='scoresheet',
            name='function',
            field=models.CharField(choices=[('sum', 'sum'), ('mean', 'mean'), ('min', 'min'), ('max', 'max'), ('stdev', 'stdev'), ('median', 'median')], max_length=200),
        ),
        migrations.AlterField(
            model_name='script',
            name='allow_display_of_results',
            field=models.BooleanField(default=False, help_text='If checked, then replies to these observations may be\n        visible to some users in the Admin area (e.g. for screening\n        questionnaires). If unchecked then only superusers will be able to\n        preview replies to observations made using this script.'),
        ),
        migrations.AlterField(
            model_name='script',
            name='asker',
            field=models.ForeignKey(blank=True, help_text='Survey which the participant will complete for the\n        Observations created by this script', null=True, on_delete=django.db.models.deletion.CASCADE, to='ask.Asker', verbose_name='Attached questionnaire'),
        ),
        migrations.AlterField(
            model_name='script',
            name='breaks_blind',
            field=models.BooleanField(default=True, help_text='If checked, indicates that observations created by this\n        Script have the potential to break the blind. If so, we will exclude\n        them from views which Assessors may access.'),
        ),
        migrations.AlterField(
            model_name='script',
            name='completion_window',
            field=models.IntegerField(blank=True, help_text='Window in minutes during which the observation can be\n        completed. If left blank, the observation will not expire.', null=True),
        ),
        migrations.AlterField(
            model_name='script',
            name='delay_by_days',
            field=models.IntegerField(default=0, help_text='Start the\n        observations this many days from the time the Observations are added.'),
        ),
        migrations.AlterField(
            model_name='script',
            name='delay_by_hours',
            field=models.IntegerField(default=0, help_text='Start the\n        observations this many hours from the time the Observations are added.'),
        ),
        migrations.AlterField(
            model_name='script',
            name='delay_by_minutes',
            field=models.IntegerField(default=0, help_text='Start the\n        observations this many minutes from the time the Observations are added.'),
        ),
        migrations.AlterField(
            model_name='script',
            name='delay_by_weeks',
            field=models.IntegerField(default=0, help_text='Start the\n        observations this many weeks from the time the Observations are added.', null=True),
        ),
        migrations.AlterField(
            model_name='script',
            name='delay_in_whole_days_only',
            field=models.BooleanField(default=True, help_text='If true, observations are delayed to the nearest number of\n        whole days, and repeat rules will start from 00:00 on the morning of\n        that day.'),
        ),
        migrations.AlterField(
            model_name='script',
            name='external_asker_url',
            field=models.URLField(blank=True, help_text='The full url of an external questionnaire. Note that\n            you can include {{variable}} syntax to identify the Reply or\n            Observation from which the user has been redirected. For example\n            including http://monkey.com/survey1?c={{reply.observation.dyad.user.username}}\n            would pass the username of the study participant to the external system.\n            In contrast including {{reply.observation.id}} would simply pass the\n            anonymous Observation id number. Where a questionnaire will be\n            completed more than once during the study, it iss recommended to\n            include the {{reply.id}} or {{reply.token}} to allow for reconciling\n            external data with internal data at a later date.', null=True, verbose_name='Externally hosted questionnaire url'),
        ),
        migrations.AlterField(
            model_name='script',
            name='is_clinical_data',
            field=models.BooleanField(default=False, help_text='\n        If checked, indicates only clinicians and superusers should\n        have access to respones made to this script.'),
        ),
        migrations.AlterField(
            model_name='script',
            name='jitter',
            field=models.IntegerField(blank=True, help_text='Number of minutes (plus or minus) to randomise observation\n        timing by.', null=True),
        ),
        migrations.AlterField(
            model_name='script',
            name='label',
            field=models.CharField(blank=True, default='{{script.name}}', help_text='<p>This field allows individual observations to have a\n        meaningful label when listed for participants.  Either enter a simple\n        text string, for example "Main questionnaire", or have the label created\n        dynamically from information about this script object.</p>\n<p>For example, you can enter <code>{{i}}</code> to add the index in of a particular\nobservation in a sequence  of generated observations. If you enter <code>{{n}}</code>\nthen this will be the position (\'first\', \'second\' etc.).</p>\n<p>Advanced use: If you want to reference attributes of the Script or Membership\nobjects these are passed in as extra context, so {{script.name}}\nincludes the script name, and <code>{{membership.user.last_name}}</code> would\ninclude the user\'s surname. Mistakes when entering  these variable names\nwill not result in an error, but won\'t produce any output either. </p>', max_length=255),
        ),
        migrations.AlterField(
            model_name='script',
            name='max_number_observations',
            field=models.IntegerField(default=1, help_text='The # of observations this scipt will generate.\n            Default is 1', verbose_name='create N observations'),
        ),
        migrations.AlterField(
            model_name='script',
            name='name',
            field=models.CharField(help_text='This is the name participants will see', max_length=200),
        ),
        migrations.AlterField(
            model_name='script',
            name='reference',
            field=models.CharField(help_text='An internal reference. Not shown to participants.', max_length=200, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='script',
            name='repeat',
            field=models.CharField(choices=[('YEARLY', 'YEARLY'), ('MONTHLY', 'MONTHLY'), ('WEEKLY', 'WEEKLY'), ('DAILY', 'DAILY'), ('HOURLY', 'HOURLY'), ('MINUTELY', 'MINUTELY'), ('SECONDLY', 'SECONDLY')], default='DAILY', max_length=80),
        ),
        migrations.AlterField(
            model_name='script',
            name='repeat_bydays',
            field=models.CharField(blank=True, help_text='One or more of MO, TU, WE, TH, FR, SA, SU separated by a\n        comma, to indicate which days observations will be created on.', max_length=100, null=True, verbose_name='repeat on these days of the week'),
        ),
        migrations.AlterField(
            model_name='script',
            name='repeat_byhours',
            field=models.CharField(blank=True, help_text="A number or list of integers, indicating the hours of the\n       day at which observations are made. For example, '13,19' would make\n       observations happen at 1pm and 7pm.", max_length=20, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z', 32), code='invalid', message='Enter only digits separated by commas.'), signalbox.models.validators.valid_hours_list], verbose_name='repeat at these hours'),
        ),
        migrations.AlterField(
            model_name='script',
            name='repeat_byminutes',
            field=models.CharField(blank=True, help_text='A list of numbers indicating at what minutes past the\n        hour the observations should be created. E.g. 0,30 will create\n        observations on the hour and half hour', max_length=20, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z', 32), code='invalid', message='Enter only digits separated by commas.'), signalbox.models.validators.in_minute_range], verbose_name='repeat at these minutes past the hour'),
        ),
        migrations.AlterField(
            model_name='script',
            name='repeat_bymonthdays',
            field=models.CharField(blank=True, help_text="An integer or comma separated list of integers; represents\n        days within a  month on observations are created. For example, '1, 24'\n        would create observations on the first and 24th of each month.", max_length=20, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z', 32), code='invalid', message='Enter only digits separated by commas.')], verbose_name='on these days in the month'),
        ),
        migrations.AlterField(
            model_name='script',
            name='repeat_bymonths',
            field=models.CharField(blank=True, help_text="A comma separated list of months as numbers (1-12),\n        indicating the months in which obervations can be made. E.g. '1,6' would\n        mean observations are only made in Jan and June.", max_length=20, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z', 32), code='invalid', message='Enter only digits separated by commas.')], verbose_name='repeat in these months'),
        ),
        migrations.AlterField(
            model_name='script',
            name='repeat_from',
            field=models.DateTimeField(blank=True, help_text='Leave blank for the observations to start relative to the\n        datetime they are  created (i.e. when the participant is randomised)', null=True, verbose_name='Fixed start date'),
        ),
        migrations.AlterField(
            model_name='script',
            name='repeat_interval',
            field=models.IntegerField(blank=True, help_text='The interval between each freq iteration. For example,\n        when repeating WEEKLY, an interval of 2 means once per fortnight,\n        but with HOURLY, it means once every two hours.', null=True, verbose_name='repeat interval'),
        ),
        migrations.AlterField(
            model_name='script',
            name='script_body',
            field=models.TextField(blank=True, help_text="Used for Email or SMS body. Can use django template syntax\n        to include variables: {{var}}. Currently variables available are {{url}}\n        (the link to the questionnaire), {{user}} and {{userprofile}} and\n        {{observation}}. Note that these are references to the django objects\n        themselves, so you can use the dot notation to access other attributed.\n        {{user.email}} or {{user.last_name}} for example, would print the user's\n        email address or last name.", verbose_name='Message'),
        ),
        migrations.AlterField(
            model_name='script',
            name='script_subject',
            field=models.CharField(blank=True, help_text='Subject line of an email if required. Can use django\n        template syntax to include variables: {{var}}. Currently variables\n        available are {{url}} (the link to the questionnaire), {{user}} and\n        {{userprofile}} and {{observation}}.', max_length=1024, verbose_name='Email subject'),
        ),
        migrations.AlterField(
            model_name='script',
            name='script_type',
            field=models.ForeignKey(help_text='IMPORTANT: This type attribute determines the\n        interpretation of some fields below.', on_delete=django.db.models.deletion.CASCADE, to='signalbox.ScriptType'),
        ),
        migrations.AlterField(
            model_name='script',
            name='show_in_tasklist',
            field=models.BooleanField(default=True, help_text="Should :class:`Observation`s generated by this script\n        appear in  a user's list of tasks to complete.", verbose_name="Show in user's list of tasks to complete"),
        ),
        migrations.AlterField(
            model_name='script',
            name='show_replies_on_dashboard',
            field=models.BooleanField(default=True, help_text='If true, replies to this script are visible to the user\n        on their personal dashboard.'),
        ),
        migrations.AlterField(
            model_name='script',
            name='user_instructions',
            field=models.TextField(blank=True, help_text='Instructions shown to user on their homepage and perhaps\n        elsewhere as the link to the survey. For example, "Please fill in the\n        questionnaire above. You will need to allow N minutes to do this  in\n        full." ', null=True),
        ),
        migrations.AlterField(
            model_name='scriptreminder',
            name='hours_delay',
            field=models.PositiveIntegerField(default='48'),
        ),
        migrations.AlterField(
            model_name='scripttype',
            name='sends_message_to_user',
            field=models.BooleanField(default=True, help_text='True\n        if observations created with this type of script send some form of\n        message to a user (e.g. email, sms or phone calls).'),
        ),
        migrations.AlterField(
            model_name='study',
            name='ad_hoc_askers',
            field=models.ManyToManyField(blank=True, help_text='Questionnaires which can be completed ad-hoc.', to='ask.Asker', verbose_name='Questionnaires available ad-hoc'),
        ),
        migrations.AlterField(
            model_name='study',
            name='ad_hoc_scripts',
            field=models.ManyToManyField(blank=True, help_text="Scripts which can be initiated by users on an ad-hoc basis.\n        IMPORTANT. Scripts selected here will appear on the 'add extra data' tab\n        of participants' profile pages, and will display the name of the study,\n        and the name of the script along with the username of any related\n        membership. BE SURE THESE DO NOT LEAK INFORMATION you would not which\n        participants to see.", to='signalbox.Script', verbose_name='scripts allowed on an ad-hoc basis'),
        ),
        migrations.AlterField(
            model_name='study',
            name='auto_add_observations',
            field=models.BooleanField(default=True, help_text='If on, and auto_randomise is also on, then observations will\n            be created when a membership is created. Has no effect if\n            auto_randomise is off.'),
        ),
        migrations.AlterField(
            model_name='study',
            name='auto_randomise',
            field=models.BooleanField(default=True, help_text='If on, then users are automatically added to a study\n            condition when a new membership is created.'),
        ),
        migrations.AlterField(
            model_name='study',
            name='blurb',
            field=models.TextField(blank=True, help_text='Snippet of\n        information displayed on the studies listing page.', null=True),
        ),
        migrations.AlterField(
            model_name='study',
            name='briefing',
            field=models.TextField(blank=True, help_text='Key information displayed to participants before joining\n        the study.', null=True),
        ),
        migrations.AlterField(
            model_name='study',
            name='consent_text',
            field=models.TextField(blank=True, help_text='User must agree to this before entering study.', null=True),
        ),
        migrations.AlterField(
            model_name='study',
            name='createifs',
            field=models.ManyToManyField(blank=True, help_text='Rules by which new observations might be made in response\n        to participant answers.', to='signalbox.ObservationCreator', verbose_name='Rules to create new\n        observations based on user responses'),
        ),
        migrations.AlterField(
            model_name='study',
            name='max_redial_attempts',
            field=models.IntegerField(default=3, help_text='Only relevant for telephone calls: maximium\n        number of times to try and complete the call. Default\n        if nothing is specified is 3'),
        ),
        migrations.AlterField(
            model_name='study',
            name='paused',
            field=models.BooleanField(db_index=True, default=False, help_text='If True, pauses sending of signals. Observations missed\n        will not be caught up later without manual intervention.'),
        ),
        migrations.AlterField(
            model_name='study',
            name='randomisation_probability',
            field=models.DecimalField(decimal_places=1, default=0.5, help_text='Indicates the probability that the adaptive algorithm will\n        choose weighted randomisation rather than allocation to the group which\n        minimises the imbalance (minimisation or adaptive randomisation).\n        For example, if set to .5, then deterministic allocation to the\n        smallest group will only happen half of the time. To turn off adaptive\n        randomisation set to 1.', max_digits=2),
        ),
        migrations.AlterField(
            model_name='study',
            name='redial_delay',
            field=models.IntegerField(default=30, help_text='Number of minutes to wait before calling again (mainly for phone calls)'),
        ),
        migrations.AlterField(
            model_name='study',
            name='required_profile_fields',
            field=models.CharField(blank=True, help_text='Profile fields which users\n        will be forced to complete for this study. Can be any of: landline, mobile, site, address_1, address_2, address_3, county, postcode,\n        separated by a space.', max_length=200, null=True, validators=[signalbox.models.validators.only_includes_allowed_fields]),
        ),
        migrations.AlterField(
            model_name='study',
            name='show_study_condition_to_user',
            field=models.BooleanField(default=False, help_text='If True, the user will be able to see their condition on\n        their homepage. Useful primarily for experiments where participants\n        signs up with the experimenter present and where blinding is not a\n        concern (e.g. where the experimenter carries out one of several\n        manipulations).'),
        ),
        migrations.AlterField(
            model_name='study',
            name='slug',
            field=models.SlugField(help_text='A short name\n        used to refer to the study in URLs and other places.'),
        ),
        migrations.AlterField(
            model_name='study',
            name='study_email',
            field=models.EmailField(help_text='The return email address for all mailings/alerts.', max_length=254),
        ),
        migrations.AlterField(
            model_name='study',
            name='study_image',
            field=models.ImageField(blank=True, null=True, storage=signalbox.s3.CustomS3BotoStorage(), upload_to='study/images/'),
        ),
        migrations.AlterField(
            model_name='study',
            name='valid_telephone_country_codes',
            field=models.CharField(default='44', help_text='Valid national dialing codes for participants in this study.', max_length=32, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z', 32), code='invalid', message='Enter only digits separated by commas.')]),
        ),
        migrations.AlterField(
            model_name='study',
            name='visible',
            field=models.BooleanField(db_index=True, default=False, help_text='Controls the display of the study on the /studies/ page.'),
        ),
        migrations.AlterField(
            model_name='study',
            name='visible_profile_fields',
            field=models.CharField(blank=True, help_text='Available profile fields\n        for this study. Can be any of: landline, mobile, site, address_1, address_2, address_3, county, postcode, separated by a space.', max_length=200, null=True, validators=[signalbox.models.validators.only_includes_allowed_fields]),
        ),
        migrations.AlterField(
            model_name='study',
            name='welcome_text',
            field=models.TextField(blank=True, default='Welcome to the study', help_text='Text user sees in a message box when they signup for the\n        the study. Note his message is not needed if participants will be\n        added to studies by the experimenter, rather than through the\n        website.', null=True),
        ),
        migrations.AlterField(
            model_name='study',
            name='working_day_ends',
            field=models.PositiveIntegerField(default=22, help_text='Hour (24h clock) at which phone\n            calls and texts should stop.', validators=[signalbox.models.validators.is_24_hour]),
        ),
        migrations.AlterField(
            model_name='study',
            name='working_day_starts',
            field=models.PositiveIntegerField(default=8, help_text='Hour (24h clock) at which phone\n            calls and texts should start to be made', validators=[signalbox.models.validators.is_24_hour]),
        ),
        migrations.AlterField(
            model_name='studycondition',
            name='display_name',
            field=models.CharField(blank=True, help_text='A label for this condition which can be shown to\n        the Participant (e.g. a non-descriptive name used to identify a\n        condition in an experimental session without breaking a blind.', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='studycondition',
            name='metadata',
            field=yamlfield.fields.YAMLField(blank=True, help_text='YAML meta data available describing this condition. Can be used on Questionnaires,\n        e.g. to conditionally display questions.', null=True),
        ),
        migrations.AlterField(
            model_name='studycondition',
            name='tag',
            field=models.SlugField(default='main', max_length=255),
        ),
        migrations.AlterField(
            model_name='studycondition',
            name='weight',
            field=models.IntegerField(default=1, help_text='Relative weights to allocate users to conditions'),
        ),
        migrations.AlterField(
            model_name='studysite',
            name='name',
            field=models.CharField(help_text="e.g. 'Liverpool', 'London' ", max_length=500),
        ),
        migrations.AlterField(
            model_name='textmessagecallback',
            name='post',
            field=jsonfield.fields.JSONField(blank=True, help_text='A serialised\n        request.POST object from the twilio callback', null=True),
        ),
        migrations.AlterField(
            model_name='usermessage',
            name='message_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to', to=settings.AUTH_USER_MODEL, verbose_name='To'),
        ),
        migrations.AlterField(
            model_name='usermessage',
            name='message_type',
            field=models.CharField(choices=[('Email', 'Email'), ('SMS', 'SMS')], default=('Email', 'Email'), max_length=80, verbose_name='Send as'),
        ),
        migrations.AlterField(
            model_name='usermessage',
            name='state',
            field=django_fsm.db.fields.fsmfield.FSMField(default='pending', max_length=50),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='landline',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, validators=[signalbox.models.validators.is_number_from_study_area, signalbox.models.validators.is_landline]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='mobile',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='mobile phone number, with international prefix', max_length=128, null=True, validators=[signalbox.models.validators.is_number_from_study_area], verbose_name='Mobile telephone number'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='organisation',
            field=models.CharField(blank=True, help_text='e.g. the\n        name of the surgery or hospital to which you are attached', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='postcode',
            field=models.CharField(blank=True, help_text='This is the postcode of your current address.', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='prefer_mobile',
            field=models.BooleanField(default=True, help_text='Make calls to mobile telephone number where possible. Unticking this\n        means the user prefers calls on their landline.'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='professional_registration_number',
            field=models.CharField(blank=True, help_text='A registration number for health professionals.', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='title',
            field=models.CharField(blank=True, choices=[('', ''), ('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Ms', 'Ms'), ('Miss', 'Miss'), ('Dr', 'Dr'), ('Prof', 'Prof'), ('Rev', 'Rev')], max_length=20, null=True),
        ),
    ]
