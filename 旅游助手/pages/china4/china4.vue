<template>
  <!-- 张家界国家森林公园 静态页面 -->
  <view class="zhangjiajie-page">
    <!-- 顶部导航 -->
    <view class="header">
      <view class="logo">张家界森林公园</view>
    </view>

    <!-- 轮播大图 -->
    <view class="banner">
      <image
        src="https://ts3.tc.mm.bing.net/th/id/OIP-C.c4-o6Ly385hokpRmGVurIAHaEK?rs=1&pid=ImgDetMain&o=7&rm=3"
        mode="widthFix"
        class="banner-img"
      ></image>
    </view>

    <!-- 景区简介 -->
    <view class="section intro">
      <view class="title">景区简介</view>
      <view class="content">
        张家界国家森林公园位于湖南省张家界市武陵源区，1982年成为中国第一个国家森林公园，是世界自然遗产、世界地质公园、国家5A级景区。公园总面积48.1平方公里，以“奇峰三千、秀水八百”闻名，独特的石英砂岩峰林地貌冠绝全球。
      </view>
      <view class="content">
        这里是电影《阿凡达》悬浮山原型取景地，也是86版《西游记》等影视作品的拍摄地。景区森林覆盖率高达98%，空气清新，物种丰富，集雄、奇、幽、野、秀于一体，是自然观光、生态康养的绝佳目的地{insert\_element\_0\_}。
      </view>
    </view>

    <!-- 核心景点 -->
    <view class="section scenic">
      <view class="title">核心景点</view>
      <view class="scenic-list">
        <view class="item" v-for="(item, index) in scenicList" :key="index">
          <image :src="item.img" mode="aspectFill" class="item-img"></image>
          <view class="item-name">{{ item.name }}</view>
          <view class="item-desc">{{ item.desc }}</view>
        </view>
      </view>
    </view>

    <!-- 游玩信息 -->
    <view class="section info">
      <view class="title">游玩信息</view>
      <view class="info-item">
        <text class="label">地址：</text>
        <text>湖南省张家界市武陵源区金鞭路279号</text>
      </view>
      <view class="info-item">
        <text class="label">门票：</text>
        <text>成人165元（4日有效），环保车119元，学生半价</text>
      </view>
      <view class="info-item">
        <text class="label">开放时间：</text>
        <text>07:00-17:00（17:00停止入园）</text>
      </view>
      <view class="info-item">
        <text class="label">最佳季节：</text>
        <text>4-10月（春夏翠绿、秋冬云海）</text>
      </view>
      <view class="info-item">
        <text class="label">必体验：</text>
        <text>百龙天梯、袁家界悬浮山、金鞭溪徒步</text>
      </view>
    </view>

    <!-- 底部 -->
    <view class="footer" @tap="toAI">
      <text>去咨询一下</text>
    </view>
  </view>
</template>

<script setup>
const toAI = () => {
  uni.navigateTo({
    url: '/pages/assistant/assistant'
  });
};
// 核心景点数据
const scenicList = [
  {
    name: '袁家界 · 悬浮山原型',
    desc: '《阿凡达》哈利路亚山原型乾坤柱，天下第一桥天然石桥，峰林险峻奇幻。',
    img: 'https://ts1.tc.mm.bing.net/th/id/OIP-C.EN9O86P5-K3G0pgyR_cfmwHaE8?rs=1&pid=ImgDetMain&o=7&rm=3'
  },
  {
    name: '金鞭溪 · 峡谷画廊',
    desc: '7.5公里清溪峡谷，两岸峰林倒映，猕猴嬉戏，被誉为“世界最美峡谷溪流”。',
    img: 'https://ts3.tc.mm.bing.net/th/id/OIP-C.YRCFzbeIHkyvq2h_lJ3lRAHaE8?rs=1&pid=ImgDetMain&o=7&rm=3'
  },
  {
    name: '黄石寨 · 全景峰林',
    desc: '海拔1080米观景台，360°俯瞰三千奇峰，“不到黄石寨，枉到张家界”。',
    img: 'https://ts4.tc.mm.bing.net/th/id/OIP-C.Vi-FIRE0cnZ7QY7MwV0EzgHaE6?rs=1&pid=ImgDetMain&o=7&rm=3'
  },
  {
    name: '杨家界 · 峰墙奇观',
    desc: '全球罕见石英砂岩峰墙，天然长城绵延3公里，天波府俯瞰峰林阵列。',
    img: 'https://ts3.tc.mm.bing.net/th/id/OIP-C.PltA4fHxPKWRvsGH_DoLLAHaE6?rs=1&pid=ImgDetMain&o=7&rm=3'
  }
]
</script>

<style scoped>
/* 全局 */
.zhangjiajie-page {
  width: 100%;
  background: #f5f9f7;
  color: #333;
}

/* 顶部导航 */
.header {
  background-color: #2c785e;
  color: #fff;
  padding: 20rpx 30rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.logo {
  font-size: 36rpx;
  font-weight: bold;
}

/* 轮播 */
.banner {
  width: 100%;
}
.banner-img {
  width: 100%;
  height: 400rpx;
}

/* 区块通用 */
.section {
  padding: 40rpx 30rpx;
}
.title {
  font-size: 40rpx;
  font-weight: bold;
  color: #2c785e;
  margin-bottom: 20rpx;
  border-left: 8rpx solid #2c785e;
  padding-left: 16rpx;
}

/* 简介 */
.intro .content {
  font-size: 30rpx;
  line-height: 50rpx;
  color: #555;
  margin-bottom: 20rpx;
  text-align: justify;
}

/* 景点卡片 */
.scenic-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 20rpx;
}
.item {
  width: 48%;
  background: #fff;
  border-radius: 12rpx;
  overflow: hidden;
  box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.1);
}
.item-img {
  width: 100%;
  height: 280rpx;
}
.item-name {
  font-size: 32rpx;
  font-weight: bold;
  padding: 16rpx 20rpx 6rpx;
  color: #2c785e;
}
.item-desc {
  font-size: 26rpx;
  color: #666;
  padding: 0 20rpx 20rpx;
  line-height: 40rpx;
}

/* 游玩信息 */
.info {
  background: #fff;
  margin: 0 30rpx 40rpx;
  border-radius: 16rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.08);
}
.info-item {
  font-size: 30rpx;
  line-height: 50rpx;
  margin-bottom: 10rpx;
}
.label {
  font-weight: bold;
  color: #2c785e;
}

/* 底部 */
.footer {
  background: #2c785e;
  color: #fff;
  text-align: center;
  padding: 30rpx;
  font-size: 26rpx;
}
</style>