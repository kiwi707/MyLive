import subprocess
import datetime
import os

# 【配置区】按你的喜好修改分类和频道
# 建议使用 /live 结尾的链接，抓取最准
CATEGORIES = {
    "新闻资讯": {
        "TVBS-新闻": "https://www.youtube.com/@TVBSNEWS01/live",
        "东森-新闻": "https://www.youtube.com/@newsebc/live",
        "凤凰-资讯": "https://www.youtube.com/@凤凰卫视PhoenixTV/live",
        "CCTV-4": "https://www.youtube.com/@CCTVChinese/live"
    },
    "英语学习": {
        "CNA-24小时": "https://www.youtube.com/@CNA/live",
        "Bloomberg-财经": "https://www.youtube.com/@BloombergQuicktake/live",
        "Sky-News": "https://www.youtube.com/@SkyNews/live"
    },
    "音乐轮播": {
        "Lofi-Girl": "https://www.youtube.com/@LofiGirl/live",
        "Chillhop-Music": "https://www.youtube.com/@ChillhopMusic/live"
    },
    "景观太空": {
        "NASA-太空": "https://www.youtube.com/@NASA/live",
        "EarthCam-全球街景": "https://www.youtube.com/@EarthCam/live"
    }
}

# 你的个人信息配置
MY_NAME = "郑州老王"
LOGO_URL = "https://gitee.com/young9956/lytv/raw/master/logo.png"

def get_m3u8(url):
    """使用 yt-dlp 抓取最高画质的实时直播地址"""
    try:
        # -g 参数只返回地址，--live-from-start 确保从直播起始点抓取
        result = subprocess.check_output([
            "yt-dlp", 
            "--quiet", 
            "--no-warnings", 
            "--live-from-start",
            "-g", 
            url
        ], stderr=subprocess.STDOUT).decode('utf-8').strip()
        return result
    except Exception as e:
        print(f"解析失败 {url}: {e}")
        return None

def main():
    # 获取北京时间 (GitHub Actions 默认是 UTC 时间，这里简单处理)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # M3U 标准头部
    m3u_content = f'#EXTM3U x-tvg-url="" x-author="{MY_NAME}"\n'
    
    # 1. 个人信息置顶 (带 Logo)
    m3u_content += f'#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="📢制作信息",🌟 {MY_NAME} 的专属源\n'
    m3u_content += f'http://0.0.0.0/welcome.mp4\n'
    
    m3u_content += f'#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="📢制作信息",🕒 更新时间：{now}\n'
    m3u_content += f'http://0.0.0.0/time.mp4\n'

    # 2. 循环分类抓取频道
    for cat, channels in CATEGORIES.items():
        print(f"--- 正在处理分类: {cat} ---")
        for name, url in channels.items():
            print(f"正在抓取: {name}...")
            real_link = get_m3u8(url)
            
            if real_link and "m3u8" in real_link:
                # 写入 M3U 格式，加入 group-title 实现自动分类
                m3u_content += f'#EXTINF:-1 tvg-name="{name}" tvg-logo="{LOGO_URL}" group-title="{cat}",{name}\n{real_link}\n'
            else:
                print(f"⚠️ {name} 目前未开播或解析失败")
    
    # 3. 保存文件
    with open("live.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print(f"✅ 直播源已更新！生成时间：{now}")

if __name__ == "__main__":
    main()
