window.addEvent("domready", function(e){

window.poo1 = function (e) {
    e.stop();
    var start_date = $('start').get('value');
    var end_date = $('end').get('value');
    var choice = $('stat_select').getSelected()[0].get('data-flag');
    var req = new Request({
        method: 'get',
        url: 'getStats',
        data: {'start_date' : start_date,
               'end_date' : end_date,
               'flag' : choice,
               'itemid' : $$('.bStats').get('data-itemid')[0]},
        onSuccess: function(res) {
            if(res == 'invalid') {
                $('message').set('html', 'Invalid input');
                (function(){$('message').set('html', "");}).delay(2000);
                return;
            }
            console.log(res);
            res = JSON.parse(res);
            var keys = []; var vals = []; var i;
            var choice = $('stat_select').getSelected()[0].get('data-flag') == '1' ? "Quantity" : "Profit";
            for(i in res) {
                keys.push(i);
                vals.push(res[i]);
            }
            var chart = new Highcharts.Chart({
                chart: {
                    renderTo: 'container'
                },
                title: {
                    text: '',
                },
                xAxis: {
                    categories: keys
                },
                yAxis: {
                    title: {
                        text: choice
                    },
                    plotLines: [{
                        color: '#808080'
                    }]
                },
                legend: {
                    layout: 'vertical',
                    align: 'center',
                    verticalAlign: 'top',
                    borderWidth: 0
                },
                series: [{
                    name: choice,
                    data: vals
                }]
            });
        }
    }).send();
};

function addTxn(res) {
    var tt = new HtmlTable($('txns_table'));
    try {
        elts = $$(".txns");
        quans = $$(".quans");
    } catch (ex) {elts = [];}
    var flag = true;
    for (var i = 0; i < elts.length; i++) {
        if (elts[i].get('data-itemid') == res['similar_item_id'] + "_" + res['id']) {
            var tmp = elts[i].parentNode.parentNode.childNodes[2];
            var foo = elts[i].parentNode.parentNode.childNodes[3].get('html').toInt();
            var bar = elts[i].parentNode.parentNode.childNodes[4];
            var tmp2 = tmp.get('html').toInt() + 1;
            var foo2 = tmp2 * foo;
            tmp.set('html', tmp2);
            bar.set('html', foo2);
            flag = false; break;
        }
    }
    if (flag) {
        var ids = res['similar_item_id'] + "_" + res['id'];
        var rows = $('txns_table').rows.length;
        tt.push([rows,
                '<span class="txns", data-itemid="' + ids + '" data-uid="' + res['id'] + '">' + res['name'] + ' ( ' + ids + ' )</span>',
                1,
                res['sale_price'],
                res['sale_price']],
                {'class' : 'txn_trs'});
    }
    elts = $$(".txns");
    var tot = 0;
    for (var i = 0; i < elts.length; i++)
        tot += elts[i].parentNode.parentNode.childNodes[4].get('html').toInt();
    $('total').set('html', 'Total: ' + tot);
}

window.fifa6 = function(e) {
    e.stop();
    if($('stock_barcode').get('value') == "" ||
       $('stock_quantity').get('value') == "" ||
       $('stock_mprice').get('value') == "" ||
       $('stock_sprice').get('value') == "" ||
       $('stock_rprice').get('value') == "") {
        $('message2').set('html', 'Invalid input');
        (function(){$('message2').set('html', "");}).delay(2000);
    }
    if ($(this).get('data-itemid') == "")
        return;
    var req = new Request({
        method: 'post',
        url: 'newItem',
        data: { 'itemid' : $(this).get('data-itemid'),
                'barcode' : $('stock_barcode').get('value'),
                'quantity' : $('stock_quantity').get('value'),
                'mprice' : $('stock_mprice').get('value'),
                'sprice' : $('stock_sprice').get('value'),
                'rprice' : $('stock_rprice').get('value')},
        onSuccess: function(res) {
            if(res == 'already') {
                $('message2').set('html', 'Same barcode Exists');
                (function(){$('message2').set('html', "");}).delay(2000);
                return;
            }
            $('message2').set('html', 'Recorded Successfully');
            $('stock_barcode').set('value', "");
            $('stock_quantity').set('value', "");
            $('stock_mprice').set('value', "");
            $('stock_sprice').set('value', "");
            $('stock_rprice').set('value', "");
            (function(){$('message2').set('html', "");}).delay(2000);
        }
    }).send();
}

window.fifa5 = function(e) {
    e.stop();
    console.log($(this).get("data-name"));
    $('stock_name').set('html', $(this).get("data-name"));
    $('bStock').set('data-itemid', $(this).get("data-itemid"));
};

window.fifa4 = function(e) {
    e.stop();
    var duration = $(this).get('id') == "top1" ? 0 : 10;
    var ff = duration == 0 ? $('top1').getSelected()[0].get('data-flag') : $('top2').getSelected()[0].get('data-flag');
    var req = new Request({
        method: 'get',
        url: 'toptop',
        data: {'duration' : duration,
               'flag' : ff},
        onSuccess: function(res) {
            if(duration == 0)
                $('top1_tbody').set('html', res);
            else
                $('top2_tbody').set('html', res);
        }
    }).send();
};

window.fifa3 = function(e) {
    e.stop();
    var req = new Request({
        method: 'post',
        url: 'newUserReg',
        data: {'type' : $('new_type').getSelected()[0].get('data-flag'),
               'userid': $('new_userid').get('value'),
               'passwd': $('new_passwd').get('value')},
        onComplete: function(res) {
            if(res == "success") {
                $('message').set('html', "Registration Successful");
                $('new_userid').set('value', '');
                $('new_passwd').set('value', '');
            }
            else
                $('message').set('html', "Invalid");
            (function(){$('message').set('html', "");}).delay(2000);
        }
    }).send();
};

window.fifa2 = function(e) {
    e.stop();
    var tmp = $(this).parentNode.parentNode.childNodes[8].childNodes[0].get('value');
    var tmp2 = $(this).get("data-itemid");
    var req = new Request({
        method: 'get',
        url: 'changePrice',
        data: {'id' : tmp2, 'price': tmp},
        onComplete: function(res) {
            if(res == "notagain")
                $('message').set('html', "Change of price allowed only once a day");
            else if(res == "less")
                $('message').set('html', "Sale price cannot be less than real price");
            else
                $('message').set('html', "Successfully changed");
            (function(){$('message').set('html', "");}).delay(2000);
        }
    }).send();
};

window.fifa = function(e) {
    e.stop();
    var SM = new SimpleModal({"width":700, "height":300});
    var id = $(this).get('data-itemid');
    SM.addButton("OK", "btn primary", function() {
        this.hide();
    });
    SM.addButton("Close", "btn");
    SM.show({
        "model":"modal-ajax",
        "title":"Item Information",
        "param":{
            "url":"/itemInfo/" + id,
            "onRequestComplete": function() {
                $$(".help_fuji").addEvent("click", window.fifa2);
                $$(".bStats").addEvent('click', window.poo1);
            }
        }
    });
};

$$("span.info_span").addEvent("click", window.fifa);
$$("span.info_search").addEvent("click", window.fifa);

window.lol1 = function(e) {
    try {e.stop();} catch(ex) {}
    var req = new Request({
        method: 'get',
        url: 'searchItem',
        data: {'term' : $$("#search_input").get('value')[0]},
        onComplete: function(res) {
            $('search_tbody').set('html', res);
            $$("span.info_search").addEvent("click", window.fifa);
            try{ $$('.add_search').addEvent('click', window.fifa5); } catch(e) {}
        }
    }).send();
};

$$("#search").addEvent("click", window.lol1);

$('addUser').addEvent('click', function(e) {
    e.stop();
    var SM = new SimpleModal({"width":600});
    SM.addButton("Close", "btn");
    SM.show({
        "model":"modal-ajax",
        "title":"New User Registration",
        "param":{
            "url":"/newUser",
            "onRequestComplete": function() {
                $$("#bnew").addEvent("click", window.fifa3);
            }
        }
    });
});

$('top1').addEvent('change', window.fifa4);
$('top2').addEvent('change', window.fifa4);

$$('.add_search').addEvent('click', window.fifa5);
$('bStock').addEvent('click', window.fifa6);
$('bItem').addEvent('click', function(e) {
    e.stop();
    var req = new Request({
        method: 'post',
        url: 'newSItem',
        data: {'name' : $("item_name").get('value')},
        onSuccess: function(res) {
            $('message3').set('html', 'Recorded Successfully');
            $("item_name").set('value', "");
            (window.lol1).delay(0);
            (function(){$('message3').set('html', "");}).delay(2000);
        }
    }).send();
});

$('register').addEvent('click', function(e) {
    e.stop();
    var req = new Request({
        method: 'get',
        url: 'regItem',
        data: {'bc' : $("barcode").get('value')},
        onSuccess: function(res) {
            $("barcode").set('value', "");
            $("barcode").focus();
            addTxn(JSON.parse(res));
        }
    }).send();
});

$('print').addEvent('click', function(e) {
    e.stop();
    var vals = {};
    var tt = $$('.txn_trs');
    for (var i = 0; i < tt.length; i ++) {
        var id = tt[i].childNodes[1].childNodes[0].get('data-uid');
        console.log(id);
        var ghj = tt[i].childNodes[2].get('html');
        vals[id] = ghj;
        console.log(ghj);
    }
    var req = new Request({
        method: 'post',
        url: 'updateRecords',
        data: {'vals' : vals},
        onSuccess: function(res) {
            var ttp = new HtmlTable($('txns_table'));
            ttp.empty();
            $('total').set('html', 'Total: 0');
        }
    }).send();
})

$('cancel_txn').addEvent('click', function(e) {
    e.stop();
    new HtmlTable($('txns_table')).empty();
});

});