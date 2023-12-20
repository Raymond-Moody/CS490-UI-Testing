use fitness;
-- Delete registration test user
DELETE FROM user_credentials WHERE user_id IN (SELECT user_id from user where email='testuser@email.com');
DELETE FROM token WHERE user_id IN (SELECT user_id from user where email='testuser@email.com'); 
DELETE FROM physical_health_log WHERE user_id IN (SELECT user_id from user where email='testuser@email.com');
DELETE FROM become_coach_request WHERE user_id IN (SELECT user_id from user where email='testuser@email.com');
DELETE FROM user WHERE email = 'testuser@email.com';

-- Reset Test user
DELETE FROM physical_health_log WHERE user_id IN (SELECT user_id from user where email='testuser123@gmail.com');
DELETE FROM mental_health_log WHERE user_id IN (SELECT user_id from user where email='testuser123@gmail.com');
DELETE FROM calorie_log WHERE user_id IN (SELECT user_id from user where email='testuser123@gmail.com');
DELETE FROM water_log WHERE user_id IN (SELECT user_id from user where email='testuser123@gmail.com');
DELETE FROM workout_log WHERE user_id IN (SELECT user_id from user where email='testuser123@gmail.com');
