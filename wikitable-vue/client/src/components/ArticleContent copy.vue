<template>
	<div class="article-container">
		<!-- 顶部控制面板（包含图注） -->
		<div class="control-panel">
			<!-- 左侧控制按钮组 -->
			<div class="control-group-container">
				<div class="control-group">
					<label class="icon-toggle">
						<input type="checkbox" v-model="showInlineComments" />
						<svg viewBox="0 0 24 24" width="18" height="18">
							<path
								fill="currentColor"
								d="M12,3C17,3 21,7 21,12C21,17 17,21 12,21C7,21 3,17 3,12C3,7 7,3 12,3M12,7C10.9,7 10,7.9 10,9C10,10.1 10.9,11 12,11C13.1,11 14,10.1 14,9C14,7.9 13.1,7 12,7M12,15.2C10.67,15.2 9.5,14.5 8.8,13.5C8.9,12.6 9.8,12 10.9,12C11.5,12 12.1,12.2 12.5,12.6C12.9,13 13.3,13.4 13.6,13.8C14.4,14.4 15.5,14.5 16.4,14.1C16.9,13.9 17.4,13.5 17.7,13C16.5,14.4 14.4,15.2 12,15.2Z" />
						</svg>
					</label>
					<span class="control-label">内联评论</span>
				</div>

				<div class="control-group">
					<label class="icon-toggle">
						<input type="checkbox" v-model="showPieCharts" />
						<svg viewBox="0 0 24 24" width="18" height="18">
							<path
								fill="currentColor"
								d="M11,2V22C5.9,21.5 2,17.2 2,12C2,6.8 5.9,2.5 11,2M13,2V11H22C21.5,6.2 17.8,2.5 13,2M13,13V22C17.7,21.5 21.5,17.8 22,13H13Z" />
						</svg>
					</label>
					<span class="control-label">饼图</span>
				</div>

				<div class="control-group">
					<label class="icon-toggle">
						<input type="checkbox" v-model="showStackedCharts" />
						<svg viewBox="0 0 24 24" width="18" height="18">
							<path
								fill="currentColor"
								d="M4,4H20V20H4V4M6,6V18H8V6H6M10,6V12H12V6H10M14,6V15H16V6H14Z" />
						</svg>
					</label>
					<span class="control-label">堆叠图</span>
				</div>

				<!-- 新增的内容高亮控制按钮 -->
				<div class="control-group">
					<label class="icon-toggle">
						<input type="checkbox" v-model="showContentHighlight" />
						<svg viewBox="0 0 24 24" width="18" height="18">
							<path
								fill="currentColor"
								d="M12,3C16.97,3 21,7.03 21,12C21,16.97 16.97,21 12,21C7.03,21 3,16.97 3,12C3,7.03 7.03,3 12,3M12,5C8.14,5 5,8.14 5,12C5,15.86 8.14,19 12,19C15.86,19 19,15.86 19,12C19,8.14 15.86,5 12,5M12,7.25C13.79,7.25 15.25,8.71 15.25,10.5C15.25,12.29 13.79,13.75 12,13.75C10.21,13.75 8.75,12.29 8.75,10.5C8.75,8.71 10.21,7.25 12,7.25Z" />
						</svg>
					</label>
					<span class="control-label">内容高亮</span>
				</div>
			</div>

			<!-- 右侧图注部分 -->
			<div class="legend-section">
				<!-- 评论类型图注 - 修改为整个图注可点击 -->
				<div class="comment-type-legend">
					<button
						class="legend-item"
						:class="{ active: visibleCommentTypes[1] }"
						@click="toggleCommentTypeVisibility(1)">
						<span class="underline blue">【陈述】</span>
					</button>
					<button
						class="legend-item"
						:class="{ active: visibleCommentTypes[2] }"
						@click="toggleCommentTypeVisibility(2)">
						<span class="circle red">【疑问】</span>
					</button>
					<button
						class="legend-item"
						:class="{ active: visibleCommentTypes[3] }"
						@click="toggleCommentTypeVisibility(3)">
						<span class="double-underline green">【感叹】</span>
					</button>
					<button
						class="legend-item"
						:class="{ active: visibleCommentTypes[4] }"
						@click="toggleCommentTypeVisibility(4)">
						<span class="solid-underline purple">【建议】</span>
					</button>
					<button
						class="legend-item"
						:class="{ active: visibleCommentTypes[5] }"
						@click="toggleCommentTypeVisibility(5)">
						<span class="rounded-box orange">【讽刺】</span>
					</button>
				</div>

				<!-- 饼图和堆叠图图注 -->
				<ChartLegend
					:comments="allCommentsForLegend"
					class="chart-legend"
					:showPieChart="showPieCharts"
					:showStackedChart="showStackedCharts" />
			</div>
		</div>

		<!-- 三栏主要内容区 -->
		<div class="main-content">
			<!-- 第一栏：文章整体评论 -->
			<div class="panel global-comments-panel" v-if="globalComments.length > 0">
				<div class="panel-header">
					<h4>文章整体评论 ({{ globalComments.length }})</h4>
				</div>
				<div class="panel-content">
					<div
						v-for="comment in globalComments"
						:key="'global-' + comment.comment_id"
						class="comment-item"
						:style="{
							'border-left': `4px solid ${getStandpointColor(comment)}`,
							'border-right': `4px solid ${getEmotionColor(comment)}`
						}"
						:title="`立场: ${getStandpointLabel(
							comment
						)} | 情感: ${getEmotionLabel(
							comment
						)} | 类型: ${getCommentTypeLabel(comment)}`">
						<div class="comment-user">
							<img
								:src="comment.user_avatar || defaultAvatar"
								class="avatar"
								@error="handleAvatarError" />
							<span class="username">{{ comment.user_nickname }}</span>
						</div>
						<div class="comment-text">{{ comment.content }}</div>
						<div class="comment-stats">
							<span class="like-count" title="点赞数">
								<svg class="icon" viewBox="0 0 24 24" width="14" height="14">
									<path
										fill="currentColor"
										d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
								</svg>
								{{ formatNumber(comment.like_count) }}
							</span>
							<span class="reply-count" title="回复数">
								<svg class="icon" viewBox="0 0 24 24" width="14" height="14">
									<path
										fill="currentColor"
										d="M12 3c5.514 0 10 3.592 10 8.007 0 4.917-5.144 7.961-9.91 7.961-1.937 0-3.384-.397-4.394-.644-1 .613-1.595 1.037-4.272 1.82.535-1.277.723-2.215.725-3.292C3.484 16.541 2 13.975 2 11.007 2 6.592 6.486 3 12 3zm0-2C5.373 1 0 5.373 0 11c0 2.042.808 3.945 2.278 5.391.239.276.283.673.117.988-.288.555-.555 1.064-.763 1.554.302-.11.744-.266 1.326-.558.379-.19.857-.207 1.24-.039.96.42 2.079.635 3.253.635 6.086 0 11-4.015 11-9 0-5.627-5.373-10-11-10z" />
								</svg>
								{{ formatNumber(comment.sub_comment_count) }}
							</span>
						</div>
					</div>
				</div>
			</div>

			<!-- 第二栏：文章内容 -->
			<div class="panel article-panel" v-if="article" ref="articleContainer">
				<h1 class="article-title">{{ article.title }}</h1>
				<div class="article-meta">
					<span class="author">作者：{{ article.user_nickname }}</span>
					<span class="publish-time"
						>发布时间：{{ formatTime(article.created_time) }}</span
					>
					<span class="update-time"
						>更新时间：{{ formatTime(article.updated_time) }}</span
					>
				</div>

				<div class="article-content">
					<template v-for="(sentence, index) in sentences" :key="index">
						<!-- 句子前的立场堆叠图 -->
						<CommentStats
							v-if="
								hasComments(index) &&
								showStackedCharts &&
								visibleCommentTypes[getCommentType(getTopComment(index))]
							"
							:comments="getCommentsForSentence(index)"
							:show-emotion="false"
							class="before-stats" />

						<!-- 句子前的类型饼图 -->
						<CommentStats
							v-if="
								hasComments(index) &&
								showPieCharts &&
								visibleCommentTypes[getCommentType(getTopComment(index))]
							"
							:comments="getCommentsForSentence(index)"
							:show-standpoint="false"
							:show-type="true"
							class="before-stats" />

						<span
							class="sentence"
							:id="'sentence-' + index"
							:class="{
								'has-comment': hasComments(index),
								[`comment-level-${getCommentLevel(index).level}`]:
									hasComments(index) && showContentHighlight,
								[`comment-type-${getCommentType(getTopComment(index))}`]:
									hasComments(index) &&
									visibleCommentTypes[getCommentType(getTopComment(index))],
								selected: activeSentence === index
							}"
							@click="toggleActiveSentence(index)">
							{{ sentence }}
							<sup
								v-if="
									hasComments(index) &&
									visibleCommentTypes[getCommentType(getTopComment(index))]
								"
								class="annotation-marker">
								{{ getCommentsForSentence(index).length }}
							</sup>
						</span>

						<!-- 内联评论 -->
						<span
							v-if="
								showInlineComments &&
								hasComments(index) &&
								visibleCommentTypes[getCommentType(getTopComment(index))]
							"
							class="inline-comment"
							:class="`comment-type-${getCommentType(getTopComment(index))}`">
							【{{ getCommentTypeLabel(getTopComment(index)) }}：{{
								formatCommentContent(getTopComment(index).content)
							}}】
						</span>
					</template>
				</div>

				<div class="article-footer">
					<div class="stats">
						<span class="vote-count"
							>点赞：{{ formatNumber(article.voteup_count) }}</span
						>
						<span class="comment-count"
							>评论：{{ formatNumber(article.comment_count) }}</span
						>
					</div>
					<a :href="article.content_url" target="_blank" class="original-link"
						>阅读原文</a
					>
				</div>
			</div>

			<!-- 第三栏：句子相关评论 -->
			<div
				class="panel annotation-panel"
				v-if="activeSentence !== null && hasComments(activeSentence)"
				ref="annotationPanel">
				<div class="panel-header">
					<h4>
						相关评论 ({{ getCommentsForSentence(activeSentence).length }})
					</h4>
					<button @click="activeSentence = null" class="close-btn">×</button>
				</div>
				<div class="panel-content">
					<div
						v-for="comment in getCommentsForSentence(activeSentence)"
						:key="comment.comment_id"
						class="annotation-item"
						:style="{
							'border-left': `4px solid ${getStandpointColor(comment)}`,
							'border-right': `4px solid ${getEmotionColor(comment)}`
						}"
						:title="`立场: ${getStandpointLabel(
							comment
						)} | 情感: ${getEmotionLabel(
							comment
						)} | 类型: ${getCommentTypeLabel(comment)} | 点赞: ${formatNumber(
							comment.like_count
						)} | 回复: ${formatNumber(comment.sub_comment_count)}`">
						<div class="annotation-user">
							<img
								:src="comment.user_avatar || defaultAvatar"
								class="avatar"
								@error="handleAvatarError" />
							<span class="username">{{ comment.user_nickname }}</span>
						</div>
						<div class="annotation-text">{{ comment.content }}</div>
						<div class="annotation-stats">
							<span class="like-count" title="点赞数">
								<svg class="icon" viewBox="0 0 24 24" width="14" height="14">
									<path
										fill="currentColor"
										d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
								</svg>
								{{ formatNumber(comment.like_count) }}
							</span>
							<span class="reply-count" title="回复数">
								<svg class="icon" viewBox="0 0 24 24" width="14" height="14">
									<path
										fill="currentColor"
										d="M12 3c5.514 0 10 3.592 10 8.007 0 4.917-5.144 7.961-9.91 7.961-1.937 0-3.384-.397-4.394-.644-1 .613-1.595 1.037-4.272 1.82.535-1.277.723-2.215.725-3.292C3.484 16.541 2 13.975 2 11.007 2 6.592 6.486 3 12 3zm0-2C5.373 1 0 5.373 0 11c0 2.042.808 3.945 2.278 5.391.239.276.283.673.117.988-.288.555-.555 1.064-.763 1.554.302-.11.744-.266 1.326-.558.379-.19.857-.207 1.24-.039.96.42 2.079.635 3.253.635 6.086 0 11-4.015 11-9 0-5.627-5.373-10-11-10z" />
								</svg>
								{{ formatNumber(comment.sub_comment_count) }}
							</span>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- 连接线容器 -->
		<div class="connection-container" ref="connectionContainer">
			<svg
				class="connection-line"
				v-if="activeSentence !== null && hasComments(activeSentence)"
				:style="connectionStyle">
				<line
					x1="0"
					y1="0"
					x2="100%"
					y2="0"
					stroke="#FF5722"
					stroke-width="2"
					stroke-dasharray="4,2" />
			</svg>
		</div>
	</div>
</template>

<script setup>
	import { ref, onMounted, computed, watch, nextTick } from "vue";
	import api from "@/api";
	import CommentStats from "./CommentStats.vue";
	import ChartLegend from "./ChartLegend.vue";

	const defaultAvatar =
		"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iI2NjYyIgZD0iTTEyLDJBMTAsMTAgMCAwLDAgMiwxMkExMCwxMCAwIDAsMCAxMiwyMkExMCwxMCAwIDAsMCAyMiwxMkExMCwxMCAwIDAsMCAxMiwyTTEyLDRBNyA3IDAgMCwxIDE5LDExQTcgNyAwIDAsMSAxMiwxOEE3LDcgMCAwLDEgNSwxMUE3LDcgMCAwLDEgMTIsNE0xMiw2QTUsNSAwIDAsMCA3LDExQTUsNSAwIDAsMCAxMiwxNkE1LDUgMCAwLDAgMTcsMTFBNSw1IDAgMCwwIDEyLDZNMTIsOEEzLDMgMCAwLDEgMTUsMTFBNCw4IDAgMCwxIDEyLDE1QTQsNCAwIDAsMSA5LDExQTMsMyAwIDAsMSAxMiw4WiIvPjwvc3ZnPg==";

	const article = ref(null);
	const sentences = ref([]);
	const comments = ref([]);
	const activeSentence = ref(null);
	const articleContainer = ref(null);
	const annotationPanel = ref(null);
	const connectionContainer = ref(null);
	const showInlineComments = ref(true);
	const showPieCharts = ref(true);
	const showStackedCharts = ref(true);
	const showContentHighlight = ref(true);

	// 评论类型可见性控制
	const visibleCommentTypes = ref({
		1: true, // 陈述
		2: true, // 疑问
		3: true, // 感叹
		4: true, // 建议
		5: true // 讽刺
	});

	const allCommentsForLegend = computed(() => {
		return comments.value;
	});

	const connectionStyle = ref({
		left: "0px",
		top: "0px",
		width: "0px",
		transform: "rotate(0deg)"
	});

	// 切换评论类型可见性
	const toggleCommentTypeVisibility = type => {
		visibleCommentTypes.value[type] = !visibleCommentTypes.value[type];
	};

	// 切换选中句子
	const toggleActiveSentence = index => {
		if (activeSentence.value === index) {
			activeSentence.value = null;
		} else if (hasComments(index)) {
			activeSentence.value = index;
		}
		updateConnectionLine();
	};

	const getCommentType = comment => {
		return comment?.comment_type || 1;
	};

	const getCommentTypeLabel = comment => {
		const type = getCommentType(comment);
		return (
			{
				1: "陈述",
				2: "疑问",
				3: "感叹",
				4: "建议",
				5: "讽刺"
			}[type] || "陈述"
		);
	};

	const formatCommentContent = content => {
		if (!content) return "";
		const lastChar = content[content.length - 1];
		const punctuation = /[。.！!？?，,；;、]/.test(lastChar) ? "" : "。";
		return content + punctuation;
	};

	const getTopComment = sentenceIndex => {
		const comments = getCommentsForSentence(sentenceIndex);
		if (comments.length === 0) return null;
		return [...comments].sort((a, b) => b.like_count - a.like_count)[0];
	};

	const formatNumber = num => {
		if (!num && num !== 0) return "0";
		if (num >= 1000) return (num / 1000).toFixed(1) + "k";
		return num;
	};

	const updateConnectionLine = () => {
		if (
			!activeSentence.value ||
			!articleContainer.value ||
			!annotationPanel.value ||
			!connectionContainer.value
		)
			return;

		const sentenceEl = document.getElementById(
			`sentence-${activeSentence.value}`
		);
		if (!sentenceEl) return;

		nextTick(() => {
			const sentenceRect = sentenceEl.getBoundingClientRect();
			const panelRect = annotationPanel.value.getBoundingClientRect();
			const containerRect = connectionContainer.value.getBoundingClientRect();

			const startX = sentenceRect.right;
			const startY = sentenceRect.top + sentenceRect.height / 2;
			const endX = panelRect.left;
			const endY = panelRect.top + panelRect.height / 2;

			const length = Math.sqrt(
				Math.pow(endX - startX, 2) + Math.pow(endY - startY, 2)
			);
			const angle = (Math.atan2(endY - startY, endX - startX) * 180) / Math.PI;

			connectionStyle.value = {
				left: `${startX - containerRect.left}px`,
				top: `${startY - containerRect.top}px`,
				width: `${length}px`,
				transform: `rotate(${angle}deg)`,
				transformOrigin: "0 0"
			};
		});
	};

	const formatTime = time => {
		if (!time) return "";
		return new Date(time * 1000).toLocaleString();
	};

	const splitIntoSentences = text => {
		if (!text) return [];
		const regex = /([^。！？.!?]+[。！？.!?]+)/g;
		const result = [];
		let match;
		while ((match = regex.exec(text)) !== null) {
			const sentence = match[0].trim();
			if (sentence) result.push(sentence);
		}
		return result.length > 0 ? result : [text];
	};

	const getCommentsForSentence = sentenceIndex => {
		return comments.value.filter(
			comment =>
				comment.link === sentenceIndex &&
				visibleCommentTypes.value[getCommentType(comment)]
		);
	};

	const hasComments = sentenceIndex => {
		return getCommentsForSentence(sentenceIndex).length > 0;
	};

	const getCommentLevel = sentenceIndex => {
		const count = getCommentsForSentence(sentenceIndex).length;
		const level = Math.min(Math.floor(count / 3) + 1, 5);
		const comments = getCommentsForSentence(sentenceIndex);
		const topComment = comments.length ? getTopComment(sentenceIndex) : null;
		const type = topComment ? getCommentType(topComment) : 1;

		return {
			level,
			type
		};
	};

	const handleAvatarError = e => {
		e.target.src = defaultAvatar;
	};

	const globalComments = computed(() => {
		return comments.value.filter(comment => comment.link === -1);
	});

	const getStandpointColor = comment => {
		return (
			{
				1: "#ccebc5",
				[-1]: "#fbb4ae",
				0: "#b3cde3"
			}[comment.standpoint] || "#9E9E9E"
		);
	};

	const getEmotionColor = comment => {
		return (
			{
				1: "#4daf4a",
				[-1]: "#e41a1c",
				0: "#377eb8"
			}[comment.emotion] || "#9E9E9E"
		);
	};

	const getStandpointLabel = comment => {
		return (
			{
				1: "支持",
				[-1]: "反对",
				0: "中立"
			}[comment.standpoint] || "未知"
		);
	};

	const getEmotionLabel = comment => {
		return (
			{
				1: "积极",
				[-1]: "消极",
				0: "中立"
			}[comment.emotion] || "未知"
		);
	};

	watch(activeSentence, updateConnectionLine);

	onMounted(() => {
		api.get("article", {}, data => {
			article.value = data[0];
			sentences.value = splitIntoSentences(data[0].content_text);
		});

		api.get("comments", {}, data => {
			comments.value = data;
		});

		window.addEventListener("resize", updateConnectionLine);
		window.addEventListener("scroll", updateConnectionLine, true);
	});
</script>

<style scoped>
	.article-container {
		display: flex;
		flex-direction: column;
		max-width: 1800px;
		margin: 0 auto;
		padding: 20px;
		position: relative;
		gap: 15px;
	}

	.control-panel {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 15px;
		padding: 12px 15px;
		background: white;
		border-radius: 8px;
		box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
		width: 100%;
		flex-wrap: wrap;
	}

	.control-group-container {
		display: flex;
		gap: 15px;
	}

	.control-group {
		display: flex;
		align-items: center;
		gap: 6px;
	}

	.icon-toggle {
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		padding: 8px;
		border-radius: 4px;
		transition: all 0.2s;
	}

	.icon-toggle:hover {
		background-color: #f0f0f0;
	}

	.icon-toggle svg {
		opacity: 0.7;
		transition: all 0.2s;
	}

	.icon-toggle input[type="checkbox"] {
		position: absolute;
		opacity: 0;
		width: 0;
		height: 0;
	}

	.icon-toggle input[type="checkbox"]:checked + svg {
		opacity: 1;
		color: #0084ff;
	}

	.control-label {
		font-size: 14px;
		color: #555;
		white-space: nowrap;
	}

	.legend-section {
		display: flex;
		gap: 15px;
		align-items: center;
		flex-wrap: wrap;
	}

	.comment-type-legend {
		display: flex;
		gap: 10px;
		align-items: center;
		flex-wrap: wrap;
		padding: 8px 12px;
		background: white;
		border-radius: 6px;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
	}

	.legend-item {
		background: none;
		border: none;
		padding: 4px 8px;
		cursor: pointer;
		border-radius: 4px;
		transition: all 0.2s;
		display: flex;
		align-items: center;
	}

	.legend-item:hover {
		background-color: #f5f5f5;
	}

	.legend-item.active {
		background-color: #e3f2fd;
	}

	.chart-legend {
		background: white;
		padding: 8px 12px;
		border-radius: 6px;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
	}

	/* 陈述样式 - 蓝色波浪线 */
	.underline.blue {
		color: #4285f4;
		text-decoration: blue wavy underline;
	}

	/* 疑问样式 - 红色圆圈 */
	.circle.red {
		color: #ea4335;
		outline: 2px solid #ea4335;
		border-radius: 50%;
		padding: 0 2px;
	}

	/* 感叹样式 - 绿色双下划线 */
	.double-underline.green {
		color: #34a853;
		text-decoration: green double underline;
	}

	/* 建议样式 - 紫色实线下划线 */
	.solid-underline.purple {
		color: #9c27b0;
		text-decoration: purple solid underline;
	}

	/* 讽刺样式 - 橙色圆角矩形框 */
	.rounded-box.orange {
		color: #ff6d00;
		outline: 2px solid #ff6d00;
		border-radius: 4px;
		padding: 0 2px;
	}

	.main-content {
		display: grid;
		grid-template-columns: 300px minmax(0, 1fr) 400px;
		gap: 20px;
		width: 100%;
	}

	.panel {
		background: white;
		border-radius: 8px;
		box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
		padding: 15px;
		height: fit-content;
		max-height: calc(100vh - 180px);
		overflow-y: auto;
	}

	.article-panel {
		position: sticky;
		top: 120px;
		max-height: calc(100vh - 140px);
	}

	.panel-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 12px;
		padding-bottom: 8px;
		border-bottom: 1px solid #eee;
	}

	.panel-header h4 {
		margin: 0;
		font-size: 16px;
		color: #333;
	}

	.panel-content {
		display: flex;
		flex-direction: column;
		gap: 12px;
	}

	.comment-item,
	.annotation-item {
		padding: 12px;
		background: #f9f9f9;
		border-radius: 6px;
		border-top: 1px solid #eee;
		border-bottom: 1px solid #eee;
		border-left: 4px solid transparent;
		border-right: 4px solid transparent;
		margin-bottom: 12px;
		transition: all 0.2s ease;
		position: relative;
	}

	.comment-item:hover,
	.annotation-item:hover {
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
		transform: translateY(-2px);
	}

	.comment-user,
	.annotation-user {
		display: flex;
		align-items: center;
		margin-bottom: 8px;
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

	.comment-text,
	.annotation-text {
		font-size: 14px;
		line-height: 1.5;
		color: #333;
	}

	.comment-stats,
	.annotation-stats {
		display: flex;
		align-items: center;
		gap: 12px;
		margin-top: 8px;
		font-size: 12px;
		color: #999;
	}

	.like-count,
	.reply-count {
		display: flex;
		align-items: center;
		gap: 4px;
	}

	.like-count .icon {
		color: #ff4757;
	}

	.reply-count .icon {
		color: #57606f;
	}

	.close-btn {
		background: none;
		border: none;
		font-size: 20px;
		cursor: pointer;
		color: #999;
		transition: color 0.2s;
	}

	.close-btn:hover {
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
		position: relative;
		white-space: pre-wrap;
		word-wrap: break-word;
	}

	.sentence {
		display: inline;
		margin-right: 0.2em;
		position: relative;
		transition: all 0.2s;
		padding: 0 1px;
		cursor: pointer;
	}

	.sentence.selected {
		background-color: rgba(255, 236, 179, 0.4);
	}

	.sentence.comment-level-1 {
		background-color: rgba(255, 236, 179, 0.2);
	}
	.sentence.comment-level-2 {
		background-color: rgba(255, 236, 179, 0.4);
	}
	.sentence.comment-level-3 {
		background-color: rgba(255, 236, 179, 0.6);
	}
	.sentence.comment-level-4 {
		background-color: rgba(255, 236, 179, 0.8);
	}
	.sentence.comment-level-5 {
		background-color: rgba(255, 236, 179, 1);
	}

	/* 句子上的评论类型标注样式 */
	.sentence.comment-type-1 {
		text-decoration: blue wavy underline;
	}

	.sentence.comment-type-2 {
		outline: 2px solid red;
		border-radius: 50%;
		padding: 0 2px;
	}

	.sentence.comment-type-3 {
		text-decoration: green double underline;
	}

	.sentence.comment-type-4 {
		text-decoration: purple solid underline;
	}

	.sentence.comment-type-5 {
		outline: 2px solid orange;
		border-radius: 4px;
		padding: 0 2px;
	}

	.annotation-marker {
		color: #ff9800;
		font-size: 0.8em;
		vertical-align: super;
		margin-left: 2px;
	}

	.before-stats {
		display: inline-flex;
		vertical-align: middle;
		margin-right: 4px;
		transform: translateY(-1px);
	}

	.after-stats {
		display: inline-flex;
		vertical-align: middle;
		margin-left: 4px;
		transform: translateY(-1px);
	}

	.inline-comment {
		display: inline;
		font-size: 0.85em;
		margin-left: 0.5em;
	}

	.inline-comment.comment-type-1 {
		color: #4285f4;
	}

	.inline-comment.comment-type-2 {
		color: #ea4335;
	}

	.inline-comment.comment-type-3 {
		color: #34a853;
	}

	.inline-comment.comment-type-4 {
		color: #9c27b0;
	}

	.inline-comment.comment-type-5 {
		color: #ff6d00;
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
		transition: opacity 0.2s;
	}

	.original-link:hover {
		opacity: 0.8;
	}

	.connection-container {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		pointer-events: none;
		z-index: 10;
		overflow: visible;
	}

	.connection-line {
		position: absolute;
		height: 2px;
		background: transparent;
		filter: drop-shadow(0 0 2px rgba(255, 87, 34, 0.5));
	}

	@media (max-width: 1400px) {
		.main-content {
			grid-template-columns: 250px minmax(0, 1fr) 350px;
		}
	}

	@media (max-width: 1200px) {
		.control-panel {
			flex-direction: column;
			align-items: stretch;
		}

		.legend-section {
			width: 100%;
			justify-content: center;
			margin-top: 10px;
		}

		.main-content {
			grid-template-columns: 1fr 1fr;
			grid-template-areas:
				"article article"
				"global annotation";
		}

		.article-panel {
			grid-area: article;
		}

		.global-comments-panel {
			grid-area: global;
		}

		.annotation-panel {
			grid-area: annotation;
		}
	}

	@media (max-width: 768px) {
		.control-group-container {
			flex-wrap: wrap;
			justify-content: center;
		}

		.comment-type-legend {
			gap: 8px;
		}

		.legend-item {
			font-size: 13px;
		}

		.main-content {
			grid-template-columns: 1fr;
			grid-template-areas:
				"article"
				"global"
				"annotation";
		}
	}

	.panel {
		scrollbar-width: none;
		-ms-overflow-style: none;
	}

	.panel::-webkit-scrollbar {
		display: none;
	}
</style>
