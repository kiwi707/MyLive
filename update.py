import subprocess
import datetime

# --- 配置区 ---
MY_NAME = "老杨TV"
# 建议先用这个 GitHub 原生链接测试，因为它是你仓库里真实存在的
LOGO_URL = "https://raw.githubusercontent.com/kiwi707/MyLive/main/logo.png"

CATEGORIES = {
    "新闻资讯": {
        "TVBS-新闻": "https://www.youtube.com/@TVBSNEWS01/live",
        "东森-新闻": "https://www.youtube.com/@newsebc/live",
        "凤凰-资讯": "https://www.youtube.com/@凤凰卫视PhoenixTV/live",
        "CCTV-4": "https://www.youtube.com/@CCTVChinese/live"
    },
    "英语学习": {
        "CNA-24小时": "https://www.youtube.com/@CNA/live",
        "Sky-News": "https://www.youtube.com/@SkyNews/live"
    },
    "音乐轮播": {
        "Lofi-Girl": "https://www.youtube.com/@LofiGirl/live"
    }
}

def get_m3u8(url):
    try:
        result = subprocess.check_output([
            "yt-dlp", "--quiet", "--no-warnings", "--live-from-start", "-g", url
        ], stderr=subprocess.STDOUT).decode('utf-8').strip()
        return result
    except:
        return None

def main():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 头部：加入作者和更新时间信息
    m3u_content = f'#EXTM3U x-tvg-url="" x-author="{MY_NAME}"\n'
    
    # --- 1. 制作信息 (带 LOGO) ---
    # 注意这里：tvg-logo 必须紧跟在 #EXTINF:-1 后面
    m3u_content += f'#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="📢制作信息",🌟 {MY_NAME} 的专属源\n'
    m3u_content += f'http://0.0.0.0/welcome.mp4\n'
    
    m3u_content += f'#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="📢制作信息",🕒 更新时间：{now}\n'
    m3u_content += f'http://0.0.0.0/time.mp4\n'

    # --- 2. 频道抓取 (带 LOGO) ---
    for cat, channels in CATEGORIES.items():
        for name, url in channels.items():
            print(f"正在抓取: {name}")
            real_link = get_m3u8(url)
            if real_link:
                # 同样在频道列表里也加上 LOGO
                m3u_content += f'#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="{cat}",{name}\n{real_link}\n'
    
    with open("live.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print(f"✅ 完成！Logo已写入：{LOGO_URL}")

if __name__ == "__main__":
    main()
