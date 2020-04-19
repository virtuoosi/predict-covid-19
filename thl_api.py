
import datetime
import json
import logging
import numpy as np
import urllib3

logger = logging.getLogger(__name__)
http_pool = urllib3.PoolManager()


def __map_label_to_value(api_data, dimension_id):
    result = {}
    category = api_data["dataset"]["dimension"][dimension_id]["category"]
    for (label_code, label) in category["label"].items():
        key = str(category["index"][label_code])
        if key in api_data["dataset"]["value"]:
            result[label] = api_data["dataset"]["value"][key]
    return result



def total_cases_by_date():
    URL = "https://sampo.thl.fi/pivot/prod/fi/epirapo/covid19case/fact_epirapo_covid19case.json?column=dateweek2020010120201231-443702L"
    response = http_pool.request('GET', URL)
    response_data = json.loads(response.data.decode('utf8'))
    label_map = __map_label_to_value(response_data, dimension_id="dateweek2020010120201231")
    dates = []
    cases = []
    for (date_str, cases_str) in label_map.items():
        dates.append(datetime.datetime.strptime(date_str, '%Y-%m-%d'))
        cases.append(int(cases_str))
    return np.array(dates), np.array(cases)


def cases_by_hdc():
    # Using CSV here instead of JSON, as it's a bit more simple 
    # in the case where we need two dimensions.
    URL = "https://sampo.thl.fi/pivot/prod/fi/epirapo/covid19case/fact_epirapo_covid19case.csv?column=dateweek2020010120201231-443702L&row=hcdmunicipality2020-445222"
    response_data = http_pool.request('GET', URL).data.decode('utf8')
    
    response_rows = response_data.split("\n")
    
    results_tmp = {}
    for row in response_rows[1:]:
        fields = row.split(";")
        if len(fields) == 3 and fields[1].lower() != "kaikki alueet":
            if len(fields[2]) > 0:
                if fields[1] not in results_tmp:
                    results_tmp[fields[1]] = []
                results_tmp[fields[1]].append((datetime.datetime.strptime(fields[0], '%Y-%m-%d'), int(fields[2])))

    results = {}
    for key in results_tmp:
        results_tmp[key] = sorted(results_tmp[key], key=lambda t: t[0])
        results[key] = ([t[0] for t in results_tmp[key]], [t[1] for t in results_tmp[key]])

    return results


def total_cases_by_age_group():
       
    URL = "https://sampo.thl.fi/pivot/prod/fi/epirapo/covid19case/fact_epirapo_covid19case.csv?column=ttr10yage-444309"
    response_data = http_pool.request('GET', URL).data.decode('utf8')
    
    response_rows = response_data.split("\n")
    results = {}
    for row in response_rows[1:-2]:
        fields = row.split(";")
        results[fields[0]] = int(fields[1])
    
    return results

def total_tests_by_date():

    URL = "https://sampo.thl.fi/pivot/prod/fi/epirapo/covid19case/fact_epirapo_covid19case.csv?column=dateweek2020010120201231-443702L&row=445356"
    response_data = http_pool.request('GET', URL).data.decode('utf8')

    response_rows = response_data.split("\n")
    dates = []
    values = []
    for row in response_rows[1:]:
        fields = row.split(";")
        if len(fields) == 3 and len(fields[2]) > 0:
            dates.append(datetime.datetime.strptime(fields[0], '%Y-%m-%d'))
            values.append(int(fields[2]))

    return dates, np.array(values)