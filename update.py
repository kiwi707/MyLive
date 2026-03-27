import subprocess
import datetime
import os

MY_NAME = "老杨TV"
LOGO_URL = "https://raw.githubusercontent.com/kiwi707/MyLive/main/logo.png"

CATEGORIES = {
    "新闻资讯": {
        "TVBS-新闻": "https://www.youtube.com/@TVBSNEWS01/live",
        "东森-新闻": "https://www.youtube.com/@newsebc/live",
        "半岛-新闻": "https://www.youtube.com/@aljazeeraenglish/live"
    },
    "音乐轮播": {
        "Lofi-Girl": "https://www.youtube.com/@LofiGirl/live"
    }
}

def get_m3u8(url):
    try:
        # 修复：将 nodejs 改为它能识别的 node
        cmd = [
            "yt-dlp", 
            "--js-runtimes", "node",  # <--- 就是这里，去掉了 js 两个字母
            "--cookies", "cookies.txt", 
            "--live-from-start",
            "-g", 
            url
        ]
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8').strip()
        print(f"  -> ✅ 成功拿到链接: {result[:40]}...")
        return result
    except subprocess.CalledProcessError as e:
        error_msg = e.output.decode('utf-8').strip()
        print(f"  -> ❌ 抓取失败: {error_msg}")
        return None
    except Exception as e:
        print(f"  -> ❌ 未知错误: {e}")
        return None

def main():
    if not os.path.exists("cookies.txt"):
        print("⚠️ 警告：未找到 cookies.txt 文件，抓取可能会被拦截！")

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    m3u_content = f'#EXTM3U x-tvg-url="" x-author="{MY_NAME}"\n'
    
    m3u_content += f'#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="📢制作信息",🌟 {MY_NAME} 的专属源\n'
    m3u_content += f'http://0.0.0.0/welcome.mp4\n'
    m3u_content += f'#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="📢制作信息",🕒 更新时间：{now}\n'
    m3u_content += f'http://0.0.0.0/time.mp4\n'

    for cat, channels in CATEGORIES.items():
        for name, url in channels.items():
            print(f"正在抓取: {name}")
            real_link = get_m3u8(url)
            if real_link and "m3u8" in real_link:
                m3u_content += f'#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="{cat}",{name}\n{real_link}\n'
    
    with open("live.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print(f"\n✅ 运行完毕！")

if __name__ == "__main__":
    main()
