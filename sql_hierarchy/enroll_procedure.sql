USE admission;
GO

CREATE OR ALTER PROCEDURE apply_enroll AS

BEGIN
    CREATE TABLE #enroll_control(
        m_group CHAR(3),
        m_id CHAR(12),
        m_primary CHAR(1) CHECK(m_primary IN (NULL, 'P', 'H')),
        m_secondary CHAR(1) CHECK(m_secondary IN (NULL, 'B', 'C', 'G', 'O')),
        max_count INT DEFAULT 0,
        current_count INT DEFAULT 0,
        PRIMARY KEY(m_group, m_id),
        CHECK(current_count <= max_count)
    );

    CREATE TABLE #adjust_control(
        c_id CHAR(14),
        c_group CHAR(3)
    );

    SET TRANSACTION ISOLATION LEVEL REPEATABLE READ
    BEGIN TRANSACTION

    DELETE FROM accept_enroll;
    DELETE FROM reject_enroll;

    -- load enroll
    INSERT INTO #enroll_control(m_group, m_id,m_primary,m_secondary, max_count) SELECT m_group, m_id, m_primary,m_secondary, COALESCE(m_max_enroll, 2147483647) FROM majors;

    DECLARE @id CHAR(14);
    DECLARE @adjust CHAR(1);
    DECLARE @primary CHAR(1);
    DECLARE @secondary CHAR(2);
    DECLARE @group CHAR(3);
    DECLARE @enroll1 CHAR(12);
    DECLARE @enroll2 CHAR(12);
    DECLARE @enroll3 CHAR(12);
    DECLARE @enroll4 CHAR(12);
    DECLARE @enroll5 CHAR(12);
    DECLARE @enroll6 CHAR(12);
    DECLARE @current_enroll CHAR(12);
    DECLARE @reject_term CHAR(100);
    DECLARE @requirement_primary CHAR(1);
    DECLARE @requirement_secondary CHAR(1);
    DECLARE cur_candidate CURSOR LOCAL FORWARD_ONLY FOR SELECT c_id, c_adjust, c_primary, c_secondary, c_group, c_enroll1, c_enroll2, c_enroll3, c_enroll4, c_enroll5, c_enroll6 FROM candidates;  

    OPEN cur_candidate

    FETCH NEXT FROM cur_candidate INTO @id, @adjust, @primary, @secondary, @group, @enroll1, @enroll2, @enroll3, @enroll4, @enroll5, @enroll6
    WHILE(@@FETCH_STATUS = 0)
    BEGIN
        IF(@enroll1 IS NOT NULL AND (((SELECT m_primary FROM majors WHERE m_id = @enroll1) IS NULL) OR COALESCE(CHARINDEX(@primary, (SELECT m_primary FROM majors WHERE m_id = @enroll1)), 0) != 0) AND (((SELECT m_secondary FROM majors WHERE m_id = @enroll1) IS NULL) OR COALESCE(CHARINDEX(@secondary, (SELECT m_secondary FROM majors WHERE m_id = @enroll1)), 0) != 0))
        BEGIN
            BEGIN TRY
                UPDATE #enroll_control SET current_count = current_count + 1 WHERE m_group = @group AND m_id = @enroll1;
                SET @current_enroll = @enroll1;
                GOTO Success;
            END TRY
            BEGIN CATCH
                IF(@adjust = 'A')
                    GOTO Adjustment;
                ELSE
                BEGIN
                    SET @reject_term = "ENROLL/NORM::ADJUSTMENT REJECT"
                    GOTO Reject;
                END
            END CATCH
        END

        IF(@enroll2 IS NOT NULL AND (((SELECT m_primary FROM majors WHERE m_id = @enroll2) IS NULL) OR COALESCE(CHARINDEX(@primary, (SELECT m_primary FROM majors WHERE m_id = @enroll2)), 0) != 0) AND (((SELECT m_secondary FROM majors WHERE m_id = @enroll2) IS NULL) OR COALESCE(CHARINDEX(@secondary, (SELECT m_secondary FROM majors WHERE m_id = @enroll2)), 0) != 0))
        BEGIN
            BEGIN TRY
                UPDATE #enroll_control SET current_count = current_count + 1 WHERE m_group = @group AND m_id = @enroll2;
                SET @current_enroll = @enroll2;
                GOTO Success;
            END TRY
            BEGIN CATCH
                IF(@adjust = 'A')
                    GOTO Adjustment;
                ELSE
                BEGIN
                    SET @reject_term = "ENROLL/NORM::ADJUSTMENT REJECT"
                    GOTO Reject;
                END
            END CATCH
        END

        IF(@enroll3 IS NOT NULL AND (((SELECT m_primary FROM majors WHERE m_id = @enroll3) IS NULL) OR COALESCE(CHARINDEX(@primary, (SELECT m_primary FROM majors WHERE m_id = @enroll3)), 0) != 0) AND (((SELECT m_secondary FROM majors WHERE m_id = @enroll3) IS NULL) OR COALESCE(CHARINDEX(@secondary, (SELECT m_secondary FROM majors WHERE m_id = @enroll3)), 0) != 0))
        BEGIN
            BEGIN TRY
                UPDATE #enroll_control SET current_count = current_count + 1 WHERE m_group = @group AND m_id = @enroll3;
                SET @current_enroll = @enroll3;
                GOTO Success;
            END TRY
            BEGIN CATCH
                IF(@adjust = 'A')
                    GOTO Adjustment;
                ELSE
                BEGIN
                    SET @reject_term = "ENROLL/NORM::ADJUSTMENT REJECT"
                    GOTO Reject;
                END
            END CATCH
        END

        IF(@enroll4 IS NOT NULL AND (((SELECT m_primary FROM majors WHERE m_id = @enroll4) IS NULL) OR COALESCE(CHARINDEX(@primary, (SELECT m_primary FROM majors WHERE m_id = @enroll4)), 0) != 0) AND (((SELECT m_secondary FROM majors WHERE m_id = @enroll4) IS NULL) OR COALESCE(CHARINDEX(@secondary, (SELECT m_secondary FROM majors WHERE m_id = @enroll4)), 0) != 0))
        BEGIN
            BEGIN TRY
                UPDATE #enroll_control SET current_count = current_count + 1 WHERE m_group = @group AND m_id = @enroll4;
                SET @current_enroll = @enroll4;
                GOTO Success;
            END TRY
            BEGIN CATCH
                IF(@adjust = 'A')
                    GOTO Adjustment;
                ELSE
                BEGIN
                    SET @reject_term = "ENROLL/NORM::ADJUSTMENT REJECT"
                    GOTO Reject;
                END
            END CATCH
        END

        IF(@enroll5 IS NOT NULL AND (((SELECT m_primary FROM majors WHERE m_id = @enroll5) IS NULL) OR COALESCE(CHARINDEX(@primary, (SELECT m_primary FROM majors WHERE m_id = @enroll5)), 0) != 0) AND (((SELECT m_secondary FROM majors WHERE m_id = @enroll5) IS NULL) OR COALESCE(CHARINDEX(@secondary, (SELECT m_secondary FROM majors WHERE m_id = @enroll5)), 0) != 0))
        BEGIN
            BEGIN TRY
                UPDATE #enroll_control SET current_count = current_count + 1 WHERE m_group = @group AND m_id = @enroll5;
                SET @current_enroll = @enroll5;
                GOTO Success;
            END TRY
            BEGIN CATCH
                IF(@adjust = 'A')
                    GOTO Adjustment;
                ELSE
                BEGIN
                    SET @reject_term = "ENROLL/NORM::ADJUSTMENT REJECT"
                    GOTO Reject;
                END
            END CATCH
        END

        IF(@enroll6 IS NOT NULL AND (((SELECT m_primary FROM majors WHERE m_id = @enroll6) IS NULL) OR COALESCE(CHARINDEX(@primary, (SELECT m_primary FROM majors WHERE m_id = @enroll6)), 0) != 0) AND (((SELECT m_secondary FROM majors WHERE m_id = @enroll6) IS NULL) OR COALESCE(CHARINDEX(@secondary, (SELECT m_secondary FROM majors WHERE m_id = @enroll6)), 0) != 0))
        BEGIN
            BEGIN TRY
                UPDATE #enroll_control SET current_count = current_count + 1 WHERE m_group = @group AND m_id = @enroll6;
                SET @current_enroll = @enroll6;
                GOTO Success;
            END TRY
            BEGIN CATCH
                IF(@adjust = 'A')
                    GOTO Adjustment;
                ELSE
                BEGIN
                    SET @reject_term = "ENROLL/NORM::ADJUSTMENT REJECT"
                    GOTO Reject;
                END
            END CATCH
        END

        SET @reject_term = "ENROLL/NORM::EMPTY/REQUIREMENT REJECT";
        GOTO Reject;
        Success:
            INSERT INTO accept_enroll(c_id, c_enroll, c_group, c_adjust) VALUES(@id, @current_enroll, @group, 'N');
            GOTO Next_element;
        Adjustment:
            INSERT INTO #adjust_control(c_id, c_group) VALUES (@id, @group);
            GOTO Next_element;
        Reject:
            INSERT INTO reject_enroll(c_id, reject_term) VALUES (@id, @reject_term);
            GOTO Next_element;

        Next_element:
        FETCH NEXT FROM cur_candidate INTO @id, @adjust, @primary, @secondary, @group, @enroll1, @enroll2, @enroll3, @enroll4, @enroll5, @enroll6
    END
    

    DEALLOCATE cur_candidate;

    DECLARE cur_adjust CURSOR LOCAL FORWARD_ONLY FOR SELECT * FROM #adjust_control;

    OPEN cur_adjust;

    FETCH NEXT FROM cur_adjust INTO @id, @group
    WHILE(@@FETCH_STATUS = 0)
    BEGIN
        DECLARE cur_gp_major CURSOR LOCAL FORWARD_ONLY FOR SELECT m_id FROM majors WHERE m_group = @group;
        DECLARE @flag INT;
        SET @flag = 0;
        OPEN cur_gp_major;
        FETCH NEXT FROM cur_gp_major INTO @current_enroll
        WHILE(@@FETCH_STATUS = 0)
        BEGIN
            BEGIN TRY
                UPDATE #enroll_control SET current_count = current_count + 1 WHERE m_group = @group AND m_id = @current_enroll;
                GOTO Adjustsuccess;
            END TRY
            BEGIN CATCH
                FETCH NEXT FROM cur_gp_major INTO @current_enroll;
                CONTINUE;
            END CATCH
            Adjustsuccess:
                INSERT INTO accept_enroll(c_id, c_enroll, c_group, c_adjust) VALUES(@id, @current_enroll, @group, 'Y');
                BREAK
                SET @flag = 1;
        END

        IF(@flag = 1)
            CONTINUE
        ELSE
            INSERT INTO reject_enroll(c_id, reject_term) VALUES (@id, "ENROLL/ADJUST::REJECT");
        DEALLOCATE cur_gp_major;

        FETCH NEXT FROM cur_adjust INTO @id, @group
    END

    DEALLOCATE cur_adjust;

    COMMIT TRANSACTION

END
