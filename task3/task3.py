from datetime import datetime
import re
import sys


def error_accounting(info, data):
    data['liters_upd_fl'] = data['liters_upd_fl'] + int(re.search(r'\d+', info)[0])
    data['errors'] = data['errors'] + 1
    return data


def success_accounting(info, data, volume_cur):
    update_sc = data['liters_upd_sc'] + int(re.search(r'\d+', info)[0])
    data['volume_cur'] = volume_cur
    data['liters_upd_sc'] = update_sc
    return data


def pour_action(info, data):
    data['attempts'] = data['attempts'] + 1
    if info.count('wanna top up') > 0:
        if info.count('(успех)') > 0:
            volume_cur = data['volume_cur'] + int(re.search(r'\d+', info)[0])
            if volume_cur > max_volume: 
                data = error_accounting(info, data)
                return data
            data = success_accounting(info, data, volume_cur)
            return data
        else:
            data = error_accounting(info, data)
            return data


def scoop_action(info, data):
    data['attempts'] = data['attempts'] + 1
    if info.count('(успех)') > 0:
        volume_cur = data['volume_cur'] - int(re.search(r'\d+', info)[0])
        if volume_cur < 0:
            data = error_accounting(info, data)
            return data
        data = success_accounting(info, data, volume_cur)
        return data
    else:
        data = error_accounting(info, data)
        return data


if __name__ == '__main__':
    file_path = sys.argv[1]
    start = sys.argv[2]
    end = sys.argv[3]
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
        max_volume = int(re.search(r'\d+', lines[1])[0])
        start_volume = int(re.search(r'\d+', lines[2])[0])
        pour_data = {'attempts': 0, 'errors': 0, 'liters_upd_sc': 0, 'liters_upd_fl': 0, 'volume_cur': 32}#start_volume}
        scoop_data = {'attempts': 0, 'errors': 0, 'liters_upd_sc': 0, 'liters_upd_fl': 0, 'volume_cur': 32} #start_volume}
        pre_data = {'pre_period': 32}
        for i, row in enumerate(lines):
            if i >= 4: 
                row_data = row.split(' - ')
                try:
                    row_dt = datetime.strptime(row_data[0], '%Y-%m-%dT%H:%M:%S.%fZ')
                    start_dt = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
                    end_dt = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S')
                except ValueError:
                    sys.stdout.write('Данные были введены некорректно. Попробуйте ввести данные в формате "yyyy-mm-ddThh:mm:ss"\n')
                    sys.exit()
                if start_dt > end_dt:
                    sys.stdout.write('Указанное время начала периода превышает время его окончания\n')
                    sys.exit()
                info = row_data[2]
                if start_dt<=row_dt<=end_dt:
                    print(start_dt, row_dt)
                    if info.count('wanna top up'):
                        pour_data = pour_action(info, pour_data)
                        scoop_data['volume_cur'] = pour_data['volume_cur']
                        print(pour_data)
                    else:
                        scoop_data = scoop_action(info, scoop_data)
                        pour_data['volume_cur'] = scoop_data['volume_cur']
                    print(scoop_data)
                elif row_dt < start_dt: 
                    if info.count('wanna top up') > 0:
                        if info.count('(успех)') > 0:
                            pre_period = pre_data['pre_period'] + int(re.search(r'\d+', info)[0])
                            if pre_period <= max_volume:
                                pre_data['pre_period'] = pre_period
                    else:
                        if info.count('(успех)') > 0:
                            pre_period = pre_data['pre_period'] - int(re.search(r'\d+', info)[0])
                            if pre_period >= 0:
                                pre_data['pre_period'] = pre_period
                    print(pre_data)
        if pour_data['attempts'] == 0 or scoop_data['attempts'] == 0:
            print('За указанный вами период не было попыток налить или набрать воды')
        else:
            print('За указанный период было {attempts} попыток налить воды в бочку'.format(attempts = pour_data['attempts']))
            print('За указанный период установленный процент ошибок - {percent:.2f}%'.format(
                percent = pour_data['errors']/pour_data['attempts'] * 100
            ))
            print('За указанный период было налито {v} литров воды'.format(v = pour_data['liters_upd_sc']))
            print('За указанный период не было налито {v} литров воды'.format(v = pour_data['liters_upd_fl']))
            print('За указанный период было {attempts} попыток зачерпнуть воду из бочки'.format(attempts = scoop_data['attempts']))
            print('За указанный период установленный процент ошибок - {percent:.2f}%'.format(
                percent = scoop_data['errors']/scoop_data['attempts'] * 100
            ))
            print('За указанный период было забрано {v} литров воды'.format(v = scoop_data['liters_upd_sc']))
            print('За указанный период не было забрано {v} литров воды'.format(v = scoop_data['liters_upd_fl']))
            print('К началу периода в бочке было {v} литров воды'.format(v = pre_data['pre_period']))
            print('К концу периода в бочке было {v} литров воды'.format(v = pre_data['pre_period'] + pour_data['volume_cur']))
