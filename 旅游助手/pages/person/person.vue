<template>
	<view class="container">
		<view class="user-header">
			<view class="user-info">
				<view class="left-part">
					<view class="avatar-wrapper" @tap="changeAvatar" @longpress="previewAvatar">
						<image class="avatar" :src="isLogin ? (userInfo.avatar || '/static/用户 (1).png') : '/static/用户.png'" mode="aspectFill">
						</image>
						<view class="avatar-tip" v-if="isLogin">+</view>
					</view>
					<view class="user-detail" v-if="isLogin">
						<text class="nickname">{{ userInfo.name || '用户' }}</text>
						<text class="phone">{{ userInfo.phone || '未绑定手机' }}</text>
					</view>
				</view>
				<view v-if="!isLogin" class="login-btn" @tap="goToLogin">登录 / 注册</view>
				<view v-else class="logout-btn" @tap="handleLogout">退出</view>
			</view>
		</view>

		

		<view class="footer-info">
			<view class="phone-row">
				<text>联系我 17823193077</text>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				isLogin: false,
				userInfo: {
					name: '',
					phone: '',
					avatar: ''
				},
				BASE_URL: 'http://127.0.0.1:8081'
			};
		},
		onShow() {
			// 每次显示页面时检查登录状态
			this.checkLoginStatus();
		},
		methods: {
			checkLoginStatus() {
				const userid = uni.getStorageSync('userid');
				const name = uni.getStorageSync('name');
				const phone = uni.getStorageSync('phone');
				let avatar = uni.getStorageSync('avatar');
							
				if (userid) {
					this.isLogin = true;
							
					// 如果是相对路径，转换为完整URL
					if (avatar && !avatar.startsWith('http')) {
						avatar = this.BASE_URL + avatar;
					}
							
					this.userInfo = {
						name: name || '用户',
						phone: phone || '未绑定手机',
						avatar: avatar || ''
					};
							
					console.log('用户信息加载:', this.userInfo);
				} else {
					this.isLogin = false;
					this.userInfo = {
						name: '',
						phone: '',
						avatar: ''
					};
				}
			},

			goToLogin() {
				uni.navigateTo({
					url: '/pages/login/login'
				});
			},

			handleLogout() {
				uni.showModal({
					title: '提示',
					content: '确定要退出登录吗？',
					success: (res) => {
						if (res.confirm) {
							// 清除本地存储
							uni.removeStorageSync('userid');
							uni.removeStorageSync('name');
							uni.removeStorageSync('phone');
							uni.removeStorageSync('avatar');
					
							this.isLogin = false;
							this.userInfo = {
								name: '',
								phone: '',
								avatar: ''
							};
					
							uni.showToast({
								title: '已退出登录',
								icon: 'success'
							});
						}
					}
				});
			},
					
			// 预览头像
			previewAvatar() {
				if (!this.isLogin) return;
				const avatarUrl = this.userInfo.avatar;
				if (!avatarUrl) {
					uni.showToast({
						title: '暂无头像',
						icon: 'none'
					});
					return;
				}
						
				// 如枟是相对路径，拼接完整URL
				const fullUrl = avatarUrl.startsWith('http') ? avatarUrl : this.BASE_URL + avatarUrl;
						
				uni.previewImage({
					urls: [fullUrl],
					current: fullUrl
				});
			},
					
			// 修改头像
			changeAvatar() {
				console.log('changeAvatar called, isLogin:', this.isLogin);
						
				if (!this.isLogin) {
					uni.showToast({
						title: '请先登录',
						icon: 'none'
					});
					return;
				}
						
				// #ifdef H5
				//console.log('H5环境，动态创建input元素');
				// H5环境动态创建input元素
				const input = document.createElement('input');
				input.type = 'file';
				input.accept = 'image/*';
				input.style.display = 'none';
						
				input.onchange = (e) => {
					this.handleFileChange(e);
					document.body.removeChild(input);
				};
						
				document.body.appendChild(input);
				input.click();
				//console.log('文件选择器已触发');
				// #endif
						
				// #ifndef H5
				// 小程序/App环境使用uni.chooseImage
				const _this = this;
				uni.chooseImage({
					count: 1,
					sizeType: ['compressed'],
					sourceType: ['album', 'camera'],
					success: (res) => {
						const tempFilePath = res.tempFilePaths[0];
						_this.uploadAvatarFile(tempFilePath);
					}
				});
				// #endif
			},
					
			// H5文件选择处理
			handleFileChange(e) {
				const file = e.target.files[0];
				if (!file) return;
						
				// 验证文件类型
				if (!file.type.startsWith('image/')) {
					uni.showToast({
						title: '请选择图片文件',
						icon: 'none'
					});
					return;
				}
						
				uni.showLoading({
					title: '上传中...'
				});
						
				// 使用FormData上传
				const formData = new FormData();
				formData.append('file1', file);
						
				const token = uni.getStorageSync('token');
						
				fetch(this.BASE_URL + '/user/upload_avatar/', {
					method: 'POST',
					headers: {
						'Authorization': `Bearer ${token}`
					},
					body: formData
				})
				.then(res => res.json())
				.then(data => {
					uni.hideLoading();
					console.log('上传响应:', data);
					if (data.status === 'success') {
						// 上传成功，直接显示头像
						const avatarUrl = data.file_url;
						const fullUrl = avatarUrl.startsWith('http') ? avatarUrl : this.BASE_URL + avatarUrl;
									
						this.userInfo.avatar = fullUrl;
						uni.setStorageSync('avatar', fullUrl);
									
						uni.showToast({
							title: '头像上传成功',
							icon: 'success'
						});
					} else {
						uni.showToast({
							title: data.message || '上传失败',
							icon: 'none'
						});
					}
				})
				.catch(err => {
					uni.hideLoading();
					console.error('上传失败:', err);
					uni.showToast({
						title: '请检查服务器是否启动',
						icon: 'none',
						duration: 2000
					});
				});
						
				// 清空input，允许重复选择同一文件
				e.target.value = '';
			},
					
			// 上传头像文件
			uploadAvatarFile(filePath) {
				const _this = this;
						
				uni.showLoading({
					title: '上传中...'
				});
						
				uni.uploadFile({
					url: _this.BASE_URL + '/user/upload_avatar/',
					filePath: filePath,
					name: 'file1',
					header: _this.getAuthHeader(),
					success: (uploadRes) => {
						try {
							const data = JSON.parse(uploadRes.data);
							if (data.status === 'success') {
								// 上传成功，直接显示头像
								const avatarUrl = data.file_url;
								const fullUrl = avatarUrl.startsWith('http') ? avatarUrl : _this.BASE_URL + avatarUrl;
											
								_this.userInfo.avatar = fullUrl;
								uni.setStorageSync('avatar', fullUrl);
								uni.hideLoading();
											
								uni.showToast({
									title: '头像上传成功',
									icon: 'success'
								});
							} else {
								uni.hideLoading();
								uni.showToast({
									title: data.message || '上传失败',
									icon: 'none'
								});
							}
						} catch (e) {
							uni.hideLoading();
							console.error('解析响应失败:', e);
							uni.showToast({
								title: '上传失败',
								icon: 'none'
							});
						}
					},
					fail: (err) => {
						uni.hideLoading();
						console.error('上传失败:', err);
						uni.showToast({
							title: '请检查服务器是否启动',
							icon: 'none',
							duration: 2000
						});
					}
				});
			},
					
			// 更新头像到数据库
			updateAvatar(avatarUrl) {
				const _this = this;
				const userid = uni.getStorageSync('userid');
				const token = uni.getStorageSync('token');
						
				console.log('准备更新头像，URL:', avatarUrl);
								
				uni.request({
					url: this.BASE_URL + '/user/update_profile/',
					method: 'POST',
					header: {
						'Content-Type': 'application/json',
						'Authorization': `Bearer ${token}`
					},
					data: {
						userid: userid,
						avatar: avatarUrl
					},
					success: (res) => {
						console.log('更新头像响应:', res.data);
						if (res.data.status === 'success') {
							// 如果是相对路径，转换为完整URL
							const fullUrl = avatarUrl.startsWith('http') ? avatarUrl : this.BASE_URL + avatarUrl;
									
							// 更新本地存储
							_this.userInfo.avatar = fullUrl;
							uni.setStorageSync('avatar', fullUrl);
											
							console.log('头像已更新:', fullUrl);
									
							uni.showToast({
								title: '头像更新成功',
								icon: 'success'
							});
						} else {
							uni.showToast({
								title: '更新失败',
								icon: 'none'
							});
						}
					},
					fail: (err) => {
						console.error('更新头像失败:', err);
						uni.showToast({
							title: '更新失败',
							icon: 'none'
						});
					}
				});
			},
					
			// 获取认证头
			getAuthHeader() {
				const token = uni.getStorageSync('token');
				if (!token) return {};
				return {
					'Authorization': `Bearer ${token}`
				};
			}
		}
	};
</script>

<style lang="scss">
	.container {
		background-color: #f8f9fb;
		min-height: 100vh;
	}

	/* 头部背景及用户信息 */
	.user-header {
		background: linear-gradient(to bottom, #666666, #999999);
		padding: 100rpx 40rpx 60rpx;
		color: #fff;

		.user-info {
			display: flex;
			justify-content: space-between;
			align-items: center;
			margin-bottom: 60rpx;

			.left-part {
				display: flex;
				align-items: center;
				flex: 1;

				.avatar-wrapper {
					position: relative;
					margin-right: 20rpx;
					
					.avatar {
						width: 120rpx;
						height: 120rpx;
						border-radius: 50%;
						border: 4rpx solid rgba(255, 255, 255, 0.3);
					}
					
					.avatar-tip {
						position: absolute;
						right: 0;
						bottom: 0;
						width: 40rpx;
						height: 40rpx;
						background: rgba(255, 255, 255, 0.9);
						color: #666;
						border-radius: 50%;
						display: flex;
						align-items: center;
						justify-content: center;
						font-size: 28rpx;
						font-weight: bold;
						box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.2);
					}
				}

				.user-detail {
					display: flex;
					flex-direction: column;
					flex: 1;

					.nickname {
						font-size: 36rpx;
						font-weight: bold;
						color: #fff;
						margin-bottom: 8rpx;
					}

					.phone {
						font-size: 26rpx;
						color: rgba(255, 255, 255, 0.8);
					}
				}
			}

			.login-btn {
				background: #e6a23c;
				padding: 15rpx 40rpx;
				border-radius: 40rpx;
				font-size: 28rpx;
			}

			.logout-btn {
				background: rgba(255, 255, 255, 0.3);
				padding: 15rpx 40rpx;
				border-radius: 40rpx;
				font-size: 28rpx;
				border: 2rpx solid rgba(255, 255, 255, 0.5);
			}
		}

		
	}


	.menu-grid {
		display: flex;
		flex-wrap: wrap;

		.menu-item {
			width: 25%;
			display: flex;
			flex-direction: column;
			align-items: center;
			margin-bottom: 40rpx;

			image {
				width: 70rpx;
				height: 70rpx;
				margin-bottom: 15rpx;
			}

			text {
				font-size: 26rpx;
				color: #333;
			}
		}
	}

	/* 针对第二个卡片（常用服务）的间距微调 */
	.service-grid {
		.menu-item {
			margin-bottom: 50rpx;
		}

		.menu-item:nth-last-child(-n+3) {
			margin-bottom: 0;
		}
	}

	/* 底部联系信息 */
	.footer-info {
		margin-top: 40rpx;
		padding-bottom: 60rpx;
		text-align: center;
		color: #999;
		font-size: 24rpx;

		.phone-row {
			margin-bottom: 10rpx;
			font-size: 28rpx;
			color: #b2b2b2;
		}

		.time-text {
			margin-bottom: 8rpx;
		}

		.feedback {
			margin-top: 30rpx;

			.link {
				color: #409eff;
				margin-left: 10rpx;
			}
		}
	}
</style>