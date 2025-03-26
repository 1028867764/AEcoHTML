import os
from pathlib import Path

# 1. 定义HTML模板
html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
<!-- 引入外部CSS文件 -->
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="pricetag">报价区间</div>
    <div class="description">{title}</div>
</body>
</html>
"""

# 2. 定义Map（键值对）
pages_map = {
    "唇形目/唇形科/薄荷属·Mentha/椒样薄荷": "Creature/MenthaJiaoyang",
    "唇形目/唇形科/薄荷属·Mentha/留兰香薄荷": "Creature/MenthaLiulanxiang",
    "唇形目/唇形科/刺蕊草属·Pogostemon/广藿香": "Creature/Pogostemon",
    "唇形目/唇形科/仙草属·Platostoma/仙草": "Creature/Platostoma",
    "唇形目/唇形科/紫苏属·Perilla/紫苏": "Creature/Perilla",
    "唇形目/木樨科/素馨属·Jasminum/茉莉花": "Creature/Jasminum",
    "唇形目/脂麻科/脂麻属·Sesamum/芝麻粒": "Creature/Sesamum",
    "豆科/菜豆属·Phaseolus/荷包豆": "Creature/PhaseolusHebaodou",
    "豆科/菜豆属·Phaseolus/四季豆": "Creature/PhaseolusSijidou",
    "豆科/大豆属·Glycine/毛豆": "Creature/GlycineMaodou",
    "豆科/大豆属·Glycine/青大豆": "Creature/GlycineQingdadou",
    "豆科/大豆属·Glycine/黄大豆1号": "Creature/GlycineHuangdadou1hao",
    "豆科/大豆属·Glycine/黑大豆": "Creature/GlycineHeidadou",
    "豆科/大豆属·Glycine/黄大豆粉": "Creature/GlycineHuangdadoufen",
    "豆科/大豆属·Glycine/豆腐": "Creature/GlycineDoufu",
    "豆科/大豆属·Glycine/豆腐泡": "Creature/GlycineDoufupao",
    "豆科/大豆属·Glycine/豆腐干": "Creature/GlycineDoufugan",
    "豆科/大豆属·Glycine/腐竹": "Creature/GlycineFuzhu",
    "豆科/大豆属·Glycine/大豆油": "Creature/GlycineDadouyou",
    "豆科/大豆属·Glycine/酱油": "Creature/GlycineJiangyou",
    "豆科/大豆属·Glycine/黑豆豉": "Creature/GlycineHeidouchi",
    "豆科/大豆属·Glycine/黄豆酱": "Creature/GlycineHuangdoujiang",
    "豆科/大豆属·Glycine/腐乳": "Creature/GlycineFuru",
    "豆科/大豆属·Glycine/豆粕": "Creature/GlycineDoupo",
    "豆科/大豆属·Glycine/黄豆芽": "Creature/GlycineHuangdouya",
    "豆科/豇豆属·Vigna/豇豆荚": "Creature/VignaJiangdoujia",
    "豆科/豇豆属·Vigna/白豇豆": "Creature/VignaBaijiangdou",
    "豆科/豇豆属·Vigna/绿豆": "Creature/VignaLvdou",
    "豆科/豇豆属·Vigna/绿豆芽": "Creature/VignaLvdouya",
    "豆科/豇豆属·Vigna/绿豆淀粉": "Creature/VignaLvdoudianfen",
    "豆科/豇豆属·Vigna/红豆": "Creature/VignaHongdou",
    "豆科/落花生属·Arachis/带壳花生": "Creature/ArachisDaikehuasheng",
    "豆科/落花生属·Arachis/花生仁": "Creature/ArachisHuashengren",
    "豆科/落花生属·Arachis/花生油": "Creature/ArachisHuashengyou",
    "豆科/落花生属·Arachis/花生粕": "Creature/ArachisHuashengpo",
    "豆科/豌豆属·Pisum/豌豆荚": "Creature/PisumWandoujia",
    "豆科/豌豆属·Pisum/豌豆": "Creature/PisumWandou",
    "豆科/豌豆属·Pisum/豌豆藤": "Creature/PisumWandouteng",
    "豆科/豌豆属·Pisum/豌豆芽": "Creature/PisumWandouya",
    "豆科/豌豆属·Pisum/豌豆淀粉": "Creature/PisumWandoudianfen",
    "豆科/甘草属·Glycyrrhiza/甘草": "Creature/Glycyrrhiza",
    "禾本目/凤梨科/凤梨属·Ananas/菠萝": "Creature/Ananas",
    "禾本目/禾本科/稻属·Oryza/籼米": "Creature/OryzaXianmi",
    "禾本目/禾本科/稻属·Oryza/粘米粉": "Creature/OryzaZhanmifen",
    "禾本目/禾本科/稻属·Oryza/糯米": "Creature/OryzaNuomi",
    "禾本目/禾本科/稻属·Oryza/糯米粉": "Creature/OryzaNuomifen",
    "禾本目/禾本科/稻属·Oryza/米糠": "Creature/OryzaMikang",
    "禾本目/禾本科/稻属·Oryza/米酒": "Creature/OryzaMijiu",
    "禾本目/禾本科/稻属·Oryza/米醋": "Creature/OryzaMicu",
    "禾本目/禾本科/稻属·Oryza/稻秆": "Creature/OryzaDaogan",
    "禾本目/禾本科/甘蔗属·Saccharum/甘蔗": "Creature/SaccharumGanzhe",
    "禾本目/禾本科/甘蔗属·Saccharum/一级白糖": "Creature/SaccharumYijibaitang",
    "禾本目/禾本科/甘蔗属·Saccharum/三氯蔗糖": "Creature/SaccharumSanlvzhetang",
    "禾本目/禾本科/甘蔗属·Saccharum/蔗渣": "Creature/SaccharumZheZha",
    "禾本目/禾本科/小麦属·Triticum/高筋面粉": "Creature/TriticumGao",
    "禾本目/禾本科/小麦属·Triticum/中筋面粉": "Creature/TriticumZhong",
    "禾本目/禾本科/小麦属·Triticum/低筋面粉": "Creature/TriticumDi",
    "禾本目/禾本科/小麦属·Triticum/澄粉": "Creature/TriticumCheng",
    "禾本目/禾本科/小麦属·Triticum/麦麸": "Creature/TriticumMaifu",
    "禾本目/禾本科/小麦属·Triticum/麦秆": "Creature/TriticumMaigan",
    "禾本目/禾本科/玉米属·Zea/饲料玉米棒": "Creature/ZeaSiliaobang",
    "禾本目/禾本科/玉米属·Zea/饲料玉米粒": "Creature/ZeaSiliaoli",
    "禾本目/禾本科/玉米属·Zea/水果玉米棒": "Creature/ZeaShuiguobang",
    "禾本目/禾本科/玉米属·Zea/水果玉米粒": "Creature/ZeaShuiguoli",
    "禾本目/禾本科/玉米属·Zea/糯玉米棒": "Creature/ZeaNuobang",
    "禾本目/禾本科/玉米属·Zea/玉米淀粉": "Creature/ZeaDianfen",
    "禾本目/禾本科/玉米属·Zea/玉米秆": "Creature/ZeaGan",
    "禾本目/竹亚科/竹亚科·Bambusoideae/竹笋": "Creature/BambusoideaeZhusun",
    "禾本目/竹亚科/竹亚科·Bambusoideae/竹浆": "Creature/BambusoideaeZhujiang",
    "禾本目/竹亚科/竹亚科·Bambusoideae/竹木材": "Creature/BambusoideaeZhumucai",
    "禾本目/竹亚科/竹亚科·Bambusoideae/竹叶": "Creature/BambusoideaeZhuye",
    "禾本目/竹亚科/竹亚科·Bambusoideae/竹篾": "Creature/BambusoideaeZhumie",
    "葫芦科/黄瓜属·Cucumis/黄瓜": "Creature/CucumisHuang",
    "葫芦科/黄瓜属·Cucumis/哈密瓜": "Creature/CucumisHami",
    "葫芦科/黄瓜属·Cucumis/香瓜": "Creature/CucumisXiang",
    "葫芦科/罗汉果属·Siraitia/罗汉果": "Creature/Siraitia",
    "葫芦科/西瓜属·Citrullus/西瓜": "Creature/Citrullus",
    "葫芦科/西瓜属·Citrullus/西瓜籽": "Creature/CitrullusZi",
    "葫芦科/南瓜属·Cucurbita/南瓜": "Creature/Cucurbita",
    "葫芦科/南瓜属·Cucurbita/南瓜籽": "Creature/CucurbitaZi",
    "葫芦科/南瓜属·Cucurbita/南瓜苗": "Creature/CucurbitaMiao",
    "葫芦科/南瓜属·Cucurbita/南瓜花": "Creature/CucurbitaHua",
    "葫芦科/丝瓜属·Luffa/丝瓜": "Creature/Luffa",
    "葫芦科/冬瓜属·Benincasa/冬瓜": "Creature/Benincasa",
    "姜目/芭蕉科/芭蕉属·Musa/Williams香蕉": "Creature/Musa",
    "姜目/竹芋科/柊叶属·Phrynium/柊叶": "Creature/Phrynium",
    "姜目/姜科/姜黄属·Curcuma/姜黄": "Creature/Curcuma",
    "姜目/姜科/姜属·Zingiber/生姜": "Creature/Zingiber",
    "姜目/姜科/砂仁属·Wurfbainia/爪哇白豆蔻": "Creature/Wurfbainia",
    "姜目/姜科/草果属·Lanxangia/草果": "Creature/Lanxangia",
    "菊科/蒲公英属·Taraxacum/蒲公英": "Creature/Taraxacum",
    "菊科/莴苣属·Lactuca/生菜": "Creature/LactucaShengcai",
    "菊科/莴苣属·Lactuca/油麦菜": "Creature/LactucaYoumaicai",
    "菊科/莴苣属·Lactuca/莴笋": "Creature/LactucaWosun",
    "菊科/向日葵属·Helianthus/葵花籽": "Creature/Helianthus",
    "菊科/菊属·Chrysanthemum/菊花": "Creature/Chrysanthemum",
    "壳斗目/壳斗科/栗属·Castanea/板栗": "Creature/Castanea",
    "壳斗目/胡桃科/胡桃属·Juglans/核桃": "Creature/Juglans",
    "壳斗目/胡桃科/黄杞属·Engelhardtia/大叶茶": "Creature/Engelhardtia",
    "蔷薇目/蔷薇科/草莓属·Fragaria/草莓": "Creature/Fragaria",
    "蔷薇目/蔷薇科/梨属·Pyrus/梨子": "Creature/Pyrus",
    "蔷薇目/蔷薇科/李属·Prunus/扁桃仁": "Creature/PrunusBiantaoren",
    "蔷薇目/蔷薇科/李属·Prunus/桃子": "Creature/PrunusTao",
    "蔷薇目/蔷薇科/李属·Prunus/李子": "Creature/PrunusLi",
    "蔷薇目/蔷薇科/李属·Prunus/梅子": "Creature/PrunusMei",
    "蔷薇目/蔷薇科/枇杷属·Eriobotrya/枇杷": "Creature/Eriobotrya",
    "蔷薇目/蔷薇科/枇杷属·Eriobotrya/枇杷叶": "Creature/EriobotryaYe",
    "蔷薇目/蔷薇科/苹果属·Malus/80mm红富士苹果": "Creature/Malus",
    "蔷薇目/蔷薇科/蔷薇属·Rosa/卡罗拉玫瑰": "Creature/RosaCarola",
    "蔷薇目/蔷薇科/蔷薇属·Rosa/黑魔术玫瑰": "Creature/RosaBlackmagic",
    "蔷薇目/蔷薇科/蔷薇属·Rosa/戴安娜玫瑰": "Creature/RosaDiana",
    "蔷薇目/蔷薇科/蔷薇属·Rosa/精油玫瑰": "Creature/RosaEssentialoil",
    "蔷薇目/蔷薇科/山楂属·Crataegus/山楂": "Creature/Crataegus",
    "蔷薇目/鼠李科/枣属·Ziziphus/一级红枣": "Creature/Ziziphus",
    "茄目/茄科/辣椒属·Capsicum/辣椒": "Creature/Capsicum",
    "茄目/茄科/茄属·Solanum/番茄": "Creature/SolanumTomato",
    "茄目/茄科/茄属·Solanum/茄子": "Creature/SolanumEggplant",
    "茄目/茄科/茄属·Solanum/土豆": "Creature/SolanumPotato",
    "茄目/旋花科/番薯属·Ipomoea/红薯": "Creature/IpomoeaHongshu",
    "茄目/旋花科/番薯属·Ipomoea/紫薯": "Creature/IpomoeaZishu",
    "茄目/旋花科/番薯属·Ipomoea/红薯叶": "Creature/IpomoeaHongshuye",
    "茄目/旋花科/番薯属·Ipomoea/空心菜": "Creature/IpomoeaKongxincai",
    "伞形科/当归属·Angelica/白芷": "Creature/Angelica",
    "伞形科/胡萝卜属·Daucus/胡萝卜": "Creature/Daucus",
    "伞形科/茴香属·Foeniculum/茴香籽": "Creature/Foeniculum",
    "伞形科/芹属·Apium/细芹菜": "Creature/ApiumXi",
    "伞形科/芹属·Apium/粗芹菜": "Creature/ApiumCu",
    "伞形科/芫荽属·Coriandrum/芫荽": "Creature/Coriandrum",
    "伞形科/芫荽属·Coriandrum/芫荽籽": "Creature/CoriandrumZi",
    "伞形科/孜然芹属·Cuminum/孜然籽": "Creature/Cuminum",
    "十字花科/萝卜属·Raphanus/萝卜": "Creature/Raphanus",
    "十字花科/菘蓝属·Isatis/大青叶": "Creature/IsatisYe",
    "十字花科/菘蓝属·Isatis/板蓝根": "Creature/IsatisGen",
    "十字花科/芸薹属_芥菜·Brassica_juncea/榨菜": "Creature/BrassicaJunceaZhacai",
    "十字花科/芸薹属_芥菜·Brassica_juncea/大头菜": "Creature/BrassicaJunceaDatoucai",
    "十字花科/芸薹属_芥菜·Brassica_juncea/雪里蕻": "Creature/BrassicaJunceaXuelihong",
    "十字花科/芸薹属_芥菜·Brassica_juncea/包心芥菜": "Creature/BrassicaJunceaBaoxin",
    "十字花科/芸薹属_芥菜·Brassica_juncea/其它芥菜": "Creature/BrassicaJunceaOther",
    "十字花科/芸薹属_芥菜·Brassica_juncea/黄芥末籽": "Creature/BrassicaJunceaZi",
    "十字花科/芸薹属_甘蓝·Brassica_oleracea/西兰花": "Creature/BrassicaOleraceaXilanhua",
    "十字花科/芸薹属_甘蓝·Brassica_oleracea/花椰菜": "Creature/BrassicaOleraceaHuayecai",
    "十字花科/芸薹属_甘蓝·Brassica_oleracea/卷心菜": "Creature/BrassicaOleraceaJuanxincai",
    "十字花科/芸薹属_甘蓝·Brassica_oleracea/其它甘蓝": "Creature/BrassicaOleraceaOther",
    "十字花科/芸薹属_芸薹·Brassica_rapa/大白菜": "Creature/BrassicaRapaDabaicai",
    "十字花科/芸薹属_芸薹·Brassica_rapa/娃娃菜": "Creature/BrassicaRapaWawacai",
    "十字花科/芸薹属_芸薹·Brassica_rapa/白菜苔": "Creature/BrassicaRapaBaicaitai",
    "十字花科/芸薹属_芸薹·Brassica_rapa/其它白菜": "Creature/BrassicaRapaOther",
    "松柏目/柏科/杉属·Cunninghamia/杉木材": "Creature/Cunninghamia",
    "松柏目/松科/松属·Pinus/马尾松木材": "Creature/Pinus",
    "桃金娘科/桉属·Eucalyptus/尾叶桉木材": "Creature/Eucalyptus",
    "桃金娘科/蒲桃属·Syzygium/公丁香": "Creature/Syzygium",
    "石蒜科/葱属·Allium/葱": "Creature/AlliumCong",
    "石蒜科/葱属·Allium/韭菜": "Creature/AlliumJiucai",
    "石蒜科/葱属·Allium/蒜瓣": "Creature/AlliumSuanban",
    "石蒜科/葱属·Allium/蒜苗": "Creature/AlliumSuanmiao",
    "石蒜科/葱属·Allium/荞头": "Creature/AlliumQiaotou",
    "石蒜科/葱属·Allium/洋葱": "Creature/AlliumYangcong",
    "石蒜科/葱属·Allium/红葱头": "Creature/AlliumHongcongtou",
    "无患子目/漆树科/芒果属·Mangifera/芒果": "Creature/Mangifera",
    "无患子目/漆树科/腰果属·Anacardium/腰果仁": "Creature/Anacardium",
    "无患子目/无患子科/荔枝属·Litchi/荔枝": "Creature/Litchi",
    "无患子目/无患子科/龙眼属·Dimocarpus/龙眼": "Creature/Dimocarpus",
    "无患子目/芸香科/柑橘属·Citrus/柚": "Creature/CitrusYou",
    "无患子目/芸香科/柑橘属·Citrus/橘": "Creature/CitrusJv",
    "无患子目/芸香科/柑橘属·Citrus/橙": "Creature/CitrusCheng",
    "无患子目/芸香科/柑橘属·Citrus/柑": "Creature/CitrusGan",
    "无患子目/芸香科/柑橘属·Citrus/柠檬": "Creature/CitrusNingmeng",
    "无患子目/芸香科/柑橘属·Citrus/橘皮": "Creature/CitrusJvpi",
    "无患子目/芸香科/花椒属·Zanthoxylum/花椒": "Creature/Zanthoxylum",
    "樟科/肉桂属·Cinnamomum/肉桂": "Creature/Cinnamomum",
    "樟科/月桂属·Laurus/月桂叶": "Creature/Laurus",
    "樟科/樟属·Camphora/樟树木材": "Creature/Camphora",
    "棕榈科/椰属·Cocos/椰子油": "Creature/CocosYou",
    "棕榈科/椰属·Cocos/椰子壳": "Creature/CocosKe",
    "棕榈科/油棕属·Elaeis/棕榈油": "Creature/ElaeisZonglvyou",
    "棕榈科/油棕属·Elaeis/棕榈仁油": "Creature/ElaeisZonglvrenyou",
    "其他植物/五味子科/八角属·Illicium/八角": "Creature/Illicium",
    "其他植物/锦葵科/棉花属·Gossypium/棉花": "Creature/GossypiumMianhua",
    "其他植物/锦葵科/棉花属·Gossypium/棉纱": "Creature/GossypiumMiansha",
    "其他植物/莲科/莲属·Nelumbo/莲藕": "Creature/Nelumbo",
    "其他植物/忍冬科/忍冬属·Lonicera/忍冬花": "Creature/Lonicera",
    "其他植物/山茶科/山茶属·Camellia/茶叶": "Creature/CamelliaChaye",
    "其他植物/山茶科/山茶属·Camellia/红茶粉": "Creature/CamelliaHongchafen",
    "其他植物/茜草科/栀子属·Gardenia/栀子": "Creature/Gardenia",
    "其他植物/葡萄科/葡萄属·Vitis/葡萄": "Creature/Vitis",
    "其他植物/葡萄科/葡萄属·Vitis/葡萄干": "Creature/VitisGan",
    "其他植物/仙人掌科/蛇鞭柱属·Selenicereus/火龙果": "Creature/Selenicereus",
    "其他植物/大戟科/木薯属·Manihot/木薯淀粉": "Creature/Manihot",
    "其他植物/天南星科/芋属·Colocasia/芋头": "Creature/ColocasiaYutou",
    "其他植物/天南星科/芋属·Colocasia/芋叶柄": "Creature/ColocasiaYuyebing",
    "雉科/原鸡属·Gallus/活鸡": "Creature/GallusAlive",
    "雉科/原鸡属·Gallus/白条鸡": "Creature/GallusBaitiao",
    "雉科/原鸡属·Gallus/鸡胸肉": "Creature/GallusChest",
    "雉科/原鸡属·Gallus/鸡腿": "Creature/GallusDrumstick",
    "雉科/原鸡属·Gallus/鸡翅": "Creature/GallusWing",
    "雉科/原鸡属·Gallus/鸡翅尖": "Creature/GallusWingtip",
    "雉科/原鸡属·Gallus/鸡翅根": "Creature/GallusDrumette",
    "雉科/原鸡属·Gallus/鸡爪": "Creature/GallusClaw",
    "雉科/原鸡属·Gallus/鸡肠": "Creature/GallusIntestine",
    "雉科/原鸡属·Gallus/鸡胗": "Creature/GallusGizzard",
    "雉科/原鸡属·Gallus/鸡心": "Creature/GallusHeart",
    "雉科/原鸡属·Gallus/鸡肝": "Creature/GallusLiver",
    "雉科/原鸡属·Gallus/鸡皮": "Creature/GallusSkin",
    "雉科/原鸡属·Gallus/鸡蛋": "Creature/GallusEgg",
    "雉科/原鸡属·Gallus/鸡毛": "Creature/GallusFeather",
    "鸭科/鸭属·Anas|疣鼻栖鸭属·Cairina/活鸭": "Creature/DuckAlive",
    "鸭科/鸭属·Anas|疣鼻栖鸭属·Cairina/白条鸭": "Creature/DuckBaitiao",
    "鸭科/鸭属·Anas|疣鼻栖鸭属·Cairina/鸭翅": "Creature/DuckWing",
    "鸭科/鸭属·Anas|疣鼻栖鸭属·Cairina/鸭腿": "Creature/DuckDrumstick",
    "鸭科/鸭属·Anas|疣鼻栖鸭属·Cairina/鸭掌": "Creature/DuckPaw",
    "鸭科/鸭属·Anas|疣鼻栖鸭属·Cairina/鸭肠": "Creature/DuckIntestine",
    "鸭科/鸭属·Anas|疣鼻栖鸭属·Cairina/鸭胗": "Creature/DuckGizzard",
    "鸭科/鸭属·Anas|疣鼻栖鸭属·Cairina/鸭舌": "Creature/DuckTongue",
    "鸭科/鸭属·Anas|疣鼻栖鸭属·Cairina/鸭脖": "Creature/DuckNeck",
    "鸭科/鸭属·Anas|疣鼻栖鸭属·Cairina/鸭心": "Creature/DuckHeart",
    "鸭科/鸭属·Anas|疣鼻栖鸭属·Cairina/鸭肝": "Creature/DuckLiver",
    "鸭科/鸭属·Anas|疣鼻栖鸭属·Cairina/鸭蛋": "Creature/DuckEgg",
    "鸭科/鸭属·Anas|疣鼻栖鸭属·Cairina/皮蛋": "Creature/DuckPidan",
    "鸭科/鸭属·Anas|疣鼻栖鸭属·Cairina/鸭毛": "Creature/DuckFeather",
    "猪科/猪属·Sus/生猪": "Creature/SusAlive",
    "猪科/猪属·Sus/白条猪": "Creature/SusBaitiao",
    "猪科/猪属·Sus/猪皮": "Creature/SusSkin",
    "猪科/猪属·Sus/猪板油": "Creature/SusZhubanyou",
    "猪科/猪属·Sus/肥膘肉": "Creature/SusFeibiaorou",
    "猪科/猪属·Sus/猪面颊": "Creature/SusFace",
    "猪科/猪属·Sus/猪下巴": "Creature/SusChin",
    "猪科/猪属·Sus/猪颈肉": "Creature/SusNeck",
    "猪科/猪属·Sus/猪舌头": "Creature/SusTongue",
    "猪科/猪属·Sus/猪耳": "Creature/SusEar",
    "猪科/猪属·Sus/猪脑": "Creature/SusBrain",
    "猪科/猪属·Sus/猪脊骨": "Creature/SusSpine",
    "猪科/猪属·Sus/猪肋排骨": "Creature/SusChop",
    "猪科/猪属·Sus/猪外脊肉": "Creature/SusOutofspine",
    "猪科/猪属·Sus/猪里脊肉": "Creature/SusTenderloin",
    "猪科/猪属·Sus/五花肉": "Creature/SusBelly",
    "猪科/猪属·Sus/猪肩胛肉": "Creature/SusShoulder",
    "猪科/猪属·Sus/猪前大腿": "Creature/SusLegfore",
    "猪科/猪属·Sus/猪后大腿": "Creature/SusLeghind",
    "猪科/猪属·Sus/猪大腿骨": "Creature/SusLegbone",
    "猪科/猪属·Sus/猪前肘": "Creature/SusElbowfore",
    "猪科/猪属·Sus/猪后肘": "Creature/SusElbowhind",
    "猪科/猪属·Sus/猪前蹄": "Creature/SusTrotterfore",
    "猪科/猪属·Sus/猪后蹄": "Creature/SusTrotterhind",
    "猪科/猪属·Sus/猪尾巴": "Creature/SusTail",
    "猪科/猪属·Sus/猪腰子": "Creature/SusKidney",
    "猪科/猪属·Sus/猪心": "Creature/SusHeart",
    "猪科/猪属·Sus/猪肝": "Creature/SusLiver",
    "猪科/猪属·Sus/猪肺": "Creature/SusLung",
    "猪科/猪属·Sus/猪小肠": "Creature/SusSmallintestine",
    "猪科/猪属·Sus/猪大肠": "Creature/SusLargeintestine",
    "猪科/猪属·Sus/猪肚": "Creature/SusStomach",
    "其他动物/粉甲虫属/粉甲虫属·Tenebrio/面包虫": "Creature/Tenebrio",
    "其他动物/对虾科/对虾科·Penaeidae/对虾": "Creature/Penaeidae",
    "其他动物/田螺科/田螺科·Viviparidae/田螺": "Creature/Viviparidae",
    "菌类/菌类·味精/米曲霉菌": "Creature/JunleiMiqumeijun",
    "菌类/菌类·味精/酿酒酵母": "Creature/JunleiNiangjiujiaomu",
    "菌类/菌类·味精/醋酸菌": "Creature/JunleiCusuanjun",
    "菌类/菌类·味精/毛霉菌": "Creature/JunleiMaomeijun",
    "菌类/菌类·味精/乳杆菌": "Creature/JunleiRuganjun",
    "菌类/菌类·味精/谷氨酸钠": "Creature/JunleiGuansuanna",
    "菌类/菌类·味精/IMP": "Creature/JunleiIMP",
    "菌类/菌类·味精/GMP": "Creature/JunleiGMP",
    "菌类/菌类·味精/黑木耳": "Creature/JunleiHeimuer",
    "菌类/菌类·味精/金针菇": "Creature/JunleiJinzhengu",
    "菌类/菌类·味精/香菇": "Creature/JunleiXianggu"
}

# 3. 指定桌面路径（跨平台兼容）
desktop_path = Path.home() / "Desktop" / "HTML_Files"
desktop_path.mkdir(exist_ok=True)  # 自动创建文件夹

# 4. 批量生成HTML文件
for page_text, filename in pages_map.items():
    # 填充模板
    html_content = html_template.format(title=page_text)
    
    # 生成文件路径（确保.html后缀）
    file_path = desktop_path / f"{filename}.html"
    
    # 写入文件
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)

print(f"✅ 已生成 {len(pages_map)} 个HTML文件到桌面目录: {desktop_path}")