get_table_names = """
SELECT table_name 
FROM (
	SELECT table_name, string_agg(lower(privilege_type),',') as perm
	FROM information_schema.role_table_grants 
	where table_schema not in ('pg_catalog', 'information_schema')
	GROUP By table_name
	) tabl
where perm like '%insert%' AND perm like '%select%' AND perm like '%update%'
"""

get_field_names = """SELECT column_name
FROM information_schema.columns
WHERE table_name   = '{0}'
ORDER BY column_name"""

get_address = """SELECT distinct {0} from {1} """

api_options = ['City', 'Subcategory', 'Category', 'Polygon', 'Searchtype', 'Radius', 'Point', 'Offset', 'Limit']
other_options = [ 'Searchtype','Polygon', 'Radius', 'Point', 'Offset', 'Limit']
populate_columns = ['address', 'city', 'subcategory' ,'category']
fileextension = {'CSV':'*.csv', 'Text':'*.txt', 'JSON':'*.json'}
thread_result = {}
logs_stylesheet = """font-size:12px;"""
db_columns = {}
lng = 0.0
lat = 0.0
precision = ''
compound_address_parents = ''
remarks = ''
subcategory = ''
category = ''
name = ''
priority = ''
raw_address = ''
final_dict = {}
count = 0
total = 0
k  = 0

process_main = "Alter Table {0} Add Column IF NOT EXISTS address_formatted varchar;Update {0} set address_formatted = {1};"
specials = "Update {0} set address_formatted = regexp_replace(address_formatted, '[^\w]+',' ','g') "
ltrim = "Update {0} set address_formatted = ltrim(address_formatted)"
rtrim = "Update {0} set address_formatted = rtrim(address_formatted)"
extraspace = "Update {0} set address_formatted = replace(address_formatted, '  ', ' ') where address_formatted ilike '%  %'"
nullvals = " address_formatted is not null "
numerical = " address_formatted !~ '^\d+$' "
lengthless = " length(address_formatted) > 5 "
