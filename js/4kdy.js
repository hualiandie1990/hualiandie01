var rule = {
    author: '',
    title: '好影快看 - 《护宝寻踪》播放页',
    类型: '影视播放页',
    //首页网址
    host: 'https://www.hitv.app/',
    hostJs: ``,
    headers: {
        'User - Agent': 'Mozilla/5.0'
    },
    编码: 'utf - 8',
    timeout: 5000,
    homeUrl: '/',
    //分类页
    url: '',
    //筛选页
    filter_url: '',
    detailUrl: '',
    searchUrl: '/search/-------------.html',
    searchable: 1,
    quickSearch: 1,
    filterable: 1,
    limit: 10,
    double: false,
    class_name: '电影&电视剧&综艺&动漫&儿童',
    //静态分类值
    class_url: 'tv/1&tv/2&tv/3&tv/4&tv/58',
    推荐: '*',
    //数组、标题、图片、副标题、链接，分类页找参数
    一级: '',
    //搜索页找参数  数组标题图片副标题链接
    搜索: '',
    二级: `js:
 let html = request(input);
 VOD = {};
 VOD.vod_id = input;
 //定位详情页标题
 VOD.vod_name = pd(html, "h1.module - info - heading a&&Text");
 //定位详情页图片链接
 VOD.vod_pic = pd(html, "meta[property='og:image']&&content");
 //定位详情页类型
 let types = pd(html, ".module - info - tag - link a:contains('电视剧')");
 types += pd(html, ".module - info - tag - link a:contains('剧情')");
 VOD.type_name = types;
 //状态备注
 VOD.vod_remarks = pd(html, ".module - info - item div.module - info - item - content font.red&&Text");
 //年份
 VOD.vod_year = pd(html, ".module - info - tag - link a[title*='20']&&Text");
 //地区
 VOD.vod_area = pd(html, ".module - info - tag - link a[title*='中国']&&Text");
 //导演
 VOD.vod_director = pd(html, "meta[property='og:video:director']&&content");
 //演员
 VOD.vod_actor = pd(html, "meta[property='og:video:actor']&&content");
 //简介
 VOD.vod_content = pd(html, "meta[name='description']&&content");
 //线路
 let r_ktabs = pd(html, '.module - tab - item.tab - item');
 let ktabs = r_ktabs.map(it => pd(it,'span&&Text'));
 VOD.vod_play_from = ktabs.join('$$$');
 let klists = [];
 //播放
 let r_plists = pd(html, '.module - play - list - link');
 r_plists.forEach((rp) => {
     let klist = pd(rp, 'a&&Text') + '$' + pd(rp, 'a&&href');
     klists.push(klist);
 });
 VOD.vod_play_url = klists.join('$$$')
 `,
    //是否启用辅助嗅探: 1,0
    sniffer: 0,
    // 辅助嗅探规则
    isVideo: 'http((?!http).){26,}\\.(m3u8|mp4|flv|avi|mkv|wmv|mpg|mpeg|mov|ts|3gp|rm|rmvb|asf|m4a|mp3|wma)',
    play_parse: true,
    //播放地址通用解析
    lazy: `js:
 let kcode = JSON.parse(request(input).match(/var player_aaaa=(.*?);/)[1]);
 let kurl = kcode.url;
 if (kcode.encrypt == '1') {
     url = unescape(url)
 } else if (kcode.encrypt == '2') {
     url = unescape(base64Decode(url))
 };
 if (/\\.(m3u8|mp4)/.test(kurl)) {
     input = { jx: 0, parse: 0, url: kurl }
 } else {
     input = { jx: 0, parse: 1, url: input }
 }`,
    filter: {}
}

// 由于没有真实运行环境（比如特定的爬虫框架），无法直接运行此代码进行测试
// 但上述代码已根据提供的HTML结构尽量准确地映射到规则模板中