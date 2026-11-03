<template>
  <!-- 故宫博物馆 静态页面 -->
  <view class="palace-page">
    <!-- 顶部导航 -->
    <view class="header">
      <view class="logo">故宫博物院</view>
    </view>

    <!-- 轮播大图 -->
    <view class="banner">
      <image
        src="https://ts4.tc.mm.bing.net/th/id/OIP-C.YDNoO-8r55ugUTVv-hZ5UwHaED?rs=1&pid=ImgDetMain&o=7&rm=3"
        mode="widthFix"
        class="banner-img"
      ></image>
    </view>

    <!-- 故宫简介 -->
    <view class="section intro">
      <view class="title">故宫简介</view>
      <view class="content">
        故宫博物院位于北京中轴线中心，是中国明清两代的皇家宫殿，旧称紫禁城。
        始建于1406年，是世界上现存规模最大、保存最为完整的木质结构古建筑之一。
        1987年被联合国教科文组织列为世界文化遗产，被誉为“紫禁城”。
      </view>
      <view class="content">
        故宫占地72万平方米，拥有宫殿9000余间，建筑气势恢宏、布局严谨，
        体现了中国古代皇家建筑的最高成就，也是中华文明无价的历史见证。
      </view>
    </view>

    <!-- 经典景点 -->
    <view class="section scenic">
      <view class="title">经典景点</view>
      <view class="scenic-list">
        <view class="item" v-for="(item, index) in scenicList" :key="index">
          <image :src="item.img" mode="aspectFill" class="item-img"></image>
          <view class="item-name">{{ item.name }}</view>
          <view class="item-desc">{{ item.desc }}</view>
        </view>
      </view>
    </view>

    <!-- 参观信息 -->
    <view class="section info">
      <view class="title">参观信息</view>
      <view class="info-item">
        <text class="label">开放时间：</text>
        <text>08:30–17:00（周一闭馆）</text>
      </view>
      <view class="info-item">
        <text class="label">门票价格：</text>
        <text>旺季60元，淡季40元</text>
      </view>
      <view class="info-item">
        <text class="label">详细地址：</text>
        <text>北京市东城区景山前街4号</text>
      </view>
      <view class="info-item">
        <text class="label">交通方式：</text>
        <text>地铁1号线「天安门东」「天安门西」站</text>
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
// 景点数据
const scenicList = [
  {
    name: "太和殿",
    desc: "故宫三大殿之首，俗称金銮殿，皇帝举行大典之地",
    img: "https://youimg1.c-ctrip.com/target/010081200009nq5joD41F.jpg"
  },
  {
    name: "中和殿",
    desc: "皇帝大典前休息、接受朝拜的场所，小巧精致",
    img: "https://ts4.tc.mm.bing.net/th/id/OIP-C.ZB_phmbsXxryt7ZvJfyFlgHaE6?rs=1&pid=ImgDetMain&o=7&rm=3"
  },
  {
    name: "御花园",
    desc: "皇宫后花园，古木参天，亭台楼阁，清幽雅致",
    img: "https://ts2.tc.mm.bing.net/th/id/OIP-C.xdJ50kSzR1HRXRKDVL2JoAHaE8?rs=1&pid=ImgDetMain&o=7&rm=3"
  },
  {
    name: "乾清宫",
    desc: "明清皇帝寝宫，内有“正大光明”匾额",
    img: "https://ts1.tc.mm.bing.net/th/id/OIP-C.0d5uzDM4S8Y5V8y1co7lbQHaFs?rs=1&pid=ImgDetMain&o=7&rm=3"
  }
];
</script>

<style scoped>
/* 全局页面样式 */
.palace-page {
  width: 100%;
  background: #f8f5f0;
  color: #333;
}

/* 顶部导航 */
.header {
  background-color: #8c2b2b;
  color: #fff;
  padding: 20rpx 30rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.logo {
  font-size: 36rpx;
  font-weight: bold;
  text-align: center;
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
  color: #8c2b2b;
  margin-bottom: 20rpx;
  border-left: 8rpx solid #8c2b2b;
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

/* 景点 */
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
}
.item-desc {
  font-size: 26rpx;
  color: #666;
  padding: 0 20rpx 20rpx;
  line-height: 40rpx;
}

/* 参观信息 */
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
  color: #8c2b2b;
}

/* 底部 */
.footer {
  background: #8c2b2b;
  color: #fff;
  text-align: center;
  padding: 30rpx;
  font-size: 26rpx;
}
</style>