from copy import copy
import math
import pandas as pd
import jinja2
import math
# import calendar
from datetime import timedelta
import numpy as np
from chart_generators.bar_generators import BarGenerators
from chart_generators.contour_generators import ContourGenerator
from chart_generators.scatter_plot_generators import ScatterGenerators
from chart_generators.histogram_generators import HistogramGenerators
# from chart_generators.boxplot_generators import BoxplotGenerators



class Report_Plotter():
    def __init__(self, output_path, xls_location):
        self.output_path = output_path
        self.xls_location = xls_location
        self.df = None


    def generate_report(self):
        self.load_data()
        self.generate_duration_timedeltas()
        self.generate_profitable_duration_timedeltas()
        self.build_html_report()
    

    #* Load data from excel into dataframes
    def load_data(self):
        self.df = pd.read_excel(self.xls_location, sheet_name='trade_data')  
        


    def generate_trade_action_chart(self):
        action_type_counts = self.df['Action'].value_counts().rename_axis('Action').reset_index(name='Count')
        chart_params = {
            'data' : action_type_counts,
            'title' : 'Total Trades by Action',
            'x' : action_type_counts['Action'],
            'y' : action_type_counts['Count'],
            'barmode' : None,
            'labels' : None,
            'showlegend' : True,
            'width': 700,
            'colorseperator': 'Action',
        }
        return BarGenerators().generate_bar_chart(chart_params)



    def generate_trade_assets_chart(self):
        asset_counts = self.df['Symbol'].value_counts().rename_axis('Symbol').reset_index(name='Count')
        chart_params = {
            'data' : asset_counts,
            'title' : 'Total Trades By Asset',
            'x' : asset_counts['Symbol'],
            'y' : asset_counts['Count'],
            'barmode' : None,
            'labels' : None,
            'showlegend' : False,
            'width': 700,
            'colorseperator': 'Symbol',
        }
        return BarGenerators().generate_bar_chart(chart_params)




    def generate_duration_timedeltas(self):
        self.df['Duration Delta'] = ''
        self.df['Duration Seconds'] = ''
        for i, row in self.df.iterrows():
            print(i, ' ', row)
            try:
                duration_value = row['Duration (DD:HH:MM:SS)']
                index = duration_value.find(':')
                days = int(duration_value[:index])
                hours = int(duration_value[index+1:index+3])
                minutes = int(duration_value[index+4:index+6])
                seconds = int(duration_value[index+7:])
                time_delta = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
                self.df.at[i, 'Duration Delta'] = time_delta
                self.df.at[i, 'Duration Seconds'] = time_delta.total_seconds()
            except:
                print(i, row)
                raise Exception("Did you forget to delete the open trades from the spreadsheet?")

        self.df['Duration Seconds'] = self.df['Duration Seconds'].astype(float)
        def convert_sec_to_hrs(x):
            return ((x/60)/60).round(2)
        self.df['Duration (Hours)'] = self.df['Duration Seconds'].transform(convert_sec_to_hrs)

    def generate_profitable_duration_timedeltas(self):
        self.df['Profitable Duration Delta'] = ''
        self.df['Profitable Duration Seconds'] = ''
        for i, row in self.df.iterrows():
            duration_value = row['Profitable(time duration)']

            if isinstance(duration_value, str):
                duration_value.replace(' ', '')

                days_index = duration_value.find('d')
                if days_index >= 0: 
                    days = int(duration_value[0:days_index])
                else:
                    days = 0

                hours_index = duration_value.find('h')
                if hours_index >= 0: 
                    if days_index >= 0:
                        hours = int(duration_value[days_index+1:hours_index])
                    else:
                        hours = int(duration_value[0:hours_index])
                else:
                    hours = 0

                minutes_index = duration_value.find('m')
                if minutes_index >= 0: 
                    if hours_index >= 0:
                        minutes = int(duration_value[hours_index+1:minutes_index])
                    elif days_index >= 0:
                        minutes = int(duration_value[days_index+1:minutes_index])
                    else:
                        minutes = int(duration_value[0:minutes_index])
                else:
                    minutes = 0

                time_delta = timedelta(days=days, hours=hours, minutes=minutes)
                self.df.at[i, 'Profitable Duration Delta'] = time_delta
                self.df.at[i, 'Profitable Duration Seconds'] = time_delta.total_seconds()
            else: # If value was null/nan enter it as 0
                self.df.at[i, 'Profitable Duration Delta'] = '0'
                self.df.at[i, 'Profitable Duration Seconds'] = '0'

        self.df['Profitable Duration Seconds'] = self.df['Profitable Duration Seconds'].astype(float)
        def convert_sec_to_hrs(x):
            return ((x/60)/60).round(2)
        self.df['Profitable Duration (Hours)'] = self.df['Profitable Duration Seconds'].transform(convert_sec_to_hrs)





    def generate_mean_duration_by_action_chart(self):
        copy_df = self.df[['Action','Duration Seconds']].copy()
        means = copy_df.groupby('Action').mean()
        means.reset_index(inplace=True)

        def convert_sec_to_hrs(x):
            return ((x/60)/60).round(2)

        means['Mean Duration (Hours)'] = means['Duration Seconds'].transform(convert_sec_to_hrs)

        chart_params = {
            'data' : means,
            'title' : 'Mean Trade Duration by Action',
            'x' : means['Action'],
            'y' : means['Mean Duration (Hours)'],
            'barmode' : None,
            'labels' : None,
            'showlegend' : True,
            'width': 700,
            'colorseperator': 'Action',
        }
        return BarGenerators().generate_bar_chart(chart_params)



    def generate_sd_by_action_chart(self):
        copy_df = self.df[['Action','Duration Seconds']].copy()
        sd = copy_df.groupby('Action').std().round(2)
        sd.reset_index(inplace=True)
        sd.rename({"Duration Seconds": "Standard Deviation Seconds"}, axis=1, inplace=True)

        def convert_sec_to_hrs(x):
            return ((x/60)/60).round(2)

        sd['Standard Deviation (Hours)'] = sd['Standard Deviation Seconds'].transform(convert_sec_to_hrs)

        chart_params = {
            'data' : sd,
            'title' : 'Standard Deviation Trade Duration by Action',
            'x' : sd['Action'],
            'y' : sd['Standard Deviation (Hours)'],
            'barmode' : None,
            'labels' : None,
            'showlegend' : True,
            'width': 700,
            'colorseperator': 'Action',
        }
        return BarGenerators().generate_bar_chart(chart_params)



    def generate_mean_duration_by_asset_chart(self):
        copy_df = self.df[['Symbol','Duration Seconds']].copy()
        means = copy_df.groupby('Symbol').mean()
        means.reset_index(inplace=True)

        def convert_sec_to_hrs(x):
            return round((x / 60) / 60, 2)


        means['Mean Duration (Hours)'] = means['Duration Seconds'].transform(convert_sec_to_hrs)

        chart_params = {
            'data' : means,
            'title' : 'Mean Trade Duration by Symbol',
            'x' : means['Symbol'],
            'y' : means['Mean Duration (Hours)'],
            'barmode' : None,
            'labels' : None,
            'showlegend' : False,
            'width': 1200,
            'colorseperator': 'Symbol'
        }
        return BarGenerators().generate_bar_chart(chart_params)



    def calculate_standard_deviations_by_asset(self):
        copy_df = self.df[['Symbol','Duration Seconds']].copy()
        sd = copy_df.groupby('Symbol').std().round(2)
        sd.reset_index(inplace=True)
        sd.rename({"Duration Seconds": "Standard Deviation Seconds"}, axis=1, inplace=True)

        def convert_sec_to_hrs(x):
            return ((x/60)/60).round(2)

        sd['Standard Deviation (Hours)'] = sd['Standard Deviation Seconds'].transform(convert_sec_to_hrs)
        return sd



    def generate_sd_by_asset_chart(self):
        sd = self.calculate_standard_deviations_by_asset()

        chart_params = {
            'data' : sd,
            'title' : 'Standard Deviation Trade Duration by Symbol',
            'x' : sd['Symbol'],
            'y' : sd['Standard Deviation (Hours)'],
            'barmode' : None,
            'labels' : None,
            'showlegend' : False,
            'width': 1200,
            'colorseperator': 'Symbol',
        }
        return BarGenerators().generate_bar_chart(chart_params)



    def generate_trade_times_scatter_by_asset(self):
        copy_df = self.df[['Symbol','Duration (Hours)']].copy()
        copy_df.sort_values(by=['Symbol'], inplace=True)

        chart_params = {
            'data' : copy_df,
            'title' : 'Trades Duration by Symbol',
            'x' : copy_df['Symbol'],
            'y' : copy_df['Duration (Hours)'],
            'labels' : None,
            'showlegend' : True,
            'width': 1200,
            'colorseperator': 'Symbol',
        }
        return ScatterGenerators().generate_scatter_plot(chart_params)



    def generate_trade_duration_variance_by_asset(self):
        copy_df = self.df[['Symbol','Duration (Hours)']].copy()
        var_df = copy_df.groupby('Symbol').var().round(2)
        var_df.reset_index(inplace=True)
        var_df.rename({'Duration (Hours)': 'Duration Variance'}, axis=1, inplace=True)
        
        chart_params = {
            'data' : var_df,
            'title' : 'Trade Duration Variance by Symbol',
            'x' : var_df['Symbol'],
            'y' : var_df['Duration Variance'],
            'barmode' : None,
            'labels' : None,
            'showlegend' : False,
            'width': 1200,
            'colorseperator': 'Symbol',
        }
        return BarGenerators().generate_bar_chart(chart_params)



    def count_trades_with_duration_exceeding_mean_by_asset(self):
        copy_df = self.df[['Symbol','Duration (Hours)']].copy()

        mean_counts_df = copy_df.groupby(['Symbol']).agg(lambda x: (x > x.mean()).sum())
        mean_counts_df.reset_index(inplace=True)
        mean_counts_df.rename({'Duration (Hours)': 'Trades Exceeding Mean Duration'}, axis=1, inplace=True)

        sd_counts_df = copy_df.groupby(['Symbol']).agg(lambda x: (x > x.std()).sum())
        sd_counts_df.reset_index(inplace=True)
        sd_counts_df.rename({'Duration (Hours)': 'Trades Above 1 SD Duration'}, axis=1, inplace=True)

        trade_counts_df = copy_df.groupby(['Symbol']).size().reset_index(name='Total Trade Count')

        result = pd.concat([mean_counts_df, sd_counts_df['Trades Above 1 SD Duration'], trade_counts_df['Total Trade Count']], axis=1)

        chart_params = {
            'data' : result,
            'title' : 'Trade Counts vs Outlier Counts',
            'x' : result['Symbol'],
            'y' : result['Total Trade Count'],
            'y2' : result['Trades Above 1 SD Duration'],
            'y3' : result['Trades Exceeding Mean Duration'],
            'barmode' : 'group',
            'labels' : None,
            'showlegend' : True,
            'width': 1200,
            'colorseperator': None
        }
        
        return BarGenerators().generate_custom_multibar_chart(chart_params)


    def generate_trade_drawdown_scatter_by_asset(self):
        copy_df = self.df[['Symbol','Drawdown']].copy()
        copy_df.sort_values(by=['Symbol'], inplace=True)

        chart_params = {
            'data' : copy_df,
            'title' : 'Trade Drawdown by Symbol',
            'x' : copy_df['Symbol'],
            'y' : copy_df['Drawdown'],
            'labels' : None,
            'showlegend' : True,
            'width': 1200,
            'colorseperator': 'Symbol',
        }
        return ScatterGenerators().generate_scatter_plot(chart_params)


    def generate_trade_drawdown_scatter_by_profit(self):
        copy_df = self.df[['Profit','Drawdown']].copy()
        copy_df.sort_values(by=['Profit'], inplace=True)

        chart_params = {
            'data' : copy_df,
            'title' : 'Trade Drawdown by Profit',
            'x' : copy_df['Profit'],
            'y' : copy_df['Drawdown'],
            'labels' : None,
            'showlegend' : True,
            'width': 1200,
            'colorseperator': 'Profit',
        }
        return ScatterGenerators().generate_scatter_plot(chart_params)


    def generate_trade_drawdown_scatter_by_duration(self):
        copy_df = self.df[['Duration (Hours)','Drawdown']].copy()
        copy_df.sort_values(by=['Duration (Hours)'], inplace=True)

        chart_params = {
            'data' : copy_df,
            'title' : 'Trade Drawdown by Duration (Hours)',
            'x' : copy_df['Duration (Hours)'],
            'y' : copy_df['Drawdown'],
            'labels' : None,
            'showlegend' : True,
            'width': 1200,
            'colorseperator': 'Duration (Hours)',
        }
        return ScatterGenerators().generate_scatter_plot(chart_params)

    def generate_trade_drawdown_scatter_by_profitable_time(self):
        copy_df = self.df[['Profitable Duration (Hours)','Drawdown']].copy()
        copy_df.sort_values(by=['Profitable Duration (Hours)'], inplace=True)

        chart_params = {
            'data' : copy_df,
            'title' : 'Trade Drawdown by Profitable Duration (Hours)',
            'x' : copy_df['Profitable Duration (Hours)'],
            'y' : copy_df['Drawdown'],
            'labels' : None,
            'showlegend' : True,
            'width': 1200,
            'colorseperator': 'Profitable Duration (Hours)',
        }
        return ScatterGenerators().generate_scatter_plot(chart_params)

    
    def build_html_report(self): # Obtain Template
        templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "myfxbook_report_template.html"
        template = templateEnv.get_template(TEMPLATE_FILE)
        self.inject_html_data(template)

    
    # #* Inject Data into HTML Template
    def inject_html_data(self, template): # Populate Template
        output_html= template.render(
    #         #! Report Text:
    #         system_name = self.get_system_name(),
    #         #! Report Charts:
            fig1_jpeg = self.generate_trade_action_chart(),
            fig2_jpeg = self.generate_trade_assets_chart(),
            fig3_jpeg = self.generate_mean_duration_by_action_chart(),
            fig4_jpeg = self.generate_sd_by_action_chart(),
            fig5_jpeg = self.generate_mean_duration_by_asset_chart(),
            fig6_jpeg = self.generate_sd_by_asset_chart(),
            fig7_jpeg = self.generate_trade_times_scatter_by_asset(),
            fig8_jpeg = self.generate_trade_duration_variance_by_asset(),
            fig9_jpeg = self.count_trades_with_duration_exceeding_mean_by_asset(),
            fig10_jpeg = self.generate_trade_drawdown_scatter_by_asset(),
            fig11_jpeg = self.generate_trade_drawdown_scatter_by_profit(),
            fig12_jpeg = self.generate_trade_drawdown_scatter_by_duration(),
            fig13_jpeg = self.generate_trade_drawdown_scatter_by_profitable_time(),
        ) 

        with open(self.xls_location[:-5] + '.html', "w") as f:
            f.write(output_html)

