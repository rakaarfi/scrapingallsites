import allsites

# list of category
categories = ['top_news', 'politics', 'business', 'sports', 'entertainment', 'health', 'science_tech', 'news', 'world_news', 'local_news', 'travel']

links_data = {
    'detik': {
        'top_news': allsites.DETIK_TOPNEWS,
        'sports': allsites.DETIK_ALL_SPORT,
        'entertainment': allsites.DETIK_POP,
        'health': allsites.DETIK_HEALTH,
        'science_tech': allsites.DETIK_INET,
        'news': allsites.DETIK_NEWS,
        'local_news': allsites.DETIK_ALL_LOCALNEWS,
        'travel': allsites.DETIK_ALL_TRAVEL
    },
    'kompas': {
        'top_news': allsites.KOMPAS_ALL_TOPNEWS,
        'business': allsites.KOMPAS_ALL_BUSINESS,
        'sports': allsites.KOMPAS_BOLA,
        'health': allsites.KOMPAS_HEALTH,
        'science_tech': allsites.KOMPAS_ALL_SCIENCETECH,
        'news': allsites.KOMPAS_NEWS,
        'world_news': allsites.KOMPAS_GLOBAL,
        'local_news': allsites.KOMPAS_ALL_LOCALNEWS,
        'travel': allsites.KOMPAS_ALL_TRAVEL
    },
    'tribun': {
        'politics': allsites.TRIBUN_ALL_POLITICS,
        'business': allsites.TRIBUN_ALL_BUSINESS,
        'sports': allsites.TRIBUN_ALL_SPORT,
        'entertainment': allsites.TRIBUN_ALL_ENTERTAINMENT,
        'health': allsites.TRIBUN_HEALTH,
        'science_tech': allsites.KOMPAS_ALL_SCIENCETECH,
        'news': allsites.TRIBUN_NEWS,
        'world_news': allsites.TRIBUN_INTERNASIONAL,
        'local_news': allsites.TRIBUN_ALL_LOCALNEWS,
        'travel': allsites.TRIBUN_TRAVEL
    }
}