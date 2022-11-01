WITH
    get_user_device AS (
        WITH
            raw AS (
                -- replace null data
                SELECT
                    id,
                    COALESCE(signup_os, 'Unknown') AS signup_os
                FROM
                    `panoply.postgres_core_user`
            ),
            add_rank AS (
                SELECT
                    id,
                    signup_os,
                    RANK() OVER (
                        PARTITION BY
                            id
                        ORDER BY
                            signup_os
                    ) AS RANK
                FROM
                    raw
            )
        SELECT
            id,
            signup_os
        FROM
            add_rank
        WHERE
            RANK = 1
    ),
    user_profile AS (
        WITH
            raw AS (
                -- replace null data
                SELECT
                    user_id,
                    COALESCE(age, 'Unknown') AS age,
                    COALESCE(gender, 'Unknown') AS gender,
                    created_at
                FROM
                    `panoply.postgres_onboarding_onboardingusermodels`
            ),
            add_rn AS (
                -- add rn
                SELECT
                    user_id,
                    age,
                    gender,
                    RANK() OVER (
                        PARTITION BY
                            user_id
                        ORDER BY
                            created_at
                    ) AS rn
                FROM
                    raw
            )
        SELECT
            user_id,
            age,
            gender
        FROM
            add_rn
        WHERE
            rn = 1
    ),
    register_table AS (
        SELECT
            a.id,
            created_at,
            DATE(created_at) AS sign_up_date,
            DATE(DATE_TRUNC(created_at, week(MONDAY))) AS week_start,
            COALESCE(a.signup_os, 'Unknown') signup_os,
            COALESCE(age, 'Unknown') age,
            COALESCE(gender, 'Unknown') gender
        FROM
            `panoply.postgres_core_user` a
            LEFT JOIN get_user_device b ON a.id = b.id
            LEFT JOIN user_profile c ON a.id = c.user_id
        WHERE
            TRUE
    ),
    tracking_table AS (
        SELECT
            user_id,
            app_screen,
            created_at,
            DATE(created_at) AS grass_date
        FROM
            `panoply.postgres_tracking_eventtrackingmodel`
        WHERE
            TRUE
            AND user_id IS NOT NULL
            AND app_screen = 'home_screen'
    )
SELECT
    week_start,
    sign_up_date,
    FORMAT_DATE("%m", sign_up_date) AS MONTH,
    gender,
    age,
    signup_os,
    COUNT(
        DISTINCT CASE
            WHEN a.sign_up_date = grass_date THEN id
        END
    ) AS total,
    COUNT(
        DISTINCT CASE
            WHEN grass_date = date_add(sign_up_date, INTERVAL + 1 DAY) THEN id
        END
    ) AS day1,
    COUNT(
        DISTINCT CASE
            WHEN grass_date = date_add(sign_up_date, INTERVAL + 2 DAY) THEN id
        END
    ) AS day2,
    COUNT(
        DISTINCT CASE
            WHEN grass_date = date_add(sign_up_date, INTERVAL + 3 DAY) THEN id
        END
    ) AS day3,
    COUNT(
        DISTINCT CASE
            WHEN grass_date = date_add(sign_up_date, INTERVAL + 4 DAY) THEN id
        END
    ) AS day4,
    COUNT(
        DISTINCT CASE
            WHEN grass_date = date_add(sign_up_date, INTERVAL + 5 DAY) THEN id
        END
    ) AS day5,
    COUNT(
        DISTINCT CASE
            WHEN grass_date = date_add(sign_up_date, INTERVAL + 6 DAY) THEN id
        END
    ) AS day6,
    COUNT(
        DISTINCT CASE
            WHEN grass_date = date_add(sign_up_date, INTERVAL + 7 DAY) THEN id
        END
    ) AS day7,
    COUNT(
        DISTINCT CASE
            WHEN grass_date = date_add(sign_up_date, INTERVAL + 8 DAY) THEN id
        END
    ) AS day8,
    COUNT(
        DISTINCT CASE
            WHEN grass_date = date_add(sign_up_date, INTERVAL + 9 DAY) THEN id
        END
    ) AS day9,
    COUNT(
        DISTINCT CASE
            WHEN grass_date = date_add(sign_up_date, INTERVAL + 10 DAY) THEN id
        END
    ) AS day10,
    COUNT(
        DISTINCT CASE
            WHEN grass_date = date_add(sign_up_date, INTERVAL + 11 DAY) THEN id
        END
    ) AS day11,
    COUNT(
        DISTINCT CASE
            WHEN grass_date = date_add(sign_up_date, INTERVAL + 12 DAY) THEN id
        END
    ) AS day12,
    COUNT(
        DISTINCT CASE
            WHEN grass_date = date_add(sign_up_date, INTERVAL + 13 DAY) THEN id
        END
    ) AS day13,
    COUNT(
        DISTINCT CASE
            WHEN grass_date BETWEEN date_add(sign_up_date, INTERVAL + 1 DAY)
            AND date_add(sign_up_date, INTERVAL + 6 DAY) THEN id
        END
    ) AS w0,
    COUNT(
        DISTINCT CASE
            WHEN grass_date BETWEEN date_add(sign_up_date, INTERVAL + 7 DAY)
            AND date_add(sign_up_date, INTERVAL + 13 DAY) THEN id
        END
    ) AS w1,
    COUNT(
        DISTINCT CASE
            WHEN grass_date BETWEEN date_add(sign_up_date, INTERVAL + 14 DAY)
            AND date_add(sign_up_date, INTERVAL + 20 DAY) THEN id
        END
    ) AS w2,
    COUNT(
        DISTINCT CASE
            WHEN grass_date BETWEEN date_add(sign_up_date, INTERVAL + 21 DAY)
            AND date_add(sign_up_date, INTERVAL + 27 DAY) THEN id
        END
    ) AS w3,
    COUNT(
        DISTINCT CASE
            WHEN grass_date > date_add(sign_up_date, INTERVAL + 27 DAY) THEN id
        END
    ) AS w4_
FROM
    register_table a
    LEFT JOIN tracking_table b ON id = user_id
WHERE
    TRUE
    AND user_id IS NOT NULL -- filter users that returned to home screen
    AND sign_up_date >= DATE '2022-04-04'
GROUP BY
    1,
    2,
    3,
    4,
    5,
    6