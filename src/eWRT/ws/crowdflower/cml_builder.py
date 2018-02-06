__author__ = 'Philipp Konrad'

import re
import unittest
import string
import itertools as it

from lxml import etree
from lxml.builder import ElementMaker


class CmlBuilder(object):
    '''
    CmlBuilder helps you to create a Crowdflower CML file.
    The following elements are included:

        * text
        * textarea
        * checkbox
        * checkboxes
        * radio buttons
        * dropdown menu
        * rating

    Each of these tags be configured with several attributes. For an
    exact listening please consult each method.

    CmlBuilder support fluid programming techniques. Of course,
    each method can be applied separately to the builder.

    Usage

        >>> builder = CmlBuilder()
        >>> builder.text('Your age', name='ageid', validates='required positiveInteger')\
        ...        .dropdown_menu('Gender', ['male', 'female', 'supercow'], 'gender', default='supercow',
        ...                      only_if='ageid')\
        ...        .textarea('Essay', name='essay', default='Write about your essay here.', validates='minLength:100')\
        ...        .radio_buttons('Essay Topic', ['romance', 'thriller', 'crime'], name='topic')\
        ...        .radio_buttons_rating('How did you like this exercise (10 = Great, 1 = Not at all)', points=10,
        ...                              name='rating')
    '''

    _maker = ElementMaker(namespace='cml', nsmap={'cml':'cml'})
    _ATTR_VALIDATES_FIELDS = ('required',
                                'url',
                                'integer',
                                'positiveInteger',
                                'numeric',
                                'alpha',
                                'alphanum',
                                'date')

    _ATTR_VALIDATES_PARAM_FIELDS = ('integerRange',
                                   'minLength',
                                   'rangeLength')

    _INTEGER_RANGE_PATTERN = r'''integerRange:{min:-?\d+,max:-?\d+}'''
    _MIN_LENGTH_PATTERN = r'''minLength:-?\d+'''
    _RANGE_LENGTH_PATTERN = r'''rangeLength:{min:-?\d+,max:-?\d+}'''


    def __init__(self):
        self._root = self._maker.root()
        self._attribute_checks = {'name' : self._attr_name_is_ok,
                                  'points' : self._attr_point_is_ok,
                                  'validates':self._attr_validates_is_ok}


    def _create_base_element(self, element_type, label='', name='', value='',
                            default='', instructions='', only_if='', validates='',
                            aggregation='', points=0):
        '''

        '''

        # get all local variables
        kwargs = locals()

        is_param = lambda k: k not in ['element_type', 'cls', 'self']

        # XML documents only can contain strings therefore unicode(v)
        # moreover, we filter all non-parameters and self, cls.
        filtered_kwargs = {k:unicode(v) for k, v in kwargs.iteritems() if is_param(k) and v}

        cleaned_kwargs = {}
        error_msg = 'The attribute is invalid: %s:%s'

        # check the sanity of all attributes.
        # each check function is looked up in a _attribute_checks dictionary
        # in the case of a bad attribute an exception is raised.
        for attr, v in filtered_kwargs.iteritems():
            check_func = self._attribute_checks.get(attr)
            if check_func: assert check_func(attr, v), error_msg % (attr, v)
            cleaned_kwargs[attr] = v

        elm_properties = {'elm_type':element_type,
                          'kwargs':cleaned_kwargs}

        # dynamically build the XML element with element builder and eval
        cmd = 'self._maker.%(elm_type)s(**%(kwargs)s)'% elm_properties
        elm = eval(cmd)

        return elm


    def _attr_name_is_ok(self, key='', value=''):
        '''
        Name attributes must be:

            * only contain lower case ASCII letters and digits
            * no other symbols like points or underlines
            * no spaces
        '''

        if not value: return False
        valid_chars = string.ascii_lowercase + string.digits
        is_valid_char = lambda c: c in valid_chars
        return all(it.imap(is_valid_char, value))


    def _attr_point_is_ok(self, key, value):
        '''
        There need to be at least 2 ratings points
        for the user.
        '''
        return value > 1

    def _attr_validates_is_ok(self, key, value):
        '''
        Check all tag attributes for correctness.
        We differ between:

            * simple attributes like `required` or `url`
            * paramatrized attributes like `minLength:10`.

        '''

        def _in(attr_value):

            # is the validator a common simple validator like 'required'
            if attr_value in self._ATTR_VALIDATES_FIELDS: return True

            # does the validator accept parameters like: minLength:4
            is_parametrized_validator =  any(attr_value.startswith(fld)
                                             for fld in self._ATTR_VALIDATES_PARAM_FIELDS)

            if not is_parametrized_validator: return False

            # check the correctness of the paramatrized validator.
            is_integer_range = (attr_value.startswith('integerRange') and
                                re.match(self._INTEGER_RANGE_PATTERN, attr_value))
            is_min_length = (attr_value.startswith('minLength') and
                             re.match(self._MIN_LENGTH_PATTERN, attr_value))
            is_range_length = (attr_value.startswith('rangeLength') and
                               re.match(self._RANGE_LENGTH_PATTERN, attr_value))

            if is_integer_range or is_min_length or is_range_length:
                return True

            return False


        assert value, 'No value for validates attribute provided!'

        values = value.split(' ')
        error_msg = 'You only can assign two values to the validates attribute: %s'
        assert len(values) < 3, error_msg % values

        if not all(_in(val) for val in values): return False

        return True


    def text(self, label='', name='', default='', instructions='', only_if='',
                   validates=''):
        '''
        Create one liner text tag. You can find an example on the crowdflower website:
        http://success.crowdflower.com/customer/portal/articles/1290342-cml-crowdflower-markup-language#CMLtext

        :param str label:  This will be displayed next to the generated form element.
                           If no name attribute is specified on a base tag, this
                           will be converted into a name by removing alpha-numeric
                           characters and replacing spaces with an underscore.

        :param str instructions: Every CML base tag can have an instructions attribute.
                                 This will be displayed next to the generated form
                                 element to help clarify the desired input.
                                 If both an instructions attribute and a
                                 `<cml:instructions />` tag is specified,
                                 only the value of the attribute will be used.

        :param str name: This must be unique across all base tags. The name should not
                         contain capital letters, spaces, or non alpha-numeric characters.
                         This will become a column header in your generated CSV.

        :param str default: this provides an example input for the user
                            and disappears once the user selects the form element.
                            Default values will not be submitted.

        :param str only_if: Every CML base tag can have an `only_if` attribute.
                            The value of this attribute should be the name of the
                            field a user must complete before this field or
                            group of fields will be displayed.

        :param str validates: CML supports a number of pre-made validation methods
                              to ensure data integrity. Some validators normalize
                              the input, making it possible to create gold for
                              complex data like phone numbers, addresses, and URLs.

                              * `required`: On a free text input, at least one
                                            non-whitespace character must be present.
                                            On a multiple choice or drop-down field,
                                            it enforces at least one item to be selected.

                              * `integer`

                              * `positiveInteger`

                              * `numeric`: Requires an integer or floating-point value.

                              * `integerRange`: Ensures that the contributor inputs an
                                                integer within a given range. Note:
                                                The values are inclusive: {min:1,max:100}

                              * `alpha`: Requires only letters, e.g., "ABCabc"

                              * `alphanum`: Allows only numbers and letters,
                                            e.g., "ahfd723nd"

                              * `date`: Requires a date in MM/DD/YYYY format,
                                        e.g., "01/21/2010"

                              * `minLength`: Ensures that the user's input is at least a
                                             certain number of characters long e.g.
                                             minLength:4

                              * `rangeLength`: Ensures that the user's input is within a
                                               given length range. Note: The values are
                                               inclusive e.g. rangeLength:{min:5,max:32}

                              * `url`: Requires a valid-looking URL,
                                       e.g. "http://crowdflower.com."
        '''

        txt_elm = self._create_base_element('text', label=label,
                                                    name=name,
                                                    default=default,
                                                    instructions=instructions,
                                                    only_if=only_if,
                                                    validates=validates)
        self._root.append(txt_elm)
        return self


    def textarea(self, label='', name='', default='', instructions='', only_if='',
                       validates=''):
        '''
        Create multiline textarea tag. You can find an example on the crowdflower website:
        http://success.crowdflower.com/customer/portal/articles/1290342-cml-crowdflower-markup-language#CMLtextarea

        :param str label:  This will be displayed next to the generated form element.
                           If no name attribute is specified on a base tag, this
                           will be converted into a name by removing alpha-numeric
                           characters and replacing spaces with an underscore.

        :param str name: This must be unique across all base tags. The name should not
                         contain capital letters, spaces, or non alpha-numeric characters.
                         This will become a column header in your generated CSV.

        :param str default: this provides an example input for the user
                            and disappears once the user selects the form element.
                            Default values will not be submitted.

        :param str instructions: Every CML base tag can have an instructions attribute.
                                 This will be displayed next to the generated form
                                 element to help clarify the desired input.
                                 If both an instructions attribute and a
                                 `<cml:instructions />` tag is specified,
                                 only the value of the attribute will be used.

        :param str only_if: Every CML base tag can have an `only_if` attribute.
                            The value of this attribute should be the name of the
                            field a user must complete before this field or
                            group of fields will be displayed.

        :param str validates: CML supports a number of pre-made validation methods
                              to ensure data integrity. Some validators normalize
                              the input, making it possible to create gold for
                              complex data like phone numbers, addresses, and URLs.

                              * `required`: On a free text input, at least one
                                            non-whitespace character must be present.
                                            On a multiple choice or drop-down field,
                                            it enforces at least one item to be selected.

                              * `integer`

                              * `positiveInteger`

                              * `numeric`: Requires an integer or floating-point value.

                              * `integerRange`: Ensures that the contributor inputs an
                                                integer within a given range. Note:
                                                The values are inclusive: e.g.
                                                integerRange:{min:1,max:100}

                              * `alpha`: Requires only letters, e.g., "ABCabc"

                              * `alphanum`: Allows only numbers and letters,
                                            e.g., "ahfd723nd"

                              * `date`: Requires a date in MM/DD/YYYY format,
                                        e.g., "01/21/2010"

                              * `minLength`: Ensures that the user's input is at least a
                                             certain number of characters long e.g.
                                             minLength:4

                              * `rangeLength`: Ensures that the user's input is within a
                                               given length range. Note: The values are
                                               inclusive e.g. rangeLength:{min:5,max:32}

                              * `url`: Requires a valid-looking URL,
                                       e.g. "http://crowdflower.com."
        '''

        txtarea = self._create_base_element('text',
                                            label=label,
                                            name=name,
                                            default=default,
                                            instructions=instructions,
                                            only_if=only_if,
                                            validates=validates)
        self._root.append(txtarea)
        return self


    def checkbox(self, label='', name='', default='', instructions='', only_if='',
                   validates=''):
        '''
        Create a checkbox tag. You can find an example on the crowdflower website:
        http://success.crowdflower.com/customer/portal/articles/1290342-cml-crowdflower-markup-language#CMLcheckbox

        :param str label:  This will be displayed next to the generated form element.
                           If no name attribute is specified on a base tag, this
                           will be converted into a name by removing alpha-numeric
                           characters and replacing spaces with an underscore.

        :param str instructions: Every CML base tag can have an instructions attribute.
                                 This will be displayed next to the generated form
                                 element to help clarify the desired input.
                                 If both an instructions attribute and a
                                 `<cml:instructions />` tag is specified,
                                 only the value of the attribute will be used.

        :param str name: This must be unique across all base tags. The name should not
                         contain capital letters, spaces, or non alpha-numeric characters.
                         This will become a column header in your generated CSV.

        :param str default: this provides an example input for the user
                            and disappears once the user selects the form element.
                            Default values will not be submitted.

        :param str only_if: Every CML base tag can have an `only_if` attribute.
                            The value of this attribute should be the name of the
                            field a user must complete before this field or
                            group of fields will be displayed.

        :param str validates: CML supports a number of pre-made validation methods
                              to ensure data integrity. Some validators normalize
                              the input, making it possible to create gold for
                              complex data like phone numbers, addresses, and URLs.

                              * `required`: On a free text input, at least one
                                            non-whitespace character must be present.
                                            On a multiple choice or drop-down field,
                                            it enforces at least one item to be selected.
        '''


        checkbox = self._create_base_element('checkbox',
                                            label=label,
                                            name=name,
                                            default=default,
                                            instructions=instructions,
                                            only_if=only_if,
                                            validates=validates)
        self._root.append(checkbox)
        return self


    def radio_buttons(self, label, radio_button_strings, name='', instructions='', only_if='',
                            validates=''):
        '''
        Create radio buttons tag. You can find an example on the crowdflower website:
        http://success.crowdflower.com/customer/portal/articles/1290342-cml-crowdflower-markup-language#CMLradios

        Usage:
            >>> builder = CmlBuilder()
            >>> builder.radio_buttons('Please choose a color', ['blue', 'red', 'green'])
            >>> builder.dumps()

        :param str label:  This will be displayed next to the generated form element.
                           If no name attribute is specified on a base tag, this
                           will be converted into a name by removing alpha-numeric
                           characters and replacing spaces with an underscore.

        :param str name: This must be unique across all base tags. The name should not
                         contain capital letters, spaces, or non alpha-numeric characters.
                         This will become a column header in your generated CSV.

        :param str instructions: Every CML base tag can have an instructions attribute.
                                 This will be displayed next to the generated form
                                 element to help clarify the desired input.
                                 If both an instructions attribute and a
                                 `<cml:instructions />` tag is specified,
                                 only the value of the attribute will be used.

        :param str only_if: Every CML base tag can have an `only_if` attribute.
                            The value of this attribute should be the name of the
                            field a user must complete before this field or
                            group of fields will be displayed.

        :param str validates: CML supports a number of pre-made validation methods
                              to ensure data integrity. Some validators normalize
                              the input, making it possible to create gold for
                              complex data like phone numbers, addresses, and URLs.

                              * `required`: On a multiple choice or drop-down field,
                                            it enforces at least one item to be selected.
        '''
        radio_btn_group = self._create_base_element('radios',
                                                    label=label,
                                                    name=name,
                                                    instructions=instructions,
                                                    only_if=only_if,
                                                    validates=validates)

        for radio_btn in radio_button_strings:
            btn = self._create_base_element('radio',
                                            label=radio_btn)
            radio_btn_group.append(btn)

        self._root.append(radio_btn_group)
        return self


    def dropdown_menu(self, label, option_strings, name='', default='', instructions='',
                            only_if='', validates=''):
        '''
        Create a dropdown menu.
        http://success.crowdflower.com/customer/portal/articles/1290342-cml-crowdflower-markup-language-#CMLselect

        Usage:
            >>> builder = CmlBuilder()
            >>> builder.dropdown_menu('Choose a city', ['Vienna', 'Chur', 'Innsbruck'])
            >>> builder.dumps()

        :param str label:  This will be displayed next to the generated form element.
                           If no name attribute is specified on a base tag, this
                           will be converted into a name by removing alpha-numeric
                           characters and replacing spaces with an underscore.

        :param str default: this provides an example input for the user
                            and disappears once the user selects the form element.
                            Default values will not be submitted.

        :param str name: This must be unique across all base tags. The name should not
                         contain capital letters, spaces, or non alpha-numeric characters.
                         This will become a column header in your generated CSV.

        :param str instructions: Every CML base tag can have an instructions attribute.
                                 This will be displayed next to the generated form
                                 element to help clarify the desired input.
                                 If both an instructions attribute and a
                                 `<cml:instructions />` tag is specified,
                                 only the value of the attribute will be used.

        :param str only_if: Every CML base tag can have an `only_if` attribute.
                            The value of this attribute should be the name of the
                            field a user must complete before this field or
                            group of fields will be displayed.

        :param str validates: CML supports a number of pre-made validation methods
                              to ensure data integrity. Some validators normalize
                              the input, making it possible to create gold for
                              complex data like phone numbers, addresses, and URLs.

                              * `required`: On a multiple choice or drop-down field,
                                            it enforces at least one item to be selected.


        '''

        assert option_strings, 'The option_strings parameter is empty!'

        if default:
            error_msg = 'Could not find default value in options: %s %s'
            assert default in option_strings, error_msg % (option_strings, default)

        drpdwn_menu = self._create_base_element('select',
                                                label=label,
                                                name=name,
                                                default=default,
                                                instructions=instructions,
                                                only_if=only_if,
                                                validates=validates)

        for option_str in option_strings:
            option = self._create_base_element('option',
                                               label=option_str)
            drpdwn_menu.append(option)

        self._root.append(drpdwn_menu)
        return self


    def radio_buttons_rating(self, label='', points=5, name='', validates=''):
        '''
        Create a task rating for the Crowdflower users. For an example see this link:
        http://success.crowdflower.com/customer/portal/articles/1290342-cml-crowdflower-markup-language#CMLratings

        Usage:
            >>> builder = CmlBuilder()
            >>> builder.radio_buttons_rating('Please rate the task from 1 to 10', points=10)
            >>> builder.dumps()

        :param str label:  This will be displayed next to the generated form element.
                           If no name attribute is specified on a base tag, this
                           will be converted into a name by removing alpha-numeric
                           characters and replacing spaces with an underscore.

        :param str instructions: Every CML base tag can have an instructions attribute.
                                 This will be displayed next to the generated form
                                 element to help clarify the desired input.
                                 If both an instructions attribute and a
                                 `<cml:instructions />` tag is specified,
                                 only the value of the attribute will be used.

        :param str name: This must be unique across all base tags. The name should not
                         contain capital letters, spaces, or non alpha-numeric characters.
                         This will become a column header in your generated CSV.

        :param str validates: CML supports a number of pre-made validation methods
                              to ensure data integrity. Some validators normalize
                              the input, making it possible to create gold for
                              complex data like phone numbers, addresses, and URLs.

                              * `required`: On a free text input, at least one
                                            non-whitespace character must be present.
                                            On a multiple choice or drop-down field,
                                            it enforces at least one item to be selected.

        http://success.crowdflower.com/customer/portal/articles/1290342-cml-crowdflower-markup-language-#CMLratings
        '''

        ratings = self._create_base_element('ratings',
                                            label=label,
                                            points=points,
                                            name=name,
                                            validates=validates)
        self._root.append(ratings)
        return self

    def checkboxes(self, label, checkbox_strings, name='', default='', instructions='',
                            only_if='', validates=''):
        '''
        Create a group of checkboxes.
        http://success.crowdflower.com/customer/portal/articles/1290342-cml-crowdflower-markup-language-#CMLcheckboxes

        Usage:
            >>> builder = CmlBuilder()
            >>> builder.checkboxes('Which fruits do you like?', ['apples', 'bananas','oranges'])
            >>> builder.dumps()
        '''

        assert checkbox_strings, 'The option_strings parameter is empty!'

        if default:
            error_msg = 'Could not find default value in options: %s %s'
            assert default in checkbox_strings, error_msg % (checkbox_strings, default)

        drpdwn_menu = self._create_base_element('checkboxes',
                                                label=label,
                                                name=name,
                                                default=default,
                                                instructions=instructions,
                                                only_if=only_if,
                                                validates=validates)

        for option_str in checkbox_strings:
            option = self._create_base_element('checkbox',
                                               label=option_str)
            drpdwn_menu.append(option)

        self._root.append(drpdwn_menu)
        return self



    def dumps(self):
        '''
        Return the CML tree as a string.

        Usage:
            >>> builder = CmlBuilder()
            >>> builder.text('Enter your age', name='name_id', validates='required positiveInteger')
            >>> builder.radio_buttons_rating('Rate the exercise', validates='required')
            >>> builder.dumps()
        '''
        children = self._root.getchildren()
        children_str = [etree.tostring(child, pretty_print=True)
                        for child in children if child is not None]
        return ''.join(children_str)


class TestCmlBuilder(unittest.TestCase):


    def test_points(self):

        test_result = '<cml:ratings xmlns:cml="cml" points="5"/>\n'
        builder = CmlBuilder()
        self.assertEquals(builder.radio_buttons_rating().dumps(), test_result)


    def test_text(self):

        builder = CmlBuilder()
        builder.text(label='My test label', name='uniquename')
        self.assertEquals(builder.dumps(),
                          '<cml:text xmlns:cml="cml" name="uniquename" label="My test label"/>\n')


    def test_textarea(self):

        builder = CmlBuilder()
        builder.textarea(label='Some explanation', name='textareaid')
        self.assertEquals(builder.dumps(),
                          '<cml:text xmlns:cml="cml" name="textareaid" label="Some explanation"/>\n')


    def test_dumps(self):

        test_result = '<cml:text xmlns:cml="cml" name="name" label="Sample text field:"/>\n' \
                    + '<cml:text xmlns:cml="cml" label="my textarea"/>\n'

        builder = CmlBuilder()
        builder.text('Sample text field:', name='name')\
               .textarea('my textarea')

        self.assertEquals(builder.dumps(), test_result)


    def test_attr_name_ok(self):

        builder = CmlBuilder()
        self.assertTrue(builder._attr_name_is_ok('key', 'testname'))
        self.assertFalse(builder._attr_name_is_ok('key', 'test_name'))
        self.assertFalse(builder._attr_name_is_ok('key', 'TestName'))
        self.assertFalse(builder._attr_name_is_ok('key', 'test name'))


    def test_attr_validates_ok(self):

        builder = CmlBuilder()

        # basic validation rules

        for config in ['required', 'integer', 'positiveInteger', 'numeric',
                       'integerRange', 'alpha', 'alphanum', 'date', 'minLength',
                       'rangeLength', 'url']:

            self.assertTrue('validates', config)

        # simple invalid values
        for faulty_config in ['.integer', 'wrong', 'URL', 'min_length']:
            self.assertFalse(builder._attr_validates_is_ok('validates', faulty_config))

        # simple composed values
        self.assertTrue(builder._attr_validates_is_ok('validates', 'required url'))
        self.assertFalse(builder._attr_validates_is_ok('validates', 'required, url'))
        self.assertFalse(builder._attr_validates_is_ok('validates', 'date x'))


    def test_attr_validates_ok_complex(self):
        builder = CmlBuilder()
        self.assertTrue(builder._attr_validates_is_ok('validates', 'integerRange:{min:10,max:100}'))
        self.assertTrue(builder._attr_validates_is_ok('validates', 'rangeLength:{min:0,max:100}'))
        self.assertTrue(builder._attr_validates_is_ok('validates', 'minLength:7'))

        self.assertTrue(builder._attr_validates_is_ok('validates', 'integerRange:{min:-4,max:100}'))
        self.assertTrue(builder._attr_validates_is_ok('validates', 'rangeLength:{min:-3000,max:100}'))
        self.assertTrue(builder._attr_validates_is_ok('validates', 'minLength:-10'))


    def test_checkbox(self):

        builder = CmlBuilder()
        builder.checkbox('A single checkbox', name='checkboxcheck')
        self.assertEquals(builder.dumps(),
                          '<cml:checkbox xmlns:cml="cml" name="checkboxcheck" label="A single checkbox"/>\n')


    def test_radioboxes(self):

        builder = CmlBuilder()
        builder.checkboxes('What are cities?', ['Wa', 'Vienna', 'Ba', 'Graz'], name='cities')
        result = '''<cml:checkboxes xmlns:cml="cml" name="cities" label="What are cities?">
  <cml:checkbox label="Wa"/>
  <cml:checkbox label="Vienna"/>
  <cml:checkbox label="Ba"/>
  <cml:checkbox label="Graz"/>
</cml:checkboxes>
'''
        self.assertEquals(builder.dumps(), result)


    def test_dropdown(self):

        builder = CmlBuilder()
        builder.dropdown_menu('Gender', ['male', 'female', 'supercow'], 'gender', default='supercow')

        result = '''<cml:select xmlns:cml="cml" default="supercow" name="gender" label="Gender">
  <cml:option label="male"/>
  <cml:option label="female"/>
  <cml:option label="supercow"/>
</cml:select>
'''
        self.assertEquals(result, builder.dumps())



    def test_cml_creation(self):

        builder = CmlBuilder()
        builder.text('Your age', name='ageid', validates='required positiveInteger')\
               .dropdown_menu('Gender', ['male', 'female', 'supercow'], 'gender', default='supercow',
                              only_if='ageid')\
               .textarea('Essay', name='essay', default='Write about your essay here.', validates='minLength:100')\
               .radio_buttons('Essay Topic', ['romance', 'thriller', 'crime'], name='topic')\
               .radio_buttons_rating('How did you like this exercise (10 = Great, 1 = Not at all', points=10,
                                     name='rating')

        builder.dumps()

if __name__ == '__main__':
    unittest.main()