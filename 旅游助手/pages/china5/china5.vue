<template>
  <!-- 西湖 静态页面 -->
  <view class="xihu-page">
    <!-- 顶部导航 -->
    <view class="header">
      <view class="logo">西湖</view>
    </view>

    <!-- 轮播大图 -->
    <view class="banner">
      <image
        src="https://ts2.tc.mm.bing.net/th/id/OIP-C.5xPJw6I5idadVo-rc8qN0wHaE8?rs=1&pid=ImgDetMain&o=7&rm=3"
        mode="widthFix"
        class="banner-img"
      ></image>
    </view>

    <!-- 简介 -->
    <view class="section intro">
      <view class="title">西湖简介</view>
      <view class="content">
        西湖位于浙江省杭州市，是中国唯一一处湖泊类世界文化遗产，自古有“人间天堂”的美誉。景区总面积约49平方公里，湖面被白堤、苏堤、杨公堤、孤山分隔为外西湖、西里湖、北里湖、小南湖、岳湖五片水面。
      </view>
      <view class="content">
        西湖以“二塔、三岛、三堤、五湖”为基本格局，拥有“西湖十景”等百余处景点。春有苏堤春晓，夏有曲院风荷，秋有三潭印月，冬有断桥残雪，四季皆景，文人墨客题咏无数，是自然与人文完美融合的典范。
      </view>
    </view>

    <!-- 西湖十景 -->
    <view class="section scenic">
      <view class="title">西湖十景</view>
      <view class="scenic-list">
        <view class="item" v-for="(item, index) in tenScenes" :key="index">
          <image :src="item.img" mode="aspectFill" class="item-img"></image>
          <view class="item-name">{{ item.name }}</view>
          <view class="item-desc">{{ item.desc }}</view>
        </view>
      </view>
    </view>

    <!-- 核心景点 -->
    <view class="section relic">
      <view class="title">核心景点</view>
      <view class="relic-list">
        <view class="relic-item">
          <image
            src="https://ts3.tc.mm.bing.net/th/id/OIP-C.yo4pEFdCl-Yl_h6Yv0j0qAHaE8?rs=1&pid=ImgDetMain&o=7&rm=3"
            class="relic-img"
          ></image>
          <view class="relic-info">
            <view class="relic-name">三潭印月</view>
            <view class="relic-desc">
              西湖最大岛屿，人民币一元纸币背面图案原型。皓月当空时，三座石塔映月水中，形成“天上月一轮，湖中影成三”的奇景。
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
        <text>浙江省杭州市西湖区龙井路1号</text>
      </view>
      <view class="info-item">
        <text class="label">门票：</text>
        <text>核心景区免费；雷峰塔40元，岳王庙25元</text>
      </view>
      <view class="info-item">
        <text class="label">开放时间：</text>
        <text>景区全天开放；雷峰塔8:00-19:00</text>
      </view>
      <view class="info-item">
        <text class="label">最佳季节：</text>
        <text>3-5月、9-11月，春秋气候宜人</text>
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
// 西湖十景数据
const tenScenes = [
  {
    name: '苏堤春晓',
    desc: '苏轼疏浚西湖所筑长堤，六桥相连，春日桃红柳绿，为西湖春景之冠。',
    img: 'https://ts2.tc.mm.bing.net/th/id/OIP-C.ryYrsF-XSShx2jc4Vdt4KQHaE6?rs=1&pid=ImgDetMain&o=7&rm=3'
  },
  {
    name: '断桥残雪',
    desc: '白堤起点，冬季雪后桥面若隐若现，远看似断非断，意境清幽。',
    img: 'https://ts2.tc.mm.bing.net/th/id/OIP-C.yD9Mlbzx8-0ittB6wcmT9gHaEg?rs=1&pid=ImgDetMain&o=7&rm=3'
  },
  {
    name: '三潭印月',
    desc: '湖中最大岛屿，三塔映月，“湖中有岛，岛中有湖”，夜景绝美。',
    img: 'https://ts1.tc.mm.bing.net/th/id/R-C.02294488b54b67038791e7a04cdb4cc6?rik=EyKVnb41E5hP7g&riu=http%3a%2f%2fn.sinaimg.cn%2ffront%2f601%2fw361h240%2f20190104%2fT2jc-hqzxptp4429943.jpg&ehk=KwAcX6OqXA5qFN49Fjb%2fjrMWBRMSbqWwvp1VxW55jeo%3d&risl=&pid=ImgRaw&r=0'
  },
  {
    name: '雷峰夕照',
    desc: '夕照山雷峰塔，黄昏时分夕阳染塔，金碧辉煌，湖山相映。',
    img: 'https://ts2.tc.mm.bing.net/th/id/OIP-C.uSpuNntYlcJ4rlxX4WGcXQHaE8?rs=1&pid=ImgDetMain&o=7&rm=3'
  },
  {
    name: '曲院风荷',
    desc: '夏日荷花连片，湖风送香，原南宋酿酒之地，荷香与酒香交融。',
    img: 'https://ts4.tc.mm.bing.net/th/id/OIP-C.IMA53V70ujffoNV7kIYzOAHaE9?rs=1&pid=ImgDetMain&o=7&rm=3'
  }
]
</script>

<style scoped>
/* 全局 */
.xihu-page {
  width: 100%;
  background: #f5f7fa;
  color: #333;
}

/* 顶部导航 */
.header {
  background-color: #2c5f2d;
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
  color: #2c5f2d;
  margin-bottom: 20rpx;
  border-left: 8rpx solid #2c5f2d;
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

/* 十景卡片 */
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
  color: #2c5f2d;
}
.item-desc {
  font-size: 26rpx;
  color: #666;
  padding: 0 20rpx 20rpx;
  line-height: 40rpx;
}

/* 核心景点 */
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
  color: #2c5f2d;
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
  color: #2c5f2d;
}

/* 底部 */
.footer {
  background: #2c5f2d;
  color: #fff;
  text-align: center;
  padding: 30rpx;
  font-size: 26rpx;
}
</style>