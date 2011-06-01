from __future__ import unicode_literals, print_function, division
from datetime import datetime
import unittest

import simplerender
from simplerender import xrender
from simplerender import xstr

class TestSimpleTemplate(unittest.TestCase):
    def setUp(self):
        super(TestSimpleTemplate, self).setUp()
        self.content =\
        """
        Hi ##FIRSTNAME## ##LASTNAME##,

        Welcome to ##LISTNAME##!

        Today we are looking for a faster template technology to render Appmail.

        The two opponents are: ##T1## vs. ##T2##

        PS.
        1.
        Basic authentication is a simple challenge/response. If you try to access a resource that's
        protected by basic authentication, and you don't provide the proper credentials, you
        receive a challenge and you have to make the request again. It's used by the del.icio.us
        web service I showed you in Chapter 2, as well as my mapping service in Chapter 6 and
        my del.icio.us clone in Chapter 7.
        2.
        Our experiences were universal: Our software crashed or couldn't scale. The databases
        crashed and data was corrupted, while every server, disk, and switch failed in ways the
        manufacturer absolutely, positively said it wouldn't. Hackers attacked-first for fun
        and then for profit. And just when we got things working again, a new feature would
        be pushed out, traffic would spike, and everything would break all over again.


        Br,
        ##FROM##
        ##COMPANY##
        ##EMAIL##
        """
        self.model = {
            'FIRSTNAME': 'Bob',
            'LASTNAME': 'Anderson',
            'LISTNAME': 'Python Club',
            'T1': 'Jinja',
            'T2': 'SimpleTemplate',
            'FROM': 'nanfang',
            'COMPANY': 'nanfang',
            'EMAIL': 'nanfang05@gmail.com'
        }

        self.expected =\
        """
        Hi Bob Anderson,

        Welcome to Python Club!

        Today we are looking for a faster template technology to render Appmail.

        The two opponents are: Jinja vs. SimpleTemplate

        PS.
        1.
        Basic authentication is a simple challenge/response. If you try to access a resource that's
        protected by basic authentication, and you don't provide the proper credentials, you
        receive a challenge and you have to make the request again. It's used by the del.icio.us
        web service I showed you in Chapter 2, as well as my mapping service in Chapter 6 and
        my del.icio.us clone in Chapter 7.
        2.
        Our experiences were universal: Our software crashed or couldn't scale. The databases
        crashed and data was corrupted, while every server, disk, and switch failed in ways the
        manufacturer absolutely, positively said it wouldn't. Hackers attacked-first for fun
        and then for profit. And just when we got things working again, a new feature would
        be pushed out, traffic would spike, and everything would break all over again.


        Br,
        nanfang
        nanfang
        nanfang05@gmail.com
        """

    def test_should_render_string_by_simple_template(self):
        self.assertEquals(simplerender.render_string('test ###name## Sucks!', {'name': 'Jinja'}, '##', '##'),
                          'test #Jinja Sucks!'
        )

    def test_should_render_string_by_simple_template(self):
        self.assertEquals(xrender('test ###name## Sucks!', {'name': 'Jinja'}),
                          'test #Jinja Sucks!'
        )
        self.assertEquals(xrender('test ####name## Sucks!', {'name': 'Jinja'}),
                          'test ##Jinja Sucks!'
        )
        self.assertEquals(xrender('test # ##name## Sucks!', {'name': 'Jinja'}),
                          'test # Jinja Sucks!'
        )
        self.assertEquals(xrender('test ## ##name## Sucks!', {'name': 'Jinja'}),
                          'test ## Jinja Sucks!'
        )

        self.assertEquals(xrender('test ## ##name## ##Sucks!', {'name': 'Jinja'}),
                          'test ## Jinja ##Sucks!'
        )


    ## test case same as test_personalizer
    def test_render_a_template_by_given_values(self):
        template = "Hello ##firstname##, welcome to our ##clubname##"
        values = {'firstname': 'Bob', 'clubname': 'NBA Club'}
        content = xrender(template, values)

        self.assertEqual("Hello Bob, welcome to our NBA Club", content)

    def test_render_a_template_and_use_alt_value_as_default(self):
        template = "Hello ##firstname##, welcome to our ##clubname##"
        values = {'clubname': 'NBA Club'}

        content = xrender(template, values, alts={'firstname': 'Daniel', 'clubname': 'Football Club'})

        self.assertEqual("Hello Daniel, welcome to our NBA Club", content)

    def test_render_a_template_and_retain_undefined_token(self):
        template = "Hello ##firstname##, welcome to our ##clubname##"
        values = {'firstname': 'Bob'}

        content = xrender(template, values)

        self.assertEqual("Hello Bob, welcome to our ##clubname##", content)

    def test_render_a_template_and_retain_illegal_sharps(self):
        template = "Hello ##firstname##, ##welcome ####to our ##clubname#### ###"
        values = {'firstname': 'Bob', 'clubname': 'NBA Club'}

        content = xrender(template, values)

        self.assertEqual("Hello Bob, ##welcome ####to our NBA Club## ###", content)

    def test_render_a_template_with_case_insensitive(self):
        template = "Hello ##firstname##, welcome to our ##clubname##"
        values = {'FirstName': 'Bob', 'ClubName': 'NBA Club'}

        content = xrender(template, values)

        self.assertEqual("Hello Bob, welcome to our NBA Club", content)

    def test_rend_a_template_when_token_prefix_is_an_sharp(self):
        template = "###No##"
        values = {'No': 1}
        content = xrender(template, values)
        self.assertEqual("#1", content)

    def test_render_a_template_with_concatenated_tokes(self):
        template = "Your user ID is ##No_prefix####No##"
        values = {'No_prefix': 'NBA-', 'No': 1}
        content = xrender(template, values)

        self.assertEqual("Your user ID is NBA-1", content)

    def test_rend_a_template_with_single_sharp(self):
        template = "#"
        values = {}

        content = xrender(template, values)

        self.assertEqual("#", content)

    def test_rend_a_template_with_odd_sharps(self):
        template = "###"
        values = {}

        content = xrender(template, values)
        self.assertEqual("###", content)

    def test_rend_a_template_with_even_sharps(self):
        template = "####"
        values = {}

        content = xrender(template, values)

        self.assertEqual("####", content)

    def test_render_to_blank_when_no_altvalue_in_personalization_define_and_not_provide_values(self):
        template = "Your name is ##firstname##.##lastname##"
        values = {}
        content = xrender(template, values, alts={'firstname': None, 'lastname': ''})

        self.assertEqual("Your name is .", content)

    def test_ignore_overmany_values_when_rendering_a_template(self):
        template = "Hello ##firstname##, welcome to our ##clubname##"
        values = {'firstname': 'Bob', 'lastname': 'Brown', 'clubname': 'NBA Club', 'age': 26}

        content = xrender(template, values)

        self.assertEqual("Hello Bob, welcome to our NBA Club", content)
        
    ## jinja can not do it
    def test_token_name_with_something(self):
        template = "Hello ##first-name## ##last name##, welcome to our ##club.name##"
        values = {'first-name': 'Bob', 'last name':'Anderson', 'club.name': 'NBA Club'}

        content = xrender(template, values)

        self.assertEqual("Hello Bob Anderson, welcome to our NBA Club", content)

    def test_customer_formatter(self):
        def my_formatter(obj):
            if isinstance(obj, datetime):
                return str(obj.year)
            return xstr(obj)

        template = "Hello your are born in ##birth-date##"
        values = {'birth-date':datetime.now()}

        content = xrender(template, values, formatter=my_formatter)

        self.assertEqual("Hello your are born in 2011", content)


    def test_should_render_string_by_xrender(self):
        self.assertEquals(xrender(self.content, self.model),
                          self.expected
        )
