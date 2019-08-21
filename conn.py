import mysql.connector

def run_query(query=''): 

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=""
        )
 
    cursor = mydb.cursor()         
    cursor.execute(query, multi=True)          
 
    #if query.upper().startswith('SELECT'): 
    #    data = cursor.fetchall()   
    #else: 
    #    mydb.commit()               
    #    data = None 
 
    cursor.close()                 
    mydb.close()
    #return data