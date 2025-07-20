from tzlocal import get_localzone_name


class ZoneService:
    @staticmethod
    def get_timezone():
        return get_localzone_name()
