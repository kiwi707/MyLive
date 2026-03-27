import subprocess
import datetime

MY_NAME = "老杨TV"
LOGO_URL = "https://raw.githubusercontent.com/kiwi707/MyLive/main/logo.png"

CATEGORIES = {
    "新闻资讯": {
        "TVBS-新闻": "https://www.youtube.com/@TVBSNEWS01/live",
        "东森-新闻": "https://www.youtube.com/@newsebc/live",
        "凤凰-资讯": "https://www.youtube.com/@凤凰卫视PhoenixTV/live" # 换成了凤凰卫视，避开美国IP封锁
    },
    "音乐轮播": {
        "Lofi-Girl": "https://www.youtube.com/@LofiGirl/live"
    }
}

def get_m3u8(url):
    try:
        # 更换伪装策略：这次伪装成苹果 iOS 客户端，避开网页版的机器人检测
        cmd = [
            "yt-dlp", 
            "--live-from-start",
            "--extractor-args", "youtube:player_client=ios", # <--- 核心修改：伪装成苹果设备
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
