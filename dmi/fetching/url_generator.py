from dmi.fetching import objects


def __generate_base_url(interval_value: str, country_value: str, datatype_value: str, area_value):
    return f'https://www.dmi.dk/dmidk_obsWS/rest/archive/{interval_value}/{country_value}/{datatype_value}/{area_value}/'


def __filter_url(url:str):
    return url.replace(' ', r'%20')

def generate_hourly_url(area: objects.Area, datatype: objects.DataType, year: int, month: int, day: int):
    base_url = __generate_base_url(
        'hourly', area.country.name, datatype.value, area.name)
    return __filter_url(base_url + f'{str(year)}/{objects.months[month]}/{str(day)}')


def generate_daily_url(area: objects.Area, datatype: objects.DataType, year: int, month: int):
    base_url = __generate_base_url(
        'daily', area.country.name, datatype.value, area.name)
    return __filter_url(base_url + f'{str(year)}/{objects.months[month]}')


def generate_monthly_url(area: objects.Area, datatype: objects.DataType, year: int):
    base_url = __generate_base_url(
        'monthly', area.country.name, datatype.value, area.name)
    return __filter_url(base_url + f'{str(year)}')


def generate_yearly_url(area: objects.Area, datatype: objects.DataType, start_year: int, end_year: int):
    base_url = __generate_base_url(
        'yearly', area.country.name, datatype.value, area.name)
    return __filter_url(base_url + f'{str(start_year)}/{str(end_year)}')
