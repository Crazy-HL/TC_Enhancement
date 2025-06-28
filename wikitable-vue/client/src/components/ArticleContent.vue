<template>
	<div class="article-layout">
		<!-- 弹幕控制面板 -->
		<div class="danmu-controls">
			<div class="control-header">
				<h4>弹幕设置</h4>
				<button @click="toggleControls" class="toggle-btn">
					{{ showControls ? "隐藏设置" : "显示设置" }}
				</button>
			</div>

			<div v-if="showControls" class="control-body">
				<!-- 样式选择 -->
				<div class="control-row">
					<div class="control-group">
						<label>弹幕样式：</label>
						<select v-model="danmuStyle" class="control-select">
							<option value="text">文字弹幕</option>
							<option value="card">卡片弹幕</option>
						</select>
					</div>
				</div>

				<!-- 基础设置 -->
				<div class="control-row">
					<div class="control-group">
						<label>
							<span>弹幕行数：{{ danmuLines }}</span>
							<input
								type="range"
								min="1"
								max="8"
								v-model.number="danmuLines"
								class="control-slider" />
						</label>
					</div>

					<div class="control-group">
						<label>
							<span>最大数量：{{ maxDanmus }}</span>
							<input
								type="range"
								min="1"
								max="15"
								v-model.number="maxDanmus"
								class="control-slider" />
						</label>
					</div>
				</div>

				<!-- 速度设置 -->
				<div class="control-row">
					<div class="control-group">
						<label>
							<span>移动速度：{{ danmuSpeed }}s</span>
							<input
								type="range"
								min="5"
								max="30"
								v-model.number="danmuSpeed"
								class="control-slider" />
						</label>
					</div>

					<div class="control-group">
						<label>
							<span>透明度：{{ opacity }}%</span>
							<input
								type="range"
								min="30"
								max="100"
								v-model.number="opacity"
								class="control-slider" />
						</label>
					</div>
				</div>

				<!-- 文字弹幕设置 -->
				<div class="control-row" v-if="danmuStyle === 'text'">
					<div class="control-group">
						<label>
							<span>字体大小：{{ textFontSize }}px</span>
							<input
								type="range"
								min="12"
								max="24"
								v-model.number="textFontSize"
								class="control-slider" />
						</label>
					</div>
				</div>

				<!-- 卡片弹幕设置 -->
				<template v-if="danmuStyle === 'card'">
					<div class="control-row">
						<div class="control-group">
							<label>
								<span>卡片宽度：{{ cardWidth }}px</span>
								<input
									type="range"
									min="200"
									max="400"
									v-model.number="cardWidth"
									class="control-slider" />
							</label>
						</div>

						<div class="control-group">
							<label>
								<span>行高：{{ lineHeight }}px</span>
								<input
									type="range"
									min="40"
									max="120"
									v-model.number="lineHeight"
									class="control-slider" />
							</label>
						</div>
					</div>

					<div class="control-row">
						<div class="control-group">
							<label>
								<span>字体大小：{{ cardFontSize }}px</span>
								<input
									type="range"
									min="12"
									max="20"
									v-model.number="cardFontSize"
									class="control-slider" />
							</label>
						</div>

						<div class="control-group">
							<label class="checkbox-label">
								<input
									type="checkbox"
									v-model="showAvatars"
									class="control-checkbox" />
								显示头像
							</label>
						</div>
					</div>
				</template>
			</div>
		</div>

		<!-- 弹幕展示区域 -->
		<DanmuDisplay
			:comments="comments"
			:active-sentence="activeSentence"
			:max-lines="danmuLines"
			:max-danmus="maxDanmus"
			:base-speed="danmuSpeed"
			:style-type="danmuStyle"
			:card-width="cardWidth"
			:line-height="lineHeight"
			:text-font-size="textFontSize"
			:card-font-size="cardFontSize"
			:opacity="opacity"
			:show-avatars="showAvatars" />

		<!-- 文章内容区域 -->
		<div class="article-container" v-if="article" ref="articleContainer">
			<!-- 文章标题 -->
			<h1 class="article-title">{{ article.title }}</h1>

			<!-- 文章元信息 -->
			<div class="article-meta">
				<span class="author">作者：{{ article.user_nickname }}</span>
				<span class="publish-time"
					>发布时间：{{ formatTime(article.created_time) }}</span
				>
				<span class="update-time"
					>更新时间：{{ formatTime(article.updated_time) }}</span
				>
			</div>

			<!-- 文章内容（分句显示） -->
			<div class="article-content">
				<span
					v-for="(sentence, index) in sentences"
					:key="index"
					class="sentence"
					:id="'sentence-' + index"
					:data-sentence-id="index"
					@mouseenter="showRelatedComments(index)"
					@mouseleave="hideComments">
					{{ sentence }}

					<!-- 相关评论浮层 -->
					<div
						class="comment-popup"
						v-if="
							activeSentence === index &&
							getCommentsForSentence(index).length > 0
						"
						:style="getPopupPosition(index)">
						<div
							v-for="comment in getCommentsForSentence(index)"
							:key="comment.comment_id"
							class="comment-card">
							<div class="comment-user">
								<img
									:src="comment.user_avatar || defaultAvatar"
									class="avatar"
									@error="handleAvatarError" />
								<span class="username">{{ comment.user_nickname }}</span>
							</div>
							<div class="comment-text">{{ comment.content }}</div>
						</div>
					</div>
				</span>
			</div>

			<!-- 全局评论 -->
			<div class="global-comments" v-if="globalComments.length > 0">
				<h3>文章整体评论</h3>
				<div
					v-for="comment in globalComments"
					:key="'global-' + comment.comment_id"
					class="comment-card global">
					<div class="comment-user">
						<img
							:src="comment.user_avatar || defaultAvatar"
							class="avatar"
							@error="handleAvatarError" />
						<span class="username">{{ comment.user_nickname }}</span>
					</div>
					<div class="comment-text">{{ comment.content }}</div>
				</div>
			</div>

			<!-- 文章页脚 -->
			<div class="article-footer">
				<div class="stats">
					<span class="vote-count">点赞：{{ article.voteup_count }}</span>
					<span class="comment-count">评论：{{ article.comment_count }}</span>
				</div>
				<a :href="article.content_url" target="_blank" class="original-link"
					>阅读原文</a
				>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { ref, onMounted, computed, watch } from "vue";
	import api from "@/api";
	import DanmuDisplay from "@/components/DanmuDisplay.vue";

	// 默认头像
	const defaultAvatar =
		"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iI2NjYyIgZD0iTTEyLDJBMTAsMTAgMCAwLDAgMiwxMkExMCwxMCAwIDAsMCAxMiwyMkExMCwxMCAwIDAsMCAyMiwxMkExMCwxMCAwIDAsMCAxMiwyTTEyLDRBNyA3IDAgMCwxIDE5LDExQTcgNyAwIDAsMSAxMiwxOEE3LDcgMCAwLDEgNSwxMUE3LDcgMCAwLDEgMTIsNE0xMiw2QTUsNSAwIDAsMCA3LDExQTUsNSAwIDAsMCAxMiwxNkE1LDUgMCAwLDAgMTcsMTFBNSw1IDAgMCwwIDEyLDZNMTIsOEEzLDMgMCAwLDEgMTUsMTFBNCw0IDAgMCwxIDEyLDE1QTQsNCAwIDAsMSA5LDExQTMsMyAwIDAsMSAxMiw4WiIvPjwvc3ZnPg==";

	// 文章数据
	const article = ref(null);
	const sentences = ref([]);
	const comments = ref([]);
	const activeSentence = ref(null);
	const articleContainer = ref(null);

	// 弹幕控制参数
	const showControls = ref(true);
	const danmuLines = ref(3);
	const maxDanmus = ref(5);
	const danmuSpeed = ref(10);
	const danmuStyle = ref("text");
	const cardWidth = ref(280);
	const lineHeight = ref(80);
	const textFontSize = ref(16);
	const cardFontSize = ref(14);
	const opacity = ref(85);
	const showAvatars = ref(true);

	// 格式化时间
	const formatTime = time => {
		if (!time) return "";
		const date = new Date(time * 1000);
		return date.toLocaleString();
	};

	// 分割句子的函数
	const splitIntoSentences = text => {
		if (!text) return [];
		const regex = /([^。！？.!?]+[。！？.!?]+)/g;
		const result = [];
		let match;

		while ((match = regex.exec(text)) !== null) {
			const sentence = match[0].trim();
			if (sentence.length > 0) {
				result.push(sentence);
			}
		}
		return result.length > 0 ? result : [text];
	};

	// 获取某句子的相关评论
	const getCommentsForSentence = sentenceIndex => {
		return comments.value.filter(comment => comment.link === sentenceIndex);
	};

	// 显示相关评论
	const showRelatedComments = index => {
		activeSentence.value = index;
	};

	// 隐藏评论
	const hideComments = () => {
		activeSentence.value = null;
	};

	// 计算浮层位置
	const getPopupPosition = index => {
		const sentenceEl = document.getElementById(`sentence-${index}`);
		if (!sentenceEl) return {};

		const rect = sentenceEl.getBoundingClientRect();
		const containerRect = articleContainer.value.getBoundingClientRect();

		// 计算相对于文章容器的位置
		const top = rect.top - containerRect.top + rect.height + 5;
		const left = rect.left - containerRect.left;

		return {
			top: `${top}px`,
			left: `${left}px`,
			minWidth: `${rect.width}px`
		};
	};

	// 处理头像加载错误
	const handleAvatarError = e => {
		e.target.src = defaultAvatar;
	};

	// 全局评论
	const globalComments = computed(() => {
		return comments.value.filter(comment => comment.link === -1);
	});

	// 切换控制面板显示
	const toggleControls = () => {
		showControls.value = !showControls.value;
	};

	// 从本地存储加载设置
	const loadSettings = () => {
		const saved = localStorage.getItem("danmuSettings");
		if (saved) {
			try {
				const settings = JSON.parse(saved);
				danmuLines.value = settings.lines || 3;
				maxDanmus.value = settings.max || 5;
				danmuSpeed.value = settings.speed || 10;
				danmuStyle.value = settings.style || "text";
				cardWidth.value = settings.cardWidth || 280;
				lineHeight.value = settings.lineHeight || 80;
				textFontSize.value = settings.textFontSize || 16;
				cardFontSize.value = settings.cardFontSize || 14;
				opacity.value = settings.opacity || 85;
				showAvatars.value = settings.showAvatars !== false;
				showControls.value = settings.showControls !== false;
			} catch (e) {
				console.error("加载设置失败", e);
			}
		}
	};

	// 保存设置到本地存储
	const saveSettings = () => {
		const settings = {
			lines: danmuLines.value,
			max: maxDanmus.value,
			speed: danmuSpeed.value,
			style: danmuStyle.value,
			cardWidth: cardWidth.value,
			lineHeight: lineHeight.value,
			textFontSize: textFontSize.value,
			cardFontSize: cardFontSize.value,
			opacity: opacity.value,
			showAvatars: showAvatars.value,
			showControls: showControls.value
		};
		localStorage.setItem("danmuSettings", JSON.stringify(settings));
	};

	// 监听所有设置变化
	watch(
		[
			danmuLines,
			maxDanmus,
			danmuSpeed,
			danmuStyle,
			cardWidth,
			lineHeight,
			textFontSize,
			cardFontSize,
			opacity,
			showAvatars,
			showControls
		],
		saveSettings,
		{ deep: true }
	);

	// 初始化
	onMounted(() => {
		loadSettings();

		api.get("article", {}, data => {
			article.value = data[0];
			sentences.value = splitIntoSentences(data[0].content_text);
		});

		api.get("comments", {}, data => {
			comments.value = data;
		});
	});
</script>

<style scoped>
	/* 布局样式 */
	.article-layout {
		display: flex;
		justify-content: center;
		max-width: 1200px;
		margin: 0 auto;
		position: relative;
	}

	/* 文章容器样式 */
	.article-container {
		max-width: 800px;
		width: 100%;
		padding: 20px;
		background: #fff;
		border-radius: 8px;
		box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
		position: relative;
		margin-top: 60px;
	}

	/* 弹幕控制面板样式 */
	.danmu-controls {
		position: fixed;
		top: 10px;
		right: 10px;
		z-index: 1000;
		background: rgba(255, 255, 255, 0.98);
		padding: 15px;
		border-radius: 10px;
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
		width: 320px;
		max-height: 80vh;
		overflow-y: auto;
		transition: all 0.3s ease;
	}

	.control-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 12px;
		padding-bottom: 8px;
		border-bottom: 1px solid #eee;
	}

	.control-header h4 {
		margin: 0;
		font-size: 16px;
		color: #333;
	}

	.toggle-btn {
		background: #f0f0f0;
		border: none;
		padding: 4px 10px;
		border-radius: 4px;
		cursor: pointer;
		font-size: 12px;
	}

	.toggle-btn:hover {
		background: #e0e0e0;
	}

	.control-body {
		display: flex;
		flex-direction: column;
		gap: 12px;
	}

	.control-row {
		display: flex;
		gap: 15px;
	}

	.control-group {
		flex: 1;
		min-width: 0;
	}

	.control-group label {
		display: flex;
		flex-direction: column;
		font-size: 13px;
		color: #555;
		margin-bottom: 5px;
	}

	.control-group label span {
		margin-bottom: 4px;
	}

	.control-slider {
		width: 100%;
		height: 6px;
		border-radius: 3px;
		background: #e0e0e0;
		outline: none;
		-webkit-appearance: none;
	}

	.control-slider::-webkit-slider-thumb {
		-webkit-appearance: none;
		width: 16px;
		height: 16px;
		border-radius: 50%;
		background: #0084ff;
		cursor: pointer;
	}

	.control-select {
		width: 100%;
		padding: 6px 8px;
		border-radius: 4px;
		border: 1px solid #ddd;
		background: white;
		font-size: 13px;
	}

	.checkbox-label {
		display: flex;
		align-items: center;
		flex-direction: row;
		gap: 6px;
		cursor: pointer;
	}

	.control-checkbox {
		width: 16px;
		height: 16px;
	}

	/* 文章内容样式 */
	.sentence {
		display: inline;
		margin-right: 0.2em;
		position: relative;
		cursor: pointer;
		transition: background-color 0.2s;
	}

	.sentence:hover {
		background-color: #f0f7ff;
	}

	.comment-popup {
		position: absolute;
		z-index: 100;
		background: white;
		border-radius: 8px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
		padding: 10px;
		max-height: 300px;
		overflow-y: auto;
		border: 1px solid #eaeaea;
	}

	.comment-card {
		padding: 10px;
		margin-bottom: 10px;
		background: #f9f9f9;
		border-radius: 6px;
	}

	.comment-card:last-child {
		margin-bottom: 0;
	}

	.comment-user {
		display: flex;
		align-items: center;
		margin-bottom: 6px;
	}

	.avatar {
		width: 24px;
		height: 24px;
		border-radius: 50%;
		margin-right: 8px;
		object-fit: cover;
		background-color: #f0f0f0;
	}

	.username {
		font-size: 14px;
		font-weight: bold;
		color: #333;
	}

	.comment-text {
		font-size: 14px;
		line-height: 1.5;
		color: #333;
	}

	.article-title {
		font-size: 24px;
		margin-bottom: 15px;
		color: #333;
		line-height: 1.4;
	}

	.article-meta {
		margin-bottom: 20px;
		font-size: 14px;
		color: #666;
	}

	.article-meta span {
		margin-right: 15px;
	}

	.article-content {
		font-size: 16px;
		line-height: 1.8;
		color: #333;
		margin-bottom: 20px;
	}

	.article-footer {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding-top: 15px;
		border-top: 1px solid #eee;
		font-size: 14px;
		color: #666;
	}

	.stats span {
		margin-right: 15px;
	}

	.original-link {
		color: #0084ff;
		text-decoration: none;
	}

	.original-link:hover {
		text-decoration: underline;
	}

	.global-comments {
		margin-top: 40px;
		padding-top: 20px;
		border-top: 1px solid #eee;
	}

	.global-comments h3 {
		margin-bottom: 15px;
		font-size: 18px;
		color: #333;
	}

	.global-comments .comment-card {
		margin-bottom: 15px;
		background: white;
		border: 1px solid #eaeaea;
		padding: 12px;
	}
</style>
