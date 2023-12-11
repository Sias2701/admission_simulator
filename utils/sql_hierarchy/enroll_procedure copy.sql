USE admission;
GO

CREATE OR ALTER PROCEDURE apply_enroll AS

BEGIN
    CREATE TABLE #enroll_control(
        m_group CHAR(3),
        m_id CHAR(12),
        max_count INT DEFAULT 0,
        current_count INT DEFAULT 0,
        PRIMARY KEY(m_group, m_id),
        CHECK(current_count <= max_count)
    );

    CREATE TABLE #adjust_control(
        c_id CHAR(12),
        c_group CHAR(3)
    );

    SET TRANSACTION ISOLATION LEVEL REPEATABLE READ
    BEGIN TRANSACTION

    DELETE FROM accept_enroll;
    DELETE FROM reject_enroll;

    -- load enroll
    INSERT INTO #enroll_control(m_id, max_count) SELECT m_id, m_max_enroll FROM majors;

    SELECT m_id FROM #enroll_control;

    COMMIT TRANSACTION

END