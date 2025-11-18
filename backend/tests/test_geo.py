import pytest
from backend.utils.geo import _haversine_km
from backend.services.geo import recommend_geo
from unittest.mock import MagicMock, patch

# Unit tests for _haversine_km
def test_haversine_km_same_location():
    """Test haversine distance for the same location should be 0."""
    lat1, lon1 = 0.0, 0.0
    lat2, lon2 = 0.0, 0.0
    distance = _haversine_km(lat1, lon1, lat2, lon2)
    assert distance == 0.0

def test_haversine_km_known_distance():
    """Test haversine distance for two known locations (e.g., equator points)."""
    # Distance between (0,0) and (0, 1 degree longitude) is approx 111.3 km
    # Using a more precise example: New York to London is approx 5570 km
    # For simplicity, let's use a smaller, easily verifiable distance
    # Distance between two points on the equator 1 degree apart is ~111.32 km
    lat1, lon1 = 0.0, 0.0
    lat2, lon2 = 0.0, 1.0
    distance = _haversine_km(lat1, lon1, lat2, lon2)
    assert abs(distance - 111.319) < 0.2 # Approximately 111.319 km

def test_haversine_km_antipodal_points():
    """Test haversine distance for antipodal points (half circumference of Earth)."""
    # Distance between (0,0) and (0, 180) should be half circumference
    lat1, lon1 = 0.0, 0.0
    lat2, lon2 = 0.0, 180.0
    distance = _haversine_km(lat1, lon1, lat2, lon2)
    assert abs(distance - (2 * 6371 * 3.14159 / 2)) < 0.1 # Half circumference

# Integration tests for recommend_geo
@pytest.fixture
def mock_models():
    """Fixture to provide mock Peewee models."""
    User = MagicMock()
    Music = MagicMock()
    UserMusicRating = MagicMock()
    return User, Music, UserMusicRating

@pytest.fixture
def mock_user(mock_models):
    User, _, _ = mock_models
    user_instance = MagicMock()
    user_instance.id = 1
    user_instance.latitude = 34.052235
    user_instance.longitude = -118.243683
    User.get_or_none.return_value = user_instance
    return user_instance

@pytest.fixture
def mock_music_query(mock_models):
    User, Music, _ = mock_models
    
    mock_music_instance = MagicMock()
    mock_music_instance.id = 101
    mock_music_instance.title = "Test Song"
    mock_music_instance.artist_id = 2
    mock_music_instance.posted_at = "2023-01-01"
    mock_music_instance.latitude = 34.052235
    mock_music_instance.longitude = -118.243683
    mock_music_instance.artist.latitude = 34.052235 # Mock artist's latitude
    mock_music_instance.artist.longitude = -118.243683 # Mock artist's longitude
    
    mock_music_instance_far = MagicMock()
    mock_music_instance_far.id = 102
    mock_music_instance_far.title = "Far Song"
    mock_music_instance_far.artist_id = 3
    mock_music_instance_far.posted_at = "2023-01-02"
    mock_music_instance_far.latitude = 35.0
    mock_music_instance_far.longitude = -119.0
    mock_music_instance_far.artist.latitude = 35.0 # Mock artist's latitude
    mock_music_instance_far.artist.longitude = -119.0 # Mock artist's longitude
    
    mock_query_result = MagicMock()
    mock_query_result.__iter__.return_value = [mock_music_instance, mock_music_instance_far]
    
    # Mock the entire chain of calls for Music.select to return the mock_query_result
    Music.select.return_value.join.return_value.where.return_value.order_by.return_value.limit.return_value = mock_query_result
    return Music

@patch('backend.services.geo.recommend_popular')
def test_recommend_geo_user_not_found_falls_back_to_popular(mock_recommend_popular, mock_models):
    User, Music, UserMusicRating = mock_models
    User.get_or_none.return_value = None
    
    mock_recommend_popular.return_value = [{"id": 1, "title": "Popular Song"}]
    
    result = recommend_geo(User=User, Music=Music, UserMusicRating=UserMusicRating, user_id=999)
    
    mock_recommend_popular.assert_called_once_with(User=User, Music=Music, UserMusicRating=UserMusicRating, user_id=999, limit=10)
    assert result == [{"id": 1, "title": "Popular Song"}]

@patch('backend.services.geo.recommend_popular')
def test_recommend_geo_user_no_location_falls_back_to_popular(mock_recommend_popular, mock_models):
    User, Music, UserMusicRating = mock_models
    user_instance = MagicMock()
    user_instance.id = 1
    user_instance.latitude = None
    user_instance.longitude = None
    User.get_or_none.return_value = user_instance
    
    mock_recommend_popular.return_value = [{"id": 1, "title": "Popular Song"}]
    
    result = recommend_geo(User=User, Music=Music, UserMusicRating=UserMusicRating, user_id=1)
    
    mock_recommend_popular.assert_called_once_with(User=User, Music=Music, UserMusicRating=UserMusicRating, user_id=1, limit=10)
    assert result == [{"id": 1, "title": "Popular Song"}]

def test_recommend_geo_haversine_within_radius(mock_models, mock_user, mock_music_query, monkeypatch):
    User, Music, UserMusicRating = mock_models
    UserMusicRating.select.return_value.where.return_value = [] # No rated music
    
    mock_haversine = MagicMock(return_value=5.0)
    monkeypatch.setattr('backend.utils.geo._haversine_km', mock_haversine)
    
    result = recommend_geo(User=User, Music=Music, UserMusicRating=UserMusicRating, user_id=1, radius_km=10.0, limit=1, method="haversine")
    mock_haversine.assert_called()
    assert len(result) == 1
    assert result[0]["id"] == 101
    assert result[0]["distance_km"] == 5.0

def test_recommend_geo_haversine_outside_radius(mock_models, mock_user, mock_music_query, monkeypatch):
    User, Music, UserMusicRating = mock_models
    UserMusicRating.select.return_value.where.return_value = [] # No rated music
    
    mock_haversine = MagicMock(return_value=15.0)
    monkeypatch.setattr('backend.utils.geo._haversine_km', mock_haversine)
    
    with patch('backend.services.geo.recommend_popular', return_value=[{"id": 200, "title": "Fallback Song"}]) as mock_popular:
        result = recommend_geo(User=User, Music=Music, UserMusicRating=UserMusicRating, user_id=1, radius_km=10.0, limit=1, method="haversine")
        mock_haversine.assert_called()
        mock_popular.assert_called_once()
        assert len(result) == 1
        assert result[0]["id"] == 200

@patch('backend.services.geo.recommend_popular')
def test_recommend_geo_haversine_fills_limit(mock_recommend_popular, mock_models, mock_user):
    User, Music, UserMusicRating = mock_models
    UserMusicRating.select.return_value.where.return_value = [] # No rated music

    # Mock Music.select to return only one music within radius
    mock_music_instance = MagicMock()
    mock_music_instance.id = 101
    mock_music_instance.title = "Close Song"
    mock_music_instance.artist_id = 2
    mock_music_instance.posted_at = "2023-01-01"
    mock_music_instance.latitude = 34.052235
    mock_music_instance.longitude = -118.243683
    
    mock_query_result = MagicMock()
    mock_query_result.__iter__.return_value = [mock_music_instance]
    Music.select.return_value.join.return_value.where.return_value.order_by.return_value.limit.return_value = mock_query_result

    mock_recommend_popular.return_value = [{"id": 200, "title": "Popular Song 1"}, {"id": 201, "title": "Popular Song 2"}]
    
    with patch('backend.utils.geo._haversine_km', return_value=5.0):
        result = recommend_geo(User=User, Music=Music, UserMusicRating=UserMusicRating, user_id=1, radius_km=10.0, limit=3)
        
        assert len(result) == 3
        assert result[0]["id"] == 101
        assert result[1]["id"] == 200
        assert result[2]["id"] == 201
        mock_recommend_popular.assert_called_once_with(user_id=1, limit=2)

@patch('backend.services.geo.recommend_popular')
def test_recommend_geo_haversine_no_duplicates_when_filling_limit(mock_recommend_popular, mock_models, mock_user):
    User, Music, UserMusicRating = mock_models
    UserMusicRating.select.return_value.where.return_value = [] # No rated music

    # Mock Music.select to return one music
    mock_music_instance = MagicMock()
    mock_music_instance.id = 101
    mock_music_instance.title = "Close Song"
    mock_music_instance.artist_id = 2
    mock_music_instance.posted_at = "2023-01-01"
    mock_music_instance.latitude = 34.052235
    mock_music_instance.longitude = -118.243683
    
    mock_query_result = MagicMock()
    mock_query_result.__iter__.return_value = [mock_music_instance]
    Music.select.return_value.join.return_value.where.return_value.order_by.return_value.limit.return_value = mock_query_result

    # popular recommendations include one music already found by geo
    mock_recommend_popular.return_value = [{"id": 101, "title": "Duplicate Song"}, {"id": 201, "title": "Popular Song 2"}]
    
    with patch('backend.utils.geo._haversine_km', return_value=5.0):
        result = recommend_geo(User=User, Music=Music, UserMusicRating=UserMusicRating, user_id=1, radius_km=10.0, limit=2)
        
        assert len(result) == 2
        assert result[0]["id"] == 101
        assert result[1]["id"] == 201
        mock_recommend_popular.assert_called_once_with(user_id=1, limit=1) # limit should be 1 because one was found by geo
