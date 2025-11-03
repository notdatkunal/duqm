from helpers.commonn_utils import get_n_digit_number


def create_internal_gatepass_serial(station_code:str, customer_code:str, running_serial_c:int)->str:
    from datetime import datetime
    running_serial:str = str(running_serial_c+1)
    run_ser_six_digit = get_n_digit_number(running_serial,constant=6)
    year = str(datetime.now().year)[-2:]
    return f'{year}{station_code}{customer_code}G{run_ser_six_digit}'

def create_internal_gatepass_serial_f(station_code:str, customer_code:str)->str:
    from datetime import datetime
    year = str(datetime.now().year)[-2:]
    return f'{year}{station_code}{customer_code}G'
