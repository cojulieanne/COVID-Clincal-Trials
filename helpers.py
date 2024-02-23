def categorical_summ(x, title):
    import pandas as pd
    from collections import Counter
    
    freq = pd.DataFrame.from_dict(Counter(x.apply(pd.Series).stack()), orient = 'index').reset_index()
    freq.columns = [title, 'Count']
    freq = freq.sort_values(by = 'Count', ascending = False)
    return freq
    
def age_clean(x):
    if '(' in x or ')' in x:
        x = x.replace(')', '')
        x = x.split('(')[-1]
        return x
    return x


def intervention_types(x):
    x = str(x)
    if ':' in x:
        return x.split(':')[0].strip()
    return None

def interventions(x):
    x = str(x)
    x = x.split('|')
    output = [y.split(':')[1].strip() for y in x if ':' in y]
    if output:
        return output
    return None

def explode_dict(x):
    output = {}
    x = str(x)
    x = x.split('|')
    for y in x:
        if ':' in y:
            values = [x.strip() for x in y.split(':')]
            if values[0] in output.keys():
                output[values[0]] += [values[1]]
            else:
                output[values[0]] = [values[1]]
    if output:
        return output
    return None

def date_convert(x):
    import pendulum
    
    try:
        return pendulum.from_format(x, 'MMMM DD, YYYY').to_date_string()
    except(ValueError):
        try:
            return pendulum.from_format(x, 'MMMM YYYY').to_date_string()
        except:
            return None
    except(TypeError):
        return None

def days_between(x, start, end):
    import pendulum
    end_dt = None
    start_dt = None

    if end == 'today':
        end_dt = pendulum.today()
    else:
        if x[end]:
            end_dt = pendulum.parse(x[end])
    if start == 'today':
        start_dt = pendulum.today()
        if end_dt and end_dt < start_dt:
            end_dt = None
    else:
        if x[start]:
            start_dt = pendulum.parse(x[start])

    if end_dt and start_dt:
        return (end_dt - start_dt).in_days()

    return None

def counter_df(x, title):
    import pandas as pd
    from collections import Counter
    
    freq = pd.DataFrame.from_dict(Counter(x.apply(pd.Series).stack()), orient = 'index').reset_index()
    freq.columns = [title, 'Count']
    freq = freq.sort_values(by = 'Count', ascending = False)
    return freq

def counter_dict(x, title, keys = True, filter = None):
    import pandas as pd
    from collections import Counter
    
    values = []
    condition = True
    for dct in x:
        if dct:
            for key, value in dct.items():
                if filter == key or (filter is None):
                    if keys and key:
                        values += [key]
                    if (not keys) and value:
                        values += value
    freq = pd.DataFrame.from_dict(Counter(values), orient = 'index').reset_index()
    freq.columns = [title, 'Count']
    freq = freq.sort_values(by = 'Count', ascending = False)
    return freq

def countries(x):
    import  pycountry
    
    output = []
    for country in pycountry.countries:
        name = country.name.replace(" ", "")
        if name.lower() in str(x['Locations']).replace(" ", "").lower():
            output.append(country.name)

    return output

def clean_puncnum(x):
    import re
    x = re.sub(r'[^\w\s]', ' ', x)
    x = re.sub(r'\d+', ' ', x) 
    
    return x


def clean_text(x):
    import nltk
    from nltk.corpus import stopwords
    
    stop_words = list(stopwords.words('english'))
    
    words = x.split()
    
    clean_words = [x.lower().strip() for x in words if x.lower() not in stop_words]
    
    return ' '.join(clean_words)