USE admission;
GO

CREATE OR ALTER VIEW final_enroll_view_all AS
SELECT accept_enroll.c_id, accept_enroll.c_group, c_enroll, accept_enroll.c_adjust, c_score, c_rank FROM accept_enroll INNER JOIN candidates ON accept_enroll.c_id = candidates.c_id;
GO

CREATE OR ALTER VIEW final_accept_adjust AS
SELECT * FROM final_enroll_view_all WHERE c_adjust = 'Y';
GO

CREATE OR ALTER PROCEDURE accept_list_stat_major
AS
BEGIN
    SELECT m_id, m_name, m_faculty, MAX(c_score) AS max_score, MIN(c_score) AS min_score, MIN(c_rank) AS max_rank, MAX(c_rank) AS min_rank, AVG(c_score) AS avg_score FROM final_enroll_view_all INNER JOIN majors ON final_enroll_view_all.c_enroll = majors.m_id GROUP BY m_id,m_name
END

GO

CREATE OR ALTER PROCEDURE accept_list_stat_faculty
AS
BEGIN
    SELECT m_faculty AS faculty_id,(SELECT f_name FROM faculties WHERE f_id = m_faculty) AS faculty_name, MAX(c_score) AS max_score, MIN(c_score) AS min_score, MIN(c_rank) AS max_rank, MAX(c_rank) AS min_rank, AVG(c_score) AS avg_score FROM final_enroll_view_all INNER JOIN (SELECT m_id,m_faculty FROM majors) AS major_less_info ON final_enroll_view_all.c_enroll = major_less_info.m_id GROUP BY m_faculty
END
GO

CREATE OR ALTER PROCEDURE accept_list_stat_all
AS
BEGIN
    DECLARE @mid_score FLOAT;
    DECLARE @max_score FLOAT;
    DECLARE @min_score FLOAT;
    DECLARE @avg_score FLOAT;
    DECLARE @max_rank INT;
    DECLARE @min_rank INT;
    SET @mid_score = (SELECT TOP 1 PERCENTILE_DISC(0.5) WITHIN GROUP(ORDER BY c_score) OVER () FROM final_enroll_view_all);
    SET @max_score = (SELECT MAX(c_score) FROM final_enroll_view_all);
    SET @min_score = (SELECT MIN(c_score) FROM final_enroll_view_all);
    SET @avg_score = (SELECT AVG(c_score) FROM final_enroll_view_all);
    SET @max_rank = (SELECT MAX(c_rank) FROM final_enroll_view_all);
    SET @min_rank = (SELECT MIN(c_rank) FROM final_enroll_view_all);
    SELECT @max_score AS max_score, @min_score AS min_score, @avg_score AS avg_score , @mid_score AS median_score, @min_rank AS max_rank, @max_rank AS min_rank
END