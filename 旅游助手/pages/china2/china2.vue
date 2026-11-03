<template>
  <!-- 漓江山水 静态页面 -->
  <view class="lijiang-page">
    <!-- 顶部导航 -->
    <view class="header">
      <view class="logo">漓江山水</view>
    </view>

    <!-- 轮播大图（漓江核心美景） -->
    <view class="banner">
      <image
        src="https://ts4.tc.mm.bing.net/th/id/OIP-C.XcIPDqsKoKQsobYSYOmz_AHaEJ?rs=1&pid=ImgDetMain&o=7&rm=3"
        mode="widthFix"
        class="banner-img"
      ></image>
    </view>

    <!-- 漓江简介 -->
    <view class="section intro">
      <view class="title">漓江简介</view>
      <view class="content">
        漓江位于广西壮族自治区桂林市，是珠江水系西江支流桂江的上游河段，全长164公里，流经桂林、阳朔等地。
        漓江以“山青、水秀、洞奇、石美”四绝闻名于世，是世界上规模最大、风景最美的岩溶山水游览区之一，
        被誉为“百里画廊”，也是国家5A级旅游景区。
      </view>
      <view class="content">
        漓江的山水相依相伴，两岸奇峰罗列、翠竹依依，江水清澈见底，倒映着青山绿树，行舟江上，如入画中。
        春有烟雨朦胧，夏有浓荫蔽日，秋有金桂飘香，冬有清秀淡雅，四季皆有不同韵味，是文人墨客笔下的灵感源泉。
      </view>
    </view>

   <!-- 核心美景 -->
    <view class="section scenic">
      <view class="title">核心美景</view>
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
        <text class="label">最佳游览时间：</text>
        <text>4-10月（雨水充足，山水更灵动）</text>
      </view>
      <view class="info-item">
        <text class="label">游览方式：</text>
        <text>游船（桂林至阳朔段）、竹筏、徒步</text>
      </view>
      <view class="info-item">
        <text class="label">门票/船票：</text>
        <text>游船210-300元，竹筏80-120元/人</text>
      </view>
      <view class="info-item">
        <text class="label">交通指南：</text>
        <text>桂林站/桂林北站转乘公交、旅游专线至漓江码头</text>
      </view>
      <view class="info-item">
        <text class="label">温馨提示：</text>
        <text>雨天游览需携带雨具，竹筏游览需遵守安全规定</text>
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
// 漓江核心美景数据
const scenicList = [
  {
    name: "九马画山",
    desc: "漓江标志性景点，山峰峭壁上有九匹“骏马”图案，栩栩如生，需仔细辨认",
    img: "https://ts4.tc.mm.bing.net/th/id/OIP-C.pPLCalnVgPvIdnzym6s7wgHaDt?rs=1&pid=ImgDetMain&o=7&rm=3"
  },
  {
    name: "黄布倒影",
    desc: "漓江精华段，江水清澈如镜，山峰倒映水中，与江面黄布滩相映成趣，是20元人民币背景图案取景地",
    img: "https://youimg1.c-ctrip.com/target/1006160000010ctsv097A.jpg"
  },
  {
    name: "阳朔西街",
    desc: "紧邻漓江，青石板路蜿蜒，融合了古朴与现代气息，美食、特色小店林立，是游览漓江后的必去之地",
    img: "https://ts1.tc.mm.bing.net/th/id/R-C.f11747e56a89f6024f58de1fe6c19531?rik=yY6ED9T16rnAaQ&riu=http%3a%2f%2fimg.daoyounet.com%2fFileUpload%2fgong-lue-wen-zhang-tu-pian%2fqi-ta%2fXiJie.png&ehk=5UR98TJovENO9kcygXrkEfBN8%2bgAEzq%2brcsn8I78DGI%3d&risl=&pid=ImgRaw&r=0"
  },
  {
    name: "兴坪古镇",
    desc: "漓江畔千年古镇，依山傍水，保留着古朴的街巷和建筑，是漓江游船的终点，风景清幽静谧",
    img: "https://img95.699pic.com/photo/60057/3401.jpg_wh860.jpg"
  }
];
</script>

<style scoped>
/* 全局页面样式 */
.lijiang-page {
  width: 100%;
  background: #f0f8fb;
  color: #333;
}

/* 顶部导航 */
.header {
  background-color: #2a8c68;
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

/* 轮播图 */
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
  color: #2a8c68;
  margin-bottom: 20rpx;
  border-left: 8rpx solid #2a8c68;
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

/* 美景卡片 */
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
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}
.item-img {
  width: 100%;
  height: 280rpx;
}
.item-name {
  font-size: 32rpx;
  font-weight: bold;
  padding: 16rpx 20rpx 6rpx;
  color: #2a8c68;
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
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.08);
}
.info-item {
  font-size: 30rpx;
  line-height: 50rpx;
  margin-bottom: 10rpx;
}
.label {
  font-weight: bold;
  color: #2a8c68;
}

/* 底部 */
.footer {
  background: #2a8c68;
  color: #fff;
  text-align: center;
  padding: 30rpx;
  font-size: 26rpx;
}
</style>