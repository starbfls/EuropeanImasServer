from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

MOCK_NEWS = [
    {
        "id": 1,
        "title": "European iMas Offline Meetup — Berlin 2025",
        "date": "2025-06-15",
        "category": "Meetup",
        "summary": "Join us for our first Berlin offline meetup! We will be gathering at a central venue for fan activities, merchandise exchange, and good times.",
        "content": "# European iMas Offline Meetup — Berlin 2025\n\nWe are thrilled to announce our first official offline meetup in Berlin!\n\n## Details\n\n- **Date**: June 15, 2025\n- **Location**: Berlin, Germany\n- **Time**: 14:00 CET\n\n## What to Expect\n\nWe will be having a viewing party, merchandise exchange, and general fan discussions. All producers are welcome!\n\n## How to Join\n\nJoin our Discord server to RSVP and receive the venue details. Spots are limited, so register early.\n\n## Agenda\n\n1. 14:00 — Arrival & introduction\n2. 15:00 — Viewing party (selected live performances)\n3. 17:00 — Merchandise exchange circle\n4. 18:30 — Group dinner (optional)\n\nSee you there, producers!",
        "cover_image": "https://placehold.co/800x400/60aac4/ffffff?text=Berlin+Meetup+2025",
        "tags": ["meetup", "berlin", "offline"]
    },
    {
        "id": 2,
        "title": "Live Viewing: THE iDOLM@STER 15th Anniversary Concert",
        "date": "2025-05-20",
        "category": "Live Viewing",
        "summary": "Celebrate 15 years of iDOLM@STER with fellow European producers! We are organizing an online live viewing event via Discord.",
        "content": "# Live Viewing: THE iDOLM@STER 15th Anniversary Concert\n\nCelebrate 15 glorious years of iDOLM@STER with the European producer community!\n\n## Event Info\n\n- **Date**: May 20, 2025\n- **Platform**: Discord Stage Channel\n- **Time**: 18:00 CET\n\n## About\n\nWe will be watching the anniversary concert stream together and reacting in real time. Bring your oshi merch and get ready!\n\n## How to Join\n\n1. Join our Discord server (see Rules & Links page)\n2. Head to the `#live-viewing` voice channel at the scheduled time\n3. The stream link will be posted in `#announcements`\n\nDon't miss this milestone celebration!",
        "cover_image": "https://placehold.co/800x400/c460aa/ffffff?text=15th+Anniversary+Live",
        "tags": ["live viewing", "anniversary", "online"]
    },
    {
        "id": 3,
        "title": "Welcome to New Members — Spring 2025",
        "date": "2025-04-10",
        "category": "Announcement",
        "summary": "Welcome to all our new members who joined this spring! Here is everything you need to know to get started in the European iMas community.",
        "content": "# Welcome New Members — Spring 2025!\n\nThe European iDOLM@STER Union is growing, and we couldn't be happier!\n\n## Getting Started\n\n1. Join our **Discord server** for real-time chat and announcements\n2. Read the **Rules** page carefully before participating\n3. Introduce yourself in the `#introductions` channel\n\n## What We Do\n\n- Organize offline meetups across Europe\n- Host online live viewing parties\n- Share fan art, merch photos, and event reports\n- Support each other as a multilingual, multicultural community\n\n## iMas Branches\n\nWe welcome fans of all iDOLM@STER branches:\n- **765 Pro** (THE iDOLM@STER)\n- **Cinderella Girls**\n- **Million Live**\n- **SideM**\n- **Shiny Colors**\n\nWelcome aboard, producers!",
        "cover_image": "https://placehold.co/800x400/aac460/ffffff?text=Welcome+New+Members",
        "tags": ["announcement", "welcome", "community"]
    },
    {
        "id": 4,
        "title": "Fan Art Showcase — March Collection",
        "date": "2025-03-25",
        "category": "Fan Content",
        "summary": "Check out the incredible fan art submitted by our community members this March. Over 30 pieces from European producers!",
        "content": "# Fan Art Showcase — March Collection\n\nEvery month we compile and showcase fan art created by our European producer community.\n\n## This Month's Highlights\n\nWe received over **30 submissions** this month featuring characters from all branches of iDOLM@STER.\n\n### Top Picks\n\n- Watercolour piece of Uzuki Shimamura by a producer from France\n- Digital illustration of Shizuka Mogami from Germany\n- Traditional sketch collection of 765 Pro from Italy\n\n## How to Submit\n\nShare your fan art in our Discord `#fan-art` channel with the hashtag `#EUiMas`. Every piece is appreciated!\n\n## Next Showcase\n\nThe April collection will be announced at the end of April. Keep creating!",
        "cover_image": "https://placehold.co/800x400/aa60c4/ffffff?text=Fan+Art+March",
        "tags": ["fan art", "community", "showcase"]
    },
    {
        "id": 5,
        "title": "Shiny Colors Unit Concert Report — Amsterdam",
        "date": "2025-03-01",
        "category": "Event Report",
        "summary": "A full report from our Amsterdam screening of the Shiny Colors unit concert. Read about the atmosphere, reactions, and post-event gathering.",
        "content": "# Shiny Colors Unit Concert Report — Amsterdam\n\nLast month, a group of Dutch and Belgian producers gathered in Amsterdam for a special screening of the Shiny Colors unit concert.\n\n## Attendance\n\n**12 producers** attended in person, with another 8 joining the simultaneous Discord stream.\n\n## Highlights\n\nThe room erupted during L'Antica's performance. Several producers had visible tears during the Straylight segment. The post-concert merchandise display was a sight to behold.\n\n## Photos\n\nEvent photos are available in the **Gallery** section.\n\n## Thank You\n\nThank you to everyone who attended or joined online. Events like this remind us why we love this community.\n\nSee you at the next one!",
        "cover_image": "https://placehold.co/800x400/60c4aa/ffffff?text=Amsterdam+Screening",
        "tags": ["event report", "shiny colors", "amsterdam"]
    }
]

MOCK_GALLERY = [
    {"id": 1, "title": "Berlin Meetup 2024 — Group Photo", "type": "meetup", "url": "https://placehold.co/800x533/60aac4/ffffff?text=Berlin+Group+Photo", "thumbnail": "https://placehold.co/400x267/60aac4/ffffff?text=Berlin+Group+Photo"},
    {"id": 2, "title": "Itasha at Amsterdam Comic Con", "type": "itasha", "url": "https://placehold.co/600x900/c460aa/ffffff?text=Amsterdam+Itasha", "thumbnail": "https://placehold.co/400x600/c460aa/ffffff?text=Amsterdam+Itasha"},
    {"id": 3, "title": "Fan Altar — Cinderella Girls", "type": "altar", "url": "https://placehold.co/700x700/aa60c4/ffffff?text=Fan+Altar+CG", "thumbnail": "https://placehold.co/400x400/aa60c4/ffffff?text=Fan+Altar+CG"},
    {"id": 4, "title": "Paris Live Viewing Party", "type": "meetup", "url": "https://placehold.co/800x533/60c4aa/ffffff?text=Paris+Live+Viewing", "thumbnail": "https://placehold.co/400x267/60c4aa/ffffff?text=Paris+Live+Viewing"},
    {"id": 5, "title": "Merchandise Collection Display", "type": "merchandise", "url": "https://placehold.co/800x600/c4aa60/ffffff?text=Merch+Collection", "thumbnail": "https://placehold.co/400x300/c4aa60/ffffff?text=Merch+Collection"},
    {"id": 6, "title": "London Cosplay — Shiny Colors", "type": "cosplay", "url": "https://placehold.co/600x900/6084c4/ffffff?text=London+Cosplay", "thumbnail": "https://placehold.co/400x600/6084c4/ffffff?text=London+Cosplay"},
    {"id": 7, "title": "Madrid Game Night", "type": "meetup", "url": "https://placehold.co/800x533/aac460/ffffff?text=Madrid+Game+Night", "thumbnail": "https://placehold.co/400x267/aac460/ffffff?text=Madrid+Game+Night"},
    {"id": 8, "title": "Fan Altar — Million Live", "type": "altar", "url": "https://placehold.co/700x700/c460aa/ffffff?text=Fan+Altar+ML", "thumbnail": "https://placehold.co/400x400/c460aa/ffffff?text=Fan+Altar+ML"},
    {"id": 9, "title": "Rome Itasha Showcase", "type": "itasha", "url": "https://placehold.co/800x533/aa60c4/ffffff?text=Rome+Itasha", "thumbnail": "https://placehold.co/400x267/aa60c4/ffffff?text=Rome+Itasha"},
    {"id": 10, "title": "Shiny Colors Screening — Amsterdam", "type": "meetup", "url": "https://placehold.co/800x533/60aac4/ffffff?text=Amsterdam+Screening", "thumbnail": "https://placehold.co/400x267/60aac4/ffffff?text=Amsterdam+Screening"},
    {"id": 11, "title": "Producer Merch Wall — Paris", "type": "merchandise", "url": "https://placehold.co/700x700/c4aa60/ffffff?text=Paris+Merch+Wall", "thumbnail": "https://placehold.co/400x400/c4aa60/ffffff?text=Paris+Merch+Wall"},
    {"id": 12, "title": "Cosplay Showcase — Berlin Con", "type": "cosplay", "url": "https://placehold.co/600x900/c46060/ffffff?text=Berlin+Cosplay", "thumbnail": "https://placehold.co/400x600/c46060/ffffff?text=Berlin+Cosplay"},
]


@app.route('/api/news', methods=['GET'])
def get_news():
    return jsonify({"success": True, "data": MOCK_NEWS})


@app.route('/api/news/<int:news_id>', methods=['GET'])
def get_news_detail(news_id):
    article = next((n for n in MOCK_NEWS if n["id"] == news_id), None)
    if not article:
        return jsonify({"success": False, "error": "Not found"}), 404
    return jsonify({"success": True, "data": article})


@app.route('/api/gallery', methods=['GET'])
def get_gallery():
    return jsonify({"success": True, "data": MOCK_GALLERY})


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "European iMas Server is running!"})


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
