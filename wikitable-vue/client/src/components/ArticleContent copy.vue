<template>
	<div class="article-container" v-if="article">
		<h1 class="article-title">{{ article.title }}</h1>

		<div class="article-meta">
			<span class="author">作者: {{ article.user_nickname }}</span>
			<span class="publish-time"
				>发布时间: {{ formatTime(article.created_time) }}</span
			>
			<span class="update-time"
				>更新时间: {{ formatTime(article.updated_time) }}</span
			>
		</div>

		<div class="article-content" v-html="article.content_text"></div>

		<div class="article-footer">
			<div class="stats">
				<span class="vote-count">点赞: {{ article.voteup_count }}</span>
				<span class="comment-count">评论: {{ article.comment_count }}</span>
			</div>
			<a :href="article.content_url" target="_blank" class="original-link"
				>原文链接</a
			>
		</div>
	</div>
</template>

<script setup>
	import { ref, onMounted } from "vue";
	import api from "@/api";

	const article = ref(null);
	const formatTime = time => {
		if (!time) return "";
		const date = new Date(time * 1000);
		return date.toLocaleString(); // 可自定义格式
	};
	onMounted(() => {
		api.get("article", {}, data => {
			article.value = data[0];
			console.log("content:", data[0]);
		});
	});
</script>

<style scoped>
	.article-container {
		max-width: 800px;
		margin: 0 auto;
		padding: 20px;
		background: #fff;
		border-radius: 8px;
		box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
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
</style>
