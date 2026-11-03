<template>
  <!-- 秦兵马俑 静态页面 -->
  <view class="bingmayong-page">
    <!-- 顶部导航 -->
    <view class="header">
      <view class="logo">秦兵马俑</view>
    </view>

    <!-- 轮播大图 -->
    <view class="banner">
      <image
        src="https://ts1.tc.mm.bing.net/th/id/R-C.bda9d69b668b7f24cbc7d8609ea96a11?rik=o13IyeZO6w34NA&riu=http%3a%2f%2fseopic.699pic.com%2fphoto%2f50094%2f9350.jpg_wh1200.jpg&ehk=z45R7GhV0%2bjk5Cbt2zAj%2bhS7nxnNgzg9LAUg2TfJctg%3d&risl=&pid=ImgRaw&r=0"
        mode="widthFix"
        class="banner-img"
      ></image>
    </view>

    <!-- 简介 -->
    <view class="section intro">
      <view class="title">兵马俑简介</view>
      <view class="content">
        兵马俑位于陕西省西安市临潼区，是秦始皇陵的陪葬坑，1974年被当地农民打井时发现。它被誉为“世界第八大奇迹”、世界文化遗产，也是中国古代辉煌文明的金字名片。
      </view>
      <view class="content">
        整个坑群由一号、二号、三号坑组成，呈品字形排列，总面积约2万平方米，埋藏陶俑、陶马近8000件，战车百余辆。俑群千人千面、神态各异，平均身高约1.8米，真实还原了秦军军阵的威武气势。
      </view>
    </view>

    <!-- 核心坑馆 -->
    <view class="section scenic">
      <view class="title">核心坑馆</view>
      <view class="scenic-list">
        <view class="item" v-for="(item, index) in pitList" :key="index">
          <image :src="item.img" mode="aspectFill" class="item-img"></image>
          <view class="item-name">{{ item.name }}</view>
          <view class="item-desc">{{ item.desc }}</view>
        </view>
      </view>
    </view>

    <!-- 镇馆之宝 -->
    <view class="section relic">
      <view class="title">镇馆之宝</view>
      <view class="relic-list">
        <view class="relic-item">
          <image
            src="https://ts1.tc.mm.bing.net/th/id/R-C.4150086ba4a269b767daf20e4419ea0e?rik=Lwv%2f2g5KQsDcBQ&riu=http%3a%2f%2fimg.pconline.com.cn%2fimages%2fupload%2fupc%2ftx%2fitbbs%2f2102%2f18%2fc3%2f253873492_1613624060582.jpg&ehk=%2fRylJUlxMaG5uCSMWdhkX0rcKqxVGpRSyqNjE36nn%2f4%3d&risl=&pid=ImgRaw&r=0"
            class="relic-img"
          ></image>
          <view class="relic-info">
            <view class="relic-name">秦始皇陵铜车马</view>
            <view class="relic-desc">
              国宝级文物，出土两乘，由数千件青铜构件组成，工艺精湛，被誉为“青铜之冠”。
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 参观信息 -->
    <view class="section info">
      <view class="title">参观信息</view>
      <view class="info-item">
        <text class="label">地址：</text>
        <text>陕西省西安市临潼区秦陵北路1号</text>
      </view>
      <view class="info-item">
        <text class="label">门票：</text>
        <text>成人120元，学生半价，老人/儿童免票</text>
      </view>
      <view class="info-item">
        <text class="label">开放时间：</text>
        <text>旺季8:30-17:00；淡季8:30-16:30</text>
      </view>
      <view class="info-item">
        <text class="label">预约方式：</text>
        <text>官方公众号实名预约，现场不售票</text>
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
// 坑馆数据
const pitList = [
  {
    name: '一号坑 · 主力军阵',
    desc: '规模最大，东西长230米，由6000余陶俑组成前锋、主力、侧翼、后卫完整军阵。',
    img: 'https://tse1-mm.cn.bing.net/th/id/OIP-C.STgaLnq-P5A1-fL2NS4jPwHaE7?o=7rm=3&rs=1&pid=ImgDetMain&o=7&rm=3'
  },
  {
    name: '二号坑 · 精华军阵',
    desc: '骑兵、战车、步兵、弩兵多兵种混合，战术最复杂，被视为兵马俑的精华。',
    img: 'https://ts2.tc.mm.bing.net/th/id/OIP-C.jzexxEv3Eo-aRWi8Hc9rTQHaFj?rs=1&pid=ImgDetMain&o=7&rm=3'
  },
  {
    name: '三号坑 · 指挥中枢',
    desc: '最小但地位最高，呈“凹”字形，被认为是统帅一、二号坑的指挥部。',
    img: 'https://ts4.tc.mm.bing.net/th/id/OIP-C.Q3McKg66wbFyUM53cgkxTAHaFj?rs=1&pid=ImgDetMain&o=7&rm=3'
  }
]
</script>

<style scoped>
/* 全局 */
.bingmayong-page {
  width: 100%;
  background: #f5f3ef;
  color: #333;
}

/* 顶部导航 */
.header {
  background-color: #8c4b2a;
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
  color: #8c4b2a;
  margin-bottom: 20rpx;
  border-left: 8rpx solid #8c4b2a;
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

/* 坑馆卡片 */
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
  color: #8c4b2a;
}
.item-desc {
  font-size: 26rpx;
  color: #666;
  padding: 0 20rpx 20rpx;
  line-height: 40rpx;
}

/* 镇馆之宝 */
.relic-list {
  background: #fff;
  border-radius: 12rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.08);
}
.relic-item {
  display: flex;
  gap: 30rpx;
  align-items: center;
}
.relic-img {
  width: 200rpx;
  height: 200rpx;
  border-radius: 8rpx;
}
.relic-name {
  font-size: 32rpx;
  font-weight: bold;
  color: #8c4b2a;
  margin-bottom: 10rpx;
}
.relic-desc {
  font-size: 28rpx;
  color: #555;
  line-height: 44rpx;
}

/* 参观信息 */
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
  color: #8c4b2a;
}

/* 底部 */
.footer {
  background: #8c4b2a;
  color: #fff;
  text-align: center;
  padding: 30rpx;
  font-size: 26rpx;
}
</style>