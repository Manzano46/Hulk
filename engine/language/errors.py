class HulkError(Exception):
    def __init__(self, text):
        super().__init__(text)

    @property
    def error_type(self):
        return 'HulkError'

    @property
    def text(self):
        return self.args[0]

    def __str__(self):
        return f'{self.error_type}: {self.text}'

    def __repr__(self):
        return str(self)
    
class HulkLexicographicError(HulkError,BaseException):
    def __init__(self, text, line, column):
        super().__init__(text)
        self.line = line
        self.column = column

    def __str__(self):
        return f'({self.line}, {self.column}) - {self.error_type}: {self.text}'

    UNKNOWN_TOKEN = 'En mi vida había visto este token \'%s\' en la línea \'%s\' columna \'%s\'.'
    STRING_INF = 'Anormal cierra el string en la línea \'%s\' columna \'%s\'.'
    UNSPECTED_TOKEN = 'De donde sacaste este token???.No se esperaba el token \'%s\' en la línea \'%s\' columna \'%s\'.'
    INVALID_CARATER = 'No se pudo tokenizar el caracter en la línea \'%s\' columna \'%s\'.'

    @property
    def error_type(self):
        return 'ERROR LEXICOGRAFICO'