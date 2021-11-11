from selenium import webdriver


class Request:
    def setup_method(self):
        path_to_gecko = '/usr/local/bin/geckodriver'
        self.driver = webdriver.Firefox(executable_path=path_to_gecko)
        self.vars = {}

    def teardown_method(self):
        self.driver.quit()
