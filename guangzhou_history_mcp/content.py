"""
Bilingual content for the Guangzhou History MCP.

Each chapter has a stable `id`, an era label, and parallel zh / en bodies.
The body is intentionally short — one screen per chapter when shown in the
flipbook viewer. Keep prose dense but readable.

Sources for facts (consulted while writing):
  - 《廣州市志》(Guangzhou Municipal Gazetteer)
  - Britannica entry on Guangzhou
  - Sun Yat-sen Memorial Hall public materials
  - Guangzhou Municipal Bureau of Culture, Radio, Television and Tourism
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Chapter:
    id: str
    era_zh: str
    era_en: str
    title_zh: str
    title_en: str
    body_zh: str
    body_en: str
    # A short, evocative tag used by the viewer for header chips.
    motif: str  # one of: "nanyue", "silk-road", "thirteen-hongs",
    #             "treaty-port", "revolution", "reform"


CHAPTERS: list[Chapter] = [
    Chapter(
        id="origins",
        era_zh="先秦 · 公元前 214 年",
        era_en="Pre-Qin · 214 BCE",
        title_zh="任嚣筑城,番禺立基",
        title_en="The Founding of Panyu",
        body_zh=(
            "公元前 214 年，秦始皇平定岭南，设南海、桂林、象三郡。"
            "南海郡尉任嚣（xiāo）选址珠江北岸高地筑起“任嚣城”，周长虽仅四里，"
            "却奠定了今日广州老城的最初雏形。秦末天下大乱，继任者赵佗自立为"
            "南越武王，以番禺（今广州）为都城，统治岭南九十三载。"
            "如今南越王墓出土的“文帝行玺”金印与角形玉杯，默默印证着这座"
            "南方古都早期的商贸繁华，以及中原、楚、越与海外多元文化的交融共生。"
        ),
        body_en=(
            "In 214 BCE, after Qin Shi Huang pacified Lingnan, three "
            "commanderies were established. Ren Xiao, commandant of Nanhai, "
            "chose a high bluff on the north bank of the Pearl River and built "
            "Renxiao City — barely four li in circumference, yet the seed of "
            "today's Guangzhou. His successor Zhao Tuo declared himself King "
            "of Southern Yue (Nanyue) as the Qin collapsed, making Panyu "
            "(modern Guangzhou) his capital for ninety-three years. The gold "
            "seal of 'Emperor Wen' and the rhyton-shaped jade cup unearthed "
            "from the Nanyue royal tomb attest to a southern capital already "
            "fluent in Central Plains, Chu, Yue and overseas vocabularies."
        ),
        motif="nanyue",
    ),
    Chapter(
        id="silk-road",
        era_zh="唐宋 · 7-13 世纪",
        era_en="Tang–Song · 7th–13th century",
        title_zh="蕃坊云集，海丝起点",
        title_en="Lighthouse of the Maritime Silk Road",
        body_zh=(
            "唐代在广州特设市舶使，这是中国历史上首个专管海外贸易的官职。"
            "彼时城西“蕃坊”云集，聚居了数万名阿拉伯、波斯与印度商人；怀圣寺光塔"
            "建于唐朝，既是穆斯林的宣礼塔，也是指引珠江入港船只的巍峨灯塔。"
            "及至宋代，海上丝绸之路达到巅峰，广州港的海关岁入成为国家财政的重要支柱。"
            "无数的陶瓷、丝绸与茶叶从这里扬帆出海，源源不断的香料、宝石与象牙溯流而起，"
            "将古老岭南与大食世界紧紧绾在同一根蔚蓝的浪线之上。"
        ),
        body_en=(
            "In the Tang dynasty Guangzhou received the empire's first Maritime "
            "Trade Commissioner — the earliest dedicated foreign-trade office "
            "in Chinese history. Tens of thousands of Arab, Persian and Indian "
            "merchants lived in the Fanfang quarter west of the walls. The "
            "Guangta minaret of Huaisheng Mosque, dating from the Tang, doubled "
            "as the harbour's lighthouse. By the Song, Guangzhou's customs "
            "revenue formed a meaningful share of the imperial budget. Porcelain, "
            "silk and tea sailed out; spices, gemstones, ivory and glass sailed "
            "in — knotting Lingnan to Srivijaya, the Chola coast and the lands "
            "of the Dashi (the Arab world) along a single line of swell."
        ),
        motif="silk-road",
    ),
    Chapter(
        id="thirteen-hongs",
        era_zh="清 · 1757-1842",
        era_en="Qing · 1757–1842",
        title_zh="一口通商，十三行天下",
        title_en="One Port, Thirteen Hongs",
        body_zh=(
            "1757 年，乾隆皇帝下令“一口通商”，广州成为大清帝国唯一对欧美开放的通商口岸。"
            "珠江北岸的“十三行”商馆区由此富甲天下：行商巨贾伍秉鉴一度被外商"
            "誉为“世界首富”，其家族财富多达 2600 万两白银。"
            "瑞典、英国、荷兰与美国的商船在黄埔锚地静候季风；满载的茶叶、"
            "丝绸、瓷器与漆器，以及精美的广彩、外销画与象牙雕，在西方掀起了狂热的“中国风”潮。"
            "此时的十三行不仅是黄金商路，更是 18 世纪中国与世界之间唯一官方允准的窄门。"
        ),
        body_en=(
            "In 1757 the Qianlong Emperor restricted European and American "
            "trade to Guangzhou alone — the famous 'Canton System'. The "
            "Thirteen Hongs (factories) along the north bank of the Pearl "
            "River became the richest square mile in the empire. The hong "
            "merchant Howqua (Wu Bingjian) was reckoned by Western traders to "
            "be the wealthiest private individual in the world, with a family "
            "fortune topping 26 million taels of silver. Swedish, British, "
            "Dutch and American ships rode at anchor off Whampoa; their cargoes "
            "of tea, silk, porcelain and lacquer — together with bespoke "
            "Canton enamel, export paintings, silverware and ivory — fed "
            "Europe's appetite for chinoiserie. The Hongs were not merely "
            "firms; they were the single licensed gateway between Qing China "
            "and the wider world."
        ),
        motif="thirteen-hongs",
    ),
    Chapter(
        id="treaty-port",
        era_zh="晚清 · 1842-1911",
        era_en="Late Qing · 1842–1911",
        title_zh="火烧十三行，沙面立租界",
        title_en="The Hongs Burn, Shamian Rises",
        body_zh=(
            "1842 年《南京条约》签订后五口通商，广州独霸对外贸易的格局被打破。"
            "1856 年第二次鸦片战争爆发，繁华百年的十三行商馆区在一场大火中化为废墟。"
            "战后，英法两国在珠江沙洲上强筑沙面租界：这座人工岛上西式洋楼林立，"
            "至今仍保留着广州最完整的近代欧陆建筑群。"
            "与此同时，与之对望的西关大屋成片拔地而起，趟栊门、满洲窗与青砖石脚，"
            "定义了广府民居的经典范式；而黄埔船坞与广州机器局的隆隆机械声，则标志着洋务运动南方据点的崛起。"
            "古老的广州，正在炮火与近代工业的洗礼中加速蝶变。"
        ),
        body_en=(
            "The 1842 Treaty of Nanking opened five ports and broke Guangzhou's "
            "monopoly on foreign trade. In 1856, during the Second Opium War, "
            "the Thirteen Hongs district was burned to the ground. The British "
            "and French then built the Shamian concession on a 300-metre sandbar "
            "in the Pearl River — still the most coherent neo-classical European "
            "townscape in southern China. Across the water, the wealthy "
            "Xiguan mansions defined a new Cantonese vernacular: trellis gates, "
            "Manchu stained-glass windows, blue-brick walls on granite plinths. "
            "Meanwhile Whampoa Dockyard, the Guangdong Arsenal and the Guangzhou "
            "Machine Bureau marked the southern outpost of the Self-Strengthening "
            "Movement. The old city accelerated into modernity between shellfire "
            "and steam."
        ),
        motif="treaty-port",
    ),
    Chapter(
        id="revolution",
        era_zh="民国 · 1911-1949",
        era_en="Republican · 1911–1949",
        title_zh="革命策源，黄埔扬帆",
        title_en="Cradle of Revolution, Whampoa Sets Sail",
        body_zh=(
            "辛亥革命前后，广州成为中国近代革命最瞩目的策源地。"
            "1911 年“黄花岗起义”爆发，七十二烈士自此长眠于白云山麓；"
            "1924 年，孙中山先生在广州主持国民党改组，并在长洲岛创办了名震天下的黄埔军校。"
            "如今，中山纪念堂、中山大学与烈士陵园等革命遗迹，"
            "如同一串闪耀的红色明珠散落在古城各处。"
            "抗战期间广州虽不幸沦陷，但东江纵队仍顽强周旋于邻近山区；"
            "直至 1949 年 10 月 14 日广州宣告解放，这座英雄之城终于翻开了崭新的一页。"
        ),
        body_en=(
            "Around the 1911 revolution Guangzhou was the wellspring of modern "
            "Chinese politics. The 72 martyrs of the 1911 Yellow Flower Mound "
            "Uprising lie at the foot of Baiyun Mountain. In 1924 Sun Yat-sen "
            "reorganised the Kuomintang here and founded the Whampoa Military "
            "Academy on Changzhou Island — Chiang Kai-shek as commandant, Zhou "
            "Enlai as head of the political department. Sun Yat-sen Memorial "
            "Hall, Sun Yat-sen (Zhongshan) University, the Peasant Movement "
            "Training Institute and the Guangzhou Uprising Martyrs' Cemetery "
            "form a red bead-string across the city. Guangzhou fell during the "
            "Anti-Japanese War while the East River Column harried the occupier "
            "from the surrounding hills; on 14 October 1949 the city was "
            "liberated, opening a new page."
        ),
        motif="revolution",
    ),
    Chapter(
        id="reform",
        era_zh="改革开放 · 1978 至今",
        era_en="Reform Era · 1978–today",
        title_zh="春风南来，千年商都新生",
        title_en="Southern Spring: A Millennial Trade-City Reborn",
        body_zh=(
            "1978 年乘着改革开放的春风，广州凭借毗邻港澳的独特优势与深厚商脉，率先弄潮试水。"
            "自 1957 年创办以来从未中断的广交会，早已成为名副其实的“中国第一展”；"
            "1983 年开业的白天鹅宾馆，更是新中国首家中外合资的五星级酒店。"
            "随着天河 CBD 的崛起，高达 600 米的广州塔（小蛮腰）于 2010 年璀璨点亮了珠江夜空。"
            "今天，这座拥有超 1800 万常住人口的繁华巨埠，既是大湾区的核心枢纽，"
            "更是岭南文化最生动的注脚——早茶烟火、粤剧余音、龙舟竞渡与广府醒狮，"
            "将两千八百年的传奇故事，温柔地写进每一个晨曦与黄昏。"
        ),
        body_en=(
            "Starting reform in 1978, Guangzhou moved first as the gateway to "
            "global trade. The Canton Fair has run since 1957 as China's premier expo, "
            "while the iconic White Swan Hotel opened in 1983. Today, with the towering "
            "Canton Tower lighting the Pearl River skyline, the city thrives with over "
            "18 million residents. It anchors the Greater Bay Area while preserving "
            "deep Cantonese roots — yum cha, Cantonese opera, and lion dances writing "
            "twenty-eight centuries of history into daily life."
        ),
        motif="reform",
    ),
]


# ---------------------------------------------------------------------------
# A compact chronological timeline used by the get_timeline tool & the
# flipbook's penultimate page.
# ---------------------------------------------------------------------------

TIMELINE: list[dict] = [
    {"year": "214 BCE", "zh": "秦南海郡建立，任嚣筑番禺城",
     "en": "Qin establishes Nanhai; Ren Xiao builds first walls."},
    {"year": "204 BCE", "zh": "赵佗建南越国，定都番禺",
     "en": "Zhao Tuo founds Nanyue Kingdom with Panyu capital."},
    {"year": "226 CE", "zh": "孙吴设广州，「广州」之名始见",
     "en": "Eastern Wu names region 'Guangzhou' first time."},
    {"year": "714", "zh": "唐设市舶使，首开专管外贸官职",
     "en": "Tang appoints first Maritime Trade Commissioner."},
    {"year": "1405-1433", "zh": "郑和下西洋，广州为重要补给港",
     "en": "Zheng He's voyages use Guangzhou as supply port."},
    {"year": "1757", "zh": "乾隆一口通商，十三行垄断欧美的贸易",
     "en": "Canton System: single-port trade restriction begins."},
    {"year": "1842", "zh": "《南京条约》开五口，独占地位结束",
     "en": "Treaty of Nanking opens five ports, ending monopoly."},
    {"year": "1859", "zh": "英法沙面租界划定，洋楼林立",
     "en": "Shamian neo-classical concession laid out."},
    {"year": "1911", "zh": "辛亥革命黄花岗起义，七十二烈士",
     "en": "Yellow Flower Uprising of 72 martyrs."},
    {"year": "1924", "zh": "孙中山创黄埔军校，长洲扬帆",
     "en": "Sun Yat-sen founds Whampoa Military Academy."},
    {"year": "1949", "zh": "10月14日广州宣告解放",
     "en": "Guangzhou liberated on 14 October 1949."},
    {"year": "1957", "zh": "首届广交会开幕，成中国第一展",
     "en": "Inaugural Canton Fair opens as premier expo."},
    {"year": "1978", "zh": "改革开放，千年商都先行先试",
     "en": "Reform and opening: Guangzhou pioneers new trade."},
    {"year": "2010", "zh": "广州亚运会举办，小蛮腰点亮",
     "en": "Guangzhou hosts Asian Games; Canton Tower lit."},
    {"year": "2019", "zh": "大湾区规划落地，广州为核心枢纽",
     "en": "Greater Bay Area plan sets Guangzhou as core hub."},
]


# ---------------------------------------------------------------------------
# Topic dictionary — the heart of "query mode".
#
# Each topic carries:
#   - aliases   : the strings users might type (zh & en, lower-case)
#   - chapter   : which chapter to render the result against
#   - title_zh / title_en : a query-specific page title (often more
#                 specific than the chapter title — e.g. "广州塔 · 小蛮腰"
#                 instead of the whole "Reform" chapter title)
#   - highlights: 2-4 short factoids shown as annotation chips on the page,
#                 mimicking flipbook.page's labelled illustrations
# ---------------------------------------------------------------------------

TOPICS: list[dict] = [
    {
        "id": "nanyue-king",
        "aliases": ["南越王", "赵佗", "南越国", "nanyue", "zhao tuo",
                    "南越王墓", "文帝行玺"],
        "chapter": "origins",
        "title_zh": "南越王 · 赵佗与文帝行玺",
        "title_en": "King of Nanyue · Zhao Tuo and the Imperial Seal",
        "highlights_zh": [
            "前 204 年立国,定都番禺",
            "在位 67 年,享年百岁有余",
            "金印「文帝行玺」出土于象岗",
            "存续 93 年,共五主",
        ],
        "highlights_en": [
            "Founded 204 BCE, capital at Panyu",
            "Ruled 67 years, lived past 100",
            "Gold seal 'Emperor Wen' unearthed at Xianggang",
            "Five rulers across 93 years",
        ],
    },
    {
        "id": "panyu-founding",
        "aliases": ["任嚣", "番禺", "任嚣城", "ren xiao", "panyu",
                    "广州建城"],
        "chapter": "origins",
        "title_zh": "任嚣筑城 · 番禺立基",
        "title_en": "Ren Xiao Builds the First Walls of Panyu",
        "highlights_zh": [
            "公元前 214 年秦定岭南",
            "南海郡尉任嚣选址珠江北岸",
            "城周仅四里,广州老城雏形",
            "毗邻今北京路、中山四路一带",
        ],
        "highlights_en": [
            "214 BCE — Qin pacifies Lingnan",
            "Commandant Ren Xiao picks the north bank of the Pearl",
            "Four li in circumference — seed of the old city",
            "Near today's Beijing Lu and Zhongshan-4 Lu",
        ],
    },
    {
        "id": "maritime-silk-road",
        "aliases": ["海上丝绸之路", "海丝", "市舶使", "蕃坊", "怀圣寺",
                    "光塔", "maritime silk road", "silk road", "fanfang",
                    "guangta", "huaisheng", "海丝起点"],
        "chapter": "silk-road",
        "title_zh": "海上丝绸之路 · 蕃坊与光塔",
        "title_en": "Maritime Silk Road · Fanfang & the Guangta Minaret",
        "highlights_zh": [
            "唐 714 年设市舶使,中国首个海贸专官",
            "蕃坊聚阿拉伯、波斯、印度商人数万",
            "怀圣寺光塔兼作珠江入港灯塔",
            "宋代港税一度占国库可观比重",
        ],
        "highlights_en": [
            "714 CE — first Maritime Trade Commissioner",
            "Tens of thousands of Arab, Persian & Indian traders",
            "Guangta minaret doubled as a lighthouse",
            "Song-era customs revenue: a real slice of the treasury",
        ],
    },
    {
        "id": "thirteen-hongs",
        "aliases": ["十三行", "广州十三行", "thirteen hongs", "thirteen factories",
                    "canton system", "one port", "一口通商"],
        "chapter": "thirteen-hongs",
        "title_zh": "广州十三行 · 一口通商的窄门",
        "title_en": "The Thirteen Hongs · One Licensed Gateway",
        "highlights_zh": [
            "1757 年乾隆「一口通商」",
            "西方商船在黄埔锚地候风",
            "出口:茶、丝、瓷;进口:白银、棉花、鸦片",
            "1842 年《南京条约》后,垄断终结",
        ],
        "highlights_en": [
            "1757 — Qianlong restricts European trade to Canton",
            "Western ships rode at anchor off Whampoa",
            "Out: tea, silk, porcelain · In: silver, cotton, opium",
            "Monopoly ended by the 1842 Treaty of Nanking",
        ],
    },
    {
        "id": "howqua",
        "aliases": ["伍秉鉴", "howqua", "伍浩官", "怡和行"],
        "chapter": "thirteen-hongs",
        "title_zh": "伍秉鉴 · 19 世纪的世界首富",
        "title_en": "Howqua · The Richest Merchant in the World",
        "highlights_zh": [
            "怡和行第三代行商",
            "西方人称「Howqua」",
            "家族财富一度逾 2600 万两白银",
            "波士顿茶商眼中的「最讲信用之人」",
        ],
        "highlights_en": [
            "Third-generation head of Ewo Hong",
            "Known to Westerners as 'Howqua'",
            "Family fortune topped 26 million taels of silver",
            "Boston traders called him the most trustworthy man alive",
        ],
    },
    {
        "id": "shamian",
        "aliases": ["沙面", "沙面租界", "shamian", "concession",
                    "british concession"],
        "chapter": "treaty-port",
        "title_zh": "沙面 · 珠江中的欧陆飞地",
        "title_en": "Shamian · A European Enclave in the Pearl River",
        "highlights_zh": [
            "1859 年英法划定,人工填筑而成",
            "面积约 0.3 平方公里",
            "150 余座新古典、巴洛克、券廊式洋楼",
            "今广州保存最完整的近代欧陆建筑群",
        ],
        "highlights_en": [
            "Laid out 1859 by Britain and France on reclaimed sand",
            "Roughly 0.3 km² in area",
            "150+ neo-classical, baroque and arcaded buildings",
            "The most coherent colonial townscape in Guangzhou",
        ],
    },
    {
        "id": "xiguan",
        "aliases": ["西关", "西关大屋", "趟栊门", "满洲窗",
                    "xiguan", "xiguan house", "qilou", "骑楼"],
        "chapter": "treaty-port",
        "title_zh": "西关大屋与骑楼 · 广府民居范式",
        "title_en": "Xiguan Mansions & the Qilou Arcade",
        "highlights_zh": [
            "晚清广州西郊富商聚居区",
            "三件套门:脚门、趟栊、大门",
            "满洲窗:套色蚀刻玻璃,源自十三行外销",
            "骑楼:岭南 + 南洋 + 欧陆的杂交形式",
        ],
        "highlights_en": [
            "A late-Qing merchant quarter west of the old walls",
            "Three-piece gates: foot-door, trellis, main door",
            "Manchu windows: stained glass from the Hong export trade",
            "Qilou: Lingnan + Nanyang + European hybrid arcade",
        ],
    },
    {
        "id": "whampoa-academy",
        "aliases": ["黄埔军校", "黄埔", "whampoa", "whampoa academy",
                    "long zhou island", "长洲岛"],
        "chapter": "revolution",
        "title_zh": "黄埔军校 · 长洲岛上的革命摇篮",
        "title_en": "Whampoa Military Academy · Cradle on Changzhou Island",
        "highlights_zh": [
            "1924 年孙中山在长洲岛创立",
            "蒋介石任校长,周恩来任政治部主任",
            "前 6 期培养军政人才约 8000 人",
            "国共两党许多高级将领的母校",
        ],
        "highlights_en": [
            "Founded 1924 on Changzhou Island by Sun Yat-sen",
            "Chiang Kai-shek commandant, Zhou Enlai political head",
            "First six classes graduated about 8,000 cadets",
            "Alma mater of many KMT and CCP generals alike",
        ],
    },
    {
        "id": "sun-yatsen-hall",
        "aliases": ["中山纪念堂", "孙中山", "sun yat-sen",
                    "sun yat-sen memorial hall", "memorial hall"],
        "chapter": "revolution",
        "title_zh": "中山纪念堂 · 八角宝蓝穹顶",
        "title_en": "Sun Yat-sen Memorial Hall · The Octagonal Blue Dome",
        "highlights_zh": [
            "1931 年落成,吕彦直设计",
            "八角形宝蓝琉璃瓦顶,无柱大跨度",
            "原址为清两广总督衙门",
            "可容纳近 4700 个座位",
        ],
        "highlights_en": [
            "Completed 1931, designed by Lü Yanzhi",
            "Octagonal cobalt-tile roof, column-free hall",
            "Built on the former Qing Viceroy's yamen site",
            "Seats nearly 4,700",
        ],
    },
    {
        "id": "canton-fair",
        "aliases": ["广交会", "中国进出口商品交易会", "canton fair"],
        "chapter": "reform",
        "title_zh": "广交会 · 中国第一展",
        "title_en": "Canton Fair · China's Oldest Trade Window",
        "highlights_zh": [
            "1957 年首届开幕,每年春秋两届",
            "至今从未中断",
            "新中国与外部世界最长的贸易桥梁",
            "今每届到会境外采购商超 20 万人次",
        ],
        "highlights_en": [
            "Inaugurated 1957; held every spring and autumn",
            "Has never missed a session",
            "Longest-running trade bridge of the PRC",
            "200,000+ overseas buyers per session today",
        ],
    },
    {
        "id": "canton-tower",
        "aliases": ["广州塔", "小蛮腰", "canton tower", "guangzhou tower"],
        "chapter": "reform",
        "title_zh": "广州塔 · 小蛮腰点亮珠江",
        "title_en": "Canton Tower · The 'Slim Waist' Lights the Pearl",
        "highlights_zh": [
            "总高 600 米,2010 年亚运会前建成",
            "双曲面网格筒身,设计「腰部」最纤细处仅 30 米",
            "建成时为世界第一观光塔",
            "夜间 LED 幕墙覆盖整个塔身",
        ],
        "highlights_en": [
            "600 metres tall, completed for the 2010 Asian Games",
            "Hyperboloid mesh tube — waist as narrow as 30 m",
            "The world's tallest tower on completion",
            "Whole shaft is an addressable LED façade at night",
        ],
    },
    {
        "id": "yum-cha",
        "aliases": ["早茶", "饮茶", "粤菜", "广府文化", "yum cha", "dim sum",
                    "lingnan culture", "cantonese cuisine"],
        "chapter": "reform",
        "title_zh": "早茶 · 一盅两件的广府生活",
        "title_en": "Yum Cha · 'One Pot, Two Pieces' Cantonese Life",
        "highlights_zh": [
            "「一盅两件」:一壶茶配两笼点心",
            "兴起于晚清广州的「二厘馆」",
            "代表点心:虾饺、烧麦、叉烧包、肠粉",
            "白天鹅、陶陶居、广州酒家等老字号传承至今",
        ],
        "highlights_en": [
            "'One pot, two pieces' — a pot of tea + two baskets",
            "Born in late-Qing 'two-cent teahouses' of Guangzhou",
            "Icons: har gow, siu mai, char siu bao, cheung fun",
            "Carried on by White Swan, Taotaoju, Guangzhou Restaurant",
        ],
    },
]


def topic_index() -> dict[str, dict]:
    """alias (lower-case) → topic dict."""
    out: dict[str, dict] = {}
    for t in TOPICS:
        for a in t["aliases"]:
            out[a.lower()] = t
    return out


def query_topic(q: str, lang: str = "zh") -> dict | None:
    """Resolve a user query to a structured 'page' result.

    Returns a dict suitable for rendering as a flipbook.page-style
    illustrated card, or None if nothing matched.
    """
    if not q or not q.strip():
        return None
    qn = q.strip().lower()
    aliases = topic_index()

    topic = aliases.get(qn)
    matched_via = "alias" if topic else None

    if topic is None:
        # 1) try alias substring (e.g. user typed "广州塔的高度" → "广州塔")
        for a, t in aliases.items():
            if a in qn or qn in a:
                topic, matched_via = t, "alias-partial"
                break

    if topic is None:
        # 2) fall back to chapter substring search
        hits = search(q, lang=lang)
        if hits:
            cid = hits[0]["id"]
            ch = chapter_index()[cid]
            # synthesize a topic-shaped result from the chapter itself
            return {
                "query": q,
                "matched_via": "chapter-fuzzy",
                "chapter_id": cid,
                "title": ch.title_zh if lang == "zh" else ch.title_en,
                "era": ch.era_zh if lang == "zh" else ch.era_en,
                "body": ch.body_zh if lang == "zh" else ch.body_en,
                "motif": ch.motif,
                "highlights": [],
                "related": [t["aliases"][0] for t in TOPICS
                            if t["chapter"] == cid][:4],
            }
        return None

    ch = chapter_index()[topic["chapter"]]
    return {
        "query": q,
        "matched_via": matched_via,
        "chapter_id": topic["chapter"],
        "title": topic["title_zh"] if lang == "zh" else topic["title_en"],
        "era": ch.era_zh if lang == "zh" else ch.era_en,
        "body": ch.body_zh if lang == "zh" else ch.body_en,
        "motif": ch.motif,
        "highlights": (topic["highlights_zh"] if lang == "zh"
                       else topic["highlights_en"]),
        # related = a handful of sibling topics from other chapters
        "related": [t["aliases"][0] for t in TOPICS
                    if t["id"] != topic["id"]][:6],
    }


def suggested_topics(lang: str = "zh", n: int = 8) -> list[str]:
    """Default chip suggestions shown on the empty state."""
    # pick the canonical (first) alias of each topic, take first n
    return [t["aliases"][0] for t in TOPICS[:n]]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def chapter_index() -> dict[str, Chapter]:
    return {c.id: c for c in CHAPTERS}


def search(query: str, lang: str = "zh") -> list[dict]:
    """Naive substring search across both languages of every chapter."""
    q = query.strip().lower()
    if not q:
        return []
    hits: list[dict] = []
    for c in CHAPTERS:
        haystack_parts = [c.title_zh, c.title_en, c.body_zh, c.body_en,
                          c.era_zh, c.era_en]
        haystack = " ".join(haystack_parts).lower()
        if q in haystack:
            hits.append({
                "id": c.id,
                "title": c.title_zh if lang == "zh" else c.title_en,
                "era": c.era_zh if lang == "zh" else c.era_en,
                # a short snippet around the first match
                "snippet": _snippet(c.body_zh if lang == "zh" else c.body_en, q),
            })
    return hits


def _snippet(text: str, q: str, width: int = 60) -> str:
    lower = text.lower()
    idx = lower.find(q)
    if idx == -1:
        # search matched the other language; just return the start.
        return text[: 2 * width] + ("…" if len(text) > 2 * width else "")
    start = max(0, idx - width)
    end = min(len(text), idx + len(q) + width)
    snippet = text[start:end]
    if start > 0:
        snippet = "…" + snippet
    if end < len(text):
        snippet = snippet + "…"
    return snippet
