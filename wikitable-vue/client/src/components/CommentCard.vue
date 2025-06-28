<template>
	<div
		class="comment-card"
		:class="position"
		@mouseenter="handleMouseEnter"
		@mouseleave="handleMouseLeave">
		<div class="comment-header">
			<img
				:src="comment.user_avatar || 'default-avatar.png'"
				:alt="comment.user_nickname"
				class="avatar" />
			<div class="user-info">
				<a :href="comment.user_link" target="_blank" class="username">{{
					comment.user_nickname
				}}</a>
				<span class="comment-time">{{ formatTime(comment.publish_time) }}</span>
			</div>
		</div>

		<div class="comment-content">{{ comment.content }}</div>

		<div class="comment-footer">
			<span class="like-count">点赞: {{ comment.like_count }}</span>
		</div>

		<div class="comment-connector" v-if="isHovered"></div>
	</div>
</template>

<script setup>
	import { ref } from "vue";

	const props = defineProps({
		comment: {
			type: Object,
			required: true
		},
		position: {
			type: String,
			default: "left",
			validator: value => ["left", "right"].includes(value)
		}
	});

	const emit = defineEmits(["highlight"]);

	const isHovered = ref(false);

	const formatTime = time => {
		if (!time) return "";
		const date = new Date(time * 1000);
		return date.toLocaleString();
	};

	const handleMouseEnter = () => {
		isHovered.value = true;
		if (props.comment.target_text) {
			emit("highlight", props.comment.target_text);
		}
	};

	const handleMouseLeave = () => {
		isHovered.value = false;
	};
</script>

<style scoped>
	.comment-card {
		padding: 15px;
		border-radius: 6px;
		background: #f9f9f9;
		border: 1px solid #eee;
		margin-bottom: 15px;
		position: relative;
		transition: all 0.2s ease;
	}

	.comment-card.left {
		margin-right: 20px;
	}

	.comment-card.right {
		margin-left: 20px;
	}

	.comment-card:hover {
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
		transform: translateY(-2px);
	}

	.comment-header {
		display: flex;
		align-items: center;
		margin-bottom: 10px;
	}

	.avatar {
		width: 32px;
		height: 32px;
		border-radius: 50%;
		margin-right: 10px;
		object-fit: cover;
	}

	.user-info {
		display: flex;
		flex-direction: column;
	}

	.username {
		font-weight: bold;
		font-size: 14px;
		color: #333;
		text-decoration: none;
	}

	.username:hover {
		color: #0084ff;
	}

	.comment-time {
		font-size: 12px;
		color: #999;
	}

	.comment-content {
		margin-bottom: 10px;
		line-height: 1.6;
		color: #333;
		font-size: 14px;
	}

	.comment-footer {
		display: flex;
		justify-content: space-between;
		align-items: center;
		font-size: 12px;
		color: #666;
	}

	.comment-connector {
		position: absolute;
		top: 50%;
		width: 50px;
		height: 2px;
		background: #0084ff;
	}

	.comment-connector::after {
		content: "";
		position: absolute;
		width: 6px;
		height: 6px;
		border-radius: 50%;
		background: #0084ff;
		top: -2px;
	}

	.left .comment-connector {
		right: -50px;
	}

	.left .comment-connector::after {
		right: 0;
	}

	.right .comment-connector {
		left: -50px;
	}

	.right .comment-connector::after {
		left: 0;
	}
</style>
