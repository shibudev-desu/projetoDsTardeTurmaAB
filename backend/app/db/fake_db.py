fake_db = {
    # id SERIAL PRIMARY KEY,
    # email VARCHAR(255) UNIQUE NOT NULL,
    # username VARCHAR(50) UNIQUE NOT NULL,
    # name VARCHAR(100) NOT NULL,
    # password_hash TEXT NOT NULL,
    # latitude DECIMAL(9,6),
    # longitude DECIMAL(9,6),
    # type VARCHAR(20) CHECK (type IN ('artist', 'normal')) NOT NULL,
    # created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    
  "users":[
    {"id": 1,
     "email": "gustavolima@gmail.com",
     "username": "Gustavo Lima",
     "name": "Nivaldo Batista Lima",
     "password_hash": "123",
     "latitude": 35.5,
     "longitude": 40,
     "type": "artist",
     "created_at": "2025-08-15"},

    # {"id": 2, "name": "Bob"},
  ],
  "artists": [],
  "musics": [
      {
        "id": 1, 
        "title": "Tchereretchetche",
        "description": "Gustavo Lima e você!",
        "artist_id": 1,
        "duration": "4.38 min",
        "posted_at": "2025-09-09", 
      },
  ],
  
}