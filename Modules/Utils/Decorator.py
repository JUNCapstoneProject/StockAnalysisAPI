import json
import functools
import base64
from datetime import datetime
# bridge
from Modules.Utils.Database.Mysql import MysqlConnector
from Modules.Utils.Interfaces.Pipeline import Output
from Utils.Error.code import *

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
            # 과거 데이터 사용
            pipeline_id, analysis_result = memoize_result(cur, self.module_name)
            status_code = SUCCESS_CODE
            message = 'Memoized Data'
            end_time = datetime.now()
        else:
            # 데이터 분석
            start_time = datetime.now()
            try:
                analysis_result = func(*args, **kwargs)  # @adpater 실행 부분
            except ValueError as e:  # adapter 인자 data 에러
                pipeline_id = None
                end_time = datetime.now()
                status_code = USER_ERR_CODE
                message = str(e)
                analysis_result = None
            except Exception as e:  # 예상하지 못한 에러
                pipeline_id = None
                end_time = datetime.now()
                status_code = SYS_ERR_CODE
                message = str(e)
                analysis_result = None
            else:
                end_time = datetime.now()
                pipeline_id = write_result(cur, self.module_name, data, analysis_result, start_time, end_time)
                status_code = SUCCESS_CODE
                message = 'Success'

        con.commit()
        cur.close()
        con.close()
        return Output(pipeline_id, end_time.strftime('%Y-%m-%d %H:%M:%S'), status_code, message, analysis_result)

    return wrapper


def memoize_result(cur, module_name):
    # 가장 최근에 분석했던 데이터 반환
    query = "SELECT pipeline_id, result " \
            "FROM analysis_vw " \
            "WHERE input_module = %s " \
            "ORDER BY output_time DESC " \
            "LIMIT 1"
    cur.execute(query, (module_name,))
    try:
        pipeline_id, analysis_result = cur.fetchone()
    except TypeError:  # 값이 존재하지 않아 튜플 언패킹 과정에서 TypeError 발생
        raise ValueError('Error in memoize'
                         '\n: 사전 학습된 데이터가 존재하지 않음')
    else:
        return pipeline_id, analysis_result


def write_result(cur, module_name, data, analysis_result, start_time, end_time):
    # 분석 결과 저장
    query = "INSERT INTO analysis_logs(input_module, input_data, start_time, end_time, result) " \
            "VALUES (%s, %s, %s, %s, %s)"
    cur.execute(query, (module_name, data, start_time, end_time, analysis_result))
    # 파이프라인 아이디 조회
    cur.execute("SELECT pipeline_id "
                "FROM analysis_vw "
                "ORDER BY output_time "  # 분석이 다 끝난 뒤에 INSERT 하므로 end_time 기준 정렬
                "DESC LIMIT 1")
    pipeline_id = cur.fetchone()[0]
    return pipeline_id
