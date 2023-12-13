from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

train = "https://static.independent.co.uk/2022/03/31/00/d0b722b78358bd1ddf031c75bdf52512Y29udGVudHNlYXJjaGFwaSwxNjQ4NzI3NDU3-2.42274411.jpg"
shuttle = "https://media-cldnry.s-nbcnews.com/image/upload/t_nbcnews-fp-1200-630,f_auto,q_auto:best/MSNBC/Components/Photo/_new/121002_AtlantisPhoto-1045a_files.jpg"
submarine = "https://anna-news.info/wp-content/uploads/2020/06/20/1400/nuclear-submarine-traveling-underwater-e1592642849265.jpg"

def test_get():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Use POST + url to JPG image for recognition."}

def test_post_submarine():
    response = client.post("/",
        params={"url": submarine}
    )

    json_data = response.json()
    assert response.status_code == 200
    assert "submarine 0.86" in str(json_data)

def test_post_train():
    response = client.post("/",
        params={"url": train}
    )

    json_data = response.json()
    assert response.status_code == 200
    assert "electric_locomotive 0.22" in str(json_data)

def test_post_shuttle():
    response = client.post("/",
        params={"url": shuttle}
    )

    json_data = response.json()
    assert response.status_code == 200
    assert "space_shuttle 0.85" in str(json_data)