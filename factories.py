def DAOfactory(relations):
    string = """
public abstract class DAOFactory {

	// --- List of supported DAO types ---

	/**
	 * Numeric constant '0' corresponds to explicit DB2 choice
	 */
	public static final int DB2 = 0;
	
	/**
	 * Numeric constant '1' corresponds to explicit Hsqldb choice
	 */
	public static final int HSQLDB = 1;
	
	/**
	 * Numeric constant '2' corresponds to explicit MySQL choice
	 */
	public static final int MYSQL = 2;
	
	
	// --- Actual factory method ---
	
	/**
	 * Depending on the input parameter
	 * this method returns one out of several possible 
	 * implementations of this factory spec 
	 */
	public static DAOFactory getDAOFactory(int whichFactory) {
		switch ( whichFactory ) {
		case DB2:
			return new Db2DAOFactory();
		//case HSQLDB:
		//	return new HsqldbDAOFactory();
		//case MYSQL:
		//	return new MySqlDAOFactory();
		default:
			return null;
		}
	}
	
	
	
"""
    for item in relations:
        string += "\tpublic abstract "+item.java_name()+"DAO get"+item.java_name()+"DAO();\n\n"
    string += "}"
    return string

def DB2DAOfactory(relations):
    string = """
import java.sql.Connection;
import java.sql.DriverManager;
    
public class Db2DAOFactory extends DAOFactory {

	/**
	 * Name of the class that holds the jdbc driver implementation for the DB2 database
	 */
	public static final String DRIVER = "com.ibm.db2.jcc.DB2Driver";
	
	/**
	 * URI of the database to connect to
	 */
	public static final String DBURL = "jdbc:db2://diva.deis.unibo.it:50000/tw_stud";

	public static final String USERNAME = "xxx";
	public static final String PASSWORD = "xxx";
	

	// --------------------------------------------

	// static initializer block to load db driver class in memory
	static {
		try {
			Class.forName(DRIVER);
		} 
		catch (Exception e) {
			System.err.println(Db2DAOFactory.class.getName()+": failed to load DB2 JDBC driver\\n" + e.toString());
			e.printStackTrace();
		}
	}

	// --------------------------------------------

	/**
	 * For the sake of simplicity, here we create a brand new connection every time we are asked to.
	 * 
	 * Anyway, this is how things should go in the real world:
	 * 1. 	DB offers a limited number of connections (typically 100) so we can't really afford to 
	 * 		rely on factory invokers to always terminate the connection we have opened
	 * 2. 	At initialization, factory creates a well-defined number of connections (say 20) and put them
	 * 		in a pool
	 * 3.	create and close connection methods actually do not create or close brand new connections, but
	 * 		pick available connections from the pool, each time, and mark them as 'busy'/'free'
	 * 4.	factory does monitoring on the connection pool and force termination of connection in use
	 * 		for a too long time (invoker prob'ly forgot to close it... maybe due to exceptions it didn't handle well)
	 * 5.	terminated connections are replaced by brand new ones
	 */
	public static Connection createConnection() {
		try {
			return DriverManager.getConnection(DBURL,USERNAME,PASSWORD);
		} 
		catch (Exception e) {
			System.err.println(Db2DAOFactory.class.getName() + ".createConnection(): failed creating connection\\n" + e.toString());
			e.printStackTrace();
			System.err.println("Was the database started? Is the database URL right?");
			return null;
		}
	}
	
	/**
	 * For the sake of simplicity, here we actually close the connection we are told to.
	 */
	public static void closeConnection(Connection conn) {
		try {
			conn.close();
		}
		catch (Exception e) {
			System.err.println(Db2DAOFactory.class.getName() + ".closeConnection(): failed closing connection\\n"  + e.toString());
			e.printStackTrace();
		}
	}

	// --------------------------------------------
	
"""
    for item in relations:
        string += "\t@Override\n"
        string += "\tpublic "+item.java_name()+"DAO get"+item.java_name()+"DAO() {\n"
        string += "\t\treturn new Db2"+item.java_name()+"DAO();\n"
        string += "\t}\n\n"
    string += "}"
    return string
