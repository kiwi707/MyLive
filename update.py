import subprocess
import datetime

# 【配置区】按你的喜好修改分类和频道
CATEGORIES = {
    "新闻资讯": {
        "TVBS-新闻": "https://www.youtube.com/@TVBSNEWS01/live",
        "东森-新闻": "https://www.youtube.com/@newsebc/live",
        "CCTV-4": "https://www.youtube.com/@CCTVChinese/live"
    },
    "英语学习": {
        "CNA-24小时": "https://www.youtube.com/@CNA/live",
        "BBC-World": "https://www.youtube.com/@BBCNews/live"
    },
    "音乐轮播": {
        "Lofi-Girl": "https://www.youtube.com/@LofiGirl/live"
    }
}

def get_m3u8(url):
    try:
        # 使用 yt-dlp 抓取最高画质地址
        result = subprocess.check_output([
            "yt-dlp", "--quiet", "--no-warnings", "-g", url
        ]).decode('utf-8').strip()
        return result
    except:
        return None

def main():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    m3u_content = f'#EXTM3U x-tvg-url=""\n'
    
    # 个人信息置顶
    m3u_content += f'#EXTINF:-1 group-title="📢制作信息",🌟 郑州老王的专属源\n'
    m3u_content += f'http://0.0.0.0/info.mp4\n'
    m3u_content += f'#EXTINF:-1 group-title="📢制作信息",🕒 更新时间：{now}\n'
    m3u_content += f'http://0.0.0.0/time.mp4\n'

    for cat, channels in CATEGORIES.items():
        for name, url in channels.items():
            print(f"正在抓取: {name}")
            real_link = get_m3u8(url)
            if real_link:
                m3u_content += f'#EXTINF:-1 group-title="{cat}",{name}\n{real_link}\n'
    
    with open("live.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)

if __name__ == "__main__":
    main()
