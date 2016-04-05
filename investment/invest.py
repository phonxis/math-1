

# объявление класса
class Investment:
    # инициализазия переменных класса
    def __init__(self, number_of_enterprises, req_dict, numb_of_rows):
        # количество предприятий
        self.number_of_enterprises = number_of_enterprises
        # данные из таблицы
        self.data = req_dict
        # количество строчек таблицы
        self.numb_of_rows = numb_of_rows
        self.number_of_answers = 0

    # метод для превращения исходных данных:
    #   'R11': '11', 'R21': '13', 'R31': '10', 'X1': '5',
    #   'R12': '16', 'R22': '15', 'R32': '17', 'X2': '10',
    #   'R13': '23', 'R23': '21', 'R33': '22', 'X3': '15',
    #   'R14': '28', 'R24': '29', 'R34': '28', 'X4': '20',
    #   'R15': '34', 'R25': '37', 'R35': '36', 'X5': '25'

    # в удобный для рассчета вид:
    #   {'company1': [{
    #           'project5': {'C1': '25', 'R1': '34'},
    #           'project2': {'C1': '10', 'R1': '16'},
    #           'project4': {'C1': '20', 'R1': '28'},
    #           'project3': {'C1': '15', 'R1': '23'},
    #           'project1': {'C1': '5', 'R1': '11'}}],
    #   'company2': [{
    #           'project5': {'R2': '37', 'C2': '25'},
    #           'project2': {'R2': '15', 'C2': '10'},
    #           'project4': {'R2': '29', 'C2': '20'},
    #           'project3': {'R2': '21', 'C2': '15'},
    #           'project1': {'R2': '13', 'C2': '5'}}],
    #   'company3': [{
    #           'project5': {'C3': '25', 'R3': '36'},
    #           'project2': {'C3': '10', 'R3': '17'},
    #           'project4': {'C3': '20', 'R3': '28'},
    #           'project3': {'C3': '15', 'R3': '22'},
    #           'project1': {'C3': '5', 'R3': '10'}}
    #   ]}
    def create_dictionary(self):
        l = []
        enterprises = []
        copy = {}
        numb_of_proj = 0

        list_rs = []
        dd = {}
        for pred in range(1, self.number_of_enterprises+1):
            for proj in range(1, self.numb_of_rows+1):
                index = 'R'+str(pred)+str(proj)
                if not self.data[index] in list_rs:
                    list_rs.append(self.data[index])
                    index_x = 'X'+str(proj)
                    dd[index_x] = [index, self.data[index]]
            #print(dd)
            index_pred = 'company'+str(pred)
            copy[index_pred] = dd.copy()
            numb_of_proj = max(numb_of_proj, len(list_rs))
            list_rs.clear()
            dd = {}
        #print("copy", copy)
        #print(numb_of_proj)

        for i in range(1,self.number_of_enterprises+1): #1,2,3,4
            enterprise = 'company'+str(i)
            enterprises.append(enterprise)

            # задаем список для  построения структуры  -- {'enterprise4': [], 'enterprise1': [], 'enterprise3': [], 'enterprise2': []}
            l.append((enterprise,[]))

            ll = []
            projects = []
            for j in range(1,numb_of_proj+1):   #1,2,3
                project = 'project'+str(j)
                projects.append(project)

                # задаем список для добавления проектов для каждого enterprise-- [{'project1': [], 'project2': [], 'project3': []}]
                ll.append((project, []))

        #добавляем предприятия для основного dict -- {'enterprise4': [], 'enterprise1': [], 'enterprise3': [], 'enterprise2': []}
        d = dict([a for a in l])

        for pred in enterprises:
            # добавляем проекты для каждого предприятия -- [{'project1': [], 'project2': [], 'project3': []}]
            d[pred] = [dict([a for a in ll])]

        for n, k in enumerate(sorted(copy.keys()), start=1):
            for p in range(0, numb_of_proj):
                proj = 'project'+str(p+1)
                try:
                    c = sorted(copy[k])[p]
                    r = sorted(copy[k].values())[p][1]
                    c = self.data[c]
                except IndexError:
                    c = None
                    r = None
                cc = 'C' + str(n)   # значения C11, C21, ....
                rr = 'R' + str(n)   # значения R11, R21, ....
                d[k][0][proj] = dict([(cc, c),(rr, r)])

        return numb_of_proj, d

    # вычесление таблицы результатов поетапно
    # количество етапом равно количеству компаний
    # сначала вычисляются результаты для последней компании, потом пред последней, ... потом первой
    # возвращает результат типа:
    #       {'y05_pr1': 10, 'y10_pr2': 17, 'y15_pr3': 22, 'y20_pr4': 28, 'y25_pr5': 36}
    # результат определяет сколько нужно вложить в эту компанию и какой будет доход и учетом вложений в другие компании
    @staticmethod
    def etap(d=None, numb_of_rows=None, numb_of_projects=None, numb_of_companies=None, et=None, xs=None, f=None):
        data_etap = {}

        #print("ETAP\t", et)
        if f is None:
            if xs is None:
                for i in range(1, numb_of_projects+1):
                    perem = 'pr' + str(i) + '_c' + str(et)
                    data_etap[perem] = {}
                for i in range(1, numb_of_projects+1):
                    perem = 'pr' + str(i) + '_c' + str(et)
                    if d['company'+str(et)][0]['project'+str(i)]['C'+str(et)] is None:
                        data_etap[perem] = None
                    else:
                        r = int(d['company'+str(et)][0]['project'+str(i)]['C'+str(et)])
                        for ii in range(numb_of_rows-1, r-1, -1):
                            y = 'y'+str(ii)
                            data_etap[perem][y] = d['company'+str(et)][0]['project'+str(i)]['R'+str(et)]
                            if ii == r and ii != 0:
                                for p in range(ii-1, -1, -1):
                                    y = 'y'+str(p)
                                    data_etap[perem][y] = None
            else:
                for i in range(1, numb_of_projects+1):
                    perem = 'pr' + str(i) + '_c' + str(et)
                    data_etap[perem] = {}
                for i in range(1, numb_of_projects+1):
                    perem = 'pr' + str(i) + '_c' + str(et)
                    if d['company'+str(et)][0]['project'+str(i)]['C'+str(et)] is None:
                        data_etap[perem] = None
                    else:
                        r = int(d['company'+str(et)][0]['project'+str(i)]['C'+str(et)])
                        for x in sorted(xs):
                            if x < r:
                                if x < 10:
                                    y = 'y0'+str(x)
                                    data_etap[perem][y] = None
                                else:
                                    y = 'y'+str(x)
                                data_etap[perem][y] = None
                            else:
                                if x < 10:
                                    y = 'y0'+str(x)
                                    data_etap[perem][y] = d['company'+str(et)][0]['project'+str(i)]['R'+str(et)]
                                else:
                                    y = 'y'+str(x)
                                    data_etap[perem][y] = d['company'+str(et)][0]['project'+str(i)]['R'+str(et)]
        else:
            if xs is None:
                for i in range(1, numb_of_projects+1):
                    perem = 'pr' + str(i) + '_c' + str(et)
                    data_etap[perem] = {}
                for i in range(1, numb_of_projects+1):
                    perem = 'pr' + str(i) + '_c' + str(et)
                    if d['company'+str(et)][0]['project'+str(i)]['C'+str(et)] is None:
                        data_etap[perem] = None
                    else:
                        r = int(d['company'+str(et)][0]['project'+str(i)]['C'+str(et)])
                        for ii in range(numb_of_rows-1, r-1, -1):
                            y = 'y'+str(ii)
                            data_etap[perem][y] = d['company'+str(et)][0]['project'+str(i)]['R'+str(et)]
                            if ii == r and ii != 0:
                                for p in range(ii-1, -1, -1):
                                    y = 'y'+str(p)
                                    data_etap[perem][y] = None

                for k in sorted(data_etap.keys()):
                    if_none = 0
                    if data_etap[k] is not None:
                        for enum, key_y in enumerate(sorted(data_etap[k].keys())):
                            if data_etap[k][key_y] is not None:
                                f_keys = sorted(f.keys())[enum-if_none]
                                data_etap[k][key_y] = str(int(data_etap[k][key_y]) + int(f[f_keys]))
                            else:
                                if_none += 1
            else:
                for i in range(1, numb_of_projects+1):
                    perem = 'pr' + str(i) + '_c' + str(et)
                    data_etap[perem] = {}
                for i in range(1, numb_of_projects+1):
                    perem = 'pr' + str(i) + '_c' + str(et)
                    if d['company'+str(et)][0]['project'+str(i)]['C'+str(et)] is None:
                        data_etap[perem] = None
                    else:
                        r = int(d['company'+str(et)][0]['project'+str(i)]['C'+str(et)])
                        for x in sorted(xs):
                            if x < r:
                                if x < 10:
                                    y = 'y0'+str(x)
                                    data_etap[perem][y] = None
                                else:
                                    y = 'y'+str(x)
                                    data_etap[perem][y] = None
                            else:
                                if x < 10:
                                    y = 'y0'+str(x)
                                    data_etap[perem][y] = d['company'+str(et)][0]['project'+str(i)]['R'+str(et)]
                                else:
                                    y = 'y'+str(x)
                                    data_etap[perem][y] = d['company'+str(et)][0]['project'+str(i)]['R'+str(et)]

                for k in sorted(data_etap.keys()):
                    if_none = 0
                    if data_etap[k] is not None:
                        for enum, key_y in enumerate(sorted(data_etap[k].keys())):
                            if data_etap[k][key_y] is not None:
                                f_keys = sorted(f.keys())[enum-if_none]
                                data_etap[k][key_y] = str(int(data_etap[k][key_y]) + int(f[f_keys]))
                            else:
                                if_none += 1
        #print(data_etap)
        data_y = {}
        max_values = []
        max_values_key = []
        max_vals = {}
        if xs is None:
            for ii in range(0, numb_of_rows):
                for k in data_etap.keys():
                    if data_etap[k] is None or data_etap[k] == {}:
                        pass
                    else:
                        y = 'y'+str(ii)
                        if data_etap[k][y] is None:
                            max_values.append(-1)
                            max_values_key.append(k+y)
                            max_vals[k+y] = -1
                        else:
                            max_values.append(int(data_etap[k][y]))
                            max_values_key.append(k+y)
                            max_vals[k+y] = int(data_etap[k][y])
                max_value = max(max_vals.values())
                if max_values.count(max_value) > 1:
                    pass

                key_for_data_y = max_values_key[max_values.index(max_value)]
                key_for_data_y = key_for_data_y.split('_')[1][-2:] + '_' + key_for_data_y.split('_')[0]
                data_y[key_for_data_y] = max_value

                max_values = []
                max_values_key = []
                max_vals = {}
        else:
            for ii in sorted(xs):
                for k in data_etap.keys():
                    if data_etap[k] is None:
                        pass
                    else:
                        if ii < 10:
                            y = 'y0'+str(ii)
                        else:
                            y = 'y'+str(ii)
                        if data_etap[k][y] is None:
                            max_values.append(-1)
                            max_values_key.append(k+y)
                            max_vals[k+y] = -1
                        else:
                            max_values.append(int(data_etap[k][y]))
                            max_values_key.append(k+y)
                            max_vals[k+y] = int(data_etap[k][y])
                max_value = max(max_vals.values())
                if max_values.count(max_value) > 1:
                    pass
                key_for_data_y = max_values_key[max_values.index(max_value)]
                if int(key_for_data_y.split('_')[1].split('y')[1]) < 10:
                    key_for_data_y = 'y' + key_for_data_y.split('_')[1].split('y')[1] + '_' + key_for_data_y.split('_')[0]
                else:
                    key_for_data_y = 'y' + key_for_data_y.split('_')[1].split('y')[1] + '_' + key_for_data_y.split('_')[0]
                data_y[key_for_data_y] = max_value
                max_values = []
                max_values_key = []
                max_vals = {}
        return data_y

    # метод который вызывает пред. метод (etap) и собирает результаты в единый словарь
    def find_maximums(self, aa, n_of_projects, xs):
        """aa - invest dict"""
        et = self.number_of_enterprises
        result_fs = {}
        f = None
        n_of_rows = self.numb_of_rows
        numb_of_proj = n_of_projects
        numb_of_companies = self.number_of_enterprises
        for e in range(et, 0, -1):
            ep = 'ETAP ' + str(e)
            f= self.etap(aa, n_of_rows, numb_of_proj, numb_of_companies, e, xs, f)
            result_fs[ep] = f
            #print("f", f)
            #print('\n')
        return result_fs

    # метод возвращает окончательные результаты, в виде оптимальных значений вложения для каждой компании
    #       ['15', '5', '5']
    def return_result(self, aa, result_fs, xs):
        """aa - invest dict"""
        et = self.number_of_enterprises
        if xs is None:
            summ_of_money = self.numb_of_rows - 1
        else:
            summ_of_money = sorted(xs)[-1]
        max_val_etap = -1
        result_proj = []
        skips = 0
        skip_int = self.number_of_enterprises - 1
        #print("skip\t", skip_int)
        for i in range(1, et+1):
            ep = 'ETAP ' + str(i)
            for v in sorted(result_fs[ep].keys(), reverse=True):
                company = 'company' + str(i)
                proj = 'project' + str(v[-1])
                c = 'C' + str(i)
                yy = 'y' + str(v.split('_')[0].split('y')[1])
                #print("money - ", summ_of_money, "from d- ", aa[company][0][proj][c], "y-", str(int(yy.split('y')[1])))
                if summ_of_money >= int(aa[company][0][proj][c]) and int(yy.split('y')[1]) <= summ_of_money:
                    if xs is not None:
                        #print("xs0\t", sorted(xs)[0], "skip_int\t", skip_int)
                        if sorted(xs)[0] != 0 and skip_int > 0:
                            skip_int -= 1
                            continue
                    if max_val_etap < result_fs[ep][v]:
                        max_val_etap = result_fs[ep][v]
                        summ_of_money -= int(aa[company][0][proj][c])
                        result_proj.append(proj)
            skips += 1
            skip_int = self.number_of_enterprises - 1 - skips
            max_val_etap = 0

        return result_proj

if __name__ == '__main__':
    # request_dict = {'R11': '0', 'R21': '0', 'R31': '0', 'R41': '0', 'X1': '0',
    #                'R12': '3', 'R22': '0', 'R32': '4', 'R42': '0', 'X2': '1',
    #                'R13': '3', 'R23': '0', 'R33': '6', 'R43': '3', 'X3': '2',
    #                'R14': '3', 'R24': '5', 'R34': '6', 'R44': '3', 'X4': '3',
    #                'R15': '3', 'R25': '5', 'R35': '6', 'R45': '3', 'X5': '4',
    #                'R16': '3', 'R26': '9', 'R36': '6', 'R46': '3', 'X6': '5'
    #            }
    request_dict = {'R11': '11', 'R21': '13', 'R31': '10', 'X1': '5',
                    'R12': '16', 'R22': '15', 'R32': '17', 'X2': '10',
                    'R13': '23', 'R23': '21', 'R33': '22', 'X3': '15',
                    'R14': '28', 'R24': '29', 'R34': '28', 'X4': '20',
                    'R15': '34', 'R25': '37', 'R35': '36', 'X5': '25'
                    }
    rows = 5
    companies = 3

    # /////////////////////////////////
    if int(request_dict['X2']) - int(request_dict['X1']) > 1 or int(request_dict['X1']) != 0:
        xs = []
        for x in request_dict:
            if 'X' in x:
                xs.append(int(request_dict[x]))
        #print(sorted(xs))
    else:
        xs = None
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #print("XS\t\t", xs)

    invest_obj = Investment(number_of_enterprises=companies, req_dict=request_dict, numb_of_rows=rows)
    n_of_proj, invest_dict = invest_obj.create_dictionary()
    print("invest_dict", invest_dict, "\nn_of_proj", n_of_proj)

    res_fs = invest_obj.find_maximums(invest_dict, n_of_proj, xs)
    #print("res_fs", res_fs)

    invest_result = invest_obj.return_result(invest_dict, res_fs, xs)
    print("invest_result", invest_result)

    our_result = []
    max_revenue = 0
    s = ""
    for i in range(len(invest_result)):
        comp = 'company' + str(i+1)
        c = 'C' + str(i+1)
        r = 'R' + str(i+1)
        our_result.append(invest_dict[comp][0][invest_result[i]][c])
        max_revenue += int(invest_dict[comp][0][invest_result[i]][r])
        s += "В компанію №{} треба вложити {} у.о.\n".format(i+1, our_result[i])
    s += "Максимальний дохід від інвестування -- {}".format(max_revenue)
    print("result\t", our_result, "max_revenue\t", max_revenue)
