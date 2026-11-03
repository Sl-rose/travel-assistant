<template>
	<view class="page-container">
		<view v-if="showHistory" class="sidebar-mask" @tap="showHistory = false">
			<view class="sidebar-body" @tap.stop>
				<view class="sidebar-header">历史记录</view>
				<scroll-view scroll-y="true" class="history-list">
					<view v-for="topic in historylist" class="history-item" @tap="getDetail(topic.topicid)"
						@longpress="delTopic(topic.topicid)">{{topic.title}}</view>
					<view v-if="historylist.length === 0" class="no-history">暂无记录</view>
				</scroll-view>
			</view>
		</view>

		<view class="main-content">
			<view class="header">
				<view class="nav-btn" @tap="openHistory">
					<image src="/static/更多.png" class="nav-icon"></image>
					<text>记录</text>
				</view>
				<view class="title">AITravel</view>
				<view class="nav-btn" @tap="resetChat">
					<image src="/static/新建对话.png" class="nav-icon"></image>
					<text>新建</text>
				</view>
			</view>

			<scroll-view class="chat-area" scroll-y :scroll-into-view="lastId">
				<view v-if="chatlist.length === 0" class="welcome">
					<image class="logo" src="/static/local.png" mode="aspectFit"></image>
					<view class="brand-name">边界旅行</view>
					<view class="slogan">无探索 不旅行</view>
					<view class="welcome-msg">嗨！我是你的旅游助手</view>
				</view>

				<view class="message-list">
				    <view v-for="(item, index) in chatlist" :key="index"
				        :class="['msg-box', item.role === 'user' ? 'user' : 'ai']">
				        <image class="avatar" :src="item.role === 'user' ? '/static/china.png' : '/static/ai (1).png'"></image>
				        <view class="bubble">
				            <block v-if="item.role === 'user'">
				                <image v-if="item.image" :src="item.image" mode="widthFix" class="content-img"></image>
				                <text>{{ item.content }}</text>
				            </block>
				            <zero-markdown-view v-else :markdown="item.content" :aiMode="false"></zero-markdown-view>
				        </view>
				    </view>
				
				    <view v-if="streamcontent" class="msg-box ai streaming">
				        <image class="avatar" src="/static/ai (1).png"></image>
				        <view class="bubble">
				            <zero-markdown-view :markdown="streamcontent" :aiMode="true" key="streaming-box"></zero-markdown-view>
				        </view>
				    </view>
				
				    <view id="bottom-anchor" style="height: 40rpx; width: 100%; clear: both;"></view>
				</view>
			</scroll-view>

			<view class="input-panel">
				<view v-if="temp_image" class="img-preview">
					<image :src="temp_image" mode="aspectFill"></image>
					<text class="del-img" @tap="temp_image='';file_url=''">×</text>
				</view>

				<view class="input-box">
					<textarea v-model="query" placeholder="给 AITravel 发送消息" auto-height :fixed="true" />
				</view>

				<view class="toolbar">
					<view class="tool-left">
						<view :class="['btn-mini', deepthink == 1 ? 'active' : '']"
							@tap="deepthink = (deepthink == 1 ? 0 : 1)">
							<image src="/static/深度思考.png" class="mini-icon"></image>
							<text>深度思考</text>
						</view>
						<view :class="['btn-mini', web == 1 ? 'active' : '']" @tap="web = (web == 1 ? 0 : 1)">
							<image src="/static/联网搜索.png" class="mini-icon"></image>
							<text>联网搜索</text>
						</view>
					</view>
					<view class="tool-right">
						<text class="plus-icon" @tap="uploadFile">+</text>
						<view class="send-btn" @tap="sendMsg">↑</view>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>


<script>
	import {
		BASE_URL
	} from '../../common/config';
	import {
		fetchSSE
	} from '../../common/tools.js'

	export default {
		data() {
			return {
				
				query: "",
				chatlist: [],
				historylist: [],
				showHistory: false,
				web: 0,
				deepthink: 0,
				temp_image: "",
				file_url: "",
				lastId: "",
				topicid: 0,
				streamcontent: "",
				isScrolling: false,
				BASE_URL:BASE_URL,
			}
		},
		methods: {
			parseTokenPayload(token) {
				if (!token || token.split('.').length !== 3) return null;
				try {
					const base64 = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/');
					const payload = JSON.parse(decodeURIComponent(escape(atob(base64))));
					return payload;
				} catch (e) {
					console.log('token解析失败', e);
					return null;
				}
			},
			clearLoginStorage() {
				uni.removeStorageSync('token');
				uni.removeStorageSync('userid');
				uni.removeStorageSync('name');
				uni.removeStorageSync('phone');
				uni.removeStorageSync('avatar');
			},
			ensureLogin(redirect = true) {
				const token = this.getToken();
				const payload = this.parseTokenPayload(token);
				const now = Math.floor(Date.now() / 1000);
				const isValid = !!(payload && payload.userid && payload.exp && payload.exp > now);
				if (isValid) return true;
				this.clearLoginStorage();
				uni.showToast({
					title: '请先登录',
					icon: 'none'
				});
				if (redirect) {
					setTimeout(() => {
						uni.reLaunch({
							url: '/pages/login/login'
						});
					}, 300);
				}
				return false;
			},
			getToken() {
				return uni.getStorageSync('token') || '';
			},
			getAuthHeader() {
				const token = this.getToken();
				if (!token) return {};
				return {
					Authorization: `Bearer ${token}`
				};
			},
			getUserIdFromToken() {
				const token = this.getToken();
				if (!token) return '';
				const payload = this.parseTokenPayload(token);
				return (payload && payload.userid) || '';
			},
			delTopic(topicid) {
				const _this = this
				const userid = this.getUserIdFromToken()
				uni.showModal({
					title: '请确认',
					content: '删除的信息不可恢复',
					success: function(res) {
						if (res.confirm) {
							uni.request({
								url: BASE_URL + '/api/deltopic/',
								method: 'GET',
								header: _this.getAuthHeader(),
								data: {
									topicid: topicid,
									userid: userid
								},
								success: (res) => {
									_this.openHistory()
								},
							});
						}
					}
				});
			},
			openHistory() {
				if (!this.ensureLogin()) return;
				const token = this.getToken()
				const userid = this.getUserIdFromToken()
				console.log('history token exists:', !!token)
				uni.request({
					url: BASE_URL + '/api/history/',
					method: 'GET',
					//带token的头消息
					header: this.getAuthHeader(),
					data: {
						userid: userid
					},
					success: (res) => {
						this.historylist = res.data.historylist
						this.showHistory = true;
					}
				});
			},
			getDetail(topicid) {
				if (!this.ensureLogin()) return;
				const userid = this.getUserIdFromToken()
				this.topicid = topicid
				uni.request({
					url: BASE_URL + '/api/detail/',
					method: 'GET',
					header: this.getAuthHeader(),
					data: {
						topicid: topicid,
						userid: userid
					},
					success: (res) => {
						this.chatlist = res.data.chat;
						this.showHistory = false;
					},
				});
			},
			resetChat() {
				uni.showModal({
					title: '提示',
					content: '确定要重置当前页面吗？',
					success: (res) => {
						if (res.confirm) {
							this.chatlist = [];
							this.query = "";
							this.temp_image = "";
							this.file_url = "";
							this.topicid = 0;
						}
					}
				});
			},
			uploadFile() {
				if (!this.ensureLogin()) return;
				uni.chooseImage({
					count: 1,
					sizeType: ['compressed'],
					success: (res) => {
						this.temp_image = res.tempFilePaths[0];
						uni.uploadFile({
							url: BASE_URL + '/api/upload/',
							filePath: this.temp_image,
							name: 'file1',
							header: this.getAuthHeader(),
							success: (uploadRes) => {
								const data = JSON.parse(uploadRes.data);
								this.file_url = data.file_url;
							}
						});
					}
				});
			},
			sendMsg() {
				if (!this.ensureLogin()) return;
				if (!this.query.trim() && !this.file_url) return;
				const userid = this.getUserIdFromToken()

				this.chatlist.push({
					role: 'user',
					content: this.query,
					image: this.temp_image
				});

				let oldQuery = this.query;
				let sendFileUrl = this.file_url;

				this.query = "";
				this.temp_image = "";
				this.file_url = "";
				this.scrollToBottom();

				fetchSSE(BASE_URL + '/api/ai/', {
					headers: this.getAuthHeader(),
					body: {
						query: oldQuery,
						topicid: this.topicid,
						file_url: sendFileUrl,
						userid: userid,
						web: this.web,
						deepthink: this.deepthink
					}
				}, (msg) => {
					console.log("收到:", msg);

					if (msg === "[@#---DONE---#@]") {
						this.chatlist.push({
							role: 'assistant',
							content: this.streamcontent
						});
						this.streamcontent = '';
						this.scrollToBottom();
						return;
					}

					if (msg.includes("<topic_id_IGCV>")) {
						this.topicid = msg.match(/<topic_id_IGCV>(\d+)<\/topic_id_IGCV>/)[1];
						return;
					}

					this.streamcontent += msg;
					this.scrollToBottom();
				});
			},
			scrollToBottom() {
			        if (this.isScrolling) return; // 如果正在执行滚动，直接跳过本次
			        
			        this.isScrolling = true;
			        this.$nextTick(() => {
			            this.lastId = 'bottom-anchor';
			            // 增加一点点延迟，给 Markdown 渲染留出高度计算时间
			            setTimeout(() => {
			                this.lastId = "";
			                this.isScrolling = false;
			            }, 100); // 100ms 左右的频率足以保证视觉流畅且不跳动
			        });
			    }
			},
		onLoad() {
			if (!this.ensureLogin()) return;
			// #ifdef H5
			document.addEventListener('contextmenu', function(e) {
				e.preventDefault()
			})
			// #endif
		}
	}
</script>

<style lang="scss">
	
	/* 布局保持不变 */
	.page-container {
		width: 100vw;
		height: 100vh;
		overflow: hidden;
		position: relative;
	}

	.sidebar-mask {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, 0.4);
		z-index: 999;

		.sidebar-body {
			width: 500rpx;
			height: 100%;
			background: #fff;
			padding: 100rpx 30rpx;
			animation: slideIn 0.3s ease;
			display: flex;
			flex-direction: column;
		}
	}

	.sidebar-header {
		font-size: 36rpx;
		font-weight: bold;
		margin-bottom: 30rpx;
		color: #333;
	}

	@keyframes slideIn {
		from {
			transform: translateX(-100%);
		}

		to {
			transform: translateX(0);
		}
	}

	/* 侧边栏列表样式 */
	.history-list {
		flex: 1;

		.history-item {
			padding: 24rpx;
			background: #f8f9fb;
			border-radius: 12rpx;
			margin-bottom: 20rpx;
			font-size: 28rpx;
			color: #444;
			overflow: hidden;
			text-overflow: ellipsis;
			white-space: nowrap;
		}

		.no-history {
			text-align: center;
			color: #999;
			margin-top: 100rpx;
			font-size: 26rpx;
		}
	}

	/* 后续样式保持你原本的... */
	.main-content {
		display: flex;
		flex-direction: column;
		height: 100%;
	}

	.header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 60rpx 30rpx 20rpx;
		border-bottom: 1rpx solid #eee;

		.nav-btn {
			display: flex;
			align-items: center;
			background: #f0f0f0;
			padding: 10rpx 20rpx;
			border-radius: 30rpx;
			font-size: 24rpx;

			.nav-icon {
				width: 30rpx;
				height: 30rpx;
				margin-right: 10rpx;
			}
		}

		.title {
			font-weight: bold;
			font-size: 32rpx;
		}
	}

	.chat-area {
		flex: 1;
		overflow: hidden;
		background: #fff;
		scroll-behavior: smooth; 
		-webkit-overflow-scrolling: touch;
	}

	.welcome {
		padding-top: 150rpx;
		text-align: center;

		.logo {
			width: 100rpx;
			height: 100rpx;
		}

		.brand-name {
			font-size: 50rpx;
			font-weight: bold;
			color: #e60012;
			margin: 20rpx 0;
		}

		.welcome-msg {
			margin-top: 50rpx;
			font-size: 36rpx;
			font-weight: bold;
		}
	}

.message-list {
    padding: 30rpx;
    display: flex;         /* 必须 */
    flex-direction: column; /* 必须：确保气泡纵向排列 */

    .msg-box {
        display: flex;
        margin-bottom: 40rpx; /* 这里的间距决定了气泡是否连在一起 */
        width: 100%;          /* 占满宽度防止并排 */
        
        &.user {
            flex-direction: row-reverse;
            .bubble {
                background: #dbe0f2;
                margin-right: 20rpx; /* 与用户头像保持距离 */
            }
        }

        &.ai {
            flex-direction: row;
            .bubble {
                background: #f5f6f8;
                margin-left: 20rpx; /* 与 AI 头像保持距离 */
            }
        }

        .avatar {
            width: 70rpx;
            height: 70rpx;
            border-radius: 50%;
            flex-shrink: 0; /* 防止头像被挤压 */
        }

        .bubble {
            max-width: 70%;
            padding: 20rpx;
            border-radius: 20rpx;
            font-size: 28rpx;
            word-break: break-all; /* 强制长文本换行 */
            position: relative;
            
            .content-img {
                max-width: 100%;
                border-radius: 12rpx;
                margin-bottom: 10rpx;
                display: block;
            }
        }
    }
    
    /* 专门为流式气泡加一点点动画，方便肉眼区分它是一个新框 */
    .streaming {
        animation: fadeIn 0.3s ease;
    }
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10rpx); }
    to { opacity: 1; transform: translateY(0); }
}
	.input-panel {
		padding: 20rpx 30rpx 50rpx;
		border-top: 1rpx solid #eee;
		background: #fff;

		.img-preview {
			position: relative;
			display: inline-block;
			margin-bottom: 10rpx;

			image {
				width: 120rpx;
				height: 120rpx;
				border-radius: 10rpx;
			}

			.del-img {
				position: absolute;
				top: -10rpx;
				right: -10rpx;
				background: #999;
				color: #fff;
				border-radius: 50%;
				padding: 0 10rpx;
			}
		}

		.input-box {
			background: #f5f6f8;
			border-radius: 20rpx;
			padding: 20rpx;

			textarea {
				width: 100%;
				min-height: 40rpx;
				font-size: 30rpx;
			}
		}

		.toolbar {
			display: flex;
			justify-content: space-between;
			align-items: center;
			margin-top: 20rpx;

			.tool-left {
				display: flex;

				.btn-mini {
					display: flex;
					align-items: center;
					background: #f5f6f8;
					padding: 10rpx 20rpx;
					border-radius: 30rpx;
					margin-right: 15rpx;
					font-size: 22rpx;

					.mini-icon {
						width: 24rpx;
						height: 24rpx;
						margin-right: 6rpx;
					}
				}

				.active {
					background: #e60012;
					color: #fff;
				}
			}

			.tool-right {
				display: flex;
				align-items: center;

				.plus-icon {
					font-size: 44rpx;
					color: #666;
					margin-right: 30rpx;
					font-weight: 300;
				}

				.send-btn {
					width: 70rpx;
					height: 70rpx;
					background: #dbe0f2;
					color: #fff;
					border-radius: 50%;
					display: flex;
					align-items: center;
					justify-content: center;
					font-weight: bold;
					font-size: 36rpx;
				}
			}
		}
	}
</style>