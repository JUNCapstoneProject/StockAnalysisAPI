from abc import ABC, abstractmethod


class Input(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __call__(self, data):
        pass


class Output:
    def __init__(self, pipeline_id, return_time, status_code, message, data):
        self.data = {
            'pipeline_id': pipeline_id,
            'return_time': return_time,
            'status_code': status_code,
            'message': message,
            'result': data
        }

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        else:
            raise KeyError(f"Key {key} not found.")

    def __repr__(self):
        return repr(self.data)

    def __str__(self):
        return str(self.data)

    def keys(self):
        return self.data.keys()
