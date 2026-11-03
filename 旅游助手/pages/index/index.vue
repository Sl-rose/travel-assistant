<template>
	<swiper class="myswiper" :indicator-dots="true" :autoplay="true" :interval="3000" :duration="1000">
		<swiper-item>
			<view class="swiper-item">
				<image src="https://ts3.tc.mm.bing.net/th/id/OIP-C.Zk_hq5qMMjZDJeFq2r0yEAHaED?rs=1&pid=ImgDetMain&o=7&rm=3" mode=""></image>
			</view>
		</swiper-item>
		
		
		<swiper-item>
			<view class="swiper-item">
				<image src="https://pic3.zhimg.com/v2-14de2621f3261ac6d97e201fc201d41b_r.jpg" mode=""></image>
			</view>
		</swiper-item>
		
		<swiper-item>
			<view class="swiper-item">
				<image src="https://n.sinaimg.cn/sinacn13/526/w855h471/20181201/16d3-hpevhcm6349986.png" mode=""></image>
			</view>
		</swiper-item>
		
		<swiper-item>
			<view class="swiper-item">
				<image src="https://ts1.tc.mm.bing.net/th/id/R-C.ef2dd6a2839403e559f9edb7eb0ab425?rik=9ts6t0qPAS6yAw&riu=http%3a%2f%2fimg.mp.itc.cn%2fupload%2f20160801%2fce087f839a214095a17c789489451f89_th.jpg&ehk=LvZkxXl1cQlwBB35NWTN4XK6CaFuZHvUrUlqsyfZj90%3d&risl=&pid=ImgRaw&r=0" mode=""></image>
			</view>
		</swiper-item>
	</swiper>
	<view class="container">
			<view class="banner-card" @tap="jumpToAssistant">
				<view class="banner-left">
					<image class="main-logo" src="/static/flower.png" mode="aspectFit"></image>
					<view class="banner-text">
						<view class="title">边界旅行</view>
					</view>
				</view>
				<view class="arrow-circle">></view>
			</view>
	
			<view class="menu-grid">
				<view class="menu-item" @tap="jumpToChina"><image src="/static/国内旅游 (1).png" mode="aspectFit"></image><text>国内旅行</text></view>
				<view class="menu-item" @tap="jumpToOut"><image src="/static/internal.png" mode="aspectFit"></image><text>国际旅行</text></view>
			</view>
	
			
		</view>
	
		<uni-fab ref="fab" :pattern="pattern" :content="content" :horizontal="horizontal" :vertical="vertical"
			:direction="direction" @trigger="trigger" />
	
</template>

<style>
	.myswiper{
		width: 750rpx;
		height: 550rpx;
		background-color: blue;
	}
	.myswiper image{
		width: 100%;
		height: 550rpx;
	}
	.container {
		padding: 30rpx;
		background-color: #ffffff;
	}
	
	/* Banner 样式 */
	.banner-card {
		background-color: #fcfcfc;
		border-radius: 40rpx;
		padding: 40rpx 30rpx;
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-bottom: 50rpx;
		box-shadow: 0 4rpx 20rpx rgba(0,0,0,0.03);
	}
	.banner-left {
		display: flex;
		align-items: center;
		.main-logo { width: 110rpx; height: 110rpx; margin-right: 20rpx; }
		.title { font-size: 36rpx; font-weight: 800; color: #1a1a1a; }
		.desc, .tags { font-size: 24rpx; color: #b2b2b2; margin-top: 4rpx; }
	}
	.arrow-circle {
		width: 54rpx; height: 54rpx; background-color: #f50057; 
		border-radius: 50%; color: #fff; text-align: center; line-height: 54rpx;
	}
	
	/* 宫格样式 */
	.menu-grid {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		.menu-item {
			width: 33.33%;
			display: flex;
			flex-direction: column;
			align-items: center;
			margin-bottom: 40rpx;
			image { width: 85rpx; height: 85rpx; margin-bottom: 10rpx; }
			text { font-size: 24rpx; color: #333; }
		}
	}
	
	/* 底部样式 */
	.footer-row {
		display: flex;
		justify-content: space-between;
		margin-top: 20rpx;
	}
	.entry-card {
		width: 335rpx;
		background-color: #f8f9fb;
		border-radius: 30rpx;
		padding: 30rpx 20rpx;
		display: flex;
		align-items: center;
	}
	.icon-box {
		width: 80rpx; height: 80rpx; border-radius: 50%;
		display: flex; align-items: center; justify-content: center;
	}
	.red-light { background-color: #ffeded; .red-dot { width: 30rpx; height: 30rpx; background: #ff4d4f; border-radius: 50%; } }
	.cyan-bg { background-color: #26d4da; border-radius: 18rpx; .num-8 { color: #fff; font-weight: bold; } }
	
	.entry-text {
		margin-left: 15rpx;
		.t1 { font-size: 32rpx; font-weight: bold; color: #000; }
		.t2 { font-size: 24rpx; color: #999; }
	}
</style>

<script>
	export default {
		data() {
			return {
				title: 'uni-fab',
				directionStr: '垂直',
				horizontal: 'right',
				vertical: 'bottom',
				direction: 'vertical',
				pattern: {
					color: '#7A7E83',
					backgroundColor: '#fff',
					selectedColor: '#007AFF',
					buttonColor: '#007AFF',
					iconColor: '#fff'
				},
				is_color_type: false,
				content: [{
						iconPath: '/static/ai (2).png',
						selectedIconPath: '/static/ai (1).png',
						text: 'ai助手',
						active: true
					},
				
					
				]
			}
		},
		onBackPress() {
			if (this.$refs.fab.isShow) {
				this.$refs.fab.close()
				return true
			}
			return false
		},
		methods: {
			jumpToAssistant() {
				uni.navigateTo({
					url: '/pages/assistant/assistant'
				});
			},
			
			jumpToChina() {
				uni.switchTab({
					url: '/pages/china/china'
				});
			},
			
			jumpToOut() {
				uni.switchTab({
					url: '/pages/out/out'
				});
			},
			
			trigger(e) {
				console.log(e)
				this.content[e.index].active = !e.item.active
				if(e.index ==0){
					uni.navigateTo({
						url:"/pages/assistant/assistant"
					})
				}
			},
			
			
			
		}
	}
</script>



