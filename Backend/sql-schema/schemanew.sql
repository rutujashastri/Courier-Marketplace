-- Create a table to store user information
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    email VARCHAR(255),
    agent_address VARCHAR(255),  -- FetchAI Agent Address
    calendar_permission_file JSON,  -- File generated when user accepts Google Calendar permission
    is_courier BOOLEAN,
    fast_price DECIMAL(10, 2),  -- Price for fast delivery (optional)
    normal_pace_price DECIMAL(10, 2),  -- Price for normal pace delivery (optional)
    slow_price DECIMAL(10, 2),  -- Price for slow delivery (optional)
    -- Add other user-related fields as needed
);

-- -- Create a table to store interactions between users and couriers
-- CREATE TABLE interactions (
--     interaction_id SERIAL PRIMARY KEY,
--     sender_user_id INT REFERENCES users(user_id),
--     receiver_courier_id INT REFERENCES couriers(courier_id),
--     request_id INT REFERENCES courier_requests(request_id),
--     interaction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     -- Add other interaction-related fields as needed
-- );

-- -- Create a table to store WhatsApp interactions
-- CREATE TABLE whatsapp_interactions (
--     interaction_id INT REFERENCES interactions(interaction_id),
--     whatsapp_chat_id VARCHAR(255),
--     -- Add other WhatsApp-related fields as needed
-- );

-- -- Create a table to store calendar events
-- CREATE TABLE calendar_events (
--     event_id SERIAL PRIMARY KEY,
--     user_id INT REFERENCES users(user_id),
--     event_type VARCHAR(50) NOT NULL,
--     event_time TIMESTAMP,
--     -- Add other calendar-related fields as needed
-- );

-- -- Create a table to store Fetch.ai agent information
CREATE TABLE fetch_agents (
    agent_id SERIAL PRIMARY KEY,
    agent_name VARCHAR(255) NOT NULL,
    agent_type VARCHAR(50) NOT NULL,
    -- Add other Fetch.ai agent-related fields as needed
);

-- -- Create a table to store Fetch.ai platform information
-- CREATE TABLE fetch_platforms (
--     platform_id SERIAL PRIMARY KEY,
--     platform_name VARCHAR(255) NOT NULL,
--     platform_type VARCHAR(50) NOT NULL,
--     -- Add other Fetch.ai platform-related fields as needed
-- );
