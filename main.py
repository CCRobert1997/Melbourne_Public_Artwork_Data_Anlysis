# -*- coding: utf-8 -*-
"""
Created on Sat May 14 22:40:37 2016

@author: chenshangyu
"""



import csv
import os
import json
import re
#import cgi
from libforphase3 import *

from collections import defaultdict
from flask import Flask, request


app = Flask(__name__, static_folder='.', static_url_path='')

csvdata = csv.reader(open("Melbourne_Public_Artwork.csv"))
header = csvdata.next()
csvdata = csv.DictReader(open("Melbourne_Public_Artwork.csv"))
data = list(csvdata)

#home html text
@app.route('/home.html', methods=['POST', 'GET'])
def handler():
  html = """<!DOCTYPE html>
  <html lang="en">
              <head>
    <meta charset="utf-8" />
    <title>MELBOURNE PUBLIC ARTWORK</title>
    <script src="jquery.js" type="text/javascript"></script>
    <link href="dom.css" type="text/css" rel="stylesheet" media="screen"/>
    <script type="text/javascript">
          
        function showdataset() {
           var html = '%s'\n%s """
  
    
  html2="""       $('#datashow').html(html);
                  $('#datashow').hide('slow');
	       $('#show_button').hover(
                  function showContent() { $('#datashow').show('slow'); }
           );
	       $('#hide_button').hover(
                  function hideContent() { $('#datashow').hide('slow'); }  
           );
        }

        $(document).ready(showdataset);
        </script>
              </head>
              <body>
      <table id="headertable" width="100%">
       <tr>
        <td width="40%"><h1>Melbourne Public Artwork</h1></td>
        <td align="right"><a href="home.html" id="link">Home</a></td>
        <td align="right"><a href="pivot.html" id="link">￼Pivot Table</a></td>
        <td align="right"><a href="observation.html" id="link">Observations</a></td>
       </tr>
      </table>
      <!--<div id="homepicture"></div>-->
      <img src='homepaper.jpg' width="100%" height="100%"> 
      <div id="footer">
        <input id="show_button" type="button" class="buttomdata" value="Show dataset" />  
        <input id="hide_button" type="button" class="buttomdata" value="Hide dataset" /> 
      </div>
      <div id="datashow">
      </div>
              </body>
            </html>"""
   
   
  
  table = '<table><tr>'
  for attributes in header:
        table = table + '<td>%s</td>'%attributes
  table = table + '</tr>'
  for row in data:
      table = table + '<tr>'
      for attributes in header:
            addthing = row[attributes]
            addthing = quotforjavascript(addthing)
            table = table + '<td>%s</td>'%(addthing)
      table = table + '</tr>'
  table = table + '</table>'
  body = html % (table, html2)
  return body, 200, {'Content-Type': 'text/html'}


#pivot table html page
#get attributes name from csv file and write it as option
def select_attributes_find():
    option = ""
    for attributes in header:
        option = option + """<option value="%s">%s</option>"""%(attributes, attributes)
    return option

#pivot.html text
@app.route("/pivot.html", methods=['POST', 'GET'])
def pivothtml():
    select_attributes = select_attributes_find()
    #print(select_attributes)
    html2 = '''<table id="headertable" width="100%">
  <tr>
      <td width="40%"><h1>Melbourne Public Artwork</h1></td>
    <td align="right"><a href="home.html" id="link">Home</a></td>
      <td align="right"><a href="pivot.html" id="link">Pivot Table</a></td>
      <td align="right"><a href="observation.html" id="link">Observations</a></td>
          </tr>
      </table>
<div>
    <form  method="POST" action="/pivot-table-generator">
        <div><table align="center" width="90%" id="pivot_table_select">
        <tr><td width="50%">
            <div>
            <table align="center">
                <tr><td>Report Filter</td><td></td></tr>
            
            <tr><td>Choose attributes</td>
            <td><select name="Filter_attributes">
            <option value="Northing">Northing</option>
            <option value="Easting">Easting</option>'''
    html3='''</select></td></tr>
            <tr><td>Filter Value Greater Than</td><td><input type="text" name="Filter_value_greater_than"></td></tr>
            <tr><td>Filter Value Less Than</td><td><input type="text" name="Filter_value_less_than"></td></tr>
            <tr><td><font size="1px" color="grey">"note: Input Easting as an integer between 315771 and 323044 Input Northing as an integer between 5810846 and 5817763"</font></td></tr>
        </table></div>
            </td>
            <td width="50%">
            <div><table align="center">
            <tr><td>Row label</td>
            <td><select name="Row_label">'''
    html4='''</select></td></tr>
        </table></div></td></tr>
            <tr height="100px"></tr>
            <tr><td width="50%"><div>
            <table align="center">
                <tr><td>Column label</td>
                <td><select name="Column_label">'''
    html5='''</select></td></tr>
             </table>
                </div>
            </td>
            <td width="50%">
                <div><table align="center">
                    <tr><td>Aggregate</td>
            <td><select name="Aggregate">
            <option value="MAX">Easternmost/Northernmost</option>
            <option value="MIN">Westernmost/Southernmost</option>
            <option value="Count">Count</option>
            <option value="Centre">Centre</option>
            <option value="None">None</option>
            </select></td></tr>
            <tr><td>Value</td>
            <td><select name="Value">
            <option value="Northing">Northing</option>
            <option value="Easting">Easting</option>
            '''
    html = '''<!DOCTYPE html>
<html lang="en">
    <head>
        <title>pivot</title>
        <link href="dom.css" type="text/css" rel="stylesheet" media="screen"/>
    </head>
<body>
%s%s%s%s%s%s
                </select></td></tr>
                </table></div></td></tr>
</table></div>
        <div><table align="center"><tr><td><input id="pivot_table_generate" type="submit" value="Generate Pivot Table"></td></tr></table></div>
                </form>
    </div>
    
</body>
</html>'''%(html2, html3, select_attributes, html4, select_attributes, html5)
                
    return html, 200, {'Content-Type': 'text/html; charset=utf-8'}




#get input value in pivot.html and hand to python
def find_value_for_pivot_table():
  Filter_attributes = request.form['Filter_attributes']
  #Logic_Operator = request.form['Logic_Operator']
  Filter_value_greater_than = request.form['Filter_value_greater_than']
  Filter_value_less_than = request.form['Filter_value_less_than']
  Row_label = request.form['Row_label']
  Column_label = request.form['Column_label']
  Aggregate = request.form['Aggregate']
  Value = request.form['Value']
  if not Filter_value_greater_than:
    if not Filter_value_less_than:
        pivotvar = [Filter_attributes, 0, 100000000, Row_label, Column_label, Aggregate, Value]
    else:
        pivotvar = [Filter_attributes, 0, int(Filter_value_less_than), Row_label, Column_label, Aggregate, Value]
  elif not Filter_value_less_than:
    pivotvar = [Filter_attributes, int(Filter_value_greater_than), 100000000, Row_label, Column_label, Aggregate, Value]
  else:
    pivotvar = [Filter_attributes, int(Filter_value_greater_than), int(Filter_value_less_than), Row_label, Column_label, Aggregate, Value]
  return pivotvar


#respond a pivot table 
@app.route("/pivot-table-generator", methods=['POST', 'GET'])
def pivottable_generate():
  inputvar = find_value_for_pivot_table()
  headtable = """<table id="headertable" width="1100px" align="left">
  <tr>
      <td width="40%"><h1>Melbourne Public Artwork</h1></td>
    <td align="right"><a href="home.html" id="link">Home</a></td>
      <td align="right"><a href="pivot.html" id="link">Pivot Table</a></td>
      <td align="right"><a href="observation.html" id="link">Observations</a></td>
          </tr>
      </table>"""
  tablefrontline = """<table width="100%"><tr><td align="center">"""
  #print("%s %d %d %s %s %s %s\n\n"%(inputvar[0], inputvar[1], inputvar[2], inputvar[3], inputvar[4], inputvar[5], inputvar[6]))
  if inputvar[3]!=inputvar[4] and inputvar[3]!=inputvar[6] and inputvar[4]!=inputvar[6]:
    pivottablehtml = pivot_table(inputvar[0], inputvar[1], inputvar[2], inputvar[3], inputvar[4], inputvar[5], inputvar[6])
    if not pivottablehtml:
        html = '''<!DOCTYPE html>
    <html>    
    <body>
    <p>Please change filter value<p>
    <a href="pivot.html" id="link">Back to ￼Pivot Table</a>
    </body>
    </html>'''
        return html, 200, {'Content-Type': 'text/html; charset=utf-8'}
    html = '''<!DOCTYPE html>
    <html>
    <head>
    <script src="jquery.js" type="text/javascript"></script>
    <link href="dom.css" type="text/css" rel="stylesheet" media="screen"/>
    </head>
    <body id="pivotbody">
    %s
    <div>
    %s
    %s
    </td></tr></table>
    </div>
    </body>
    </html>'''%(tablefrontline, headtable, pivottablehtml)
    #html = pivottablehtml 
  else:
    html = '''<!DOCTYPE html>
    <html>    
    <body>
    <p>Please do not choose same Row_label, Colume_label and Value<p>
    <a href="pivot.html" id="link">Back to ￼Pivot Table</a>
    </body>
    </html>'''
  return html, 200, {'Content-Type': 'text/html; charset=utf-8'}



#chart3 html
@app.route("/chart3.html", methods=['POST', 'GET'])
def chart3_html():
    headtable = """<table id="headertable" width="100%">
  <tr>
      <td width="40%"><h1>Melbourne Public Artwork</h1></td>
    <td align="right"><a href="home.html" id="link">Home</a></td>
      <td align="right"><a href="pivot.html" id="link">￼Pivot Table</a></td>
      <td align="right"><a href="observation.html" id="link">Observations</a></td>
          </tr>
      </table>"""
    html = """<!DOCTYPE html>
<html>
    
    <head>
        <link href="dom.css" type="text/css" rel="stylesheet" media="screen"/>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.3/jquery.min.js"></script>
        <script src="https://code.highcharts.com/highcharts.js"></script>
        <script src="https://code.highcharts.com/modules/data.js"></script>
        <script src="https://code.highcharts.com/modules/drilldown.js"></script>
        </head>
<body>
    %s
    <div id="tablearea" style="min-width: 310px; height: 400px; margin: 0 auto"></div>
    <p>Some suburbs of artworks are not given by the dataset</p>
    <script type="text/javascript">
        $(function () {
          // Create the chart
          $('#tablearea').highcharts({
                                     chart: {
                                     type: 'column'
                                     },
                                     title: {
                                     text: 'Artwork under each Xorg'
                                     },
                                     subtitle: {
                                     text: 'Click the columns to view versions. Source: <a href="https://data.melbourne.vic.gov.au/Assets-Infrastructure/Melbourne-Public-Artwork/6fzs-45an">data.melbourne.vic.gov.au.com</a>.'
                                     },
                                     xAxis: {
                                     type: 'category'
                                     },
                                     yAxis: {
                                     title: {
                                     text: 'Total number of artwork under Xorg'
                                     }
                                     
                                     },
                                     legend: {
                                     enabled: false
                                     },
                                     plotOptions: {
                                     series: {
                                     borderWidth: 0,
                                     dataLabels: {
                                     enabled: true,
                                     format: '{point.y:.0f}'
                                     }
                                     }
                                     },
                                     
                                     tooltip: {
                                     headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                                     pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.0f}</b> artworks of total<br/>'
                                     },
                                     
                                     series: [{
                                              name: 'Xorg',
                                              colorByPoint: true,
                                              data: %s drilldown: {series: [ %s ]
                                              }
                                              });
                                              });
                                              </script>
                                              </body>
        </html>"""%(headtable, main_data_json(), drilldowndata())
    return html, 200, {'Content-Type': 'text/html; charset=utf-8'}




#for coordinates.html
@app.route('/coordinates.json', methods=['POST', 'GET'])
def coordinate():
    main_dict = defaultdict(dict)
    csvdata = list(csv.DictReader(open("Melbourne_Public_Artwork.csv")))
    jsonfile = "["
    address = csvdata[0]["Co-ordinates"]
    spilt_add = address.split(",")
    jsonfile = jsonfile + "[" + spilt_add[1].split(")")[0] + "," + spilt_add[0].split("(")[1] + "]"
    for row in range(1, len(csvdata)):
        address = csvdata[row]["Co-ordinates"]
        spilt_add = address.split(",")
        jsonfile = jsonfile + ", [" + spilt_add[1].split(")")[0] + "," + spilt_add[0].split("(")[1] + "]"
    jsonfile = jsonfile + "]\n"
    return jsonfile, 200, {'Content-Type': 'application/json'}




#for correlation.html
#get attributes name from csv file and write it as option
def select_category_attributes_find():
    option = ""
    for attributesid in range(0, len(header)-3):
        option = option + """<option value="%s">%s</option>"""%(header[attributesid], header[attributesid])
    return option


#correlation.html

@app.route("/correlation.html", methods=['POST', 'GET'])
def correlationpick():
    select_attributes = select_category_attributes_find()
    #print(select_attributes)
    html2 = '''<table id="headertable" width="100%">
  <tr>
      <td width="40%"><h1>Melbourne Public Artwork</h1></td>
    <td align="right"><a href="home.html" id="link">Home</a></td>
      <td align="right"><a href="pivot.html" id="link">Pivot Table</a></td>
      <td align="right"><a href="observation.html" id="link">Observations</a></td>
          </tr>
      </table>
<div>
    <form  method="POST" action="/correlationgraph.html">
        <div><table align="center" width="90%" id="pivot_table_select">
        <tr><td width="50%">
            <table align="center">
                <tr><td>X_axis</td>
            <td><select name="X_axis">'''
    html3='''</select></td></tr>
        </table></div></td><td width="50%">
            <table align="center">
                <tr><td>Compare with</td>
                <td><select name="compare_with">'''
    html4='''</select></td></tr>
             </table>
                </div>
            </td>
            
            '''
    html = '''<!DOCTYPE html>
<html lang="en">
    <head>
        <title>pivot</title>
        <link href="dom.css" type="text/css" rel="stylesheet" media="screen"/>
    </head>
<body>
%s%s%s%s%s
</table></div>
        <div><table align="center"><tr><td><input id="pivot_table_generate" type="submit" value="Generate graph"></td></tr></table></div>
                </form>
    </div>
    
</body>
</html>'''%(html2, select_attributes, html3, select_attributes, html4)
                
    return html, 200, {'Content-Type': 'text/html; charset=utf-8'}


def createjsonforcorrelation():
    X_axis = request.form['X_axis']
    compare_with = request.form['compare_with']
    dictdata = correlation_data(compare_with, X_axis)
    jsondata = """["%s" """%(quotforjavascript(dictdata[1][0]))
    for xelements in range(1, len(dictdata[1])):
        jsondata = jsondata + """,  "%s" """%(quotforjavascript(dictdata[1][xelements]))
    jsondata = jsondata + "]"
    
    jsondataseries = "["
    dictlict = dictdata[0].items()
    attributelist = "[%d"%(dictlict[0][1][dictdata[1][0]])
    for xelements in range(1, len(dictdata[1])):
        attributelist = attributelist + ", %d"%(dictlict[0][1][dictdata[1][xelements]])
    attributelist = attributelist + "]"
    attribute = """{name: "%s", \ndata: %s}"""%(quotforjavascript(dictlict[0][0]), quotforjavascript(attributelist))
    jsondataseries = jsondataseries + attribute
    for parts in range(1, len(dictlict)):
        attributelist = "[%d"%(dictlict[parts][1][dictdata[1][0]])
        for xelements in range(1, len(dictdata[1])):
            attributelist = attributelist + ", %d"%(dictlict[parts][1][dictdata[1][xelements]])
        attributelist = attributelist + "]"
        attribute = """{name: "%s", \ndata: %s}"""%(quotforjavascript(dictlict[parts][0]), quotforjavascript(attributelist))
        jsondataseries = jsondataseries + ", \n" + attribute
    jsondataseries = jsondataseries + "]"
    return [jsondata, jsondataseries]

@app.route("/correlationgraph.html", methods=['POST', 'GET'])
def creategraph():
    html = """<!DOCTYPE html>
<html>
    
<head>
    <link href="dom.css" type="text/css" rel="stylesheet" media="screen"/>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.3/jquery.min.js"></script>
    <script src="https://code.highcharts.com/highcharts-more.js"></script>
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/modules/exporting.js"></script>
    
</head>
<body>
<table id="headertable" width="100%">
  <tr>
      <td width="40%"><h1>Melbourne Public Artwork</h1></td>
    <td align="right"><a href="home.html" id="link">Home</a></td>
      <td align="right"><a href="pivot.html" id="link">Pivot Table</a></td>
      <td align="right"><a href="observation.html" id="link">Observations</a></td>
          </tr>
      </table>
<div id="tablecontainer" style="min-width: 310px; height: 1000px; margin: 0 auto"></div>
<script type="text/javascript">
    $(function () {
      $('#tablecontainer').highcharts({
                                 chart: {
                                 type: 'column',
                                 verticalAlign: 'top'
                                 },
                                 title: {
                                 text: 'Stacked column chart'
                                 },
                                 xAxis: {
                                 categories: """ + createjsonforcorrelation()[0] + """
                                 },
                                 yAxis: {
                                 min: 0,
                                 title: {
                                 text: 'Total'
                                 },
                                 stackLabels: {
                                 enabled: true,
                                 style: {
                                 fontWeight: 'bold',
                                 color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                                 }
                                 }
                                 },
                                 legend: {
                                 align: 'right',
                                 x: 0,
                                 verticalAlign: 'top',
                                 y: 100,
                                 floating: true,
                                 backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || 'white',
                                 borderColor: '#CCC',
                                 borderWidth: 1,
                                 shadow: false
                                 },
                                 tooltip: {
                                 headerFormat: '<b>{point.x}</b><br/>',
                                 pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
                                 },
                                 plotOptions: {
                                 column: {
                                 stacking: 'normal',
                                 dataLabels: {
                                 enabled: true,
                                 color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white',
                                 style: {
                                 textShadow: '0 0 3px black'
                                 }
                                 }
                                 }
                                 },
                                 series: """ + createjsonforcorrelation()[1] + """
                                 });
      });

    
</script>
</body>
</html>"""
    print html
    return html, 200, {'Content-Type': 'text/html; charset=utf-8'}








#persentage for each structure type
@app.route("/chart2.html", methods=['POST', 'GET'])
def chart2_html():
    headtable = """<table id="headertable" width="100%"><tr>
      <td width="40%"><h1>Melbourne Public Artwork</h1></td>
    <td align="right"><a href="home.html" id="link">Home</a></td>
      <td align="right"><a href="pivot.html" id="link">￼Pivot Table</a></td>
      <td align="right"><a href="observation.html" id="link">Observations</a></td>
          </tr>
      </table>"""
    html = """<!DOCTYPE HTML>
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<title>Highcharts Example</title>
        <link href="dom.css" type="text/css" rel="stylesheet" media="screen"/>
		<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
		<style type="text/css">
${demo.css}
		</style>
		<script type="text/javascript">
$(function () {

    $(document).ready(function () {

        // Build the chart
        $('#container').highcharts({
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie'
            },
            title: {
                text: '<b>Percentage of Each Type of Structure</b>'
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: false
                    },
                    showInLegend: true
                }
            },
            series: [{
                name: 'Type Share',
                colorByPoint: true,
                data: [""" + chart2_data_transform() + """]}]
        });
    });
});
		</script>
	</head>
	<body>%s
<script src="https://code.highcharts.com/highcharts.js"></script>
<script src="https://code.highcharts.com/modules/exporting.js"></script>

<div id="container" style="min-width: 310px; height: 600px; max-width: 1500px; margin: 0 auto"></div>%s""" %(headtable,"</body></html>")
    print html
    return html, 200, {'Content-Type': 'text/html; charset=utf-8'}






#chart.html
@app.route("/chart1.html", methods=['POST', 'GET'])
def chart1_html():
    headtable = """<table id="headertable" width="100%">
  <tr>
      <td width="40%"><h1>Melbourne Public Artwork</h1></td>
    <td align="right"><a href="home.html" id="link">Home</a></td>
      <td align="right"><a href="pivot.html" id="link">￼Pivot Table</a></td>
      <td align="right"><a href="observation.html" id="link">Observations</a></td>
          </tr>
      </table>"""


    html = """<!DOCTYPE HTML>
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<title>Highcharts Example</title>
        <link href="dom.css" type="text/css" rel="stylesheet" media="screen"/>
		<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
		<style type="text/css">
${demo.css}
		</style>
		<script type="text/javascript">
$(function () {
    $('#containerchart1').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Each Ten-Year Performance between Suburbs'
        },
        subtitle: {
            text: 'Source: https://data.melbourne.vic.gov.au/Assets-Infrastructure/Melbourne-Public-Artwork/6fzs-45an'
        },
        xAxis: {
            categories: %s,
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Number of Art Works'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [%s]
    });
});
		</script>
    </head>
	<body>%s
        
        
        
        
        
<script src="https://code.highcharts.com/highcharts.js"></script>
<script src="https://code.highcharts.com/modules/exporting.js"></script>

<div id="containerchart1" style="min-width: 450px; height: 600px; margin: 0 auto"></div>

	</body>
</html>"""%(chart1_year(), chart1_data(),headtable)
    return html , 200, {'Content-Type': 'text/html; charset=utf-8'}






if __name__ == "__main__":
    app.run(debug=True)







