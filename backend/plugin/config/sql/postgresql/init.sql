insert into sys_config (id, name, type, "key", value, is_frontend, remark, created_time, updated_time)
values
(1, 'Status', 'EMAIL', 'EMAIL_STATUS', '1', false, null, now(), null),
(2, 'Server Address', 'EMAIL', 'EMAIL_HOST', 'smtp.qq.com', false, null, now(), null),
(3, 'Server Port', 'EMAIL', 'EMAIL_PORT', '465', false, null, now(), null),
(4, 'Email Account', 'EMAIL', 'EMAIL_USERNAME', 'fba@qq.com', false, null, now(), null),
(5, 'Email Password', 'EMAIL', 'EMAIL_PASSWORD', '', false, null, now(), null),
(6, 'SSL Encryption', 'EMAIL', 'EMAIL_SSL', '1', false, null, now(), null);

select setval(pg_get_serial_sequence('sys_config', 'id'),coalesce(max(id), 0) + 1, true) from sys_config;
