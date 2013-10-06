import re
from collections import namedtuple
from django.utils.encoding import smart_unicode

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def unslugify(*args, **kwargs):
    """Unslugify a slug 
    ie. my-crazy-aunt becomes My crazy aunt
    capable of multiple *args and returns list
    """
    return_result = []
    delim = kwargs.get('delim', ' ')
    for slug in args:
        result = []
        for i,word in enumerate(_punct_re.split(slug.lower())):
            # uppercase first char
            word = word.title() if i is 0 else word
            # extend list
            result.extend(smart_unicode(word).split())
        # add inner result to outer, so we can have multi returns
        return_result.append(unicode(delim.join(result)))
    # return first item in list but if there are more items then return the complete list
    return return_result if len(return_result) > 1 else return_result[0]


def get_namedtuple_choices(name, choices_tuple):
    """Factory function for quickly making a namedtuple suitable for use in a
    Django model as a choices attribute on a field. It will preserve order.

    Usage::

        class MyModel(models.Model):
            COLORS = get_namedtuple_choices('COLORS', (
                (0, 'BLACK', 'Black'),
                (1, 'WHITE', 'White'),
            ))
            colors = models.PositiveIntegerField(choices=COLORS)

        >>> MyModel.COLORS.BLACK
        0
        >>> MyModel.COLORS.get_choices()
        [(0, 'Black'), (1, 'White')]

        class OtherModel(models.Model):
            GRADES = get_namedtuple_choices('GRADES', (
                ('FR', 'FR', 'Freshman'),
                ('SR', 'SR', 'Senior'),
            ))
            grade = models.CharField(max_length=2, choices=GRADES)

        >>> OtherModel.GRADES.FR
        'FR'
        >>> OtherModel.GRADES.get_choices()
        [('FR', 'Freshman'), ('SR', 'Senior')]

    """
    class Choices(namedtuple(name, [name for val,name,desc in choices_tuple])):
        __slots__ = ()
        _choices = tuple([desc for val,name,desc in choices_tuple])

        def get_choices(self):
            return zip(tuple(self), self._choices)

        def get_values(self):
            values = []
            for val,name,desc in choices_tuple:
                if isinstance(val, type([])):
                    values.extend(val)
                else:
                    values.append(val)
            return values

        def get_value_by_name(self, input_name):
            for val,name,desc in choices_tuple:
                if name == input_name:
                    return val
            return False

        def is_valid(self, selection):
            for val,name,desc in choices_tuple:
                if val == selection or name == selection or desc == selection:
                    return True
            return False

    return Choices._make([val for val,name,desc in choices_tuple])


TWEET_TYPES = get_namedtuple_choices('TWEET_TYPES', (
    (0, 'unknown', 'Unknown'),
    (1, 'mention', 'Mentions'),
    (2, 'dm', 'Direct Message'),
))

