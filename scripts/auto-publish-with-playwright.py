import os
import json
import time
import logging
import argparse
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class XiaohongshuPoster:
    def __init__(self, path=os.path.dirname(os.path.abspath(__file__))):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context(permissions=['geolocation'])
        self.page = self.context.new_page()
        
        # 获取当前执行文件所在目录
        current_dir = path
        self.token_file = os.path.join(current_dir, "xiaohongshu_token.json")
        self.cookies_file = os.path.join(current_dir, "xiaohongshu_cookies.json")
        self.token = self._load_token()
        self._load_cookies()

    def _set_local_storage_item(self, key, value):
        self.page.evaluate(f"() => localStorage.setItem('{key}', '{value}')")

    def _load_token(self):
        """从文件加载token"""
        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, 'r') as f:
                    token_data = json.load(f)
                    # 检查token是否过期
                    if token_data.get('expire_time', 0) > time.time():
                        return token_data.get('token')
            except:
                pass
        return None

    def _save_token(self, token):
        """保存token到文件"""
        token_data = {
            'token': token,
            # token有效期设为30天
            'expire_time': time.time() + 30 * 24 * 3600
        }
        with open(self.token_file, 'w') as f:
            json.dump(token_data, f)

    def _load_cookies(self):
        """从文件加载cookies"""
        if os.path.exists(self.cookies_file):
            try:
                with open(self.cookies_file, 'r') as f:
                    cookies = json.load(f)
                    self.page.goto("https://creator.xiaohongshu.com")
                    self.context.add_cookies(cookies)
            except:
                pass

    def _save_cookies(self):
        """保存cookies到文件"""
        cookies = self.context.cookies()
        with open(self.cookies_file, 'w') as f:
            json.dump(cookies, f)

    def login_to_publish_image(self, title, content, images=None, slow_mode=False):
        print(f"开始发布图文")
        logger.info(f"开始发布图文")
        self._load_cookies()
        
        self.page.goto("https://creator.xiaohongshu.com/publish/publish?from=menu&target=image")
        time.sleep(3)
        self._set_local_storage_item('creator-short-note-guide-v2', 'true')
        self._set_local_storage_item('draft-tooltip-guide', 'true')
        self._set_local_storage_item('creator-new-publish', 'true')
        self.page.reload()
        time.sleep(5)

        # 上传图片
        if images:
            self.page.wait_for_selector(".upload-input", timeout=30000)
            # 直接传入图片路径列表
            self.page.locator(".upload-input").set_input_files(images)
            time.sleep(5)

        title = title[:20]
        self.page.wait_for_selector(".d-text", timeout=30000)
        self.page.get_by_placeholder("填写标题会有更多赞哦～").fill(title)

        # Start of Selection
        print(content)
        content = content[:1000]
        self.page.wait_for_selector(".tiptap")
        self.page.locator(".editor-content .tiptap").fill(content)
        
        # 发布
        if slow_mode:
            time.sleep(5)
        time.sleep(5)
        self.page.locator(".publishBtn").click(force=True)
        self.page.wait_for_url("https://creator.xiaohongshu.com/publish/success*")
        print('图文发布成功')
        return True, "图文发布成功"

    def login_to_publish_video(self, title, content, videos=None, slow_mode=False):
        print(f"开始发布视频")
        logger.info(f"开始发布视频")
        self._load_cookies()
        
        self.page.goto("https://creator.xiaohongshu.com/publish/publish?from=menu&target=video")
        self._set_local_storage_item('creator-short-note-guide-v2', 'true')
        self._set_local_storage_item('draft-tooltip-guide', 'true')
        self._set_local_storage_item('creator-new-publish', 'true')
        self.page.reload()

        # 上传视频
        if videos:
            self.page.wait_for_selector(".upload-input")
            # 直接传入路径列表
            self.page.locator(".upload-input").set_input_files(videos)
            time.sleep(1)
        
        title = title[:20]
        self.page.wait_for_selector(".d-text", timeout=30000)
        self.page.get_by_placeholder("填写标题会有更多赞哦～").fill(title)

        # Start of Selection
        print(content)
        content = content[:1000]
        self.page.wait_for_selector(".tiptap")
        self.page.locator(".editor-content .tiptap").fill(content)
        
        # 发布
        if slow_mode:
            time.sleep(5)
        time.sleep(5)
        self.page.locator(".publishBtn").click(force=True)
        self.page.wait_for_url("https://creator.xiaohongshu.com/publish/success*")
        print('视频发布成功')
        return True, "视频发布成功"

    def close(self):
        """关闭浏览器"""
        self.context.close()
        self.browser.close()
        self.playwright.stop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def login(self, phone, country_code="+86"):
        """登录小红书"""
        # 如果token有效则直接返回
        if self.token:
            return

        # 尝试加载cookies进行登录
        self.page.goto("https://creator.xiaohongshu.com/login")
        self._load_cookies()
        self.page.reload()
        time.sleep(5)
        # 检查是否已经登录
        if self.page.url != "https://creator.xiaohongshu.com/new/home":
            print("使用cookies登录成功")
            self.token = self._load_token()
            self._save_cookies()
            time.sleep(2)
            return
        else:
            # 清理无效的cookies
            self.context.clear_cookies()
            print("无效的cookies，已清理")

        # 如果cookies登录失败，则进行手动登录
        self.page.goto("https://creator.xiaohongshu.com/login")

        # 等待登录页面加载完成
        time.sleep(5)
        # 点击国家区号输入框
        skip = True
        if not skip:
            country_input = self.page.wait_for_selector("input[placeholder='请选择选项']")
            country_input.click()
            time.sleep(30)
            # 等待区号列表出现并点击+86

            try:
                self.page.locator("/html/body/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div/div/div/div/div[2]/div[1]/div[1]/div/div/div[1]/input").click()
                time.sleep(2)
                self.page.locator("/html/body/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div/div/div/div/div[2]/div[1]/div[1]/div/div/div[1]/input").fill(country_code)
                time.sleep(2)
                self.page.locator("/html/body/div[6]/div/div").click()
                time.sleep(2)
            except Exception as e:
                print("无法找到国家区号选项")
                print(e)

        # 定位手机号输入框
        phone_input = self.page.wait_for_selector("input[placeholder='手机号']")
        phone_input.fill(phone)

        # 点击发送验证码按钮
        try:
            send_code_btn = self.page.wait_for_selector(".css-uyobdj", state="visible")
            send_code_btn.click()
        except:
            # 尝试其他可能的选择器
            try:
                send_code_btn = self.page.wait_for_selector(".css-1vfl29", state="visible")
                send_code_btn.click()
            except:
                try:
                    send_code_btn = self.page.locator("//button[contains(text(),'发送验证码')]")
                    send_code_btn.click()
                except:
                    print("无法找到发送验证码按钮")

        # 输入验证码
        verification_code = input("请输入验证码: ")
        code_input = self.page.wait_for_selector("input[placeholder='验证码']")
        code_input.fill(verification_code)

        # 点击登录按钮
        login_button = self.page.wait_for_selector(".beer-login-btn", state="visible")
        login_button.click()

        # 等待登录成功,获取token
        time.sleep(3)
        # 保存cookies
        self._save_cookies()

        # 关闭浏览器
        # self.close()


def main():
    parser = argparse.ArgumentParser(description="小红书自动发布工具")
    subparsers = parser.add_subparsers(dest="command", help="子命令", required=True)

    # login 子命令
    login_parser = subparsers.add_parser("login", help="登录小红书")

    # login_to_publish_image 子命令
    publish_image_parser = subparsers.add_parser("login_to_publish_image", help="登录并发布图文")
    publish_image_parser.add_argument("--title", "-t", type=str, required=True, help="标题 (最多20字)")
    publish_image_parser.add_argument("--content", "-c", type=str, required=True, help="正文内容")
    publish_image_parser.add_argument("--images", "-i", type=str, nargs="+", help="图片路径列表")
    publish_image_parser.add_argument("--slow-mode", "-s", action="store_true", help="慢速模式 (发布前等待5秒)")

    # login_to_publish_video 子命令
    publish_video_parser = subparsers.add_parser("login_to_publish_video", help="登录并发布视频")
    publish_video_parser.add_argument("--title", "-t", type=str, required=True, help="标题 (最多20字)")
    publish_video_parser.add_argument("--content", "-c", type=str, required=True, help="正文内容")
    publish_video_parser.add_argument("--videos", "-v", type=str, nargs="+", help="视频路径列表")
    publish_video_parser.add_argument("--slow-mode", "-s", action="store_true", help="慢速模式 (发布前等待5秒)")

    args = parser.parse_args()

    # 加载 .env 文件
    load_dotenv()

    with XiaohongshuPoster() as poster:
        if args.command == "login":
            phone = os.getenv("XHS_PHONE")
            country_code = os.getenv("XHS_COUNTRY_CODE", "+86")
            poster.login(phone, country_code)
        elif args.command == "login_to_publish_image":
            poster.login_to_publish_image(args.title, args.content, args.images, args.slow_mode)
        elif args.command == "login_to_publish_video":
            poster.login_to_publish_video(args.title, args.content, args.videos, args.slow_mode)


if __name__ == "__main__":
    main()
