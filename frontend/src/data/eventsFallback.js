// 后端未启动时的兜底数据，由 backend/data/announcements.json 生成（已去掉正文 content 字段）。
// 改活动请改后端 JSON，然后重新生成这个文件。
export default [
  {
    "id": 2,
    "title": "MCM London Comic Con",
    "title_local": "伦敦 MCM 动漫展 · 2026 秋",
    "date_event": "2026-10-23",
    "date_end": "2026-10-25",
    "date_posted": "2026-10-13",
    "category": "动漫展会",
    "country": "英国",
    "country_code": "gb",
    "city": "伦敦",
    "venue": "ExCeL London",
    "location": "伦敦，英国",
    "accent": "#5b8dee",
    "featured": true,
    "status": "upcoming",
    "summary": "英国规模最大的流行文化展会将于 10 月 23—25 日在 ExCeL London 举行。除动漫、游戏、Cosplay 与创作者区域外，本届确认日本演员新田真剑佑于周六、周日出席。",
    "highlight": "新田真剑佑 · 周六、周日出席",
    "cover_image": "/assets/events/mcm-london-oct-2026-hero.jpg",
    "cover_credit": "2026 官方嘉宾页宣传图 · MCM Comic Con / ReedPop",
    "official_logo": "/assets/events/mcm-london-fall-logo.png",
    "guests_note": "截至 2026 年 10 月 13 日，官网主嘉宾名单中可确认的日本嘉宾如下；暂未查到日本声优、歌手或漫画家。名单与出席安排仍可能变动。",
    "guests": [
      {
        "name": "Mackenyu",
        "name_local": "新田真剑佑",
        "role": "演员",
        "note": "《航海王》真人版索隆；周六、周日出席",
        "image": "/assets/events/mackenyu-mcm-london-2026.png"
      }
    ],
    "tags": [
      "展会",
      "英国",
      "伦敦",
      "Cosplay",
      "日本嘉宾"
    ],
    "external_link": "https://www.mcmcomiccon.com/london/en-us.html"
  },
  {
    "id": 3,
    "title": "Japan Expo Paris",
    "title_local": "巴黎日本博览会",
    "date_event": "2027-07-08",
    "date_end": "2027-07-11",
    "date_posted": "2026-09-20",
    "category": "日本文化节",
    "country": "法国",
    "country_code": "fr",
    "city": "巴黎",
    "venue": "Paris Nord Villepinte",
    "location": "巴黎，法国",
    "accent": "#60aac4",
    "featured": false,
    "status": "upcoming",
    "summary": "欧洲规模最大的日本文化综合展，四天会期，涵盖动漫、游戏、音乐现场、传统文化与武道，每年吸引二十余万人次。",
    "highlight": "欧洲最大日本文化展",
    "cover_image": "/assets/events/japan-expo-paris-previous-edition.jpg",
    "cover_credit": "往届 Cosplay 舞台照片 · Japan Expo 官方网站",
    "cover_source": "https://paris.japan-expo.com/en",
    "guests": [],
    "tags": [
      "展会",
      "法国",
      "巴黎",
      "Live"
    ],
    "external_link": "https://paris.japan-expo.com/en"
  },
  {
    "id": 4,
    "title": "DoKomi",
    "title_local": "杜塞尔多夫日本与动漫博览会",
    "date_event": "2027-07-09",
    "date_end": "2027-07-11",
    "date_posted": "2026-09-20",
    "category": "动漫展会",
    "country": "德国",
    "country_code": "de",
    "city": "杜塞尔多夫",
    "venue": "Messe Düsseldorf",
    "location": "杜塞尔多夫，德国",
    "accent": "#f472b6",
    "featured": false,
    "status": "upcoming",
    "summary": "德国规模最大的日本与动漫博览会，2026 年到场约 23 万人次。所在城市杜塞尔多夫本身就拥有欧洲最大的日本人社区「小东京」。",
    "highlight": "2026 年约 23 万人次",
    "cover_image": "/assets/events/dokomi-previous-edition.jpg",
    "cover_credit": "往届 Live Stage 现场照片 · DoKomi / AkibaDreams GmbH",
    "cover_source": "https://www.dokomi.de/en/event/what-is-dokomi",
    "guests": [],
    "tags": [
      "展会",
      "德国",
      "杜塞尔多夫",
      "小东京"
    ],
    "external_link": "https://www.dokomi.de/en/"
  }
]
