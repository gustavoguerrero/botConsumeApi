class Utils:

    def monthTranslate(month):
        '''
        Necesite de un traductor del mes en espanol al mes en numero
        '''  
        month = month.lower()

        if month == "enero":
            return "01"
        if month == "febrero":
            return "02"
        if month == "marzo":
            return "03"
        if month == "abril":
            return "04"
        if month == "mayo":
            return "05"
        if month == "junio":
            return "06"
        if month == "julio":
            return "07"
        if month == "agosto":
            return "08"
        if month == "setiembre":
            return "09"
        if month == "octubre":
            return "10"
        if month == "noviembre":
            return "11"
        if month == "diciembre":
            return "12"
