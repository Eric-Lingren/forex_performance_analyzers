from copy import copy
import pandas as pd
import jinja2
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
        # self.trades_data_df = None
        # self.summary_data_df = None
        # self.trades_duration_dataset = None
        # self.account_balance_df = None
        # self.monthly_trades_df = None
        # self.monthly_order_types_df = None
        # self.monthly_profits_df = None


    def generate_report(self):
        self.load_data()
        self.generate_duration_timedeltas()
        # self.generate_account_balance_df()
        # self.generate_monthly_trades_df()
        # self.generate_monthly_profits_df()
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
            duration_value = row['Duration (DD:HH:MM:SS)']
            index = duration_value.find(':')
            days = int(duration_value[:index])
            hours = int(duration_value[index+1:index+3])
            minutes = int(duration_value[index+4:index+6])
            seconds = int(duration_value[index+7:])
            time_delta = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
            self.df.at[i, 'Duration Delta'] = time_delta
            self.df.at[i, 'Duration Seconds'] = time_delta.total_seconds()

        self.df['Duration Seconds'] = self.df['Duration Seconds'].astype(float)
        def convert_sec_to_hrs(x):
            return ((x/60)/60).round(2)
        self.df['Duration (Hours)'] = self.df['Duration Seconds'].transform(convert_sec_to_hrs)

        # def convert_sec_to_hrs(x):
        #         return ((x/60)/60).round(2)
        # self.df['Duration Hours'] = ''
        # self.df['Duration Hours'] = self.df['Duration Seconds'].transform(convert_sec_to_hrs)
        # print(self.df.head())




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
        # print(sd)

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
            return ((x/60)/60).round(2)

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
            # fig7_jpeg = self.generate_sd_vs_mean_by_asset_chart(),
    #         fig2_jpeg = self.generate_heatmap({
    #             'data' : self.trades_duration_dataset,
    #             'x' : 'Duration (hrs)',
    #             'y' : 'Profit',
    #             'nbinsx' : 50,
    #             'nbinsy' : 20
    #         }),
    #         fig4_jpeg = self.generate_2d_histogram_contour({
    #             'x' : self.trades_duration_dataset['Duration (hrs)'],
    #             'y' : self.trades_duration_dataset['Profit'],
    #         }),
    #         # fig6_jpeg = self.generate_density_contour({
    #         #     'data' : self.trades_duration_dataset,
    #         #     'x' : self.trades_duration_dataset['Duration (hrs)'],
    #         #     'y' : self.trades_duration_dataset['Profit'],
    #         # }),
    #         fig6_jpeg = self.generate_histogram({
    #             'data' : self.trades_duration_dataset,
    #             'x' : 'Duration (hrs)',
    #             'nbins' : 20,
    #         }),
        ) 

        with open(self.xls_location[:-5] + '.html', "w") as f:
            f.write(output_html)







        # chart_params = {
        #     'data' : copy_df,
        #     'title' : 'Total Trades by Action',
        #     'x' : copy_df['Action'],
        #     # 'y' : copy_df['Count'],
        #     'y' : copy_df['Duration Seconds'],
        #     'labels' : None,
        #     'showlegend' : True,
        #     'width': 700,
        #     'colorseperator': 'Action',
        # }
        # return BoxplotGenerators().generate_boxplot_chart(chart_params)


    # def get_system_name(self):
    #     system_name = self.summary_data_df.loc[self.summary_data_df['Key'] == 'System Name']
    #     return system_name.iloc[0]['Value']
    
    # def get_equity(self):
    #     symbol_data = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Symbol']
    #     return symbol_data.iloc[0]['Value']
    
    # def get_period(self):
    #     period_data = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Period']
    #     return period_data.iloc[0]['Value']

    # def get_duration(self):
    #     duration_data = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Duration']
    #     return duration_data.iloc[0]['Value']

    # def get_bars(self):
    #     bars_data = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Bars in test']
    #     return bars_data.iloc[0]['Value']
    
    # def get_ticks_modeled(self):
    #     ticks_modeled_data = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Ticks modelled']
    #     return ticks_modeled_data.iloc[0]['Value']
    
    # def get_modeling_quality(self):
    #     modelling_quality_data = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Modelling quality']
    #     return modelling_quality_data.iloc[0]['Value']

    # def get_mismatched_chart_errors(self):
    #     mismatched_charts_errors = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Mismatched charts errors']
    #     return mismatched_charts_errors.iloc[0]['Value']

    # def get_gross_profit(self):
    #     gross_profit = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Gross profit']
    #     return gross_profit.iloc[0]['Value']

    # def get_gross_loss(self):
    #     gross_loss = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Gross loss']
    #     return gross_loss.iloc[0]['Value']

    # def get_net_profit(self):
    #     net_profit = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Total net profit']
    #     return net_profit.iloc[0]['Value']

    # def get_absolute_drawdown(self):
    #     absolute_drawdown = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Absolute drawdown']
    #     return absolute_drawdown.iloc[0]['Value']

    # def get_max_drawdown(self):
    #     maximal_drawdown = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Maximal drawdown']
    #     return  maximal_drawdown.iloc[0]['Value']

    # def get_relative_drawdown(self):
    #     relative_drawdown = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Relative drawdown']
    #     relative_drawdown_value = relative_drawdown.iloc[0]['Value']
    #     slice_index = relative_drawdown_value.find('(')
    #     relative_drawdown_dollar = relative_drawdown_value[slice_index+1:-1]
    #     relative_drawdown_percent = relative_drawdown_value[:slice_index-1]
    #     return relative_drawdown_dollar + ' (' + relative_drawdown_percent + ')'
    
    # def get_total_positions_count(self):
    #     total_trades = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Total trades']
    #     return total_trades.iloc[0]['Value']
    
    # def get_short_postions_count(self):
    #     short_positions = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Short positions (won %)']
    #     return short_positions.iloc[0]['Value']

    # def get_long_postions_count(self):
    #     long_positions = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Long positions (won %)']
    #     return long_positions.iloc[0]['Value']
    
    # def get_largest_profitable_trade(self):
    #     largest_profit_trade = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Largest profit trade']
    #     return largest_profit_trade.iloc[0]['Value']
    
    # def get_largest_unprofitable_trade(self):
    #     largest_loss_trade = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Largest loss trade']
    #     return largest_loss_trade.iloc[0]['Value']

    # def get_average_profit_per_trade(self):
    #     average_profit_trade = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Average profit trade']
    #     return  average_profit_trade.iloc[0]['Value']
    
    # def get_average_loss_per_trade(self):
    #     average_loss_trade = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Average loss trade']
    #     return average_loss_trade.iloc[0]['Value']
    
    # def get_max_consecutive_wins(self):
    #     max_consecutive_wins = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Maximum consecutive wins (profit in money)']
    #     return max_consecutive_wins.iloc[0]['Value']

    # def get_max_consecutive_losses(self):
    #     max_consecutive_losses = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Maximum consecutive losses (loss in money)']
    #     return max_consecutive_losses.iloc[0]['Value']

    # def get_max_consecutive_profit_amt(self):
    #     max_consecutive_profit = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Maximal consecutive profit (count of wins)']
    #     return max_consecutive_profit.iloc[0]['Value']
    
    # def get_max_consecutive_loss_amt(self):
    #     max_consecutive_loss = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Maximal consecutive loss (count of losses)']
    #     return  max_consecutive_loss.iloc[0]['Value']

    # def get_avg_consecutive_win_count(self):
    #     average_consecutive_wins = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Average consecutive wins']
    #     return average_consecutive_wins.iloc[0]['Value']

    # def get_avg_consecutive_loss_count(self):
    #     average_consecutive_losses = self.summary_data_df.loc[self.summary_data_df['Key'] == 'Average consecutive losses']
    #     return average_consecutive_losses.iloc[0]['Value']