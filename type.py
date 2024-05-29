class Type:
    def __init__(self, java_name, sql_name, prepared_name, array_list=False, foreign=False):
        self.java_name = java_name
        self.sql_name = sql_name
        self.prepared_name = prepared_name
        self.array_list = array_list
        self.foreign = foreign
        
    def static_name(self):
        if self.foreign:
            return "int"
        else:
            return self.java_name