import subprocess
import datetime

# --- 配置区 ---
MY_NAME = "老杨TV"
LOGO_URL = "https://raw.githubusercontent.com/kiwi707/MyLive/main/logo.png"

CATEGORIES = {
    "新闻资讯": {
        "TVBS-新闻": "https://www.youtube.com/@TVBSNEWS01/live",
        "东森-新闻": "https://www.youtube.com/@newsebc/live",
        "CCTV-4": "https://www.youtube.com/@CCTVChinese/live"
    },
    "音乐轮播": {
        "Lofi-Girl": "https://www.youtube.com/@LofiGirl/live"
    }
}

def get_m3u8(url):
    try:
        # 加入伪装成安卓客户端的参数，专门对抗 YouTube 拦截
        cmd = [
            "yt-dlp", 
            "--live-from-start",
            "--extractor-args", "youtube:player_client=android", # 绕过拦截的核心
            "-g", 
            url
        ]
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8').strip()
        # 如果成功，打印出链接的前 40 个字符看看
        print(f"  -> ✅ 成功拿到链接: {result[:40]}...")
        return result
    except subprocess.CalledProcessError as e:
        # 如果失败，把 YouTube 的真实报错原因打印出来
        error_msg = e.output.decode('utf-8').strip()
        print(f"  -> ❌ 抓取失败: {error_msg}")
        return None
    except Exception as e:
        print(f"  -> ❌ 未知错误: {e}")
        return None

def main():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    m3u_content = f'#EXTM3U x-tvg-url="" x-author="{MY_NAME}"\n'
    
    # --- 1. 制作信息 ---
    m3u_content += f'#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="📢制作信息",🌟 {MY_NAME} 的专属源\n'
    m3u_content += f'http://0.0.0.0/welcome.mp4\n'
    m3u_content += f'#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="📢制作信息",🕒 更新时间：{now}\n'
    m3u_content += f'http://0.0.0.0/time.mp4\n'

    # --- 2. 频道抓取 ---
    for cat, channels in CATEGORIES.items():
        for name, url in channels.items():
            print(f"正在抓取: {name} ({url})")
            real_link = get_m3u8(url)
            if real_link and "m3u8" in real_link:
                m3u_content += f'#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="{cat}",{name}\n{real_link}\n'
    
    with open("live.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print(f"\n✅ 运行完毕！文件已更新。")

if __name__ == "__main__":
    main()
