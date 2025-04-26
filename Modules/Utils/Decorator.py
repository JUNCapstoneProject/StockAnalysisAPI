import json
import functools
from datetime import datetime
# bridge
from Modules.Utils.Database.Mysql import MysqlConnector
from Modules.Utils.Interfaces.Pipeline import Output

DB_NAME = 'analysis_db'


def memoization(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        memoize = self.memoize
        if len(args) >= 2:  # 위치 인자로 전달된 경우
            data = args[1]
        else:  # 키워드 인자로 전달된 경우
            data = kwargs.get('data', False)

        data = json.dumps(data)
        con = MysqlConnector.connect_db(DB_NAME)
        cur = con.cursor()
        if memoize:
            # 가장 최근에 분석했던 데이터 반환
            query = "SELECT pipeline_id, result " \
                    "FROM analysis_vw " \
                    "WHERE input_module = %s " \
                    "ORDER BY output_time DESC " \
                    "LIMIT 1"
            cur.execute(query, (self.module_name,))
            try:
                pipeline_id, analysis_result = cur.fetchone()
            except TypeError:  # 값이 존재하지 않아 튜플 언패킹 과정에서 TypeError 발생
                raise ValueError('Error in memoize'
                                 '\n: 사전 학습된 데이터가 존재하지 않음')
            else:
                status_code = 200
                message = 'Memoized Data'
                end_time = datetime.now()

        else:
            # 데이터 분석
            start_time = datetime.now()
            # TODO : 다양한 예외 처리하기
            try:
                analysis_result = func(*args, **kwargs)
            except Exception as e:
                print('e :', e)
                status_code = 400
                message = 'Error (need to edit error message)'
                analysis_result = None
            else:
                status_code = 200
                message = 'Success'

            end_time = datetime.now()
            # 분석 결과 저장
            query = "INSERT INTO analysis_logs(input_module, input_data, start_time, end_time, result) " \
                    "VALUES (%s, %s, %s, %s, %s)"
            cur.execute(query, (self.module_name, data, start_time, end_time, analysis_result))
            # 파이프라인 아이디 조회
            cur.execute("SELECT pipeline_id "
                        "FROM analysis_logs "
                        "ORDER BY end_time "  # 분석이 다 끝난 뒤에 INSERT 하므로 end_time 기준 정렬
                        "DESC LIMIT 1")
            pipeline_id = cur.fetchone()[0]

        con.commit()
        cur.close()
        con.close()
        return Output(pipeline_id, end_time.strftime('%Y-%m-%d %H:%M:%S'), status_code, message, analysis_result)

    return wrapper
