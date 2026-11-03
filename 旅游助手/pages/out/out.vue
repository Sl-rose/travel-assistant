<template>
	<view class="container">
		<view class="header-box">
			<text class="page-title">探索全球之美</text>
		</view>
		<view class="attraction-list">
			<view class="column">
				<!-- 景点卡片 1 - 埃菲尔铁塔 -->
				<view class="card" @tap="toout1()">
					<view class="img-placeholder">
						<!-- 预留图片位置：建议尺寸 750x500 -->
						<image src="/static/国外/埃菲尔铁塔.jpg" mode="aspectFill"></image>
						<view class="location-tag">法国 · 巴黎</view>
					</view>
					<view class="info">
						<view class="name">埃菲尔铁塔</view>
						<view class="desc">巴黎地标，浪漫之都的象征</view>
					</view>
				</view>

				<!-- 景点卡片 2 - 京都清水寺 -->
				<view class="card">
					<view class="img-placeholder" style="height: 320rpx;">
						<!-- 预留图片位置：建议尺寸 750x580 -->
						<image src="/static/国外/清水寺.jpg" mode="aspectFill"></image>
						<view class="location-tag">日本 · 京都</view>
					</view>
					<view class="info">
						<view class="name">清水寺枫叶季</view>
						<view class="desc">千年古刹，秋日红叶绝景</view>
					</view>
				</view>

				<!-- 景点卡片 3 - 圣托里尼 -->
				<view class="card">
					<view class="img-placeholder" style="height: 360rpx;">
						<!-- 预留图片位置：建议尺寸 750x520 -->
						<image src="/static/国外/爱琴海.webp" mode="aspectFill"></image>
						<view class="location-tag">希腊 · 圣托里尼</view>
					</view>
					<view class="info">
						<view class="name">爱琴海蓝顶教堂</view>
						<view class="desc">蓝白相间的梦幻海岛</view>
					</view>
				</view>
			</view>

			<view class="column">
				<!-- 景点卡片 4 - 冰岛蓝湖 -->
				<view class="card">
					<view class="img-placeholder" style="height: 300rpx;">
						<!-- 预留图片位置：建议尺寸 750x450 -->
						<image src="/static/国外/蓝湖地热温泉.jpg" mode="aspectFill"></image>
						<view class="location-tag">冰岛</view>
					</view>
					<view class="info">
						<view class="name">蓝湖地热温泉</view>
						<view class="desc">冰与火之歌，世界最美温泉</view>
					</view>
				</view>

				<!-- 景点卡片 5 - 普吉岛 -->
				<view class="card">
					<view class="img-placeholder">
						<!-- 预留图片位置：建议尺寸 750x500 -->
						<image src="/static/国外/斯米兰.webp" mode="aspectFill"></image>
						<view class="location-tag">泰国 · 普吉岛</view>
					</view>
					<view class="info">
						<view class="name">斯米兰群岛潜水</view>
						<view class="desc">碧海蓝天，潜水胜地</view>
					</view>
				</view>

				<!-- 景点卡片 6 - 马尔代夫 -->
				<view class="card">
					<view class="img-placeholder" style="height: 340rpx;">
						<!-- 预留图片位置：建议尺寸 750x490 -->
						<image src="/static/国外/马尔代夫.jpg" mode="aspectFill"></image>
						<view class="location-tag">马尔代夫</view>
					</view>
					<view class="info">
						<view class="name">水上屋度假</view>
						<view class="desc">人间天堂，一岛一酒店</view>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script setup>
	const toout1 = () => {
		uni.navigateTo({
			url: '/pages/out1/out1'
		});
	};
</script>

<style lang="scss">
.container {
	background-color: #f7f8fa;
	min-height: 100vh;
	padding-bottom: 40rpx;
}

/* 顶部标题与搜索 */
.header-box {
	padding: 40rpx 30rpx;
	background-color: #fff;
	.page-title {
		font-size: 44rpx;
		font-weight: bold;
		color: #333;
		display: block;
		margin-bottom: 30rpx;
	}
	.search-bar {
		background-color: #f1f2f6;
		height: 80rpx;
		border-radius: 40rpx;
		display: flex;
		align-items: center;
		padding: 0 30rpx;
		.search-icon { margin-right: 15rpx; }
		.placeholder { color: #999; font-size: 28rpx; }
	}
}

/* 滚动标签 */
.category-tabs {
	white-space: nowrap;
	padding: 20rpx 0;
	background-color: #fff;
	.tab {
		display: inline-block;
		padding: 12rpx 35rpx;
		margin: 0 15rpx;
		font-size: 28rpx;
		color: #666;
		border-radius: 30rpx;
		&:first-child { margin-left: 30rpx; }
		&.active {
			background-color: #3cc51f;
			color: #fff;
			font-weight: bold;
		}
	}
}

/* 瀑布流列表 */
.attraction-list {
	display: flex;
	padding: 20rpx;
	justify-content: space-between;
	.column {
		width: 48.5%;
	}
}

.card {
	background-color: #fff;
	border-radius: 20rpx;
	overflow: hidden;
	margin-bottom: 20rpx;
	box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.05);
	
	.img-placeholder {
		width: 100%;
		height: 400rpx; /* 默认高度，可在行内样式修改实现瀑布流错落感 */
		background-color: #e1e1e1;
		position: relative;
		image { width: 100%; height: 100%; }
		
		.location-tag {
			position: absolute;
			left: 15rpx;
			bottom: 15rpx;
			background-color: rgba(0,0,0,0.5);
			color: #fff;
			font-size: 22rpx;
			padding: 4rpx 15rpx;
			border-radius: 8rpx;
		}
	}
	
	.info {
		padding: 20rpx;
		.name {
			font-size: 30rpx;
			font-weight: bold;
			color: #333;
			margin-bottom: 10rpx;
		}
		.rating {
			font-size: 24rpx;
			color: #ff9500;
			margin-bottom: 10rpx;
		}
		.desc {
			font-size: 24rpx;
			color: #666;
			margin-bottom: 15rpx;
			line-height: 1.4;
		}
		.price-box {
			color: #ff4d4f;
			.currency { font-size: 22rpx; font-weight: bold; }
			.price { font-size: 36rpx; font-weight: bold; }
			.unit { font-size: 22rpx; color: #999; margin-left: 4rpx; }
		}
	}
}
</style>