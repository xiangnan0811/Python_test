DELIMITER $$

CREATE PROCEDURE UpdateDiagDataById(IN id_list text)
BEGIN
    -- 将输入的ID列表字符串分割成单独的ID，这里用逗号分隔
    DECLARE id VARCHAR(255);
    DECLARE done INT DEFAULT FALSE;
    DECLARE cur CURSOR FOR SELECT DISTINCT id FROM new_table WHERE FIND_IN_SET(id, id_list);
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO id;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- 开始事务
        START TRANSACTION;

        -- 删除old_table中的数据
        DELETE FROM old_table WHERE id = id;

        -- 从new_table插入新数据到old_table
        INSERT INTO old_table (id, data1, data2)
        SELECT id, data1, data2 FROM new_table WHERE id = id;

        -- 提交事务
        COMMIT;
    END LOOP;

    CLOSE cur;
END$$

DELIMITER ;
