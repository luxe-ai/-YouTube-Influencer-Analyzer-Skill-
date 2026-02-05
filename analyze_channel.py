#!/usr/bin/env python3
"""
YouTube Channel Analyzer
Extracts key metrics from YouTube channels for collaboration assessment
"""

import urllib.request
import re
import json
import sys


def fetch_page(url, timeout=15):
    """Fetch a webpage with proper headers"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read().decode('utf-8')


def extract_subscriber_count(html):
    """Extract subscriber count from channel page"""
    patterns = [
        r'"subscriberCountText":\{"simpleText":"([^"]+)"',
        r'(\d+\.?\d*[KMB]?) subscribers',
        r'(\d+\.?\d*[KMB]?) subscriber'
    ]

    for pattern in patterns:
        matches = re.findall(pattern, html)
        if matches:
            return matches[0].replace(' subscribers', '').replace(' subscriber', '').strip()
    return None


def extract_videos(html, count=5):
    """Extract video titles and view counts"""
    view_patterns = re.findall(r'"viewCountText":\{"simpleText":"([^"]+)"', html)
    title_patterns = re.findall(r'"title":\{"runs":\[\{"text":"([^"]+)"', html)
    time_patterns = re.findall(r'"publishedTimeText":\{"simpleText":"([^"]+)"', html)

    videos = []
    for i in range(min(count, len(view_patterns), len(title_patterns))):
        videos.append({
            'title': title_patterns[i],
            'views': view_patterns[i],
            'published': time_patterns[i] if i < len(time_patterns) else 'Unknown'
        })

    return videos


def parse_view_count(view_str):
    """Convert view string to numeric value"""
    view_num_str = view_str.replace(' views', '').replace(' view', '').replace(',', '').strip()

    multiplier = 1
    if 'K' in view_num_str:
        multiplier = 1000
        view_num_str = view_num_str.replace('K', '')
    elif 'M' in view_num_str:
        multiplier = 1000000
        view_num_str = view_num_str.replace('M', '')
    elif 'B' in view_num_str:
        multiplier = 1000000000
        view_num_str = view_num_str.replace('B', '')

    try:
        return float(view_num_str) * multiplier
    except:
        return 0


def calculate_average_views(videos):
    """Calculate average views from video list"""
    total_views = sum(parse_view_count(v['views']) for v in videos)
    return int(total_views / len(videos)) if videos else 0


def determine_update_frequency(times):
    """Determine update frequency from published times"""
    days = []
    for time_str in times:
        match = re.search(r'(\d+)\s+days?\s+ago', time_str)
        if match:
            days.append(int(match.group(1)))
        elif 'hour' in time_str or 'minute' in time_str:
            days.append(0)
        elif '1 week' in time_str:
            days.append(7)
        elif re.search(r'(\d+)\s+weeks?\s+ago', time_str):
            weeks = int(re.search(r'(\d+)\s+weeks?\s+ago', time_str).group(1))
            days.append(weeks * 7)
        elif '1 month' in time_str:
            days.append(30)

    if not days or len(days) < 2:
        return "Unknown"

    # Check most recent videos (use average for better accuracy)
    recent = days[:3]
    avg_interval = sum(recent) / len(recent) if recent else 0

    if avg_interval <= 3:
        return "3天/条"
    elif avg_interval <= 7:
        return "4-7天/条"
    elif avg_interval <= 14:
        return "7天+/条"
    else:
        return "14天+/条"


def check_ai_relevance(videos):
    """Check if content is AI-related"""
    ai_keywords = ['ai', 'artificial intelligence', 'claude', 'gpt', 'chatgpt',
                   'machine learning', 'deep learning', 'neural', 'automation',
                   'grok', 'luma', 'midjourney', 'stable diffusion']

    relevant_count = 0
    for video in videos:
        title_lower = video['title'].lower()
        if any(keyword in title_lower for keyword in ai_keywords):
            relevant_count += 1

    return relevant_count >= len(videos) * 0.6  # 60% threshold


def evaluate_happycapy_fit(videos, channel_data):
    """Evaluate channel fit for HappyCapy collaboration

    Categories:
    1. AI tools / Automation tutorials
    2. Side hustle / Make money online
    3. Learning / Productivity improvement
    4. Professional developer / Tech deep dive
    """

    ai_tool_keywords = ['ai', 'gpt', 'claude', 'automation', 'tool', 'chatgpt', 'midjourney', 'stable diffusion']
    money_keywords = ['make money', 'side hustle', 'passive income', 'earn', 'dollar', 'monetize', '赚钱', '副业']
    learning_keywords = ['tutorial', 'how to', 'guide', 'learn', 'course', 'tip', 'productivity', 'efficiency', '教程', '学习', '效率']
    dev_keywords = ['code', 'coding', 'programming', 'developer', 'software', 'github', 'api', 'backend', 'frontend']

    scores = {
        'ai_tools': 0,
        'money': 0,
        'learning': 0,
        'dev': 0
    }

    # Check video titles
    for video in videos:
        title_lower = video['title'].lower()

        if any(kw in title_lower for kw in ai_tool_keywords):
            scores['ai_tools'] += 1
        if any(kw in title_lower for kw in money_keywords):
            scores['money'] += 1
        if any(kw in title_lower for kw in learning_keywords):
            scores['learning'] += 1
        if any(kw in title_lower for kw in dev_keywords):
            scores['dev'] += 1

    # Calculate match level
    matched_categories = sum(1 for score in scores.values() if score >= 2)
    total_matches = sum(scores.values())

    # Determine rating
    if matched_categories >= 3 or total_matches >= 8:
        rating = "高-hpcp"
        reason = []
        if scores['ai_tools'] >= 2: reason.append("✅AI工具类")
        if scores['money'] >= 2: reason.append("✅副业赚钱类")
        if scores['learning'] >= 2: reason.append("✅学习/效率提升类")
        if scores['dev'] >= 2: reason.append("✅专业开发者类")
    elif matched_categories >= 2 or total_matches >= 5:
        rating = "中高-hpcp"
        reason = []
        if scores['ai_tools'] >= 1: reason.append("✅AI工具相关")
        if scores['money'] >= 1: reason.append("✅副业赚钱相关")
        if scores['learning'] >= 1: reason.append("✅学习/效率提升类")
        if scores['dev'] >= 1: reason.append("✅开发者相关")
    elif matched_categories >= 1 or total_matches >= 2:
        rating = "中-hpcp"
        reason = []
        if scores['ai_tools'] >= 1: reason.append("✅AI工具相关")
        if scores['money'] >= 1: reason.append("✅副业赚钱相关")
        if scores['learning'] >= 1: reason.append("✅学习/效率提升类")
        if scores['dev'] >= 1: reason.append("✅开发者相关")
    else:
        rating = "低-hpcp"
        reason = ["❌不匹配目标分类"]

    # Add engagement metrics
    if channel_data.get('subscriber_numeric', 0) > 0:
        engagement_rate = (channel_data.get('average_views', 0) / channel_data['subscriber_numeric']) * 100
        if engagement_rate >= 70:
            reason.append(f"✅高互动率({engagement_rate:.0f}%)")
        elif engagement_rate >= 50:
            reason.append(f"⚠️中等互动率({engagement_rate:.0f}%)")

    # Check for viral potential
    if videos:
        views_list = [parse_view_count(v['views']) for v in videos]
        avg_views = sum(views_list) / len(views_list)
        max_views = max(views_list)
        if max_views > avg_views * 3:
            reason.append(f"✅有爆款潜力({int(max_views):,}观看)")

    return {
        'rating': rating,
        'reason': ' '.join(reason),
        'scores': scores
    }


def analyze_channel(channel_url):
    """Main analysis function"""
    try:
        # Ensure proper URL format
        if not channel_url.startswith('http'):
            channel_url = 'https://www.youtube.com/' + channel_url

        channel_handle = channel_url.split('/')[-1]
        base_url = f"https://www.youtube.com/{channel_handle}"
        videos_url = f"{base_url}/videos"

        print(f"Analyzing channel: {channel_handle}\n")

        # Fetch main page for subscriber count
        print("Fetching channel data...")
        main_html = fetch_page(base_url)
        subscribers = extract_subscriber_count(main_html)

        # Fetch videos page
        print("Fetching video data...")
        videos_html = fetch_page(videos_url)
        videos = extract_videos(videos_html, count=5)

        if not videos:
            print("Error: Could not extract video data")
            return None

        # Calculate metrics
        avg_views = calculate_average_views(videos)
        frequency = determine_update_frequency([v['published'] for v in videos])
        ai_relevant = check_ai_relevance(videos)

        # Prepare results
        result = {
            'channel_handle': channel_handle,
            'channel_url': base_url,
            'subscribers': subscribers,
            'subscriber_numeric': int(parse_view_count(subscribers + ' views')) if subscribers else 0,
            'recent_videos': videos,
            'average_views': avg_views,
            'update_frequency': frequency,
            'ai_relevant': ai_relevant
        }

        # Evaluate HappyCapy fit
        happycapy_eval = evaluate_happycapy_fit(videos, result)
        result['happycapy_rating'] = happycapy_eval['rating']
        result['happycapy_reason'] = happycapy_eval['reason']

        return result

    except Exception as e:
        print(f"Error analyzing channel: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None


def format_report(data):
    """Format analysis data into readable report"""
    if not data:
        return "Analysis failed"

    report = f"""
{'='*70}
YouTube Channel Analysis Report
{'='*70}

Channel: {data['channel_handle']}
URL: {data['channel_url']}

METRICS:
- Subscribers: {data['subscribers']} ({data['subscriber_numeric']:,})
- Average Views (Recent 5): {data['average_views']:,}
- Update Frequency: {data['update_frequency']}
- AI/Tech Related: {'Yes ✓' if data['ai_relevant'] else 'No ✗'}

RECENT VIDEOS:
"""

    for i, video in enumerate(data['recent_videos'], 1):
        views_numeric = int(parse_view_count(video['views']))
        report += f"\n{i}. {video['title'][:60]}"
        report += f"\n   Views: {views_numeric:,} ({video['views']})"
        report += f"\n   Published: {video['published']}\n"

    engagement_rate = (data['average_views'] / data['subscriber_numeric'] * 100) if data['subscriber_numeric'] > 0 else 0

    report += f"""
{'='*70}
KEY INSIGHTS:
- Engagement Rate: {engagement_rate:.1f}% (views/subscribers)
- Content Focus: {'AI/Tech Tools' if data['ai_relevant'] else 'General Content'}
- Publishing Consistency: {data['update_frequency']}

HAPPYCAPY COLLABORATION FIT:
- Rating: {data.get('happycapy_rating', 'N/A')}
- Reason: {data.get('happycapy_reason', 'N/A')}

"""

    return report


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_channel.py <youtube_channel_url>")
        print("Example: python3 analyze_channel.py https://www.youtube.com/@MoeLueker")
        sys.exit(1)

    channel_url = sys.argv[1]
    data = analyze_channel(channel_url)

    if data:
        print(format_report(data))

        # Output JSON for programmatic use
        if '--json' in sys.argv:
            print("\nJSON Output:")
            print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
