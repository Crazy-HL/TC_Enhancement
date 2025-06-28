<template>
	<div
		class="danmu-container"
		ref="danmuContainer"
		:style="{
			'--container-height': `${maxLines * lineHeight + 20}px`,
			'--line-height': `${lineHeight}px`,
			'--card-width': `${cardWidth}px`,
			'--text-font-size': `${textFontSize}px`,
			'--card-font-size': `${cardFontSize}px`,
			'--opacity': `${opacity / 100}`
		}">
		<!-- 文本样式弹幕 -->
		<template v-if="styleType === 'text'">
			<div
				v-for="danmu in visibleDanmus"
				:key="danmu.id"
				class="danmu-item danmu-text"
				:style="{
					top: `${danmu.top}px`,
					'animation-duration': `${danmu.speed}s`,
					color: danmu.color,
					'font-size': 'var(--text-font-size)'
				}"
				@animationend="removeDanmu(danmu.id)">
				{{ danmu.user }}：{{ danmu.content }}
			</div>
		</template>

		<!-- 卡片样式弹幕 -->
		<template v-else>
			<div
				v-for="danmu in visibleDanmus"
				:key="danmu.id"
				class="danmu-item danmu-card"
				:style="{
					top: `${danmu.top}px`,
					'animation-duration': `${danmu.speed}s`,
					width: 'var(--card-width)'
				}"
				@animationend="removeDanmu(danmu.id)">
				<div class="danmu-card-content">
					<div class="danmu-user" v-if="showAvatars">
						<img
							:src="danmu.avatar"
							class="avatar"
							@error="handleAvatarError" />
						<span class="username">{{ danmu.user }}</span>
					</div>
					<div class="danmu-text">{{ danmu.content }}</div>
				</div>
			</div>
		</template>
	</div>
</template>

<script setup>
	import { ref, computed, watch, onMounted } from "vue";

	const props = defineProps({
		comments: Array,
		activeSentence: Number,
		maxLines: {
			type: Number,
			default: 3,
			validator: value => value >= 1 && value <= 8
		},
		lineHeight: {
			type: Number,
			default: 80,
			validator: value => value >= 40 && value <= 120
		},
		maxDanmus: {
			type: Number,
			default: 5,
			validator: value => value >= 1 && value <= 15
		},
		baseSpeed: {
			type: Number,
			default: 10,
			validator: value => value >= 5 && value <= 30
		},
		styleType: {
			type: String,
			default: "text",
			validator: value => ["text", "card"].includes(value)
		},
		cardWidth: {
			type: Number,
			default: 280,
			validator: value => value >= 200 && value <= 400
		},
		textFontSize: {
			type: Number,
			default: 16,
			validator: value => value >= 12 && value <= 24
		},
		cardFontSize: {
			type: Number,
			default: 14,
			validator: value => value >= 12 && value <= 20
		},
		opacity: {
			type: Number,
			default: 85,
			validator: value => value >= 30 && value <= 100
		},
		showAvatars: {
			type: Boolean,
			default: true
		}
	});

	// 默认头像
	const defaultAvatar =
		"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iI2NjYyIgZD0iTTEyLDJBMTAsMTAgMCAwLDAgMiwxMkExMCwxMCAwIDAsMCAxMiwyMkExMCwxMCAwIDAsMCAyMiwxMkExMCwxMCAwIDAsMCAxMiwyTTEyLDRBNyA3IDAgMCwxIDE5LDExQTcgNyAwIDAsMSAxMiwxOEE3LDcgMCAwLDEgNSwxMUE3LDcgMCAwLDEgMTIsNE0xMiw2QTUsNSAwIDAsMCA3LDExQTUsNSAwIDAsMCAxMiwxNkE1LDUgMCAwLDAgMTcsMTFBNSw1IDAgMCwwIDEyLDZNMTIsOEEzLDMgMCAwLDEgMTUsMTFBNCw0IDAgMCwxIDEyLDE1QTQsNCAwIDAsMSA5LDExQTMsMyAwIDAsMSAxMiw4WiIvPjwvc3ZnPg==";

	// 弹幕数据
	const danmuContainer = ref(null);
	const allDanmus = ref([]);
	const lineOccupancy = ref([]);

	// 计算可见弹幕
	const visibleDanmus = computed(() => {
		cleanExpiredDanmus();
		return allDanmus.value.slice(-props.maxDanmus * 2);
	});

	// 获取随机颜色
	const getRandomColor = () => {
		const colors = [
			"#FF6B6B",
			"#4ECDC4",
			"#45B7D1",
			"#FFA07A",
			"#98D8C8",
			"#F06292",
			"#7986CB",
			"#9575CD",
			"#64B5F6",
			"#4DB6AC",
			"#81C784",
			"#FFD54F"
		];
		return colors[Math.floor(Math.random() * colors.length)];
	};

	// 获取相关评论
	const getCommentsForSentence = sentenceIndex => {
		return (
			props.comments?.filter(comment => comment.link === sentenceIndex) || []
		);
	};

	// 计算弹幕速度
	const calculateSpeed = text => {
		const baseSpeed = props.baseSpeed;
		const lengthFactor = Math.min(text.length / 50, 2);
		return baseSpeed + Math.random() * 5 * lengthFactor;
	};

	// 分配弹幕行（修复显示不全问题）
	const assignDanmuLine = () => {
		const now = Date.now();
		const availableLines = [];

		// 找出可用的行
		for (let i = 0; i < props.maxLines; i++) {
			if (!lineOccupancy.value[i] || lineOccupancy.value[i] < now) {
				availableLines.push(i);
			}
		}

		if (availableLines.length > 0) {
			const lineIndex =
				availableLines[Math.floor(Math.random() * availableLines.length)];
			return {
				lineIndex,
				top: lineIndex * props.lineHeight + 10
			};
		}

		// 没有可用行时选择最久未使用的行
		let oldestLine = 0;
		let oldestTime = Infinity;
		for (let i = 0; i < props.maxLines; i++) {
			if (lineOccupancy.value[i] < oldestTime) {
				oldestTime = lineOccupancy.value[i];
				oldestLine = i;
			}
		}
		return {
			lineIndex: oldestLine,
			top: oldestLine * props.lineHeight + 10
		};
	};

	// 生成弹幕
	const generateDanmus = () => {
		if (props.activeSentence === null || !props.comments) return;

		const relatedComments = getCommentsForSentence(props.activeSentence);
		if (relatedComments.length === 0) return;

		// 限制弹幕数量
		const commentsToShow = relatedComments.slice(0, props.maxDanmus);

		commentsToShow.forEach(comment => {
			const { lineIndex, top } = assignDanmuLine();
			const speed = calculateSpeed(comment.content);

			// 记录行占用时间（动画结束后释放）
			lineOccupancy.value[lineIndex] = Date.now() + speed * 1000;

			allDanmus.value.push({
				id: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
				content: comment.content,
				user: comment.user_nickname || "匿名用户",
				avatar: comment.user_avatar || defaultAvatar,
				color: getRandomColor(),
				top: top,
				speed: speed,
				createTime: Date.now()
			});
		});
	};

	// 移除弹幕
	const removeDanmu = id => {
		allDanmus.value = allDanmus.value.filter(danmu => danmu.id !== id);
	};

	// 清理过期弹幕
	const cleanExpiredDanmus = () => {
		const now = Date.now();
		allDanmus.value = allDanmus.value.filter(danmu => {
			return now - danmu.createTime < danmu.speed * 1000 * 1.5;
		});
	};

	// 处理头像错误
	const handleAvatarError = e => {
		e.target.src = defaultAvatar;
	};

	// 监听激活句子变化
	watch(
		() => props.activeSentence,
		newVal => {
			if (newVal !== null) {
				generateDanmus();
			}
		}
	);

	// 监听样式变化重置
	watch(
		() => props.styleType,
		() => {
			allDanmus.value = [];
			lineOccupancy.value = Array(props.maxLines).fill(0);
		}
	);

	// 初始化
	onMounted(() => {
		lineOccupancy.value = Array(props.maxLines).fill(0);
	});
</script>

<style scoped>
	.danmu-container {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: var(--container-height);
		overflow: visible;
		z-index: 100;
		pointer-events: none;
	}

	.danmu-item {
		position: absolute;
		left: 100%;
		transform: translateX(0);
		will-change: transform;
		animation: danmu-move linear forwards;
		opacity: var(--opacity);
	}

	/* 文本样式弹幕 */
	.danmu-text {
		font-size: var(--text-font-size);
		padding: 0 15px;
		border-radius: calc(var(--line-height) / 2);
		background-color: rgba(255, 255, 255, 0.85);
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
		text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
		height: var(--line-height);
		line-height: var(--line-height);
		white-space: nowrap;
		display: inline-block;
	}

	/* 卡片样式弹幕 */
	.danmu-card {
		background: white;
		border-radius: 8px;
		box-shadow: 0 3px 12px rgba(0, 0, 0, 0.15);
		overflow: hidden;
		width: var(--card-width);
		min-height: var(--line-height);
	}

	.danmu-card-content {
		padding: 12px;
	}

	.danmu-user {
		display: flex;
		align-items: center;
		margin-bottom: 8px;
	}

	.danmu-user .avatar {
		width: calc(var(--line-height) - 20px);
		height: calc(var(--line-height) - 20px);
		border-radius: 50%;
		margin-right: 10px;
		object-fit: cover;
		background-color: #f0f0f0;
	}

	.danmu-user .username {
		font-weight: bold;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
		font-size: var(--card-font-size);
	}

	.danmu-card .danmu-text {
		line-height: 1.5;
		white-space: normal;
		word-break: break-word;
		display: block;
		padding: 5px 0;
		font-size: var(--card-font-size);
	}

	@keyframes danmu-move {
		to {
			transform: translateX(calc(-100vw - var(--card-width, 0px)));
		}
	}
</style>
