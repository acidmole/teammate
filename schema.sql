CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	username TEXT,
	password TEXT,
	first_name TEXT,
	last_name TEXT,
	admin BOOLEAN DEFAULT FALSE,
	visible BOOLEAN DEFAULT TRUE
);

CREATE TABLE players (
	id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	jersey_number INTEGER DEFAULT 0,
	height INTEGER DEFAULT 0,
	weight INTEGER DEFAULT 0,
	position CHAR
);

CREATE TABLE events (
	id SERIAL PRIMARY KEY,
	type INTEGER DEFAULT 0,
	day DATE,
	h_min TIME,
	name TEXT,
	location TEXT
);

CREATE TABLE sign_ups (
	id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	event_id INTEGER REFERENCES events,
	sign_up BOOLEAN
);

CREATE TABLE comments (
	id SERIAL PRIMARY KEY,
	t_stamp TIMESTAMP,
	user_id INTEGER REFERENCES users,
	event_id INTEGER REFERENCES events,
	message TEXT NOT NULL
);

CREATE TABLE game_stats (
	id SERIAL PRIMARY KEY,
	event_id INTEGER REFERENCES events,
	player_id INTEGER REFERENCES users,
	mins TIME,
	fg INTEGER,
	fga INTEGER,
	three INTEGER,
	three_a INTEGER,
	ft INTEGER,
	ft_a INTEGER,
	dreb INTEGER,
	oreb INTEGER,
	foul INTEGER,
	ass INTEGER,
	tover INTEGER,
	steal INTEGER,
	block INTEGER
);


