import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="module")
def mock_driver(request):
  chrome_options = Options()
  chrome_options.add_argument("--headless")

  def finalizer():
    mock_driver.quit()
    print("mock driver closed")
  
  request.addfinalizer(finalizer)
  return webdriver.Chrome(options=chrome_options)
