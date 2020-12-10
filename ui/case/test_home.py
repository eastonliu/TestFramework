#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time   : 2020/7/27 17:31
# @Author : Eastonliu
# @Desc   :

import unittest
from selenium import webdriver
from time import sleep
from common import GOOGLE_DRIVER, URL, USERNAME, PASSWORD, CONFIG_FILE
from ui.page.loginPage import LoginPage
from ui.page.homePage import HomePage
from common.operatedb import OperatorMysql
from common.readYaml import YamlReader


class TestHome(unittest.TestCase):
    """
    工作台页面功能
    """
    driver = webdriver.Chrome(executable_path=GOOGLE_DRIVER)

    @classmethod
    def setUpClass(cls) -> None:
        login_page = LoginPage(cls.driver)
        login_page.get(URL)
        cls.driver.maximize_window()
        login_page.login(username=USERNAME, password=PASSWORD)
        sleep(3)
        cls.page = HomePage(cls.driver)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()

    def test_001(self):
        """
        建筑健康状况显示
        :return:
        """
        elms = self.page.build_health
        health_list = [elm.text for elm in elms]
        self.assertEqual(len(health_list), 3)
        self.assertIn(health_list[0], self.page.health_status)
        self.assertIn(health_list[1], self.page.health_status)
        self.assertIn(health_list[2], self.page.health_status)

    def test_002(self):
        """
        设备运行状态占比显示
        :return:
        """
        total_nums = int(self.page.device_nums.text)
        device_status = self.page.device_status
        online_device_nums = int(device_status[0].text.split(' ')[1])
        offline_device_nums = int(device_status[1].text.split(' ')[1])
        trouble_device_nums = int(device_status[2].text.split(' ')[1])
        # 查询所有设备信息
        sql = 'select * from t_device;'
        config = YamlReader(CONFIG_FILE).data['mysql']
        ds_dbname = YamlReader(CONFIG_FILE).data['ds'].get('dbname')
        config['db'] = ds_dbname
        db = OperatorMysql(config)
        values = db.executesql(sql).fetchall()
        db.closedb()
        self.assertEqual(total_nums, len(values))
        self.assertEqual(online_device_nums, len(list(filter(lambda value: value.get("ONLINE_STATUS") == 1, values))))
        self.assertEqual(offline_device_nums, len(list(filter(lambda value: value.get("ONLINE_STATUS") == 0, values))))
        self.assertEqual(trouble_device_nums, len(list(filter(lambda value: value.get("STATUS") == 3, values))))

    def test_003(self):
        """
        快捷入口显示
        :return:
        """
        elms = self.page.quick_entry
        quick_entry_text = list(map(lambda elm: elm.text, elms))
        self.assertIsNotNone(quick_entry_text)


if __name__ == '__main__':
    unittest.main(verbosity=2)
