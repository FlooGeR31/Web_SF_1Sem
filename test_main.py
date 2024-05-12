import json
from pathlib import Path

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

train = "https://static.independent.co.uk/2022/03/31/00/" + \
    "d0b722b78358bd1ddf031c75bdf52512Y29udGVudHNlYXJjaGFwaSwxNjQ4NzI3NDU3" + \
    "-2.42274411.jpg"
shuttle = "https://media-cldnry.s-nbcnews.com/image/upload/" + \
    "t_nbcnews-fp-1200-630,f_auto,q_auto:best/MSNBC/Components/" + \
    "Photo/_new/121002_AtlantisPhoto-1045a_files.jpg"
submarine = "https://anna-news.info/wp-content/uploads/2020/06/20/1400/" + \
    "nuclear-submarine-traveling-underwater-e1592642849265.jpg"
# tram "Results: streetcar 0.74; passenger_car 0.23;
# electric_locomotive 0.02"
# shuttle "Results: space_shuttle 0.96; warplane 0.01; airliner 0.0"
# submarine "Results: submarine 0.89; missile 0.01; projectile 0.01"


def test_get():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message":
                               "Use POST + url to JPG image for recognition."}


def test_post_submarine():
    response = client.post("/",
                           params={"url": submarine}
                           )

    json_data = response.json()
    data_cleaning(submarine)
    assert response.status_code == 200
    assert "submarine 0.58" in str(json_data)


def test_post_train():
    response = client.post("/",
                           params={"url": train}
                           )

    json_data = response.json()
    data_cleaning(train)
    assert response.status_code == 200
    assert "electric_locomotive 0.23" in str(json_data)


def test_post_shuttle():
    response = client.post("/",
                           params={"url": shuttle}
                           )

    json_data = response.json()
    data_cleaning(shuttle)
    assert response.status_code == 200
    assert "space_shuttle 0.84" in str(json_data)


def test_get_all_data():
    response = client.get("/base/")
    assert response.status_code == 200
    assert Path("./base.json").is_file()
    with open(Path("./base.json"), 'r') as openfile:
        datafile_content = json.load(openfile)
    print(response.json())
    print(datafile_content)
    assert response.json() == datafile_content


def test_not_image_url():
    response = client.post("/",
                           params={"url": "not_a_url"}
                           )
    assert response.status_code == 200
    assert response.json() == "This is not image."


def data_cleaning(url):
    datafile_path = Path("./base.json")
    if datafile_path.is_file():
        with open(datafile_path, 'r+') as f:
            datafile_content = json.load(f)
            if url in datafile_content:
                del datafile_content[url]
            f.seek(0)
            f.write(json.dumps(datafile_content, sort_keys=True, indent=4))
            f.truncate()
