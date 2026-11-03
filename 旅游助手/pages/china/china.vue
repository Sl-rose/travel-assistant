<template>
	<view class="container">
		<view class="header-box">
			<text class="page-title">发现中国之美</text>
		</view>
		<view class="attraction-list">
			<view class="column">
				<!-- 景点卡片 1 - 北京故宫 -->
				<view class="card" @tap="tochina1()">
					<view class="img-placeholder">
						<!-- 预留图片位置：建议尺寸 750x500 -->
						<image src="/static/国内/故宫博物馆.jpg" mode="aspectFill"></image>
						<view class="location-tag">北京</view>
					</view>
					<view class="info">
						<view class="name">故宫博物院</view>
						<view class="desc">明清两代皇家宫殿，世界文化遗产</view>
					</view>
				</view>

				<!-- 景点卡片 2 - 桂林山水 -->
				<view class="card" @tap="tochina2()">
					<view class="img-placeholder" style="height: 350rpx;">
						<!-- 预留图片位置：建议尺寸 750x600 -->
						<image src="/static/国内/漓江山水.jpg" mode="aspectFill"></image>
						<view class="location-tag">广西 · 桂林</view>
					</view>
					<view class="info">
						<view class="name">漓江山水</view>
						<view class="desc">桂林山水甲天下，阳朔山水甲桂林</view>
					</view>
				</view>

				<!-- 景点卡片 3 - 西安兵马俑 -->
				<view class="card" @tap="tochina3()">
					<view class="img-placeholder" style="height: 300rpx;">
						<!-- 预留图片位置：建议尺寸 750x450 -->
						<image src="/static/国内/兵马俑.jpg" mode="aspectFill"></image>
						<view class="location-tag">陕西 · 西安</view>
					</view>
					<view class="info">
						<view class="name">秦始皇兵马俑</view>
						<view class="desc">世界第八大奇迹，千年地下军团</view>
					</view>
				</view>
			</view>

			<view class="column">
				<!-- 景点卡片 4 - 张家界 -->
				<view class="card" @tap="tochina4()">
					<view class="img-placeholder" style="height: 380rpx;">
						<!-- 预留图片位置：建议尺寸 750x550 -->
						<image src="/static/国内/张家界森林公园.jpg" mode="aspectFill"></image>
						<view class="location-tag">湖南 · 张家界</view>
					</view>
					<view class="info">
						<view class="name">张家界国家森林公园</view>
						<view class="desc">阿凡达取景地，奇峰三千秀水八百</view>
					</view>
				</view>

				<!-- 景点卡片 5 - 杭州西湖 -->
				<view class="card" @tap="tochina5()">
					<view class="img-placeholder">
						<!-- 预留图片位置：建议尺寸 750x500 -->
						<image src="/static/国内/西湖.webp" mode="aspectFill"></image>
						<view class="location-tag">浙江 · 杭州</view>
					</view>
					<view class="info">
						<view class="name">西湖风景区</view>
						<view class="desc">欲把西湖比西子，淡妆浓抹总相宜</view>
					</view>
				</view>

				<!-- 景点卡片 6 - 九寨沟 -->
				<view class="card">
					<view class="img-placeholder" style="height: 320rpx;">
						<!-- 预留图片位置：建议尺寸 750x480 -->
						<image src="/static/国内/九寨沟.webp" mode="aspectFill"></image>
						<view class="location-tag">四川 · 九寨沟</view>
					</view>
					<view class="info">
						<view class="name">九寨沟风景区</view>
						<view class="desc">童话世界，人间仙境，彩林碧水</view>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script setup>
	// 跳转到china1页面
	const tochina1 = () => {
		uni.navigateTo({
			url: '/pages/china1/china1'
		});
	};
	
	// 跳转到china2页面
	const tochina2 = () => {
		uni.navigateTo({
			url: '/pages/china2/china2'
		});
	};
	
	const tochina3 = () => {
		uni.navigateTo({
			url: '/pages/china3/china3'
		});
	};
	
	const tochina4 = () => {
		uni.navigateTo({
			url: '/pages/china4/china4'
		});
	};
	
	const tochina5 = () => {
		uni.navigateTo({
			url: '/pages/china5/china5'
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
			background-color: #e74c3c;
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
	}
}
</style>
