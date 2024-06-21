class Dimensions:

    @staticmethod
    def getFrom(size: int, percent: float):
        return round(size * percent)
