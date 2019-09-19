import sys
import subprocess
import os
import logging

# Set source directory
os.chdir(os.path.split(sys.argv[1])[0])

''' 
   configure logging 
'''
logging.basicConfig(filename='script.log',filemode='w',format='%(asctime)s - %(levelname)s - %(message)s')



# Directory to output converted csv files
def OutputFileDir(file):
	database_path,filename = os.path.split(file)	
	
	source_dir = os.path.dirname(database_path) 
	
	output_home = os.path.dirname(source_dir)

	output_dir = output_home+"/output/"

	if not os.path.exists(output_dir):
		try:
			os.mkdir(output_dir)
		except Exception as e:
			logging.error("Exception occurred", exc_info=True)
		

	return filename,output_dir



# Handles both .mdb and .accdb 
def access_mdb_and_accdb_ToCsv(access_Database):

	access_Database_extension = access_Database.rsplit('.',1)[-1]
	
	if(access_Database_extension in ["mdb","MDB","accdb","ACCDB"]):
		
		'''
		   Get list of tables from access db with "mdb-tables" i.e "mdb-tables database_name".
		   Works for both .mdb(2003 access version) and .accdb(2007-2013 version - latest access version).
		   Returns bytes
		'''
		try:
			table_names = subprocess.Popen(["mdb-tables","-1",access_Database],
										   stdout=subprocess.PIPE).communicate()[0]
		except Exception as e:
			logging.error("Exception occurred", exc_info=True)
		
		
		# List of tables 
		tables = table_names.split()
	


		''' 
			Dump each returned table as a csv  file using "mdb-export" i.e "mdb-export database_name table".
			Converting " " in table names to "_" for the csv filenames

		'''
		for table in tables:
			if table != '':
				try:
					csv_filename = output_dir+table.decode("UTF-8").replace(" ","_")+".csv"                    
                 
					
					with open(csv_filename,'w') as csv_file:

						data = subprocess.Popen(["mdb-export",access_Database,table],
											    stdout=subprocess.PIPE).communicate()[0]

						#write to csv file.
						csv_file.write(data.decode('UTF-8'))


		                 # Close the csv file.
						csv_file.close()
						print("extracted to "+output_dir)
				except Exception as e:
					logging.error("Exception occurred", exc_info=True)

		os.remove(access_Database)
	else:
		logging.warning('No access file found') 
		

if __name__ == '__main__':
	 # Output filedir
    filename,output_dir = OutputFileDir(sys.argv[1])
   
    access_mdb_and_accdb_ToCsv(filename)
   
