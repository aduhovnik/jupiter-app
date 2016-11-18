import moneyed
from moneyed.localization import _FORMATTER
from decimal import ROUND_HALF_EVEN


BYN = moneyed.add_currency(
    code='BYN',
    numeric='933',
    name='Belarusian ruble',
    countries=('BELARUS', )
)

_FORMATTER.add_sign_definition(
    'default',
    BYN,
    suffix=u'Br'
)

_FORMATTER.add_formatting_definition(
    'by_BY',
    group_size=3, group_separator=".", decimal_point=",",
    positive_sign="",  trailing_positive_sign="",
    negative_sign="-", trailing_negative_sign="",
    rounding_method=ROUND_HALF_EVEN
)
