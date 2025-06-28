<template>
	<div class="comment-section">
		<h2 class="comment-title">评论 ({{ comments.length }})</h2>

		<div class="comment-list">
			<div
				v-for="comment in comments"
				:key="comment.comment_id"
				class="comment-card">
				<div class="comment-header">
					<img
						:src="comment.user_avatar || 'default-avatar.png'"
						:alt="comment.user_nickname"
						class="avatar" />
					<div class="user-info">
						<a :href="comment.user_link" target="_blank" class="username">{{
							comment.user_nickname
						}}</a>
						<span class="comment-time">{{
							formatTime(comment.publish_time)
						}}</span>
					</div>
				</div>

				<div class="comment-content">{{ comment.content }}</div>

				<div class="comment-footer">
					<span class="like-count">点赞: {{ comment.like_count }}</span>
					<!-- <span class="reply-btn">回复</span> -->
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { ref, onMounted } from "vue";
	import api from "@/api";

	const comments = ref([]);

	const formatTime = time => {
		if (!time) return "";
		const date = new Date(time * 1000);
		return date.toLocaleString(); // 可自定义格式
	};

	onMounted(() => {
		api.get("comments", {}, data => {
			comments.value = data;
		});
	});
</script>

<style scoped>
	.comment-section {
		max-width: 800px;
		margin: 20px auto;
		padding: 20px;
		background: #fff;
		border-radius: 8px;
		box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
	}

	.comment-title {
		font-size: 20px;
		margin-bottom: 20px;
		color: #333;
		padding-bottom: 10px;
		border-bottom: 1px solid #eee;
	}

	.comment-list {
		display: flex;
		flex-direction: column;
		gap: 20px;
	}

	.comment-card {
		padding: 15px;
		border-radius: 6px;
		background: #f9f9f9;
		border: 1px solid #eee;
	}

	.comment-header {
		display: flex;
		align-items: center;
		margin-bottom: 10px;
	}

	.avatar {
		width: 40px;
		height: 40px;
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
	}

	.comment-footer {
		display: flex;
		justify-content: space-between;
		align-items: center;
		font-size: 14px;
		color: #666;
	}

	.like-count {
		color: #666;
	}

	.reply-btn {
		color: #0084ff;
		cursor: pointer;
	}

	.reply-btn:hover {
		text-decoration: underline;
	}
</style>
