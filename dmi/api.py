

def generate_base_url(interval_value: str, country_value: str, datatype_value: str, area_value):
    return f'https://www.dmi.dk/dmidk_obsWS/rest/archive/{interval_value}/{country_value}/{datatype_value}/{area_value}/'

def generate_hourly_url():
    pass