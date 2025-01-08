import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="session")
def mock_driver():
  chrome_options = Options()
  chrome_options.add_argument("--headless")

  driver = webdriver.Chrome(options=chrome_options)
  yield driver

  driver.quit()
  print("mock driver closed")
  
  '''
  def finalizer():
      mock_driver.quit()
      print("mock driver closed")
  request.addfinalizer(finalizer)
  '''
  
  
  
