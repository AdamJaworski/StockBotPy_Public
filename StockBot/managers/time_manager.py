from datetime import timedelta


class TimeManager:
    @staticmethod
    def add(time_base: int, adding_minutes=0, adding_hours=0) -> int:
        return int(time_base + timedelta(hours=adding_hours, minutes=adding_minutes).total_seconds()*1000)
