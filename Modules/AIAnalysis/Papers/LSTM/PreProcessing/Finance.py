from sklearn.preprocessing import RobustScaler
import pandas as pd


class FinancePreProcessing:
    @classmethod
    def process(cls, balance_sheet, income_statement, cash_flow) -> pd.DataFrame:
        stability = cls.analysis_stability(balance_sheet, income_statement)
        profitability = cls.analysis_profitability(income_statement, cash_flow)
        financial_power = cls.analysis_financial_power(cash_flow, income_statement)

        pre_processed_data = pd.concat([stability, profitability, financial_power], axis=1, join='inner')
        cls.scalar_normalize(pre_processed_data)
        return pre_processed_data

    @staticmethod
    def transform_df(df):
        transed_df = df.T
        transed_df.columns = transed_df.iloc[0]
        transed_df = transed_df.iloc[1:]
        return transed_df

    @staticmethod
    def analysis_stability(balance_sheet, income_statement) -> pd.DataFrame:
        liquidity_ratio = balance_sheet['Current Assets'] / balance_sheet['Current Liabilities']
        current_accounting_ratio = (balance_sheet['Cash And Cash Equivalents'] + balance_sheet['Accounts Receivable'] \
                                    - balance_sheet['Inventory']) \
                                   / balance_sheet['Current Liabilities']
        _cash_and_equivalents = (balance_sheet['Cash And Cash Equivalents'] +
                                 balance_sheet['Cash Cash Equivalents And Short Term Investments'] +
                                 balance_sheet['Cash Equivalents'] +
                                 balance_sheet['Cash Financial'] +
                                 balance_sheet['Other Short Term Investments'])
        short_term_liquidity = _cash_and_equivalents / income_statement['Total Revenue'] * 12
        equity_capital_ratio = balance_sheet['Stockholders Equity'] / balance_sheet['Total Assets']
        retained_earnings = balance_sheet['Retained Earnings']
        # asset_turnover_ratio = income_statement['Total Revenue'] / balance_sheet['Total Assets']
        # accounts_receivable_turnover = balance_sheet['Accounts Receivable'] / income_statement['Total Revenue']
        # inventory_to_receivables_ratio = balance_sheet['Inventory'] / balance_sheet['Accounts Receivable']

        stability = pd.DataFrame({
            'liquidity ratio': liquidity_ratio,
            'current accounting ratio': current_accounting_ratio,
            'short term liquidity': short_term_liquidity,
            'equity capital ratio': equity_capital_ratio,
            'retained earnings': retained_earnings,
            #         'asset turnover ratio': asset_turnover_ratio,
            #         'accounts receivable turnover': accounts_receivable_turnover,
            #         'inventory to receivables ratio': inventory_to_receivables_ratio
        })
        return stability

    @staticmethod
    def analysis_profitability(income_statement, cash_flow) -> pd.DataFrame:
        total_revenue = income_statement['Total Revenue']
        gross_profit = income_statement['Gross Profit']
        cost_revenue_ratio = income_statement['Cost Of Revenue'] / income_statement['Total Revenue']
        sgna_ratio = income_statement['Selling General And Administration'] / income_statement['Total Revenue']
        operating_income_ratio = income_statement['Operating Income'] / income_statement['Total Revenue']
        other_non_operating_income_expenses = income_statement['Other Non Operating Income Expenses']

        profitability = pd.DataFrame({
            'total revenue': total_revenue,
            'gross profit': gross_profit,
            'cost revenue ratio': cost_revenue_ratio,
            'sgna ratio': sgna_ratio,
            'operating income ratio': operating_income_ratio,
            'other non operating income expenses': other_non_operating_income_expenses
        })
        return profitability

    @staticmethod
    def analysis_financial_power(cash_flow, income_statement) -> pd.DataFrame:
        cash_flow.to_csv('./check.csv')
        operating_cash_flow_ratio = cash_flow['Operating Cash Flow'] / income_statement['Total Revenue']
        future_investment = cash_flow['Capital Expenditure'] - income_statement['Reconciled Depreciation']
        cash_flow_sufficiency = cash_flow['Operating Cash Flow'] > abs(cash_flow['Investing Cash Flow'])
        ebitda = income_statement['EBITDA']
        # (ticker.info.get('marketCap', None) + Total Debt) / EBITDA

        financial_power = pd.DataFrame({
            'operating cash flow ratio': operating_cash_flow_ratio,
            'future investment': future_investment,
            'cash flow sufficiency': cash_flow_sufficiency,
            'ebitda': ebitda
        })
        return financial_power

    @staticmethod
    def scalar_normalize(data):
        scaler = RobustScaler()
        scaler.fit(data)
        data = scaler.transform(data)
