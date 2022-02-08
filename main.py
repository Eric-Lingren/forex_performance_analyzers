from myfxbook_backtest_analyzer.myfxbook_app import run_myfxbook
from mt4_backtest_analyzer.mt4_app import run_mt4

def get_user_analyzer_selection():
    choice_options = '\nChoose a Report Type to Analyze:\n\n[1] - MT4\n[2] - MyFxBook\n\n'
    while True:
        try:
            print(choice_options)
            choice = int(input('Selection... '))
        except ValueError:
            print('\nInput not understood. Please try again and enter a number.\n')
            continue
        if choice != 1 and choice != 2: 
            print('\nInvalid Selection. Please try again.')
        else:
            break
    return choice



if __name__ == '__main__':
    choice = get_user_analyzer_selection()
    if choice == 1: 
        run_mt4()
    else:
        run_myfxbook()