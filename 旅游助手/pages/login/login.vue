<template>
	<view class="login-container">
		<view class="login-header">
			<image class="logo" src="/static/local.png" mode="aspectFit"></image>
			<text class="app-name">边界旅行</text>
			<text class="slogan">无探索 不旅行</text>
		</view>

		<view class="login-form">
			<!-- 登录注册切换 -->
			<view class="tab-switch">
				<view :class="['tab-item', isLogin ? 'active' : '']" @tap="isLogin = true">登录</view>
				<view :class="['tab-item', !isLogin ? 'active' : '']" @tap="isLogin = false">注册</view>
			</view>

			<!-- 登录表单 -->
			<view v-if="isLogin" class="form-content">
				<view class="input-group">
					<text class="icon"></text>
					<input v-model="loginForm.username" placeholder="请输入手机号/用户名" placeholder-class="placeholder" />
				</view>
				<view class="input-group">
					<text class="icon"></text>
					<input v-model="loginForm.password" type="password" placeholder="请输入密码"
						placeholder-class="placeholder" />
				</view>
				<view class="forgot-pwd" @tap="showToast('请联系客服重置密码')">忘记密码？</view>
				<button class="submit-btn" @tap="handleLogin">登录</button>
			</view>

			<!-- 注册表单 -->
			<view v-else class="form-content">
				<view class="input-group">
					<text class="icon"></text>
					<input v-model="registerForm.username" placeholder="请输入手机号" placeholder-class="placeholder"
						maxlength="11" />
				</view>
				<view class="input-group">
					<text class="icon"></text>
					<input v-model="registerForm.password" type="password" placeholder="请设置密码(6-20位)"
						placeholder-class="placeholder" />
				</view>
				<view class="input-group">
					<text class="icon"></text>
					<input v-model="registerForm.confirmPassword" type="password" placeholder="请确认密码"
						placeholder-class="placeholder" />
				</view>
				<view class="input-group">
					<text class="icon"></text>
					<input v-model="registerForm.nickname" placeholder="请输入昵称(选填)" placeholder-class="placeholder" />
				</view>
				<button class="submit-btn" @tap="handleRegister">注册</button>
			</view>
		</view>
	</view>
</template>

<script>
	import {
		BASE_URL
	} from '../../common/config';

	export default {
		data() {
			return {
				isLogin: true, // true: 登录模式, false: 注册模式
				loginForm: {
					username: '',
					password: ''
				},
				registerForm: {
					username: '',
					password: '',
					confirmPassword: '',
					nickname: ''
				}
			};
		},
		methods: {
			showToast(message) {
				uni.showToast({
					title: message,
					icon: 'none'
				});
			},

			// 登录处理
			handleLogin() {
				if (!this.loginForm.username.trim()) {
					this.showToast('请输入用户名/手机号');
					return;
				}
				if (!this.loginForm.password) {
					this.showToast('请输入密码');
					return;
				}

				uni.showLoading({
					title: '登录中...'
				});

				uni.request({
					url: `${BASE_URL}/user/login/`,
					method: 'POST',
					header: {
						'Content-Type': 'application/x-www-form-urlencoded'
					},
					data: {
						username: this.loginForm.username,
						password: this.loginForm.password
					},
					success: (res) => {
						uni.hideLoading();
						if (res.data.status === 'success') {
							// 保存 token 和用户信息
							const token = res.data.token;
							const userInfo = res.data.user_info;

							uni.setStorageSync('token', token);
							uni.setStorageSync('userid', userInfo.userid);
							uni.setStorageSync('name', userInfo.name);
							uni.setStorageSync('phone', userInfo.phone);
							uni.setStorageSync('avatar', userInfo.avatar || '');

							this.showToast('登录成功');

							// 延迟跳转到首页（tabBar页面）
							setTimeout(() => {
								uni.reLaunch({
								    url: '/pages/index/index'
								});
							}, 1500);
						} else {
							this.showToast(res.data.message || '登录失败');
						}
					},
					fail: () => {
						uni.hideLoading();
						this.showToast('网络错误，请检查服务器连接');
					}
				});
			},

			// 注册处理
			handleRegister() {
				if (!this.registerForm.username.trim()) {
					this.showToast('请输入手机号');
					return;
				}

				// 验证手机号格式
				const phoneReg = /^1[3-9]\d{9}$/;
				if (!phoneReg.test(this.registerForm.username)) {
					this.showToast('请输入正确的手机号');
					return;
				}

				if (!this.registerForm.password || this.registerForm.password.length < 6) {
					this.showToast('密码长度不能少于6位');
					return;
				}

				if (this.registerForm.password !== this.registerForm.confirmPassword) {
					this.showToast('两次输入的密码不一致');
					return;
				}

				uni.showLoading({
					title: '注册中...'
				});

				uni.request({
					url: `${BASE_URL}/user/register/`,
					method: 'POST',
					header: {
						'Content-Type': 'application/x-www-form-urlencoded'
					},
					data: {
						username: this.registerForm.username,
						password: this.registerForm.password,
						nickname: this.registerForm.nickname || this.registerForm.username
					},
					success: (res) => {
						uni.hideLoading();
						if (res.data.status === 'success') {
							this.showToast('注册成功，请登录');
							// 切换到登录模式
							this.isLogin = true;
							// 清空注册表单
							this.registerForm = {
								username: '',
								password: '',
								confirmPassword: '',
								nickname: ''
							};
						} else {
							this.showToast(res.data.message || '注册失败');
						}
					},
					fail: () => {
						uni.hideLoading();
						this.showToast('网络错误，请检查服务器连接');
					}
				});
			}
		}
	};
</script>

<style lang="scss">
	.login-container {
		min-height: 100vh;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		padding: 0 60rpx;
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	.login-header {
		margin-top: 150rpx;
		text-align: center;
		margin-bottom: 80rpx;

		.logo {
			width: 160rpx;
			height: 160rpx;
			margin-bottom: 20rpx;
		}

		.app-name {
			display: block;
			font-size: 48rpx;
			font-weight: bold;
			color: #fff;
			margin-bottom: 15rpx;
		}

		.slogan {
			font-size: 28rpx;
			color: rgba(255, 255, 255, 0.9);
		}
	}

	.login-form {
		width: 100%;
		background: #fff;
		border-radius: 30rpx;
		padding: 50rpx 40rpx;
		box-shadow: 0 10rpx 40rpx rgba(0, 0, 0, 0.1);
	}

	.tab-switch {
		display: flex;
		justify-content: center;
		margin-bottom: 50rpx;
		border-bottom: 2rpx solid #f0f0f0;

		.tab-item {
			flex: 1;
			text-align: center;
			padding: 20rpx 0;
			font-size: 32rpx;
			color: #999;
			position: relative;

			&.active {
				color: #667eea;
				font-weight: bold;

				&::after {
					content: '';
					position: absolute;
					bottom: -2rpx;
					left: 50%;
					transform: translateX(-50%);
					width: 60rpx;
					height: 4rpx;
					background: #667eea;
					border-radius: 2rpx;
				}
			}
		}
	}

	.form-content {
		.input-group {
			display: flex;
			align-items: center;
			padding: 30rpx;
			background: #f8f9fb;
			border-radius: 15rpx;
			margin-bottom: 25rpx;

			.icon {
				font-size: 36rpx;
				margin-right: 20rpx;
			}

			input {
				flex: 1;
				font-size: 30rpx;
			}

			.placeholder {
				color: #bbb;
			}
		}

		.forgot-pwd {
			text-align: right;
			font-size: 26rpx;
			color: #667eea;
			margin-bottom: 30rpx;
		}

		.submit-btn {
			width: 100%;
			height: 90rpx;
			background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
			color: #fff;
			border: none;
			border-radius: 45rpx;
			font-size: 32rpx;
			font-weight: bold;
			margin-top: 20rpx;

			&::after {
				border: none;
			}

			&:active {
				opacity: 0.8;
			}
		}
	}

	.third-party {
		margin-top: 60rpx;

		.divider {
			display: flex;
			align-items: center;
			margin-bottom: 40rpx;

			.line {
				flex: 1;
				height: 1rpx;
				background: #e0e0e0;
			}

			text {
				padding: 0 20rpx;
				font-size: 26rpx;
				color: #999;
			}
		}

		
	}

	.agreement {
		margin-top: 40rpx;
		font-size: 24rpx;
		color: rgba(255, 255, 255, 0.8);
		text-align: center;
		line-height: 1.8;

		.link {
			color: #fff;
			text-decoration: underline;
		}
	}
</style>