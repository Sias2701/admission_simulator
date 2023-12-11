USE admission;

INSERT INTO faculties(f_id, f_name, f_location)
VALUES
('F-INFO', '信息工程学院', '大学城'),
('F-INTL', '国际教育学院', '番禺'),
('F-CENG', '土木与交通工程学院', '大学城'),
('F-LANG', '外国语学院', '大学城'),
('F-BULD', '建筑与城市规划学院', '东风路'),
('F-MATH', '数学与统计学院', '龙洞'),
('F-MECH', '机电工程学院', '大学城'),
('F-MATE', '材料与能源学院', '大学城'),
('F-LAWS', '法学院', '龙洞'),
('F-PHYS', '物理与光电工程学院', '大学城'),
('F-ENVE', '环境科学与工程学院', '大学城'),
('F-ECOL', '生态环境与资源学院', '大学城'),
('F-BIOM', '生物医药学院', '大学城'),
('F-MANG', '管理学院', '龙洞'),
('F-ECON', '经济学院', '龙洞'),
('F-AUTO', '自动化学院', '大学城'),
('F-DSGN', '艺术与设计学院', '东风路'),
('F-COMP', '计算机学院', '大学城'),
('F-CHME', '轻工化工学院', '大学城'),
('F-INTC', '集成电路学院', '大学城');

CREATE INDEX falcuty_location ON faculties(f_location);