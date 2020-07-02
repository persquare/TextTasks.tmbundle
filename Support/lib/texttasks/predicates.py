import operator
from datetime import datetime

def date_predicate(op, iso_date):
    try:
        _op = {
            '<': operator.lt,
            '<=': operator.le,
            '==': operator.eq,
            '!=': operator.ne,
            '>=': operator.ge,
            '>': operator.gt,
        }[op]
        right = datetime.strptime(iso_date, "%Y-%m-%d").date()
    except:
        # Failsafe construction – predicate always returns True
        return lambda x: True

    def predicate(iso_date):
        # operand is an iso-date, i.e. %Y-%m-%d
        try:
            left = datetime.strptime(iso_date, "%Y-%m-%d").date()
            return _op(left, right)
        except:
            # Failsafe at runtime – return True
            return True

    return predicate

def substring_predicate(substring):
    substring = str(substring).lower()
    def predicate(tag_value):
        return tag_value and substring in tag_value.lower()
    return predicate




