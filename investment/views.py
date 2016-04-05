from django.shortcuts import render, render_to_response
from .forms import FirstForm
from django.http import HttpResponse
from .invest import Investment
# from .invest4float import Investment

import json

# Create your views here.



def index(request):

    if request.method == 'POST':
        print(request.POST)
        form = FirstForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
    else:
        form = FirstForm(initial={'number_of_companies': '4', 'number_of_rows': '5'})


    return render(request,
        'investment/base.html',
        {'form': form})


def get_data(request):
    our_result = []
    max_revenue = 0
    res = {}
    if request.is_ajax():
        if request.method == 'POST':
            data = json.loads(request.body.decode())
            rows = int(data.pop('numberOfRows'))
            companies = int(data.pop('numberOfCompanies'))


            if int(data['X2']) - int(data['X1']) > 1 or int(data['X1']) != 0:
                xs = []
                for x in data:
                    if 'X' in x:
                        xs.append(int(data[x]))
                print(sorted(xs))
            else:
                xs = None

            invest_obj = Investment(number_of_enterprises=companies, req_dict=data, numb_of_rows=rows)
            n_of_proj, invest_dict = invest_obj.create_dictionary()
            print("invest_dict", invest_dict)
            res_fs = invest_obj.find_maximums(invest_dict, n_of_proj, xs)
            print("res_fs", res_fs)
            invest_result = invest_obj.return_result(invest_dict, res_fs, xs)
            print("invest_result", invest_result)

            s = "Iнвестувавши "
            ss = {}
            ss['companies'] = []
            for i in range(len(invest_result)):
                comp = 'company' + str(i+1)
                c = 'C' + str(i+1)
                r = 'R' + str(i+1)
                our_result.append(invest_dict[comp][0][invest_result[i]][c])
                try:
                    max_revenue += int(invest_dict[comp][0][invest_result[i]][r]) # БЫЛо int(...)
                except Exception:
                    max_revenue += float(invest_dict[comp][0][invest_result[i]][r])
                s += "в компанiю №{} - {} у.о., \n".format(i+1, our_result[i])
                ss['companies'].append({"company": i+1, "investValue": int(our_result[i])})
            s += "ви зможете отримати максимальний дохiд від iнвестування -- {}".format(max_revenue)
            ss['revenue'] = max_revenue
            ss['out_result'] = s

            res = json.dumps(ss)
            return HttpResponse(json.dumps(ss), content_type="application/json")
        else:
            return HttpResponse(json.dumps("response_data"), content_type="application/json")
