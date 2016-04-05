$(document).ready(function(){
        $('.popup .close_window, .overlay').click(function (){
                $('.popup, .overlay').css({'opacity':'0', 'visibility':'hidden'});
        });
        $('a.open_window').click(function (e){
            $('.popup, .overlay').css({'opacity':'1', 'visibility':'visible'});
        });
        var selectCompanies = $('#id_number_of_companies');
        var selectVariants = $('#id_number_of_rows');
        var numberOfCompanies = $('#id_number_of_companies').find(":selected").text();
        var numberOfVariants = $('#id_number_of_rows').find(":selected").text();
        selectCompanies.change(function(){
            numberOfCompanies = $('#id_number_of_companies').find(":selected").text();
        });
        selectVariants.change(function(){
            numberOfVariants = $('#id_number_of_rows').find(":selected").text();
        });

        var changeBtn = $('#changeCompaniesVariants');
        changeBtn.click(function(e){
            //for(var i=numberOfVariants; i>0; i--){
            //    insRow(i);
            //}
            for(var i=numberOfVariants; i>=0; i--){
                insRow(i);
            }
            e.preventDefault();
            $('#go').show();
        });

        $('#check').click(function(e){
            e.preventDefault();


        });

        var data={}, ids, values;
        $('#go').click(function(e){
            e.preventDefault();
            $('td').each(function(index, el) {
                $(this).find('input').attr('style', 'color: #333; width: 125px; font-weight: normal; background-color: #fff;');
            });
            var rows = $('#myTable').find('tr');
            //console.log(rows.length);
            for(var i=0; i < rows.length; i++){
                for(var j=1; j < numberOfCompanies+2; j++){
                    //console.log($(rows[i]).find('td:eq('+j+') input').val());
                    ids = $(rows[i]).find('td:eq('+j+') input').attr('id');
                    values = $(rows[i]).find('td:eq('+j+') input').val();
                    console.log(ids, values);
                    data[ids] = String(values);
                    
                }
            }
            data['numberOfRows'] = String(numberOfVariants);
            data['numberOfCompanies'] = String(numberOfCompanies);
            console.log(data);
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            var csrftoken = getCookie('csrftoken');
            function csrfSafeMethod(method) {
                // these HTTP methods do not require CSRF protection
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            }
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        console.log(csrftoken);
                    }
                }
            });
            $.ajax({ 
                    url : "/counts/", // the endpoint
                    //contentType: 'application/json; charset=utf-8',
                    type : "POST", // http method
                    //processData: false,
                    data : JSON.stringify(data),
                    success: function(json) {
                        //text = json.split(' ');

                        $('#result p').remove();
                        console.log(json);
                        console.log(json['companies']);
                        console.log(json['revenue']);
                        
                        $('#result').append('<p>'+json['out_result']+'</p>');
                        var charData = json['companies'];

                        AmCharts.makeChart("chartdiv",
                            {
                                "type": "serial",
                                "categoryField": "company",
                                "autoMarginOffset": 40,
                                "marginRight": 60,
                                "marginTop": 60,
                                "startDuration": 1,
                                "fontSize": 13,
                                "theme": "light",
                                "categoryAxis": {
                                    "gridPosition": "start"
                                },
                                "trendLines": [],
                                "graphs": [
                                    {
                                        "balloonText": "[[title]] of [[category]]:[[value]]",
                                        "bullet": "round",
                                        "bulletSize": 10,
                                        "id": "AmGraph-1",
                                        "lineAlpha": 1,
                                        "lineThickness": 3,
                                        "title": "graph 1",
                                        "type": "smoothedLine",
                                        "valueField": "investValue"
                                    }
                                ],
                                "guides": [],
                                "valueAxes": [
                                    {
                                        "id": "ValueAxis-1",
                                        "title": ""
                                    }
                                ],
                                "allLabels": [],
                                "balloon": {},
                                "titles": [],
                                "dataProvider": charData
                            }
                        );

                        $('#myTable tr').each(function(index, el) {
                            for(var i=numberOfCompanies+1; i<=numberOfCompanies+1; i++){
                                for (var ii=0; ii < json['companies'].length; ii++){
                                    var v = $(this).find("td").eq(i).find('input').val()
                                    //console.log('v ' + v);
                                    //console.log(json['companies'][ii]['investValue']);
                                    if (json['companies'][ii]['investValue'] == v){
                                        console.log(i, index);
                                        $(this).find("td").eq(json['companies'][ii]['company']).find('input').attr('style', 'color: #428bca; width: 125px; font-weight: bold; background-color: #B0CFEA;');//.val('THIS');
                                    }
                                }
                                //console.log($(this).find("td").eq(i).find('input').val());
                            }
                        });

                    },
                    error : function(xhr,errmsg,err) {
                        $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                            " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                    }
            });
            //window.location.pathname = '/counts';
        });




        function insRow(variant){
            var x=document.getElementById('myTable').insertRow(0);
            //console.log(x);
            var y=x.insertCell(0);
            var z=x.insertCell(1);
            // выделяем на однин столбик больше, 1 для Хі
            numberOfCompanies = numberOfCompanies++;
            if (variant === 0){
                for(var i=1; i<=numberOfCompanies+1; i++){
                    y=x.insertCell(i);
                    if (i === numberOfCompanies+1){
                        cell = 'Вклад';
                    }
                    else {
                        cell = 'Компанія '+String(i);
                    }
                    y.outerHTML="<th>"+cell+"</th>";
                }
            } else {
                for(var i=1; i<=numberOfCompanies+1; i++){
                    y=x.insertCell(i);
                    if (i === numberOfCompanies+1){
                        cell = 'X'+String(variant);
                    }
                    else {
                        cell = 'R'+String(i)+String(variant);
                    }
                    y.innerHTML="<input type='text' style='width: 125px;' id='"+cell+"' onKeyPress ='console.log(event.keyCode);if ((event.keyCode < 46) || (event.keyCode > 57)) event.returnValue = false;'>";
                }
            }
            //z.innerHTML="<input type='button' value='Delete' class='deleteBtn' onclick='deleteRow(this)' visible='false'>";
        }
        function deleteRow(r){
            var i=r.parentNode.parentNode.rowIndex;
            document.getElementById('myTable').deleteRow(i);
        }
    });