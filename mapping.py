class Mapping:
    def __init__(self, relation1, relation2):
        self.relation1 = relation1
        self.relation2 = relation2

    def java_name(self):
        return snake2pascal(self.relation1)+snake2pascal(self.relation2)+"Mapping"
    
    def getDAO(self):
        return """
public interface """+self.java_name()+"""DAO {

	// --- CRUD -------------

	public void create(int id"""+snake2pascal(self.relation1)+""", int id"""+snake2pascal(self.relation1)+""");

	public boolean delete(int id"""+snake2pascal(self.relation1)+""", int id"""+snake2pascal(self.relation1)+""");

	
	// ----------------------------------
	
	public boolean createTable();

	public boolean dropTable();

}
"""
