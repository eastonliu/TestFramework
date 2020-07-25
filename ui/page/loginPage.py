#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time   : 2020/7/6 17:20
# @Author : Eastonliu
# @Desc   :

import os
from PIL import Image
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from common import STATIC_PATH
from ui.baseobject.page import Page
from ui.baseobject.pageobject import PageElement

# 原始图片保存路径
template_path = os.path.join(STATIC_PATH, 'image', 'templateimage')
# 截图图片保存路径
captcha_path = os.path.join(STATIC_PATH, 'image', 'tmpimage')


class LoginPage(Page):
    captcha_image = PageElement(id_='scream', describe='拼图图片')
    re_btn = PageElement(class_name='re-btn', describe='图片刷新按钮')
    slider_btn = PageElement(class_name='slider-btn', describe='滑块按钮')
    username_input = PageElement(id_='username', describe='用户名输入框')
    password_input = PageElement(id_='password', describe='密码输入框')
    submit_btn = PageElement(name='submit', describe='登录按钮')
    msg_tips = PageElement(class_name='msg-tips', describe='滑块提示信息')
    msg_login = PageElement(css='div.alert', describe='登录结果提示信息')

    def get_snap(self):
        """
        对整个登录网页截图
        :return:网页截图对象
        """
        self.driver.get_screenshot_as_file(os.path.join(captcha_path, 'fullimage.png'))
        page_snap_obj = Image.open(os.path.join(captcha_path, 'fullimage.png'))
        return page_snap_obj

    def get_captcha_image(self):
        """
        从登录页面截图中，截取验证码图片
        :return:验证码图片对象
        """
        location = self.captcha_image.location  # 验证图在网页中的位置
        size = self.captcha_image.size  # 验证图的图片大小
        top = location['y']
        bottom = location['y'] + size['height']
        left = location['x']
        right = location['x'] + size['width']
        page_snap_obj = self.get_snap()
        crop_imag_obj = page_snap_obj.crop((left, top, right, bottom))
        crop_imag_obj.save(os.path.join(STATIC_PATH, 'image', 'tmpimage', 'obj.png'))
        return crop_imag_obj

    def get_template_image(self):
        """
        和本地的原始图片库对比，找出原始图,任意取两个点，对比RGB，RGB差值在一定范围内，就认为两张图一样
        :return: 原始图对象
        """
        diff = 10
        captcha_image_obj = self.get_captcha_image()
        template_images = os.listdir(template_path)
        for image in template_images:
            image_obj = Image.open(template_path + "/" + image)
            captcha_image_point1 = captcha_image_obj.getpixel((200, 130))
            image_obj_point1 = image_obj.getpixel((200, 130))
            captcha_image_point2 = captcha_image_obj.getpixel((330, 130))
            image_obj_point2 = image_obj.getpixel((330, 130))
            condition1 = abs(captcha_image_point1[0] - image_obj_point1[0]) < diff and abs(
                captcha_image_point1[1] - image_obj_point1[1]) < diff and abs(
                captcha_image_point1[2] - image_obj_point1[2]) < diff
            condition2 = abs(captcha_image_point2[0] - image_obj_point2[0]) < diff and abs(
                captcha_image_point2[1] - image_obj_point2[1]) < diff and abs(
                captcha_image_point2[2] - image_obj_point2[2]) < diff
            if condition1 and condition2:
                return image_obj
        return None

    def get_distance(self, template_image, captcha_image):
        """
        获取滑块到缺口的距离，通过对比原始图和验证码图RGB差值，找到缺口位置
        :param template_image:原始图对象
        :param captcha_image:验证码图对象
        :return:滑块到缺口的距离
        """
        diff = 60
        left = 10  # 验证图最左边到滑块的距离
        for i in range(50, template_image.size[0]):
            for j in range(10, template_image.size[1]):
                pixel1 = template_image.getpixel((i, j))
                pixel2 = captcha_image.getpixel((i, j))
                if abs(pixel1[0] - pixel2[0]) >= diff and abs(pixel1[1] - pixel2[1]) >= diff and abs(
                        pixel1[2] - pixel2[2]) >= diff:
                    return i - left - 4
        return 20

    def get_tracks(self, distance):
        """
        拿到移动轨迹，模仿人的滑动行为，先匀加速后匀减速
        匀变速运动基本公式：
        ①v=v0+at
        ②s=v0t+½at²
        ③v²-v0²=2as

        :param distance: 需要移动的距离
        :return: 轨迹列表
        """
        # 初速度
        v = 0
        # 单位时间为0.2s来统计轨迹，轨迹即0.2内的位移
        t = 0.3
        # 位移/轨迹列表，列表内的一个元素代表0.2s的位移
        tracks = []
        # 当前的位移
        current = 0
        # 到达mid值开始减速
        mid = distance * 4 / 5

        while current < distance:
            if current < mid:
                # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
                a = 2
            else:
                a = -3
            # 初速度
            v0 = v
            # 0.2秒时间内的位移
            s = v0 * t + 0.5 * a * (t ** 2)
            # 当前的位置
            current += s
            # 添加到轨迹列表
            tracks.append(round(s))
            # 速度已经达到v,该速度作为下次的初速度
            v = v0 + a * t
        return tracks

    def drag_captcha(self):
        """
        拖动滑块验证
        :return:
        """
        template_image = self.get_template_image()
        while not template_image:
            ActionChains(self.driver).click(self.re_btn).perform()
            template_image = self.get_template_image()
        captcha_image = self.get_captcha_image()
        distance = self.get_distance(template_image, captcha_image)
        tracks = self.get_tracks(distance)
        slide_block = self.slider_btn
        ActionChains(self.driver).click_and_hold(slide_block).perform()
        sleep(0.2)
        # 根据轨迹拖拽圆球
        for track in tracks:
            ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()
        else:
            ActionChains(self.driver).move_by_offset(xoffset=3, yoffset=0).perform()
            ActionChains(self.driver).move_by_offset(xoffset=-3, yoffset=0).perform()

        sleep(0.5)  # 0.5秒后释放鼠标
        ActionChains(self.driver).release().perform()
        sleep(3)
        result_text = self.msg_tips.text
        if result_text != "验证成功":
            ActionChains(self.driver).click(self.re_btn).perform()
            self.drag_captcha()
        return None

    def login(self, username, password):
        """
        登录
        :param username:用户名
        :param password:密码
        :return:
        """
        self.username_input.send_keys(username)
        self.password_input.send_keys(password)
        self.drag_captcha()
        self.submit_btn.click()
