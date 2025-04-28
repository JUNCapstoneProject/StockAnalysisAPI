ROUTE_TABLE = {}


def RequestMapping(base_path):
    def class_decorator(cls):
        # 클래스의 메서드 중 Mapping 데코레이터가 붙은 것만 찾아 처리
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if hasattr(attr, '_route_path'):
                full_path = base_path.rstrip('/') + attr._route_path
                ROUTE_TABLE[full_path] = (cls, attr_name)
        return cls
    return class_decorator


def GetMapping(path):
    def method_decorator(func):
        # 함수에 _route_pat 속성 추가하여 RequestMapping에서 인식
        func._route_path = path
        return func
    return method_decorator
