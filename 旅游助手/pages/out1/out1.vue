<template>
  <!-- 法国巴黎 静态页面 -->
  <view class="paris-page">
    <!-- 顶部导航 -->
    <view class="header">
      <view class="logo">法国巴黎</view>
    </view>

    <!-- 轮播大图 -->
    <view class="banner">
      <image
        src="https://ts1.tc.mm.bing.net/th/id/OIP-C.j6esrp6sAV7yNybWcxja0AHaJ4?rs=1&pid=ImgDetMain&o=7&rm=3"
        mode="widthFix"
        class="banner-img"
      ></image>
    </view>

    <!-- 巴黎简介 -->
    <view class="section intro">
      <view class="title">巴黎简介</view>
      <view class="content">
        巴黎是法国的首都和最大城市，位于法国北部巴黎盆地中央，塞纳河穿城而过，是世界著名的时尚、艺术、文化和旅游胜地，被誉为“光之城”“浪漫之都”。
        作为欧洲历史最悠久的城市之一，巴黎拥有2000多年历史，见证了无数历史变迁，也是全球重要的政治、经济、文化中心。
      </view>
      <view class="content">
        巴黎以其独特的建筑风貌、丰富的艺术遗产和浪漫的城市氛围闻名世界，埃菲尔铁塔、卢浮宫、巴黎圣母院等标志性建筑享誉全球，
        这里既有古典与现代的完美融合，也有浪漫与文艺的极致碰撞，是无数人心中的梦想旅行目的地。
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
        <text class="label">最佳季节：</text>
        <text>4-6月、9-10月，气候宜人，景色优美</text>
      </view>
      <view class="info-item">
        <text class="label">货币单位：</text>
        <text>欧元（EUR），1欧元≈7.8元人民币（参考）</text>
      </view>
      <view class="info-item">
        <text class="label">详细地址：</text>
        <text>法国巴黎市（核心景区集中在塞纳河两岸）</text>
      </view>
      <view class="info-item">
        <text class="label">交通方式：</text>
        <text>巴黎戴高乐机场、奥利机场可达，市内地铁、公交便捷</text>
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
    name: "埃菲尔铁塔",
    desc: "巴黎的象征，建于1889年，高324米，是世界著名钢铁建筑，登顶可俯瞰整个巴黎市区风光。",
    img: "https://ts1.tc.mm.bing.net/th/id/R-C.d2fd3e91c8bfc84119a27996d892ee69?rik=IjwbSdz9EMiC5g&riu=http%3a%2f%2fyouimg1.c-ctrip.com%2ftarget%2f1003080000003dz636F56.jpg&ehk=ub1h821FpdxQ22X4%2bOOPdxPhdFYGPpia2ol0EuX9Kfk%3d&risl=&pid=ImgRaw&r=0"
  },
  {
    name: "卢浮宫",
    desc: "世界四大博物馆之一，原法国王宫，收藏有《蒙娜丽莎》《维纳斯》等世界级艺术珍品。",
    img: "https://ts1.tc.mm.bing.net/th/id/R-C.d678df8aa7800ddb6d5920d8a448f270?rik=7CD5MZOJxuGITQ&riu=http%3a%2f%2fn.sinaimg.cn%2fsinacn%2fw1500h991%2f20180224%2f64b7-fyrwsqh7948784.jpg&ehk=LaoI%2fKV3cYr9qV7M1rCpiDs29JXCvEQEyQ1Ipt2XlOA%3d&risl=&pid=ImgRaw&r=0"
  },
  {
    name: "巴黎圣母院",
    desc: "哥特式建筑的典范，建于12世纪，拥有精致的雕刻和彩绘玻璃，是巴黎历史文化的重要象征。",
    img: "https://ts1.tc.mm.bing.net/th/id/R-C.a435a7a5d3950e0c075a01230c195f43?rik=u9SqZ5XzESKT9Q&riu=http%3a%2f%2fi7.qhimg.com%2ft01068da7902d22c4b6.jpg&ehk=tyRLSlsxrjTIXeA89sN2D77fKG83oIA2vORyEQHKMqU%3d&risl=&pid=ImgRaw&r=0"
  },
  {
    name: "塞纳河",
    desc: "巴黎的母亲河，两岸遍布著名建筑，乘坐游船可欣赏埃菲尔铁塔、卢浮宫等景点，感受巴黎浪漫气息。",
    img: "https://ts2.tc.mm.bing.net/th/id/OIP-C.VM7CPN3HbbkXnwcTZnYsuwHaE8?rs=1&pid=ImgDetMain&o=7&rm=3"
  }
];
</script>

<style scoped>
/* 全局页面样式 */
.paris-page {
  width: 100%;
  background: #f8f5f0;
  color: #333;
}

/* 顶部导航 */
.header {
  background-color: #3a5f8b;
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
  color: #3a5f8b;
  margin-bottom: 20rpx;
  border-left: 8rpx solid #3a5f8b;
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
  color: #3a5f8b;
}

/* 底部 */
.footer {
  background: #3a5f8b;
  color: #fff;
  text-align: center;
  padding: 30rpx;
  font-size: 26rpx;
}
</style>