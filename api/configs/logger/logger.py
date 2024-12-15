import ast
from datetime import datetime
import logging
from logging import INFO
from pythonjsonlogger import jsonlogger
from starlette.requests import Request
from zoneinfo import ZoneInfo
from api.configs.constants import LogConstants
import sys

#JsonFormatter: Log kayıtlarını Json formatında özelleştirmek için sınıf.
class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        if len(message_dict.keys()) > 0:
            message_dict = {"message": message_dict.copy()}
        customjsonformatter = jsonlogger.JsonFormatter(rename_fields={'message': 'context'})
        customjsonformatter.add_fields(log_record, record, message_dict)
        log_record = self.convert_to_dict(log_record)
        if not log_record.get('timestamp'):
            now = datetime.now(ZoneInfo('Europe/Istanbul')).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname
    @staticmethod
    def convert_to_dict(d): #Mesajı dictionary'e çevirir.
        for key, val in d.items():
            if key == "message":
                try:
                    check = ast.literal_eval(val)
                except:
                    if isinstance(val, str):
                        d[key] = {"message": val}
                    continue
                if isinstance(check, dict):
                    d[key] = check
        return d


class RagLogger(object):

    def __init__(self, name, level=INFO):
        self.level = level #Log seviyesi
        self.name = str(name) #Log'un adı
        self.console_logger = logging.StreamHandler(sys.stdout) #Konsola yazdırmak için.
        self.formatter = CustomJsonFormatter() #Log formatları için.
        self.console_logger.setFormatter(self.formatter)
        self.console_logger.stream.reconfigure(encoding='utf-8') #Türkçe karakterler için.
        self.logger = logging.getLogger(name) #Girilen isimde logger döner.
        self.logger.setLevel(self.level)
        self.logger.addHandler(self.console_logger) #FileHandler logları file'a yazmak için.

    def info(self, msg, extra={}):
        self.logger.info(msg, extra=extra)

    def error(self, msg, extra={}, exc_info=True):
        self.logger.error(msg, extra=extra, exc_info=exc_info)

    def start_service_operation(self, operation_name, request: Request=None):
        return OperationLog(operation_name, self, request)

class OperationLog(object):
    def __init__(self, operation_name, logger:RagLogger, request:Request = None):
        self.__start_time = datetime.now()
        self.__logger = logger #Raglogger tarafondan üretilecek.
        self.__log = {LogConstants.OPERATION_NAME:operation_name}#log mesajı.
        self.__add_ip_address(request)

    def add_field(self, field, value):
        self.__log[field] = value
        return self

    def __get_start_time(self):
        return self.__start_time

    def __add_ip_address(self, request):
        if request:
            ip_address = request.headers.get('x-real-ip', None)
            host = request.headers.get('host', None)
            if not ip_address and host != "testserver":
                ip_address = request.client.host
            self.add_field(LogConstants.IP_ADDRESS, ip_address)

    def succeed(self):
        self.add_field(LogConstants.OPERATION_STATUS, LogConstants.OPERATION_SUCCEEDED)
        self.__add_operation_duration()
        self.__logger.info(self.__log)

    def fail(self, exc_info=True):
        self.add_field(LogConstants.OPERATION_STATUS, LogConstants.OPERATION_FAILED)
        self.__add_operation_duration()
        self.__logger.error(self.__log, exc_info=exc_info)

    def __add_operation_duration(self):
        self.__log[LogConstants.OPERATION_TOOK] = round((datetime.now() - self.__start_time).total_seconds() * 1000, 2)




