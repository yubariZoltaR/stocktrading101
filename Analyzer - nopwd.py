import pandas as pd
import pymysql
from datetime import datetime
from datetime import timedelta
import re

class MarketDB:
    def __init__(self):
        """생성자 : MariaDB 연결 및 종목코드 딕셔너리 생성"""
        self.conn = pymysql.connect(host='localhost',user='root',
                                    password="****",db='INVESTAR',charset='utf8')
        self.codes = {}
        self.get_comp_info()


    def __del__(self):
        """소멸자: MariaDB 연결해제"""
        self.conn.close()

    def get_comp_info(self):
        """company_info 테이블에서 읽어와서 codes에 저장"""
        sql = "SELECT * FROM company_info"
        df = pd.read_sql(sql, self.conn)
        for idx in range(len(df)):
            self.codes[df['CODE'].values[idx]] = df['company'].values[idx]

    def get_daily_price(self, code, start_date=None, end_date=None):
        """KRX 종목별 시세를 데이터프레임 형태로 변환
            - code : KRX 종목코드 또는 상장기업명
            - start_date : 조회시작일, 미입력시 1년전 오늘
            - end_date : 조회 종료일, 미입력시 오늘
        """
        if start_date is None:
            one_year_ago = datetime.today() - timedelta(days=365)
            start_date = one_year_ago.strftime('%Y-%m-%d')
            print("start_date is initialized to '{}'".format(start_date))
        else:
            start_lst = re.split('\D+',start_date)
            if start_lst[0] == '':
                start_lst = start_lst[1:]
            start_year = int(start_lst[0])
            start_month = int(statr_lst[1])
            start_day = int(start_lst[2])
            if start_year < 1900 or start_year > 2200:
                print(f"ValueError: start_year({start_year:d}) is wrong.")
                return
            if start_month < 1 or start_month > 12:
                print(f"ValueError: start_month({start_month:d}) is wrong.")
                return
            if start_day < 1 or start_day > 31:
                print(f"ValueError: start_day({start_day:d}) is wrong.")
                return
            start_day=f"{start_year:04d}-{start_month:02d}-{start_day:02d}"

        if (end_date is None):
            end_date = datetime.today().strftime('%Y-%m-%d')
            print("end_date is initialized to '{}'".format(end_date))
        else:
            end_lst = re.split('\D+',end_date)
            if end_lst[0] == '':
                end_lst = end_lst[1:]
            end_year = int(end_lst[0])
            end_month = int(end_lst[1])
            end_day = int(end_lst[2])
            if end_year < 1900 or end_year > 2200:
                print(f"ValueError: end_year({end_year:d}) is wrong.")
                return
            if end_month < 1 or end_month > 12:
                print(f"ValueError: end_month({end_month:d}) is wrong.")
                return
            if end_day < 1 or end_day > 31:
                print(f"ValueError: end_day({end_day:d}) is wrong.")
                return
            end_day=f"{end_year:04d}-{end_month:02d}-{end_day:02d}"

        codes_key = list(self.codes.keys())
        codes_values = list(self.codes.values())
        if code in codes_keys:
            pass
        elif code in codes_values:
            idx = codes_values.index(code)
            code = codes_keys[idx]
        else:
            print("ValueError: Code({}) doesn't exist.".format(code))
        
        sql = f"SELECT * FROM daily_price WHERE code = '{code}'"\
              f" and date >= '{start_date}' and date <= '{end_date}'"
        df = pd.read_sql(sql, sql.conn)
        df.index = df['date']
        return df
    

    
