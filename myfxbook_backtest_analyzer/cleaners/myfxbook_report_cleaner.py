import pandas as pd


class Myfxbook_Report_Cleaner():
    def __init__(self, input_file, output_path):
        self.input_file = input_file
        self.output_path = output_path
        self.output_filename = ''
        self.df = None



    def run_cleaner(self):
        self.open_report()
        self.drop_withdrawls_deposits()
        self.drop_unused_columns()
        self.write_data_to_xls()
        return self.output_filename



    def open_report(self):
        col_names = [
            "Tags","Ticket","Open Date",'Close Date', 'Symbol','Action','Units/Lots', 'SL', 'TP', 'Open Price',	'Close Price', 'Commission', 'Swap', 'Pips', 'Profit', 'Gain', 'Comment', 'Magic Number', 'Duration (DD:HH:MM:SS)', 'Profitable(%)', 'Profitable(time duration)', 'Drawdown', 'Risk:Reward', 'Max(pips)', 'Max(USD)', 'Min(pips)', 'Min(USD)', 'Entry Accuracy(%)', 'Exit Accuracy(%)', 'ProfitMissed(pips)', 'ProfitMissed(USD)'
        ]
        self.df = pd.read_csv(self.input_file, engine='python', names=col_names,)
        # self.df = pd.read_csv(self.input_file, engine='python', encoding='utf-8')
        # self.df = pd.read_csv(self.input_file, sep=',', engine='c', encoding='utf-8')
        # self.df = pd.read_csv(self.input_file, encoding='Latin-1', names=col_names, lineterminator='\n')
        # self.df = pd.read_csv(self.input_file, engine='c')
        # self.df = pd.read_csv(self.input_file, engine='python', encoding = "ISO-8859-1")
        # self.df = pd.read_csv(self.input_file, engine='python', encoding = "latin")
        # self.df = pd.read_csv(self.input_file, engine='c', encoding = "ISO-8859-1")
        # with open(self.input_file, encoding='utf-16') as f:
        #     self.df = pd.read_csv(f)
        output_filename = self.input_file.replace('.csv', '-cleaned.xlsx') 
        slice_index = output_filename.rfind('/')
        self.output_filename = self.output_path + output_filename[slice_index:]



    #* Drops all withdrawal and deposit orders to leave only tradesx
    def drop_withdrawls_deposits(self):
        self.df.drop(self.df[self.df['Action'] == 'Deposit'].index, inplace = True)
        self.df.drop(self.df[self.df['Action'] == 'Withdrawal'].index, inplace = True)



    #* Drops all Unused Columns
    def drop_unused_columns(self):
        self.df.drop(['Tags', 'SL', 'TP', 'Commission', 'Swap', 'Comment', 'Magic Number'], axis = 1, inplace = True) 



    # #*  Output the contents of the trade data table in excel format
    def write_data_to_xls(self):
        #  Create a Pandas Excel writer using XlsxWriter as the engine.
        with pd.ExcelWriter(self.output_filename, engine='xlsxwriter') as writer:    
            # Write each dataframe to a different worksheet.
            self.df.to_excel(writer, sheet_name='trade_data', index=False)
    