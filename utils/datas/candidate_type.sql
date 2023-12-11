USE admission;
GO

BEGIN TRANSACTION

INSERT INTO candidate_type_info(t_id, t_name) VALUES
('NOR', '普通类'),
('ART', '美术类'),
('INT', '国际班'),
('LOC', '地方专项'),
('PHY', '高水平运动队'),
('PEF', '表演专业组');

COMMIT