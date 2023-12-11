from faker import Faker
import random
import numpy as np
import pyodbc
from tqdm import tqdm

data_source = Faker('zh_CN')

COUNT = 10000

gd_location_code = ['440101', '440103', '440104', '440105', '440106', '440111', '440112', '440113', '440114', '440115', '440116', '440183', '440184', '440201', '440203', '440204', '440205', '440222', '440224', '440229', '440232', '440233', '440281', '440282', '440301', '440303', '440304', '440305', '440306', '440307', '440308', '440401', '440402', '440403', '440404', '440501', '440507', '440511', '440512', '440513', '440514', '440515', '440523', '440601', '440604', '440605', '440606', '440607', '440608', '440701', '440703', '440704', '440705', '440781', '440783', '440784', '440785', '440801', '440802', '440803', '440804', '440811', '440823', '440825', '440881', '440882', '440883', '440901', '440902', '440903', '440923', '440981', '440982', '440983', '441201', '441202', '441203', '441223', '441224', '441225', '441226', '441283', '441284', '441301', '441302', '441303', '441322', '441323', '441324', '441401', '441402', '441421', '441422', '441423', '441424', '441426', '441427', '441481', '441501', '441502', '441521', '441523', '441581', '441601', '441602', '441621', '441622', '441623', '441624', '441625', '441701', '441702', '441721', '441723', '441781', '441801', '441802', '441821', '441823', '441825', '441826', '441827', '441881', '441882', '445101', '445102', '445121', '445122', '445201', '445202', '445221', '445222', '445224', '445281', '445301', '445302', '445321', '445322', '445323', '445381']
types = ['NOR','INT','LOC','ART','PEF','PHY']
exam_id_pool = set()

SERVER = '172.16.50.128'
DATABASE = 'admission'
USERNAME = 'sa'
PASSWORD = '12345678a@'

connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};TrustServerCertificate=yes'

def random_exam_id(exam_type,primary_choice, year='23'):
    type_code = ''

    if exam_type in ['NOR', 'INT', 'LOC'] and primary_choice == 'H':
        type_code = '1'
    if exam_type in ['NOR', 'INT', 'LOC'] and primary_choice == 'P':
        type_code = '5'
    if exam_type in ['ART','PEF'] and primary_choice == 'H':
        type_code = '3'
    if exam_type in ['ART','PEF'] and primary_choice == 'P':
        type_code = '6'
    if exam_type in ['PHY']:
        type_code = '8'
    
    ret = year + random.choice(gd_location_code) + '1' + type_code + str(data_source.random_number(4)).zfill(4)

    while ret in exam_id_pool:
        ret = year + random.choice(gd_location_code) + '1' + type_code + str(data_source.random_number(4)).zfill(4)
    
    exam_id_pool.add(ret)
    assert len(ret) == 14

    return ret

conn = pyodbc.connect(connectionString) 

out_file = open('candidates.sql', 'w')

out_file.write(
"""
USE admission;
INSERT INTO candidates(c_id, c_score, c_rank, c_adjust, c_type, c_primary, c_secondary, c_group, c_enroll1, c_enroll2, c_enroll3, c_enroll4, c_enroll5, c_enroll6) VALUES
""")

candidates = []

for _ in tqdm(range(COUNT)):
    c_type = random.choice(types)

    c_p = random.choice(['P', 'H'])
    c_s = "".join(random.sample(['B', 'C', 'G', 'O'], 2))
    c_id = random_exam_id(c_type, c_p)

    adj = random.choice(['A','R'])
    c_tag = c_type + '/' + 'G' + '#' + c_p + '-' + c_s + '::' + adj + '000'
    cursor = conn.cursor()
    cursor.execute(f"SELECT g_id FROM major_groups WHERE g_type='{c_type}'")
    valid_groups = [r.g_id for r in cursor.fetchall()]
    c_group = random.choice(valid_groups)
    cursor = conn.cursor()

    cursor.execute(f"SELECT m_id FROM majors WHERE m_group='{c_group}'")
    valid_major = [r.m_id for r in cursor.fetchall()]
    c_score = random.randrange(0, 750)
    c_enrolls = random.sample(valid_major, min(6, random.randint(1,len(valid_major))))
    candidates.append((c_id, c_score, adj, c_type, c_p, c_s, c_group, c_enrolls))

candidates.sort(key=lambda x: x[1],reverse=True)

for i in tqdm(range(len(candidates))):
    entry = candidates[i]
    insert_str = '('
    insert_str += "'" + entry[0] + "', "
    insert_str += str(entry[1]) + ', '
    insert_str += str(i+1) + ', '
    insert_str += "'" + str(entry[2]) + "', "
    insert_str += "'" + str(entry[3]) + "', "
    insert_str += "'" + str(entry[4]) + "', "
    insert_str += "'" + str(entry[5]) + "', "
    insert_str += "'" + str(entry[6]) + "', "
    e_cnt = 0
    for e in entry[7]:
        insert_str += "'" + str(e) + "', "
        e_cnt += 1

    for _ in range(e_cnt, 6):
        insert_str += "NULL, "
    insert_str = insert_str[:-2]
    if i == len(candidates) - 1:
        insert_str += ');\n'
    elif i % 999 == 0:
        insert_str += ');\nINSERT INTO candidates(c_id, c_score, c_rank, c_adjust, c_type, c_primary, c_secondary, c_group, c_enroll1, c_enroll2, c_enroll3, c_enroll4, c_enroll5, c_enroll6) VALUES\n'
    else:
        insert_str += '),\n'
    out_file.write(insert_str)
# SQL_QUERY = """
# SELECT * FROM major_groups;
# """
# 
# cursor = conn.cursor()
# cursor.execute(SQL_QUERY)
# 
# records = cursor.fetchall()
# for r in records:
#     print(r.g_id)