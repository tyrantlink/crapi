from fastapi.responses import JSONResponse
from math import ceil


#? very hardcoded because i just do not care
class RateLimiter:
	def __init__(self,per_second:int,per_minute:int,res_code:int=429) -> None:
		self.per_second = per_second
		self.per_minute = per_minute
		self.res_code = res_code
		self.__requests:dict[str,list[float]] = {}
		self.last_day = 0
	
	def clear_old_requests(self,time:float,identifier:str|None=None) -> None:
		if identifier is not None:
			self.__requests[identifier] = [t for t in self.__requests[identifier] if t > time-60]
		else:
			for key in self.__requests:
				self.__requests[key] = [t for t in self.__requests[key] if t > time-60]
				if not self.__requests[key]:
					del self.__requests[key]

	def request(self,identifier:str,time:float) -> None:
		if identifier == 'bypass_ratelimit': return
		self.__requests.setdefault(identifier,[]).append(time)
		self.clear_old_requests(time,identifier)
	
	def _requests_per_second(self,identifier:str,time:float,get_retry_time:bool=False) -> int:
		times = [t for t in self.__requests.get(identifier,[]) if t > time-1]
		return ((1-(time-min(times[self.per_second*-1:]))) if times else 0) if get_retry_time else len(times)

	def _requests_per_minute(self,identifier:str,time:float,get_retry_time:bool=False) -> int:
		times = [t for t in self.__requests.get(identifier,[]) if t > time-60]
		return ((60-(time-min(times[self.per_minute*-1:]))) if times else 0) if get_retry_time else len(times)
	
	def check(self,identifier:str,time:float) -> bool:
		if self._requests_per_second(identifier,time) > self.per_second:
			return False
		if self._requests_per_minute(identifier,time) > self.per_minute:
			return False
		return True

	def error(self,identifier:str,time:float) -> None:
		message,retry_after = '',0
		if self._requests_per_second(identifier,time) > self.per_second:
			message,retry_after = f'{self.per_second}/second limit exceeded',self._requests_per_second(identifier,time,True)
		if self._requests_per_minute(identifier,time) > self.per_minute:
			message,retry_after = f'{self.per_minute}/minute limit exceeded',self._requests_per_minute(identifier,time,True)
		return JSONResponse(status_code=self.res_code,content={
			'message': f'enhance your calm. {message}',
			'retry_after': ceil(retry_after*1000)
		})
		
